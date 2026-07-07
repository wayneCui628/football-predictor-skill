import sys
import argparse
import subprocess
import os
import math

def parse_and_weighted_average(data_string, default_val, xi=0.3, min_val=0.0, max_val=100.0):
    """
    Parse comma-separated values and compute a TIME-DECAY WEIGHTED average.
    Values are assumed to be in chronological order (most recent LAST).
    Uses exponential decay: w_i = exp(-xi * i) where i=0 is the most recent.
    Enforces min/max boundaries to prevent LLM hallucination skew.
    """
    if not data_string or data_string.lower() in ['none', 'null', 'n/a', '']:
        return default_val
    try:
        vals = [float(v.strip()) for v in data_string.split(',') if v.strip()]
        if not vals:
            return default_val
        
        # Clamp inputs to bounds to prevent extreme hallucinations (e.g. 820% possession)
        vals = [max(min_val, min(max_val, v)) for v in vals]
        
        # Reverse so index 0 = most recent match
        vals.reverse()
        
        # Compute exponential decay weights
        weights = [math.exp(-xi * i) for i in range(len(vals))]
        
        # Weighted average
        weighted_sum = sum(v * w for v, w in zip(vals, weights))
        total_weight = sum(weights)
        
        return round(weighted_sum / total_weight, 2)
    except Exception as e:
        print(f"Warning: Could not parse '{data_string}'. Using default {default_val}. Error: {e}")
        return default_val

def compute_strength_modifier(poss, pass_acc, ppda, duel, sca, progp):
    """
    Convert 6 auxiliary dimensions into a single Composite Strength Modifier.
    Returns a value between -0.15 and +0.15 that adjusts the team's xG expectancy.
    
    Weights reflect each dimension's empirical correlation with goal creation:
    - SCA (Shot-Creating Actions): highest weight, directly tied to chances
    - PPDA (Passes Per Defensive Action): high weight, measures pressing intensity
    - ProgP (Progressive Passes): measures attacking transitions
    - Possession: moderate, controls tempo
    - Pass Accuracy: moderate, sustains attacks
    - Duel Success: lower, more defensive metric
    """
    baselines = {
        'poss': 50.0, 'pass_acc': 82.0, 'ppda': 12.0,
        'duel': 50.0, 'sca': 25.0, 'progp': 40.0
    }
    weights = {
        'poss': 0.15, 'pass_acc': 0.10, 'ppda': 0.20,
        'duel': 0.10, 'sca': 0.25, 'progp': 0.20
    }
    
    deltas = {
        'poss':     (poss - baselines['poss']) / baselines['poss'],
        'pass_acc': (pass_acc - baselines['pass_acc']) / baselines['pass_acc'],
        'ppda':     (baselines['ppda'] - ppda) / baselines['ppda'],  # Inverted: lower = better
        'duel':     (duel - baselines['duel']) / baselines['duel'],
        'sca':      (sca - baselines['sca']) / baselines['sca'],
        'progp':    (progp - baselines['progp']) / baselines['progp'],
    }
    
    raw = sum(deltas[k] * weights[k] for k in weights)
    
    # Hard clamp to ±15%
    return round(max(-0.15, min(0.15, raw)), 4)

def main():
    parser = argparse.ArgumentParser(description="Quantitative Data Pipeline v3.0 (Industrial Grade)")
    parser.add_argument("--home", type=str, required=True)
    parser.add_argument("--away", type=str, required=True)
    parser.add_argument("--output-radar", type=str, required=True)
    
    # Dynamic league stats (passed through to poisson_predict.py)
    parser.add_argument("--league-avg-goals", type=float, default=0.0)
    parser.add_argument("--league-home-goals-avg", type=float, default=0.0)
    parser.add_argument("--league-away-goals-avg", type=float, default=0.0)
    parser.add_argument("--venue", type=str, default="home")
    parser.add_argument("--ref-penalty-boost", type=float, default=0.0)
    parser.add_argument("--home-missing-xg-pct", type=float, default=0.0)
    parser.add_argument("--away-missing-xg-pct", type=float, default=0.0)
    parser.add_argument("--home-missing-def-pct", type=float, default=0.0)
    parser.add_argument("--away-missing-def-pct", type=float, default=0.0)
    
    # Raw array inputs (comma separated, chronological order: oldest first, newest last)
    parser.add_argument("--home-xg", type=str, default="")
    parser.add_argument("--home-xga", type=str, default="")
    parser.add_argument("--home-poss", type=str, default="")
    parser.add_argument("--home-pass", type=str, default="")
    parser.add_argument("--home-ppda", type=str, default="")
    parser.add_argument("--home-duel", type=str, default="")
    parser.add_argument("--home-sca", type=str, default="")
    parser.add_argument("--home-progp", type=str, default="")
    
    parser.add_argument("--away-xg", type=str, default="")
    parser.add_argument("--away-xga", type=str, default="")
    parser.add_argument("--away-poss", type=str, default="")
    parser.add_argument("--away-pass", type=str, default="")
    parser.add_argument("--away-ppda", type=str, default="")
    parser.add_argument("--away-duel", type=str, default="")
    parser.add_argument("--away-sca", type=str, default="")
    parser.add_argument("--away-progp", type=str, default="")
    
    args = parser.parse_args()

    print(f"{'='*60}")
    print(f"QUANTITATIVE DATA PIPELINE v3.0 (Industrial Grade)")
    print(f"Processing: {args.home} vs {args.away}")
    print(f"Venue: {args.venue}")
    if args.league_avg_goals > 0:
        print(f"League Stats: AvgGoals={args.league_avg_goals}, HomeAvg={args.league_home_goals_avg}, AwayAvg={args.league_away_goals_avg}")
    print(f"{'='*60}")
    
    # ========== TIME-DECAY WEIGHTED AVERAGES ==========
    print(f"\n[1/4] Computing time-decay weighted averages (xi=0.3)...")
    
    h_xg   = parse_and_weighted_average(args.home_xg, 1.40, max_val=10.0)
    h_xga  = parse_and_weighted_average(args.home_xga, 1.40, max_val=10.0)
    h_poss = parse_and_weighted_average(args.home_poss, 50.0, max_val=100.0)
    h_pass = parse_and_weighted_average(args.home_pass, 82.0, max_val=100.0)
    
    h_ppda = parse_and_weighted_average(args.home_ppda, None, max_val=50.0)
    h_ppda = h_ppda if h_ppda is not None else round(max(5.0, 12.0 - ((h_poss - 50.0) / 10.0) * 2.0), 2)
    
    h_duel = parse_and_weighted_average(args.home_duel, None, max_val=100.0)
    h_duel = h_duel if h_duel is not None else round(min(100.0, max(0.0, 50.0 + (h_poss - 50.0) * 0.15)), 2)
    
    h_sca  = parse_and_weighted_average(args.home_sca, None, max_val=100.0)
    h_sca = h_sca if h_sca is not None else round(25.0 * (h_xg / 1.40), 2)
    
    h_progp = parse_and_weighted_average(args.home_progp, None, max_val=200.0)
    h_progp = h_progp if h_progp is not None else round(40.0 * (h_poss / 50.0), 2)
    
    a_xg   = parse_and_weighted_average(args.away_xg, 1.40, max_val=10.0)
    a_xga  = parse_and_weighted_average(args.away_xga, 1.40, max_val=10.0)
    a_poss = parse_and_weighted_average(args.away_poss, 50.0, max_val=100.0)
    a_pass = parse_and_weighted_average(args.away_pass, 82.0, max_val=100.0)
    
    a_ppda = parse_and_weighted_average(args.away_ppda, None, max_val=50.0)
    a_ppda = a_ppda if a_ppda is not None else round(max(5.0, 12.0 - ((a_poss - 50.0) / 10.0) * 2.0), 2)
    
    a_duel = parse_and_weighted_average(args.away_duel, None, max_val=100.0)
    a_duel = a_duel if a_duel is not None else round(min(100.0, max(0.0, 50.0 + (a_poss - 50.0) * 0.15)), 2)
    
    a_sca  = parse_and_weighted_average(args.away_sca, None, max_val=100.0)
    a_sca = a_sca if a_sca is not None else round(25.0 * (a_xg / 1.40), 2)
    
    a_progp = parse_and_weighted_average(args.away_progp, None, max_val=200.0)
    a_progp = a_progp if a_progp is not None else round(40.0 * (a_poss / 50.0), 2)
    
    print(f"  {args.home}: xG:{h_xg}, xGA:{h_xga}, Poss:{h_poss}%, Pass:{h_pass}%, PPDA:{h_ppda}, Duel:{h_duel}%, SCA:{h_sca}, ProgP:{h_progp}")
    print(f"  {args.away}: xG:{a_xg}, xGA:{a_xga}, Poss:{a_poss}%, Pass:{a_pass}%, PPDA:{a_ppda}, Duel:{a_duel}%, SCA:{a_sca}, ProgP:{a_progp}")
    
    # ========== COMPOSITE STRENGTH MODIFIER ==========
    print(f"\n[2/4] Computing composite strength modifiers...")
    
    h_mod = compute_strength_modifier(h_poss, h_pass, h_ppda, h_duel, h_sca, h_progp)
    a_mod = compute_strength_modifier(a_poss, a_pass, a_ppda, a_duel, a_sca, a_progp)
    
    print(f"  {args.home} Strength Modifier: {h_mod:+.4f}")
    print(f"  {args.away} Strength Modifier: {a_mod:+.4f}")
    
    # ========== RADAR CHART ==========
    print(f"\n[3/4] Generating radar chart...")
    
    home_stats = [h_xg, h_xga, h_poss, h_pass, h_ppda, h_duel, h_sca, h_progp]
    away_stats = [a_xg, a_xga, a_poss, a_pass, a_ppda, a_duel, a_sca, a_progp]
    
    def normalize(stats):
        return [
            min(stats[0] * 33.3, 100),
            max(100 - (stats[1] * 33.3), 0),
            stats[2],
            stats[3],
            max(100 - (stats[4] * 4), 0),
            stats[5],
            min(stats[6] * 3, 100),
            min(stats[7] * 1.5, 100)
        ]
        
    h_norm = normalize(home_stats)
    a_norm = normalize(away_stats)
    
    home_stat_str = ",".join(map(str, h_norm))
    away_stat_str = ",".join(map(str, a_norm))
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    python_exe = sys.executable
    
    home_raw_str = ",".join(map(str, home_stats))
    away_raw_str = ",".join(map(str, away_stats))
    
    radar_cmd = [
        python_exe, os.path.join(script_dir, 'generate_radar.py'),
        '--team1', args.home, '--team2', args.away,
        '--stats1', home_stat_str, '--stats2', away_stat_str,
        '--raw-stats1', home_raw_str, '--raw-stats2', away_raw_str,
        '--output', args.output_radar
    ]
    subprocess.run(radar_cmd)
    
    # ========== DIXON-COLES POISSON ENGINE ==========
    print(f"\n[4/4] Running Dixon-Coles Poisson Engine v3.0...")
    
    poisson_cmd = [
        python_exe, os.path.join(script_dir, 'poisson_predict.py'),
        '--home', args.home, '--away', args.away,
        '--home-xg', str(h_xg), '--away-xg', str(a_xg),
        '--home-xga', str(h_xga), '--away-xga', str(a_xga),
        '--league-avg-goals', str(args.league_avg_goals),
        '--league-home-goals-avg', str(args.league_home_goals_avg),
        '--league-away-goals-avg', str(args.league_away_goals_avg),
        '--venue', args.venue,
        '--ref-penalty-boost', str(args.ref_penalty_boost),
        '--home-missing-xg-pct', str(args.home_missing_xg_pct),
        '--away-missing-xg-pct', str(args.away_missing_xg_pct),
        '--home-missing-def-pct', str(args.home_missing_def_pct),
        '--away-missing-def-pct', str(args.away_missing_def_pct),
        '--strength-mod-home', str(h_mod),
        '--strength-mod-away', str(a_mod),
    ]
    subprocess.run(poisson_cmd)
    
    print(f"\n[+] Pipeline v3.0 execution complete.")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
