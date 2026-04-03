---
name: check-consistency
description: Fast cross-section consistency scan for numbers, terminology, and references
user_invocable: true
---

# Check Consistency Skill

Fast, focused scan for cross-section inconsistencies in `main.tex`. Lighter than `/pre-submission-review` -- designed for iterative use during editing.

## Examples
- `/check-consistency` -- full scan of main.tex
- `/check-consistency numbers` -- only check quantitative claims
- `/check-consistency terminology` -- only check terminology consistency

## Workflow

### Step 1: Load Reference Values
Read `notes/project_state.md` to get canonical values (if it exists):
- Key quantitative results and their canonical magnitudes
- Sample description (date range, number of observations, variable counts)
- Any other numbers that appear in multiple sections

If no project state file exists, the skill still works by cross-referencing sections against each other (without a canonical reference).

### Step 2: Quantitative Consistency
Grep `main.tex` for all quantitative claims and cross-reference:
- Percentages and basis points mentioning specific variables or factors
- Sample period mentions (start date, end date, number of periods)
- Counts (variables, observations, subsamples, etc.)
- Any number that appears in more than one section

Flag: mismatches between text claims and canonical values (if available), or between sections.

### Step 3: Terminology Consistency
If `notes/project_state.md` defines a terminology table, grep across all sections for violations.

Also check for within-paper drift regardless of project state:
- Same concept called different names in different sections
- Inconsistent abbreviation introduction (defined in one section, used without definition in another)
- Check against `references/banned-words.md` for hard-banned terms

### Step 4: Cross-Reference Integrity
1. Extract all `\ref{...}` and `\eqref{...}` targets
2. Extract all `\label{...}` definitions
3. Flag any `\ref` or `\eqref` that points to a non-existent label
4. Flag any `\ref` used where `\eqref` should be (equation references)
5. Check that all tables and figures are cited at least once in the text

### Step 5: Section Cross-References
Check that claims about other sections are accurate:
- "As shown in Section X" -- does Section X actually show this?
- "Table Y reports" -- does Table Y match the claim?
- "See Appendix Z" -- does the appendix contain the referenced content?

### Step 5b: Caption Consistency
Run `/audit-captions`. Include CRITICAL and IMPORTANT findings in the output.

### Step 6: Output

```
CONSISTENCY CHECK
=================

QUANTITATIVE MISMATCHES: [N found]
- Line X: claims "[value]" but canonical value is "[value]" for [variable]
- Line Y: says "[count]" but project_state.md says "[count]"
(or: "No project_state.md -- cross-section comparison only")

TERMINOLOGY VIOLATIONS: [N found]
- Line X: "[deprecated term]" (should be "[correct term]")
- Line Y: "[term A]" in this section vs "[term B]" in [other section]

REFERENCE INTEGRITY: [N issues]
- Line X: \ref{eq:decomp} should be \eqref{eq:decomp}
- Line Y: \ref{fig:missing} -- label not found

CROSS-SECTION CONSISTENCY: [N issues]
- Line X claims "Table 3 shows..." but Table 3 actually shows...

SUMMARY:
- Critical issues: N
- Warnings: M
- All clear: [list of checks that passed]
```
