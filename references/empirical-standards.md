# Empirical Standards

## Idea screening

### Design feasibility check
- Can you define the estimand in one sentence?
- Is there a plausible source of exogenous or quasi-exogenous variation?
- Can you name the comparison group and explain why it is informative?
- Can you write a baseline specification? If not, the idea is too vague.

### Data feasibility check
- Does the data exist and can you access it within a reasonable timeframe?
- Is the sample large enough? (Rule of thumb: N > 1000 cross-sectional, T > 20 time-series, clusters > 50.)
- Are the key variables measurable, or do they require heroic proxies?
- Is there look-ahead bias risk in the proposed variable construction?

### Common idea killers
- The variation is endogenous and no credible instrument or natural experiment is available.
- The data are too noisy or too small for the magnitude of the expected effect.
- The closest paper already answers the question convincingly with better data or identification.
- The mechanism cannot be distinguished from obvious alternatives.

## Data construction

### Sample construction
- Define the unit of observation, sampling frame, and time aggregation before any merges.
- Document every filter and exclusion with observation counts at each step.
- Build a sample-flow table: raw N -> after filter 1 -> ... -> final N.
- Justify each exclusion with an economic or statistical reason.

### Identifier integrity
- Verify identifier uniqueness at the intended unit of observation.
- For CRSP-Compustat merges: use CCM link table, primary links only, within valid date ranges.
- For CRSP-IBES: use ICLINK, prefer score=1 matches.
- For real estate: validate parcel IDs, address matches, and geocoding accuracy.
- Document unmatched observation rates at every merge step. Flag rates above 10-15%.

### Variable construction
- Define every variable in the codebook before running regressions.
- Include: exact formula, source fields, sample restrictions, transformations.
- Be explicit about scaling: per-share, per-dollar-of-assets, logged, standardized.
- Note when log transformations drop zeros and how zeros are handled.

### Date alignment and look-ahead bias
- Standard lag for annual Compustat: 4-6 months after fiscal year end.
- For quarterly data: at least 45 days after quarter end.
- Flag any potential look-ahead issues explicitly.

### Winsorization and outliers
- Do not winsorize by default. Justify the level if used.
- Typical levels: 1%/99% or 5%/95%, cross-sectional within each period.
- Report results with and without winsorization.

## Identification design

### Before estimation
- Define the unit of observation, sampling frame, and time aggregation.
- Write down the estimand in plain English and in notation.
- Define treatment, outcome, timing, and comparison set.

### Baseline specification
- State the baseline specification in notation and plain English.
- Explain fixed effects, clustering, and variation used for identification.
- Tie each control to a threat or precision goal — no kitchen-sink controls.
- Standard errors clustered at the level of treatment variation.

### Modern methods checklist
- **Staggered DiD**: Consider Callaway-Sant'Anna, Sun-Abraham, or Borusyak-Jaravel-Spiess. TWFE is biased under heterogeneous treatment effects.
- **Pretrends**: Roth (2022) sensitivity analysis. Conventional pre-trend tests are low-powered.
- **IV**: Report effective F-statistic (Olea-Pflueger). Discuss LATE interpretation.
- **RD**: Calonico-Cattaneo-Titiunik bandwidth, McCrary density test, plot raw data.
- **Shift-share**: GPSS (2020) or BHJ (2022) framework.
- **Sensitivity**: Oster (2019) bounds for selection on unobservables.
- **Clustering**: AAIW (2023) guidance on when to cluster.

## Analysis

### Interpretation protocol
For every main result:
1. State the result (what happened)
2. Name the specification (controls, FE, sample)
3. Quantify the magnitude (SD change, dollar amount, percentage relative to mean)
4. Interpret cautiously (what the result is consistent with)
5. State the limit (what the design cannot claim)

### Robustness logic
- Only run checks that address a real, named threat.
- Group by threat category: measurement, comparison group, FE, sample, timing, placebo, channel, inference.
- A robustness check without a named threat is uninformative.

### Mechanism evidence
- State the hypothesized channel before testing it.
- Distinguish mechanism tests from heterogeneity patterns. Heterogeneity is suggestive, not proof.
- Discuss at least one competing channel seriously.

### Table construction
- Each table should have a single purpose.
- Summary statistics: means, SDs, medians, p25/p75, N. Treatment-control comparison if relevant.
- Baseline: build up specifications. Show the preferred specification clearly.
- Robustness: organize by threat, not by arbitrary specification number.

## Reproducibility
- Number scripts and tables consistently.
- Every table should be reproducible from a single script run.
- Maintain a variable dictionary (codebook).
- Keep a merge audit and unmatched-observation report.
- Preserve a one-command path from raw data to final tables.
