---
name: python-empirical-code
description: "Generate publication-ready Python code for empirical finance and real-estate research. Use for data cleaning, merges, regressions, portfolio sorts, event studies, tables, figures, and reproducible project pipelines."
---

# Python Empirical Code

Write code the way a careful empirical finance researcher would — clean, reproducible, and aligned with what top journals expect in tables, figures, and replication packages.

## Core mandate

Generate Python code that:
- Runs correctly on the first attempt whenever possible
- Follows finance-specific conventions (variable naming, date alignment, identifier handling)
- Produces publication-ready output (tables and figures that can go directly into a LaTeX paper)
- Is reproducible (seeds, logging, clear data flow, no hidden state)
- Is readable by a coauthor who knows Stata or R but is learning Python

## When to use this skill

- The user needs code for any stage of an empirical finance or real-estate project
- The user has results in Stata/R and wants to port them to Python
- The user needs a figure or table formatted for journal submission
- The user needs a full project pipeline from raw data to output

## Python stack

Default to these libraries unless the user specifies otherwise:

| Task | Library | Notes |
|---|---|---|
| Data manipulation | `pandas`, `numpy` | Always import both |
| Regressions (OLS, FE, IV, panel) | `linearmodels` | Preferred for panel data — supports entity/time FE, clustered SEs, IV, Fama-MacBeth |
| Cross-sectional OLS, logit, probit | `statsmodels` | `smf.ols`, `smf.logit` with formula API |
| Robust/clustered SEs (non-panel) | `statsmodels` | `.get_robustcov_results(cov_type='cluster', groups=...)` |
| Survival / hazard models | `lifelines` | Cox PH, Kaplan-Meier, competing risks |
| Portfolio sorts & AP tests | Custom functions (provide) | No standard library — write clean sort/alpha code |
| Tables | `stargazer` (Python port) or custom LaTeX | See table-generation section below |
| Figures | `matplotlib` + `seaborn` | Journal-quality defaults |
| Spatial analysis | `geopandas`, `libpysal` | For real-estate spatial designs |
| Large datasets | `pyarrow` / `polars` | When pandas is too slow (TRACE, TAQ, large property datasets) |
| Database access | `wrds` (WRDS Python library) | Direct WRDS PostgreSQL queries |

### Import block template

Always start scripts with a consistent import block:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

# Project paths
ROOT = Path(__file__).resolve().parent.parent  # adjust to project root
RAW = ROOT / 'raw'
BUILD = ROOT / 'build'
OUTPUT = ROOT / 'output'
for d in [RAW, BUILD, OUTPUT]:
    d.mkdir(exist_ok=True)

# Reproducibility
np.random.seed(42)
pd.set_option('display.max_columns', 50)
pd.set_option('display.float_format', '{:.4f}'.format)
```

## Code quality rules

### Naming and structure
- Use snake_case for all variables and functions
- Name DataFrames descriptively: `df_crsp`, `df_comp`, `df_merged` — not `df`, `df2`, `temp`
- Name columns to match the paper's variable names when possible
- One script per logical task (e.g., `01_clean_crsp.py`, `02_merge_ccm.py`, `03_baseline_reg.py`)
- Every script should be runnable independently after the build stage completes

### Comments and documentation
- Comment the *why*, not the *what* — `# Lag accounting data 6 months to avoid look-ahead bias` not `# merge dataframes`
- Add a docstring at the top of every script explaining its purpose, inputs, and outputs
- For complex operations, add a brief inline explanation

### Data handling
- Never modify raw data in place — always read from `raw/`, write cleaned data to `build/`
- Use explicit dtypes when reading CSVs: `pd.read_csv(..., dtype={'permno': int, 'gvkey': str})`
- Parse dates explicitly: `pd.to_datetime(df['date'], format='%Y%m%d')`
- Always sort panel data by entity and time before operations: `df.sort_values(['permno', 'date'])`

### Defensive coding
- Assert expected shapes after merges: `assert len(df_merged) > 0, "Merge produced empty DataFrame"`
- Check for unexpected duplicates: `assert not df.duplicated(subset=['permno', 'date']).any()`
- Print observation counts at key stages: `print(f"After merge: {len(df):,} obs, {df['permno'].nunique():,} firms")`
- Validate merge quality: use `indicator=True` and tabulate `_merge` values

## Finance-specific data operations

### WRDS data access

```python
import wrds

from dotenv import load_dotenv
load_dotenv()
db = wrds.Connection(wrds_username=os.getenv('WRDS_USERNAME'))

# CRSP monthly
df_crsp = db.raw_sql("""
    SELECT a.permno, a.date, a.ret, a.retx, a.shrout, a.prc, a.vol,
           b.shrcd, b.exchcd
    FROM crsp.msf AS a
    LEFT JOIN crsp.msenames AS b
        ON a.permno = b.permno
        AND a.date BETWEEN b.namedt AND b.nameendt
    WHERE a.date BETWEEN '2000-01-01' AND '2023-12-31'
        AND b.shrcd IN (10, 11)
        AND b.exchcd IN (1, 2, 3)
""")

# Compustat annual
df_comp = db.raw_sql("""
    SELECT gvkey, datadate, fyear, at, lt, ceq, sale, ni, csho, prcc_f,
           sich, seq, txditc, pstkrv, pstkl, pstk
    FROM comp.funda
    WHERE datadate BETWEEN '2000-01-01' AND '2023-12-31'
        AND indfmt = 'INDL' AND datafmt = 'STD'
        AND popsrc = 'D' AND consol = 'C'
""")
```

### CCM merge (CRSP-Compustat)

```python
# Get CCM link table
df_ccm = db.raw_sql("""
    SELECT gvkey, lpermno AS permno, linktype, linkprim, linkdt, linkenddt
    FROM crsp.ccmxpf_lnkhist
    WHERE linktype IN ('LU', 'LC')
        AND linkprim IN ('P', 'C')
""")

# Merge Compustat to CRSP via CCM
df_comp['datadate'] = pd.to_datetime(df_comp['datadate'])
df_ccm['linkdt'] = pd.to_datetime(df_ccm['linkdt'])
df_ccm['linkenddt'] = pd.to_datetime(df_ccm['linkenddt']).fillna(pd.Timestamp('2099-12-31'))

df_comp_crsp = df_comp.merge(df_ccm, on='gvkey', how='inner')
df_comp_crsp = df_comp_crsp[
    (df_comp_crsp['datadate'] >= df_comp_crsp['linkdt']) &
    (df_comp_crsp['datadate'] <= df_comp_crsp['linkenddt'])
]
# Keep primary link when multiple matches
df_comp_crsp = df_comp_crsp.sort_values(['gvkey', 'datadate', 'linkprim'])
df_comp_crsp = df_comp_crsp.drop_duplicates(subset=['gvkey', 'datadate'], keep='first')

print(f"CCM merge: {len(df_comp_crsp):,} firm-years, {df_comp_crsp['permno'].nunique():,} firms")
```

### Date alignment (avoid look-ahead bias)

```python
# Standard Fama-French timing: fiscal year ending in calendar year t
# is available for portfolios formed in June of year t+1
df_comp_crsp['jdate'] = df_comp_crsp['datadate'] + pd.DateOffset(months=6)
df_comp_crsp['jdate'] = df_comp_crsp['jdate'] + pd.offsets.MonthEnd(0)

# Merge to monthly CRSP returns
df_crsp['jdate'] = pd.to_datetime(df_crsp['date']) + pd.offsets.MonthEnd(0)
df = df_crsp.merge(df_comp_crsp, on=['permno', 'jdate'], how='left')
```

### Winsorization

```python
def winsorize(df, var, limits=(0.01, 0.99), by=None):
    """Winsorize variable at specified percentiles, optionally by group."""
    if by is None:
        lo, hi = df[var].quantile([limits[0], limits[1]])
        df[var] = df[var].clip(lower=lo, upper=hi)
    else:
        df[var] = df.groupby(by)[var].transform(
            lambda x: x.clip(lower=x.quantile(limits[0]), upper=x.quantile(limits[1]))
        )
    return df

# Cross-sectional winsorization at 1%/99% by year
for var in ['bm', 'roa', 'leverage']:
    df = winsorize(df, var, limits=(0.01, 0.99), by='year')
```

### Industry classification

```python
# Fama-French 12 industry classification from SIC
def sic_to_ff12(sic):
    """Map SIC code to Fama-French 12 industry."""
    if pd.isna(sic): return np.nan
    sic = int(sic)
    if 100 <= sic <= 999 or 2000 <= sic <= 2399 or 2700 <= sic <= 2749 or 2770 <= sic <= 2799 or 3100 <= sic <= 3199 or 3940 <= sic <= 3989:
        return 'NoDur'
    elif 2500 <= sic <= 2519 or 2590 <= sic <= 2599 or 3630 <= sic <= 3659 or 3710 <= sic <= 3711 or 3714 <= sic <= 3714 or 3716 <= sic <= 3716 or 3750 <= sic <= 3751 or 3792 <= sic <= 3792 or 3900 <= sic <= 3939 or 3990 <= sic <= 3999:
        return 'Durbl'
    # ... (complete mapping available in assets/ff12_industries.py)
    else:
        return 'Other'

# Or use Ken French's data library directly
ff12 = pd.read_csv('https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Siccodes12.zip')
```

## Regression code

### Panel regressions with linearmodels

```python
from linearmodels.panel import PanelOLS, BetweenOLS, FirstDifferenceOLS
from linearmodels.iv import IV2SLS

# Set multi-index for panel
df = df.set_index(['permno', 'date'])

# OLS with entity and time fixed effects, clustered SEs
model = PanelOLS.from_formula(
    'y ~ 1 + x1 + x2 + x3 + EntityEffects + TimeEffects',
    data=df,
    drop_absorbed=True
)
result = model.fit(cov_type='clustered', cluster_entity=True)
print(result.summary)

# Two-way clustering (entity and time)
result_2way = model.fit(cov_type='clustered', cluster_entity=True, cluster_time=True)

# IV regression
iv_model = IV2SLS.from_formula(
    'y ~ 1 + x2 + x3 + EntityEffects + TimeEffects ~ [x1 ~ z1 + z2]',
    data=df
)
iv_result = iv_model.fit(cov_type='clustered', cluster_entity=True)
```

### Fama-MacBeth regressions

```python
from linearmodels.asset_pricing import FamaMacBeth

# Fama-MacBeth with Newey-West adjustment
fm_model = FamaMacBeth.from_formula(
    'ret_excess ~ 1 + beta + size + bm + mom',
    data=df
)
fm_result = fm_model.fit(cov_type='kernel', bandwidth=6)
print(fm_result.summary)
```

### Difference-in-differences

```python
# Standard 2x2 DiD
model_did = PanelOLS.from_formula(
    'y ~ 1 + treated:post + controls + EntityEffects + TimeEffects',
    data=df,
    drop_absorbed=True
)
did_result = model_did.fit(cov_type='clustered', cluster_entity=True)

# Event study with leads and lags
# Create event-time dummies
for k in range(-4, 8):
    if k == -1:  # omit t-1 as reference
        continue
    col = f'event_t{k:+d}'
    df[col] = (df['event_time'] == k).astype(int)

event_vars = ' + '.join([f'event_t{k:+d}' for k in range(-4, 8) if k != -1])
model_es = PanelOLS.from_formula(
    f'y ~ 1 + {event_vars} + controls + EntityEffects + TimeEffects',
    data=df,
    drop_absorbed=True
)
es_result = model_es.fit(cov_type='clustered', cluster_entity=True)
```

### Staggered DiD (modern estimators)

```python
# Callaway and Sant'Anna (2021) via the csdid package
# pip install csdid
from csdid import ATTgt

# g: first treatment period for each unit; t: time period
att = ATTgt(
    data=df.reset_index(),
    yname='y',
    gname='first_treat_year',
    tname='year',
    idname='firm_id',
    control_group='notyettreated'
)
results = att.fit()
results.summary()

# Aggregate to event study
agg_es = results.aggregate('event')
agg_es.summary()
agg_es.plot()
```

## Portfolio sorts (asset pricing)

```python
def portfolio_sort(df, signal, n_portfolios=5, nyse_breakpoints=True, weight='vw'):
    """
    Single-sort portfolios with NYSE breakpoints and value-weighting.

    Parameters
    ----------
    df : DataFrame with columns [permno, date, ret_excess, mktcap, signal, exchcd]
    signal : str, column name of the sorting variable
    n_portfolios : int
    nyse_breakpoints : bool, use NYSE stocks only for breakpoints
    weight : 'vw' or 'ew'

    Returns
    -------
    DataFrame of portfolio returns by date
    """
    df = df.dropna(subset=[signal, 'ret_excess', 'mktcap']).copy()

    def assign_portfolio(group):
        if nyse_breakpoints:
            nyse = group[group['exchcd'] == 1][signal]
            breakpoints = nyse.quantile(np.linspace(0, 1, n_portfolios + 1)[1:-1])
        else:
            breakpoints = group[signal].quantile(np.linspace(0, 1, n_portfolios + 1)[1:-1])
        group['portfolio'] = np.searchsorted(breakpoints, group[signal]) + 1
        return group

    df = df.groupby('date', group_keys=False).apply(assign_portfolio)

    if weight == 'vw':
        port_ret = df.groupby(['date', 'portfolio']).apply(
            lambda x: np.average(x['ret_excess'], weights=x['mktcap'])
        ).reset_index(name='ret')
    else:
        port_ret = df.groupby(['date', 'portfolio'])['ret_excess'].mean().reset_index(name='ret')

    port_ret = port_ret.pivot(index='date', columns='portfolio', values='ret')
    port_ret.columns = [f'Q{i}' for i in port_ret.columns]
    port_ret['HML'] = port_ret[f'Q{n_portfolios}'] - port_ret['Q1']

    return port_ret


def alpha_table(port_returns, factor_df, models=['CAPM', 'FF3', 'FF5']):
    """
    Compute alphas for each portfolio against multiple factor models.
    Returns a summary DataFrame.
    """
    import statsmodels.api as sm

    factor_cols = {
        'CAPM': ['mktrf'],
        'FF3': ['mktrf', 'smb', 'hml'],
        'FF5': ['mktrf', 'smb', 'hml', 'rmw', 'cma'],
        'FF6': ['mktrf', 'smb', 'hml', 'rmw', 'cma', 'umd'],
    }

    merged = port_returns.merge(factor_df, left_index=True, right_index=True)
    results = []

    for col in port_returns.columns:
        for model_name in models:
            y = merged[col]
            X = sm.add_constant(merged[factor_cols[model_name]])
            reg = sm.OLS(y, X).fit(cov_type='HAC', cov_kwds={'maxlags': 6})
            results.append({
                'portfolio': col,
                'model': model_name,
                'alpha': reg.params['const'] * 100,  # in percent
                't_stat': reg.tvalues['const'],
            })

    return pd.DataFrame(results)
```

## Publication-ready tables

### LaTeX table/figure format (match the LaTeX template)

All generated tables and figures must follow the formatting in `latex_template/academic_paper_template.tex`:

1. **Caption first**: `\caption{Descriptive Title}` at the top of the float
2. **Label + tighten**: `\label{tab:name}\vspace{-2.5ex}` immediately after caption
3. **Descriptive note above the body**: `\floatnotes{This table reports... Sample is... t-statistics in parentheses.}` placed *between* the caption and the table/figure body, not below it
4. **Table body**: `booktabs` rules (`\toprule`, `\midrule`, `\bottomrule`), `\sym{}` macro for significance stars, t-statistics in parentheses with `\\[0.5ex]` spacing
5. **Significance legend at bottom**: `\multicolumn{N}{l}{\footnotesize \sym{*} $p<0.10$, ...}` as the last row inside `tabular`
6. **Figures**: same caption + label + `\floatnotes` structure, then `\centering` + `\includegraphics` or the matplotlib output

The `\floatnotes` command is defined in the template as:
```latex
\newcommand{\floatnotes}[1]{%
\begin{quotation}\noindent \scriptsize #1\end{quotation}}
```

### LaTeX regression tables

```python
def reg_to_latex(results_list, dep_var_label, col_labels=None,
                 coef_subset=None, fe_rows=None, stats_rows=None,
                 filename=None, note=None, label=None):
    """
    Convert a list of linearmodels/statsmodels results to a LaTeX table.
    Follows the template format: caption → label → floatnotes → tabular body.

    Parameters
    ----------
    results_list : list of fitted model results
    dep_var_label : str, used as both caption title and dep var header
    col_labels : list of str for column headers
    coef_subset : list of str, variable names to display (None = all)
    fe_rows : dict, e.g., {'Firm FE': ['Yes','No','Yes'], 'Year FE': ['Yes','Yes','Yes']}
    stats_rows : list of str from ['nobs', 'r2', 'r2_adj']
    filename : str, path to save .tex file
    note : str, descriptive table note (sample, controls, clustering, etc.)
    label : str, LaTeX label (e.g., 'tab:baseline')
    """
    n_cols = len(results_list)
    if col_labels is None:
        col_labels = [f'({i+1})' for i in range(n_cols)]
    if stats_rows is None:
        stats_rows = ['nobs', 'r2_adj']
    if label is None:
        label = 'tab:' + dep_var_label.lower().replace(' ', '_')[:30]

    # Extract coefficients and t-stats
    rows = {}
    for res in results_list:
        for var in res.params.index:
            if var not in rows:
                rows[var] = []

    if coef_subset:
        display_vars = [v for v in coef_subset if v in rows]
    else:
        display_vars = list(rows.keys())

    lines = []
    lines.append(r'\begin{table}[!htbp]')
    lines.append(r'\centering')
    lines.append(f'\\caption{{{dep_var_label}}}')
    lines.append(f'\\label{{{label}}}\\vspace{{-2.5ex}}')
    # Descriptive note ABOVE the table body (matching template format)
    if note:
        lines.append(r'\floatnotes{' + note + ' t-statistics in parentheses.}')
    else:
        lines.append(r'\floatnotes{t-statistics in parentheses.}')
    lines.append(r'\small')
    lines.append(r'\begin{tabular}{l' + 'c' * n_cols + '}')
    lines.append(r'\toprule')
    lines.append(' & ' + ' & '.join(col_labels) + r' \\')
    lines.append(r'\midrule')

    for var in display_vars:
        coefs = []
        tstats = []
        for res in results_list:
            if var in res.params.index:
                coef = res.params[var]
                tval = res.tvalues[var]
                pval = res.pvalues[var]
                stars = '***' if pval < 0.01 else '**' if pval < 0.05 else '*' if pval < 0.1 else ''
                coefs.append(f'{coef:.4f}\\sym{{{stars}}}')
                tstats.append(f'({tval:.2f})')
            else:
                coefs.append('')
                tstats.append('')
        lines.append(var + ' & ' + ' & '.join(coefs) + r' \\')
        lines.append(' & ' + ' & '.join(tstats) + r' \\[0.5ex]')

    lines.append(r'\midrule')

    if fe_rows:
        for label_fe, vals in fe_rows.items():
            lines.append(label_fe + ' & ' + ' & '.join(vals) + r' \\')

    for stat in stats_rows:
        vals = []
        for res in results_list:
            if stat == 'nobs':
                vals.append(f'{int(res.nobs):,}')
            elif stat == 'r2':
                vals.append(f'{res.rsquared:.3f}')
            elif stat == 'r2_adj':
                r2 = getattr(res, 'rsquared_adj', getattr(res, 'rsquared', np.nan))
                vals.append(f'{r2:.3f}')
        stat_label = {'nobs': 'Observations', 'r2': '$R^2$', 'r2_adj': 'Adj. $R^2$'}[stat]
        lines.append(stat_label + ' & ' + ' & '.join(vals) + r' \\')

    lines.append(r'\bottomrule')
    sig_note = r'\footnotesize \sym{*} $p<0.10$, \sym{**} $p<0.05$, \sym{***} $p<0.01$.'
    lines.append(r'\multicolumn{' + str(n_cols + 1) + '}{l}{' + sig_note + '}')
    lines.append(r'\end{tabular}')
    lines.append(r'\end{table}')

    tex = '\n'.join(lines)
    if filename:
        Path(filename).write_text(tex)
        print(f"Table saved to {filename}")
    return tex
```

### Summary statistics table

```python
def summary_stats_latex(df, variables, labels=None, stats=None, filename=None):
    """
    Generate a LaTeX summary statistics table.

    Parameters
    ----------
    df : DataFrame
    variables : list of column names
    labels : dict mapping column names to display labels
    stats : list from ['mean', 'sd', 'p25', 'median', 'p75', 'n']
    """
    if labels is None:
        labels = {v: v for v in variables}
    if stats is None:
        stats = ['mean', 'sd', 'p25', 'median', 'p75', 'n']

    stat_funcs = {
        'mean': lambda x: f'{x.mean():.3f}',
        'sd': lambda x: f'{x.std():.3f}',
        'p25': lambda x: f'{x.quantile(0.25):.3f}',
        'median': lambda x: f'{x.median():.3f}',
        'p75': lambda x: f'{x.quantile(0.75):.3f}',
        'n': lambda x: f'{x.notna().sum():,}',
    }
    stat_labels = {
        'mean': 'Mean', 'sd': 'SD', 'p25': 'P25',
        'median': 'Median', 'p75': 'P75', 'n': 'N',
    }

    header = ['Variable'] + [stat_labels[s] for s in stats]
    lines = []
    lines.append(r'\begin{table}[!htbp]')
    lines.append(r'\centering')
    lines.append(r'\caption{Summary Statistics}')
    lines.append(r'\label{tab:summary}\vspace{-2.5ex}')
    lines.append(r'\floatnotes{This table reports summary statistics for the main variables. The sample period is [PERIOD]. See Appendix Table~\ref{tab:appendix_variables} for variable definitions.}')
    lines.append(r'\small')
    lines.append(r'\begin{tabularx}{\textwidth}{@{}X' + 'r' * len(stats) + '@{}}')
    lines.append(r'\toprule')
    lines.append(' & '.join([f'\\textbf{{{h}}}' for h in header]) + r' \\')
    lines.append(r'\midrule')

    for var in variables:
        row = [labels.get(var, var)]
        for s in stats:
            row.append(stat_funcs[s](df[var]))
        lines.append(' & '.join(row) + r' \\')

    lines.append(r'\bottomrule')
    lines.append(r'\end{tabularx}')
    lines.append(r'\end{table}')

    tex = '\n'.join(lines)
    if filename:
        Path(filename).write_text(tex)
    return tex
```

## Publication-ready figures

### Global figure defaults

```python
# Set once at the top of every figure script
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'Computer Modern Roman'],
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.figsize': (6.5, 4.5),       # fits single-column journal layout
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.grid': False,
    'axes.spines.top': False,
    'axes.spines.right': False,
})
COLORS = ['#2c3e50', '#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']
```

### Event-study plot

```python
def plot_event_study(coefs, ci_lower, ci_upper, event_times,
                     ref_period=-1, ylabel='Coefficient', xlabel='Event time',
                     title=None, filename=None):
    """
    Plot event-study coefficients with confidence intervals.

    Parameters
    ----------
    coefs : array-like of coefficient estimates
    ci_lower, ci_upper : array-like of CI bounds
    event_times : array-like of integer event-time indices
    ref_period : int, the omitted reference period (plotted as zero)
    """
    fig, ax = plt.subplots(figsize=(7, 4.5))

    # Insert the reference period
    all_times = sorted(set(list(event_times) + [ref_period]))
    plot_coefs = []
    plot_lo = []
    plot_hi = []
    j = 0
    for t in all_times:
        if t == ref_period:
            plot_coefs.append(0)
            plot_lo.append(0)
            plot_hi.append(0)
        else:
            plot_coefs.append(coefs[j])
            plot_lo.append(ci_lower[j])
            plot_hi.append(ci_upper[j])
            j += 1

    ax.axhline(y=0, color='grey', linewidth=0.8, linestyle='--')
    ax.axvline(x=-0.5, color='grey', linewidth=0.8, linestyle=':', alpha=0.6)

    ax.plot(all_times, plot_coefs, 'o-', color=COLORS[0], markersize=5, linewidth=1.5)
    ax.fill_between(all_times, plot_lo, plot_hi, alpha=0.15, color=COLORS[0])

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.set_xticks(all_times)

    fig.tight_layout()
    if filename:
        fig.savefig(filename)
        print(f"Figure saved to {filename}")
    return fig, ax
```

### Coefficient plot

```python
def plot_coefficients(labels, coefs, ci_lower, ci_upper,
                      title=None, filename=None):
    """Horizontal coefficient plot with confidence intervals."""
    fig, ax = plt.subplots(figsize=(6, 0.4 * len(labels) + 1.5))

    y_pos = np.arange(len(labels))
    ax.axvline(x=0, color='grey', linewidth=0.8, linestyle='--')
    ax.errorbar(coefs, y_pos, xerr=[np.array(coefs) - np.array(ci_lower),
                np.array(ci_upper) - np.array(coefs)],
                fmt='o', color=COLORS[0], markersize=6, capsize=3, linewidth=1.5)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    if title:
        ax.set_title(title)

    fig.tight_layout()
    if filename:
        fig.savefig(filename)
    return fig, ax
```

### Binned scatter plot

```python
def plot_binned_scatter(df, x, y, n_bins=20, controls=None, absorb=None,
                        xlabel=None, ylabel=None, filename=None):
    """
    Binned scatter plot, optionally residualizing on controls.
    Standard visualization for finance papers.
    """
    plot_df = df[[x, y]].dropna().copy()

    if controls:
        import statsmodels.api as sm
        for var in [x, y]:
            X = sm.add_constant(df[controls].loc[plot_df.index])
            resid = sm.OLS(plot_df[var], X, missing='drop').fit().resid
            plot_df[var] = resid

    plot_df['bin'] = pd.qcut(plot_df[x], n_bins, labels=False, duplicates='drop')
    binned = plot_df.groupby('bin').agg({x: 'mean', y: 'mean'}).reset_index()

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.scatter(binned[x], binned[y], color=COLORS[0], s=40, zorder=3)

    # Fit line through binned means
    z = np.polyfit(binned[x], binned[y], 1)
    p = np.poly1d(z)
    x_line = np.linspace(binned[x].min(), binned[x].max(), 100)
    ax.plot(x_line, p(x_line), color=COLORS[1], linewidth=1.5, linestyle='--')

    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)

    fig.tight_layout()
    if filename:
        fig.savefig(filename)
    return fig, ax
```

## Real-estate-specific code

### Spatial operations

```python
import geopandas as gpd
from shapely.geometry import Point

# Load property data and convert to GeoDataFrame
df_props = pd.read_csv(RAW / 'properties.csv')
gdf = gpd.GeoDataFrame(
    df_props,
    geometry=gpd.points_from_xy(df_props['longitude'], df_props['latitude']),
    crs='EPSG:4326'
)

# Spatial join: assign Census tract to each property
tracts = gpd.read_file(RAW / 'census_tracts.shp')
gdf = gpd.sjoin(gdf, tracts[['GEOID', 'geometry']], how='left', predicate='within')

# Distance to a point (e.g., new transit station)
station = Point(-96.7970, 32.7767)  # lon, lat
gdf_proj = gdf.to_crs('EPSG:3857')  # project for distance in meters
station_proj = gpd.GeoSeries([station], crs='EPSG:4326').to_crs('EPSG:3857').iloc[0]
gdf_proj['dist_station_m'] = gdf_proj.geometry.distance(station_proj)
gdf_proj['dist_station_km'] = gdf_proj['dist_station_m'] / 1000
```

### Conley spatial standard errors

```python
# Using the conleySE package or manual implementation
# pip install spreg
from spreg import OLS as Spatial_OLS
from libpysal.weights import DistanceBand

# Create spatial weights (e.g., 10km bandwidth)
coords = list(zip(gdf_proj.geometry.x, gdf_proj.geometry.y))
w = DistanceBand(coords, threshold=10000, binary=True, silence_warnings=True)

# OLS with Conley SEs
spatial_ols = Spatial_OLS(
    y=gdf_proj[['log_price']].values,
    x=gdf_proj[['treatment', 'sqft', 'bedrooms']].values,
    w=w,
    name_y='log_price',
    name_x=['treatment', 'sqft', 'bedrooms'],
    robust='hac'
)
print(spatial_ols.summary)
```

### Repeat-sales index

```python
def repeat_sales_index(df, price_col='price', date_col='sale_date', prop_col='property_id'):
    """
    Estimate a simple repeat-sales house price index.

    df must contain properties with at least two sales.
    """
    df = df.sort_values([prop_col, date_col])

    # Keep only repeat sales
    df['sale_num'] = df.groupby(prop_col).cumcount() + 1
    df['n_sales'] = df.groupby(prop_col)[prop_col].transform('count')
    df_rs = df[df['n_sales'] >= 2].copy()

    # Create sale pairs
    df_rs['log_price'] = np.log(df_rs[price_col])
    df_rs['prev_log_price'] = df_rs.groupby(prop_col)['log_price'].shift(1)
    df_rs['prev_date'] = df_rs.groupby(prop_col)[date_col].shift(1)
    pairs = df_rs.dropna(subset=['prev_log_price']).copy()
    pairs['log_return'] = pairs['log_price'] - pairs['prev_log_price']

    # Create time dummies and estimate
    import statsmodels.api as sm
    pairs['period'] = pd.to_datetime(pairs[date_col]).dt.to_period('Q')
    pairs['prev_period'] = pd.to_datetime(pairs['prev_date']).dt.to_period('Q')

    periods = sorted(pairs['period'].unique())
    for p in periods[1:]:  # first period is reference
        pairs[f'd_{p}'] = ((pairs['period'] == p).astype(int) -
                           (pairs['prev_period'] == p).astype(int))

    time_dummies = [f'd_{p}' for p in periods[1:]]
    X = pairs[time_dummies]
    y = pairs['log_return']
    model = sm.OLS(y, X).fit()

    index = pd.Series([0] + list(model.params), index=periods, name='log_index')
    index = np.exp(index) * 100  # normalize to 100 at base period

    return index
```

## Project structure

When generating code for a full project, organize as:

```
project/
  raw/                   # Untouched source data (read-only)
  build/                 # Cleaned and merged intermediate datasets
    01_clean_crsp.py
    02_clean_compustat.py
    03_merge_ccm.py
    04_construct_variables.py
  analysis/              # Scripts that produce tables and figures
    01_summary_stats.py
    02_baseline_regression.py
    03_robustness.py
    04_mechanism.py
    05_heterogeneity.py
  output/
    tables/              # .tex files
    figures/             # .pdf or .png files
    logs/                # Regression logs and diagnostics
  codebook/              # Variable definitions
  utils/                 # Shared helper functions
    data_utils.py        # Winsorize, merge helpers, date alignment
    table_utils.py       # LaTeX table generation
    figure_utils.py      # Figure defaults and plot functions
    portfolio_utils.py   # Portfolio sort and alpha functions (AP papers)
  run_all.py             # Master script that executes the full pipeline
  requirements.txt       # Pin all package versions
```

### Master script

```python
"""
run_all.py — Execute the full pipeline from raw data to output.
"""
import subprocess
import sys
from pathlib import Path

scripts = [
    'build/01_clean_crsp.py',
    'build/02_clean_compustat.py',
    'build/03_merge_ccm.py',
    'build/04_construct_variables.py',
    'analysis/01_summary_stats.py',
    'analysis/02_baseline_regression.py',
    'analysis/03_robustness.py',
    'analysis/04_mechanism.py',
    'analysis/05_heterogeneity.py',
]

for script in scripts:
    print(f"\n{'='*60}\nRunning {script}\n{'='*60}")
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"ERROR in {script}:\n{result.stderr}")
        sys.exit(1)

print("\nPipeline complete. Output in output/tables/ and output/figures/")
```

## Tool integration (Corbis MCP)

- `search_papers` (query: specific Python method + finance application, e.g., "Fama-MacBeth Python linearmodels") → find papers and documentation for implementation guidance.
- `internet_search` (Enterprise; fallback: `search_papers` for academic content, or ask user for URLs) (query: "[package name] documentation [specific function]") → find library documentation for unfamiliar functions.
- `read_web_page` (Enterprise) (documentation URL) → read package docs when needed. If unavailable, ask the user to provide the URL directly.
- `fred_series_batch` (series IDs) → pull FRED data directly for macro controls.
- `search_datasets` → discover data sources when the user is unsure what's available.
- `export_citations` (format: `bibtex`) → export BibTeX entries for methodological papers underlying the generated code (e.g., Callaway-Sant'Anna for staggered DiD, Fama-MacBeth for cross-sectional tests, Conley for spatial SEs). Offer this after the code package is produced.
- `format_citation` → format individual method citations for inclusion in code comments or the paper's reference list.

## Guardrails

- Do not generate code that modifies raw data files. Always read from `raw/`, write to `build/`.
- Do not use deprecated pandas syntax (`append`, `inplace=True` in chained operations).
- Do not suppress warnings globally — suppress only specific known warnings.
- Always include observation counts after merges and filters.
- Always cluster standard errors at the level of treatment variation — do not default to heteroskedasticity-robust only.
- Do not hardcode file paths — use `Path` objects relative to the project root.
- Pin package versions in `requirements.txt` for reproducibility.
- When the user provides Stata code to translate, preserve the exact specification (same fixed effects, same clustering, same sample restrictions).
- If a computation will be slow (>1 minute), warn the user and suggest optimizations (e.g., `polars`, chunked processing, or pre-filtering).
- For asset-pricing code, always use NYSE breakpoints for portfolio sorts and value-weighted returns as the default.
- For real-estate code, always project coordinates before computing distances.

## Output format

```
# Code package
## Task description
## Dependencies (with versions)
## Script(s) with full code
## Expected output (what tables/figures/datasets this produces)
## How to run
## Key assumptions and choices made
```

## Example prompts
- "Write the Python code to merge CRSP and Compustat via CCM and construct standard variables."
- "Generate an event-study plot from these regression results."
- "Create a LaTeX regression table from these three specifications."
- "Port this Stata DiD code to Python using linearmodels."
- "Build the full portfolio-sort pipeline for this anomaly paper."
- "Write the code to compute Conley standard errors for my housing regression."
- "Create a binned scatter plot of house prices and distance to transit."
- "Set up the project structure for a corporate-finance paper with CRSP, Compustat, and IBES."
