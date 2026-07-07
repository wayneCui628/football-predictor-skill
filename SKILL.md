---
name: football-predictor
description: Analyze and predict football match results (soccer) comprehensively and autonomously. Use this whenever the user asks to predict a football match, analyze a soccer team's chances, or wants betting/score predictions. This skill covers both club and national team matches.
---

# Football Match Predictor

A comprehensive, agent-driven skill to analyze and predict football (soccer) matches. This skill uses your native web search capabilities to act as a professional football analyst, fetching data from multiple sources to eliminate hallucination, and performing a multi-dimensional analysis before outputting a prediction.

## Core Workflow

Whenever you are invoked to predict a match:

1. **Acknowledge and Plan**: Briefly acknowledge the match you are predicting.
2. **Execute Exhaustive Autonomous Research (NO INTERNAL MEMORY)**: You MUST proactively use your `search_web` and `read_url_content` tools to gather ALL necessary data. **NEVER rely on your internal training memory for ANY facts.** You MUST execute dedicated searches for the following:
   - **Basic Info**: Current 2026 manager of each team.
   - **League Stats**: Current season's average goals per game, average home goals, and average away goals for the league (use soccerstats.com or fbref).
   - **Referee**: The announced referee for the match. If a general search fails, you MUST try specific queries like `"[Team A] vs [Team B] referee"` combined with `site:transfermarkt.com`, `site:soccerway.com`, or checking official federation sites (UEFA/FIFA). Do not give up easily. Once found, search their penalty stats on Transfermarkt.
   - **Injuries/Suspensions (DUAL-PRONGED)**: First, search for `"[Team A] vs [Team B] team news predicted lineup [Current Month]"` to catch all missing role-players and defenders. Second, execute individual, specific searches for the team's absolute star players (e.g. "Mbappe injury news [Current Month]") as insurance to confirm their status and latest stats. Once all missing players are found, search their season xG on FBref to calculate their combined share of the team's xG.
   - **Conditions**: Weather forecast for the match day/location.
   - **Fatigue**: The date of both teams' last match to calculate rest days.
   Do not give up on finding this data. You must search exhaustively.
3. **Follow the Research Protocol**: Read `references/research_protocol.md` BEFORE searching.
4. **Gather Advanced Factors**: Read `references/advanced_factors.md` to understand how to incorporate weather, tactics, referees, and travel fatigue.
5. **Extract Raw Data (LEFT BRAIN)**: 
   - Use the `search_web` and `read_url_content` tools to find the FBref match logs for the two teams.
   - Extract the last 5 matches' data for **8 dimensions**: xG, xGA (Expected Goals Against), Possession (%), Pass Completion (%), PPDA, Aerial Duel Success (%), SCA (Shot-Creating Actions), and ProgP (Progressive Passes). **DO NOT calculate the averages yourself.**
   - **CRITICAL**: On FBref, advanced stats like ProgP, SCA, and PPDA/Duels are NOT on the main match log summary page. You MUST execute separate searches or navigate to the specific sub-tabs (e.g., search for `"FBref [Team Name] Match Logs Passing"`, `"FBref [Team Name] Match Logs Shot Creation"`, or `"FBref [Team Name] Match Logs Defensive Actions"`). Do NOT falsely assume the data is missing just because it's not on the first page you check!
   - **Data must be in chronological order (oldest match first, newest match last)** so the time-decay weighting in Python works correctly.
6. **Peer Review Subagent Verification (PROOFREADER CHECK)**: 
   - After you extract your initial data from a webpage, you MUST use the `invoke_subagent` tool to spawn a subagent (TypeName: "research", Role: "Data Proofreader Subagent").
   - **Prompt for Subagent**: "I extracted the following data arrays for the [Team A] vs [Team B] match: [Insert your extracted arrays here]. I used this exact URL: [Insert your URL here]. I need you to go to this exact same URL, find the tables, and act as a strict Proofreader. Verify every single number against the webpage. Tell me if I misread a row, swapped home/away, or hallucinated any numbers. If I made a mistake, provide the corrected arrays."
   - **Wait and Correct**: Once the subagent replies via the messaging system, carefully review its corrections. If it found an error (visual misalignment or hallucination), you MUST update your arrays with the corrected data.
   - You may only proceed to Python execution when the subagent confirms your data arrays perfectly match the webpage.
7. **Determine Match Context Parameters**: Before running the quantitative model, you MUST determine the following parameters from your research:
   - **`--league-avg-goals`**: Search for the current season's average total goals per game for this competition (e.g., search "Premier League 2025-26 average goals per game site:soccerstats.com" or check the FBref league page). Pass the number (e.g., `2.75`).
   - **`--league-home-goals-avg`**: Search for the average goals scored by HOME teams per game this season (e.g., `1.55`).
   - **`--league-away-goals-avg`**: Search for the average goals scored by AWAY teams per game this season (e.g., `1.20`). These three numbers allow the Python engine to dynamically derive the Dixon-Coles ρ and home advantage multiplier from real data instead of hardcoded constants.
   - **`--venue`**: Determine the venue type: `home` (standard home match), `away` (standard away match), `neutral` (neutral venue, e.g., a cup final at Wembley for non-English teams), or `host_nation` (the team IS the World Cup/Euro host nation playing in their own country).
   - **`--ref-penalty-boost`**: If you found the referee, search for their stats on Transfermarkt (total penalties awarded / total matches officiated this season). Calculate: `(referee_penalties_per_game - 0.25) * 0.76`. If the result is negative or you cannot find the data, use `0.0`.
   - **`--home-missing-xg-pct`** and **`--away-missing-xg-pct`**: For each confirmed injured/suspended key player, search FBref for that player's season xG and the team's total season xG. Calculate `player_xG / team_total_xG`. Sum this for all missing players on the same team. If no key players are missing, use `0.0`. Example: if Haaland (xG=20) is out and Man City's team xG is 80, pass `0.25`.
 8. **Run Quantitative Models (LEFT BRAIN)**: 
    - Create a dedicated folder for this match in your workspace: `[Your_Current_Workspace_Path]\[TeamA]_vs_[TeamB]\`. You will store all outputs here.
    - Pass the audited raw numbers AND all context parameters to the Python script. **Use your active workspace path and default python**:
      `python [Your_Skill_Directory]\scripts\run_pipeline.py --home "Team A" --away "Team B" --output-radar "[Your_Current_Workspace_Path]\[TeamA]_vs_[TeamB]\radar.png" --league-avg-goals 2.75 --league-home-goals-avg 1.55 --league-away-goals-avg 1.20 --venue "home" --ref-penalty-boost 0.11 --home-missing-xg-pct 0.0 --away-missing-xg-pct 0.15 --home-xg "1.2,1.5,0.8,2.1,1.1" --home-xga "0.8,1.1,1.5,0.5,1.0" --home-poss "55,60,45,50,52" --home-pass "80,85,78,82,81" --home-ppda "10,12,8,11,9" --home-duel "50,55,48,52,51" --home-sca "20,25,18,30,22" --home-progp "40,45,35,50,42" --away-xg "..." --away-xga "..." --away-poss "..." --away-pass "..." --away-ppda "..." --away-duel "..." --away-sca "..." --away-progp "..."`
    - *If you absolutely cannot find a specific advanced stat (like PPDA or SCA) after multiple attempts, omit that specific `--flag`, and Python will use a safe default. xG and xGA are mandatory.*
    - **CRITICAL**: The radar chart MUST be saved into the dedicated match folder you just created.
 9. **Analyze and Output (RIGHT BRAIN)**: Synthesize the quantitative math with your qualitative research (injuries, weather, tactics, rest days, travel fatigue, team morale). Instead of outputting the analysis directly to the chat, you MUST use the `write_to_file` tool to create a detailed markdown report file in the dedicated match folder (e.g., `[Your_Current_Workspace_Path]\[TeamA]_vs_[TeamB]\Report.md`). Ensure the analysis in the file is extremely detailed, expanding heavily on tactics, historical context, and player matchups. **IMPORTANT: Whenever you cite data, stats, or facts, you MUST use academic-style inline citations like [1] or [2] and link them to the sources.** Non-quantifiable factors (rest days, travel fatigue, team morale, weather impact) should be analyzed in prose form here, NOT fed into the mathematical model. **Language Alignment Directive**: You MUST detect the language used in the user's initial prompt. The entire final Markdown report—including all headings, bullet points, and analysis prose from the template below—MUST be translated and generated entirely in that detected language.
 10. **Generate Interactive HTML Webpage**: After creating the Markdown report, you MUST use the `run_command` tool to compile it into a beautifully formatted interactive HTML page with an Export button. Run the following command:
    `python [Your_Skill_Directory]\scripts\generate_html.py --md "[Your_Current_Workspace_Path]\[TeamA]_vs_[TeamB]\Report.md" --out "[Your_Current_Workspace_Path]\[TeamA]_vs_[TeamB]\Prediction.html" --radar "[Your_Current_Workspace_Path]\[TeamA]_vs_[TeamB]\radar.png"`
 11. **Finalize**: Inform the user in the chat that the interactive Web Report has been generated successfully in the dedicated folder. Instruct them to double-click the `Prediction.html` file to open it in their browser, where they will see the beautiful layout and can use the floating "Export PDF" button.

## Report File Template

**CRITICAL INSTRUCTION FOR THE LLM**: You MUST strictly follow the template below. You are FORBIDDEN from skipping any headers, bullet points, or analytical dimensions. You MUST analyze EVERY single factor listed in the italic text under each heading. If you absolutely cannot find data for a specific point, you must still keep the bullet point and explicitly state "Data not found for this dimension". Do NOT summarize or compress the template. You MUST translate this template into the detected language of the user's prompt before generating the final report.

ALWAYS use this exact structural template for the markdown report file you generate:

# 🏆 [Deep Match Prediction]: [Team A] vs [Team B]

## 🕵️‍♂️ [Intelligence & Parameter Display]
*You MUST clearly display all underlying parameters and facts you obtained through search here. DO NOT hide data. Format as follows:*
* **[League Macro Data]**: Avg Goals ___, Home Avg ___, Away Avg ___ (Source Link)
* **[Referee Data]**: Referee Name ___, Avg Penalties/Game ___ (Source Link)
* **[Missing Players Impact]**:
  * Home missing: ___ (___% of team xG) (Source Link)
  * Away missing: ___ (___% of team xG) (Source Link)
* **[Physical Condition]**: Home rested ___ days, Away rested ___ days.
* **[Weather Forecast]**: ___ (Source Link)

## 📊 [Core Data Collision & Radar Chart]
*Compare last 5-10 matches, H2H, home/away differences. [1]*
*The radar chart will be automatically injected into the generated HTML. You do not need to write markdown image tags here, just text analysis.*

## 🧮 [Poisson Quantitative Probability]
*Paste the rigorous math probabilities (Win/Draw/Loss %) and top 3 scoreline probabilities you obtained from running `run_pipeline.py`. Include the engine's key parameters (competition, venue, rho, ref_boost, missing_xg_pct, strength_modifier).*

## 🏥 [Squad & Injury Brief]
*List injuries/suspensions and assess their on-paper impact. Note the key players fed into the quantitative model and their xG share. [2]*

## 🧑‍🏫 [Managerial Duel & Key Matchups]
* **[Managerial Tactics]**: (MUST name current managers) Analyze tactical preferences (e.g., possession vs counter-attack) and preferred formations. [3]
* **[Key Players]**: Identify players in red-hot form and how they will dictate the game.
* **[Defensive Weaknesses]**: Identify soft spots (e.g., slow CBs, out-of-position fullbacks) and how the opponent might exploit them.

## 💡 [X-Factors (Qualitative Analysis)]
*Conduct deep qualitative analysis based on the data published in section 1:*
* **[Referee Leniency]**: How this referee's card/penalty tendencies affect defensive aggression inside the box. [4]
* **[Pitch & Weather]**: How extreme weather impacts stamina or passing accuracy.
* **[Fatigue & Motivation]**: Analyze rest day differences, intercontinental travel, and motivation (relegation/title race/friendlies).

## 🔮 [Final Prediction]
* **[Core Prediction]**: 90-minute Win/Draw/Loss probability analysis and inclination.
* **[Knockout Stage]**: (Cup matches only) Will it go to extra time/penalties? Who advances?
* **[Scoreline Reference]**: 1-2 most likely 90-minute scorelines (e.g., 1-1, 2-1).

## 📚 [References]
*List all URLs cited in the text in order.*
* [1] [Stats Site Name] (URL)
* [2] [Injury Site Name] (URL)
* [3] [Tactics Blog Name] (URL)
* [4] [Weather/Ref Site] (URL)
