# Empirical Asset Pricing Norms

## Core objects
- Signal definition: exact variable, source, and construction formula
- Breakpoints and sort construction: NYSE percentiles preferred; specify equal- vs. value-weighted
- Holding period (typically 1 month) and skip period (if any)
- Long-short return series: long top decile/quintile, short bottom
- Time-series alpha tests against multiple factor models
- Cross-sectional pricing tests (Fama-MacBeth)
- Economic implementability assessment

## Factor model benchmarks (current standards)
- CAPM: baseline, insufficient alone
- Fama-French 3-factor: legacy benchmark
- Carhart 4-factor: when momentum exposure relevant
- Fama-French 5-factor: current default standard (MKT, SMB, HML, RMW, CMA)
- Fama-French 6-factor: FF5 + momentum
- q-factor model (Hou, Xue, Zhang): investment-based alternative (MKT, ME, I/A, ROE)
- q5 model: q-factor + expected growth
- Stambaugh-Yuan mispricing factors: behavioral benchmark (MKT, SMB, MGMT, PERF)
- Daniel-Hirshleifer-Sun: behavioral 3-factor (MKT, FIN, PEAD)
- At minimum report: CAPM, FF3, FF5, and q-factor or FF6

## Default checks
- NYSE breakpoints where appropriate (avoid microcap-driven results)
- Microcap sensitivity: exclude stocks below NYSE 20th percentile
- Liquidity and trading-cost discussion: bid-ask spread, Amihud illiquidity
- Turnover and implementability: monthly turnover rate, capacity estimates
- Delisting returns: use CRSP delisting returns, not just last trading day
- Standard factor benchmarks for alpha attribution (see above)
- Out-of-sample or post-publication checks when relevant
- Multiple-testing awareness: Harvey-Liu-Zhu (2016) suggest t > 3.0 threshold when many signals searched
- Anomaly zoo context: position relative to Chen-Zimmermann (2022) replication project

## Data snooping and replication crisis
- Hundreds of published anomalies; many fail out-of-sample or post-publication
- Chordia, Goyal, and Saretto (2020): most anomalies weakened after accounting for trading costs and data-mining adjustments
- McLean and Pontiff (2016): average anomaly returns decline ~58% post-publication
- A new signal must clear a higher bar than the historical t > 2.0 standard
- If the paper tests multiple signals, apply formal multiple-testing corrections

## Machine learning context
- Gu, Kelly, and Xiu (2020): ML methods can capture substantial cross-sectional return predictability
- A new characteristic should be assessed against ML-based expected return models
- If ML subsumes the signal, the contribution must come from economic interpretation, not prediction alone
- Consider variable importance measures from ML models as supporting evidence

## Reporting
- Explain exactly how the signal is lagged and standardized
- Show portfolio construction choices clearly
- Separate in-sample discovery from validation
- Discuss whether the effect survives reasonable implementation frictions
- Do not equate a strong t-statistic with a tradable strategy unless implementability is addressed
- Report both value-weighted and equal-weighted results (VW is harder to pass and more economically meaningful)
