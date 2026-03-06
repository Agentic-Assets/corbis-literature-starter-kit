# Empirical Standards for Analysis

## Before estimation
- Define the unit of observation, sampling frame, and time aggregation.
- Write down the estimand in words and notation.
- Define treatment, outcome, timing, and comparison set.
- Document all screens, exclusions, and winsorization or trimming rules.
- Verify that the sample construction is complete and documented before running regressions.

## Baseline design
- State the baseline specification in notation and plain English.
- Explain fixed effects, clustering, and variation used for identification.
- Tie each control to a threat or precision goal — no kitchen-sink controls.
- Standard errors clustered at the level of treatment variation.
- Build specifications from simple to complex: show that the result is not an artifact of a particular specification.

## Interpretation protocol
For every main result:
1. State the result (what happened)
2. Name the specification (what controls, FE, sample)
3. Quantify the magnitude (SD change, dollar amount, percentage relative to mean)
4. Interpret cautiously (what the result is consistent with)
5. State the limit (what the design cannot claim)

## Economic magnitude
- Always translate coefficients into economically meaningful units.
- Standard-deviation changes, dollar changes, or percentage changes relative to the sample mean.
- Compare to other known effects in the literature when possible.
- "Statistically significant" is not an economic result. "A one-SD increase in X reduces Y by Z%, equivalent to [real-world benchmark]" is.

## Robustness logic
- Only run checks that address a real, named threat.
- Group robustness checks by threat category (measurement, comparison group, FE, sample, timing, placebo, channel, inference).
- A robustness check without a named threat is uninformative.
- If all robustness checks pass, that strengthens the design. If some fail, explain why and what it means.

## Mechanism evidence
- State the hypothesized channel before testing it.
- Distinguish mechanism tests from heterogeneity patterns. Heterogeneity is suggestive, not proof.
- If testing an intermediate outcome, justify why it is on the causal path.
- Discuss at least one competing channel seriously.
- If mechanism evidence is suggestive rather than definitive, say so.

## Table construction
- Each table should have a single purpose.
- Summary statistics: means, SDs, medians, p25/p75, N. Treatment-control comparison if relevant.
- Baseline: build up specifications. Show the preferred specification clearly.
- Robustness: organize by threat, not by arbitrary specification number.
- Mechanism/heterogeneity: explain why each split is informative.

## Reproducibility
- Log all output.
- Number scripts and tables consistently.
- Every table should be reproducible from a single script run.
