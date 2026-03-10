# Figure Code Catalog

Complete Python code for every common figure type in finance and real-estate papers.

## Global defaults (use in every script)

```python
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np
import pandas as pd
from pathlib import Path

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'Computer Modern Roman'],
    'font.size': 11, 'axes.labelsize': 12, 'axes.titlesize': 13,
    'xtick.labelsize': 10, 'ytick.labelsize': 10, 'legend.fontsize': 10,
    'figure.figsize': (6.5, 4.5), 'figure.dpi': 300,
    'savefig.dpi': 300, 'savefig.bbox': 'tight', 'savefig.pad_inches': 0.1,
    'axes.grid': False, 'axes.spines.top': False, 'axes.spines.right': False,
    'axes.linewidth': 0.8, 'lines.linewidth': 1.5, 'patch.linewidth': 0.8,
})

COLORS = {
    'primary': '#2c3e50', 'secondary': '#e74c3c', 'tertiary': '#3498db',
    'quaternary': '#2ecc71', 'accent1': '#f39c12', 'accent2': '#9b59b6',
    'light_gray': '#bdc3c7', 'ci_fill': '#2c3e50',
}
COLOR_LIST = ['#2c3e50', '#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']

OUTPUT = Path('output/figures')
OUTPUT.mkdir(parents=True, exist_ok=True)

def save_fig(fig, name, formats=('pdf', 'png')):
    for fmt in formats:
        fig.savefig(OUTPUT / f'{name}.{fmt}')
    print(f"Saved: {name}")
    plt.close(fig)
```

---

## 1. Event-study plot

```python
def plot_event_study(coefs, ci_lower, ci_upper, event_times,
                     ref_period=-1, ylabel='Coefficient estimate',
                     xlabel='Event time', title=None, filename=None,
                     shade_post=True, annotate_coef=None):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    all_times = sorted(set(list(event_times) + [ref_period]))
    y_vals, lo_vals, hi_vals = [], [], []
    j = 0
    for t in all_times:
        if t == ref_period:
            y_vals.append(0); lo_vals.append(0); hi_vals.append(0)
        else:
            y_vals.append(coefs[j]); lo_vals.append(ci_lower[j]); hi_vals.append(ci_upper[j])
            j += 1
    ax.axhline(y=0, color='grey', linewidth=0.8, linestyle='--', zorder=1)
    ax.axvline(x=-0.5, color='grey', linewidth=0.8, linestyle=':', alpha=0.5, zorder=1)
    if shade_post:
        ax.axvspan(-0.5, max(all_times) + 0.5, alpha=0.04, color=COLORS['primary'], zorder=0)
    ax.plot(all_times, y_vals, 'o-', color=COLORS['primary'], markersize=5, zorder=3)
    ax.fill_between(all_times, lo_vals, hi_vals, alpha=0.15, color=COLORS['ci_fill'], zorder=2)
    if annotate_coef is not None and annotate_coef in all_times:
        idx = all_times.index(annotate_coef)
        ax.annotate(f'{y_vals[idx]:.3f}', xy=(annotate_coef, y_vals[idx]),
                    xytext=(10, 10), textcoords='offset points', fontsize=9,
                    arrowprops=dict(arrowstyle='->', color='grey', lw=0.8))
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
    ax.set_xticks(all_times)
    if title: ax.set_title(title)
    fig.tight_layout()
    if filename: save_fig(fig, filename)
    return fig, ax
```

**Note template:** "This figure plots the estimated coefficients $\beta_k$ from Equation (X), which regresses [outcome] on event-time indicators relative to [event], controlling for [FE and controls]. The omitted category is $k = [ref]$. The shaded region indicates the 95% confidence interval based on standard errors clustered at the [level] level."

---

## 2. Parallel trends plot

```python
def plot_parallel_trends(df, time_col, outcome_col, group_col,
                         treatment_time=None, ylabel=None, xlabel=None,
                         group_labels=None, filename=None):
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
    ax.set_xlabel(xlabel or time_col); ax.set_ylabel(ylabel or outcome_col)
    ax.legend(frameon=False)
    fig.tight_layout()
    if filename: save_fig(fig, filename)
    return fig, ax
```

**Note template:** "This figure plots the mean [outcome] for treated and control [units] from [start] to [end]. Treated [units] are those that [treatment definition]. The vertical dashed line marks [event]."

---

## 3. Binned scatter plot

```python
def plot_binned_scatter(df, x, y, n_bins=20, controls=None,
                        absorb_fe=None, xlabel=None, ylabel=None,
                        fit='linear', ci=True, filename=None):
    import statsmodels.api as sm
    plot_df = df[[x, y] + (controls or [])].dropna().copy()
    if controls:
        X_ctrl = sm.add_constant(plot_df[controls])
        for var in [x, y]:
            plot_df[var] = sm.OLS(plot_df[var], X_ctrl).fit().resid
    if absorb_fe:
        for var in [x, y]:
            group_means = df.groupby(absorb_fe)[var].transform('mean')
            plot_df[var] = plot_df[var] - group_means.loc[plot_df.index]
    plot_df['bin'] = pd.qcut(plot_df[x], n_bins, labels=False, duplicates='drop')
    binned = plot_df.groupby('bin').agg(
        x_mean=(x, 'mean'), y_mean=(y, 'mean'),
        y_se=(y, 'sem'), n=(y, 'count')
    ).reset_index()
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.scatter(binned['x_mean'], binned['y_mean'], color=COLORS['primary'],
               s=40, zorder=3, edgecolors='white', linewidth=0.5)
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
    ax.set_xlabel(xlabel or x); ax.set_ylabel(ylabel or y)
    fig.tight_layout()
    if filename: save_fig(fig, filename)
    return fig, ax
```

**Note template:** "This figure plots binned means of [Y] against [X], with [N] equal-sized bins. [If residualized:] Both variables are residualized on [controls/FE]. The dashed line shows the [linear/quadratic] fit."

---

## 4. Coefficient plot (horizontal)

```python
def plot_coefficients(labels, coefs, ci_lower, ci_upper,
                      group_labels=None, group_breaks=None,
                      xlabel='Coefficient estimate', title=None, filename=None):
    n = len(labels)
    fig, ax = plt.subplots(figsize=(6.5, max(0.4 * n + 1.5, 3)))
    y_pos = np.arange(n)
    ax.axvline(x=0, color='grey', linewidth=0.8, linestyle='--')
    xerr = [np.array(coefs) - np.array(ci_lower), np.array(ci_upper) - np.array(coefs)]
    ax.errorbar(coefs, y_pos, xerr=xerr, fmt='o', color=COLORS['primary'],
                markersize=6, capsize=3, linewidth=1.5, zorder=3)
    ax.set_yticks(y_pos); ax.set_yticklabels(labels)
    ax.invert_yaxis(); ax.set_xlabel(xlabel)
    if group_breaks and group_labels:
        for brk in group_breaks:
            if brk > 0:
                ax.axhline(y=brk - 0.5, color=COLORS['light_gray'], linewidth=0.5)
    if title: ax.set_title(title)
    fig.tight_layout()
    if filename: save_fig(fig, filename)
    return fig, ax
```

---

## 5. Regression discontinuity plot

```python
def plot_rd(df, running_var, outcome, cutoff=0, bandwidth=None,
            n_bins=40, polynomial=1, xlabel=None, ylabel=None, filename=None):
    import statsmodels.api as sm
    plot_df = df[[running_var, outcome]].dropna().copy()
    plot_df['centered'] = plot_df[running_var] - cutoff
    if bandwidth:
        plot_df = plot_df[plot_df['centered'].abs() <= bandwidth]
    plot_df['bin'] = pd.cut(plot_df['centered'], bins=n_bins)
    binned = plot_df.groupby('bin', observed=True).agg(
        x_mean=('centered', 'mean'), y_mean=(outcome, 'mean')
    ).dropna().reset_index()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    left = binned[binned['x_mean'] < 0]
    right = binned[binned['x_mean'] >= 0]
    ax.scatter(left['x_mean'], left['y_mean'], color=COLORS['primary'], s=30, zorder=3)
    ax.scatter(right['x_mean'], right['y_mean'], color=COLORS['secondary'], s=30, zorder=3)
    for subset, color in [(plot_df[plot_df['centered'] < 0], COLORS['primary']),
                          (plot_df[plot_df['centered'] >= 0], COLORS['secondary'])]:
        if len(subset) < 10: continue
        x_fit = np.linspace(subset['centered'].min(), subset['centered'].max(), 200)
        X = np.column_stack([subset['centered'] ** p for p in range(1, polynomial + 1)])
        X = sm.add_constant(X)
        model = sm.OLS(subset[outcome], X).fit()
        X_pred = np.column_stack([x_fit ** p for p in range(1, polynomial + 1)])
        X_pred = sm.add_constant(X_pred)
        ax.plot(x_fit, model.predict(X_pred), color=color, linewidth=2)
    ax.axvline(x=0, color='grey', linewidth=0.8, linestyle=':', alpha=0.6)
    ax.set_xlabel(xlabel or f'{running_var} (centered at cutoff)')
    ax.set_ylabel(ylabel or outcome)
    fig.tight_layout()
    if filename: save_fig(fig, filename)
    return fig, ax
```

**Note template:** "This figure plots binned means of [outcome] against [running variable], centered at the [cutoff]. Each dot represents the mean of [N] bins. Solid lines show local [linear/polynomial] fits on each side of the cutoff."

---

## 6. Time-series trend plot

```python
def plot_time_series(df, date_col, value_cols, labels=None,
                     ylabel=None, xlabel=None, recession_bars=True,
                     highlight_period=None, filename=None):
    if isinstance(value_cols, str): value_cols = [value_cols]
    if labels is None: labels = value_cols
    fig, ax = plt.subplots(figsize=(7, 4))
    for i, (col, label) in enumerate(zip(value_cols, labels)):
        ax.plot(df[date_col], df[col], color=COLOR_LIST[i], label=label, linewidth=1.5)
    if highlight_period:
        ax.axvspan(highlight_period[0], highlight_period[1],
                   alpha=0.08, color=COLORS['secondary'], zorder=0)
    if recession_bars:
        recessions = [('2001-03-01', '2001-11-01'), ('2007-12-01', '2009-06-01'),
                      ('2020-02-01', '2020-04-01')]
        for start, end in recessions:
            ax.axvspan(pd.Timestamp(start), pd.Timestamp(end), alpha=0.06, color='grey', zorder=0)
    ax.set_xlabel(xlabel or ''); ax.set_ylabel(ylabel or '')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    if len(value_cols) > 1: ax.legend(frameon=False)
    fig.tight_layout()
    if filename: save_fig(fig, filename)
    return fig, ax
```

---

## 7. Distribution plots

```python
def plot_distributions(df, variables, labels=None, ncols=2,
                       kind='hist_kde', filename=None):
    if labels is None: labels = {v: v for v in variables}
    n = len(variables)
    nrows = int(np.ceil(n / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(6.5, 2.5 * nrows))
    axes = np.atleast_2d(axes).flatten()
    for i, var in enumerate(variables):
        ax = axes[i]
        data = df[var].dropna()
        if kind == 'hist_kde':
            ax.hist(data, bins=50, density=True, color=COLORS['primary'], alpha=0.5, edgecolor='white')
            data.plot.kde(ax=ax, color=COLORS['secondary'], linewidth=1.5)
        elif kind == 'hist':
            ax.hist(data, bins=50, color=COLORS['primary'], alpha=0.7, edgecolor='white')
        elif kind == 'kde':
            data.plot.kde(ax=ax, color=COLORS['primary'], linewidth=1.5)
        ax.set_xlabel(labels.get(var, var)); ax.set_ylabel('')
    for j in range(n, len(axes)):
        axes[j].set_visible(False)
    fig.tight_layout()
    if filename: save_fig(fig, filename)
    return fig, axes
```

---

## 8. Choropleth map

```python
def plot_choropleth(gdf, value_col, title=None, cmap='RdYlBu_r',
                    legend_label=None, edgecolor='white', linewidth=0.3,
                    boundary_gdf=None, filename=None):
    fig, ax = plt.subplots(figsize=(8, 6))
    gdf.plot(column=value_col, ax=ax, cmap=cmap, legend=True,
             edgecolor=edgecolor, linewidth=linewidth,
             legend_kwds={'label': legend_label or value_col, 'shrink': 0.6})
    if boundary_gdf is not None:
        boundary_gdf.boundary.plot(ax=ax, color=COLORS['secondary'], linewidth=1.5, linestyle='--')
    ax.set_axis_off()
    if title: ax.set_title(title, fontsize=13)
    fig.tight_layout()
    if filename: save_fig(fig, filename)
    return fig, ax
```

**Note template:** "This figure maps [variable] at the [geographic level] level for [region], [time period]. Darker shading indicates [higher/lower values]."

---

## 9. Portfolio return plots

```python
def plot_cumulative_returns(df, date_col, return_cols, labels=None,
                            log_scale=False, ylabel='Cumulative return ($1 invested)',
                            filename=None):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    if labels is None: labels = return_cols
    for i, (col, label) in enumerate(zip(return_cols, labels)):
        cumret = (1 + df[col]).cumprod()
        ax.plot(df[date_col], cumret, color=COLOR_LIST[i], label=label, linewidth=1.5)
    ax.axhline(y=1, color='grey', linewidth=0.5, linestyle='--')
    ax.set_ylabel(ylabel); ax.legend(frameon=False)
    if log_scale: ax.set_yscale('log')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    fig.tight_layout()
    if filename: save_fig(fig, filename)
    return fig, ax

def plot_portfolio_bars(portfolio_returns, labels=None, ylabel='Mean monthly return (%)',
                        show_hml=True, filename=None):
    means = portfolio_returns.mean() * 100
    cols = [c for c in means.index if c.startswith('Q')]
    if show_hml and 'HML' in means.index: cols.append('HML')
    fig, ax = plt.subplots(figsize=(6.5, 4))
    colors = [COLORS['primary']] * (len(cols) - (1 if show_hml and 'HML' in cols else 0))
    if show_hml and 'HML' in cols: colors.append(COLORS['secondary'])
    ax.bar(range(len(cols)), [means[c] for c in cols], color=colors, edgecolor='white', width=0.7)
    xlabels = [c for c in cols]
    if show_hml and 'HML' in cols: xlabels[-1] = 'H-L'
    ax.set_xticks(range(len(cols))); ax.set_xticklabels(labels or xlabels)
    ax.set_ylabel(ylabel); ax.axhline(y=0, color='grey', linewidth=0.5)
    fig.tight_layout()
    if filename: save_fig(fig, filename)
    return fig, ax
```

---

## 10. Kaplan-Meier survival curves

```python
def plot_kaplan_meier(df, duration_col, event_col, group_col=None,
                      group_labels=None, xlabel='Time', ylabel='Survival probability',
                      filename=None):
    from lifelines import KaplanMeierFitter
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    kmf = KaplanMeierFitter()
    if group_col is None:
        kmf.fit(df[duration_col], event_observed=df[event_col])
        kmf.plot_survival_function(ax=ax, color=COLORS['primary'], ci_show=True)
    else:
        groups = sorted(df[group_col].unique())
        if group_labels is None: group_labels = {g: str(g) for g in groups}
        for i, group in enumerate(groups):
            mask = df[group_col] == group
            kmf.fit(df.loc[mask, duration_col], event_observed=df.loc[mask, event_col],
                    label=group_labels.get(group, str(group)))
            kmf.plot_survival_function(ax=ax, color=COLOR_LIST[i], ci_show=True, ci_alpha=0.1)
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel); ax.legend(frameon=False)
    fig.tight_layout()
    if filename: save_fig(fig, filename)
    return fig, ax
```

---

## 11. Heatmap

```python
def plot_heatmap(data, labels=None, title=None, annot=True, fmt='.2f',
                 cmap='RdBu_r', center=0, filename=None):
    fig, ax = plt.subplots(figsize=(max(6, len(data.columns) * 0.8),
                                     max(4, len(data) * 0.6)))
    sns.heatmap(data, annot=annot, fmt=fmt, cmap=cmap, center=center,
                ax=ax, linewidths=0.5, linecolor='white', cbar_kws={'shrink': 0.7},
                xticklabels=labels or data.columns, yticklabels=labels or data.index)
    if title: ax.set_title(title)
    fig.tight_layout()
    if filename: save_fig(fig, filename)
    return fig, ax
```

---

## 12. Sample flow diagram

```python
def plot_sample_flow(stages, filename=None):
    """stages: list of dicts with 'label', 'n', and optionally 'filter'."""
    fig, ax = plt.subplots(figsize=(5, len(stages) * 1.2 + 0.5))
    ax.set_xlim(0, 10); ax.set_ylim(0, len(stages) * 1.2 + 0.5); ax.axis('off')
    for i, stage in enumerate(stages):
        y = len(stages) * 1.2 - i * 1.2
        is_filter = stage.get('filter', False)
        color = COLORS['light_gray'] if is_filter else COLORS['primary']
        text_color = 'black' if is_filter else 'white'
        rect = plt.Rectangle((1, y - 0.4), 8, 0.8, facecolor=color,
                              edgecolor='grey', linewidth=0.5, alpha=0.9)
        ax.add_patch(rect)
        ax.text(5, y, f"{stage['label']}\nN = {stage['n']:,}",
                ha='center', va='center', fontsize=9, color=text_color, weight='bold')
        if i < len(stages) - 1:
            ax.annotate('', xy=(5, y - 0.5), xytext=(5, y - 0.8),
                        arrowprops=dict(arrowstyle='->', color='grey', lw=1.2))
    fig.tight_layout()
    if filename: save_fig(fig, filename)
    return fig, ax
```

---

## 13. Mechanism / conceptual diagram

```python
def plot_mechanism_diagram(nodes, edges, filename=None):
    """nodes: list of dicts with 'label', 'x', 'y', optionally 'box_color'.
    edges: list of dicts with 'from_idx', 'to_idx', optionally 'label', 'style'."""
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_xlim(-0.5, 10.5); ax.set_ylim(-0.5, 5.5); ax.axis('off')
    for node in nodes:
        color = node.get('box_color', COLORS['primary'])
        rect = plt.Rectangle((node['x'] - 1.2, node['y'] - 0.4), 2.4, 0.8,
                              facecolor=color, edgecolor='grey', linewidth=0.8, alpha=0.9)
        ax.add_patch(rect)
        text_color = 'white' if color == COLORS['primary'] else 'black'
        ax.text(node['x'], node['y'], node['label'], ha='center', va='center',
                fontsize=9, color=text_color, weight='bold', wrap=True)
    for edge in edges:
        n_from, n_to = nodes[edge['from_idx']], nodes[edge['to_idx']]
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
    if filename: save_fig(fig, filename)
    return fig, ax
```
