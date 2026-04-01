---
name: paper-elevator
description: "Read an academic paper and identify missing tests, analyses, and conceptual elements that would elevate it toward acceptance at a top finance or real-estate journal. Use when a draft is 'done' but needs to become top-journal ready."
---

# Paper Elevator: What Else Does This Paper Need?

Read a working draft and produce a prioritized gap report: what empirical tests, robustness checks, conceptual elements, and structural improvements are missing that would materially increase the probability of acceptance at a top finance or real-estate journal.

## When to use this skill

- The paper has a baseline result and some robustness, but you want to know what a top-journal referee would still ask for
- You are transitioning from "working paper" to "submission-ready"
- You want to audit the test battery before sending to coauthors or presenting at a seminar
- A referee gave a vague "needs more work" signal and you want to anticipate specific requests

## First move

1. **Determine what to read.** If a `.tex` file or PDF exists, read it. If not, ask the user for: (a) the research question in one sentence, (b) the identification strategy, (c) the list of current tables and figures with one-line descriptions, and (d) the target journal track (finance or RE).

2. **Check project state.** Read `notes/project_state.md` if it exists to pick up the identification strategy, threat map, literature positioning, and analysis status from prior skill invocations.

3. **Read the paper.** If a `.tex` file is available, read it section by section. Extract:
   - The research question and main hypothesis
   - The identification strategy (DiD, IV, RD, event study, portfolio sorts, hedonic, etc.)
   - Treatment timing (staggered or single-period)
   - The current table inventory (what each table tests)
   - The current figure inventory
   - The mechanism story and competing channels mentioned
   - The robustness checks already performed
   - The contribution claims
   - Whether a theoretical or conceptual framework exists

## Paper classification

Classify the paper on four dimensions before generating recommendations:

### A. Paper type
| Type | Signature features |
|---|---|
| Corporate finance | Firm-level panel, investment/financing/payout outcomes, governance or contracting |
| Asset pricing | Return predictability, anomalies, factors, portfolio sorts |
| Banking / financial intermediation | Lending, deposits, bank behavior, regulation |
| Household finance | Mortgage, savings, portfolio choice, behavioral |
| Real estate (property markets) | Transactions, prices, hedonic, spatial, zoning |
| Real estate (commercial) | Cap rates, REITs, leasing, CRE markets |
| Housing / urban economics | Affordability, mobility, neighborhoods, policy |
| Market microstructure | Trading, liquidity, price discovery |

### B. Identification strategy
DiD (single-period), DiD (staggered), IV, RD, boundary RD, event study (corporate), event study (asset pricing), portfolio sorts, structural estimation, descriptive/reduced-form, synthetic control, shift-share

### C. Target track
- **Finance track** (JF, JFE, RFS, JFQA, RoF): Expects broad contribution, sharp identification, mechanism depth
- **Real-estate track** (REE, JREFE, JRER, JHE, RSUE): Expects institutional detail, spatial awareness, data transparency

### D. Current completeness
Rate each area as: present / partial / missing

| Area | Check for |
|---|---|
| Summary statistics | Means, SDs, N, panel structure |
| Sample construction | Filters documented, observation counts at each step |
| Baseline result | Main specification with preferred controls and FE |
| Magnitude interpretation | Economic magnitude in real units, not just statistical significance |
| Robustness (specification) | Alternative controls, FE, functional form |
| Robustness (sample) | Subsamples, time periods, outlier sensitivity |
| Robustness (identification) | Placebo, falsification, pretrends, instrument diagnostics |
| Robustness (inference) | Alternative clustering, Conley SEs, bootstrap |
| Mechanism tests | Tests that distinguish competing channels |
| Heterogeneity | Cross-sectional splits with prior motivation |
| Conceptual framework | Theory, simple model, or structured predictions |
| Literature positioning | Specific differentiation from closest 2-3 papers |
| Magnitude benchmarking | Comparison to related estimates in the literature |

---

## Gap analysis: five layers

Work through each layer. For each missing item, classify it as **Must-have**, **Expected**, or **Elevating**.

### Layer 1: Universal requirements

Every empirical paper, regardless of type or design:

| Test / Element | Must / Expected / Elevating | Notes |
|---|---|---|
| Summary statistics table | Must-have | With means, SDs, percentiles, N |
| Sample construction documentation | Must-have | Observation counts at each filter step |
| Economic magnitude in real units | Must-have | Three-tier: statistical → real-world → anchored comparison |
| Comparison to related estimates | Expected | "Our estimate of X% is [larger/smaller/comparable] to Y (2020) who find Z%" |
| Variable definitions table | Expected | In appendix if not in text |
| Correlation matrix or pairwise correlations | Expected | For key variables, especially if multicollinearity is a concern |
| Data availability statement | Expected | Increasingly required; describe access path |
| Internet Appendix for overflow | Expected | If main paper exceeds target length |

### Layer 2: Design-specific requirements

#### Difference-in-differences (single-period)
| Test | Priority | What it shows |
|---|---|---|
| Parallel pretrends (event-study plot) | Must-have | Pre-treatment coefficients insignificant and flat |
| Pretrend test (joint F-test on pre-period coefficients) | Must-have | Statistical test, not just visual |
| Placebo treatment timing | Expected | Fake the treatment date; should find no effect |
| Placebo treatment group | Expected | Apply treatment to untreated group; should find no effect |
| Roth (2022) pretrends sensitivity | Elevating | Honest power analysis for pretrends; bounds on bias |
| Oster (2019) bounds (delta) | Elevating | Coefficient stability to unobservables; report delta |

#### Difference-in-differences (staggered)
All of the above, plus:
| Test | Priority | What it shows |
|---|---|---|
| Modern estimator (Callaway-Sant'Anna or Sun-Abraham) | Must-have | TWFE is biased with staggered timing; must use or justify not using |
| Cohort-specific treatment effects | Expected | Heterogeneity across adoption cohorts |
| Bacon decomposition | Expected | Shows which 2x2 comparisons drive the TWFE estimate |
| Goodman-Bacon or de Chaisemartin-D'Haultfoeuille diagnostics | Expected | Quantify potential TWFE bias |
| Never-treated vs. last-treated comparison | Elevating | Robustness to control group definition |

#### Instrumental variables
| Test | Priority | What it shows |
|---|---|---|
| First-stage F-statistic | Must-have | Instrument relevance; report effective F (Olea-Pflueger) not just Cragg-Donald |
| Reduced-form estimate | Must-have | Direct effect of instrument on outcome |
| Exclusion restriction discussion | Must-have | Prose argument; cannot be tested directly |
| Overidentification test (if multiple instruments) | Expected | Hansen J; fails if instruments are invalid |
| Instrument exogeneity / balance test | Expected | Instrument uncorrelated with observables |
| Anderson-Rubin confidence set | Elevating | Robust to weak instruments |
| Plausibly exogenous (Conley et al. 2012) | Elevating | Bounds allowing partial violation of exclusion |
| Lee et al. (2022) tF procedure | Elevating | Weak-instrument robust inference |

#### Regression discontinuity
| Test | Priority | What it shows |
|---|---|---|
| McCrary (2008) density test | Must-have | No manipulation of the running variable |
| Bandwidth sensitivity | Must-have | Results robust to alternative bandwidths (0.5x, 1.5x, 2x optimal) |
| Local polynomial plot | Must-have | Visual of the discontinuity |
| Covariate balance at the cutoff | Expected | Predetermined covariates smooth through the cutoff |
| Placebo cutoffs | Expected | No effect at non-cutoff values |
| Donut-hole RD | Expected | Exclude observations closest to cutoff; addresses heaping |
| CCT (Calonico, Cattaneo, Titiunik) optimal bandwidth | Expected | Modern bandwidth selection |
| Higher-order polynomial robustness | Elevating | Linear, quadratic, cubic local polynomials |

#### Event study (corporate events)
| Test | Priority | What it shows |
|---|---|---|
| CAR with appropriate benchmark | Must-have | Market model, FF3, or matched-firm returns |
| Cross-sectional regression of CARs | Must-have | What predicts announcement returns |
| Event clustering adjustment | Expected | Calendar-time portfolio or bootstrap if events cluster |
| Long-run returns (BHAR or DGTW) | Expected | Post-event drift or reversal |
| Confounding events filter | Expected | Exclude firms with other news in the event window |

#### Portfolio sorts (asset pricing)
| Test | Priority | What it shows |
|---|---|---|
| Univariate sorts with NYSE breakpoints | Must-have | Raw return spreads |
| Alphas against FF5 + one alternative model | Must-have | Risk-adjusted returns |
| Fama-MacBeth cross-sectional regressions | Must-have | Signal predicts returns controlling for known predictors |
| Bivariate sorts controlling for size, value, momentum | Expected | Signal not subsumed by known characteristics |
| Implementability (turnover, capacity, microcap exclusion) | Expected | Can you actually trade this? |
| GRS test | Expected | Joint test of alpha significance |
| Factor spanning test | Expected | If proposing a new factor |
| ML robustness (variable importance, incremental R-squared) | Elevating | Signal not captured by nonlinear combinations |
| International or out-of-sample test | Elevating | Generalizability |

#### Hedonic / repeat-sales (real estate)
| Test | Priority | What it shows |
|---|---|---|
| Spatial fixed effects (census tract, ZIP, neighborhood) | Must-have | Absorb unobserved location heterogeneity |
| Time fixed effects (year-quarter or year-month) | Must-have | Absorb market-wide trends |
| Property characteristics controls | Must-have | Bedrooms, bathrooms, sqft, age, lot size |
| Repeat-sales specification (if feasible) | Expected | Controls for time-invariant property quality |
| Spatial clustering (Conley SEs or cluster at geography) | Expected | Correct for spatial correlation |
| Distance-based heterogeneity | Expected | Effect gradient with distance from treatment |
| Sensitivity to property-type composition | Expected | Results hold for single-family, condos separately |
| Boundary discontinuity (if applicable) | Elevating | Sharp geographic variation |

### Layer 3: Paper-type-specific requirements

#### Corporate finance
| Element | Priority | Notes |
|---|---|---|
| Mechanism test separating competing channels | Expected | Not just heterogeneity relabeled as mechanism |
| Intermediate outcome on the causal path | Expected | If the effect goes through channel A, does the intermediate move? |
| Competing channel ruled out | Expected | Test for alternative explanation, show it does not explain the result |
| Within-firm variation (firm FE) | Expected | Rules out time-invariant firm confounds |
| Industry-time FE | Expected | Rules out industry-level shocks |
| Dynamic effects (event-time coefficients) | Expected | Treatment effect timing |

#### Asset pricing
| Element | Priority | Notes |
|---|---|---|
| Microcap exclusion | Must-have | Exclude NYSE bottom 20th percentile; does the signal survive? |
| Turnover and trading costs | Expected | Signal implementable after costs? |
| Short-leg feasibility | Expected | Is the short side tradeable? |
| Subsample stability (pre-2000, post-2000) | Expected | Signal not an artifact of one era |
| Signal persistence (1-month, 3-month, 12-month horizons) | Expected | How quickly does the signal decay? |
| Chen-Zimmermann anomaly zoo positioning | Elevating | Explicit comparison to known anomalies |

#### Real estate (property markets)
| Element | Priority | Notes |
|---|---|---|
| Map of treatment geography | Expected | Especially for spatial designs |
| Data construction transparency | Expected | RE journals expect more detail than finance journals |
| Appraisal vs. transaction price distinction | Expected | If using assessed values, discuss smoothing bias |
| Spatial autocorrelation diagnostic (Moran's I) | Expected | Document spatial dependence |
| Urban/suburban/rural heterogeneity | Expected | Treatment effects may vary by density |
| Competing land-use or zoning controls | Expected | For policy evaluations |

#### Banking / lending
| Element | Priority | Notes |
|---|---|---|
| Borrower vs. lender fixed effects | Expected | Separate demand from supply |
| Loan-level vs. bank-level results | Expected | Extensive vs. intensive margin |
| Regulatory threshold manipulation test | Expected | If design exploits a regulatory cutoff |
| Bank balance-sheet controls | Expected | Capital ratio, size, NPL ratio |

### Layer 4: Track-specific expectations

#### Finance track (JF, JFE, RFS, JFQA, RoF)
| Element | Priority | Notes |
|---|---|---|
| Broad contribution framing | Expected | Result must matter beyond the specific setting |
| Mechanism depth (2+ channel tests) | Expected | Especially at JFE |
| Clean execution with no loose ends | Expected | Especially at RFS |
| Magnitude in context of existing literature | Expected | How does this compare to known effects? |
| Simple model or conceptual framework | Elevating | Not required, but increasingly common at top journals; disciplines predictions |

#### Real-estate track (REE, JREFE, JHE, RSUE)
| Element | Priority | Notes |
|---|---|---|
| Institutional background section | Expected | RE journals expect more setting detail |
| Geographic coverage description | Expected | States, MSAs, counties; why this sample? |
| Spatial robustness (Conley, geographic clustering) | Expected | Standard for RE papers with spatial data |
| Maps or geographic figures | Expected | For spatial designs |
| Policy relevance paragraph | Expected | Especially at JHE and RSUE |

### Layer 5: Frontier tests (elevating regardless of design)

These signal that the authors are current with methodological developments. Include them when applicable.

| Test | When applicable | Reference |
|---|---|---|
| Oster (2019) bounds | Any observational study with controls | Reports delta: how large would selection on unobservables need to be to explain away the result |
| Roth (2022) pretrends sensitivity | Any DiD with pretrend tests | Honest power analysis; bounds on bias given observed pretrends |
| Callaway-Sant'Anna (2021) | Staggered DiD | Heterogeneity-robust estimator |
| Sun-Abraham (2021) | Staggered DiD | Interaction-weighted estimator |
| de Chaisemartin-D'Haultfoeuille (2020) | Staggered DiD | Diagnostic and alternative estimator |
| Andrews-Stock-Sun (2019) | Weak IV | Weak-instrument robust confidence sets |
| Goldsmith-Pinkham-Sorkin-Swift (2020) | Shift-share / Bartik IV | Rotemberg weights; which shares drive the estimate |
| Borusyak-Hull-Jaravel (2022) | Shift-share | Quasi-experimental approach to shift-share |
| Conley (1999) spatial HAC | Any spatial data | Correct SEs for spatial autocorrelation |
| AAIW (Abadie et al. 2023) clustering | When cluster count is small | Design-based vs. sampling-based inference |
| Lee et al. (2022) tF procedure | IV | Weak-instrument robust test |
| Coefficient stability plots | Any study with controls | Visual of how the coefficient moves as controls are added |

---

## Conceptual and structural gaps

Beyond empirical tests, check for missing conceptual elements:

### Simple model or framework
- **When needed**: Paper proposes a mechanism but has no formal structure. The mechanism generates multiple predictions, and a model would discipline which are testable.
- **Priority**: Elevating for finance track, less common at RE track
- **What to recommend**: A 2-3 page partial-equilibrium model that generates the key comparative statics. Does not need to be novel; can adapt an existing framework.
- **Signal**: "If you can write down the mechanism in 3 equations, the paper benefits. If you cannot, the mechanism may be underspecified."

### Competing channel structure
- **When needed**: Paper claims mechanism A but has not tested against mechanism B
- **Priority**: Expected at top finance journals
- **What to recommend**: Identify 2-3 alternative explanations. For each, state the differential prediction and propose a test.

### External validity discussion
- **When needed**: Design exploits a specific setting (one country, one regulation, one time period)
- **Priority**: Expected for broad-contribution papers
- **What to recommend**: Explicit discussion of what the setting-specific estimate tells us (or does not tell us) about the general phenomenon. Not a caveat paragraph; an analytical argument.

### Contribution precision
- **When needed**: The contribution paragraph is vague ("we add to the literature on X")
- **Priority**: Must-have
- **What to recommend**: Name the 2-3 closest papers. For each, state the exact dimension of differentiation: mechanism, identification, data, setting, implication, or magnitude.

### Heterogeneity with economic motivation
- **When needed**: Paper has no cross-sectional variation analysis, or has heterogeneity splits without prior motivation
- **Priority**: Expected
- **What to recommend**: 2-4 splits motivated by economic theory. Each split should have a stated prediction *before* the result: "If the effect operates through X, we expect it to be larger when Y is high."

---

## Output format

```
# Paper Elevator: Gap Report

## Paper diagnosis
- **Paper type**: [classification]
- **Identification strategy**: [method]
- **Target track**: [finance / real-estate]
- **Current test inventory**: [list what the paper already has]
- **Completeness rating**: [X/13 areas covered — from the completeness table]

## Must-have (paper will be rejected or R&R'd without these)
1. **[Test/element name]**
   - Why: [specific reason tied to the paper's design or claims]
   - Where it goes: [which section of the paper]
   - Effort: [low / medium / high]

## Expected (referees will likely ask; preempting saves a revision round)
1. **[Test/element name]**
   - Why: [specific reason]
   - Where it goes: [section]
   - Effort: [low / medium / high]

## Elevating (signals top-journal quality and methodological awareness)
1. **[Test/element name]**
   - Why: [what it signals to referees]
   - Where it goes: [section]
   - Effort: [low / medium / high]

## Conceptual gaps
1. **[Element name]**
   - Current state: [what the paper has now]
   - What's needed: [specific recommendation]
   - Priority: [must / expected / elevating]

## Not recommended (tests that would NOT add value)
- **[Test name]**: [Why it is not appropriate for this paper]

## Implementation priority
[Ordered list: what to do first based on impact/effort ratio]
1. [Highest impact, lowest effort first]
2. ...

## Next skill
[Which skill to invoke next: python-empirical-code for implementation, finance-identification-design for design revision, research-paper-writer for writing the new sections]
```

## Tool integration (Corbis MCP)

### Literature verification
- `search_papers` (query: the paper's main claim or method, `matchCount: 10`) → find recent papers that may have raised the bar for what is expected in this subfield
- `search_papers` (query: the identification strategy + "robustness", `minYear: 2020`) → find recent examples of state-of-the-art test batteries in comparable papers
- `get_paper_details` (closest papers) → verify what tests the closest papers included, to ensure parity

### Frontier methods
- `search_papers` (query: method name + "finance" or "real estate", `minYear: 2021`) → check whether a frontier method has been adopted widely enough to be expected vs. still optional

### Magnitude benchmarking
- `search_papers` (query: comparable empirical estimates) → find estimates from the literature to benchmark the paper's magnitudes against

## Process

1. Read the paper (or collect structured inputs from the user)
2. Classify: paper type, identification strategy, target track
3. Inventory: what tests and elements already exist
4. Run through all five layers + conceptual gaps
5. Deduplicate: if a test appears in multiple layers, keep the highest-priority classification
6. Remove tests that are not applicable to this paper
7. Prioritize by impact/effort
8. Produce the gap report
9. Log to `notes/lab_notebook.md`
10. Update `notes/project_state.md`

## Guardrails

- Do NOT recommend tests that do not map to a specific threat, design feature, or conceptual gap in this paper. Every recommendation must have a "why" tied to the paper.
- Do NOT recommend tests just because they are trendy. Oster bounds are not useful for an RD paper. ML robustness is not useful for a corporate finance paper. Match the test to the design.
- Do NOT inflate the list. A paper with 15 tables is too long. Recommend what to add AND what to move to the Internet Appendix if the paper is already dense.
- Do NOT recommend a simple model for papers where the mechanism is well-established and the contribution is empirical.
- Be honest about effort. If a recommended test requires new data or a fundamentally different estimation approach, say so.
- Account for what is already in the paper. If the paper already has pretrends, do not recommend pretrends. Read carefully.
- If the paper is conceptually weak (the question does not matter, the contribution is incremental), say so directly. No amount of additional tests will save a paper with a weak question. Flag this as the binding constraint.

## Example prompts
- `/what-else` (with a `.tex` file in the project)
- "What tests does my paper need to be competitive at JFE?"
- "Read my paper and tell me what's missing for a top RE journal."
- "I have a staggered DiD paper. What should I add before submitting to RFS?"
- "Audit my test battery and tell me what referees will ask for."
