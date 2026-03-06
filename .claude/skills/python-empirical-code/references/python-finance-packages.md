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

## requirements.txt template

```
pandas>=2.0
numpy>=1.24
matplotlib>=3.7
seaborn>=0.12
statsmodels>=0.14
linearmodels>=5.3
scipy>=1.10
wrds>=3.1
```

## Key API patterns

### linearmodels

```python
# Panel OLS
from linearmodels.panel import PanelOLS
# Must set multi-index: df.set_index(['entity', 'time'])
model = PanelOLS.from_formula('y ~ x + EntityEffects + TimeEffects', data=df)
result = model.fit(cov_type='clustered', cluster_entity=True)

# Fama-MacBeth
from linearmodels.asset_pricing import FamaMacBeth
model = FamaMacBeth.from_formula('ret ~ x1 + x2', data=df)
result = model.fit(cov_type='kernel', bandwidth=6)

# IV
from linearmodels.iv import IV2SLS
model = IV2SLS.from_formula('y ~ x2 + [x1 ~ z1 + z2]', data=df)
```

### statsmodels

```python
import statsmodels.formula.api as smf

# OLS with formula
result = smf.ols('y ~ x1 + x2 + C(industry)', data=df).fit()

# Clustered SEs
result_cl = result.get_robustcov_results(cov_type='cluster', groups=df['firm_id'])

# Logit/Probit
result = smf.logit('default ~ ltv + dti + fico', data=df).fit()

# Newey-West
result = smf.ols('y ~ x', data=df).fit(cov_type='HAC', cov_kwds={'maxlags': 6})
```

## Common pitfalls

- `linearmodels` requires a MultiIndex (entity, time) — set it before estimation
- `statsmodels` formula API uses `C()` for categorical variables, not `pd.Categorical`
- Newey-West in statsmodels: use `cov_type='HAC'`, not `'newey-west'`
- `wrds.Connection()` reads credentials from `~/.pgpass` — set up once
- `geopandas` spatial joins require matching CRS — always check with `.crs`
- `polars` syntax differs significantly from pandas — don't mix in the same script
