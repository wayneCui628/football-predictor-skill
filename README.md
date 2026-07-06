# Football Predictor Skill (足球预测智能体技能)

*An Industrial-Grade, Multi-Agent Football Match Predictor for AI Agents.*
*工业级、多智能体协作的 AI 足球赛事预测框架。*

## 🇬🇧 English

### Overview
This repository contains a highly advanced, agentic skill designed for LLM-based autonomous AI agents (like Claude/Antigravity). It enables the AI to act as a professional football data analyst. Instead of relying on hallucinated internal memory, the AI is strictly instructed to execute real-time web searches, gather statistics across 8 advanced dimensions (xG, Possession, PPDA, SCA, etc.), and feed them into a quantitative Poisson distribution model before writing a deep qualitative report.

### Key Features (v3.0)
- **Zero Hallucination Policy**: The AI must search for real-time data, and a "Proofreader Subagent" verifies extracted tables before math execution.
- **Dynamic Math Engine**: Calculates time-decayed exponential weights (recent matches matter more) and dynamically derives Dixon-Coles `rho` and Home Advantage based on current league averages.
- **Advanced Contextual Parameters**: Incorporates referee penalty boost percentages and injured/suspended key players' xG shares directly into the Poisson math.
- **i18n Support**: The LLM will automatically detect your prompt's language and output the final HTML/Markdown report in your preferred language.
- **Beautiful Output**: Generates an interactive HTML dashboard with Radar Charts comparing the two teams.

### How to Use
1. Clone this repository into your agent's `skills` folder.
2. Ask your agent: *"Predict the match between Arsenal and Liverpool"* (or in any language).
3. Wait as the agent researches, runs the python engine, and generates the final HTML report in your workspace.

---

## 🇨🇳 简体中文

### 项目简介
这是一个为 LLM 智能体（如 Claude/Antigravity）打造的工业级足球赛事预测技能库。它能够让 AI 化身为专业的数据分析师。该技能严格禁止大模型使用内部记忆“凭空捏造”比分，而是强制 AI 进行实时的全网深度搜索，抓取 8 大高阶维度数据（预期进球 xG、球权、PPDA、SCA 等），并将其喂给量化的泊松分布（Poisson Distribution）引擎，最后生成深度的定性与定量分析报告。

### 核心特性 (v3.0)
- **零幻觉机制**：AI 必须实时搜索数据，并且内置了“审查子智能体（Proofreader Subagent）”对抓取的数据表进行严格的二次核对。
- **动态数学引擎**：使用时间衰减加权（越近的比赛权重越大），并基于当前联赛的真实场均进球数，动态推导 Dixon-Coles 模型的 `rho` 值和主场优势系数。
- **高阶语境参数**：主裁判的点球倾向、伤停核心球员的 xG（预期进球）占比等高阶数据，将直接参与泊松数学模型的计算。
- **多语言自适应 (i18n)**：大模型会自动侦测你提问的语言，并用该语言生成最终的图文报告（无论中英日韩）。
- **精美可视化**：自动在你的工作区生成包含“双方战力雷达图”的精美交互式 HTML 网页报告。

### 如何使用
1. 将此代码库克隆到你智能体的 `skills` 目录下。
2. 对你的智能体说：*“帮我预测一下阿森纳对阵利物浦的比赛”*。
3. 稍作等待，智能体将自主完成全网搜集、Python 量化引擎计算，并在你的工作区生成最终的 HTML 网页版报告。
