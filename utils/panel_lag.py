"""Safe panel lagging/leading with mandatory gap validation.

Shifts columns forward (lag) or backward (lead) within groups, then validates
that the date gap between paired observations falls within frequency-appropriate
bounds. Observations with invalid gaps (missing periods, fiscal year changes,
delistings) are set to NaN rather than silently pairing non-adjacent records.

Works for any panel data: CRSP stocks, Dickerson bonds, OptionMetrics,
quarterly/annual accounting data.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# (min_gap_days, max_gap_days) per single period shift
_GAP_THRESHOLDS: dict[str, tuple[int, int]] = {
    "D": (0, 5),       # daily: weekends/holidays up to 5 calendar days
    "M": (28, 31),     # monthly: month-end normalized
    "Q": (80, 100),    # quarterly: ~90 days, allow for fiscal quirks
    "A": (350, 380),   # annual: ~365 days, allow for FYE variation
}

_VALID_FREQS = set(_GAP_THRESHOLDS.keys())

_SENTINEL = object()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def panel_lag(
    df: pd.DataFrame,
    id_col: str = "permno",
    date_col: str = "date",
    cols: list[str] | str | None = None,
    periods: int = 1,
    freq: str = "M",
    suffix: str | None = _SENTINEL,
    max_gap: int | None = None,
    min_gap: int | None = None,
) -> pd.DataFrame:
    """Lag or lead panel columns with mandatory gap validation.

    Parameters
    ----------
    df : DataFrame
        Panel with columns [id_col, date_col, ...].
    id_col : str
        Column identifying entities (e.g., "permno", "cusip", "gvkey").
    date_col : str
        Date column name.
    cols : list of str, str, or None
        Columns to shift. If str, coerced to [str]. If None, all numeric
        columns except id_col and date_col.
    periods : int
        Number of periods to shift. Positive = lag (previous period's value),
        negative = lead (next period's value). Zero raises ValueError.
    freq : str
        Frequency code: "M" (monthly), "Q" (quarterly), "A" (annual),
        "D" (daily). Case-insensitive. Determines gap thresholds.
    suffix : str or None
        Format string for output column names. Use {k} for the absolute
        shift size. Default auto-selects "_lag{k}" or "_lead{k}".
        Pass None to overwrite columns in place.
    max_gap : int, optional
        Override maximum gap threshold (calendar days). If provided,
        bypasses frequency lookup. Caller handles k-scaling.
    min_gap : int, optional
        Override minimum gap threshold (calendar days). If provided,
        bypasses frequency lookup. Caller handles k-scaling.

    Returns
    -------
    DataFrame
        Copy of df with lagged/led columns added (or overwritten if
        suffix is None). Original row order preserved.
    """
    # --- Input validation ---
    if periods == 0:
        raise ValueError("periods must be nonzero")

    for col in [id_col, date_col]:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in DataFrame")

    freq = freq.upper()
    if freq not in _VALID_FREQS:
        raise ValueError(f"freq must be one of {sorted(_VALID_FREQS)}, got '{freq}'")

    # Resolve columns
    if cols is None:
        numeric = df.select_dtypes(include="number").columns.tolist()
        cols = [c for c in numeric if c not in (id_col, date_col)]
    elif isinstance(cols, str):
        cols = [cols]

    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"Columns not found: {missing}")
    if not cols:
        raise ValueError("No columns to shift")

    if df.empty:
        return df.copy()

    # --- Copy and prepare ---
    out = df.copy()
    out[date_col] = pd.to_datetime(out[date_col])

    # Check for duplicates
    dup_mask = out.duplicated(subset=[id_col, date_col], keep=False)
    if dup_mask.any():
        n_dup = dup_mask.sum()
        raise ValueError(
            f"Found {n_dup} duplicate ({id_col}, {date_col}) rows. "
            f"Deduplicate before lagging."
        )

    # Sort by (entity, date), track original order
    out["_orig_idx"] = np.arange(len(out))
    out = out.sort_values([id_col, date_col], kind="mergesort").reset_index(drop=True)

    # --- Resolve suffix ---
    k = abs(periods)
    if suffix is _SENTINEL:
        suffix = "_lead{k}" if periods < 0 else "_lag{k}"

    suffix_str = suffix.format(k=k) if suffix is not None else None

    # --- Resolve gap thresholds ---
    if max_gap is None:
        max_gap = _GAP_THRESHOLDS[freq][1] * k
    if min_gap is None:
        min_gap = _GAP_THRESHOLDS[freq][0] * k

    # --- Vectorized NumPy fast path ---
    gid, _ = pd.factorize(out[id_col], sort=False)
    gid = gid.astype(np.int32)

    dates_days = out[date_col].to_numpy("datetime64[D]").astype(np.int64)
    vals = out[cols].to_numpy(dtype=np.float64, na_value=np.nan)

    N = len(vals)

    if periods > 0:
        # Lag: shifted[i] = vals[i - k] if same group and gap valid
        same_group = gid[k:] == gid[:N - k]
        gap = dates_days[k:] - dates_days[:N - k]
        valid = same_group & (gap >= min_gap) & (gap <= max_gap)

        shifted = np.full_like(vals, np.nan)
        shifted[k:][valid] = vals[:N - k][valid]
    else:
        # Lead: shifted[i] = vals[i + k] if same group and gap valid
        same_group = gid[:N - k] == gid[k:]
        gap = dates_days[k:] - dates_days[:N - k]
        valid = same_group & (gap >= min_gap) & (gap <= max_gap)

        shifted = np.full_like(vals, np.nan)
        shifted[:N - k][valid] = vals[k:][valid]

    # --- Assign output columns ---
    if suffix_str is None:
        # Overwrite in place
        for j, c in enumerate(cols):
            out[c] = shifted[:, j]
    else:
        for j, c in enumerate(cols):
            out[c + suffix_str] = shifted[:, j]

    # --- Restore original order ---
    out = out.sort_values("_orig_idx").reset_index(drop=True)
    out = out.drop(columns=["_orig_idx"])

    return out
