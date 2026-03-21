---
name: asset-pricing-test-suite
description: "Run the core workflow for empirical asset-pricing papers. Use for anomalies, factors, portfolio sorts, alphas, Fama-MacBeth tests, turnover, and validation."
---

# Asset Pricing Test Suite

Use this skill for signal, anomaly, factor, or return-predictability papers.

## Workflow

1. Define the signal exactly — variable name, source, construction, and economic rationale.
2. Specify timing: signal observation date, portfolio formation date, holding period, skip period, and rebalancing frequency.
3. Choose breakpoints (NYSE percentiles preferred) and weighting conventions (value-weighted preferred, equal-weighted as robustness).
4. Build the portfolio-sort logic (univariate, bivariate independent, bivariate dependent).
5. Choose benchmark factor models for alpha attribution.
6. Plan cross-sectional tests if needed.
7. Assess implementability: turnover, capacity, liquidity, and trading costs.
8. Separate discovery evidence from validation evidence.

## Factor model benchmarks

Use the appropriate benchmarks for the paper's contribution:

| Model | Factors | When to use |
|---|---|---|
| CAPM | MKT | Baseline only |
| Fama-French 3 | MKT, SMB, HML | Legacy benchmark |
| Carhart 4 | MKT, SMB, HML, UMD | When momentum exposure matters |
| Fama-French 5 | MKT, SMB, HML, RMW, CMA | Current standard for most papers |
| Fama-French 6 | FF5 + UMD | When momentum is relevant |
| q-factor (HXZ) | MKT, ME, I/A, ROE | Alternative to FF5; investment-based |
| q5 | q-factor + expected growth | Most recent HXZ model |
| Mispricing factors (Stambaugh-Yuan) | MKT, SMB, MGMT, PERF | When testing behavioral vs. rational |
| DHS 3-factor | MKT, FIN, PEAD | Behavioral benchmark |

Report at minimum: CAPM, FF3, FF5, and one of q-factor or FF6. If the signal is behavioral, add mispricing factors.

## Standard test families

### Portfolio sorts
- Univariate sorts: typically quintiles or deciles using NYSE breakpoints
- Long-short portfolio: long top quintile/decile, short bottom
- Report: mean excess returns, alphas against each model, t-statistics (Newey-West with appropriate lags)
- Bivariate sorts when needed to control for known predictors

### Time-series alpha regressions
- Regress long-short portfolio returns on factor models
- Report alpha, factor loadings, and adjusted R-squared
- Use Newey-West standard errors (lag = 0.75 * T^(1/3) or similar)
- GRS test for joint alpha significance across portfolios when relevant

### Cross-sectional tests
- Fama-MacBeth regressions: cross-sectional regression each month, then time-series average of coefficients
- Report Newey-West adjusted t-statistics for the time-series average
- Include standard controls: size, book-to-market, momentum, profitability, investment
- Alternatively: characteristic-sorted portfolio spanning tests

### Factor spanning / redundancy
- If proposing a new factor: does it survive when added to existing models?
- Test whether the new factor's alpha is significant controlling for existing factors
- Test whether existing anomalies' alphas are reduced when the new factor is added
- Maximum Sharpe ratio tests (Barillas and Shanken 2018)

## Implementability assessment

This section is mandatory. A signal with a large alpha but no implementable strategy is an incomplete paper.

- **Turnover**: Report monthly portfolio turnover. Above 50%/month is a red flag.
- **Capacity**: Is the strategy concentrated in microcaps? Report the fraction of long-short return from stocks below NYSE 20th percentile.
- **Microcap exclusion**: Re-run the main test excluding microcaps (typically below NYSE 20th percentile or $100M market cap). If the result vanishes, flag this prominently.
- **Liquidity**: Report the average bid-ask spread and Amihud illiquidity of the long and short legs.
- **Trading costs**: Use at minimum a simple proportional cost model. Consider Novy-Marx and Velikov (2016) or DeMiguel et al. (2020) for more sophisticated cost estimation.
- **Short-leg feasibility**: Is the short leg composed of hard-to-borrow stocks? Check against shorting-fee data if available.

## Validation and replication concerns

- **Out-of-sample**: Test in a holdout time period (pre-discovery or post-publication).
- **International**: Test in international markets if data permit.
- **Post-publication decay**: If replicating a known anomaly, report post-publication performance.
- **Data snooping**: If many signals were searched, address multiple-testing risk (Harvey, Liu, and Zhu 2016 t-statistic threshold of ~3.0; Chordia, Goyal, and Saretto 2020).
- **Anomaly zoo context**: Position the signal relative to the Chen-Zimmermann (2022) open-source asset pricing project and existing anomaly databases.
- **Machine learning complement**: See the "Machine learning robustness" section below for the full ML test battery. At minimum, assess variable importance and incremental R-squared.

## Machine learning robustness

Modern anomaly papers increasingly require ML benchmarks. This section is recommended (not mandatory) for papers proposing new signals or factors, and optional for papers focused on mechanism or institutional explanation.

### When to include ML tests

- **Required**: The paper's primary contribution is a new return predictor or anomaly
- **Recommended**: The signal is a constructed variable that could plausibly be captured by nonlinear combinations of known characteristics
- **Optional**: The paper's contribution is mechanism or institutional, not the signal itself

### Standard ML benchmark tests

#### 1. Variable importance analysis

Use tree-based models to assess whether the proposed signal has incremental predictive power beyond known characteristics:

```python
import lightgbm as lgb
from sklearn.inspection import permutation_importance
import numpy as np
import pandas as pd

# Panel of firm-month observations with characteristics and future returns
# X: N x K matrix of known characteristics + the new signal
# y: next-month excess returns

model = lgb.LGBMRegressor(
    n_estimators=500,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    min_child_samples=100,
    reg_alpha=0.1,
    reg_lambda=0.1,
    random_state=42,
    n_jobs=-1
)

# Train on expanding window (no future data leakage)
# For each month t, train on months 1..t-1, predict month t
predictions = []
for t in sorted(df['date'].unique())[120:]:  # start after 10-year burn-in
    train = df[df['date'] < t]
    test = df[df['date'] == t]
    model.fit(train[features], train['ret_excess'])
    pred = model.predict(test[features])
    predictions.append(pd.DataFrame({
        'date': t, 'permno': test['permno'].values, 'pred': pred
    }))

# Feature importance: both built-in (split-based) and permutation
importance_split = pd.Series(
    model.feature_importances_, index=features
).sort_values(ascending=False)

perm_imp = permutation_importance(
    model, X_test, y_test, n_repeats=10, random_state=42
)
importance_perm = pd.Series(
    perm_imp.importances_mean, index=features
).sort_values(ascending=False)
```

**What to report**: Rank of the new signal in both split-importance and permutation-importance. If the signal ranks in the top 10 of 50+ characteristics, it has meaningful predictive content. If it does not appear in the top 20, the signal may be subsumed by known predictors in a nonlinear model.

#### 2. Incremental R-squared test

Compare out-of-sample R-squared (Campbell and Thompson 2008) with and without the new signal:

```python
from sklearn.metrics import r2_score

# R_oos^2 = 1 - sum((r_t - r_hat_t)^2) / sum((r_t - r_bar)^2)
# where r_bar is the expanding-window historical mean

def oos_r2(actual, predicted, hist_mean):
    ss_res = np.sum((actual - predicted) ** 2)
    ss_tot = np.sum((actual - hist_mean) ** 2)
    return 1 - ss_res / ss_tot

# Run two models: with and without the new signal
r2_with = oos_r2(y_test, pred_with_signal, hist_mean)
r2_without = oos_r2(y_test, pred_without_signal, hist_mean)
delta_r2 = r2_with - r2_without
# A positive delta_r2 of even 0.1-0.5% is economically meaningful at monthly frequency
```

**What to report**: Out-of-sample R-squared with and without the signal. The difference (Delta R-squared). Even a 0.1-0.5% improvement at monthly frequency is economically meaningful (Gu, Kelly, and Xiu 2020).

#### 3. Partial dependence and interaction effects

Show how the signal's marginal effect varies across its range and interacts with other characteristics:

```python
from sklearn.inspection import PartialDependenceDisplay

# Partial dependence plot for the new signal
fig, ax = plt.subplots(figsize=(6.5, 4.5))
PartialDependenceDisplay.from_estimator(
    model, X_test, features=[signal_col],
    ax=ax, line_kw={'color': 'black'}
)
ax.set_xlabel('Signal value')
ax.set_ylabel('Predicted excess return')
ax.set_title('')
fig.savefig('output/figures/fig_pdp_signal.pdf', dpi=300, bbox_inches='tight')

# 2D interaction: signal x size (to check if the effect is microcap-driven)
fig, ax = plt.subplots(figsize=(6.5, 4.5))
PartialDependenceDisplay.from_estimator(
    model, X_test, features=[(signal_col, 'log_me')],
    ax=ax
)
fig.savefig('output/figures/fig_pdp_signal_size.pdf', dpi=300, bbox_inches='tight')
```

**What to report**: Partial dependence plot showing monotonicity (or non-monotonicity) of the signal-return relationship. 2D interaction plot with size to verify the effect is not concentrated in microcaps.

#### 4. Signal persistence after ML filtering

The strongest evidence for a signal's economic content: does it predict returns even after controlling for the ML model's predictions?

```python
# Double-sort: first sort on ML-predicted return, then on the new signal within each ML quintile
df['ml_pred_quintile'] = df.groupby('date')['ml_predicted_return'].transform(
    lambda x: pd.qcut(x, 5, labels=False, duplicates='drop')
)
df['signal_quintile'] = df.groupby(['date', 'ml_pred_quintile'])[signal_col].transform(
    lambda x: pd.qcut(x, 5, labels=False, duplicates='drop')
)

# If the signal still predicts returns within ML quintiles,
# it contains information the ML model does not capture
```

**What to report**: Long-short returns within each ML-predicted-return quintile. If the signal's spread persists, it captures economic content beyond what flexible ML models extract from known characteristics.

### ML model specifications

Use these defaults unless the paper's context requires otherwise:

| Model | Use case | Key hyperparameters |
|---|---|---|
| LightGBM / XGBoost | Primary benchmark | max_depth=4, n_estimators=500, learning_rate=0.05 |
| Random forest | Robustness | max_depth=6, n_estimators=500 |
| Elastic net | Linear benchmark | alpha=0.01, l1_ratio=0.5 |
| Neural network | If paper claims nonlinear effects | 3 hidden layers (32-16-8), dropout=0.1, batch_norm |

### Training protocol (to avoid look-ahead bias)

- **Expanding window only**: train on months 1..t-1, predict month t. Never use future data.
- **Minimum burn-in**: 10 years (120 months) of training data before first prediction.
- **Feature set**: Use the standard Gu-Kelly-Xiu (2020) 94-characteristic set as the baseline, plus the new signal.
- **Cross-validation for hyperparameters**: Use time-series cross-validation (e.g., 5-fold with expanding windows), never random splits.
- **No survivorship bias**: Include delisted firms with proper return adjustment.

### Interpretation guidance

- If the signal ranks highly in variable importance AND has incremental R-squared AND survives the double-sort: the signal contains genuine economic information. The paper's contribution is secure.
- If the signal ranks highly but does NOT survive the double-sort: the signal is captured by nonlinear combinations of known characteristics. The paper must pivot to economic interpretation (why does this combination matter?) rather than claiming a new predictor.
- If the signal does NOT rank highly: the signal may have economic content that is too noisy for ML to capture, or the signal may be weak. Report honestly and focus the contribution on the economic mechanism, not the predictive power.

### References for ML in asset pricing
- Gu, Kelly, and Xiu (2020) "Empirical Asset Pricing via Machine Learning" RFS
- Gu, Kelly, and Xiu (2021) "Autoencoder Asset Pricing Models" JFE
- Chen, Pelger, and Zhu (2024) "Deep Learning in Asset Pricing" Management Science
- Freyberger, Neuhierl, and Weber (2020) "Dissecting Characteristics Nonparametrically" RFS
- Avramov, Cheng, and Metzker (2023) "Machine Learning vs. Economic Restrictions" Management Science

## Tool integration (Corbis MCP)

### Signal novelty verification (mandatory before proceeding)
1. `search_papers` (query: the signal name + "return predictability" or "cross-section of returns", `matchCount: 15`) → check whether the signal or a close variant has been documented.
2. `search_papers` (query: the economic mechanism behind the signal, `matchCount: 10`) → find papers with different signals but the same mechanism.
3. `get_paper_details` (paper IDs from top results) → read abstracts to determine true overlap vs. superficial similarity.

### Anomaly zoo context
- `top_cited_articles` (field: "asset pricing", topic: "anomalies" or "return predictability") → identify the canonical papers the user must cite and benchmark against.

### Macro conditioning variables
- `fred_search` (keywords like "investor sentiment" or "market volatility") → find series for conditional tests.
- `fred_series_batch` (series IDs, e.g., `["VIXCLS","BAMLC0A0CM","T10Y2Y","UMCSENT"]`) → pull conditioning variables for time-series variation tests.

### Literature for methodology
- `search_papers` (query: specific methodology, e.g., "Fama-MacBeth Newey-West", `minYear: 2018`) → find recent applied examples of the testing framework.
- `export_citations` (format: `bibtex`) → export BibTeX entries for methodological and anomaly-zoo references cited in the test matrix and contribution statement (e.g., Harvey-Liu-Zhu, Chen-Zimmermann, Gu-Kelly-Xiu). Offer this after the test matrix is produced.
- `format_citation` → format individual references for the anomaly-positioning discussion.

## LaTeX output — write to `.tex` files

Follow the float format specified in CLAUDE.md. Before first use, read `latex_template/academic_paper_template.tex` for the template's custom commands. Write tables to `output/tables/*.tex` and figure wrappers to `output/figures/*.tex`. Use `utils.table_utils.reg_to_latex()` for programmatic table generation and `utils.regression_utils.portfolio_sort()` / `alpha_table()` for the core AP tests.

## Deliverables

Produce:
- an asset-pricing test matrix using assets/ap-test-matrix-template.md
- a table and figure plan
- a statement of the likely contribution and how it advances the literature
- a list of standard objections with pre-planned responses
- suggested Stata/R/Python code structure for the main tests
- ML robustness assessment (variable importance, incremental R-squared, partial dependence) when the contribution is a new signal

## Output format

```
# Asset-pricing analysis plan
## Signal definition (exact formula, source, timing)
## Construction choices (breakpoints, weighting, rebalancing)
## Baseline return tests (univariate sorts)
## Factor benchmark tests (alphas against each model)
## Cross-sectional pricing tests (Fama-MacBeth)
## Factor spanning / redundancy tests
## Implementability checks (turnover, capacity, microcaps, costs)
## Validation checks (out-of-sample, international, post-publication)
## Data-snooping assessment
## ML robustness (if applicable: variable importance, incremental R², PDP, double-sort)
## Interpretation limits
```

## Reference files
Read if needed:
- references/asset-pricing-norms.md
- references/writing-norms.md

## Guardrails

- Do not treat a highly significant alpha as economically meaningful without discussing implementability.
- Do not mix discovery and validation samples casually.
- Be explicit about microcap exposure, liquidity, and turnover.
- If many signals were searched, address multiple-testing risk — a t-statistic of 2.0 is not enough.
- Do not claim a new "factor" without spanning tests showing it is not redundant to existing factors.
- Do not ignore the post-2004 decline in many anomalies.
- Flag when results are driven primarily by the short leg, which is harder to implement.

## Example prompts
- "Design the full empirical test suite for this new characteristic."
- "How should I validate an anomaly after 2003?"
- "What tables does an empirical factor paper need?"
- "Is my signal just a relabeled version of profitability?"
- "Assess the implementability of this high-turnover strategy."
