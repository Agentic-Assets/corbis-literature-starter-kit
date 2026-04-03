"""Rolling OLS betas for panel data.

Computes rolling-window factor betas for any panel of returns (stocks, bonds,
options, etc.) against one or more factors. Uses Numba-compiled kernels for
speed: cumulative-sum approach for single-factor, ring-buffer + Gramian solve
for multi-factor.

Adapted from Dickerson bond data pipeline (process_bond_data.py).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from numba import njit


# ---------------------------------------------------------------------------
# Numba kernels (private)
# ---------------------------------------------------------------------------

@njit(cache=True, fastmath=True)
def _outer_add(A, z):
    """Rank-1 update: A += z z'."""
    p = z.shape[0]
    for i in range(p):
        zi = z[i]
        for j in range(p):
            A[i, j] += zi * z[j]


@njit(cache=True, fastmath=True)
def _outer_sub(A, z):
    """Rank-1 downdate: A -= z z'."""
    p = z.shape[0]
    for i in range(p):
        zi = z[i]
        for j in range(p):
            A[i, j] -= zi * z[j]


@njit(cache=True, fastmath=True)
def _panel_rolling_ols_k1(gid, y, x, window, min_obs):
    """Single-factor rolling OLS using cumulative sums.

    Returns (alpha, beta, sig_tot, sig_idi, adj_r2), each length N.
    """
    N = y.shape[0]

    alpha = np.full(N, np.nan)
    beta = np.full(N, np.nan)
    sig_tot = np.full(N, np.nan)
    sig_idi = np.full(N, np.nan)
    adj_r2 = np.full(N, np.nan)

    # Within-group cumulative sums
    cx = np.empty(N, dtype=np.float64)
    cy = np.empty(N, dtype=np.float64)
    cxx = np.empty(N, dtype=np.float64)
    cyy = np.empty(N, dtype=np.float64)
    cxy = np.empty(N, dtype=np.float64)

    prev = -1
    sx = sy = sxx = syy = sxy = 0.0
    for i in range(N):
        g = gid[i]
        if g != prev:
            prev = g
            sx = sy = sxx = syy = sxy = 0.0

        xi = x[i]
        yi = y[i]

        sx += xi
        sy += yi
        sxx += xi * xi
        syy += yi * yi
        sxy += xi * yi

        cx[i] = sx
        cy[i] = sy
        cxx[i] = sxx
        cyy[i] = syy
        cxy[i] = sxy

    gstart = 0
    for i in range(N):
        if i == 0 or gid[i] != gid[i - 1]:
            gstart = i

        left = i - window + 1
        if left < gstart:
            left = gstart

        m = i - left + 1
        if m < min_obs:
            continue

        if left == gstart:
            Sx, Sy, Sxx, Syy, Sxy = cx[i], cy[i], cxx[i], cyy[i], cxy[i]
        else:
            j = left - 1
            Sx = cx[i] - cx[j]
            Sy = cy[i] - cy[j]
            Sxx = cxx[i] - cxx[j]
            Syy = cyy[i] - cyy[j]
            Sxy = cxy[i] - cxy[j]

        mf = float(m)
        xbar = Sx / mf
        ybar = Sy / mf

        Sxxc = Sxx - (Sx * Sx) / mf
        Sxyc = Sxy - (Sx * Sy) / mf
        Syyc = Syy - (Sy * Sy) / mf  # SST

        if Sxxc <= 0.0 or Syyc <= 0.0:
            continue

        b = Sxyc / Sxxc
        a = ybar - b * xbar

        SSE = Syyc - b * Sxyc
        if SSE < 0.0:
            SSE = 0.0

        if m > 1:
            sig_tot[i] = np.sqrt(Syyc / (mf - 1.0))

        if m > 2:
            sig_idi[i] = np.sqrt(SSE / (mf - 2.0))
            R2 = 1.0 - SSE / Syyc
            adj_r2[i] = 1.0 - (1.0 - R2) * (mf - 1.0) / (mf - 2.0)

        alpha[i] = a
        beta[i] = b

    return alpha, beta, sig_tot, sig_idi, adj_r2


@njit(cache=True, fastmath=True)
def _panel_rolling_ols_kgt1(gid, y, X, window, min_obs, ridge):
    """Multi-factor rolling OLS using ring buffer + Gramian solve.

    Returns (betas [N x K+1], sig_tot, sig_idi, adj_r2).
    betas[:, 0] = alpha, betas[:, 1:] = factor betas.
    """
    N, K = X.shape
    K1 = K + 1

    betas = np.full((N, K1), np.nan)
    sig_tot = np.full(N, np.nan)
    sig_idi = np.full(N, np.nan)
    adj_r2 = np.full(N, np.nan)

    buf_y = np.empty(window, dtype=np.float64)
    buf_x = np.empty((window, K), dtype=np.float64)

    ZZ = np.zeros((K1, K1), dtype=np.float64)
    Zy = np.zeros(K1, dtype=np.float64)
    Sy = 0.0
    Syy = 0.0
    n = 0

    z = np.empty(K1, dtype=np.float64)

    prev = -1
    head = 0

    for i in range(N):
        g = gid[i]
        if g != prev:
            prev = g
            ZZ[:, :] = 0.0
            Zy[:] = 0.0
            Sy = 0.0
            Syy = 0.0
            n = 0
            head = 0

        yi = y[i]

        # Remove oldest if window full
        if n >= window:
            yo = buf_y[head]
            z[0] = 1.0
            for k in range(K):
                z[k + 1] = buf_x[head, k]
            _outer_sub(ZZ, z)
            for k1 in range(K1):
                Zy[k1] -= z[k1] * yo
            Sy -= yo
            Syy -= yo * yo
            n -= 1

        # Add new observation
        buf_y[head] = yi
        for k in range(K):
            buf_x[head, k] = X[i, k]

        z[0] = 1.0
        for k in range(K):
            z[k + 1] = X[i, k]

        _outer_add(ZZ, z)
        for k1 in range(K1):
            Zy[k1] += z[k1] * yi
        Sy += yi
        Syy += yi * yi
        n += 1

        head += 1
        if head == window:
            head = 0

        if n < min_obs:
            continue

        mf = float(n)
        SST = Syy - (Sy * Sy) / mf
        if SST <= 0.0:
            continue

        # Solve (ZZ + ridge*I) b = Zy
        A = ZZ.copy()
        for d in range(K1):
            A[d, d] += ridge

        try:
            b = np.linalg.solve(A, Zy)
        except Exception:
            continue

        betas[i, :] = b

        if n > 1:
            sig_tot[i] = np.sqrt(SST / (mf - 1.0))

        dof = n - K1
        if dof <= 0:
            continue

        # SSE via quadratic form (unregularized ZZ)
        quad = 0.0
        for a in range(K1):
            tmp = 0.0
            for c in range(K1):
                tmp += ZZ[a, c] * b[c]
            quad += b[a] * tmp

        SSE = Syy - 2.0 * np.dot(b, Zy) + quad
        if SSE < 0.0:
            SSE = 0.0

        sig_idi[i] = np.sqrt(SSE / float(dof))
        R2 = 1.0 - SSE / SST
        adj_r2[i] = 1.0 - (1.0 - R2) * (mf - 1.0) / float(dof)

    return betas, sig_tot, sig_idi, adj_r2


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def rolling_betas(
    returns: pd.DataFrame,
    factors: pd.DataFrame,
    id_col: str = "permno",
    date_col: str = "date",
    ret_col: str = "ret",
    factor_cols: list[str] | None = None,
    window: int = 36,
    min_obs: int = 12,
    ridge: float = 1e-12,
    include_alpha: bool = False,
) -> pd.DataFrame:
    """Compute rolling OLS betas for a panel of returns against factor(s).

    Parameters
    ----------
    returns : DataFrame
        Panel with columns [id_col, date_col, ret_col].
    factors : DataFrame
        Factor time series with columns [date_col, factor1, factor2, ...].
        One row per date (not per entity).
    id_col : str
        Column identifying entities (e.g., "permno", "cusip").
    date_col : str
        Date column name, present in both DataFrames.
    ret_col : str
        Return column name in *returns*.
    factor_cols : list of str, optional
        Which columns in *factors* to use. If None, all non-date columns.
    window : int
        Rolling window size (months/periods).
    min_obs : int
        Minimum observations required in window.
    ridge : float
        Ridge regularization for multi-factor solve (prevents singular matrices).
    include_alpha : bool
        If True, include the regression intercept in output.

    Returns
    -------
    DataFrame with columns:
        [id_col, date_col, beta_{f1}, ..., beta_{fK},
         sigma_total, sigma_idio, adj_r2]
        Plus alpha if include_alpha=True.
    """
    # --- Input validation ---
    for col in [id_col, date_col, ret_col]:
        if col not in returns.columns:
            raise ValueError(f"Column '{col}' not found in returns DataFrame")
    if date_col not in factors.columns:
        if date_col in getattr(factors.index, "names", [None]):
            factors = factors.reset_index()
        else:
            raise ValueError(f"Column '{date_col}' not found in factors DataFrame")

    if factor_cols is None:
        factor_cols = [c for c in factors.columns if c != date_col]
    else:
        missing = [c for c in factor_cols if c not in factors.columns]
        if missing:
            raise ValueError(f"Factor columns not found: {missing}")

    if not factor_cols:
        raise ValueError("No factor columns specified or found")

    # --- Prepare data ---
    rdf = returns[[id_col, date_col, ret_col]].copy()
    rdf[date_col] = pd.to_datetime(rdf[date_col])

    fdf = factors[[date_col] + factor_cols].copy()
    fdf[date_col] = pd.to_datetime(fdf[date_col])

    # Handle column name collision between ret_col and a factor
    rename_map = {}
    fac_cols_use = []
    for c in factor_cols:
        if c == ret_col:
            rename_map[c] = c + "_fac"
            fac_cols_use.append(c + "_fac")
        else:
            fac_cols_use.append(c)
    if rename_map:
        fdf = fdf.rename(columns=rename_map)

    # Merge returns with factors on date
    merged = pd.merge(rdf, fdf, on=date_col, how="left", sort=False)
    merged = merged.dropna(subset=[ret_col] + fac_cols_use).reset_index(drop=True)

    if merged.empty:
        raise ValueError("No observations after merging returns with factors and dropping NaNs")

    # Factorize entity IDs to contiguous int codes, sort by (entity, date)
    gid, _ = pd.factorize(merged[id_col], sort=False)
    merged["_gid"] = gid.astype(np.int32, copy=False)
    merged = merged.sort_values(["_gid", date_col], kind="mergesort").reset_index(drop=True)

    gid_arr = merged["_gid"].to_numpy(dtype=np.int32, copy=False)
    y = merged[ret_col].to_numpy(dtype=np.float64, copy=False)

    K = len(fac_cols_use)

    # --- Dispatch to K=1 or K>1 kernel ---
    if K == 1:
        x = merged[fac_cols_use[0]].to_numpy(dtype=np.float64, copy=False)
        a, b, sig_tot, sig_idi, r2 = _panel_rolling_ols_k1(
            gid_arr, y, x, int(window), int(min_obs)
        )
        out = pd.DataFrame({
            id_col: merged[id_col].to_numpy(copy=False),
            date_col: merged[date_col].to_numpy(copy=False),
            f"beta_{factor_cols[0]}": b,
            "sigma_total": sig_tot,
            "sigma_idio": sig_idi,
            "adj_r2": r2,
        })
        if include_alpha:
            out["alpha"] = a
        return out

    # K > 1
    X = merged[fac_cols_use].to_numpy(dtype=np.float64, copy=False)
    betas_arr, sig_tot, sig_idi, r2 = _panel_rolling_ols_kgt1(
        gid_arr, y, X, int(window), int(min_obs), float(ridge)
    )

    cols = {
        id_col: merged[id_col].to_numpy(copy=False),
        date_col: merged[date_col].to_numpy(copy=False),
    }
    for j, c in enumerate(factor_cols):
        cols[f"beta_{c}"] = betas_arr[:, j + 1]

    cols["sigma_total"] = sig_tot
    cols["sigma_idio"] = sig_idi
    cols["adj_r2"] = r2

    out = pd.DataFrame(cols)

    if include_alpha:
        out["alpha"] = betas_arr[:, 0]

    return out
