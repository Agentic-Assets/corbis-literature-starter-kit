"""Figure utilities for empirical finance research.

Publication-quality matplotlib defaults and standard plot types.
Import as:

    from utils.figure_utils import (
        set_publication_defaults, plot_event_study, plot_binned_scatter,
        coef_plot, set_size, plot_portfolio_bars, add_recession_bands,
        savefig, COLORS, BLUE_RED, GRAYSCALE
    )
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pathlib import Path

# ============================================================
# Color Palettes (Okabe-Ito colorblind-safe)
# ============================================================

COLORS = ['#377EB8', '#E41A1C', '#4DAF4A', '#984EA3',
          '#FF7F00', '#A65628', '#F781BF', '#999999']

# Two-series: long vs short, treatment vs control
BLUE_RED = ['#377EB8', '#E41A1C']

# Grayscale-safe (combine with linestyles for print)
GRAYSCALE = ['#000000', '#555555', '#999999', '#CCCCCC']


# ============================================================
# Style Setup
# ============================================================

def set_publication_defaults():
    """Apply matplotlib rcParams for publication-quality figures.

    Serif fonts (STIX math), 600 DPI, Type 42 font embedding,
    clean axes (no top/right spines). Call once at the top of
    any script that produces figures.
    """
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Times New Roman', 'STIXGeneral', 'DejaVu Serif'],
        'mathtext.fontset': 'stix',
        'font.size': 9,
        'axes.labelsize': 9,
        'axes.titlesize': 10,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 8,
        'axes.linewidth': 0.6,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.grid': False,
        'axes.axisbelow': True,
        'lines.linewidth': 1.2,
        'lines.markersize': 4,
        'xtick.direction': 'out',
        'ytick.direction': 'out',
        'xtick.major.size': 4,
        'ytick.major.size': 4,
        'xtick.major.width': 0.6,
        'ytick.major.width': 0.6,
        'legend.frameon': False,
        'figure.figsize': (6.5, 4.0),
        'figure.dpi': 150,
        'savefig.dpi': 600,
        'savefig.format': 'pdf',
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.05,
        'pdf.fonttype': 42,
        'ps.fonttype': 42,
        'axes.prop_cycle': plt.cycler('color', COLORS),
    })


def set_size(width='single', ratio='golden'):
    """Return (width, height) tuple in inches for journal-aware figure sizing.

    Parameters
    ----------
    width : str or float
        'single' (3.5"), 'onehalf' (5.25"), 'double' (7.0"),
        'slide' (10.0"), or a float in inches.
    ratio : str or float
        'golden' (1.618), 'square' (1.0), 'wide' (2.0), or a float.

    Returns
    -------
    tuple of (width, height) in inches.
    """
    widths = {'single': 3.5, 'onehalf': 5.25, 'double': 7.0, 'slide': 10.0}
    ratios = {'golden': 1.618, 'square': 1.0, 'wide': 2.0}
    w = widths.get(width, width) if isinstance(width, str) else width
    r = ratios.get(ratio, ratio) if isinstance(ratio, str) else ratio
    return (w, w / r)


def savefig(fig, name, formats=('pdf',), dpi=600, preview=True):
    """Save figure with publication settings and metadata embedding.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
    name : str
        Output path without extension (e.g., 'output/figures/hml_deciles').
    formats : tuple of str
        File formats to save ('pdf', 'png', 'eps', 'tif').
    dpi : int
        Resolution for raster formats.
    preview : bool
        If True, also save a low-res PNG for quick viewing.
    """
    path = Path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    for fmt in formats:
        fig.savefig(f'{name}.{fmt}', bbox_inches='tight', dpi=dpi)
    if preview and 'png' not in formats:
        fig.savefig(f'{name}.png', bbox_inches='tight', dpi=150)


# ============================================================
# Statistical Utilities
# ============================================================

def _newey_west_se(x, lag=None):
    """Newey-West HAC standard error of the mean.

    Parameters
    ----------
    x : array-like
        Time series of observations.
    lag : int, optional
        Number of lags. Defaults to floor(T^0.25).

    Returns
    -------
    float
        Newey-West standard error of the mean.
    """
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]
    T = len(x)
    if T < 2:
        return np.nan
    if lag is None:
        lag = int(np.floor(T ** 0.25))
    xbar = x.mean()
    e = x - xbar
    gamma0 = np.dot(e, e) / T
    nw_var = gamma0
    for j in range(1, lag + 1):
        gamma_j = np.dot(e[j:], e[:-j]) / T
        nw_var += 2 * (1 - j / (lag + 1)) * gamma_j
    return np.sqrt(nw_var / T)


# ============================================================
# Finance-Specific Plot Types
# ============================================================

def plot_event_study(coefs, ci_lower, ci_upper, event_times,
                     ref_period=-1, ylabel='Coefficient',
                     xlabel='Event time', title=None, filename=None):
    """Plot event-study coefficients with confidence bands.

    Parameters
    ----------
    coefs : array-like
        Point estimates (excluding reference period).
    ci_lower, ci_upper : array-like
        Confidence interval bounds (same length as coefs).
    event_times : array-like
        Event-time integers corresponding to coefs (excluding reference).
    ref_period : int
        Omitted reference period (plotted as zero).
    ylabel, xlabel : str
    title : str, optional
    filename : str or Path, optional
        Save path (e.g. 'output/figures/event_study.pdf').

    Returns
    -------
    (fig, ax)
    """
    set_publication_defaults()

    all_times = sorted(set(list(event_times) + [ref_period]))
    plot_coefs, plot_lo, plot_hi = [], [], []
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

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.axhline(y=0, color='grey', linewidth=0.8, linestyle='--')
    ax.axvline(x=-0.5, color='grey', linewidth=0.8, linestyle=':', alpha=0.6)
    ax.plot(all_times, plot_coefs, 'o-', color=COLORS[0],
            markersize=5, linewidth=1.5)
    ax.fill_between(all_times, plot_lo, plot_hi,
                    alpha=0.15, color=COLORS[0])
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.set_xticks(all_times)
    fig.tight_layout()
    if filename:
        fig.savefig(filename)
        print(f'Figure saved to {filename}')
    return fig, ax


def plot_binned_scatter(df, x, y, n_bins=20, controls=None,
                        xlabel=None, ylabel=None, filename=None):
    """Binned scatter plot with optional residualization.

    Parameters
    ----------
    df : DataFrame
    x, y : str
        Column names for x and y axes.
    n_bins : int
        Number of equal-frequency bins.
    controls : list of str, optional
        Control variables to residualize x and y against.
    xlabel, ylabel : str, optional
    filename : str or Path, optional

    Returns
    -------
    (fig, ax)
    """
    set_publication_defaults()

    plot_df = df[[x, y] + (controls or [])].dropna().copy()

    if controls:
        import statsmodels.api as sm
        for var in [x, y]:
            X = sm.add_constant(plot_df[controls])
            resid = sm.OLS(plot_df[var], X, missing='drop').fit().resid
            plot_df[var] = resid

    plot_df['bin'] = pd.qcut(plot_df[x], n_bins, labels=False,
                             duplicates='drop')
    binned = plot_df.groupby('bin').agg({x: 'mean', y: 'mean'}).reset_index()

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.scatter(binned[x], binned[y], color=COLORS[0], s=40, zorder=3)

    z = np.polyfit(binned[x], binned[y], 1)
    p = np.poly1d(z)
    x_line = np.linspace(binned[x].min(), binned[x].max(), 100)
    ax.plot(x_line, p(x_line), color=COLORS[1], linewidth=1.5,
            linestyle='--')

    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    fig.tight_layout()
    if filename:
        fig.savefig(filename)
        print(f'Figure saved to {filename}')
    return fig, ax


def coef_plot(results, vars_subset, var_labels=None,
              ylabel='', filename=None):
    """Coefficient plot with 95% confidence intervals.

    Parameters
    ----------
    results : fitted result object
        Must have .params, .conf_int() methods.
    vars_subset : list of str
        Variable names to plot.
    var_labels : dict, optional
        Display labels for variables.
    ylabel : str
    filename : str or Path, optional

    Returns
    -------
    (fig, ax)
    """
    set_publication_defaults()

    if var_labels is None:
        var_labels = {v: v for v in vars_subset}

    ci = results.conf_int()
    coefs = results.params[vars_subset]
    lower = ci.loc[vars_subset].iloc[:, 0]
    upper = ci.loc[vars_subset].iloc[:, 1]
    labels = [var_labels.get(v, v) for v in vars_subset]

    fig, ax = plt.subplots(figsize=(6.5, max(3, len(vars_subset) * 0.5)))
    y_pos = range(len(vars_subset))
    ax.axvline(x=0, color='grey', linewidth=0.8, linestyle='--')
    ax.errorbar(coefs, y_pos, xerr=[coefs - lower, upper - coefs],
                fmt='o', color=COLORS[0], markersize=5, linewidth=1.5,
                capsize=3)
    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(labels)
    ax.set_xlabel(ylabel)
    ax.invert_yaxis()
    fig.tight_layout()
    if filename:
        fig.savefig(filename)
        print(f'Figure saved to {filename}')
    return fig, ax


def plot_portfolio_bars(ax, returns_df, labels=None, highlight_extremes=True,
                        ylabel='Mean Return (% monthly)', show_ls=True,
                        ls_label='10-1', scale=100, lag=None):
    """Bar chart of decile portfolio means with Newey-West 95% CI error bars.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
    returns_df : pd.DataFrame
        Columns are portfolios (0, 1, ..., N-1), rows are time periods.
        Each column is the return time series for that portfolio.
    labels : list of str, optional
        X-axis labels for portfolios. Defaults to 1, 2, ..., N.
    highlight_extremes : bool
        Color the short (low) and long (high) legs differently.
    ylabel : str
    show_ls : bool
        If True, append a long-short (last - first) bar.
    ls_label : str
        Label for the long-short bar.
    scale : float
        Multiply returns by this (default 100 for percent).
    lag : int, optional
        Newey-West lag. Defaults to floor(T^0.25).
    """
    port_cols = [c for c in returns_df.columns if c != 'hml']
    n = len(port_cols)
    if labels is None:
        labels = [str(i + 1) for i in range(n)]

    means = [returns_df[c].mean() * scale for c in port_cols]
    ses = [_newey_west_se(returns_df[c].values, lag=lag) * scale for c in port_cols]

    if show_ls:
        ls_series = returns_df[port_cols[-1]] - returns_df[port_cols[0]]
        ls_mean = ls_series.mean() * scale
        ls_se = _newey_west_se(ls_series.values, lag=lag) * scale
        means.append(ls_mean)
        ses.append(ls_se)
        labels = list(labels) + [ls_label]

    n_bars = len(means)
    x = np.arange(n_bars)
    ci95 = [1.96 * s for s in ses]

    colors = [COLORS[0]] * n
    if highlight_extremes:
        colors[0] = COLORS[1]       # Short leg = red
        colors[-1] = COLORS[2]      # Long leg = green
    if show_ls:
        colors.append(COLORS[3])    # L-S = purple

    ax.bar(x, means, color=colors, edgecolor='white', linewidth=0.5, width=0.7,
           yerr=ci95, error_kw=dict(capsize=3, linewidth=0.8, color='black'))
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_xlabel('Portfolio')
    ax.set_ylabel(ylabel)
    ax.axhline(0, color='grey', linewidth=0.4, zorder=0)

    # Annotate L-S with t-stat
    if show_ls:
        t_stat = means[-1] / ses[-1] if ses[-1] > 0 else np.nan
        y_pos = means[-1] + ci95[-1] if means[-1] >= 0 else means[-1] - ci95[-1]
        va = 'bottom' if means[-1] >= 0 else 'top'
        ax.text(x[-1], y_pos, f't = {t_stat:.2f}',
                ha='center', va=va, fontsize=7, style='italic')


def add_recession_bands(ax, recessions=None):
    """Add NBER recession shading to a time series axis.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
    recessions : list of (start, end) tuples, optional
        If None, uses NBER recessions from 2001 onward.
    """
    if recessions is None:
        recessions = [
            ('2001-03-01', '2001-11-01'),
            ('2007-12-01', '2009-06-01'),
            ('2020-02-01', '2020-04-01'),
        ]
    for start, end in recessions:
        ax.axvspan(pd.Timestamp(start), pd.Timestamp(end),
                   alpha=0.08, color='grey', zorder=0)
