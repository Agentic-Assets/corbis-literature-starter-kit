# Empirical Standards for Data Construction

## Sample construction
- Define the unit of observation, sampling frame, and time aggregation before any merges.
- Document every filter and exclusion with observation counts at each step.
- Build a sample-flow table: raw N -> after filter 1 -> after filter 2 -> ... -> final N.
- Justify each exclusion with an economic or statistical reason.

## Identifier integrity
- Verify identifier uniqueness at the intended unit of observation.
- For CRSP-Compustat merges: use CCM link table, primary links only, within valid date ranges.
- For CRSP-IBES: use ICLINK, prefer score=1 matches.
- For real estate: validate parcel IDs, address matches, and geocoding accuracy on a random audit sample.
- Document unmatched observation rates at every merge step. Flag rates above 10-15%.

## Variable construction
- Define every variable in the codebook before running regressions.
- Include: exact formula, source fields, sample restrictions, transformations.
- Be explicit about scaling: per-share, per-dollar-of-assets, logged, standardized.
- Note when log transformations drop zeros and how zeros are handled.

## Date alignment and look-ahead bias
- Ensure accounting data are available at the time of portfolio formation or regression.
- Standard lag for annual Compustat: 4-6 months after fiscal year end (June of year t+1 for December FYE firms).
- For quarterly data: at least 45 days after quarter end.
- Flag any potential look-ahead issues explicitly.

## Winsorization and outliers
- Do not winsorize by default. Justify the level if used.
- Typical levels: 1%/99% or 5%/95%, cross-sectional within each period.
- Report results with and without winsorization.
- Consider trimming vs. winsorization and explain the choice.

## Missingness
- Document missingness rates for every key variable.
- Distinguish between missing (not reported), zero, and zero-but-meaningful.
- State the rule for each variable: drop, impute, flag, or leave.
- If imputation is used, justify the method and report sensitivity.

## Reproducibility
- Maintain a sample-construction log.
- Maintain a variable dictionary (codebook).
- Keep a merge audit and unmatched-observation report.
- Preserve a one-command path from raw data to final tables.
- Use version control for code. Date-stamp data extracts.
- Number scripts sequentially (01_clean.do, 02_merge.do, 03_analysis.do).
