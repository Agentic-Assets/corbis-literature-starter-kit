---
name: asset-pricing-test-suite
description: "Run the core workflow for empirical asset-pricing papers. Use for anomalies, factors, portfolio sorts, alphas, Fama-MacBeth tests, turnover, and validation."
---

# Asset Pricing Test Suite

Use this skill for signal, anomaly, factor, or return-predictability papers.

## Workflow

1. Define the signal exactly — variable name, source, construction, and economic rationale.
2. Specify timing: signal observation date, portfolio formation date, holding period, skip period, and rebalancing frequency.
3. Choose breakpoints (NYSE percentiles preferred) and weighting conventions (value-weighted preferred, equal-weighted as robustness).
4. Build the portfolio-sort logic (univariate, bivariate independent, bivariate dependent).
5. Choose benchmark factor models for alpha attribution.
6. Plan cross-sectional tests if needed.
7. Assess implementability: turnover, capacity, liquidity, and trading costs.
8. Separate discovery evidence from validation evidence.

## Factor model benchmarks

Use the appropriate benchmarks for the paper's contribution:

| Model | Factors | When to use |
|---|---|---|
| CAPM | MKT | Baseline only |
| Fama-French 3 | MKT, SMB, HML | Legacy benchmark |
| Carhart 4 | MKT, SMB, HML, UMD | When momentum exposure matters |
| Fama-French 5 | MKT, SMB, HML, RMW, CMA | Current standard for most papers |
| Fama-French 6 | FF5 + UMD | When momentum is relevant |
| q-factor (HXZ) | MKT, ME, I/A, ROE | Alternative to FF5; investment-based |
| q5 | q-factor + expected growth | Most recent HXZ model |
| Mispricing factors (Stambaugh-Yuan) | MKT, SMB, MGMT, PERF | When testing behavioral vs. rational |
| DHS 3-factor | MKT, FIN, PEAD | Behavioral benchmark |

Report at minimum: CAPM, FF3, FF5, and one of q-factor or FF6. If the signal is behavioral, add mispricing factors.

## Standard test families

### Portfolio sorts
- Univariate sorts: typically quintiles or deciles using NYSE breakpoints
- Long-short portfolio: long top quintile/decile, short bottom
- Report: mean excess returns, alphas against each model, t-statistics (Newey-West with appropriate lags)
- Bivariate sorts when needed to control for known predictors

### Time-series alpha regressions
- Regress long-short portfolio returns on factor models
- Report alpha, factor loadings, and adjusted R-squared
- Use Newey-West standard errors (lag = 0.75 * T^(1/3) or similar)
- GRS test for joint alpha significance across portfolios when relevant

### Cross-sectional tests
- Fama-MacBeth regressions: cross-sectional regression each month, then time-series average of coefficients
- Report Newey-West adjusted t-statistics for the time-series average
- Include standard controls: size, book-to-market, momentum, profitability, investment
- Alternatively: characteristic-sorted portfolio spanning tests

### Factor spanning / redundancy
- If proposing a new factor: does it survive when added to existing models?
- Test whether the new factor's alpha is significant controlling for existing factors
- Test whether existing anomalies' alphas are reduced when the new factor is added
- Maximum Sharpe ratio tests (Barillas and Shanken 2018)

## Implementability assessment

This section is mandatory. A signal with a large alpha but no implementable strategy is an incomplete paper.

- **Turnover**: Report monthly portfolio turnover. Above 50%/month is a red flag.
- **Capacity**: Is the strategy concentrated in microcaps? Report the fraction of long-short return from stocks below NYSE 20th percentile.
- **Microcap exclusion**: Re-run the main test excluding microcaps (typically below NYSE 20th percentile or $100M market cap). If the result vanishes, flag this prominently.
- **Liquidity**: Report the average bid-ask spread and Amihud illiquidity of the long and short legs.
- **Trading costs**: Use at minimum a simple proportional cost model. Consider Novy-Marx and Velikov (2016) or DeMiguel et al. (2020) for more sophisticated cost estimation.
- **Short-leg feasibility**: Is the short leg composed of hard-to-borrow stocks? Check against shorting-fee data if available.

## Validation and replication concerns

- **Out-of-sample**: Test in a holdout time period (pre-discovery or post-publication).
- **International**: Test in international markets if data permit.
- **Post-publication decay**: If replicating a known anomaly, report post-publication performance.
- **Data snooping**: If many signals were searched, address multiple-testing risk (Harvey, Liu, and Zhu 2016 t-statistic threshold of ~3.0; Chordia, Goyal, and Saretto 2020).
- **Anomaly zoo context**: Position the signal relative to the Chen-Zimmermann (2022) open-source asset pricing project and existing anomaly databases.
- **Machine learning complement**: Consider whether ML methods (Gu, Kelly, and Xiu 2020) capture the same return predictability or whether the signal adds incremental information.

## Tool integration (Corbis MCP)

### Signal novelty verification (mandatory before proceeding)
1. `search_papers` (query: the signal name + "return predictability" or "cross-section of returns", `matchCount: 15`) → check whether the signal or a close variant has been documented.
2. `search_papers` (query: the economic mechanism behind the signal, `matchCount: 10`) → find papers with different signals but the same mechanism.
3. `get_paper_details` (paper IDs from top results) → read abstracts to determine true overlap vs. superficial similarity.

### Anomaly zoo context
- `top_cited_articles` (field: "asset pricing", topic: "anomalies" or "return predictability") → identify the canonical papers the user must cite and benchmark against.

### Macro conditioning variables
- `fred_search` (keywords like "investor sentiment" or "market volatility") → find series for conditional tests.
- `fred_series_batch` (series IDs, e.g., `["VIXCLS","BAMLC0A0CM","T10Y2Y","UMCSENT"]`) → pull conditioning variables for time-series variation tests.

### Literature for methodology
- `search_papers` (query: specific methodology, e.g., "Fama-MacBeth Newey-West", `minYear: 2018`) → find recent applied examples of the testing framework.
- `export_citations` (format: `bibtex`) → export BibTeX entries for methodological and anomaly-zoo references cited in the test matrix and contribution statement (e.g., Harvey-Liu-Zhu, Chen-Zimmermann, Gu-Kelly-Xiu). Offer this after the test matrix is produced.
- `format_citation` → format individual references for the anomaly-positioning discussion.

## Deliverables

Produce:
- an asset-pricing test matrix using assets/ap-test-matrix-template.md
- a table and figure plan
- a statement of the likely contribution and how it advances the literature
- a list of standard objections with pre-planned responses
- suggested Stata/R/Python code structure for the main tests

## Output format

```
# Asset-pricing analysis plan
## Signal definition (exact formula, source, timing)
## Construction choices (breakpoints, weighting, rebalancing)
## Baseline return tests (univariate sorts)
## Factor benchmark tests (alphas against each model)
## Cross-sectional pricing tests (Fama-MacBeth)
## Factor spanning / redundancy tests
## Implementability checks (turnover, capacity, microcaps, costs)
## Validation checks (out-of-sample, international, post-publication)
## Data-snooping assessment
## Interpretation limits
```

## Reference files
Read if needed:
- references/asset-pricing-norms.md
- references/writing-norms.md

## Guardrails

- Do not treat a highly significant alpha as economically meaningful without discussing implementability.
- Do not mix discovery and validation samples casually.
- Be explicit about microcap exposure, liquidity, and turnover.
- If many signals were searched, address multiple-testing risk — a t-statistic of 2.0 is not enough.
- Do not claim a new "factor" without spanning tests showing it is not redundant to existing factors.
- Do not ignore the post-2004 decline in many anomalies.
- Flag when results are driven primarily by the short leg, which is harder to implement.

## Example prompts
- "Design the full empirical test suite for this new characteristic."
- "How should I validate an anomaly after 2003?"
- "What tables does an empirical factor paper need?"
- "Is my signal just a relabeled version of profitability?"
- "Assess the implementability of this high-turnover strategy."
