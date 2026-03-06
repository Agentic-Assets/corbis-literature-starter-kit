# Empirical Standards for Identification Design

## Before estimation
- Define the unit of observation, sampling frame, and time aggregation.
- Write down the estimand in plain English and in notation.
- Define treatment, outcome, timing, and comparison set.
- Document all screens, exclusions, and winsorization or trimming rules.
- Check that identifiers and time stamps support the intended design.

## Baseline design
- State the baseline specification in notation and plain English.
- Explain fixed effects, clustering, and variation used for identification.
- Tie each control to a threat or precision goal — no "kitchen sink" controls.
- Explain whether standard errors are clustered at the level of treatment variation.
- If using TWFE with staggered treatment, justify or use modern DiD estimators.

## Modern methods checklist
- **Staggered DiD**: Consider Callaway-Sant'Anna, Sun-Abraham, Borusyak-Jaravel-Spiess, or de Chaisemartin-D'Haultfoeuille estimators. TWFE is biased under heterogeneous treatment effects.
- **Pretrends**: Roth (2022) shows conventional pre-trend tests are low-powered. Consider sensitivity analysis.
- **IV**: Report effective F-statistic (Olea-Pflueger), not just first-stage F. Discuss LATE interpretation.
- **RD**: Calonico-Cattaneo-Titiunik bandwidth, McCrary density test, and plot raw data.
- **Shift-share**: Apply GPSS (2020) or BHJ (2022) framework. Clarify shares vs. shocks identification.
- **Sensitivity**: Oster (2019) bounds for selection on unobservables.
- **Clustering**: Abadie-Athey-Imbens-Wooldridge (2023) guidance on when to cluster.

## Interpretation
- Report both statistical precision and economic magnitude.
- Clarify scaling and units.
- Translate coefficients into economically meaningful changes.
- Distinguish between association, causal, and mechanism evidence explicitly.

## Robustness logic
- Only run checks that address a real, named threat.
- Group robustness checks by threat category.
- Separate identification checks, measurement checks, and sample-sensitivity checks.

## Mechanism evidence
- State the hypothesized channel before testing it.
- Distinguish mechanism tests from heterogeneity patterns.
- Discuss competing channels rather than pretending they do not exist.
- Heterogeneity is suggestive, not proof, of mechanism.

## Reproducibility
- Maintain a sample-construction log.
- Maintain a variable dictionary.
- Keep a merge audit and unmatched-observation report.
- Preserve a one-command path from raw to final tables whenever feasible.
