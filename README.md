# ⚽ Football Predictor Skill (v3.0 Industrial Grade)

A professional-grade, multi-agent LLM skill for predicting football (soccer) matches. This system combines deterministic mathematical modeling (Dixon-Coles Poisson Engine) with autonomous AI research and qualitative analysis.

## 🌟 Core Architecture

The skill operates on a "Split-Brain" architecture:

1. **Left Brain (Quantitative)**: A robust Python pipeline (`run_pipeline.py` & `poisson_predict.py`) that handles hard data.
   - Computes time-decay weighted averages (exponential decay, $\xi=0.3$) for 8 advanced performance metrics (xG, xGA, Possession, Pass%, PPDA, Duel%, SCA, ProgP).
   - Dynamically derives Dixon-Coles parameters ($\rho$ and Home Advantage) directly from current season league statistics (goals per game, home/away splits) rather than using hardcoded lookup tables.
   - Uses a bespoke composite strength modifier to fine-tune goal expectancies.
   - Calculates the impact of referee penalty tendencies and missing player xG contributions.
2. **Right Brain (Qualitative)**: The LLM acts as an elite football analyst.
   - Performs exhaustive autonomous web searches (via Transfermarkt, FBref, Soccerstats, etc.) to gather real-time data, weather conditions, rest days, and managerial tactics.
   - Avoids "AI hallucinations" by strictly separating facts from internal training memory.
   - Synthesizes the mathematical probabilities with qualitative variables (e.g., travel fatigue, pitch conditions, tactical matchups) into a comprehensive Markdown report.
3. **Data Verification Agent**: An embedded sub-agent process that acts as a "Data Proofreader" to verify scraped web tables against LLM extraction, ensuring 100% data integrity before hitting the mathematical model.

## 📂 Directory Structure

```text
football-predictor/
├── SKILL.md                  # Main LLM instruction file (Agent Prompt)
├── README.md                 # This documentation file
├── references/
│   ├── advanced_factors.md   # Guidelines for analyzing qualitative X-factors
│   └── research_protocol.md  # Standard operating procedures for data scraping
└── scripts/
    ├── poisson_predict.py    # v3.0 Dixon-Coles Mathematical Engine
    ├── run_pipeline.py       # Data aggregator and weighting pipeline
    └── generate_html.py      # Markdown to interactive HTML renderer
```

## 🚀 How to Use

Simply load this skill into your Gemini/Claude environment and prompt the agent:
> *"Predict the upcoming match between Arsenal and Manchester City."*

The agent will automatically:
1. Search the web for league stats, referee info, missing players, and tactical context.
2. Search FBref for the last 5 matches' advanced metrics.
3. Call a sub-agent to proofread the data.
4. Run the Python pipeline to generate a Radar Chart and Match Probabilities.
5. Write a detailed analytical report in Markdown.
6. Compile the report into an interactive HTML page.

## 🛠 Requirements

- Python 3.10+
- `scipy` (for Poisson distribution)
- `matplotlib` (for Radar charts)
- `pandas` & `numpy` (for data manipulation)
- `markdown` (for HTML generation)

## 🔄 Version History

- **v3.0 (Industrial Grade)**: Eliminated hardcoded $\rho$ and Home Advantage constants. Implemented dynamic derivation from league stats. Added bounded data parsing constraints. Removed hardcoded workspace paths.
- **v2.0**: Introduced the Multi-Agent proofreading workflow and the 8-dimensional time-decay weighting model.
- **v1.0**: Initial implementation of the Dixon-Coles Poisson distribution model.
