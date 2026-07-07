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

## 2. Search Syntax & Temporal Micro-Targeting (搜索语法与核心球员精确定向)
- **Always include the current year and EXACT current month** in your search query to prevent pulling matches from previous seasons or pre-tournament previews.
  - *Example Search*: `Morocco national team injury news July 2026`
- **Micro-Target Core Players (CRITICAL)**: Never rely *solely* on broad macro searches (e.g., "France injuries"). You MUST identify the 2-3 most important star players for each team (e.g., Mbappe, Hakimi) and run INDIVIDUAL, exact searches for them (e.g., `"Kylian Mbappe injury news July 2026"`, `"Kylian Mbappe total goals World Cup 2026"`). This guarantees you do not miss sudden injuries or latest stats from a match that happened yesterday.
- **Verify the Publication Date**: When you read a page (`read_url_content`), immediately look for the publication date. If the article is more than 3-5 days old during a fast-paced tournament, DISCARD IT. Do not use outdated injury news.

## 3. Cross-Validation of Critical Intelligence (核心情报交叉验证)
- If you find a piece of critical news (e.g., "Kevin De Bruyne is out injured"), you MUST attempt to find confirmation from a second source in the whitelist.
- If you cannot confirm it across two sources, note it as "unconfirmed" in your analysis.

## 4. Fact vs. Opinion (事实与观点剥离)
- Extract ONLY objective facts: confirmed lineups, historical scores, official injury reports, xG data.
- IGNORE the original author's subjective predictions or commentary. You are the analyst; you formulate your own opinion based on the hard data.
