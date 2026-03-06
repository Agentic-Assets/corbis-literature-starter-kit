# Asset Pricing Test Matrix

## Signal definition
- **Variable name**:
- **Source**: [dataset and fields]
- **Construction formula**: [exact formula]
- **Economic rationale**: [why should this predict returns?]

## Breakpoints and portfolio rules
- **Breakpoint source**: [NYSE percentiles / all-stock percentiles]
- **Number of groups**: [quintiles / deciles]
- **Weighting**: [value-weighted (primary) / equal-weighted (robustness)]
- **Rebalancing frequency**: [monthly / quarterly / annual]
- **Holding period**: [1 month / 3 months / etc.]
- **Skip period**: [if any, and justification]

## Return horizon and lag structure
- **Signal observation date**: [when is the signal value known?]
- **Portfolio formation date**: [date of portfolio assignment]
- **Lag between signal and formation**: [to avoid look-ahead bias]
- **Return measurement period**: [t to t+1, etc.]

## Baseline factor benchmarks

| Model | Alpha | t-stat | Key factor loadings | Adj R-sq |
|---|---|---|---|---|
| CAPM | | | | |
| FF3 | | | | |
| Carhart 4 | | | | |
| FF5 | | | | |
| FF6 | | | | |
| q-factor (HXZ) | | | | |
| Mispricing (SY) | | | | |

## Time-series alpha tests
- **Long-short portfolio**: [top minus bottom quintile/decile]
- **Standard errors**: [Newey-West, lag = ]
- **GRS test**: [joint test across all portfolio groups]
- **Subsample alphas**: [pre/post split, pre/post-2004, etc.]

## Cross-sectional tests (Fama-MacBeth)

| Specification | Controls | Avg coefficient | NW t-stat | Avg N | Avg R-sq |
|---|---|---|---|---|---|
| Univariate | None | | | | |
| + Size, B/M | | | | | |
| + Momentum | | | | | |
| + Profitability, Investment | | | | | |
| Full controls | | | | | |

## Factor spanning / redundancy tests
- [ ] Does the new factor's alpha survive controlling for existing factors?
- [ ] Does adding the new factor reduce alphas of existing anomalies?
- [ ] Maximum Sharpe ratio comparison (Barillas-Shanken)

## Implementability and turnover
- **Monthly turnover**: [%]
- **Fraction of return from microcaps**: [% from stocks below NYSE 20th pctile]
- **Result excluding microcaps**: [alpha and t-stat]
- **Average bid-ask spread (long leg)**:
- **Average bid-ask spread (short leg)**:
- **Amihud illiquidity (long/short)**:
- **Net-of-cost return estimate**: [method and result]
- **Short-leg feasibility**: [are short-leg stocks hard to borrow?]

## Out-of-sample validation
- **Holdout period**: [dates]
- **Post-publication performance**: [if replicating known anomaly]
- **International evidence**: [if available]
- **Anomaly zoo check**: [relationship to Chen-Zimmermann database]

## Interpretation limits
- [What can the evidence claim?]
- [What alternative explanations remain?]
- [Risk-based vs. behavioral interpretation: which is more consistent with the evidence?]
