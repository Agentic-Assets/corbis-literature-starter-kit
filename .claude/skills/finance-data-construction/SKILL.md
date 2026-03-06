---
name: finance-data-construction
description: "Plan data sourcing, merges, variables, codebooks, and reproducibility for finance and real-estate projects. Use for sample construction, identifier mapping, and audit trails."
---

# Finance Data Construction

Treat sample construction and variable definitions as part of the contribution, not as a back-office chore.

## Workflow

1. List the raw data sources with exact access paths and vintage dates.
2. State the unit of observation after each merge stage.
3. Define join keys and likely failure points (identifier mismatches, timing gaps, coverage holes).
4. Build a sample-flow diagram showing observation counts at each stage.
5. Define all main variables and transformations with explicit formulas.
6. Record missingness, outlier, and winsorization rules with justification.
7. Create a merge audit and unmatched-observation plan.
8. Design the folder and script architecture for reproducibility.
9. Plan the data appendix.

## Common source families

### Finance data
- **Equity**: CRSP (returns, delisting, shares), Compustat (fundamentals), merged via CCM link table (PERMNO-GVKEY)
- **Analyst/Earnings**: IBES (recommendations, forecasts, actuals), linked to CRSP via ICLINK
- **Deals/Lending**: SDC Platinum (M&A, IPOs, SEOs), Dealscan (syndicated loans, linked via Roberts Dealscan-Compustat link), Capital IQ
- **Fixed income**: TRACE (corporate bonds), Mergent FISD (bond characteristics), WRDS Bond Returns
- **Microstructure**: TAQ (trades and quotes), LOBSTER (limit order book)
- **Ownership/Governance**: 13F (institutional holdings), ISS/RiskMetrics (governance, directors), proxy statements
- **Mutual funds/Hedge funds**: CRSP Mutual Fund Database, Morningstar, Lipper, HFR, Preqin
- **Options**: OptionMetrics (IvyDB)
- **Text/NLP**: SEC EDGAR filings (10-K, 10-Q, 8-K, proxy), earnings call transcripts, news archives
- **ESG**: MSCI ESG, Sustainalytics, CDP, Trucost
- **Alternative data**: Satellite imagery, web traffic, credit card transactions, social media, patent data (USPTO/PATSTAT)
- **Macro**: FRED (via `fred_search` and `fred_series_batch`), BEA, BLS

### Real-estate data
- **Transaction**: Assessor records (county or vendor: CoreLogic, ATTOM, Zillow ZTRAX), deeds/recordings, MLS data
- **Commercial**: CoStar (rents, vacancies, cap rates), Real Capital Analytics (transactions), NCREIF (institutional returns), CMBS servicer data
- **Mortgage**: HMDA (originations), loan-level agency data (Freddie Mac LLPD, Fannie Mae), Black Knight/ICE McDash, CoreLogic LoanPerformance
- **Geographic**: Census (ACS, decennial), LODES (employment), FHFA HPI, Zillow indices, parcel/GIS shapefiles
- **Zoning/Policy**: Municipal zoning codes, building permits, rent control registries, opportunity zone boundaries, tax abatement records
- **Climate/Environmental**: FEMA flood maps, wildfire risk data, air quality indices, energy efficiency ratings

## Identifier mapping — common pitfalls

| Merge | Key | Known issues |
|---|---|---|
| CRSP-Compustat | PERMNO-GVKEY via CCM | Multiple GVKEYs per PERMNO; use primary link only; watch link date ranges |
| CRSP-IBES | PERMNO-TICKER via ICLINK | Ticker reuse; use score=1 links preferentially |
| Dealscan-Compustat | Roberts link table | Coverage declines for recent years; manual matching may be needed |
| TRACE-FISD | CUSIP | TRACE 144A and when-issued bonds; cleaning required (Dick-Nielsen methodology) |
| Real estate: assessor-deeds | Parcel ID / APN | Format varies by county; fuzzy address matching often needed |
| Real estate: MLS-assessor | Address matching | Geocoding errors; unit-level vs. property-level mismatches in condos |
| Mortgage: HMDA-assessor | Census tract + loan characteristics | Probabilistic matching only; no universal loan ID across datasets |

## Variable construction standards

- **Define every variable in the codebook** before running regressions. Include: exact formula, source fields, sample restrictions, and any transformations.
- **Winsorization**: Do not winsorize by default. If used, justify the level (typically 1% or 5%), report results with and without, and note whether the winsorization is cross-sectional or pooled.
- **Scaling**: Be explicit about whether variables are per-share, per-dollar-of-assets, or logged. Note when log transformations drop zeros.
- **Date alignment**: Ensure accounting data are available at the time of portfolio formation or the regression date. Use a minimum lag (typically 4-6 months for annual Compustat) to avoid look-ahead bias.
- **Industry codes**: Specify SIC vs. NAICS vs. FF industry classification and the vintage used.

## Code architecture

Recommend this folder structure for reproducibility:
```
project/
  raw/           # Untouched source files (read-only)
  build/         # Scripts that clean and merge (numbered: 01_clean_crsp.do, etc.)
  analysis/      # Scripts that produce tables and figures
  output/        # Tables, figures, logs
  codebook/      # Variable definitions and sample documentation
  docs/          # Data appendix, merge audit
```

When generating code, default to Python. Use clear variable names, comment every non-obvious step, and log all output.

## Tool integration (Corbis MCP)

### Data discovery
- `search_datasets` (topic keywords, e.g., "mortgage origination loan level") → discover datasets, coverage periods, and access paths.

### Macro variables via FRED
- `fred_search` (keywords, e.g., "house price index national") → find the right FRED series.
- `fred_series_batch` (series IDs as a list) → pull multiple series at once for controls, context, or sample period validation.

**Common FRED series for finance/RE research:**
| Purpose | Series IDs |
|---|---|
| Housing prices | `CSUSHPISA` (Case-Shiller National), `USSTHPI` (FHFA HPI) |
| Mortgage rates | `MORTGAGE30US`, `MORTGAGE15US`, `MORTGAGE5US` |
| Credit conditions | `DRTSCILM` (bank lending standards), `BAMLC0A0CM` (IG spread) |
| Macro controls | `UNRATE`, `GDPC1`, `CPIAUCSL`, `FEDFUNDS`, `T10Y2Y` |
| CRE indicators | `BOGZ1FL075035503Q` (CRE loans), `COMREPUSQ159N` (CRE price index) |
| Housing supply | `HOUST` (starts), `PERMIT` (permits), `MSACSR` (months supply) |

### Literature for data methods
- `search_papers` (query: "[dataset] [merge methodology]", e.g., "TRACE Dick-Nielsen corporate bond", `matchCount: 5`) → find methodological papers for data cleaning and construction.
- `get_paper_details` (paper IDs) → read how published papers describe their data construction.
- `export_citations` (format: `bibtex`) → export BibTeX entries for data methodology references cited in the construction plan (e.g., Dick-Nielsen for TRACE cleaning, Roberts for Dealscan-Compustat linking). Offer this after the data construction plan is produced.
- `format_citation` → format individual data-method citations for the codebook or data appendix.

### For real-estate data projects
- `get_market_data` (metro name) → current CRE market fundamentals to validate sample period representativeness.
- `compare_markets` (metro list) → compare market conditions across study geographies.

## Required outputs

Produce:
- a sample-construction memo with observation counts at each stage
- a variable dictionary using assets/codebook-template.md
- a merge audit checklist with expected and actual match rates
- a folder and script architecture plan
- a data appendix outline

## Output format

```
# Data construction plan
## Raw sources (with access paths and vintage)
## Join logic (with keys and expected match rates)
## Sample filters (with observation counts)
## Sample flow diagram
## Core variables (with formulas)
## Missingness and outliers (with justification)
## Reproducibility plan (folder structure and script sequence)
## Merge-risk diagnostics
## Data appendix material
```

## Reference files
Read if needed:
- references/empirical-standards.md
- references/real-estate-methods.md

## Guardrails

- Do not treat winsorization as default. Explain why it is used.
- Be explicit about date alignment and look-ahead risk.
- If an identifier bridge is fragile, say so early and quantify the expected match rate.
- For real-estate work, be especially careful about property identifiers, geography joins, and repeat observations.
- Flag survivorship bias in any panel dataset.
- Note when a data source has known coverage gaps (e.g., TRACE before Phase 3, Dealscan after 2017).
- If the user's merge strategy would lose more than 20% of observations, flag it and suggest diagnostics.

## Example prompts
- "Help me merge Compustat, CRSP, and bond data for a capital-structure paper."
- "Build a sample-construction plan for MLS, assessor, and zoning data."
- "Create a codebook and merge audit for this private-credit dataset."
- "What's the right way to link HMDA to property-level data?"
- "Design the data pipeline for a paper using TRACE corporate bond data."
