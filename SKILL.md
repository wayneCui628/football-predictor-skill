---
name: football-predictor
description: Analyze and predict football match results (soccer) comprehensively and autonomously. Use this whenever the user asks to predict a football match, analyze a soccer team's chances, or wants betting/score predictions. This skill covers both club and national team matches.
---

# Football Match Predictor (Multi-Agent Architecture)

A highly advanced, multi-agent skill to analyze and predict football (soccer) matches. This skill utilizes parallel Subagent dispatching to ensure absolute data accuracy and exhaustive intelligence gathering.

## Core Workflow (The Agentic Pipeline)

Whenever you are invoked to predict a match, you MUST strictly follow this multi-agent pipeline:

### Phase 1: Parallel Subagent Dispatch
You MUST IMMEDIATELY use the `invoke_subagent` tool to spawn TWO parallel subagents. Do NOT attempt to do the research yourself. You are the Main Coordinator and your job is to dispatch the specialists.

**Subagent A: Football Data Extractor**
- **TypeName**: `research`
- **Role**: `FBref Data Extractor`
- **Prompt**: "Go to FBref.com and extract the EXACT raw data for [Team A] and [Team B]. First, establish their last 5 meaningful matches. Then, extract the following 8 metrics for BOTH teams across those 5 matches: xG, xGA, Possession, Pass Completion %, PPDA, Duel Success %, Shot-Creating Actions (SCA), and Progressive Passes (ProgP). BE EXTREMELY CAREFUL reading the tables to avoid swapping columns (e.g., do not confuse GA with xGA, check if a team kept 5 clean sheets their xGA should be very low). Note: Advanced stats like ProgP, SCA, and PPDA are often on sub-tabs, not the main match log. Output your final result ONLY as a structured JSON object containing the arrays, so I can parse it easily."

**Subagent B: Football Intelligence Scout**
- **TypeName**: `research`
- **Role**: `Intelligence Scout`
- **Prompt**: "Perform exhaustive web research for the [Team A] vs [Team B] match. 1. Find the tournament's average goals per game. 2. Find the match referee and their penalties-per-game stat on Transfermarkt. 3. Find weather and rest days. 4. CRITICAL: Search specifically on Transfermarkt AND major news outlets for ANY injuries or suspensions (e.g., search 'Amadou Onana injury' or 'Nico Williams adductor'). Do not trust a single source if it says 'no injuries', cross-verify with recent news. 5. Calculate the missing xG penalty % for offensive absences, and the missing defense penalty % for defensive absences. 6. CRITICAL LINEUP LOGIC: Find the ACTUAL starting XI lineups of BOTH teams for their LAST 2 matches in this tournament/league. Under NO circumstances should you guess predicted lineups based on historical reputation (e.g., do not include players like Phil Foden if they are not in the current squad or were benched). Verify the actual squad list of the team for the current season. Use the logic: [Actual lineup from last match] + [adjustments for new injuries/suspensions/returns] to deduce the predicted starting XI. Output your final result ONLY as a structured JSON object containing these parameters."


### Phase 2: Wait and Parse
Stop and wait. You will be automatically notified via the messaging system when Subagents A and B reply with their JSON payloads. Parse their data. If any data is missing or looks suspicious (e.g., xGA is 0.6 but the team had 5 clean sheets, or missing parameters), you MUST reply to the subagent using `send_message` demanding a recount and correction.

### Phase 3: The Python Engine (Quantitative)
Once you have the audited data from both subagents:
1. Create a dedicated folder for this match in your workspace: `[Your_Current_Workspace_Path]\[TeamA]_vs_[TeamB]\`.
2. Run the pipeline script using the data from the subagents:
   `python [Your_Skill_Directory]\scripts\run_pipeline.py --home "Team A" --away "Team B" --output-radar "[Your_Current_Workspace_Path]\[TeamA]_vs_[TeamB]\radar.png" --league-avg-goals ... [insert all flags based on subagent JSONs]`
3. The script will output math probabilities (Win/Draw/Loss %) and create `radar.png`.

### Phase 4: Qualitative Synthesis and Report Generation
Synthesize the quantitative math with the intelligence from Subagent B. 
1. Use the `write_to_file` tool to create `[Your_Current_Workspace_Path]\[TeamA]_vs_[TeamB]\Report.md`.
2. Follow the exact Report Template (see below).
3. Translate all headings and content into the detected language of the user's prompt. 
4. Include academic-style inline citations [1] linking to the sources the subagents provided.
5. CRITICAL LINEUP VERIFICATION: For the starting lineups section of the report, strictly use the actual lineups of the last 2 matches and injury adjustments provided by Subagent B. You are strictly forbidden from fabricating a lineup based on player name recognition, historical memory, or generic team templates. Ensure players listed are confirmed members of the current tournament squad.


### Phase 5: Generate Interactive Webpage
Run the HTML compiler:
`python [Your_Skill_Directory]\scripts\generate_html.py --md "[Your_Current_Workspace_Path]\[TeamA]_vs_[TeamB]\Report.md" --out "[Your_Current_Workspace_Path]\[TeamA]_vs_[TeamB]\Prediction.html" --radar "[Your_Current_Workspace_Path]\[TeamA]_vs_[TeamB]\radar.png"`

Finally, inform the user they can double-click `Prediction.html` to view the interactive report.

## Report File Template

**CRITICAL INSTRUCTION**: You MUST strictly follow the template below. You are FORBIDDEN from skipping any headers or analytical dimensions. Do NOT summarize or compress the template. You MUST translate all section headings and content into the detected language of the user's prompt.

# 🏆 Deep Match Prediction: [Team A] vs [Team B]

## 🕵️‍♂️ Intelligence & Parameter Display
* **League Macro Data**: Avg Goals ___, Home Avg ___, Away Avg ___ (Source Link)
* **Referee Data**: Referee Name ___, Avg Penalties/Game ___ (Source Link)
* **Missing Players Impact**:
  * Home missing: ___ (___% of team xG) (Source Link)
  * Away missing: ___ (___% of team xG) (Source Link)
* **Physical Condition**: Home rested ___ days, Away rested ___ days.
* **Weather Forecast**: ___ (Source Link)

## 📊 Core Data Collision & Radar Chart
*Compare last 5 matches, H2H, home/away differences.*
*The radar chart will be automatically injected into the generated HTML.*

## 🧮 Poisson Quantitative Probability
*Paste the rigorous math probabilities (Win/Draw/Loss %) and top 3 scoreline probabilities.*

## 👥 Starting Lineups & Tactical Shifts
* **Team A Predicted XI**: ...
* **Team B Predicted XI**: ...
* **Forced Tactical Shifts & Replacements**: Analyze how absences (reported by Subagent B) force the manager to change formations or impact the team's rating.

## 🧑‍🏫 Managerial Duel & Key Matchups
* **Managerial Tactics**: ...
* **Key Players**: ...
* **Defensive Weaknesses**: ...

## 💡 X-Factors (Qualitative Analysis)
* **Referee Leniency**: ...
* **Pitch & Weather**: ...
* **Fatigue & Motivation**: ...

## 🔮 Final Prediction
* **Core Prediction**: 90-minute Win/Draw/Loss probability analysis and inclination.
* **Knockout Stage**: (Cup matches only) Will it go to extra time/penalties? Who advances?
* **Scoreline Reference**: 1-2 most likely 90-minute scorelines.

## 📚 References
*List all URLs cited in the text in order.*
