---
name: audit-math
description: Adversarial audit of mathematical proofs, derivations, and formal environments
user_invocable: true
---

# Audit Math Skill

Structured adversarial audit of mathematical content: proofs, derivations, definitions, assumptions, and formal environments. Works on any section containing formal math.

## Examples
- `/audit-math appendix-a` -- full audit of Appendix A
- `/audit-math methodology` -- audit math content in the methodology section
- `/audit-math 200-450` -- audit specific line range in main.tex

## Input

The user provides one of:
- A section key (e.g., `appendix-a`, `methodology`, `results`)
- A line range (e.g., `200-450`)
- If omitted, scans main.tex for sections containing formal environments and audits the first one found

## Workflow

### Step 1: Load Context
1. Read the project's notation file (if it exists) for custom commands, core variables, subscript conventions, theorem environment numbering, and math writing rules
2. Read `notes/project_state.md` for key labels, formal environment ordering, and canonical results (if it exists)
3. Read `references/writing-norms.md` for cross-reference style rules and terminology
4. Extract the target section from `main.tex` using `%% BEGIN/END` markers (or line range)

### Step 2: Inventory Formal Environments
Build a registry of every formal environment in the target section:
- Definitions (`\begin{definition}`)
- Assumptions (`\begin{assumption}`)
- Lemmas (`\begin{lemma}`)
- Propositions (`\begin{proposition}`)
- Corollaries (`\begin{corollary}`)
- Theorems (`\begin{theorem}`)
- Proofs (`\begin{proof}`)
- Remarks (`\begin{remark}`)

For each, record: label, name (from `[...]` bracket), line number, and which assumptions/results it references.

If a notation protocol file registers environment numbering, cross-check against it. Flag any missing or extra environments, misordered labels, or mismatched names.

### Step 3: Assumption Dependency Audit
For each lemma, proposition, corollary, and theorem:
1. List the assumptions explicitly invoked in the **statement** (e.g., "Under Assumptions \ref{assum:iid} and \ref{assum:overlap}")
2. List the assumptions actually **used in the proof**
3. Flag **hidden dependencies**: assumptions used in the proof but not stated in the result
4. Flag **unused declarations**: assumptions stated in the result but never invoked in the proof
5. Flag **implicit prerequisites**: does the result depend on an earlier definition or lemma not cited?
6. Check that assumption references use `\ref{assum:...}` (not prose descriptions like "the independence assumption")

Present as a table:

| Result | States | Uses | Hidden | Unused |
|--------|--------|------|--------|--------|

### Step 4: Proof Completeness Audit
For each proof, check:
1. **Hand-waved steps**: Are there jumps marked by "it follows that," "clearly," "one can verify," or "by standard arguments" without justification? Flag with the specific step that is skipped.
2. **Approximations**: Are approximations (first-order, asymptotic, etc.) flagged explicitly? Does the proof state where the approximation is used and what is neglected?
3. **Substitution steps**: When a definition or earlier result is substituted, is the substitution shown or just asserted? For a top-journal appendix, key algebraic steps should be shown.
4. **Symmetry arguments**: When "by symmetry" is invoked, verify the symmetry actually holds.
5. **Proof endings**: Does every `\begin{proof}` have a matching `\end{proof}`?

### Step 5: Sign Analysis
For each inequality or signed result:
1. Trace the sign through each step of the proof. Does the chain of inequalities yield the stated direction?
2. Check WLOG conventions: when "without loss of generality, assume $a > 0$" is stated, verify the other case is handled and that the final result is invariant to this choice.
3. Check that the sign of the result aligns with the economic intuition in the interpretive prose.
4. For results stated with $\ge$ (weak inequality): is there a condition under which equality holds? Is it stated?

### Step 6: Boundary and Degenerate Cases
Test each result at the edges of its parameter space:
1. Identify the key parameters and check behavior at their extremes (0, 1, $\infty$, etc.)
2. Do closed-form expressions simplify correctly at these limits?
3. Are limiting cases stated as corollaries? If so, do they match the general result at those parameter values?
4. Are expressions well-defined at all points in the claimed parameter range? (No division by zero, no undefined logs, etc.)

### Step 7: Notation Consistency
Using the project's notation file as the reference (if available):
1. **Symbol reuse**: Is the same symbol used for the same quantity throughout?
2. **Hat convention**: If hats are used (e.g., observed vs. true), is the convention consistent?
3. **Define before use**: Is every symbol defined where it first appears? Flag any symbol used before its definition.
4. **Custom commands**: Are custom commands used consistently? (`\E[...]` not `E[...]`, `\Var` not `\text{Var}`, etc.)
5. **Subscript conventions**: Are subscripts consistent throughout?
6. **Cross-check with main body**: If the same symbol appears in the main body, verify it has the same meaning.

### Step 8: Cross-Reference Integrity
1. Every `\ref{...}` to a definition, assumption, lemma, proposition, corollary, or theorem must point to a valid `\label{...}`
2. Equation references must use `\eqref{...}` (not `\ref{...}`)
3. Non-breaking spaces must precede all references: `Eq.~\eqref{...}`, `Lemma~\ref{...}`, `Assumption~\ref{...}`
4. Check that references to main body sections resolve correctly
5. Check for dangling forward references (result X cites result Y that appears later -- is Y actually proven independently?)

### Step 9: Interpretive Prose Audit
Each formal result should be followed by interpretive prose. Check:
1. Does every lemma/proposition/theorem/corollary have a remark or explanatory paragraph after it?
2. Does the interpretive prose connect the mathematical result to the paper's economic argument?
3. Does the prose use correct terminology (per `references/writing-norms.md`)?
4. Is the prose free of banned words (per `references/banned-words.md`)?

### Step 10: Edge Case -- No Math Found
If the target section contains no formal environments:
- Report: "No formal mathematical environments found in [section]. This skill is designed for sections with proofs and derivations."
- Suggest: "Consider running a general content audit instead."
- If the section contains inline math or displayed equations (but no formal environments), note the equations found and flag any that lack surrounding context or definitions.

## Output

```
MATH AUDIT: [section name / line range]
========================================

ENVIRONMENT INVENTORY:
  Definitions: N (labels: ...)
  Assumptions: N (labels: ...)
  Lemmas: N
  Propositions: N
  Corollaries: N
  Theorems: N
  Proofs: N
  Remarks: N
  Inventory vs notation protocol: [MATCH / N discrepancies / not available]

ASSUMPTION DEPENDENCIES:
| Result | States | Uses | Hidden | Unused |
|--------|--------|------|--------|--------|
| Lemma 1 | none | none | -- | -- |
| Prop 1 | 1,2 | 1,2 | -- | -- |
| ... | ... | ... | ... | ... |

PROOF COMPLETENESS: [N issues]
- [Line X] [SEVERITY]: [description]

SIGN ANALYSIS: [N issues]
- [Line X] [SEVERITY]: [description]

BOUNDARY CASES: [N issues]
- [Line X] [SEVERITY]: [description]

NOTATION CONSISTENCY: [N issues]
- [Line X] [SEVERITY]: [description]

CROSS-REFERENCES: [N issues]
- [Line X] [SEVERITY]: [description]

INTERPRETIVE PROSE: [N issues]
- [Line X] [SEVERITY]: [description]

SEVERITY SUMMARY:
  CRITICAL: N (errors that invalidate a result or hide a dependency)
  IMPORTANT: N (gaps that a referee would flag)
  MINOR: N (notation inconsistencies, style issues)
  NICE-TO-HAVE: N (polish items)

TOP PRIORITY FIXES:
1. [CRITICAL] [Line X]: [description and suggested fix]
2. [IMPORTANT] [Line Y]: [description and suggested fix]
3. [etc.]
```

## Severity Definitions

- **CRITICAL**: A hidden assumption, incorrect sign, missing proof step, or broken cross-reference that could invalidate a formal result. A referee would reject on this basis.
- **IMPORTANT**: A gap that does not invalidate the result but that a careful referee would flag -- e.g., an unhandled boundary case, an approximation not explicitly flagged, or an assumption invoked in the proof but not stated in the theorem.
- **MINOR**: A notation inconsistency, a missing non-breaking space, or a style violation in interpretive prose. Does not affect correctness.
- **NICE-TO-HAVE**: Polish items -- e.g., adding an extra remark for economic intuition, clarifying a "by standard arguments" step that is in fact standard.

## Composability

This skill can be called from `/pre-submission-review` as an additional pass on sections containing formal math. The recommended integration point is after the section-by-section audit:

```
For sections containing formal environments (any appendix or main body
section with \begin{proposition}), run /audit-math.
```

When called from a full paper audit, suppress the full output template and return only the SEVERITY SUMMARY and TOP PRIORITY FIXES sections.
