"""Regression utilities for empirical finance research.

Quick exploration regressions, portfolio sorts, and alpha tests.
Import as:

    from utils.regression_utils import explore_reg, portfolio_sort, alpha_table
"""

import numpy as np
import pandas as pd


def explore_reg(df, y, x_list, fe=None, cluster=None, controls=None,
                label=None):
    """Run quick regressions and print one-line summaries. For exploration only.

    Parameters
    ----------
    df : DataFrame
    y : str
        Dependent variable.
    x_list : list of str
        Variables of interest (one regression per variable).
    fe : str or list, optional
        Fixed effect index column(s) for PanelOLS. If provided, uses
        linearmodels with EntityEffects and entity clustering.
    cluster : str, optional
        Clustering variable for cross-sectional OLS (statsmodels).
    controls : list of str, optional
        Additional RHS controls included in every regression.
    label : str, optional
        Header label for the output block.
    """
    from linearmodels.panel import PanelOLS
    import statsmodels.formula.api as smf

    if label:
        print(f"\n{'=' * 60}\n{label}\n{'=' * 60}")
    print(f"{'Variable':<30} {'Coef':>10} {'t-stat':>10} {'N':>10} {'R2':>8}")
    print('-' * 72)

    for x in x_list:
        try:
            rhs = [x] + (controls or [])
            if fe:
                fe_cols = fe if isinstance(fe, list) else [fe]
                all_cols = [y] + rhs
                df_reg = df[fe_cols + all_cols].dropna().set_index(fe_cols)
                formula = f'{y} ~ 1 + {" + ".join(rhs)} + EntityEffects'
                res = PanelOLS.from_formula(formula, df_reg).fit(
                    cov_type='clustered', cluster_entity=True
                )
            else:
                all_cols = [y] + rhs + ([cluster] if cluster else [])
                df_reg = df[all_cols].dropna()
                formula = f'{y} ~ {" + ".join(rhs)}'
                fit_kwargs = {}
                if cluster:
                    fit_kwargs = {
                        'cov_type': 'cluster',
                        'cov_kwds': {'groups': df_reg[cluster]},
                    }
                res = smf.ols(formula, df_reg).fit(**fit_kwargs)

            coef = res.params[x]
            tval = res.tvalues[x]
            nobs = int(res.nobs)
            r2 = getattr(res, 'rsquared_adj',
                         getattr(res, 'rsquared', float('nan')))
            print(f'{x:<30} {coef:>10.4f} {tval:>10.2f} {nobs:>10,} {r2:>8.3f}')
        except Exception as e:
            print(f'{x:<30} {"FAILED":>10} — {str(e)[:40]}')


def portfolio_sort(df, signal, n_portfolios=5, nyse_breakpoints=True,
                   weight='vw'):
    """Single-sort portfolios with NYSE breakpoints and value-weighting.

    Parameters
    ----------
    df : DataFrame
        Must contain columns: date, ret_excess, mktcap, exchcd (if
        nyse_breakpoints=True), and the signal column.
    signal : str
        Sorting variable.
    n_portfolios : int
        Number of portfolios (default 5 for quintiles).
    nyse_breakpoints : bool
        Use NYSE-listed stocks only for breakpoints.
    weight : str
        'vw' for value-weighted, 'ew' for equal-weighted.

    Returns
    -------
    DataFrame with columns Q1, Q2, ..., Qn, HML indexed by date.
    """
    required = [signal, 'ret_excess', 'mktcap', 'date']
    if nyse_breakpoints:
        required.append('exchcd')
    df = df.dropna(subset=[signal, 'ret_excess', 'mktcap']).copy()

    def assign_portfolio(group):
        if nyse_breakpoints:
            nyse = group[group['exchcd'] == 1][signal]
            if len(nyse) < n_portfolios:
                group['portfolio'] = np.nan
                return group
            breakpoints = nyse.quantile(
                np.linspace(0, 1, n_portfolios + 1)[1:-1]
            )
        else:
            breakpoints = group[signal].quantile(
                np.linspace(0, 1, n_portfolios + 1)[1:-1]
            )
        group['portfolio'] = np.searchsorted(breakpoints, group[signal]) + 1
        return group

    df = df.groupby('date', group_keys=False).apply(assign_portfolio)
    df = df.dropna(subset=['portfolio'])
    df['portfolio'] = df['portfolio'].astype(int)

    if weight == 'vw':
        port_ret = df.groupby(['date', 'portfolio']).apply(
            lambda x: np.average(x['ret_excess'], weights=x['mktcap'])
        ).reset_index(name='ret')
    else:
        port_ret = (df.groupby(['date', 'portfolio'])['ret_excess']
                    .mean().reset_index(name='ret'))

    port_ret = port_ret.pivot(index='date', columns='portfolio', values='ret')
    port_ret.columns = [f'Q{i}' for i in port_ret.columns]
    port_ret['HML'] = port_ret[f'Q{n_portfolios}'] - port_ret['Q1']
    return port_ret


def alpha_table(port_returns, factor_df, models=None):
    """Compute alphas for each portfolio against multiple factor models.

    Parameters
    ----------
    port_returns : DataFrame
        Portfolio returns indexed by date (columns: Q1, ..., Qn, HML).
    factor_df : DataFrame
        Factor returns indexed by date. Must contain: mktrf, smb, hml,
        and optionally rmw, cma, umd.
    models : list of str, optional
        Factor models to test (default: ['CAPM', 'FF3', 'FF5']).

    Returns
    -------
    DataFrame with columns: portfolio, model, alpha (annualized bps
    if monthly, or raw %), t_stat.
    """
    import statsmodels.api as sm

    if models is None:
        models = ['CAPM', 'FF3', 'FF5']

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
            cols = factor_cols[model_name]
            valid = merged[[col] + cols].dropna()
            if len(valid) < 24:
                continue
            y = valid[col]
            X = sm.add_constant(valid[cols])
            reg = sm.OLS(y, X).fit(cov_type='HAC', cov_kwds={'maxlags': 6})
            results.append({
                'portfolio': col,
                'model': model_name,
                'alpha': reg.params['const'] * 100,
                't_stat': reg.tvalues['const'],
            })

    return pd.DataFrame(results)
