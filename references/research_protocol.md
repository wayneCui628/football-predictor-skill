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

## 2. Search Syntax & Timestamp Verification (搜索语法与时效校验)
- **Always include the current year and month** in your search query to prevent pulling matches from previous seasons.
  - *Example Search*: `Manchester City vs Arsenal injuries site:bbc.com [Current Year] [Current Month]`
- **Verify the Publication Date**: When you read a page (`read_url_content`), immediately look for the publication date. If the article is more than 7-10 days old, DISCARD IT. Do not use 2-year-old injury news.

## 3. Cross-Validation of Critical Intelligence (核心情报交叉验证)
- If you find a piece of critical news (e.g., "Kevin De Bruyne is out injured"), you MUST attempt to find confirmation from a second source in the whitelist.
- If you cannot confirm it across two sources, note it as "unconfirmed" in your analysis.

## 4. Fact vs. Opinion (事实与观点剥离)
- Extract ONLY objective facts: confirmed lineups, historical scores, official injury reports, xG data.
- IGNORE the original author's subjective predictions or commentary. You are the analyst; you formulate your own opinion based on the hard data.
