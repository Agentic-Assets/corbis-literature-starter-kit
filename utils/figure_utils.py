"""Figure utilities for empirical finance research.

Publication-quality matplotlib defaults and standard plot types.
Import as:

    from utils.figure_utils import set_publication_defaults, plot_event_study, plot_binned_scatter
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

COLORS = ['#2c3e50', '#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']


def set_publication_defaults():
    """Apply matplotlib rcParams for publication-quality figures.

    Serif fonts, 300 DPI, clean axes (no top/right spines).
    Call once at the top of any script that produces figures.
    """
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
        'axes.grid': False,
        'axes.spines.top': False,
        'axes.spines.right': False,
    })


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
