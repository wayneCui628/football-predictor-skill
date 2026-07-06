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
   - **Referee**: The announced referee for the match. Once found, search their penalty stats on Transfermarkt.
   - **Injuries/Suspensions**: Current missing key players. Once found, search their season xG on FBref to calculate their share of the team's xG.
   - **Conditions**: Weather forecast for the match day/location.
   - **Fatigue**: The date of both teams' last match to calculate rest days.
   Do not give up on finding this data. You must search exhaustively.
3. **Follow the Research Protocol**: Read `references/research_protocol.md` BEFORE searching.
4. **Gather Advanced Factors**: Read `references/advanced_factors.md` to understand how to incorporate weather, tactics, referees, and travel fatigue.
5. **Extract Raw Data (LEFT BRAIN)**: 
   - Use the `search_web` and `read_url_content` tools to find the FBref match logs for the two teams.
   - Extract the last 5 matches' data for **8 dimensions**: xG, xGA (Expected Goals Against), Possession (%), Pass Completion (%), PPDA, Aerial Duel Success (%), SCA (Shot-Creating Actions), and ProgP (Progressive Passes). **DO NOT calculate the averages yourself.**
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
   - Pass the audited raw numbers AND all context parameters to the Python script. **Use your active workspace path and default python**:
     `python [Your_Skill_Directory]\scripts\run_pipeline.py --home "Team A" --away "Team B" --output-radar "[Your_Artifact_Directory_Path]\[TeamA]_[TeamB]_radar.png" --league-avg-goals 2.75 --league-home-goals-avg 1.55 --league-away-goals-avg 1.20 --venue "home" --ref-penalty-boost 0.11 --home-missing-xg-pct 0.0 --away-missing-xg-pct 0.15 --home-xg "1.2,1.5,0.8,2.1,1.1" --home-xga "0.8,1.1,1.5,0.5,1.0" --home-poss "55,60,45,50,52" --home-pass "80,85,78,82,81" --home-ppda "10,12,8,11,9" --home-duel "50,55,48,52,51" --home-sca "20,25,18,30,22" --home-progp "40,45,35,50,42" --away-xg "..." --away-xga "..." --away-poss "..." --away-pass "..." --away-ppda "..." --away-duel "..." --away-sca "..." --away-progp "..."`
   - *If you absolutely cannot find a specific advanced stat (like PPDA or SCA) after multiple attempts, omit that specific `--flag`, and Python will use a safe default. xG and xGA are mandatory.*
   - **CRITICAL**: You MUST find your current "Artifact Directory Path" from your system instructions. You MUST pass that absolute path as the `--output-radar` argument so the image is saved directly into the Artifact folder.
9. **Analyze and Output (RIGHT BRAIN)**: Synthesize the quantitative math with your qualitative research (injuries, weather, tactics, rest days, travel fatigue, team morale). Instead of outputting the analysis directly to the chat, you MUST use the `write_to_file` tool to create a detailed markdown report file in your current workspace (e.g., `[Your_Current_Workspace_Path]\[TeamA]_[TeamB]_Report.md`). Ensure the analysis in the file is extremely detailed, expanding heavily on tactics, historical context, and player matchups. **IMPORTANT: Whenever you cite data, stats, or facts, you MUST use academic-style inline citations like [1] or [2] and link them to the sources.** Non-quantifiable factors (rest days, travel fatigue, team morale, weather impact) should be analyzed in prose form here, NOT fed into the mathematical model.
10. **Generate Interactive HTML Webpage**: After creating the Markdown report, you MUST use the `run_command` tool to compile it into a beautifully formatted interactive HTML page with an Export button. Run the following command:
   `python [Your_Skill_Directory]\scripts\generate_html.py --md "[Your_Current_Workspace_Path]\[TeamA]_[TeamB]_Report.md" --out "[Your_Current_Workspace_Path]\[TeamA]_[TeamB]_Prediction.html" --radar "[Your_Artifact_Directory_Path]\[TeamA]_[TeamB]_radar.png"`
11. **Finalize**: Inform the user in the chat that the interactive Web Report has been generated successfully. Instruct them to double-click the `.html` file to open it in their browser, where they will see the beautiful layout and can use the floating "Export PDF" button.

## Report File Template

**CRITICAL INSTRUCTION FOR THE LLM**: You MUST strictly follow the template below. You are FORBIDDEN from skipping any headers, bullet points, or analytical dimensions. You MUST analyze EVERY single factor listed in the italic text under each heading. If you absolutely cannot find data for a specific point, you must still keep the bullet point and explicitly state "Data not found for this dimension". Do NOT summarize or compress the template.

ALWAYS use this exact template for the markdown report file you generate:

# 🏆 足球赛事深度预测：[Team A] vs [Team B]

## 🕵️‍♂️ 情报搜集与参数公示 (Mandatory Data Display)
*必须在这里清晰地公示你通过搜索得出的所有底层参数和事实，严禁隐藏数据。格式如下：*
* **联赛宏观数据**：场均进球 ___，主队场均 ___，客队场均 ___ (数据源链接)
* **主裁判数据**：本场主裁 ___，本赛季场均点球 ___ (数据源链接)
* **伤缺评估**：
  * 主队缺阵：___ (占队内 xG ___%) (数据源链接)
  * 客队缺阵：___ (占队内 xG ___%) (数据源链接)
* **体能状况**：主队休息 ___ 天，客队休息 ___ 天。
* **天气预报**：___ (数据源链接)

## 📊 核心数据碰撞与雷达图
*对比双方近 5-10 场战绩、历史交锋（H2H）、主客场差异。 [1]*
*雷达图将被自动注入到最终生成的 HTML 网页报告的这一部分。你在此处无需写入任何 markdown 图片标签，保持文字分析即可。*

## 🧮 泊松分布量化概率
*将你运行 `run_pipeline.py` 脚本得到的严谨数学概率（胜平负 %）以及排名前 3 的比分概率粘贴在这里。包括引擎使用的关键参数（competition, venue, rho, ref_boost, missing_xg_pct, strength_modifier）。*

## 🏥 阵容与伤停简报
*列出双方伤病名单及停赛情况，评估其对整体实力的纸面影响。标注已纳入量化模型的核心伤缺球员及其 xG 占比。 [2]*

## 🧑‍🏫 教练博弈与核心对决
* **教练战术**：(必须列出现任教练姓名) 分析双方主教练的战术偏好（如瓜迪奥拉的极致传控 vs 穆里尼奥的大巴防反），以及他们习惯的阵型。 [3]
* **核心发力点**：指出双方近期状态最火热的核心球员，以及他们将如何在比赛中发挥决定性作用。
* **防线短板**：找出双方阵容中的"软肋"（如转身慢的中卫、客串的边卫），推演对手会如何针对性打击。

## 💡 X因素剖析（定性分析）
*基于你在第一部分公示的数据，进行深度的定性分析：*
* **主裁尺度**：分析该裁判的掏牌率和点球频率对双方防守动作（尤其是禁区内防守）的具体心理影响。[4]
* **场地与天气**：分析天气预报（如极端高温、暴雨）对双方体能消耗、传球成功率的具体影响。
* **体能与战意**：综合分析双方的休息天数差异（疲劳差）、是否涉及跨大洲旅行、以及当前赛事的战意（保级/争冠/练兵）。

## 🔮 最终预测
* **核心预测**：常规时间（90分钟）的 胜/平/负 概率分析与倾向。
* **淘汰赛补充**：（仅适用杯赛）是否会进入加时/点球，以及最终晋级方。
* **比分参考**：1-2个最可能的常规时间比分（如 1-1, 2-1）。

## 📚 参考文献 (References)
*将你在正文中引用的所有 URL 来源按顺序列在这里。*
* [1] [数据来源网站名] (URL)
* [2] [伤停情报网站名] (URL)
* [3] [战术分析博客名] (URL)
* [4] [天气/裁判信息网] (URL)
