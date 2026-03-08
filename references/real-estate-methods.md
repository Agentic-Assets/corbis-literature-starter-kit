# Real Estate Methods Notes

## Real estate specific design issues
- Distinguish listings, contracts, closings, assessments, appraisals, leases, and mortgages — each represents a different economic object and observation timing.
- Geography is not just a control. It is often part of the treatment assignment, the equilibrium, and the error structure.
- Spatial correlation can be first order, neighborhood level, market level, or policy-boundary based.
- Institutional detail matters: zoning, tax rules, lending constraints, brokerage practices, lease structure, appraisal conventions, and insurance markets.

## Common empirical designs

### Hedonic regressions
- Standard approach for valuing amenities and disamenities.
- Omitted variable bias is the primary concern — always discuss what unobserved factor could correlate with both X and price.
- Functional form: log-linear is default but test sensitivity.
- Spatial FE (tract, block group) absorb location-level unobservables.

### Repeat-sales designs
- Difference out time-invariant property characteristics.
- Assumptions: no renovation bias, non-selected transaction timing, constant quality.
- Case-Shiller weighted repeat-sales for index construction; unweighted for causal inference.
- Address: renovations (permit data), selected sample (comparison to non-transacted properties), and time between sales.

### Boundary discontinuity designs
- Ideal for school districts, zoning, tax jurisdictions, flood zones, opportunity zones.
- Key concerns: sorting across boundaries, bunching in density, bandwidth choice.
- Calonico-Cattaneo-Titiunik optimal bandwidth. McCrary/CCT density test for manipulation.
- Show balance on observables across the boundary.

### Spatial difference-in-differences
- Ring-based designs: varying distance from point source.
- Spatial spillovers can invalidate SUTVA — use donut-hole buffers.
- Modern DiD concerns apply: staggered timing, heterogeneous effects.
- Pre-treatment parallel trends in property values or other outcomes.

### Mortgage and borrower-level designs
- Competing risks: prepayment and default.
- Regulatory cutoffs create quasi-experimental variation: GSE conforming loan limits, QM thresholds, DTI/LTV/FICO cutoffs.
- Cox vs. discrete-time hazard; time-varying covariates.
- Selection into loan products is endogenous.

### Commercial real estate
- Cap rate decomposition: discount rate vs. cash flow expectations.
- Appraisal smoothing is severe — use transaction-based data when possible.
- REIT analysis: NAV discount/premium, capital structure, dividend policy.
- Lease-level: tenant quality, duration, escalation clauses, renewal options.

### Climate and environmental risk
- Flood zone reclassification, wildfire risk disclosure, sea-level rise expectations.
- Challenge: separating risk pricing from amenity valuation.
- Insurance market disruptions as natural experiments.
- Energy efficiency capitalization in property values.

## Measurement cautions
- Listing prices are not transaction prices.
- Appraisal-based values can be smoothed — Quan and Quigley (1991).
- Property characteristics change over time (renovations, deterioration).
- Geographic joins can induce substantial data loss or measurement error.
- Property identifiers are often messy and require hand auditing.
- Assessed values may not reflect market values (assessment ratio varies).
- Condo and multi-unit properties create unit-vs-property identification challenges.

## Spatial inference
- Conley (1999) spatial HAC standard errors for spatially correlated data.
- Cluster at the geographic level of the shock (tract, ZIP, county, MSA).
- Two-way clustering (geography x time) when both dimensions create dependence.
- Moulton (1990): cluster at the treatment level when treatment varies at a higher level than observations.
- Do not use standard OLS standard errors in property-level regressions without addressing spatial dependence.

## Reporting norms
- Make maps, institutional timelines, and local-market context do real analytical work — not decoration.
- Explain whether results are property-level, borrower-level, lender-level, neighborhood-level, or market-level.
- State clearly how repeat observations and spatial dependence are handled.
- Report the geographic scope and discuss external validity limitations.
- For hedonic regressions, discuss the implicit price interpretation.
