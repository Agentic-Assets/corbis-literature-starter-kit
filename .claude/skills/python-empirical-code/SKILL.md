---
name: python-empirical-code
description: "Generate publication-ready Python code for empirical finance and real-estate research. Use for data cleaning, merges, regressions, portfolio sorts, event studies, tables, figures, and reproducible project pipelines."
---

# Python Empirical Code

Write code the way a careful empirical finance researcher would: clean, reproducible, and aligned with what top journals expect.

## When to use this skill

- Code for any stage of an empirical finance or real-estate project
- Porting Stata/R results to Python
- Figures or tables formatted for journal submission
- Full project pipeline from raw data to output

## Python stack

| Task | Library |
|---|---|
| Data manipulation | `pandas`, `numpy` |
| Panel regressions (FE, IV, Fama-MacBeth) | `linearmodels` |
| Cross-sectional OLS, logit, probit | `statsmodels` (formula API) |
| Survival / hazard models | `lifelines` |
| Portfolio sorts & AP tests | Custom functions |
| Tables | Custom LaTeX generation |
| Figures | `matplotlib` + `seaborn` |
| Spatial analysis | `geopandas`, `libpysal` |
| Large datasets | `pyarrow` / `polars` |
| Database access | `wrds` |

Read `references/python-finance-packages.md` for versions, API patterns, and common pitfalls.

## Code quality rules

### Naming and structure
- snake_case for all variables and functions
- Descriptive DataFrame names: `df_crsp`, `df_comp`, `df_merged` — not `df`, `df2`, `temp`
- One script per logical task (e.g., `01_clean_crsp.py`, `02_merge_ccm.py`)
- Every script runnable independently after the build stage completes

### Data handling
- Never modify raw data in place — read from `raw/`, write to `build/`
- Explicit dtypes when reading CSVs
- Parse dates explicitly: `pd.to_datetime(df['date'], format='%Y%m%d')`
- Sort panel data by entity and time before operations

### Defensive coding
- Assert expected shapes after merges
- Check for unexpected duplicates
- Print observation counts at key stages
- Validate merge quality with `indicator=True`

### Comments
- Comment the *why*, not the *what*
- Docstring at the top of every script: purpose, inputs, outputs

## Shared utilities

The `utils/` module at the project root provides ready-to-use helpers. Import them in any script:
- `utils.data_utils`: `connect_wrds()`, `winsorize()`, `merge_with_check()`, `align_fiscal_to_calendar()`
- `utils.table_utils`: `reg_to_latex()`, `summary_stats_latex()`
- `utils.figure_utils`: `set_publication_defaults()`, `plot_event_study()`, `plot_binned_scatter()`, `coef_plot()`, `COLORS`
- `utils.regression_utils`: `explore_reg()`, `portfolio_sort()`, `alpha_table()`

## Code examples

For complete, ready-to-use code templates, read `assets/code-examples.md`. It covers:
- WRDS data access (CRSP, Compustat, CCM merge)
- Date alignment for look-ahead bias avoidance
- Winsorization and industry classification
- Panel regressions (OLS, IV, DiD, event study, Fama-MacBeth)
- Staggered DiD (Callaway-Sant'Anna)
- Portfolio sorts and alpha tables
- Quick exploration functions
- LaTeX regression and summary statistics tables
- Publication figure defaults and common plot functions
- Spatial operations (geocoding, Conley SEs, repeat-sales)
- Project scaffold and master pipeline script

## LaTeX table/figure format

Follow the float format specified in CLAUDE.md. Before first use, read `latex_template/academic_paper_template.tex` for the template's custom commands (`\floatnotes`, `\sym`). Use `utils.table_utils.reg_to_latex()` and `utils.table_utils.summary_stats_latex()` to generate compliant tables programmatically.

## Exploration workflow

- Exploration scripts go in `explore/`, not `analysis/`.
- Print coefficient, t-stat, N, and R-squared to console. That is enough to decide keep/toss.
- When a test works, move script to `analysis/` and log in `notes/lab_notebook.md`.

## Tool integration (Corbis MCP)

- `search_papers` → find design precedents for implementation guidance
- `fred_series_batch` → pull FRED data for macro controls
- `search_datasets` → discover data sources
- `export_citations` (format: `bibtex`) → export BibTeX for methodological papers cited in the code

## Guardrails

- Do not generate code that modifies raw data files.
- Do not use deprecated pandas syntax (`append`, `inplace=True` in chains).
- Always include observation counts after merges and filters.
- Always cluster SEs at the level of treatment variation.
- Do not hardcode file paths — use `Path` objects relative to project root.
- Pin package versions in `requirements.txt`.
- When translating Stata code, preserve the exact specification.
- For asset-pricing code, use NYSE breakpoints and value-weighted returns as default.
- For real-estate code, project coordinates before computing distances.

Read these references as needed:
- `references/empirical-standards.md`
- `references/python-finance-packages.md`
