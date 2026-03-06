---
name: real-estate-empirical-design
description: "Design empirical strategies for real-estate research. Use for housing, mortgages, urban markets, commercial real estate, repeat sales, hedonic models, and spatial designs."
---

# Real Estate Empirical Design

Use this skill when property markets, mortgage institutions, spatial equilibrium, or local policy detail are central to the paper.

## Workflow

1. Define the economic object: property, borrower, lender, neighborhood, market, lease, REIT, or developer.
2. Define the institutional mechanism that creates the variation you want to study.
3. Specify geography and timing precisely.
4. Decide whether the setting calls for hedonic, repeat-sales, boundary, panel, hazard, event-study, or spatial equilibrium logic.
5. Address spatial dependence and equilibrium spillovers.
6. Address measurement issues unique to real-estate data.
7. Build the table, figure, and map plan.

## Design-method guidance by setting

### Hedonic price models
- Include structural characteristics (square footage, bedrooms, lot size, age, condition) and location attributes.
- Functional form matters: log-linear is standard but test sensitivity.
- Time dummies or time-tract interactions to control for market trends.
- Spatial fixed effects: tract, block group, or even street-level when data permit.
- Omitted variable bias is the core concern — what unobserved amenity or disamenity is correlated with both X and price?

### Repeat-sales designs
- Advantage: difference out time-invariant property characteristics.
- Key assumptions: no renovation bias, random timing of sales, constant property quality.
- Address: renovations between sales (use permit data if available), selected sample of properties that transact twice, and time between sales.
- Consider Case-Shiller weighted repeat-sales for index construction vs. unweighted for causal inference.

### Boundary discontinuity designs
- Ideal for: school districts, zoning boundaries, tax jurisdictions, flood zones, opportunity zones.
- Bandwidth choice: balance proximity (credibility) against sample size (power).
- Sorting: households sort across boundaries, so RD validity requires that sorting is smooth, not bunched.
- Test: Are observable characteristics balanced across the boundary? Is there bunching in the density of observations?

### Spatial difference-in-differences
- Treatment and control areas must be comparable before the shock.
- Ring-based designs: varying distance from a point source (new transit station, toxic site, development).
- Spatial spillovers can invalidate SUTVA — control units close to treated areas may be affected.
- Consider spatial buffers (donut holes) between treatment and control.
- Modern DiD considerations apply (staggered timing, heterogeneous effects) — see finance-identification-design skill.

### Mortgage and borrower-level designs
- Loan-level panels: address prepayment and default as competing risks.
- Origination-level studies: selection into loan products is endogenous.
- DTI, LTV, and FICO cutoffs create quasi-experimental variation (GSE conforming loan limits, QM thresholds).
- Hazard models: Cox vs. discrete-time logit; time-varying covariates; competing risks.

### Commercial real estate
- Cap rate decomposition: distinguish between discount rate and cash flow expectations.
- Lease-level analysis: tenant quality, lease duration, rent escalation clauses.
- REIT analysis: NAV discount/premium, dividend policy, capital structure decisions.
- Appraisal smoothing is severe in commercial data — use transaction-based measures when possible.

### Climate and environmental risk
- Flood zone reclassification as a natural experiment.
- Wildfire risk disclosure and pricing.
- Energy efficiency capitalization.
- Insurance market disruptions and property values.
- Sea-level rise expectations and coastal property markets.
- Challenge: separating risk pricing from amenity valuation (beach proximity vs. flood risk).

## High-priority measurement issues

| Issue | Context | Remedy |
|---|---|---|
| Transaction vs. listing price | MLS data contain both | Use transaction price for valuation; listing price for market-time studies |
| Appraisal smoothing | Commercial indices, refinance appraisals | Use transaction-based data; flag appraisal-based results |
| Property improvements | Repeat-sales, panel designs | Building permit data, satellite imagery, assessed improvement value changes |
| Boundary spillovers | RD designs near jurisdiction borders | Donut-hole buffers, test for gradient effects |
| Local-policy anticipation | Zoning changes, tax abatements | Date the legislative process, not the effective date |
| Repeat-observation selection | Properties that sell twice are not random | Compare transacted vs. non-transacted properties on observables |
| Spatial error correlation | Nearly all property-level studies | Conley (1999) standard errors, cluster at geographic level, spatial HAC |
| Geographic join errors | Geocoding, parcel matching | Validate match rates, hand-audit a random sample |

## Spatial inference

Standard errors in real estate research require special attention:
- **Conley (1999) spatial HAC**: when observations are spatially correlated but discrete clusters are inappropriate.
- **Cluster at geography**: MSA, county, tract, or ZIP depending on the level of the shock.
- **Two-way clustering**: geography and time when both dimensions create dependence.
- **Moulton (1990) concern**: if treatment varies at a higher level than the observation, cluster at the treatment level.

## Tool integration (Corbis MCP)

### Design precedents
- `search_papers` (query: the specific RE design, e.g., "boundary discontinuity school district house prices", `matchCount: 10`) → find published papers using comparable methods in real estate.
- `top_cited_articles` (journals: RE journals) → find seminal papers using comparable empirical designs in the real-estate literature.
- `get_paper_details` (paper IDs) → read how they handle spatial dependence, measurement, and identification.
### Data discovery
- `search_datasets` (query: "property transaction [geography]" or "mortgage origination") → find available data sources.
### Housing and macro context via FRED
- `fred_search` (keywords, e.g., "house price index" or "housing starts") → find relevant series.
- `fred_series_batch` (series IDs) → pull housing market context data.

**Key FRED series for RE research:**
| Purpose | Series IDs |
|---|---|
| National house prices | `CSUSHPISA` (Case-Shiller), `USSTHPI` (FHFA) |
| Metro-level HPI | `ATNHPIUS[MSA code]A` (FHFA metro) |
| Mortgage rates | `MORTGAGE30US`, `MORTGAGE15US` |
| Housing supply | `HOUST`, `PERMIT`, `MSACSR` |
| Rental markets | `CUUR0000SEHA` (CPI rent), `CUSR0000SEHC` (CPI OER) |
| Construction | `TLRESCONS` (residential construction spending) |

### CRE market intelligence (critical for commercial RE papers)
- `get_market_data` (metro name, e.g., "Dallas") → current cap rates, vacancy rates, rent growth, absorption, inventory, and construction pipeline for a metro.
- `compare_markets` (metro list, e.g., `["Dallas","Houston","Austin","San Antonio"]`) → side-by-side market comparison for cross-market studies or external validity assessment.
- `search_markets` (criteria, e.g., "lowest office vacancy" or "highest multifamily rent growth") → find metros matching specific research criteria for sample construction or natural experiment identification.

**Use CRE tools to:**
- Motivate the paper with current market conditions
- Validate that the sample period is representative of broader trends
- Identify treatment and control markets for cross-metro designs
- Provide institutional context for referee responses

### Citation management
- `export_citations` (format: `bibtex`) → export BibTeX entries for design precedent papers cited in the real-estate design memo (e.g., boundary-discontinuity, spatial DiD, or hedonic methodology references). Offer this after the design memo is produced.
- `format_citation` → format individual design-precedent citations for inline use in the memo.

## Deliverables

Produce:
- a real-estate design memo using assets/real-estate-design-template.md
- a threats-and-remedies table
- a map or visual checklist if relevant
- a spatial inference plan
- a results-plan outline with suggested table and figure sequence

## Output format

```
# Real-estate design memo
## Economic object and unit of analysis
## Institutional setting (detailed)
## Geography and timing
## Core design (with notation)
## Spatial or equilibrium concerns
## Measurement concerns (with remedies)
## Spatial inference plan
## Key visuals needed (maps, event-study plots)
## Identification threats (ranked)
## Safe interpretation
## What the design cannot claim
```

## Reference files
Read if needed:
- references/real-estate-methods.md
- references/journal-targets.md

## Guardrails

- Do not import generic finance-panel advice without checking local-market structure.
- Treat maps, zoning rules, lender institutions, and appraisal conventions as analytical inputs, not decoration.
- Say explicitly whether the result is property-level, borrower-level, neighborhood-level, or market-level.
- If the design depends on a boundary or local shock, discuss spillovers and sorting.
- Do not use standard OLS standard errors in spatially correlated data.
- Flag when the geographic scope limits external validity.
- If using hedonic regressions, discuss omitted variable bias seriously.

## Example prompts
- "Stress-test this repeat-sales design for a gentrification paper."
- "How should I handle spatial correlation in a commercial-real-estate vacancy study?"
- "Turn this zoning shock idea into a top-journal real-estate design memo."
- "Design a boundary discontinuity around opportunity zone boundaries."
- "What's the right way to study climate risk capitalization in housing prices?"
