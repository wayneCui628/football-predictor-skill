import sys
import argparse
import math
import numpy as np
from scipy.stats import poisson

# ============================================================
# DYNAMIC PARAMETER DERIVATION
# Instead of hardcoded lookup tables, rho and home_adv are
# computed from real-time league statistics that the LLM
# searches for at prediction time.
# ============================================================

def derive_rho(league_avg_goals):
    """
    Derive the Dixon-Coles rho parameter from the league's
    average goals per game this season.
    
    Logic: Lower-scoring leagues have more 0-0 / 1-1 draws,
    requiring a more negative rho to correct the Poisson model.
    
    Calibrated against published research values:
      avg 3.0 goals -> rho ~ -0.04 (high-scoring, minimal correction)
      avg 2.7 goals -> rho ~ -0.13 (typical EPL)
      avg 2.3 goals -> rho ~ -0.25 (defensive league)
    """
    rho = -0.04 - 0.30 * (3.0 - league_avg_goals)
    return round(max(-0.30, min(-0.02, rho)), 3)

def derive_home_adv(league_home_goals_avg, league_away_goals_avg):
    """
    Derive the home advantage multiplier from the league's
    actual home vs away goal averages this season.
    
    Formula: home_adv = home_avg / overall_per_team_avg
    
    Example: home_avg=1.55, away_avg=1.20
      overall = (1.55 + 1.20) / 2 = 1.375
      home_adv = 1.55 / 1.375 = 1.127
    """
    overall = (league_home_goals_avg + league_away_goals_avg) / 2
    if overall <= 0:
        return 1.08  # Safety fallback
    ha = league_home_goals_avg / overall
    return round(max(1.0, min(1.25, ha)), 3)

# Venue context applied ON TOP of derived home_adv
VENUE_MULTIPLIER = {
    "home":        lambda ha: ha,           # Normal home advantage
    "away":        lambda ha: 2.0 - ha,     # Mirror (e.g., 1.08 -> 0.92)
    "neutral":     lambda ha: 1.0,          # No advantage
    "host_nation": lambda ha: max(ha, 1.15), # Host nation: at least 1.15
}

# FALLBACK defaults (only used if LLM fails to provide league stats)
FALLBACK_RHO = -0.13
FALLBACK_HOME_ADV = 1.08

def rho_correction(x, y, lambda_x, mu_y, rho):
    """
    Dixon-Coles tau adjustment for low-scoring outcomes.
    Breaks the independence assumption to better model 0-0, 1-0, 0-1, 1-1.
    """
    if x == 0 and y == 0:
        return 1.0 - (lambda_x * mu_y * rho)
    elif x == 0 and y == 1:
        return 1.0 + (lambda_x * rho)
    elif x == 1 and y == 0:
        return 1.0 + (mu_y * rho)
    elif x == 1 and y == 1:
        return 1.0 - rho
    else:
        return 1.0

def simulate_match(home_xg, away_xg, home_xga, away_xga,
                   venue="home",
                   league_avg_goals=0.0, league_home_goals_avg=0.0, league_away_goals_avg=0.0,
                   ref_penalty_boost=0.0,
                   home_missing_xg_pct=0.0, away_missing_xg_pct=0.0,
                   strength_mod_home=0.0, strength_mod_away=0.0):
    """
    Dixon-Coles Poisson Engine v3.0
    Full-spectrum quantitative prediction with dynamically derived parameters.
    """
    # 1. Derive rho and home_adv from real league data (or use fallback)
    if league_avg_goals > 0:
        rho = derive_rho(league_avg_goals)
    else:
        rho = FALLBACK_RHO
    
    if league_home_goals_avg > 0 and league_away_goals_avg > 0:
        base_ha = derive_home_adv(league_home_goals_avg, league_away_goals_avg)
    else:
        base_ha = FALLBACK_HOME_ADV
    
    # 2. Apply venue context
    venue_fn = VENUE_MULTIPLIER.get(venue, VENUE_MULTIPLIER["home"])
    effective_ha = venue_fn(base_ha)
    effective_da = 2.0 - effective_ha  # Disadvantage is the mirror
    
    # 3. Apply missing player xG reduction (capped at 30% max impact)
    home_missing_factor = 1.0 - min(home_missing_xg_pct * 0.6, 0.30)
    away_missing_factor = 1.0 - min(away_missing_xg_pct * 0.6, 0.30)
    
    # 4. Apply multi-dimensional strength modifier (from run_pipeline.py)
    home_strength = 1.0 + strength_mod_home
    away_strength = 1.0 + strength_mod_away
    
    # 5. Calculate final goal expectancy
    home_expectancy = ((home_xg + away_xga) / 2) * effective_ha * home_missing_factor * home_strength + ref_penalty_boost
    away_expectancy = ((away_xg + home_xga) / 2) * effective_da * away_missing_factor * away_strength + ref_penalty_boost
    
    # Ensure non-negative
    home_expectancy = max(0.1, home_expectancy)
    away_expectancy = max(0.1, away_expectancy)
    
    # 6. Build Dixon-Coles adjusted probability matrix
    max_goals = 8
    matrix = np.zeros((max_goals + 1, max_goals + 1))
    
    home_win_prob = 0.0
    draw_prob = 0.0
    away_win_prob = 0.0
    
    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            base_prob = poisson.pmf(i, home_expectancy) * poisson.pmf(j, away_expectancy)
            tau = rho_correction(i, j, home_expectancy, away_expectancy, rho)
            adjusted_prob = max(0, base_prob * tau)
            matrix[i][j] = adjusted_prob
            
            if i > j:
                home_win_prob += adjusted_prob
            elif i == j:
                draw_prob += adjusted_prob
            else:
                away_win_prob += adjusted_prob
                
    # Normalize
    total_prob = home_win_prob + draw_prob + away_win_prob
    home_win_prob = (home_win_prob / total_prob) * 100
    draw_prob = (draw_prob / total_prob) * 100
    away_win_prob = (away_win_prob / total_prob) * 100
    matrix = matrix / total_prob
    
    return matrix, home_win_prob, draw_prob, away_win_prob, home_expectancy, away_expectancy, rho, effective_ha

def print_report(args):
    matrix, home_win, draw, away_win, h_exp, a_exp, rho, eff_ha = simulate_match(
        args.home_xg, args.away_xg, args.home_xga, args.away_xga,
        venue=args.venue,
        league_avg_goals=args.league_avg_goals,
        league_home_goals_avg=args.league_home_goals_avg,
        league_away_goals_avg=args.league_away_goals_avg,
        ref_penalty_boost=args.ref_penalty_boost,
        home_missing_xg_pct=args.home_missing_xg_pct,
        away_missing_xg_pct=args.away_missing_xg_pct,
        strength_mod_home=args.strength_mod_home,
        strength_mod_away=args.strength_mod_away,
    )
    
    print("=" * 60)
    print(f"DIXON-COLES POISSON ENGINE v3.0 (Industrial Grade)")
    print(f"Match: {args.home} (Home) vs {args.away} (Away)")
    print("-" * 60)
    print(f"Venue: {args.venue}")
    if args.league_avg_goals > 0:
        print(f"League Stats: Avg Goals/Game={args.league_avg_goals:.2f}, Home Avg={args.league_home_goals_avg:.2f}, Away Avg={args.league_away_goals_avg:.2f}")
        print(f"Derived Rho (ρ): {rho} | Derived Home Adv: x{eff_ha:.3f}")
    else:
        print(f"Fallback Rho (ρ): {rho} | Fallback Home Adv: x{eff_ha:.3f}")
    if args.ref_penalty_boost > 0:
        print(f"Referee xG Boost (each team): +{args.ref_penalty_boost:.3f}")
    if args.home_missing_xg_pct > 0:
        print(f"{args.home} Missing Player xG Share: {args.home_missing_xg_pct*100:.1f}%")
    if args.away_missing_xg_pct > 0:
        print(f"{args.away} Missing Player xG Share: {args.away_missing_xg_pct*100:.1f}%")
    if args.strength_mod_home != 0 or args.strength_mod_away != 0:
        print(f"Strength Modifier: {args.home} {args.strength_mod_home:+.3f} | {args.away} {args.strength_mod_away:+.3f}")
    print(f"Adjusted Expectancy: {args.home} ({h_exp:.2f}) - {args.away} ({a_exp:.2f})")
    print("=" * 60)
    
    print(f"\n[MATCH OUTCOME PROBABILITIES (90 mins)]")
    print(f"{args.home} Win: {home_win:.1f}%")
    print(f"Draw: {draw:.1f}%")
    print(f"{args.away} Win: {away_win:.1f}%")
    
    print(f"\n[MOST LIKELY EXACT SCORELINES]")
    scorelines = []
    for i in range(6):
        for j in range(6):
            scorelines.append(((i, j), matrix[i][j] * 100))
    scorelines.sort(key=lambda x: x[1], reverse=True)
    
    for i in range(5):
        score, prob = scorelines[i]
        print(f"{score[0]} - {score[1]} : {prob:.1f}%")
    
    print("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dixon-Coles Poisson Engine v3.0")
    parser.add_argument("--home", required=True)
    parser.add_argument("--away", required=True)
    parser.add_argument("--home-xg", type=float, required=True)
    parser.add_argument("--away-xg", type=float, required=True)
    parser.add_argument("--home-xga", type=float, required=True)
    parser.add_argument("--away-xga", type=float, required=True)
    
    # Dynamic league stats (for deriving rho and home_adv)
    parser.add_argument("--league-avg-goals", type=float, default=0.0,
                        help="League average total goals per game this season (e.g., 2.75)")
    parser.add_argument("--league-home-goals-avg", type=float, default=0.0,
                        help="League average goals scored by home teams per game (e.g., 1.55)")
    parser.add_argument("--league-away-goals-avg", type=float, default=0.0,
                        help="League average goals scored by away teams per game (e.g., 1.20)")
    parser.add_argument("--venue", type=str, default="home",
                        help="Venue type: home, away, neutral, host_nation")
    
    # Quantifiable modifiers
    parser.add_argument("--ref-penalty-boost", type=float, default=0.0,
                        help="xG boost from referee penalty tendency (e.g., 0.11)")
    parser.add_argument("--home-missing-xg-pct", type=float, default=0.0,
                        help="Fraction of home team xG from injured/suspended players (e.g., 0.25 for 25%)")
    parser.add_argument("--away-missing-xg-pct", type=float, default=0.0,
                        help="Fraction of away team xG from injured/suspended players (e.g., 0.15 for 15%)")
    parser.add_argument("--strength-mod-home", type=float, default=0.0,
                        help="Composite strength modifier for home team (from run_pipeline.py)")
    parser.add_argument("--strength-mod-away", type=float, default=0.0,
                        help="Composite strength modifier for away team (from run_pipeline.py)")
    
    args = parser.parse_args()
    print_report(args)
