# Corbis MCP API Reference — [corbis.ai](https://corbis.ai)

Complete reference for the [Corbis](https://corbis.ai) API tools available via Model Context Protocol (MCP). These tools give Claude direct access to 265,000+ academic papers, economic data, commercial real estate market intelligence, and web research.

---

## Tier availability

Most tools are available on all Corbis plans. Five tools require an enterprise subscription.

| Tool | Tier |
|---|---|
| `search_papers`, `get_paper_details`, `top_cited_articles` | All tiers |
| `search_datasets` | All tiers |
| `get_market_data`, `compare_markets`, `search_markets` | All tiers |
| `get_national_macro`, `fred_search`, `fred_series_batch` | All tiers |
| `find_academic_identity`, `confirm_academic_identity` | All tiers |
| `export_citations`, `format_citation` | All tiers |
| `literature_search` | Enterprise |
| `internet_search`, `read_web_page` | Enterprise |
| `deep_research`, `query_corbis` | Enterprise |

**If an enterprise tool is unavailable**, fall back to the all-tiers alternatives:
- Instead of `literature_search` → run multiple `search_papers` queries with different keywords and year ranges
- Instead of `internet_search` / `deep_research` → use `search_papers` for academic content; for news/policy, ask the user to provide URLs
- Instead of `query_corbis` → call individual tools directly

---

## Overview

Corbis exposes 19 tools organized into six functional categories:

| Category | Tools | Purpose |
|---|---|---|
| **Academic Research** | `search_papers`, `get_paper_details`, `literature_search`*, `top_cited_articles`, `search_datasets` | Find, analyze, and synthesize academic literature |
| **Citation Management** | `format_citation`, `export_citations` | Format and export references in any standard style |
| **Economic Data** | `fred_search`, `fred_series_batch`, `get_national_macro` | Access FRED macroeconomic time series |
| **CRE Market Intelligence** | `get_market_data`, `compare_markets`, `search_markets` | U.S. metro-level commercial real estate data |
| **Web Research** | `internet_search`*, `read_web_page`*, `deep_research`*, `query_corbis`* | Real-time internet search and page extraction |
| **Identity** | `find_academic_identity`, `confirm_academic_identity` | Link to OpenAlex author profile |

*\* Enterprise only*

---

## Academic Research Tools

### `search_papers`

Hybrid semantic-keyword search across 265,000+ academic papers. Uses Reciprocal Rank Fusion (RRF) to combine vector similarity with full-text keyword matching for high-quality results.

**How it works internally:**
1. The raw query is optimized via LLM for keyword expansion
2. The optimized query runs full-text search (FTS); the original query runs vector/semantic search
3. Both result sets are merged via RRF: `score = sum(1/(k + rank_i))`
4. Results are ranked by combined relevance

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `query` | string | Yes | — | Search query (1-500 chars) |
| `matchCount` | integer | No | 10 | Results to return (1-20) |
| `minYear` | integer | No | — | Minimum publication year (>= 1900) |
| `maxYear` | integer | No | — | Maximum publication year (<= current year) |
| `rrfK` | integer | No | 25 | RRF fusion parameter (higher = more weight to keyword match) |

**Returns per result:** `id`, `title`, `authors`, `year`, `journal`, `abstract`, `doi`, `openalexId`, `url`, `citedByCount`, `semanticScore`, `keywordScore`, `combinedRank`

**Best practices:**
- Use specific academic language in queries ("difference-in-differences housing prices" not "housing price effects")
- Use year filters to focus on recent work or a specific era
- Request 15-20 results for literature mapping; 5-10 for targeted searches
- Follow up with `get_paper_details` on high-citation results

---

### `get_paper_details`

Retrieve comprehensive metadata for a specific paper. Use after `search_papers` to get full details on papers of interest.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `paperId` | string | Yes | Document ID, OpenAlex ID (e.g., "W4388234567"), or DOI |

**Returns:** Full metadata, abstract, citation information, and available full-text content.

---

### `literature_search` (Enterprise)

Multi-iteration deep literature search with AI synthesis. A specialized subagent performs up to 5 rounds of targeted searches, identifies themes, and returns a structured synthesis with inline citations.

**Fallback if unavailable:** Run multiple `search_papers` queries with varied keywords and year ranges, then synthesize manually.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `researchQuestion` | string | Yes | — | Research question or topic (1-500 chars) |
| `maxSearches` | integer | No | 3 | Search iterations (1-5). More iterations = broader coverage |
| `focusAreas` | string[] | No | — | Specific subtopics to explore |

**Returns:** Structured synthesis with themes, inline citations, and paper metadata across all search rounds.

**Best practices:**
- Use for comprehensive literature mapping, not quick lookups (use `search_papers` for quick lookups)
- Specify `focusAreas` to guide the search into specific subtopics
- Set `maxSearches: 4-5` for thorough coverage; `maxSearches: 2` for focused exploration

---

### `top_cited_articles`

Find the most-cited papers within specific journals. Essential for identifying seminal work and understanding the intellectual foundations of a field.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `journalNames` | string[] | Yes | — | Journal names (e.g., ["Journal of Finance", "Review of Financial Studies"]) |
| `limit` | integer | No | 20 | Number of results (1-50) |
| `minYear` | integer | No | — | Minimum publication year |
| `maxYear` | integer | No | — | Maximum publication year |

**Best practices:**
- Use to find foundational papers in a field before doing targeted searches
- Combine with year filters to find influential recent work (e.g., `minYear: 2018`)
- Search across multiple journals to see which outlet published the most-cited work on a topic
- Finance journals: "Journal of Finance", "Journal of Financial Economics", "Review of Financial Studies", "Journal of Financial and Quantitative Analysis"
- Real estate journals: "Real Estate Economics", "Journal of Real Estate Finance and Economics", "Journal of Urban Economics", "Journal of Housing Economics"

---

### `search_datasets`

Discover free research datasets by topic, use case, or data type. Returns dataset name, description, link, and access information.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `query` | string | Yes | — | Search query (topic, use case, or data type) |
| `matchCount` | integer | No | 5 | Number of results (1-20) |
| `topicFilter` | string | No | — | Filter by topic (e.g., "Asset Pricing", "Real Estate") |
| `regionFilter` | string | No | — | Filter by region (e.g., "US", "Global") |

---

## Citation Management Tools

### `format_citation`

Format paper metadata into standard citation styles.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `papers` | object[] | Yes | Paper metadata (title, authors, year, journal required; doi, volume, issue, pages, url optional) |
| `style` | string | Yes | One of: `apa`, `mla`, `chicago`, `harvard`, `bibtex` |

**Returns:** Formatted citation strings ready for manuscripts.

---

### `export_citations`

Generate downloadable citation files (BibTeX, Markdown, JSON) from paper metadata.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `citations` | object[] | Yes | — | Paper metadata (title required; authors, year, journal, doi, abstract, url, pages, publisher optional) |
| `formats` | string[] | No | ["bibtex", "markdown"] | Export formats: `bibtex`, `markdown`, `json` |
| `fileName` | string | No | "references" | Base filename (no extension) |
| `includeAbstract` | boolean | No | false | Include abstracts in exports |

**Best practices:**
- Use `bibtex` format for LaTeX/Overleaf workflows
- Use `markdown` for quick reference lists in working documents
- Set `includeAbstract: true` when building annotated bibliographies

---

## Economic Data Tools

### `fred_search`

Search FRED (Federal Reserve Economic Data) series by text. Use this first to find correct series IDs before fetching data.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `query` | string | Yes | — | Free-text search (e.g., "30-year mortgage rate", "Case-Shiller home price") |
| `limit` | integer | No | 10 | Results to return (1-50) |

**Returns:** Series IDs, titles, frequency, and units.

**Key series for finance/real estate research:**
- `CSUSHPISA` — S&P/Case-Shiller U.S. National Home Price Index
- `MORTGAGE30US` — 30-Year Fixed Rate Mortgage Average
- `USSTHPI` — FHFA All-Transactions House Price Index
- `DGS10` — 10-Year Treasury Constant Maturity Rate
- `FEDFUNDS` — Federal Funds Effective Rate
- `CPIAUCSL` — Consumer Price Index for All Urban Consumers
- `GDPC1` — Real Gross Domestic Product
- `UNRATE` — Unemployment Rate
- `HOUST` — Housing Starts: Total
- `PERMIT` — Building Permits

---

### `fred_series_batch`

Fetch multiple FRED time series at once. Returns data as structured DataFrames.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `items` | object[] | Yes | Array of series requests (1-15 series per call) |

Each item in `items`:
| Field | Type | Required | Description |
|---|---|---|---|
| `seriesId` | string | Yes | FRED series ID |
| `observationStart` | string | No | Start date (ISO format: "2010-01-01") |
| `observationEnd` | string | No | End date (ISO format) |
| `frequency` | string | No | Aggregation: `d`, `w`, `bw`, `m`, `q`, `sa`, `a` |
| `aggregationMethod` | string | No | Method: `avg`, `sum`, `eop` |
| `units` | string | No | Transform: `lin` (levels), `chg` (change), `pch` (% change), `pc1` (YoY % change), `pca` (annualized % change) |

---

### `get_national_macro`

Retrieve national macroeconomic time series for economic context.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `series_id` | string | No | — | One of: `GDPC1` (Real GDP), `CPIAUCSL` (CPI), `DGS10` (10Y Treasury) |
| `start_date` | string | No | — | Start date (YYYY-MM-DD) |
| `end_date` | string | No | — | End date (YYYY-MM-DD) |
| `limit` | integer | No | 100 | Max rows (1-500) |

---

## CRE Market Intelligence Tools

### `get_market_data`

Retrieve comprehensive commercial real estate data for a U.S. metro area. Returns metrics, national rankings, strengths/weaknesses, and 5-year trends.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `market` | string | Yes | City name, CBSA code, or regional alias (e.g., "Fayetteville, AR", "22220", "Northwest Arkansas") |

---

### `compare_markets`

Compare 2-10 U.S. metro areas side-by-side on CRE metrics and national rankings.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `markets` | string[] | Yes | City names or CBSA codes (2-10 markets) |
| `metrics` | string[] | No | Optional metric keys to filter comparison |

---

### `search_markets`

Rank U.S. metro areas by any CRE metric. Use for "top 10 markets by job growth," "most affordable metros," etc.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `metric` | string | Yes | — | Metric key (e.g., `jobs_yoy`, `pop_yoy`, `trend_jobs_5y_cagr`) |
| `order` | string | No | "top" | `top` for highest first, `bottom` for lowest |
| `limit` | integer | No | 10 | Number of results (1-50) |
| `min_percentile` | number | No | — | Minimum percentile filter (0-100) |
| `max_percentile` | number | No | — | Maximum percentile filter (0-100) |

---

## Web Research Tools (Enterprise)

### `internet_search`

Search the internet for current information using Perplexity AI. Returns concise summaries with source citations.

**Fallback if unavailable:** Use `search_papers` for academic content. For news/policy, ask the user to provide specific URLs.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `query` | string | Yes | — | Search query (1-500 chars) |
| `maxResults` | integer | No | 14 | Maximum sources (2-14) |

**Best practices:**
- Use for recent working papers on SSRN/NBER that may not be in academic databases yet
- Use for current policy information (regulatory changes, new legislation)
- Use for institutional details (submission guidelines, conference deadlines)
- Run 2-3 parallel queries with different angles for comprehensive coverage

---

### `read_web_page`

Extract full content from a specific URL. Returns markdown content and page metadata.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `url` | string (URI) | Yes | The URL to extract content from |

---

### `deep_research`

Comprehensive multi-engine research combining Tavily + Perplexity discovery with Firecrawl extraction of top sources.

**Fallback if unavailable:** Run multiple `search_papers` queries; ask the user for specific sources.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `query` | string | Yes | — | Research query |
| `maxExtractions` | integer | No | 3 | Max URLs to deep-extract (1-5) |

---

### `query_corbis`

Send a free-form query to Corbis and get a concise, tool-grounded response. The Corbis agent selects and chains tools autonomously to answer the query.

**Fallback if unavailable:** Call individual tools directly.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `query` | string | Yes | — | Free-form query (1-4000 chars) |
| `maxSteps` | integer | No | 6 | Maximum reasoning steps (1-8) |
| `maxOutputTokens` | integer | No | 6000 | Maximum output tokens (256-6000) |

---

## Identity Tools

### `find_academic_identity`

Search for the user's academic profile in OpenAlex using profile data.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `nameOverride` | string | No | Override user's profile name |
| `institutionOverride` | string | No | Override user's institution |

### `confirm_academic_identity`

Link or unlink the user's account to an OpenAlex author ID.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `action` | string | Yes | `accept` (link) or `clear` (unlink) |
| `authorId` | string | Conditional | OpenAlex author ID (required for `accept`) |
| `authorName` | string | No | Display name |
| `confidenceScore` | number | No | Confidence score (0-100) |

---

## Recommended Tool Chains for Academic Research

### Literature Review Workflow
1. `search_papers` — Initial broad search to map the landscape
2. `top_cited_articles` — Find seminal papers in target journals
3. `get_paper_details` — Deep-dive into the closest papers
4. `search_papers` (with `minYear: 2023`) — Catch recent working papers
5. `format_citation` / `export_citations` — Format references for the manuscript

### Idea Validation Workflow
1. `search_papers` — Check if the idea has been studied before
2. `search_papers` (with `minYear: 2023`) — Check for recent working papers
3. `search_datasets` — Assess data feasibility
4. `fred_search` — Find relevant economic indicators for context

### Data Construction Workflow
1. `search_datasets` — Discover available datasets
2. `fred_search` + `fred_series_batch` — Pull macro variables
3. `search_papers` — Find papers that use similar data for methodology reference

### Real Estate Market Context
1. `get_market_data` — Metro-level CRE data
2. `compare_markets` — Side-by-side metro comparison
3. `search_markets` — Rank metros by specific metrics
4. `fred_search` + `fred_series_batch` — Housing indices, mortgage rates, macro context
5. `get_national_macro` — GDP, CPI, Treasury rates for economic context

### Revision and Positioning Workflow
1. `search_papers` — Verify claims about the literature
2. `get_paper_details` — Read abstracts of papers referees mention
3. `search_papers` (with `minYear`) — Check for new papers published since submission
4. `format_citation` — Format new references added during revision
