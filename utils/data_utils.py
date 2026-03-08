"""Data utilities for empirical finance research.

Helpers for WRDS connection, winsorization, merge validation,
and Fama-French date alignment. Import as:

    from utils.data_utils import connect_wrds, winsorize, merge_with_check
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path


def connect_wrds():
    """Connect to WRDS using .env credentials and ~/.pgpass.

    Returns
    -------
    wrds.Connection
    """
    import wrds
    from dotenv import load_dotenv
    load_dotenv()

    username = os.getenv('WRDS_USERNAME')
    if not username:
        raise EnvironmentError(
            'WRDS_USERNAME not set. Copy .env.example to .env and fill in your username.'
        )
    return wrds.Connection(wrds_username=username)


def winsorize(df, var, limits=(0.01, 0.99), by=None):
    """Winsorize variable at specified percentiles, optionally by group.

    Parameters
    ----------
    df : DataFrame
    var : str
        Column to winsorize.
    limits : tuple
        Lower and upper percentile thresholds (e.g. (0.01, 0.99)).
    by : str or list, optional
        Group column(s) for within-group winsorization.

    Returns
    -------
    DataFrame with winsorized column (modified in place).
    """
    if by is None:
        lo, hi = df[var].quantile([limits[0], limits[1]])
        df[var] = df[var].clip(lower=lo, upper=hi)
    else:
        df[var] = df.groupby(by)[var].transform(
            lambda x: x.clip(
                lower=x.quantile(limits[0]),
                upper=x.quantile(limits[1])
            )
        )
    return df


def merge_with_check(left, right, on, how='inner', indicator=True,
                     min_match_rate=0.5, name=''):
    """Merge two DataFrames with match-rate validation.

    Parameters
    ----------
    left, right : DataFrame
    on : str or list
        Join key(s).
    how : str
        Merge type (default 'inner').
    indicator : bool
        Print merge diagnostics.
    min_match_rate : float
        Minimum fraction of left rows that must match. Raises ValueError
        if the match rate falls below this threshold.
    name : str
        Label for diagnostic output.

    Returns
    -------
    DataFrame (without the _merge indicator column).
    """
    label = f' [{name}]' if name else ''
    n_left = len(left)

    merged = left.merge(right, on=on, how=how, indicator=True)

    if indicator:
        counts = merged['_merge'].value_counts()
        print(f'Merge{label}: {n_left:,} left rows')
        for k, v in counts.items():
            print(f'  {k}: {v:,}')

    if how in ('inner', 'left'):
        match_rate = (merged['_merge'] == 'both').sum() / max(n_left, 1)
        if match_rate < min_match_rate:
            raise ValueError(
                f'Merge{label} match rate {match_rate:.1%} below '
                f'threshold {min_match_rate:.1%}'
            )

    merged = merged.drop(columns=['_merge'])
    return merged


def align_fiscal_to_calendar(df, date_col='datadate', lag_months=6):
    """Align fiscal year-end dates to Fama-French portfolio formation timing.

    Adds a 'jdate' column: datadate + lag_months, snapped to month-end.
    This avoids look-ahead bias by ensuring accounting data is available
    before portfolio formation.

    Parameters
    ----------
    df : DataFrame
    date_col : str
        Fiscal year-end date column.
    lag_months : int
        Months to lag (default 6 for June formation).

    Returns
    -------
    DataFrame with 'jdate' column added.
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df['jdate'] = df[date_col] + pd.DateOffset(months=lag_months)
    df['jdate'] = df['jdate'] + pd.offsets.MonthEnd(0)
    return df
