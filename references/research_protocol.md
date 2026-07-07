# Research Protocol: Data Reliability & Anti-Hallucination

This protocol outlines strictly how you must search for and extract football data. DO NOT rely on your pre-trained knowledge for recent matches, injuries, or odds. You MUST use your web search tools.

## 1. Domain Whitelists (强制白名单)
To avoid SEO spam, fan blogs, and unreliable rumors, you MUST restrict your searches using the `site:` operator.

**For Basic Stats, Standings, and H2H:**
- `site:fbref.com` (Best for xG and advanced stats)
- `site:transfermarkt.com` (Good for historical matchups and team values)
- `site:whoscored.com` (Good for player ratings and basic stats)

**For Injuries, Suspensions, and Lineups:**
- `site:transfermarkt.com` (Look for the "Injuries and Suspensions" page for the specific club)
- `site:bbc.com/sport/football`
- `site:theathletic.com`
- `site:skysports.com`
- `site:reuters.com`

**For National Teams (Specifically):**
- `site:fifa.com` (For official world rankings)
- Search queries like `[National Team] squad announcement` restricted to reliable news sites.

## 2. Dual-Pronged Search Strategy & Temporal Targeting (双管齐下的搜索与时效校验)
- **Always include the current year and EXACT current month** in your search query to prevent pulling matches from previous seasons.
- **Prong 1: The "Team News" Sweep (Coverage for All Players)**: To ensure you do not miss injuries to crucial role-players (defenders, midfielders), you MUST search for the specific match's preview articles. Use queries like `"[Team A] vs [Team B] team news injuries predicted lineup [Current Month] [Current Year]"`. These articles usually list EVERY injured or suspended player for the upcoming match.
- **Prong 2: Micro-Target Core Players (Star Insurance)**: Never rely *solely* on broad macro searches. After Prong 1, identify the 2-3 most important star players for each team (e.g., Mbappe) and run INDIVIDUAL, exact searches for them (e.g., `"Kylian Mbappe injury news July 2026"`). This guarantees you do not miss sudden training injuries for the most critical players.
- **Verify the Publication Date**: When you read a page (`read_url_content`), immediately look for the publication date. If the article is more than 3-5 days old during a fast-paced tournament, DISCARD IT.

## 3. Cross-Validation of Critical Intelligence (核心情报交叉验证)
- If you find a piece of critical news (e.g., "Kevin De Bruyne is out injured"), you MUST attempt to find confirmation from a second source in the whitelist.
- If you cannot confirm it across two sources, note it as "unconfirmed" in your analysis.

## 4. Fact vs. Opinion (事实与观点剥离)
- Extract ONLY objective facts: confirmed lineups, historical scores, official injury reports, xG data.
- IGNORE the original author's subjective predictions or commentary. You are the analyst; you formulate your own opinion based on the hard data.
