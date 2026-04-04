# Corbis MCP Tool Reference

Complete reference for all Corbis MCP tools. Use this guide to understand each tool's parameters, output shape, and best practices.

> **Setup**: See [CORBIS_MCP_CLAUDE_CODE_GUIDE.md](./CORBIS_MCP_CLAUDE_CODE_GUIDE.md) for connection setup.
> **Tier 1** = all users. **Tier 2** = enterprise only. Every tool call costs **1 credit**.

---

## Research & Papers

### `search_papers` (Tier 1)

Hybrid semantic + keyword search across ~250K academic papers. Uses Reciprocal Rank Fusion (RRF) to combine vector similarity and full-text search.

| Param | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `query` | string | Yes | — | 1–500 chars. Search terms. |
| `matchCount` | number | No | 10 | 1–20. Number of results. |
| `minYear` | number | No | — | Filter: earliest publication year. |
| `maxYear` | number | No | — | Filter: latest publication year. |
| `journalNames` | string[] | No | — | Max 10. Case-insensitive partial match. |
| `sortBy` | enum | No | `"relevance"` | `"relevance"` \| `"citedByCount"` \| `"year"` |
| `compact` | boolean | No | `false` | Strips abstracts and scores to reduce payload. |
| `rrfK` | number | No | 25 | RRF ranking parameter. Rarely needs changing. |

**Returns**: `results[]` with `id`, `title`, `authors`, `year`, `journal`, `abstract`, `doi`, `openalexId`, `url`, `citedByCount`, `semanticScore`, `keywordScore`, `combinedRank`. In compact mode, abstract and scores are null.

**Tips**:
- Use `compact: true` when you only need titles/metadata (saves ~80% payload).
- `sortBy: "citedByCount"` is useful for finding seminal papers on a topic.
- Combine `journalNames` with `query` to search within specific journals.
- For broad literature surveys, prefer `literature_search` (enterprise) which runs multiple queries automatically.

---

### `get_paper_details` (Tier 1)

Full metadata for a single paper. Accepts UUID, OpenAlex ID (`W123456`), DOI, or full URLs.

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `paperId` | string | Yes | UUID, OpenAlex ID, DOI, or URL containing one of these. |

**Returns**: `id`, `title`, `authors`, `year`, `journal`, `abstract`, `fullText`, `doi`, `openalexId`, `url`, `citedByCount`, `metadata`.

**Tips**:
- Accepts URLs directly: `https://openalex.org/W123456` or `https://doi.org/10.1234/...`
- Falls back to hybrid search if exact ID lookup fails.
- For multiple papers, use `get_paper_details_batch` instead (one call vs. many).

---

### `get_paper_details_batch` (Tier 1)

Fetch up to 25 papers in a single call. Groups IDs by type and runs parallel queries.

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `paperIds` | string[] | Yes | 1–25 items. Mix of UUIDs, OpenAlex IDs, and DOIs. |

**Returns**: `results[]` (same fields as `get_paper_details` plus `requestedId`), `errors[]` (`paperId` + `error` message), `totalRequested`, `totalFound`.

**Tips**:
- Partial success is normal — check both `results` and `errors`.
- Much more efficient than calling `get_paper_details` 25 times.
- Good for enriching search results: search first, then batch-fetch full details.

---

### `top_cited_articles` (Tier 1)

Rank the most-cited papers within specific journals. Optionally filter by topic.

| Param | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `journalNames` | string[] | Yes | — | Min 1, max 10. Journals to search. |
| `query` | string | No | — | Topic filter (combines keyword + semantic matching). |
| `minYear` | number | No | — | Earliest publication year. |
| `maxYear` | number | No | — | Latest publication year. |
| `limit` | number | No | 10 | 1–50. Max results. |
| `compact` | boolean | No | `true` | **Default is true for MCP.** Set `false` to include abstracts. |

**Returns**: `results[]` with `id`, `title`, `authors`, `year`, `journal`, `abstract`, `doi`, `openalexId`, `url`, `citedByCount`, `rank`. Also: `journalsMatched`, `journalsUnmatched`, `journalSuggestions`, `totalFound`, `yearRange`.

**Tips**:
- If a journal name doesn't match, check `journalSuggestions` for close matches.
- Use `query` to narrow from "all highly-cited papers in Journal X" to "highly-cited papers on [topic] in Journal X".
- Compact mode is on by default — set `compact: false` if you need abstracts.

---

### `literature_search` (Tier 2 — Enterprise)

AI-powered multi-step literature review. Runs iterative searches, aggregates findings, and synthesizes a narrative with citations.

| Param | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `researchQuestion` | string | Yes | — | 1–500 chars. Main research question. |
| `maxSteps` | number | No | 3 | 1–10. More steps = broader coverage. |
| `focusAreas` | string[] | No | — | Themes to prioritize in the search. |

**Returns**: `summary` (narrative with `[1]`, `[2]` citations), `papers[]`, `themes`, `searchQueries`, `searchesPerformed`, `totalSearched`.

**Tips**:
- Start with `maxSteps: 3` (default). Increase to 5–7 for comprehensive surveys.
- `focusAreas` steers the search — e.g., `["methodology", "empirical results"]`.
- The `summary` uses numbered citations that map to the `papers` array.

---

### `search_datasets` (Tier 1)

Search free finance research datasets by topic.

| Param | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `query` | string | Yes | — | Dataset search terms. |
| `matchCount` | number | No | 5 | 1–20. Number of results. |
| `topicFilter` | string | No | — | e.g., `"CRE"`, `"bonds"`, `"housing"`. |
| `regionFilter` | string | No | — | e.g., `"U.S."`, `"global"`. |

**Returns**: `results[]` with `name`, `description`, `link`, `accessInfo`, `dataType`, `tags`.

---

## Economic Data (FRED)

### `fred_search` (Tier 1)

Search the Federal Reserve Economic Database for series metadata. Use this first to find correct series IDs.

| Param | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `query` | string | Yes | — | 1–200 chars. e.g., `"unemployment rate"`, `"housing starts"`. |
| `limit` | number | No | 10 | 1–50. |

**Returns**: `results[]` with `id` (FRED series ID like `"UNRATE"`), `title`, `frequency`, `units`, `observationStart`, `observationEnd`.

**Tips**:
- Always search first to confirm the correct series ID before fetching data.
- Check `frequency` and `units` to verify you have the right series.

---

### `fred_series_batch` (Tier 1)

Fetch actual time series data for 1–15 FRED series. Returns data and injects Python DataFrames into the code execution context.

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `items` | object[] | Yes | 1–15 series requests. |
| `items[].seriesId` | string | Yes | FRED series ID (e.g., `"CSUSHPISA"`). |
| `items[].observationStart` | string | No | ISO date `YYYY-MM-DD`. |
| `items[].observationEnd` | string | No | ISO date `YYYY-MM-DD`. |
| `items[].units` | string | No | Unit transform: `"pch"` (% change), `"log"`, etc. |
| `items[].frequency` | string | No | Resample: `"M"`, `"Q"`, `"A"`. |
| `items[].aggregationMethod` | string | No | `"average"`, `"sum"`, `"eop"`. |

**Returns**: `ok`, `seriesCount`, `perSeries[]` (status per series), `series[]` (metadata + variable names), `aliases`, `dataset`.

**Critical**: The Python code injection is **ephemeral** — tied to the current execution session. You **must** create a fresh code artifact immediately after calling this tool. Do not update existing code artifacts that reference different data.

---

## Market Intelligence

### `get_market_data` (Tier 1)

CRE snapshot for a single U.S. metro area. Returns metrics, rankings, strengths/weaknesses.

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `market` | string | Yes | City name (e.g., `"Austin, TX"`), CBSA code (e.g., `"12580"`), or region. |

**Returns**: `market`, `metrics` (jobs, composite score, multifamily demand, 5Y CAGR, etc.), `rankings`, `strengths`, `weaknesses`, `benchmarks`, optional `narrative`, `peers`, `historical_snapshots`.

---

### `compare_markets` (Tier 1)

Side-by-side comparison of 2–10 metros.

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `markets` | string[] | Yes | 2–10 city names or CBSA codes. |
| `metrics` | string[] | No | Specific metrics to compare. Default: all. |

---

### `search_markets` (Tier 1)

Rank metros by any CRE metric. Great for "top 10 markets by job growth".

| Param | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `metric` | string | Yes | — | e.g., `"jobs_yoy"`, `"composite_score"`. |
| `order` | enum | No | `"top"` | `"top"` or `"bottom"`. |
| `limit` | number | No | 10 | 1–50. |
| `min_percentile` | number | No | — | 0–100. Filter by percentile floor. |
| `max_percentile` | number | No | — | 0–100. Filter by percentile ceiling. |
| `region` | string | No | — | Filter by region. |
| `market_tier` | string | No | — | Filter by market classification. |

---

### `get_national_macro` (Tier 1)

National macro time series: GDP, CPI, Treasury rates, mortgage rates, Fed funds.

| Param | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `series_id` | enum | No | — | `"GDPC1"` \| `"CPIAUCSL"` \| `"DGS10"` \| `"DGS2"` \| `"MORTGAGE30US"` \| `"FEDFUNDS"` |
| `start_date` | string | No | — | `YYYY-MM-DD`. |
| `end_date` | string | No | — | `YYYY-MM-DD`. |
| `limit` | number | No | 100 | 1–500 observations. |

---

### `get_market_trends` (Tier 1)

Metro-level historical time series from BLS, Zillow, BEA, Census, FHFA, HUD, IRS. Deeper history than snapshots.

| Param | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `cbsa_code` | string | Yes | — | 5-digit CBSA code (e.g., `"12580"` for Austin). |
| `source` | string | No | — | e.g., `"bls_employment"`, `"zillow"`. |
| `metric` | string | No | — | Specific metric key. |
| `start_date` | string | No | — | `YYYY-MM-DD`. |
| `end_date` | string | No | — | `YYYY-MM-DD`. |
| `limit` | number | No | 500 | 1–2000. |

---

## Web & Deep Research (Tier 2 — Enterprise)

### `internet_search`

Real-time web search via Perplexity AI. Returns a summary with source citations.

| Param | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `query` | string | Yes | — | 1–500 chars. |
| `maxResults` | number | No | 14 | 2–14 sources. |

**Returns**: `summary` (with `[1]`, `[2]` citations), `sources[]` (`title`, `url`, `snippet`, `sourceName`, `publicationDate`).

**Tip**: For thorough coverage, run 2–3 parallel searches with different angles on the same topic.

---

### `read_web_page`

Extract full content from a URL as clean markdown.

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `url` | string | Yes | Full URL to extract. |

**Returns**: `content` (markdown), `metadata` (title, author, language, etc.).

---

### `deep_research`

Multi-engine research: Tavily discovery → Perplexity ranking → Firecrawl extraction.

| Param | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `query` | string | Yes | — | Research query. |
| `maxExtractions` | number | No | 3 | 1–5. How many top sources to fully extract. |

**Returns**: `synthesis`, `sources[]` (with `extractedContent`), `engines_used`, `totalSourcesFound`, `sourcesExtracted`.

---

## Citations

### `format_citation` (Tier 1)

Format 1–50 papers in APA 7, MLA 9, Chicago 17, Harvard, or BibTeX.

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `papers` | object[] | Yes | 1–50 items. Each needs at least `title`. Optional: `authors`, `year`, `journal`, `volume`, `issue`, `pages`, `doi`, `url`, `publisher`. |
| `style` | enum | Yes | `"apa"` \| `"mla"` \| `"chicago"` \| `"harvard"` \| `"bibtex"` |

**Returns**: `citations[]` (formatted strings), `style`, `count`.

---

### `export_citations` (Tier 1)

Generate citation files (BibTeX `.bib`, Markdown `.md`, JSON `.json`). Output `content` is ready to write to disk.

| Param | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `citations` | object[] | Yes | — | Paper records with `title`, optional `authors`, `year`, `journal`, `doi`, `url`, `abstract`. |
| `formats` | enum[] | No | `["bibtex","markdown"]` | Which formats to generate. |
| `fileName` | string | No | — | Base filename (alphanumeric, `-`, `_`, `.` only). |
| `includeAbstract` | boolean | No | `false` | Include abstracts in BibTeX/JSON output. |

**Returns**: `exports[]` with `format`, `filename`, `content` (write directly to disk), `bytes`.

---

## Academic Identity

### `find_academic_identity` (Tier 1)

Search for the user's OpenAlex author profile. Returns the best candidate for review.

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `nameOverride` | string | No | Override display name for search. |
| `institutionOverride` | string | No | Override institution for search. |

**Returns**: `candidate` (with `authorId`, `name`, `institution`, `hIndex`, `citedByCount`, `papersCount`, `confidenceScore`), `status`.

---

### `confirm_academic_identity` (Tier 1)

Link or unlink the user's account to an OpenAlex author ID. Use after `find_academic_identity`.

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `action` | enum | Yes | `"accept"` (link) or `"clear"` (unlink). |
| `authorId` | string | Conditional | Required when `action: "accept"`. OpenAlex author ID. |
| `authorName` | string | No | Author display name. |
| `confidenceScore` | number | No | 0–100. |

---

## General

### `query_corbis` (Tier 2 — Enterprise)

Free-form question answered by Corbis's agentic AI. Automatically calls other tools as needed and synthesizes a response.

| Param | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `query` | string | Yes | — | 1–4000 chars. Any research question. |
| `modelId` | string | No | — | Model override (e.g., `"claude-sonnet-4-6"`). |
| `maxSteps` | number | No | 6 | 1–10. Reasoning/tool steps. |
| `maxOutputTokens` | number | No | 6000 | 256–6000. |

**Returns**: `text`, `modelId`, `steps`, `toolsUsed`, `finishReason`, `usage`.

**Tip**: This is the "do everything" tool. Use it for open-ended questions where you're not sure which specific tools to call.

---

## Recommended Workflows

### Literature Review
1. `search_papers` with your topic → get initial results
2. `top_cited_articles` with relevant journals → find seminal works
3. `get_paper_details_batch` with IDs from steps 1–2 → full metadata
4. `format_citation` or `export_citations` → generate bibliography

### Market Analysis
1. `search_markets` → find top metros by your metric
2. `get_market_data` for each top metro → detailed snapshots
3. `compare_markets` → side-by-side comparison
4. `get_market_trends` with CBSA codes → historical context
5. `get_national_macro` → national backdrop

### Economic Data Visualization
1. `fred_search` → find correct series IDs
2. `fred_series_batch` → fetch data (creates Python DataFrames)
3. Create a **new** code artifact immediately to use the injected data

### Research with Web Sources
1. `search_papers` → academic foundation
2. `internet_search` → current market data, news, regulations
3. `read_web_page` → extract specific sources in full
4. `deep_research` → comprehensive multi-source synthesis

---

## Rate Limits & Response Metadata

- **200 requests/hour** per authenticated user
- **10 concurrent requests** max
- Every response includes `_meta.responseChars` indicating payload size
- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

---

## MCP Resources (Read-Only)

These documentation resources are available via `resources/read`:

| URI | Description |
|-----|-------------|
| `docs://system` | Server overview, paper schema, auth, rate limits |
| `docs://tools` | Quick tool reference |
| `docs://auth` | Authentication methods and error codes |
| `docs://quickstart` | 5-minute getting started guide |
| `docs://data-sources` | Market data sources (BLS, Census, FHFA, HUD, BEA, IRS) |
| `docs://workflows` | Paper Reviews, Investment Memos, Market Outlooks |
| `docs://mcp-guide` | Multi-platform MCP integration guide |
| `docs://pricing` | Subscription tiers and credit details |
