# Python Packages for Empirical Finance

## Core stack

| Package | Version | Purpose |
|---|---|---|
| `pandas` | >= 2.0 | Data manipulation, panel data |
| `numpy` | >= 1.24 | Numerical operations |
| `matplotlib` | >= 3.7 | Publication figures |
| `seaborn` | >= 0.12 | Statistical visualization |
| `statsmodels` | >= 0.14 | Cross-sectional regressions, diagnostics |
| `linearmodels` | >= 5.3 | Panel regressions (FE, IV, Fama-MacBeth) |
| `scipy` | >= 1.10 | Statistical tests, distributions |

## Specialized

| Package | Purpose | When needed |
|---|---|---|
| `wrds` | WRDS PostgreSQL access | Data download |
| `lifelines` | Survival analysis (Cox PH, KM) | Hazard models, mortgage default |
| `csdid` | Callaway-Sant'Anna staggered DiD | Modern DiD |
| `geopandas` | Spatial data, shapefiles | Real estate spatial designs |
| `libpysal` / `spreg` | Spatial weights, Conley SEs | Spatial inference |
| `pyarrow` / `polars` | Fast data processing | Large datasets (TRACE, TAQ, property records) |
| `stargazer` | Regression table formatting | Quick LaTeX tables |
| `sklearn` | Machine learning | ML-based anomaly detection, prediction |
| `arch` | GARCH, volatility models | Time-series finance |
| `pyblp` | BLP demand estimation | Structural IO/RE |

## Common pitfalls

- `linearmodels` requires a MultiIndex (entity, time) — set it before estimation
- `statsmodels` formula API uses `C()` for categorical variables, not `pd.Categorical`
- Newey-West in statsmodels: use `cov_type='HAC'`, not `'newey-west'`
- `wrds.Connection()` reads credentials from `~/.pgpass` — set up once
- `geopandas` spatial joins require matching CRS — always check with `.crs`
- `polars` syntax differs significantly from pandas — don't mix in the same script
