---
name: finance-empirical-analysis
description: "Plan and interpret baseline empirical analyses for finance and real-estate papers. Use for table plans, regressions, robustness structure, mechanisms, and results writeup."
---

# Finance Empirical Analysis

Organize the empirical section so that each table answers a clear question and each robustness check addresses a real threat.

## Workflow

### Exploration phase (discovering the results)

Before the table sequence is finalized, the user will typically run many tests to see what works. Support this phase with:

1. **Initialize a lab notebook.** Copy `assets/lab-notebook-template.md` to `notes/lab_notebook.md`. This is the running log of what was tested, what worked, what didn't, and the emerging economic narrative.
2. **Help design exploration batches.** Suggest sets of tests to run together: alternative dependent variables, candidate explanatory variables, subsample splits, mechanism proxies. Use `utils.regression_utils.explore_reg()` for fast iteration.
3. **Log results.** After each batch, update the lab notebook with the question, what was run, the result, and the verdict (keep/toss/modify).
4. **Update the emerging narrative.** As results accumulate, periodically revise the "Emerging narrative" section of the lab notebook to reflect the current economic story.
5. **Identify the table candidates.** When exploration is mostly done, populate the "Table and figure candidates" section of the lab notebook.

### Paper-ready phase (organizing for the paper)

Once the table candidates are identified:

1. Define the empirical sequence before discussing estimates.
2. Build a table and figure plan using assets/table-plan-template.md.
3. Start with sample description and summary statistics.
4. Present the baseline specification with full notation.
5. Translate the baseline estimate into economic magnitude.
6. Group robustness checks by threat category.
7. Separate mechanism, heterogeneity, and external-validity evidence.
8. Draft paragraph-ready interpretations.

The transition from exploration to paper-ready happens when the lab notebook's "Ready to write?" checklist is complete.

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

When referencing model predictions or theoretical variables in results discussion, describe the economic concept first and place the notation in parentheses. BAD: "The coefficient on β₂ is positive." GOOD: "The coefficient on AI adoption intensity (β₂) is positive, indicating that..."

## Table and figure formatting — write to `.tex` files

Follow the float format specified in CLAUDE.md. Before first use, read `latex_template/academic_paper_template.tex` for the template's custom commands (`\floatnotes`, `\sym`) and working examples.

Write all table and figure LaTeX to `output/tables/*.tex` and `output/figures/*.tex`. Do not put LaTeX in the chat. Each float gets its own file (e.g., `output/tables/tab_summary.tex`), included in the paper via `\input{}`. Use `utils.table_utils.reg_to_latex()` for programmatic table generation.

Table notes must be self-contained: state what the table reports, the sample, clustering level, and "t-statistics in parentheses."

## Statistical significance reporting

- **Tables**: Report t-statistics in parentheses below coefficients. Not standard errors, not p-values.
- **Text**: Reference the t-statistic when discussing significance: "the coefficient is -0.013 (t = -4.36)."
- **Stars**: Use *** p<0.01, ** p<0.05, * p<0.10 alongside t-statistics. Stars provide quick visual scanning; t-statistics provide the actual information.
- **Table notes**: State "t-statistics in parentheses" and the clustering level.

## Economic magnitude translations

Always convert coefficients into economically meaningful units using a three-tier approach:

1. **Statistical units** (minimum): SD change in the dependent variable, percentage-point change relative to sample mean.
2. **Real-world units** (standard): dollar amounts, basis points, square feet, months of rent, jobs gained or lost.
3. **Anchored comparison** (best): compare to a familiar quantity the reader already grasps (a known effect from prior literature, a typical firm decision, a common policy change, or a household-scale equivalent).

- BAD: "A one-unit increase in X leads to a beta increase in Y."
- BETTER: "A one-SD increase in X is associated with a 2.3 percentage-point decline in Y, relative to a sample mean of 8.1%."
- BEST: "A one-SD increase in X reduces Y by roughly $4.7 million per firm per year, comparable to the average annual R&D budget cut documented by Brown, Fazzari, and Petersen (2009) during credit contractions."

The goal is for a reader who has never seen the data to immediately understand whether the effect is large or small. If the magnitude sentence requires the reader to look up the sample mean or the SD to interpret it, add another layer.

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

When the user needs code for the analysis, produce clean Python (default), R, or Stata:
- Include clear comments explaining each specification choice
- Use `statsmodels` (Python), `stargazer`/`modelsummary` (R), or `estout`/`esttab` (Stata) for table output
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
