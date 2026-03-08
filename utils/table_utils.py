"""LaTeX table utilities for empirical finance research.

Generates publication-ready regression and summary statistics tables
matching the project's latex_template format. Import as:

    from utils.table_utils import reg_to_latex, summary_stats_latex
"""

import numpy as np
import pandas as pd
from pathlib import Path


def reg_to_latex(results_list, dep_var_label, col_labels=None,
                 coef_subset=None, coef_labels=None, fe_rows=None,
                 stats_rows=None, filename=None, note=None, label=None):
    """Convert linearmodels/statsmodels results to a LaTeX regression table.

    Follows template format: caption -> label -> vspace -> floatnotes -> tabular body.
    Reports t-statistics in parentheses below coefficients.

    Parameters
    ----------
    results_list : list
        Fitted result objects (linearmodels or statsmodels).
    dep_var_label : str
        Table caption / dependent variable description.
    col_labels : list of str, optional
        Column headers (default: (1), (2), ...).
    coef_subset : list of str, optional
        Variable names to display (default: all).
    coef_labels : dict, optional
        Mapping from variable names to display labels.
    fe_rows : dict, optional
        Fixed effects indicators. Keys are labels, values are lists
        of 'Yes'/'No' strings, one per column.
    stats_rows : list of str, optional
        Statistics to report: 'nobs', 'r2', 'r2_adj' (default: nobs, r2_adj).
    filename : str or Path, optional
        Output path (e.g. 'output/tables/baseline.tex').
    note : str, optional
        Descriptive table note (prepended to standard t-stat note).
    label : str, optional
        LaTeX label (default: tab:<dep_var_label>).

    Returns
    -------
    str : LaTeX table source.
    """
    n_cols = len(results_list)
    if col_labels is None:
        col_labels = [f'({i+1})' for i in range(n_cols)]
    if stats_rows is None:
        stats_rows = ['nobs', 'r2_adj']
    if label is None:
        label = 'tab:' + dep_var_label.lower().replace(' ', '_')[:30]
    if coef_labels is None:
        coef_labels = {}

    # Collect all variable names across models
    all_vars = []
    seen = set()
    for res in results_list:
        for var in res.params.index:
            if var not in seen:
                all_vars.append(var)
                seen.add(var)

    display_vars = (
        [v for v in coef_subset if v in seen] if coef_subset else all_vars
    )

    lines = []
    lines.append(r'\begin{table}[!htbp]')
    lines.append(r'\centering')
    lines.append(f'\\caption{{{dep_var_label}}}')
    lines.append(f'\\label{{{label}}}\\vspace{{-2.5ex}}')

    note_text = note + ' t-statistics in parentheses.' if note else 't-statistics in parentheses.'
    lines.append(r'\floatnotes{' + note_text + '}')

    lines.append(r'\small')
    lines.append(r'\begin{tabular}{l' + 'c' * n_cols + '}')
    lines.append(r'\toprule')
    lines.append(' & ' + ' & '.join(col_labels) + r' \\')
    lines.append(r'\midrule')

    for var in display_vars:
        var_label = coef_labels.get(var, var)
        coefs, tstats = [], []
        for res in results_list:
            if var in res.params.index:
                coef = res.params[var]
                tval = res.tvalues[var]
                pval = res.pvalues[var]
                stars = _sig_stars(pval)
                coefs.append(f'{coef:.4f}\\sym{{{stars}}}')
                tstats.append(f'({tval:.2f})')
            else:
                coefs.append('')
                tstats.append('')
        lines.append(var_label + ' & ' + ' & '.join(coefs) + r' \\')
        lines.append(' & ' + ' & '.join(tstats) + r' \\[0.5ex]')

    lines.append(r'\midrule')

    if fe_rows:
        for fe_label, vals in fe_rows.items():
            lines.append(fe_label + ' & ' + ' & '.join(vals) + r' \\')

    stat_labels = {
        'nobs': 'Observations',
        'r2': '$R^2$',
        'r2_adj': 'Adj.\\ $R^2$',
    }
    for stat in stats_rows:
        vals = []
        for res in results_list:
            if stat == 'nobs':
                vals.append(f'{int(res.nobs):,}')
            elif stat == 'r2':
                vals.append(f'{res.rsquared:.3f}')
            elif stat == 'r2_adj':
                r2 = getattr(res, 'rsquared_adj',
                             getattr(res, 'rsquared', np.nan))
                vals.append(f'{r2:.3f}')
        lines.append(stat_labels[stat] + ' & ' + ' & '.join(vals) + r' \\')

    lines.append(r'\bottomrule')
    sig_note = (r'\footnotesize \sym{*} $p<0.10$, '
                r'\sym{**} $p<0.05$, \sym{***} $p<0.01$.')
    lines.append(r'\multicolumn{' + str(n_cols + 1) + '}{l}{' + sig_note + '}')
    lines.append(r'\end{tabular}')
    lines.append(r'\end{table}')

    tex = '\n'.join(lines)
    if filename:
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        Path(filename).write_text(tex)
        print(f'Table saved to {filename}')
    return tex


def summary_stats_latex(df, variables, labels=None, stats=None,
                        filename=None, caption='Summary Statistics',
                        label='tab:summary', note=None):
    """Generate a LaTeX summary statistics table.

    Parameters
    ----------
    df : DataFrame
    variables : list of str
        Columns to summarize.
    labels : dict, optional
        Mapping from column names to display labels.
    stats : list of str, optional
        Statistics to compute: 'mean', 'sd', 'p25', 'median', 'p75', 'n'.
    filename : str or Path, optional
        Output path.
    caption : str
        Table caption.
    label : str
        LaTeX label.
    note : str, optional
        Descriptive note.

    Returns
    -------
    str : LaTeX table source.
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

    default_note = (
        'This table reports summary statistics for the main variables. '
        'The sample period is [PERIOD]. '
        r'See Appendix Table~\ref{tab:appendix_variables} for variable definitions.'
    )

    lines = []
    lines.append(r'\begin{table}[!htbp]')
    lines.append(r'\centering')
    lines.append(f'\\caption{{{caption}}}')
    lines.append(f'\\label{{{label}}}\\vspace{{-2.5ex}}')
    lines.append(r'\floatnotes{' + (note or default_note) + '}')
    lines.append(r'\small')
    lines.append(r'\begin{tabularx}{\textwidth}{@{}X' + 'r' * len(stats) + '@{}}')
    lines.append(r'\toprule')
    lines.append(' & '.join([f'\\textbf{{{h}}}' for h in header]) + r' \\')
    lines.append(r'\midrule')

    for var in variables:
        row = [labels.get(var, var)]
        row += [stat_funcs[s](df[var]) for s in stats]
        lines.append(' & '.join(row) + r' \\')

    lines.append(r'\bottomrule')
    lines.append(r'\end{tabularx}')
    lines.append(r'\end{table}')

    tex = '\n'.join(lines)
    if filename:
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        Path(filename).write_text(tex)
        print(f'Table saved to {filename}')
    return tex


def _sig_stars(pval):
    """Return significance stars based on p-value."""
    if pval < 0.01:
        return '***'
    elif pval < 0.05:
        return '**'
    elif pval < 0.10:
        return '*'
    return ''
