---
name: theoretical-model-builder
description: "Build theoretical models for finance and real-estate papers. Use for partial/general equilibrium, contract theory, search, signaling, and mechanism models. Includes mathematical consistency audit and empirical reasonableness checks."
---

# Theoretical Model Builder

Build simple, sharp theoretical models that generate testable predictions for empirical finance and real-estate papers. The model should clarify the mechanism, discipline the empirical design, and survive both mathematical scrutiny and common-sense plausibility checks.

## Core mandate

A model in an empirical paper is not a theory paper. It exists to (1) clarify the economic mechanism, (2) generate testable predictions that distinguish the proposed channel from alternatives, and (3) discipline the empirical specification. The model should be as simple as possible while doing all three jobs. If a two-period, two-agent setup suffices, do not build a continuous-time overlapping-generations economy.

## First move

Before building anything, answer four questions:

1. **What economic force are you modeling?** State the mechanism in one sentence, no math.
2. **What predictions must the model generate?** List the comparative statics or cross-sectional patterns the empirical tests need.
3. **What alternative mechanisms must the model rule out?** The model's value comes from generating predictions that competing stories cannot match.
4. **What is the simplest framework that delivers all three?** Match the mechanism to a modeling tradition (see framework menu below).

If the user already has empirical results, work backward: identify which results need theoretical grounding and build the minimal model that rationalizes the documented patterns while generating at least one additional testable prediction.

## Framework menu

Choose the simplest framework that delivers the needed predictions. Mixing elements across frameworks is common and fine.

| Framework | Use when | Canonical references |
|---|---|---|
| Two-period partial equilibrium | Default. Most empirical-finance models. Investment, payout, capital structure decisions under frictions | Stein (2003) survey approach |
| Real options | Irreversible investment, exercise timing, option value of waiting | Dixit and Pindyck (1994) |
| Contracting / moral hazard | Principal-agent problems, compensation, delegation, monitoring | Holmstrom (1979), Bolton and Dewatripont (2005) |
| Adverse selection / signaling | Information asymmetry drives outcomes, separating/pooling equilibria | Spence (1973), Akerlof (1970) |
| Search and matching | Bilateral matching with frictions (labor, housing, OTC markets) | Pissarides (2000), Duffie, Garleanu, Pedersen (2005) |
| Portfolio choice / asset pricing | Investor optimization, risk premia, demand-based pricing | Merton (1971), Campbell and Viceira (2002) |
| General equilibrium | When partial equilibrium misses important feedback (prices, quantities adjust) | Standard Arrow-Debreu, DSGE variants |
| Spatial equilibrium | Location choice, capitalization, sorting across locations | Rosen (1979), Roback (1982) |
| Dynamic games | Strategic interaction over time, entry/exit, competition | Fudenberg and Tirole (1991) |
| Mechanism design / auctions | Optimal institution design, auction formats, information revelation | Myerson (1981), Milgrom (2004) |

## Workflow

### Phase 1: Setup

1. **State the economic question** in plain English.
2. **Define agents**: who are they, what do they choose, what do they know?
3. **Define the timing**: number of periods, sequence of actions and information revelation. Draw the timeline.
4. **Define the friction or force**: what market imperfection, information asymmetry, behavioral bias, or institutional feature drives the result? Without a friction, there is usually no interesting prediction.
5. **Write the objective functions**: utility, profit, or value functions for each agent. State functional form assumptions (concavity, monotonicity, single-crossing) and why they are economically reasonable.
6. **Define the equilibrium concept**: Nash, subgame perfect, competitive, Bayesian, Walrasian. Justify the choice.

### Phase 2: Solution

1. **Solve the model** by working backward from the last period/stage.
2. **Characterize the equilibrium**: existence, uniqueness, interior vs. corner solutions.
3. **Derive comparative statics**: how do endogenous outcomes change with exogenous parameters? These are the testable predictions.
4. **Sign the derivatives** using the economic assumptions. If a sign is ambiguous, state the conditions under which it goes each way. Ambiguous signs are fine if they map to testable heterogeneity.
5. **State predictions in plain English** after each mathematical result. The prose should be self-contained: a reader who skips the math should still understand the prediction.

### Phase 3: Consistency audit

Run the full consistency audit (see section below). Fix any failures before proceeding.

### Phase 4: Empirical reasonableness check

Run the full reasonableness battery (see section below). Flag any concerns and either recalibrate or document the limitation.

### Phase 5: Mapping to empirics

1. **Prediction-to-test table**: map each comparative static to a regression specification, variable, and expected sign.
2. **Identify discriminating predictions**: which predictions distinguish this mechanism from the top 2-3 alternative stories? These are the high-value tests.
3. **Identify auxiliary predictions**: what else does the model predict that you did not originally set out to test? These strengthen the paper if confirmed and are honest to report if violated.
4. **Parameter interpretation**: which model parameters map to observable data? Which are calibrated? Which are estimated?
5. **State what the model does not explain**: every model has limits. Be explicit.

## Mathematical consistency audit

Run every check below after solving the model. Report results in a consistency table.

### Structural checks

| Check | What to verify | Common failure |
|---|---|---|
| **Budget / resource constraints bind** | Does every agent's constraint hold with equality (if claimed) or inequality (if slack)? Sum resource allocations across agents: do they equal the aggregate endowment? | Agents spend more than they have; resources created from nowhere |
| **Equilibrium conditions satisfied** | Substitute the solution back into each first-order condition, market-clearing condition, and incentive constraint. Do they all hold simultaneously? | FOC holds for agent A's problem but violates agent B's constraint |
| **Boundary conditions respected** | Are non-negativity constraints, limited-liability constraints, and participation constraints satisfied at the solution? Is the solution interior when claimed? | Negative quantities, negative prices, agents participating when IR is violated |
| **Second-order conditions** | Is the SOC satisfied (concavity of objective at the optimum)? For constrained problems, check bordered Hessian. | FOC gives a minimum, not maximum; saddle point |
| **Uniqueness / multiplicity** | If uniqueness is claimed, verify there are no other solutions. If multiplicity is expected, catalog all equilibria and state the selection criterion. | Uniquely characterized solution is actually one of several |
| **Comparative statics signs** | Differentiate the equilibrium conditions totally (implicit function theorem). Verify the sign of each comparative static follows from stated assumptions (concavity, single-crossing, etc.). Does the sign require assumptions beyond those already stated? | Claimed sign requires an unstated assumption |
| **Dimensional consistency** | Do units match on both sides of every equation? Dollars equal dollars, probabilities are between 0 and 1, rates are per-period consistent. | LHS is a level, RHS is a rate; probability exceeds 1 at extreme parameters |
| **Limiting / special cases** | Take each key parameter to 0, 1, or infinity. Does the model reduce to a known benchmark? (e.g., no friction → Modigliani-Miller, no information asymmetry → first-best) | Model gives nonsensical results when the friction disappears |
| **Existence of equilibrium** | Do standard fixed-point conditions hold (compactness, convexity of action spaces, continuity of payoffs)? For finite games, Nash existence is guaranteed; for infinite-dimensional problems, state the existence argument. | Existence is assumed but action space is unbounded or payoffs discontinuous |
| **Logical flow** | Does each step follow from the previous? Are there implicit assumptions smuggled between lines? | A derivation skips a step that actually requires a new assumption |

### Notation and presentation checks

| Check | What to verify |
|---|---|
| **Every symbol defined** | No variable appears in an equation before being defined in text |
| **No overloaded notation** | The same symbol is not used for two different objects |
| **Subscripts/superscripts consistent** | Agent indices, time indices, and state indices follow a fixed convention throughout |
| **Assumptions numbered and referenced** | Every assumption is labeled (A1, A2, ...) and comparative statics cite which assumptions they require |
| **Propositions state full conditions** | "Under Assumptions A1-A3, the equilibrium satisfies..." rather than "The equilibrium satisfies..." |

## Empirical reasonableness battery

After the model is mathematically consistent, stress-test it against real-world plausibility. Models that are internally correct but externally absurd will not survive a referee.

### Magnitude checks

| Check | How to do it |
|---|---|
| **Calibrate to data** | Assign reasonable values to key parameters (risk-free rate, default probability, return volatility, house price appreciation, etc.) from published sources or FRED. Compute the model's quantitative predictions. Are they in the right ballpark? |
| **Elasticity check** | Compute the implied elasticities from comparative statics. Are they within the range of published empirical estimates? A model that predicts investment elasticities of 5 when the literature finds 0.2-0.5 has a problem. |
| **Effect size sanity** | If the model predicts a 1 s.d. increase in X raises Y by Z, is Z plausible given prior evidence? Compare to the closest empirical paper. |
| **Monotonicity at extremes** | Push parameters to extreme but real-world-possible values. Does the model produce extreme but directionally sensible predictions, or does it blow up, reverse sign, or produce nonsensical magnitudes? |

### Economic plausibility checks

| Check | What to verify |
|---|---|
| **Agent behavior is rational given information** | Would a real economic agent (firm manager, investor, homebuyer) plausibly behave as the model assumes? If the model requires agents to perform complex calculations, is this a reasonable approximation of actual behavior? |
| **Timing is realistic** | Does the sequence of decisions match how the real market works? (e.g., firms set prices before observing demand, not after; borrowers apply for loans before learning the rate) |
| **Outside options are reasonable** | What happens if an agent opts out entirely? Is the participation constraint binding at plausible parameter values, or does it only bind in knife-edge cases? |
| **Prediction matches stylized facts** | The model should be consistent with well-established empirical regularities in the relevant literature. If it contradicts a known stylized fact, either the model needs adjustment or the contradiction itself is a contribution (which must be flagged explicitly). |
| **Partial equilibrium is justified (if used)** | If using partial equilibrium, are the price-taking and fixed-supply/demand assumptions reasonable? Could general-equilibrium feedback reverse the result? |
| **Comparative statics survive heterogeneity** | The model likely has a representative agent or homogeneous agents. Would the predictions hold (at least directionally) if agents were heterogeneous in the natural dimensions (wealth, risk aversion, information)? |

### Discriminating power checks

| Check | What to verify |
|---|---|
| **Alternative mechanisms** | List the top 2-3 alternative explanations. Does the model generate at least one prediction that these alternatives do not? If every prediction is also consistent with a simpler story, the model adds little. |
| **Necessary vs. sufficient** | Does the model show the mechanism is *sufficient* to generate the pattern, or that it is the *only* explanation? Be honest about which claim you are making. |
| **Null result interpretation** | If the key comparative static turned out to be zero in the data, would the model have a coherent interpretation, or would it simply be wrong? A good model accommodates both positive and null results through parameter values. |

## Consistency audit report format

```
# Model Consistency Audit

## Structural checks
| Check | Status | Notes |
|---|---|---|
| Budget constraints | PASS / FAIL | [details] |
| Equilibrium conditions | PASS / FAIL | [details] |
| Boundary conditions | PASS / FAIL | [details] |
| Second-order conditions | PASS / FAIL | [details] |
| Uniqueness | PASS / FAIL | [details] |
| Comparative statics signs | PASS / FAIL | [details] |
| Dimensional consistency | PASS / FAIL | [details] |
| Limiting cases | PASS / FAIL | [details] |
| Existence | PASS / FAIL | [details] |
| Logical flow | PASS / FAIL | [details] |

## Reasonableness checks
| Check | Status | Notes |
|---|---|---|
| Calibration magnitudes | PLAUSIBLE / CONCERN | [comparison to published estimates] |
| Elasticities | PLAUSIBLE / CONCERN | [range vs. literature] |
| Effect sizes | PLAUSIBLE / CONCERN | [benchmark comparison] |
| Extreme parameters | PLAUSIBLE / CONCERN | [behavior at boundaries] |
| Agent behavior | PLAUSIBLE / CONCERN | [realism assessment] |
| Timing | PLAUSIBLE / CONCERN | [market structure match] |
| Stylized fact consistency | PLAUSIBLE / CONCERN | [which facts, any contradictions] |
| PE justification | PLAUSIBLE / CONCERN / N/A | [GE feedback risk] |
| Heterogeneity robustness | PLAUSIBLE / CONCERN | [fragility to agent differences] |
| Discriminating predictions | STRONG / WEAK | [vs. top alternatives] |

## Summary
- Structural failures: [count]
- Reasonableness concerns: [count]
- Discriminating power: [STRONG / MODERATE / WEAK]
- Recommended fixes: [list]
```

## Writing the model section

When writing the model for the paper (coordinate with `research-paper-writer`):

1. **Lead with economics, not math.** Open the section with a plain-English description of the mechanism: who does what, why, and what friction drives the result. A reader should understand the story from the first two paragraphs alone.
2. **Setup subsection**: Define agents, timing, information, and objective functions. Use a timeline figure if the sequence has more than two stages.
3. **Equilibrium subsection**: State the equilibrium concept, solve, and characterize.
4. **Predictions subsection**: State each prediction as a numbered proposition. Each proposition should have: (a) the formal result, (b) a plain-English interpretation, and (c) the mapping to an empirical test. Group assumptions and reference them explicitly in proposition statements.
5. **Discussion subsection** (optional): extensions, limitations, relationship to existing models. Keep this short. If it exceeds one page, the model may be too complex.
6. **Notation conventions**: Follow the target journal's style. Use Greek letters for parameters, Latin letters for choice variables, subscripts for agents/time, superscripts for types/states. Define everything at first use.

### Common mistakes in model sections

- Writing a theory paper inside an empirical paper (too many extensions, proofs in the main text)
- Predictions that match the existing results too perfectly (looks reverse-engineered)
- No prediction that distinguishes the model from obvious alternatives
- Assuming away the friction in a special case and not checking what happens
- Notation inconsistency between the model section and the empirical section
- Proofs that belong in an appendix cluttering the main text

## Tool integration (Corbis MCP)

Use tools to ground the model in published theory and empirical benchmarks:

- `search_papers` (query: the modeling tradition + setting, e.g., "moral hazard corporate investment model", `matchCount: 10`, `minYear: 2015`) — find papers with similar model structures to learn from their setup and avoid reinventing existing frameworks.
- `search_papers` (query: "calibration [parameter]" or "[elasticity] estimate") — find published calibration values and empirical estimates for the reasonableness checks.
- `get_paper_details` (paper IDs) — read abstracts of papers with comparable models to understand their approach and assumptions.
- `fred_series_batch` — pull actual data for calibration (risk-free rates, default rates, volatilities, growth rates, house price indices).
- `top_cited_articles` (journals: theory-publishing journals in the field) — find canonical models in the area to position against.
- `export_citations` (format: `bibtex`) — export references for the model's intellectual antecedents.

## Reference files

Read if needed:
- references/empirical-standards.md (for how the model connects to empirical design)
- references/writing-norms.md (for model section prose standards)
- references/latex-formatting-reference.md (for equation and notation formatting)

## Guardrails

- Do not build a model more complex than the empirical tests warrant. If the paper has three regressions, it does not need a six-period dynamic game.
- Do not present a model as "novel" if it is a relabeled version of a standard framework. Say "we adapt the framework of [cite] to the setting of [X]." Originality comes from the application and predictions, not from re-deriving known results.
- Do not skip the consistency audit. Every model must pass all structural checks before it goes into the paper.
- Do not skip the reasonableness battery. Internal consistency without external plausibility is not enough.
- Do not hide assumptions in functional form choices. If the result requires log utility, say so and discuss what happens with CRRA.
- Do not generate predictions that your data cannot test. Every prediction in the model section should map to a column in your tables (or be explicitly noted as untestable with current data).
- If the model has parameter regions where the prediction reverses sign, document this. Do not pretend the sign is unambiguous when it is not.
- Flag when a "simple model" in a referee report means different things: (a) a full micro-founded model, (b) a stylized partial-equilibrium model, (c) a conceptual framework with math, or (d) just clearer verbal reasoning. Ask the user which the referee likely means.

## Example prompts

- "Build a simple model of how information asymmetry about tenant quality affects commercial lease terms."
- "I need a two-period model showing why covenant violations reduce R&D more than capex."
- "Create a search model of the housing market where inspection costs affect price dispersion."
- "My referee wants a simple model. Here are my three main results — build the minimal model that generates all three."
- "I have a moral hazard model but the comparative statics don't sign cleanly. Help me fix it."
- "Calibrate my model's key prediction against published estimates of the investment-q sensitivity."
- "Run the consistency audit on this model before I write it up."
