# Lab Notebook: [Project Name]

## Project question
[One sentence: what are you trying to find out?]

## Data
- **Sample**: [data sources, sample period, unit of observation]
- **Key variables**: [dependent variable(s), main explanatory variable(s)]
- **Build script**: [path to the script that constructs the analysis dataset]

---

## Exploration log

### [Date] — [Brief description of what you tested]

**Question**: [What were you trying to learn?]

**What you ran**: [Specification: dep var, main RHS, controls, FE, clustering, sample filters]

**Result**: [Coefficient, t-stat, sign, magnitude. One sentence.]

**Verdict**: Keep / Toss / Modify and rerun

**Script**: [path to script, or "discarded"]

**Notes**: [What did this tell you about the economic story? What to try next?]

---

### [Date] — [Next test]

**Question**:

**What you ran**:

**Result**:

**Verdict**: Keep / Toss / Modify and rerun

**Script**:

**Notes**:

---

## Emerging narrative

[Update this section as the story develops. What mechanism is emerging? What is the main effect? What drives heterogeneity? What doesn't work and why?]

### Main finding
[What is the baseline result? How robust is it?]

### Mechanism evidence
[Which channel tests worked? Which competing channels were ruled out?]

### Heterogeneity
[Where is the effect stronger/weaker? Does the pattern support the mechanism?]

### What didn't work (and why it's informative)
[Tests that produced nulls or unexpected signs. What does that tell you about the economic story?]

---

## Table and figure candidates

List the tests that survived exploration and are candidates for the paper.

| # | Type | Description | Key result | Script | Status |
|---|---|---|---|---|---|
| 1 | Summary stats | Sample description | — | `analysis/01_summary_stats.py` | Ready |
| 2 | Baseline | Main effect | coef, t-stat | `analysis/02_baseline.py` | Ready |
| 3 | Robustness | [threat addressed] | [result] | [path] | Draft |
| 4 | Mechanism | [channel test] | [result] | [path] | Draft |
| 5 | Heterogeneity | [subgroup split] | [result] | [path] | Draft |
| 6 | Figure | [type and message] | — | [path] | Draft |

---

## Open questions

- [ ] [Things still to test or resolve before writing]
- [ ] [Alternative specifications to try]
- [ ] [Data issues to investigate]

---

## Ready to write?

Check these before transitioning to the paper:

- [ ] Baseline result is stable across reasonable specifications
- [ ] At least one mechanism test discriminates between channels
- [ ] Robustness checks map to specific threats (not a grab bag)
- [ ] Economic magnitude is computed and benchmarked
- [ ] Table/figure candidates above are complete and organized
- [ ] Scripts for all "Ready" tables produce clean output
- [ ] Emerging narrative section tells a coherent economic story
