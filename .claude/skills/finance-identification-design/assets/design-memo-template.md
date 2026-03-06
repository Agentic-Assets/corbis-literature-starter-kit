# Design Memo

## Estimand
[State in plain English: "The causal effect of X on Y for population Z."]
[State in notation: beta = E[Y(1) - Y(0) | ...]]

## Unit of observation
[Firm-year, loan-month, property-transaction, borrower-quarter, etc.]

## Treatment and timing
[What is the treatment? When does it occur? Is timing clean or staggered?]

## Outcome variables
[Primary outcome, secondary outcomes. Source and construction for each.]

## Comparison group
[Who are the controls? Why are they comparable? Economic justification.]

## Baseline specification
[Full equation with notation. Example:]
[Y_it = alpha + beta * Treatment_it + X_it * gamma + mu_i + delta_t + epsilon_it]
[Explain what each term represents.]

## Identification assumption
[State the assumption in economic terms: "Conditional on [controls/FE], the treatment is uncorrelated with unobserved determinants of Y because..."]

## Threats and diagnostics

| Threat | Severity | Diagnostic | Expected result |
|---|---|---|---|
| [e.g., Reverse causality] | [High/Med/Low] | [e.g., Leads test] | [e.g., No pre-treatment effect] |
| | | | |
| | | | |

## Mechanism tests
[What intermediate outcome or interaction will distinguish channel A from channel B?]

## Heterogeneity tests
[Which cross-sectional splits are informative about the mechanism? Why?]

## Falsification tests
[Placebo treatments, placebo outcomes, placebo samples]

## Inference plan
[Clustering level and justification. Bootstrap or RI if applicable. Conley SE if spatial.]

## Data requirements
[What datasets, sample period, and observation counts are needed?]

## Modern methods check
- [ ] If staggered DiD: modern estimator considered?
- [ ] If IV: effective F-statistic and LATE interpretation?
- [ ] If RD: optimal bandwidth and manipulation test?
- [ ] Oster (2019) bounds for selection on unobservables?
- [ ] Appropriate pretrend analysis (Roth 2022 sensitivity)?

## Journal-fit notes
[How does the design map to expectations at the target journal?]
