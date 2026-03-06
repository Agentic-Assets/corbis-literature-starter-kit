---
name: finance-empirical-analysis
description: "Plan and interpret baseline empirical analyses for finance and real-estate papers. Use for table plans, regressions, robustness structure, mechanisms, and results writeup."
---

# Finance Empirical Analysis

Organize the empirical section so that each table answers a clear question and each robustness check addresses a real threat.

## Workflow

1. Define the empirical sequence before discussing estimates.
2. Build a table and figure plan using assets/table-plan-template.md.
3. Start with sample description and summary statistics.
4. Present the baseline specification with full notation.
5. Translate the baseline estimate into economic magnitude.
6. Group robustness checks by threat category.
7. Separate mechanism, heterogeneity, and external-validity evidence.
8. Draft paragraph-ready interpretations.

## Standard table sequence for empirical finance papers

| Table | Purpose | What the reader learns |
|---|---|---|
| 1 | Summary statistics | Sample composition, variable distributions, key correlations |
| 2 | Baseline result | Main effect with preferred specification |
| 3 | Robustness | Alternative measures, samples, fixed effects, clustering |
| 4 | Mechanism / channel | Why the effect operates — intermediate outcomes or channel variables |
| 5 | Heterogeneity | Where the effect is stronger or weaker, and why |
| 6+ | Extensions | Cross-sectional tests, dynamics, external validity |

This is a default — adjust to the paper's logic. Some papers need a "first stage" or "event study" table before the baseline.

## Interpretation protocol

For every main result, write the interpretation in this order:
1. **State the result**: "Firms exposed to the shock reduce investment by..."
2. **Name the specification**: "...in column 3, which includes firm and year fixed effects..."
3. **Quantify the magnitude**: "A one-standard-deviation increase in X is associated with a Y% decline in investment, relative to a sample mean of Z%."
4. **Interpret cautiously**: "This is consistent with [mechanism] but does not rule out [alternative]."
5. **State the limit**: "The design identifies the effect of [narrow thing], not [broader claim the reader might infer]."

## Table and figure formatting

All tables and figures must follow the float format in `latex_template/academic_paper_template.tex`:
1. `\caption{Descriptive Title}` at the top
2. `\label{tab:name}\vspace{-2.5ex}` immediately after
3. `\floatnotes{...}` with a self-contained descriptive note *above* the table/figure body (not below it). The note should state: what the table reports, the sample, clustering level, and "t-statistics in parentheses."
4. Table body using `booktabs` (`\toprule`/`\midrule`/`\bottomrule`), `\sym{}` for stars, t-stats in parentheses with `\\[0.5ex]` spacing
5. Significance legend as last row inside `tabular`: `\sym{*} $p<0.10$, \sym{**} $p<0.05$, \sym{***} $p<0.01$`

The `\floatnotes` command renders as a scriptsize quotation. See the template for examples.

## Statistical significance reporting

- **Tables**: Report t-statistics in parentheses below coefficients. Not standard errors, not p-values.
- **Text**: Reference the t-statistic when discussing significance: "the coefficient is -0.013 (t = -4.36)."
- **Stars**: Use *** p<0.01, ** p<0.05, * p<0.10 alongside t-statistics. Stars provide quick visual scanning; t-statistics provide the actual information.
- **Table notes**: State "t-statistics in parentheses" and the clustering level.

## Economic magnitude translations

Always convert coefficients into economically meaningful units:
- Standard-deviation changes in the dependent variable
- Dollar or percentage-point changes relative to the sample mean
- Comparison to other known effects in the literature
- Back-of-envelope welfare or policy implications when appropriate

Avoid: "a one-unit increase in X leads to a beta increase in Y" without contextualizing what a one-unit increase means economically.

## Robustness categories

Map every robustness check to a specific threat:

| Category | What it addresses | Example |
|---|---|---|
| Alternative measurement | Variable definition drives the result | Different proxy for main variable |
| Alternative comparison groups | Comparison group drives the result | Matched sample, different control firms |
| Fixed-effects sensitivity | Unobserved heterogeneity | Add/remove industry, state, firm FE |
| Sample sensitivity | Outliers or subsamples drive the result | Exclude financial firms, winsorize differently |
| Timing and dynamics | Treatment timing or lags matter | Different event windows, lead/lag structure |
| Placebo / falsification | Test for spurious patterns | Placebo treatment, pre-period outcome |
| Channel discrimination | Distinguish competing mechanisms | Interact with channel proxies, mediation |
| Inference sensitivity | Statistical inference drives significance | Alternative clustering, bootstrap, RI |

**Do not include a robustness check that does not map to a threat.** If you cannot name the threat, the check is uninformative.

## Mechanism evidence standards

Mechanism evidence in finance is difficult. Heterogeneity is not mechanism. Follow these rules:
- State the hypothesized channel before testing it.
- Explain why the heterogeneity pattern supports channel A over channel B.
- If testing an intermediate outcome, justify why it is on the causal path and not a competing outcome.
- Discuss at least one competing channel seriously.
- If the mechanism evidence is suggestive rather than definitive, say so.

## Code generation guidance

When the user needs code for the analysis, produce clean Stata (default), R, or Python:
- Include clear comments explaining each specification choice
- Use `estout`/`esttab` (Stata), `stargazer`/`modelsummary` (R), or `statsmodels` (Python) for table output
- Cluster standard errors at the level of treatment variation
- Always show the observation count and R-squared
- Log all output for reproducibility

## Deliverables

Produce:
- a table and figure plan using assets/table-plan-template.md
- a results memo with interpretation for each table
- paragraph-ready writeups for main results (following the interpretation protocol)
- a prioritized robustness roadmap linked to threats
- suggested code structure for the main specifications

## Output format

```
# Empirical section plan
## Table sequence (with purpose for each)
## Figure sequence (with message for each)
## Baseline interpretation (5-step protocol)
## Economic magnitude translation
## Robustness by threat (table mapping threats to checks)
## Mechanism strategy
## Heterogeneity strategy
## What not to include (and why)
```

## Tool integration (Corbis MCP)

Use tools to benchmark results and ground interpretations:

- `search_papers` (query: the specific empirical finding, e.g., "investment response to debt covenant violation", `matchCount: 10`, `minYear: 2015`) → find comparable magnitudes in the literature to benchmark the user's estimates.
- `top_cited_articles` (journals: target journals, topic-relevant years) → find the most-cited papers with comparable findings to benchmark economic magnitudes.
- `get_paper_details` (paper IDs) → read how comparable papers report and interpret their results.
- `fred_search` / `fred_series_batch` → pull macro variables for subsample analysis, time-series context, or conditional tests (e.g., recession vs. expansion splits).
- `internet_search` (Enterprise; fallback: `search_papers` for academic content, or ask user for URLs) (query: "[specific robustness method] applied example finance") → find examples of how published papers implement specific robustness checks.
- `export_citations` (format: `bibtex`) → export BibTeX entries for benchmark and comparison papers identified during magnitude calibration and results interpretation. Offer this after the results memo is produced.
- `format_citation` → format individual references for inline use in the results writeup.

## Reference files
Read if needed:
- references/empirical-standards.md
- references/writing-norms.md

## Guardrails

- Do not let robustness become a bag of disconnected tests.
- Do not write results paragraphs that merely narrate coefficients ("Column 1 shows...Column 2 shows...").
- Do not present heterogeneity as mechanism unless the logic is explicit and competing channels are addressed.
- If the empirical section is too long, cut low-information checks first.
- Do not report results as "significant" without the economic magnitude.
- Flag when a table has too many specifications that all say the same thing — consolidate.

## Example prompts
- "Plan the results section for this corporate-finance paper."
- "Which robustness checks matter for this mortgage-credit design?"
- "Write paragraph-ready interpretations of Tables 2 through 4."
- "Convert these regression coefficients into economically meaningful magnitudes."
- "Design the mechanism tests for a paper about lending discrimination."
