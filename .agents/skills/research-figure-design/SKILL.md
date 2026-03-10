---
name: research-figure-design
description: "Design and generate publication-ready figures for finance and real-estate papers. Use for figure planning, plot selection, visual design, maps, diagrams, and journal-quality Python code for every common figure type."
---

# Research Figure Design

Every figure must earn its place. A figure that restates what a table already shows is a wasted slot. A figure that reveals a pattern no table can convey is worth more than three robustness tables.

## When to use this skill

- The user needs to decide which figures the paper should include
- The user needs Python code for a specific figure type
- The user wants to convert a table into a visual for a talk or paper
- The user needs maps, diagrams, or conceptual figures
- The user wants to improve existing figures for journal submission

## Figure planning workflow

1. Identify the paper's key messages (main result, mechanism, heterogeneity, dynamics).
2. For each message, ask: is a figure or a table the better vehicle?
3. Assign each figure a specific job from the catalog below.
4. Decide placement: main paper vs. appendix vs. presentation only.
5. Generate the code with journal-quality defaults.
6. Write self-contained figure notes.

### When to use a figure instead of a table

| Use a figure when... | Use a table when... |
|---|---|
| The pattern is nonlinear or dynamic | The reader needs exact coefficients |
| Spatial variation matters | Multiple specifications need comparison |
| You want to show a distribution or trend | Precision of individual estimates matters |
| The result is best seen as a comparison | The result is a set of heterogeneous effects |
| A talk audience needs to grasp it in seconds | The referee needs to verify the numbers |

## Standard figure set by paper type

### Corporate finance / causal inference paper
1. **Motivating trend** (time series showing the phenomenon)
2. **Event-study plot** (main result, pre/post with CIs)
3. **Parallel trends** (DiD validity)
4. **Binned scatter** (key relationship, residualized)
5. **Coefficient plot** (heterogeneity across subgroups)
6. **Mechanism bar chart** (channel decomposition)

### Asset pricing paper
1. **Cumulative return plot** (long-short portfolio over time)
2. **Portfolio sort bar chart** (mean returns across quintiles/deciles)
3. **Factor exposure heatmap** (loadings across models)
4. **Time-series alpha plot** (rolling or expanding window)
5. **Turnover/capacity plot** (implementability)

### Real estate paper
1. **Choropleth map** (treatment geography, price variation)
2. **Boundary RD plot** (outcome vs. distance to boundary)
3. **Event-study or spatial DiD plot** (main result)
4. **Binned scatter** (hedonic relationship)
5. **Density map** (transaction locations, treatment intensity)

### Descriptive / measurement paper
1. **Distribution plots** (histograms, KDEs of key variables)
2. **Time-series trends** (evolution of the measure)
3. **Correlation heatmap** (relationship to existing measures)
4. **Cross-sectional scatter** (new measure vs. existing proxies)

## Figure catalog with Python code

### Global defaults (use in every script)

```python
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np
import pandas as pd
from pathlib import Path

# Journal-quality defaults
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'Computer Modern Roman'],
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.figsize': (6.5, 4.5),
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1,
    'axes.grid': False,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.linewidth': 0.8,
    'lines.linewidth': 1.5,
    'patch.linewidth': 0.8,
})

# Consistent color palette
COLORS = {
    'primary': '#2c3e50',
    'secondary': '#e74c3c',
    'tertiary': '#3498db',
    'quaternary': '#2ecc71',
    'accent1': '#f39c12',
    'accent2': '#9b59b6',
    'light_gray': '#bdc3c7',
    'ci_fill': '#2c3e50',
}
COLOR_LIST = ['#2c3e50', '#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']

OUTPUT = Path('output/figures')
OUTPUT.mkdir(parents=True, exist_ok=True)

def save_fig(fig, name, formats=('pdf', 'png')):
    """Save figure in multiple formats."""
    for fmt in formats:
        fig.savefig(OUTPUT / f'{name}.{fmt}')
    print(f"Saved: {name}")
    plt.close(fig)
```

---

### 1. Event-study plot

The workhorse of causal inference papers. Shows dynamic treatment effects with pre-trends.

```python
def plot_event_study(coefs, ci_lower, ci_upper, event_times,
                     ref_period=-1, ylabel='Coefficient estimate',
                     xlabel='Event time', title=None, filename=None,
                     shade_post=True, annotate_coef=None):
    """
    Event-study plot with confidence intervals.

    Parameters
    ----------
    coefs, ci_lower, ci_upper : array-like, estimated coefficients and CI bounds
    event_times : array-like of int, event-time indices (excluding ref_period)
    ref_period : int, omitted reference period (plotted as zero)
    shade_post : bool, lightly shade the post-treatment region
    annotate_coef : int or None, event time to annotate with coefficient value
    """
    fig, ax = plt.subplots(figsize=(7, 4.5))

    # Build full series including reference period
    all_times = sorted(set(list(event_times) + [ref_period]))
    y_vals, lo_vals, hi_vals = [], [], []
    j = 0
    for t in all_times:
        if t == ref_period:
            y_vals.append(0); lo_vals.append(0); hi_vals.append(0)
        else:
            y_vals.append(coefs[j]); lo_vals.append(ci_lower[j]); hi_vals.append(ci_upper[j])
            j += 1

    # Zero line and treatment marker
    ax.axhline(y=0, color='grey', linewidth=0.8, linestyle='--', zorder=1)
    ax.axvline(x=-0.5, color='grey', linewidth=0.8, linestyle=':', alpha=0.5, zorder=1)

    # Shade post-treatment region
    if shade_post:
        ax.axvspan(-0.5, max(all_times) + 0.5, alpha=0.04, color=COLORS['primary'], zorder=0)

    # Point estimates and CIs
    ax.plot(all_times, y_vals, 'o-', color=COLORS['primary'], markersize=5, zorder=3)
    ax.fill_between(all_times, lo_vals, hi_vals, alpha=0.15, color=COLORS['ci_fill'], zorder=2)

    # Optional annotation
    if annotate_coef is not None and annotate_coef in all_times:
        idx = all_times.index(annotate_coef)
        ax.annotate(f'{y_vals[idx]:.3f}', xy=(annotate_coef, y_vals[idx]),
                    xytext=(10, 10), textcoords='offset points', fontsize=9,
                    arrowprops=dict(arrowstyle='->', color='grey', lw=0.8))

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xticks(all_times)
    if title:
        ax.set_title(title)

    fig.tight_layout()
    if filename:
        save_fig(fig, filename)
    return fig, ax
```

**Figure note template:** "This figure plots the estimated coefficients $\beta_k$ from Equation (X), which regresses [outcome] on event-time indicators relative to [event], controlling for [FE and controls]. The omitted category is $k = [ref]$. The shaded region indicates the 95% confidence interval based on standard errors clustered at the [level] level. The vertical dashed line marks the [event]."

---

### 2. Parallel trends plot

Specifically for DiD validity. Distinct from event study because it shows raw or adjusted means for treatment and control groups.

```python
def plot_parallel_trends(df, time_col, outcome_col, group_col,
                         treatment_time=None, ylabel=None, xlabel=None,
                         group_labels=None, filename=None):
    """
    Parallel trends: mean outcome over time for treatment and control groups.

    Parameters
    ----------
    df : DataFrame
    time_col : str, time variable
    outcome_col : str, outcome variable
    group_col : str, binary treatment indicator
    treatment_time : scalar, time of treatment (vertical line)
    group_labels : dict, e.g., {1: 'Treated', 0: 'Control'}
    """
    fig, ax = plt.subplots(figsize=(7, 4.5))

    if group_labels is None:
        group_labels = {1: 'Treated', 0: 'Control'}

    means = df.groupby([time_col, group_col])[outcome_col].mean().reset_index()

    for i, (group, label) in enumerate(group_labels.items()):
        subset = means[means[group_col] == group]
        ax.plot(subset[time_col], subset[outcome_col], 'o-',
                color=COLOR_LIST[i], label=label, markersize=4)

    if treatment_time is not None:
        ax.axvline(x=treatment_time, color='grey', linewidth=0.8, linestyle=':', alpha=0.6)
        ax.text(treatment_time, ax.get_ylim()[1] * 0.98, ' Treatment',
                fontsize=9, color='grey', va='top')

    ax.set_xlabel(xlabel or time_col)
    ax.set_ylabel(ylabel or outcome_col)
    ax.legend(frameon=False)

    fig.tight_layout()
    if filename:
        save_fig(fig, filename)
    return fig, ax
```

**Figure note template:** "This figure plots the mean [outcome] for treated and control [units] from [start] to [end]. Treated [units] are those that [treatment definition]. The vertical dashed line marks [event]. The pre-treatment trends are [parallel / approximately parallel / divergent], [supporting / raising concerns about] the parallel trends assumption."

---

### 3. Binned scatter plot

The cleanest way to show a nonparametric relationship, optionally residualized.

```python
def plot_binned_scatter(df, x, y, n_bins=20, controls=None,
                        absorb_fe=None, xlabel=None, ylabel=None,
                        fit='linear', ci=True, filename=None):
    """
    Binned scatter plot with optional residualization and fit line.

    Parameters
    ----------
    controls : list of str, control variables to partial out
    absorb_fe : str, column for fixed effects to absorb (demeaning)
    fit : 'linear', 'quadratic', or 'lowess'
    ci : bool, show confidence band around fit
    """
    import statsmodels.api as sm

    plot_df = df[[x, y] + (controls or [])].dropna().copy()

    # Residualize
    if controls:
        X_ctrl = sm.add_constant(plot_df[controls])
        for var in [x, y]:
            plot_df[var] = sm.OLS(plot_df[var], X_ctrl).fit().resid

    if absorb_fe:
        for var in [x, y]:
            group_means = df.groupby(absorb_fe)[var].transform('mean')
            plot_df[var] = plot_df[var] - group_means.loc[plot_df.index]

    # Bin
    plot_df['bin'] = pd.qcut(plot_df[x], n_bins, labels=False, duplicates='drop')
    binned = plot_df.groupby('bin').agg(
        x_mean=(x, 'mean'), y_mean=(y, 'mean'),
        y_se=(y, 'sem'), n=(y, 'count')
    ).reset_index()

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.scatter(binned['x_mean'], binned['y_mean'], color=COLORS['primary'],
               s=40, zorder=3, edgecolors='white', linewidth=0.5)

    # Fit line
    if fit == 'linear':
        z = np.polyfit(binned['x_mean'], binned['y_mean'], 1)
        p = np.poly1d(z)
        x_line = np.linspace(binned['x_mean'].min(), binned['x_mean'].max(), 100)
        ax.plot(x_line, p(x_line), color=COLORS['secondary'], linewidth=1.5, linestyle='--')
    elif fit == 'quadratic':
        z = np.polyfit(binned['x_mean'], binned['y_mean'], 2)
        p = np.poly1d(z)
        x_line = np.linspace(binned['x_mean'].min(), binned['x_mean'].max(), 100)
        ax.plot(x_line, p(x_line), color=COLORS['secondary'], linewidth=1.5, linestyle='--')

    if ci:
        ax.errorbar(binned['x_mean'], binned['y_mean'], yerr=1.96 * binned['y_se'],
                     fmt='none', ecolor=COLORS['light_gray'], elinewidth=0.8, capsize=2, zorder=2)

    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)

    fig.tight_layout()
    if filename:
        save_fig(fig, filename)
    return fig, ax
```

**Figure note template:** "This figure plots binned means of [Y] against [X], with [N] equal-sized bins. [If residualized:] Both variables are residualized on [controls/FE]. The dashed line shows the [linear/quadratic] fit through the bin means. [If CI:] Error bars show 95% confidence intervals for the bin means."

---

### 4. Coefficient plot (horizontal)

Better than a table for showing heterogeneity, subgroup effects, or comparing specs.

```python
def plot_coefficients(labels, coefs, ci_lower, ci_upper,
                      group_labels=None, group_breaks=None,
                      xlabel='Coefficient estimate', title=None,
                      filename=None):
    """
    Horizontal coefficient plot with confidence intervals.

    Parameters
    ----------
    labels : list of str, variable or subgroup names
    coefs, ci_lower, ci_upper : array-like
    group_labels : list of str, section headers (e.g., ['Panel A: ...', 'Panel B: ...'])
    group_breaks : list of int, indices where groups start
    """
    n = len(labels)
    fig, ax = plt.subplots(figsize=(6.5, max(0.4 * n + 1.5, 3)))

    y_pos = np.arange(n)
    ax.axvline(x=0, color='grey', linewidth=0.8, linestyle='--')

    xerr = [np.array(coefs) - np.array(ci_lower), np.array(ci_upper) - np.array(coefs)]
    ax.errorbar(coefs, y_pos, xerr=xerr, fmt='o', color=COLORS['primary'],
                markersize=6, capsize=3, linewidth=1.5, zorder=3)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel(xlabel)

    # Group separators
    if group_breaks and group_labels:
        for i, (brk, lbl) in enumerate(zip(group_breaks, group_labels)):
            if brk > 0:
                ax.axhline(y=brk - 0.5, color=COLORS['light_gray'], linewidth=0.5)

    if title:
        ax.set_title(title)

    fig.tight_layout()
    if filename:
        save_fig(fig, filename)
    return fig, ax
```

---

### 5. Regression discontinuity plot

Shows raw data around a cutoff with local polynomial fits on each side.

```python
def plot_rd(df, running_var, outcome, cutoff=0, bandwidth=None,
            n_bins=40, polynomial=1, xlabel=None, ylabel=None, filename=None):
    """
    Regression discontinuity plot with binned scatter and local fits.

    Parameters
    ----------
    running_var : str, running variable column
    outcome : str, outcome column
    cutoff : float, RD cutoff value
    bandwidth : float, restrict plot to [cutoff - bw, cutoff + bw]
    polynomial : int, degree of local polynomial fit on each side
    """
    import statsmodels.api as sm

    plot_df = df[[running_var, outcome]].dropna().copy()
    plot_df['centered'] = plot_df[running_var] - cutoff

    if bandwidth:
        plot_df = plot_df[plot_df['centered'].abs() <= bandwidth]

    # Bin the data
    plot_df['bin'] = pd.cut(plot_df['centered'], bins=n_bins)
    binned = plot_df.groupby('bin', observed=True).agg(
        x_mean=('centered', 'mean'), y_mean=(outcome, 'mean')
    ).dropna().reset_index()

    fig, ax = plt.subplots(figsize=(7, 4.5))

    # Points
    left = binned[binned['x_mean'] < 0]
    right = binned[binned['x_mean'] >= 0]
    ax.scatter(left['x_mean'], left['y_mean'], color=COLORS['primary'], s=30, zorder=3)
    ax.scatter(right['x_mean'], right['y_mean'], color=COLORS['secondary'], s=30, zorder=3)

    # Local polynomial fits
    for subset, color in [(plot_df[plot_df['centered'] < 0], COLORS['primary']),
                          (plot_df[plot_df['centered'] >= 0], COLORS['secondary'])]:
        if len(subset) < 10:
            continue
        x_fit = np.linspace(subset['centered'].min(), subset['centered'].max(), 200)
        X = np.column_stack([subset['centered'] ** p for p in range(1, polynomial + 1)])
        X = sm.add_constant(X)
        model = sm.OLS(subset[outcome], X).fit()
        X_pred = np.column_stack([x_fit ** p for p in range(1, polynomial + 1)])
        X_pred = sm.add_constant(X_pred)
        y_pred = model.predict(X_pred)
        ax.plot(x_fit, y_pred, color=color, linewidth=2)

    # Cutoff line
    ax.axvline(x=0, color='grey', linewidth=0.8, linestyle=':', alpha=0.6)

    ax.set_xlabel(xlabel or f'{running_var} (centered at cutoff)')
    ax.set_ylabel(ylabel or outcome)

    fig.tight_layout()
    if filename:
        save_fig(fig, filename)
    return fig, ax
```

**Figure note template:** "This figure plots binned means of [outcome] against [running variable], centered at the [cutoff description]. Each dot represents the mean of [N] bins. The solid lines show local [linear/polynomial] fits estimated separately on each side of the cutoff. The sample is restricted to a bandwidth of [bw] around the threshold."

---

### 6. Time-series trend plot

For motivation figures or showing macro context.

```python
def plot_time_series(df, date_col, value_cols, labels=None,
                     ylabel=None, xlabel=None, recession_bars=True,
                     highlight_period=None, filename=None):
    """
    Time-series plot with optional recession shading and event highlighting.

    Parameters
    ----------
    value_cols : str or list of str
    recession_bars : bool, shade NBER recessions
    highlight_period : tuple of (start_date, end_date) to shade
    """
    if isinstance(value_cols, str):
        value_cols = [value_cols]
    if labels is None:
        labels = value_cols

    fig, ax = plt.subplots(figsize=(7, 4))

    for i, (col, label) in enumerate(zip(value_cols, labels)):
        ax.plot(df[date_col], df[col], color=COLOR_LIST[i], label=label, linewidth=1.5)

    if highlight_period:
        ax.axvspan(highlight_period[0], highlight_period[1],
                   alpha=0.08, color=COLORS['secondary'], zorder=0)

    if recession_bars:
        # NBER recession dates (add more as needed)
        recessions = [
            ('2001-03-01', '2001-11-01'),
            ('2007-12-01', '2009-06-01'),
            ('2020-02-01', '2020-04-01'),
        ]
        for start, end in recessions:
            ax.axvspan(pd.Timestamp(start), pd.Timestamp(end),
                       alpha=0.06, color='grey', zorder=0)

    ax.set_xlabel(xlabel or '')
    ax.set_ylabel(ylabel or '')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    if len(value_cols) > 1:
        ax.legend(frameon=False)

    fig.tight_layout()
    if filename:
        save_fig(fig, filename)
    return fig, ax
```

---

### 7. Distribution plots

For summary statistics visualization and variable inspection.

```python
def plot_distributions(df, variables, labels=None, ncols=2,
                       kind='hist_kde', filename=None):
    """
    Panel of distribution plots for multiple variables.

    kind : 'hist_kde', 'hist', 'kde', 'box'
    """
    if labels is None:
        labels = {v: v for v in variables}
    n = len(variables)
    nrows = int(np.ceil(n / ncols))

    fig, axes = plt.subplots(nrows, ncols, figsize=(6.5, 2.5 * nrows))
    axes = np.atleast_2d(axes).flatten()

    for i, var in enumerate(variables):
        ax = axes[i]
        data = df[var].dropna()

        if kind == 'hist_kde':
            ax.hist(data, bins=50, density=True, color=COLORS['primary'],
                    alpha=0.5, edgecolor='white', linewidth=0.5)
            data.plot.kde(ax=ax, color=COLORS['secondary'], linewidth=1.5)
        elif kind == 'hist':
            ax.hist(data, bins=50, color=COLORS['primary'],
                    alpha=0.7, edgecolor='white', linewidth=0.5)
        elif kind == 'kde':
            data.plot.kde(ax=ax, color=COLORS['primary'], linewidth=1.5)
        elif kind == 'box':
            ax.boxplot(data, vert=True, widths=0.5,
                       boxprops=dict(color=COLORS['primary']),
                       medianprops=dict(color=COLORS['secondary']))

        ax.set_xlabel(labels.get(var, var))
        ax.set_ylabel('')

    # Hide unused subplots
    for j in range(n, len(axes)):
        axes[j].set_visible(False)

    fig.tight_layout()
    if filename:
        save_fig(fig, filename)
    return fig, axes
```

---

### 8. Choropleth map

For real-estate and spatial papers. Shows geographic variation.

```python
def plot_choropleth(gdf, value_col, title=None, cmap='RdYlBu_r',
                    legend_label=None, edgecolor='white', linewidth=0.3,
                    boundary_gdf=None, filename=None):
    """
    Choropleth map from a GeoDataFrame.

    Parameters
    ----------
    gdf : GeoDataFrame with geometry and value_col
    boundary_gdf : optional GeoDataFrame to overlay (e.g., treatment boundaries)
    """
    import geopandas as gpd

    fig, ax = plt.subplots(figsize=(8, 6))

    gdf.plot(column=value_col, ax=ax, cmap=cmap, legend=True,
             edgecolor=edgecolor, linewidth=linewidth,
             legend_kwds={'label': legend_label or value_col, 'shrink': 0.6})

    if boundary_gdf is not None:
        boundary_gdf.boundary.plot(ax=ax, color=COLORS['secondary'],
                                   linewidth=1.5, linestyle='--')

    ax.set_axis_off()
    if title:
        ax.set_title(title, fontsize=13)

    fig.tight_layout()
    if filename:
        save_fig(fig, filename)
    return fig, ax
```

**Figure note template:** "This figure maps [variable] at the [geographic level] level for [region], [time period]. Darker shading indicates [higher/lower values]. [If boundary:] The dashed line indicates the [boundary description]. Data source: [source]."

---

### 9. Portfolio return plots (asset pricing)

```python
def plot_cumulative_returns(df, date_col, return_cols, labels=None,
                            log_scale=False, ylabel='Cumulative return ($1 invested)',
                            filename=None):
    """
    Cumulative return plot for portfolio strategies.

    return_cols : list of str, columns with periodic returns (not cumulative)
    """
    fig, ax = plt.subplots(figsize=(7, 4.5))

    if labels is None:
        labels = return_cols

    for i, (col, label) in enumerate(zip(return_cols, labels)):
        cumret = (1 + df[col]).cumprod()
        ax.plot(df[date_col], cumret, color=COLOR_LIST[i], label=label, linewidth=1.5)

    ax.axhline(y=1, color='grey', linewidth=0.5, linestyle='--')
    ax.set_ylabel(ylabel)
    ax.legend(frameon=False)

    if log_scale:
        ax.set_yscale('log')

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    fig.tight_layout()
    if filename:
        save_fig(fig, filename)
    return fig, ax


def plot_portfolio_bars(portfolio_returns, labels=None, ylabel='Mean monthly return (%)',
                        show_hml=True, filename=None):
    """
    Bar chart of mean returns across sorted portfolios.

    portfolio_returns : DataFrame with columns Q1, Q2, ..., Qn, [HML]
    """
    means = portfolio_returns.mean() * 100
    cols = [c for c in means.index if c.startswith('Q')]
    if show_hml and 'HML' in means.index:
        cols.append('HML')

    fig, ax = plt.subplots(figsize=(6.5, 4))

    colors = [COLORS['primary']] * (len(cols) - (1 if show_hml else 0))
    if show_hml and 'HML' in cols:
        colors.append(COLORS['secondary'])

    bars = ax.bar(range(len(cols)), [means[c] for c in cols], color=colors,
                  edgecolor='white', linewidth=0.5, width=0.7)

    ax.set_xticks(range(len(cols)))
    if labels:
        ax.set_xticklabels(labels)
    else:
        xlabels = [c.replace('Q', 'Q') for c in cols]
        if show_hml and 'HML' in cols:
            xlabels[-1] = 'H-L'
        ax.set_xticklabels(xlabels)

    ax.set_ylabel(ylabel)
    ax.axhline(y=0, color='grey', linewidth=0.5)

    fig.tight_layout()
    if filename:
        save_fig(fig, filename)
    return fig, ax
```

---

### 10. Kaplan-Meier survival curves

For mortgage default, fund exit, CEO turnover studies.

```python
def plot_kaplan_meier(df, duration_col, event_col, group_col=None,
                      group_labels=None, xlabel='Time', ylabel='Survival probability',
                      filename=None):
    """
    Kaplan-Meier survival curves, optionally by group.
    """
    from lifelines import KaplanMeierFitter

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    kmf = KaplanMeierFitter()

    if group_col is None:
        kmf.fit(df[duration_col], event_observed=df[event_col])
        kmf.plot_survival_function(ax=ax, color=COLORS['primary'], ci_show=True)
    else:
        groups = sorted(df[group_col].unique())
        if group_labels is None:
            group_labels = {g: str(g) for g in groups}
        for i, group in enumerate(groups):
            mask = df[group_col] == group
            kmf.fit(df.loc[mask, duration_col], event_observed=df.loc[mask, event_col],
                    label=group_labels.get(group, str(group)))
            kmf.plot_survival_function(ax=ax, color=COLOR_LIST[i], ci_show=True, ci_alpha=0.1)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(frameon=False)

    fig.tight_layout()
    if filename:
        save_fig(fig, filename)
    return fig, ax
```

---

### 11. Heatmap (correlation, factor exposure)

```python
def plot_heatmap(data, labels=None, title=None, annot=True, fmt='.2f',
                 cmap='RdBu_r', center=0, filename=None):
    """
    Heatmap for correlation matrices, factor loadings, or comparison grids.
    """
    fig, ax = plt.subplots(figsize=(max(6, len(data.columns) * 0.8),
                                     max(4, len(data) * 0.6)))

    sns.heatmap(data, annot=annot, fmt=fmt, cmap=cmap, center=center,
                ax=ax, linewidths=0.5, linecolor='white',
                cbar_kws={'shrink': 0.7},
                xticklabels=labels or data.columns,
                yticklabels=labels or data.index)

    if title:
        ax.set_title(title)

    fig.tight_layout()
    if filename:
        save_fig(fig, filename)
    return fig, ax
```

---

### 12. Sample flow diagram

Not a data plot but critical for transparency. Uses matplotlib text and arrows.

```python
def plot_sample_flow(stages, filename=None):
    """
    Sample construction flow diagram.

    Parameters
    ----------
    stages : list of dicts with keys 'label', 'n', and optionally 'filter'
        Example: [
            {'label': 'CRSP-Compustat merged', 'n': 245000},
            {'label': 'Drop financials (SIC 6000-6999)', 'n': 198000, 'filter': True},
            {'label': 'Drop missing controls', 'n': 178500, 'filter': True},
            {'label': 'Final sample', 'n': 172300},
        ]
    """
    fig, ax = plt.subplots(figsize=(5, len(stages) * 1.2 + 0.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, len(stages) * 1.2 + 0.5)
    ax.axis('off')

    for i, stage in enumerate(stages):
        y = len(stages) * 1.2 - i * 1.2
        is_filter = stage.get('filter', False)

        # Box
        color = COLORS['light_gray'] if is_filter else COLORS['primary']
        text_color = 'black' if is_filter else 'white'
        rect = plt.Rectangle((1, y - 0.4), 8, 0.8, facecolor=color,
                              edgecolor='grey', linewidth=0.5, alpha=0.9)
        ax.add_patch(rect)

        # Text
        ax.text(5, y, f"{stage['label']}\nN = {stage['n']:,}",
                ha='center', va='center', fontsize=9, color=text_color, weight='bold')

        # Arrow to next
        if i < len(stages) - 1:
            ax.annotate('', xy=(5, y - 0.5), xytext=(5, y - 0.8),
                        arrowprops=dict(arrowstyle='->', color='grey', lw=1.2))

    fig.tight_layout()
    if filename:
        save_fig(fig, filename)
    return fig, ax
```

---

### 13. Mechanism / conceptual diagram

For illustrating economic channels or research design logic.

```python
def plot_mechanism_diagram(nodes, edges, filename=None):
    """
    Simple mechanism/conceptual diagram.

    Parameters
    ----------
    nodes : list of dicts with 'label', 'x', 'y', and optionally 'box_color'
    edges : list of dicts with 'from_idx', 'to_idx', and optionally 'label', 'style'
    """
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 5.5)
    ax.axis('off')

    # Draw nodes
    box_patches = []
    for node in nodes:
        color = node.get('box_color', COLORS['primary'])
        rect = plt.Rectangle((node['x'] - 1.2, node['y'] - 0.4), 2.4, 0.8,
                              facecolor=color, edgecolor='grey', linewidth=0.8, alpha=0.9)
        ax.add_patch(rect)
        box_patches.append(rect)
        text_color = 'white' if color == COLORS['primary'] else 'black'
        ax.text(node['x'], node['y'], node['label'], ha='center', va='center',
                fontsize=9, color=text_color, weight='bold', wrap=True)

    # Draw edges
    for edge in edges:
        n_from = nodes[edge['from_idx']]
        n_to = nodes[edge['to_idx']]
        style = edge.get('style', '->')
        ax.annotate('', xy=(n_to['x'] - 1.2, n_to['y']),
                    xytext=(n_from['x'] + 1.2, n_from['y']),
                    arrowprops=dict(arrowstyle=style, color='grey', lw=1.5))
        if 'label' in edge:
            mid_x = (n_from['x'] + n_to['x']) / 2
            mid_y = (n_from['y'] + n_to['y']) / 2
            ax.text(mid_x, mid_y + 0.3, edge['label'], ha='center',
                    fontsize=8, color='grey', style='italic')

    fig.tight_layout()
    if filename:
        save_fig(fig, filename)
    return fig, ax
```

---

## Figure notes standard

Every figure in the paper must have a self-contained note. The note should include:

1. What is plotted (outcome variable, conditioning, residualization)
2. Sample used (time period, filters, N)
3. Estimation details (equation reference, controls, FE)
4. Statistical details (CI level, SE clustering, bandwidth)
5. Data source

Use the note templates provided with each figure type above.

## Design rules

- **One message per figure.** If you need two messages, make two figures.
- **No chartjunk.** Remove gridlines, unnecessary borders, redundant labels. Less ink, more data.
- **Consistent style across all figures.** Same fonts, colors, line widths throughout the paper.
- **Colorblind-safe.** The default palette works. If adding colors, test with a simulator.
- **Text must be readable at print size.** Minimum 9pt after scaling to journal column width.
- **Axis labels with units.** Never leave an axis unlabeled.
- **Save as PDF for LaTeX.** PNG at 300 DPI as backup. Never use JPG for plots.
- **Figure size: 6.5 x 4.5 inches** fits a single journal column. Use 7 x 4.5 for wider figures.

## Tool integration (Corbis MCP)

- `fred_series_batch` → pull FRED data for time-series motivation figures.
- `get_market_data` / `compare_markets` → pull CRE market data for RE motivation or context figures.
- `search_papers` (query: "figure [type] [topic]", `minYear: 2020`) → find examples of how recent published papers visualize similar results.
- `export_citations` (format: `bibtex`) → export BibTeX entries for papers whose figures served as design references or visual benchmarks. Offer this after the figure plan is produced.
- `format_citation` → format individual references for figure notes that cite published visual precedents.

## Guardrails

- Do not generate a figure that simply restates a table. The figure must reveal something the table cannot.
- Do not use 3D charts, pie charts, or stacked bar charts in academic finance papers.
- Do not use rainbow color schemes or more than 4-5 colors in a single figure.
- Do not forget confidence intervals on coefficient, event-study, or RD plots.
- Do not use raw (non-residualized) binned scatters when the paper includes controls in the regression.
- Do not leave axis labels as raw variable names from the DataFrame.
- For maps, always include a scale indicator or recognizable geographic context.

## LaTeX float format — write to `.tex` files

**Before generating any figure float, read `latex_template/academic_paper_template.tex`** to see the template's custom commands (`\floatnotes`, `\sym`) and working examples of figure floats.

**Write each figure's LaTeX float wrapper to a `.tex` file** in `output/figures/` (e.g., `output/figures/fig_event_study.tex`). Do not put float LaTeX in the chat for the user to copy-paste. These files can then be `\input{}` into the main paper `.tex` file.

Every figure must include a LaTeX float wrapper that follows the template. The structure is: **caption on top, descriptive note between caption and figure, figure below**.

```latex
\begin{figure}[!htbp]
\caption{Descriptive Title of the Figure}
\label{fig:name}\vspace{-2.5ex}
\floatnotes{This figure plots [what]. The sample includes [scope/period]. [For
event studies: The omitted period is t = -1. Confidence intervals are 95\%
based on clustered SEs.] [For binned scatters: Both axes are residualized on
firm and year fixed effects. Each bin contains an equal number of observations.
The solid line shows a linear fit.] [For maps: Data source is X. Shading
represents Y.]}
\centering
\includegraphics[width=\textwidth]{./output/figures/name.pdf}
\end{figure}
```

The `\floatnotes` command (defined in the template) renders as a scriptsize quotation block. The note should be self-contained: a reader who sees only the figure and its note should understand the figure without reading the paper body.

## Output format

Write all figure Python code to `analysis/` scripts and all LaTeX float wrappers to `output/figures/*.tex` files. In the chat, provide only:
```
# Figure plan
## Figures for the main paper (with placement rationale)
## Figures for the appendix
## Figures for presentations only
## For each figure:
  - Figure number and title
  - What message it conveys
  - Figure type (from catalog)
  - Data requirements
  - File paths: Python script, output image, LaTeX float wrapper
```

## Example prompts
- "Plan the figures for this corporate-finance DiD paper."
- "Create an event-study plot from these regression coefficients."
- "Make a choropleth map of treatment intensity across counties."
- "Build a sample flow diagram for my CRSP-Compustat merge."
- "Convert Table 3 into a coefficient plot for my seminar talk."
- "What figures should a housing-price boundary RD paper include?"
- "Create a motivation figure showing mortgage rate trends with recession shading."
- "Generate a Kaplan-Meier plot for mortgage default by LTV bucket."
