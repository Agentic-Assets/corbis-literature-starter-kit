# Python Code Examples for Empirical Finance

## Import block template

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

## WRDS data access

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

## CCM merge (CRSP-Compustat)

```python
df_ccm = db.raw_sql("""
    SELECT gvkey, lpermno AS permno, linktype, linkprim, linkdt, linkenddt
    FROM crsp.ccmxpf_lnkhist
    WHERE linktype IN ('LU', 'LC')
        AND linkprim IN ('P', 'C')
""")

df_comp['datadate'] = pd.to_datetime(df_comp['datadate'])
df_ccm['linkdt'] = pd.to_datetime(df_ccm['linkdt'])
df_ccm['linkenddt'] = pd.to_datetime(df_ccm['linkenddt']).fillna(pd.Timestamp('2099-12-31'))

df_comp_crsp = df_comp.merge(df_ccm, on='gvkey', how='inner')
df_comp_crsp = df_comp_crsp[
    (df_comp_crsp['datadate'] >= df_comp_crsp['linkdt']) &
    (df_comp_crsp['datadate'] <= df_comp_crsp['linkenddt'])
]
df_comp_crsp = df_comp_crsp.sort_values(['gvkey', 'datadate', 'linkprim'])
df_comp_crsp = df_comp_crsp.drop_duplicates(subset=['gvkey', 'datadate'], keep='first')
```

## Date alignment (avoid look-ahead bias)

```python
# Fama-French timing: fiscal year ending in calendar year t
# available for portfolios formed in June of year t+1
df_comp_crsp['jdate'] = df_comp_crsp['datadate'] + pd.DateOffset(months=6)
df_comp_crsp['jdate'] = df_comp_crsp['jdate'] + pd.offsets.MonthEnd(0)

df_crsp['jdate'] = pd.to_datetime(df_crsp['date']) + pd.offsets.MonthEnd(0)
df = df_crsp.merge(df_comp_crsp, on=['permno', 'jdate'], how='left')
```

## Winsorization

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
```

## Panel regressions with linearmodels

```python
from linearmodels.panel import PanelOLS
from linearmodels.iv import IV2SLS

df = df.set_index(['permno', 'date'])

# OLS with entity and time FE, clustered SEs
model = PanelOLS.from_formula(
    'y ~ 1 + x1 + x2 + x3 + EntityEffects + TimeEffects',
    data=df, drop_absorbed=True
)
result = model.fit(cov_type='clustered', cluster_entity=True)

# Two-way clustering
result_2way = model.fit(cov_type='clustered', cluster_entity=True, cluster_time=True)

# IV regression
iv_model = IV2SLS.from_formula(
    'y ~ 1 + x2 + x3 + EntityEffects + TimeEffects ~ [x1 ~ z1 + z2]',
    data=df
)
iv_result = iv_model.fit(cov_type='clustered', cluster_entity=True)
```

## Fama-MacBeth regressions

```python
from linearmodels.asset_pricing import FamaMacBeth

fm_model = FamaMacBeth.from_formula('ret_excess ~ 1 + beta + size + bm + mom', data=df)
fm_result = fm_model.fit(cov_type='kernel', bandwidth=6)
```

## Difference-in-differences

```python
# Standard 2x2 DiD
model_did = PanelOLS.from_formula(
    'y ~ 1 + treated:post + controls + EntityEffects + TimeEffects',
    data=df, drop_absorbed=True
)
did_result = model_did.fit(cov_type='clustered', cluster_entity=True)

# Event study with leads and lags
for k in range(-4, 8):
    if k == -1: continue  # omit t-1 as reference
    col = f'event_t{k:+d}'
    df[col] = (df['event_time'] == k).astype(int)

event_vars = ' + '.join([f'event_t{k:+d}' for k in range(-4, 8) if k != -1])
model_es = PanelOLS.from_formula(
    f'y ~ 1 + {event_vars} + controls + EntityEffects + TimeEffects',
    data=df, drop_absorbed=True
)
es_result = model_es.fit(cov_type='clustered', cluster_entity=True)
```

## Staggered DiD (Callaway-Sant'Anna)

```python
from csdid import ATTgt

att = ATTgt(
    data=df.reset_index(),
    yname='y', gname='first_treat_year',
    tname='year', idname='firm_id',
    control_group='notyettreated'
)
results = att.fit()
results.summary()
agg_es = results.aggregate('event')
agg_es.summary()
```

## Portfolio sorts

```python
def portfolio_sort(df, signal, n_portfolios=5, nyse_breakpoints=True, weight='vw'):
    """Single-sort portfolios with NYSE breakpoints and value-weighting."""
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
```

## Alpha table

```python
def alpha_table(port_returns, factor_df, models=['CAPM', 'FF3', 'FF5']):
    """Compute alphas for each portfolio against multiple factor models."""
    import statsmodels.api as sm
    factor_cols = {
        'CAPM': ['mktrf'], 'FF3': ['mktrf', 'smb', 'hml'],
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
                'portfolio': col, 'model': model_name,
                'alpha': reg.params['const'] * 100, 't_stat': reg.tvalues['const'],
            })
    return pd.DataFrame(results)
```

## Quick exploration function

```python
def explore_reg(df, y, x_list, fe=None, cluster=None, controls=None, label=None):
    """Run a quick regression and print a one-line summary. For exploration only."""
    from linearmodels.panel import PanelOLS
    import statsmodels.formula.api as smf

    if label:
        print(f"\n{'='*60}\n{label}\n{'='*60}")
    print(f"{'Variable':<30} {'Coef':>10} {'t-stat':>10} {'N':>10} {'R2':>8}")
    print('-' * 72)

    for x in x_list:
        try:
            rhs = [x] + (controls or [])
            if fe:
                fe_cols = fe if isinstance(fe, list) else [fe]
                df_reg = df.set_index(fe_cols)[[y] + rhs].dropna()
                formula = f'{y} ~ 1 + {" + ".join(rhs)} + EntityEffects'
                res = PanelOLS.from_formula(formula, df_reg).fit(
                    cov_type='clustered', cluster_entity=True)
            else:
                formula = f'{y} ~ {" + ".join(rhs)}'
                res = smf.ols(formula, df.dropna(subset=[y] + rhs)).fit(
                    cov_type='cluster', cov_kwds={'groups': df.dropna(subset=[y] + rhs)[cluster]}
                    if cluster else {})
            coef = res.params[x]
            tval = res.tvalues[x]
            nobs = int(res.nobs)
            r2 = getattr(res, 'rsquared_adj', getattr(res, 'rsquared', float('nan')))
            print(f'{x:<30} {coef:>10.4f} {tval:>10.2f} {nobs:>10,} {r2:>8.3f}')
        except Exception as e:
            print(f'{x:<30} {"FAILED":>10} — {str(e)[:40]}')
```

## LaTeX regression table

```python
def reg_to_latex(results_list, dep_var_label, col_labels=None,
                 coef_subset=None, fe_rows=None, stats_rows=None,
                 filename=None, note=None, label=None):
    """Convert linearmodels/statsmodels results to a LaTeX table.
    Follows template format: caption → label → floatnotes → tabular body."""
    n_cols = len(results_list)
    if col_labels is None:
        col_labels = [f'({i+1})' for i in range(n_cols)]
    if stats_rows is None:
        stats_rows = ['nobs', 'r2_adj']
    if label is None:
        label = 'tab:' + dep_var_label.lower().replace(' ', '_')[:30]

    rows = {}
    for res in results_list:
        for var in res.params.index:
            if var not in rows:
                rows[var] = []
    display_vars = [v for v in coef_subset if v in rows] if coef_subset else list(rows.keys())

    lines = []
    lines.append(r'\begin{table}[!htbp]')
    lines.append(r'\centering')
    lines.append(f'\\caption{{{dep_var_label}}}')
    lines.append(f'\\label{{{label}}}\\vspace{{-2.5ex}}')
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
        coefs, tstats = [], []
        for res in results_list:
            if var in res.params.index:
                coef = res.params[var]
                tval = res.tvalues[var]
                pval = res.pvalues[var]
                stars = '***' if pval < 0.01 else '**' if pval < 0.05 else '*' if pval < 0.1 else ''
                coefs.append(f'{coef:.4f}\\sym{{{stars}}}')
                tstats.append(f'({tval:.2f})')
            else:
                coefs.append(''); tstats.append('')
        lines.append(var + ' & ' + ' & '.join(coefs) + r' \\')
        lines.append(' & ' + ' & '.join(tstats) + r' \\[0.5ex]')

    lines.append(r'\midrule')
    if fe_rows:
        for label_fe, vals in fe_rows.items():
            lines.append(label_fe + ' & ' + ' & '.join(vals) + r' \\')
    for stat in stats_rows:
        vals = []
        for res in results_list:
            if stat == 'nobs': vals.append(f'{int(res.nobs):,}')
            elif stat == 'r2': vals.append(f'{res.rsquared:.3f}')
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

## Summary statistics table

```python
def summary_stats_latex(df, variables, labels=None, stats=None, filename=None):
    """Generate a LaTeX summary statistics table."""
    if labels is None: labels = {v: v for v in variables}
    if stats is None: stats = ['mean', 'sd', 'p25', 'median', 'p75', 'n']
    stat_funcs = {
        'mean': lambda x: f'{x.mean():.3f}', 'sd': lambda x: f'{x.std():.3f}',
        'p25': lambda x: f'{x.quantile(0.25):.3f}', 'median': lambda x: f'{x.median():.3f}',
        'p75': lambda x: f'{x.quantile(0.75):.3f}', 'n': lambda x: f'{x.notna().sum():,}',
    }
    stat_labels = {'mean': 'Mean', 'sd': 'SD', 'p25': 'P25', 'median': 'Median', 'p75': 'P75', 'n': 'N'}
    header = ['Variable'] + [stat_labels[s] for s in stats]

    lines = [r'\begin{table}[!htbp]', r'\centering', r'\caption{Summary Statistics}',
             r'\label{tab:summary}\vspace{-2.5ex}',
             r'\floatnotes{This table reports summary statistics for the main variables. The sample period is [PERIOD]. See Appendix Table~\ref{tab:appendix_variables} for variable definitions.}',
             r'\small', r'\begin{tabularx}{\textwidth}{@{}X' + 'r' * len(stats) + '@{}}',
             r'\toprule',
             ' & '.join([f'\\textbf{{{h}}}' for h in header]) + r' \\',
             r'\midrule']
    for var in variables:
        row = [labels.get(var, var)] + [stat_funcs[s](df[var]) for s in stats]
        lines.append(' & '.join(row) + r' \\')
    lines += [r'\bottomrule', r'\end{tabularx}', r'\end{table}']

    tex = '\n'.join(lines)
    if filename: Path(filename).write_text(tex)
    return tex
```

## Publication figure defaults

```python
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'Computer Modern Roman'],
    'font.size': 11, 'axes.labelsize': 12, 'axes.titlesize': 13,
    'xtick.labelsize': 10, 'ytick.labelsize': 10, 'legend.fontsize': 10,
    'figure.figsize': (6.5, 4.5), 'figure.dpi': 300,
    'savefig.dpi': 300, 'savefig.bbox': 'tight',
    'axes.grid': False, 'axes.spines.top': False, 'axes.spines.right': False,
})
COLORS = ['#2c3e50', '#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']
```

## Event-study plot

```python
def plot_event_study(coefs, ci_lower, ci_upper, event_times,
                     ref_period=-1, ylabel='Coefficient', xlabel='Event time',
                     title=None, filename=None):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    all_times = sorted(set(list(event_times) + [ref_period]))
    plot_coefs, plot_lo, plot_hi = [], [], []
    j = 0
    for t in all_times:
        if t == ref_period:
            plot_coefs.append(0); plot_lo.append(0); plot_hi.append(0)
        else:
            plot_coefs.append(coefs[j]); plot_lo.append(ci_lower[j]); plot_hi.append(ci_upper[j])
            j += 1
    ax.axhline(y=0, color='grey', linewidth=0.8, linestyle='--')
    ax.axvline(x=-0.5, color='grey', linewidth=0.8, linestyle=':', alpha=0.6)
    ax.plot(all_times, plot_coefs, 'o-', color=COLORS[0], markersize=5, linewidth=1.5)
    ax.fill_between(all_times, plot_lo, plot_hi, alpha=0.15, color=COLORS[0])
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
    if title: ax.set_title(title)
    ax.set_xticks(all_times)
    fig.tight_layout()
    if filename: fig.savefig(filename)
    return fig, ax
```

## Binned scatter plot

```python
def plot_binned_scatter(df, x, y, n_bins=20, controls=None, absorb=None,
                        xlabel=None, ylabel=None, filename=None):
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
    z = np.polyfit(binned[x], binned[y], 1)
    p = np.poly1d(z)
    x_line = np.linspace(binned[x].min(), binned[x].max(), 100)
    ax.plot(x_line, p(x_line), color=COLORS[1], linewidth=1.5, linestyle='--')
    ax.set_xlabel(xlabel or x); ax.set_ylabel(ylabel or y)
    fig.tight_layout()
    if filename: fig.savefig(filename)
    return fig, ax
```

## Spatial operations

```python
import geopandas as gpd
from shapely.geometry import Point

# Load and convert to GeoDataFrame
df_props = pd.read_csv(RAW / 'properties.csv')
gdf = gpd.GeoDataFrame(
    df_props,
    geometry=gpd.points_from_xy(df_props['longitude'], df_props['latitude']),
    crs='EPSG:4326'
)

# Spatial join: assign Census tract
tracts = gpd.read_file(RAW / 'census_tracts.shp')
gdf = gpd.sjoin(gdf, tracts[['GEOID', 'geometry']], how='left', predicate='within')

# Distance computation (project first!)
gdf_proj = gdf.to_crs('EPSG:3857')
station_proj = gpd.GeoSeries([Point(-96.7970, 32.7767)], crs='EPSG:4326').to_crs('EPSG:3857').iloc[0]
gdf_proj['dist_station_km'] = gdf_proj.geometry.distance(station_proj) / 1000
```

## Conley spatial standard errors

```python
from spreg import OLS as Spatial_OLS
from libpysal.weights import DistanceBand

coords = list(zip(gdf_proj.geometry.x, gdf_proj.geometry.y))
w = DistanceBand(coords, threshold=10000, binary=True, silence_warnings=True)
spatial_ols = Spatial_OLS(
    y=gdf_proj[['log_price']].values,
    x=gdf_proj[['treatment', 'sqft', 'bedrooms']].values,
    w=w, name_y='log_price', name_x=['treatment', 'sqft', 'bedrooms'],
    robust='hac'
)
```

## Project structure

```
project/
  raw/                   # Untouched source data (read-only)
  build/                 # Cleaned and merged intermediate datasets
    01_clean_crsp.py
    02_clean_compustat.py
    03_merge_ccm.py
    04_construct_variables.py
  explore/               # Throwaway exploration scripts
  analysis/              # Promoted scripts producing final output
  output/
    tables/              # .tex files
    figures/             # .pdf or .png files
  notes/
    lab_notebook.md
  codebook/              # Variable definitions
  utils/                 # Shared helpers
  paper/                 # LaTeX manuscript (copy of latex_template/)
  run_all.py             # Master script
  requirements.txt
```

## Master script

```python
"""run_all.py — Execute the full pipeline from raw data to output."""
import subprocess, sys
from pathlib import Path

scripts = [
    'build/01_clean_crsp.py', 'build/02_clean_compustat.py',
    'build/03_merge_ccm.py', 'build/04_construct_variables.py',
    'analysis/01_summary_stats.py', 'analysis/02_baseline_regression.py',
    'analysis/03_robustness.py', 'analysis/04_mechanism.py',
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
