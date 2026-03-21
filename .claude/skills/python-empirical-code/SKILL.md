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
- Use `merge_with_validation()` from `utils/data_utils.py` for all merges (see Testing and validation section)
- Track sample flow with `SampleTracker` when building the analysis sample
- Run `data_quality_report()` before any analysis and save output to `notes/`

### Comments
- Comment the *why*, not the *what*
- Docstring at the top of every script: purpose, inputs, outputs

## Shared utilities

The `utils/` module at the project root provides ready-to-use helpers. Import them in any script:
- `utils.data_utils`: `connect_wrds()`, `winsorize()`, `merge_with_check()`, `merge_with_validation()`, `validate_variable()`, `SampleTracker`, `data_quality_report()`, `align_fiscal_to_calendar()`
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

## Testing and validation

Reproducibility requires not just running scripts but verifying they produce correct intermediate outputs. Every data pipeline should include validation checks that catch silent errors before they propagate to final results.

### Merge quality checks

After every merge, validate the result:

```python
def merge_with_validation(left, right, on, how='inner', name='merge',
                          expect_match_rate=None, allow_many_to_many=False):
    """Merge with automatic quality reporting."""
    n_left = len(left)
    n_right = len(right)
    
    merged = left.merge(right, on=on, how=how, indicator=True,
                        validate='many_to_one' if not allow_many_to_many else None)
    
    # Report match rates
    match_counts = merged['_merge'].value_counts()
    match_rate = (match_counts.get('both', 0)) / n_left
    
    print(f"\n--- {name} ---")
    print(f"Left: {n_left:,}  Right: {n_right:,}  Result: {len(merged):,}")
    print(f"Match rate: {match_rate:.1%}")
    print(match_counts.to_string())
    
    # Assert minimum match rate if specified
    if expect_match_rate is not None:
        assert match_rate >= expect_match_rate, (
            f"{name}: match rate {match_rate:.1%} below expected {expect_match_rate:.1%}"
        )
    
    # Check for unexpected observation count changes
    if how == 'inner':
        assert len(merged) <= n_left, (
            f"{name}: inner merge expanded rows ({n_left:,} → {len(merged):,}). "
            f"Check for duplicates in the right table on key: {on}"
        )
    
    merged = merged.drop(columns='_merge')
    return merged
```

### Variable construction checks

Validate that constructed variables have expected properties:

```python
def validate_variable(df, col, checks):
    """
    Run a battery of checks on a constructed variable.
    
    checks: dict with optional keys:
        'min', 'max': hard bounds (assert failure if violated)
        'pct_missing_max': max allowable fraction missing
        'pct_zero_max': max allowable fraction zero
        'expected_sign_corr': (other_col, expected_sign) for sanity check
        'no_negatives': bool
    """
    print(f"\n--- Validating: {col} ---")
    print(f"  N: {df[col].notna().sum():,}  Missing: {df[col].isna().sum():,} "
          f"({df[col].isna().mean():.1%})")
    print(f"  Mean: {df[col].mean():.4f}  Median: {df[col].median():.4f}")
    print(f"  Min: {df[col].min():.4f}  Max: {df[col].max():.4f}")
    
    if 'min' in checks:
        assert df[col].min() >= checks['min'], (
            f"{col}: min value {df[col].min():.4f} below hard floor {checks['min']}"
        )
    if 'max' in checks:
        assert df[col].max() <= checks['max'], (
            f"{col}: max value {df[col].max():.4f} above hard ceiling {checks['max']}"
        )
    if 'no_negatives' in checks and checks['no_negatives']:
        assert (df[col].dropna() >= 0).all(), (
            f"{col}: contains {(df[col] < 0).sum():,} negative values"
        )
    if 'pct_missing_max' in checks:
        pct_missing = df[col].isna().mean()
        assert pct_missing <= checks['pct_missing_max'], (
            f"{col}: {pct_missing:.1%} missing exceeds threshold "
            f"{checks['pct_missing_max']:.1%}"
        )
    if 'pct_zero_max' in checks:
        pct_zero = (df[col] == 0).mean()
        assert pct_zero <= checks['pct_zero_max'], (
            f"{col}: {pct_zero:.1%} zeros exceeds threshold {checks['pct_zero_max']:.1%}"
        )
    if 'expected_sign_corr' in checks:
        other_col, expected_sign = checks['expected_sign_corr']
        corr = df[[col, other_col]].corr().iloc[0, 1]
        if expected_sign == '+':
            assert corr > 0, f"{col}: expected positive correlation with {other_col}, got {corr:.3f}"
        elif expected_sign == '-':
            assert corr < 0, f"{col}: expected negative correlation with {other_col}, got {corr:.3f}"
    
    print(f"  ✓ All checks passed")


# Example usage for common finance variables:
validate_variable(df, 'market_cap', {
    'no_negatives': True,
    'pct_missing_max': 0.05,
})
validate_variable(df, 'book_to_market', {
    'min': 0,
    'pct_missing_max': 0.15,
    'expected_sign_corr': ('ret_annual', '+'),  # value premium
})
validate_variable(df, 'leverage', {
    'min': 0, 'max': 10,  # leverage above 10 is likely an error
    'pct_missing_max': 0.10,
})
```

### Sample flow tracking

Generate a sample-flow table that documents observation counts at each filter step:

```python
class SampleTracker:
    """Track observation counts through the data pipeline."""
    
    def __init__(self, name='Sample Construction'):
        self.name = name
        self.steps = []
    
    def record(self, df, step_name, entity_col=None):
        """Record the current state after a filter or merge step."""
        n_obs = len(df)
        n_entities = df[entity_col].nunique() if entity_col else None
        self.steps.append({
            'step': step_name,
            'n_obs': n_obs,
            'n_entities': n_entities,
            'dropped': self.steps[-1]['n_obs'] - n_obs if self.steps else 0,
        })
        dropped_str = f" (dropped {self.steps[-1]['dropped']:,})" if self.steps[-1]['dropped'] > 0 else ""
        entity_str = f"  Entities: {n_entities:,}" if n_entities else ""
        print(f"  [{step_name}] N={n_obs:,}{dropped_str}{entity_str}")
    
    def to_dataframe(self):
        return pd.DataFrame(self.steps)
    
    def to_latex(self, path):
        """Export as a LaTeX table for the appendix."""
        tbl = self.to_dataframe()
        # Generate LaTeX using project conventions
        ...

# Usage:
tracker = SampleTracker('CRSP-Compustat Panel')
tracker.record(df_raw, 'Raw CRSP monthly', entity_col='permno')
df = df_raw[df_raw['shrcd'].isin([10, 11])]
tracker.record(df, 'Common shares only', entity_col='permno')
df = df[df['exchcd'].isin([1, 2, 3])]
tracker.record(df, 'NYSE/AMEX/NASDAQ', entity_col='permno')
df = df.merge(df_comp, on=['permno', 'date'], how='inner')
tracker.record(df, 'After Compustat merge', entity_col='permno')
```

### Data quality report

Generate a summary report at the end of the build stage:

```python
def data_quality_report(df, key_vars, entity_col, time_col, output_path=None):
    """
    Generate a data quality report for the analysis sample.
    
    Checks: missingness, duplicates, time coverage, outliers.
    """
    report = []
    report.append(f"Data Quality Report")
    report.append(f"{'='*50}")
    report.append(f"Observations: {len(df):,}")
    report.append(f"Entities: {df[entity_col].nunique():,}")
    report.append(f"Time range: {df[time_col].min()} to {df[time_col].max()}")
    report.append(f"Periods: {df[time_col].nunique():,}")
    report.append(f"")
    
    # Missingness
    report.append("MISSINGNESS")
    for var in key_vars:
        pct = df[var].isna().mean()
        flag = " ⚠" if pct > 0.10 else ""
        report.append(f"  {var}: {pct:.1%}{flag}")
    report.append("")
    
    # Duplicates
    n_dup = df.duplicated(subset=[entity_col, time_col]).sum()
    report.append(f"DUPLICATES on ({entity_col}, {time_col}): {n_dup:,}")
    if n_dup > 0:
        report.append(f"  ⚠ Duplicates found — investigate before proceeding")
    report.append("")
    
    # Panel balance
    obs_per_entity = df.groupby(entity_col)[time_col].count()
    report.append(f"PANEL BALANCE")
    report.append(f"  Obs per entity: mean={obs_per_entity.mean():.1f}, "
                  f"median={obs_per_entity.median():.0f}, "
                  f"min={obs_per_entity.min()}, max={obs_per_entity.max()}")
    report.append("")
    
    # Outliers (values beyond 5 SDs)
    report.append("POTENTIAL OUTLIERS (beyond 5 SDs)")
    for var in key_vars:
        if df[var].dtype in ['float64', 'float32', 'int64']:
            z = (df[var] - df[var].mean()) / df[var].std()
            n_outliers = (z.abs() > 5).sum()
            if n_outliers > 0:
                report.append(f"  {var}: {n_outliers:,} observations")
    
    text = "\n".join(report)
    print(text)
    if output_path:
        with open(output_path, 'w') as f:
            f.write(text)
    return text
```

### When to validate

- **After every merge**: Use `merge_with_validation` with expected match rates
- **After variable construction**: Use `validate_variable` on all key variables
- **After sample filters**: Use `SampleTracker` to document the pipeline
- **Before running regressions**: Run `data_quality_report` on the analysis sample
- **After winsorization**: Verify the distribution changed as expected (print before/after percentiles)

### Integration with the exploration workflow

When running exploration regressions in `explore/`, validation can be lighter (print N and check signs). When promoting a script to `analysis/`, add full validation:
1. Merge checks with expected match rates
2. Variable validation with hard bounds
3. Sample tracker for the appendix table
4. Data quality report saved to `notes/`

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
