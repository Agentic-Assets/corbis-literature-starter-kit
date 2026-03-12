---
name: finance-identification-design
description: "Design and stress-test identification strategies for finance and real-estate papers. Use for DiD, event studies, IV, RD, treatment timing, clustering, and threat mapping."
---

# Finance Identification Design

Design the empirical strategy like a skeptical referee would.

## Core mandate

Move from a broad hypothesis to a defensible estimand, comparison set, specification, and threat map. Every design choice should be justified by the economic question, not by convention.

## Workflow

1. Define the estimand in plain English first, then in notation. Lead with the economic meaning; the formal expression follows in parentheses or a displayed equation after the intuition is established.
2. Define the unit of observation and treatment timing.
3. State the source of variation and why it is plausibly exogenous.
4. Write the baseline specification in words first, then in notation. The reader should understand what the regression does from the prose before seeing the equation.
5. List the key threats (use the threat taxonomy below).
6. Match each threat to a diagnostic, design tweak, falsification, or stated limitation.
7. Separate main-effect tests, mechanism tests, and heterogeneity tests.
8. Design the pretrends / balance / falsification battery.
9. Specify the inference approach: clustering, bootstrap, randomization inference, or other.

## Design-method guidance

### Difference-in-differences
- Is treatment timing clean or staggered? If staggered, consider Callaway and Sant'Anna (2021), Sun and Abraham (2021), Borusyak, Jaravel, and Spiess (2024), or de Chaisemartin and D'Haultfoeuille (2020) estimators.
- Are pretrends informative? Apply Roth (2022) sensitivity analysis for pre-trend power.
- Is the parallel trends assumption economically motivated, not just statistically convenient?
- For two-way fixed effects with staggered adoption, TWFE can be biased under heterogeneous treatment effects — flag this explicitly.

### Event studies
- Define the event window, estimation window, and any gap between them.
- Address anticipation effects with theory, not just by adding leads.
- Choose between abnormal-return approaches (short window) and panel event-study designs (long window).
- For financial events, consider confounding announcements in the same window.

### Instrumental variables
- State the exclusion restriction in economic terms, not just statistical terms.
- Discuss the first-stage F-statistic threshold (Stock-Yogo weak instrument tests, or effective F from Olea and Pflueger 2013).
- Discuss LATE interpretation: who are the compliers and does the local effect matter economically?
- Consider the monotonicity assumption explicitly.

### Regression discontinuity
- Justify bandwidth choice (Calonico, Cattaneo, Titiunik optimal bandwidth).
- Show density tests (McCrary/Cattaneo-Jansson-Ma) for manipulation.
- Plot the raw data around the cutoff.
- Discuss whether the running variable is truly continuous or discrete.

### Matching and propensity score methods
- These are generally insufficient for top finance journals as standalone identification — pair with a design-based argument.
- If used, discuss overlap, balance, and sensitivity to unobservables (Oster 2019 bounds).

### Shift-share / Bartik instruments
- Apply Goldsmith-Pinkham, Sorkin, and Swift (2020) or Borusyak, Hull, and Jaravel (2022) framework.
- Clarify whether identification comes from the shares or the shocks.
- Test for pre-trends in the shares.

## Threat taxonomy

Map every identified threat to a specific diagnostic:

| Threat | Diagnostic or remedy |
|---|---|
| Reverse causality | Timing structure, leads test, Granger-style falsification |
| Omitted confounders | Additional controls, Oster (2019) bounds, placebo treatments |
| Endogenous timing | Examine whether treatment timing predicts pre-treatment outcomes |
| Sample selection | Heckman correction, bounds, or explicit discussion of selected sample |
| Bad controls | Angrist and Pischke test: does adding the control change the coefficient for a reason? |
| Treatment spillovers | Spatial buffers, exclude neighbors, test for spillover gradient |
| Anticipation effects | Leads in event study, theory-based anticipation window |
| Dynamic / heterogeneous treatment effects | Modern DiD estimators, event-study plots by cohort |
| Measurement error | Alternative measures, IV for mismeasured variable, attenuation bounds |
| Equilibrium responses | Discuss general vs. partial equilibrium, bound the scope of the claim |
| Multiple testing | Bonferroni, Holm, or Romano-Wolf corrections; pre-registration |

## Finance-specific checks

- Is the clustering level aligned with the level of treatment variation? (Abadie, Athey, Imbens, Wooldridge 2023 guidance on when to cluster.)
- Are fixed effects doing identification work or only cleaning up noise? Can you explain what variation remains after fixed effects absorb?
- If the design is staggered, has the user thought through heterogeneous treatment effects?
- If the design is event-time based, are pretrends and anticipation explicit?
- If the setting is contracts, deals, loans, funds, or firms, is the comparison group economically sensible?
- For corporate finance: is the endogeneity of corporate decisions addressed?
- For household finance: are selection into financial products and financial literacy concerns addressed?

## Real-estate-specific checks

These are quick checks. For deeper RE design guidance (hedonic, repeat-sales, boundary RD, spatial DiD, CRE, mortgage, climate), use the `real-estate-empirical-design` skill.

- Does the design account for spatial autocorrelation in the error structure?
- Is the geographic unit of analysis appropriate (property, block, tract, ZIP, MSA)?
- Are boundary designs vulnerable to sorting across boundaries?
- For hedonic designs, is the functional form justified?
- For repeat-sales, are property improvements between sales addressed?

## Deliverables

Produce:
- a design memo using assets/design-memo-template.md
- a threats-and-remedies table (use the format above)
- a baseline regression blueprint with full notation
- a prioritized robustness list, ranked by how much a referee would care
- suggested Stata/R/Python code structure for the main specification

## Output format

```
# Identification memo
## Estimand (plain English and notation)
## Variation used
## Baseline specification (notation and code sketch)
## Why this could identify the effect
## Main threats (ranked, with diagnostics)
## Modern methods considerations
## Diagnostics and falsifications
## Mechanism tests
## Heterogeneity tests
## What the design cannot claim
## Inference: clustering and standard errors
```

## Tool integration (Corbis MCP)

Use tools to ground design decisions in published precedent:

- `search_papers` (query: the specific method + setting, e.g., "staggered DiD bank regulation", `matchCount: 10`, `minYear: 2018`) → find recent papers using the same or similar design. Learn from their specification choices, threats addressed, and referee responses.
- `top_cited_articles` (journals: target field journals, `minYear` as appropriate) → find canonical methodological papers to ensure the design references current best practices.
- `get_paper_details` (paper IDs) → read abstracts and methods of papers with comparable designs.
- `search_papers` (query: the econometric method itself, e.g., "Callaway Sant'Anna staggered treatment", `minYear: 2020`) → find applied examples of modern estimators.
- `export_citations` (format: `bibtex`) → export BibTeX entries for methodological references cited in the design memo (e.g., Callaway-Sant'Anna, Roth, Sun-Abraham). Offer this after the design memo is produced.
- `format_citation` → format individual methodological citations for inline use in the memo.

## Reference files
Read if needed:
- references/empirical-standards.md
- references/journal-targets.md

## Guardrails

- Do not recommend robustness checks that do not map to a specific threat.
- Do not label a paper causal if the assumptions are weakly articulated.
- If the design is not yet publication grade, say exactly what is missing.
- Do not default to TWFE when the setting calls for a modern DiD estimator.
- Do not treat statistical significance of pretrend coefficients as proof of parallel trends — it is low-powered.
- Flag when the user's design choice is outdated relative to current best practice.

## Example prompts
- "Stress-test my DiD design for a debt covenant shock paper."
- "Turn this broad natural-experiment idea into a proper identification memo."
- "How should I cluster and what falsifications do I need in this housing-policy design?"
- "Is TWFE appropriate for my staggered adoption design?"
- "Design the identification strategy for a boundary discontinuity around school districts."
