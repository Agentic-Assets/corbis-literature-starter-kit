---
name: audit-captions
description: Audit all table and figure captions for language, notation, and formatting consistency
user_invocable: true
---

# Audit Captions Skill

Systematic audit of all `\caption{}` blocks, tablenotes, and figure notes for cross-caption consistency in language, notation, terminology, number formatting, and structure.

## Examples
- `/audit-captions` -- audit all captions in main.tex
- `/audit-captions tables` -- audit only table captions
- `/audit-captions figures` -- audit only figure captions
- `/audit-captions appendix` -- audit captions in appendix sections only

## Input

The user provides an optional scope filter. If omitted, all captions in `main.tex` are audited.

## Workflow

### Step 1: Load Context
1. Read the project's notation file (if it exists) for mathematical notation conventions
2. Read `references/writing-norms.md` for terminology rules and banned words
3. Read `notes/project_state.md` for canonical numbers, sample description, and project-specific terminology (if it exists)
4. Read `main.tex` in full

### Step 2: Extract All Captions
For each `\caption{...}` in `main.tex`, extract:
- **Line number** in main.tex
- **Environment type**: table or figure
- **Label**: the `\label{...}` associated with this float
- **Caption title**: the text inside `\caption{...}`
- **Caption notes**: any footnote-size block that follows the caption. Common patterns:
  - Tables: `\caption{Title.}` followed by `\begin{spacing}{1}{\footnotesize ... }\end{spacing}`
  - Figures: `\caption{Title.}` followed by `\begin{justify}\begin{spacing}{1}\footnotesize{...}\end{spacing}\end{justify}`
  - Or `\begin{tablenotes}...\end{tablenotes}`
- **Panel descriptions**: any `\textbf{Panel A:}` or `\multicolumn{...}{...}{\textbf{Panel A:} ...}` text inside the float

Build a numbered registry of all captions for cross-comparison. Record the section each caption belongs to (using `%% BEGIN/END` markers).

### Step 3: Language Consistency
Compare the phrasing of recurring concepts across ALL captions. Flag inconsistencies in:

**3a. Sample period description**
- Extract every mention of the sample period
- Flag: different date formats for the same sample (e.g., "YYYY-YYYY" vs "YYYY-MM to YYYY-MM" vs "Month YYYY to Month YYYY")
- Flag: inconsistent use of observation counts (some captions include $T$=N, others omit it)
- Note: different sample start dates are legitimate when different datasets start at different points. Only flag genuinely inconsistent formatting, not substantively different samples.

**3b. Return descriptions**
- How are returns described? Flag inconsistencies:
  - "monthly returns" vs "excess returns" vs "risk-adjusted returns"
  - "mean monthly return (\%)" vs "mean return (\%)"

**3c. Statistical methodology descriptions**
- Standard error specification (e.g., Newey-West): must be identical across all captions that mention it
  - Pick the most common form as canonical; flag all deviations
- How t-statistics are described: "$t$-statistics" vs "t-statistics" vs "$t$-stats"
- How significance is described: flag any inconsistency

**3d. Variable definitions**
- When the same variable appears in multiple captions (e.g., "$\mu$ is mean monthly return (\%)"), the definition must be identical
- Flag any variable defined differently across captions

**3e. Approach/method naming**
- If the paper uses named approaches or methods, check they are named consistently across captions
- Flag: same method called different names in different captions
- Note: column headers inside tables may use short forms; caption prose should use the paper's terminology

### Step 4: Notation Consistency
Check mathematical notation in captions against the project's notation file (if available):
1. Are custom commands used consistently? (e.g., `$\E[...]$` not `$E[...]$`)
2. Are variables consistent with their definitions?
3. Are subscripts consistent? ($r_{i,t+1}$ not $r_{it+1}$)
4. Are factor names consistently formatted?
5. Flag any mathematical notation in captions not defined in the notation file or in the caption notes themselves

### Step 5: Terminology Compliance
If `notes/project_state.md` defines a terminology table, apply it to all captions. Flag any use of deprecated or incorrect terms.

Also check for banned words from `references/banned-words.md` appearing in captions.

### Step 6: Structural Consistency
Check that all captions follow a consistent structure:

**6a. Caption title format**
- Do all caption titles end with a period?
- Do all titles follow a consistent pattern? (e.g., "Descriptive phrase." not "Table showing X")
- Flag titles that are too long (>15 words) or too short (single word)

**6b. Caption notes structure**
- Do all tables with empirical results include: (1) variable definitions, (2) methodology description, (3) sample period?
- Do all figures include: (1) what the figure shows, (2) any data transformations, (3) sample period?
- Flag any table or figure with empirical content but no caption notes

**6c. Panel descriptions**
- Are panels described consistently? ("Panel~A" vs "Panel A" vs "Panel (A)")
- Do caption notes describe what each panel shows?
- Does the panel labeling in the caption match the actual panel labels in the table/figure?

### Step 7: Number Format Consistency
Check consistency in how numbers are formatted across captions:
1. **Percentages**: "(\%)" vs "percent" vs "pct" vs "basis points" vs "bp"
2. **Decimal places**: are significance thresholds described with consistent precision?
3. **Lag notation**: if a lag formula is used, is it identical everywhere it appears?

### Step 8: Abbreviation Consistency
1. List all abbreviations used in captions
2. Check: is each abbreviation defined on first use in the paper?
3. Check: are abbreviations used consistently? (not spelled out in one caption and abbreviated in another without definition)
4. Flag abbreviations used in captions but never defined anywhere in the paper

### Step 9: Caption-Text Cross-Reference
For each table/figure referenced in the body text:
1. Check that what the text says about the table/figure matches the caption
2. Check that the text's description of panels matches the caption's panel labels
3. Check that the sample period stated in the text matches the sample period in the caption

### Step 10: Copy-Paste Drift Detection
Compare all captions pairwise for near-duplicate phrases:
1. Identify captions that share >60% of their notes text (likely copy-pasted)
2. For each pair: verify that any differences are intentional (e.g., different sample periods, different panel descriptions) vs. accidental (one was updated, the other was not)
3. Flag specific sentences that are identical across captions -- these are candidates for mutual consistency verification

### Step 11: Edge Case -- No Captions Found
If the target scope contains no `\caption{}` commands:
- Report: "No captions found in [scope]. Nothing to audit."
- Suggest: "Run `/audit-captions` without a scope filter to audit all captions."

## Output

```
CAPTION AUDIT
=============

INVENTORY:
  Tables: N captions extracted
  Figures: M captions extracted
  Total: N+M

CAPTION REGISTRY:
| # | Type | Label | Line | Title (truncated) | Has Notes | Sample Period |
|---|------|-------|------|-------------------|-----------|---------------|
| 1 | Table | tab:summary | 560 | Summary Statist... | Yes | [start] to [end] |
| 2 | Figure | fig:ts | 660 | Time series of... | Yes | [start] to [end] |
| ... | ... | ... | ... | ... | ... | ... |

LANGUAGE CONSISTENCY: [N issues]
- [Line X vs Line Y] [SEVERITY]: Sample period format inconsistency
  Caption A: "Sample: YYYY-MM to YYYY-MM, $T$=N"
  Caption B: "Sample: YYYY-MM to YYYY-MM" (missing $T$)
- [Line X vs Line Y] [SEVERITY]: Variable definition inconsistency
  Caption A: "$\mu$ is mean monthly return (\%)"
  Caption B: "$\mu$ is mean return (\%)"

NOTATION CONSISTENCY: [N issues]
- [Line X] [SEVERITY]: [description]

TERMINOLOGY COMPLIANCE: [N issues]
- [Line X] [SEVERITY]: [description]

STRUCTURAL CONSISTENCY: [N issues]
- [Line X] [SEVERITY]: [description]

NUMBER FORMAT: [N issues]
- [Line X vs Line Y] [SEVERITY]: [description]

ABBREVIATIONS: [N issues]
- [Line X] [SEVERITY]: [description]

CAPTION-TEXT ALIGNMENT: [N issues]
- [Line X (text) vs Line Y (caption)] [SEVERITY]: [description]

COPY-PASTE DRIFT: [N pairs flagged]
- Captions [A] and [B]: N% overlap in notes text
  Difference: [specific divergent detail]

SEVERITY SUMMARY:
  CRITICAL: N (factual mismatches between caption and text/data)
  IMPORTANT: N (language or notation inconsistencies visible to referees)
  MINOR: N (formatting preferences, abbreviation nits)
  NICE-TO-HAVE: N (structural polish)

STANDARDIZATION RECOMMENDATIONS:
[3-5 specific phrases that should be standardized across all captions, with the recommended canonical form:]
1. Sample period: "[recommended canonical form]"
2. Standard errors: "[recommended canonical form]"
3. [etc.]

TOP PRIORITY FIXES:
1. [CRITICAL] [Line X]: [description and suggested fix]
2. [IMPORTANT] [Line Y]: [description and suggested fix]
3. [etc.]
```

## Severity Definitions

- **CRITICAL**: A factual mismatch between caption and text, or a caption that contradicts the data in its table/figure. A referee would question the paper's accuracy.
- **IMPORTANT**: A language, notation, or terminology inconsistency that a careful referee would notice and that signals carelessness (e.g., different date formats for the same sample across captions).
- **MINOR**: A formatting preference that does not affect understanding but looks unpolished (e.g., inconsistent use of $T$ across captions).
- **NICE-TO-HAVE**: Structural suggestions for improving caption quality (e.g., adding panel descriptions where missing).

## Composability

This skill can be called from `/check-consistency` as an additional pass focused on float environments:

```
Step 5b: Caption Consistency
Run /audit-captions. Include CRITICAL and IMPORTANT findings in the output.
```

It can also be called from `/pre-submission-review` after the cross-section consistency step:

```
Run /audit-captions to check caption-level consistency.
Include CRITICAL and IMPORTANT findings in the master report.
```
