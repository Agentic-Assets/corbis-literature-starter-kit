---
name: pre-submission-review
description: "Run a 6-agent pre-submission audit of an academic paper. Use before submitting to catch consistency errors, overclaiming, missing table notes, notation issues, and contribution weaknesses. Simulates a demanding referee."
---

# Pre-Submission Review

Simulate the scrutiny of a top journal's editorial board before you submit. Six specialized review agents run in parallel and their findings are consolidated into a single structured report.

Credit: Core review architecture adapted from Claes Bäckman's AI Research Feedback tool.

## When to use this skill

- The paper is nearly complete and the user wants a pre-submission audit
- The user wants to catch errors before a coauthor or advisor reads the draft
- The user wants a simulated referee report to anticipate objections
- The user is deciding whether the paper is ready for a specific journal

## Phase 1: Parse target and discover the paper

### Determine the target journal

Recognized journal names (case-insensitive):

| Category | Journals |
|---|---|
| Top-5 economics | `AER`, `QJE`, `JPE`, `Econometrica`, `REStud` |
| Finance | `JF`, `JFE`, `RFS`, `JFQA`, `MS` |
| Real estate / urban | `REE`, `JREFE`, `JUE`, `JHE` |
| Other finance | `RCFS`, `JBF`, `JCF`, `JMCB` |
| Macro | `AEJMacro`, `JME`, `RED` |

If no journal is specified, apply high general standards (`top-field`).

### Discover the paper files

1. Use Glob with `**/*.tex` to find all .tex files in the project directory.
2. Identify the main document (contains `\documentclass` or `\begin{document}`).
3. Read the main file and extract all `\input{}`, `\include{}`, `\subfile{}` references.
4. Read all component .tex files.
5. Glob for figure files: `**/figures/**/*.{pdf,png,eps,jpg}`, `**/Figures/**/*.{pdf,png,eps,jpg}`, root-level image files.
6. Glob for table files: `**/tables/**/*.tex`, `**/Tables/**/*.tex`, `*table*.tex`.

Record:
- Full path of each .tex file and its role
- List of figure and table file paths
- Paper title, authors, and abstract

## Phase 2: Launch 6 review agents in parallel

In a **single message**, launch all 6 agents using the Agent tool with `subagent_type: "general-purpose"`. Each agent reads the paper files independently. Pass the complete file lists to each agent.

---

### Agent 1 — Spelling, Grammar & Academic Style

You are a copy editor at a top economics journal. Read all .tex files and perform a thorough review. Ignore LaTeX commands unless they cause formatting issues.

**Check:**

1. **Spelling errors**: Misspelled words, proper nouns, technical terms, commonly confused words (affect/effect, principal/principle, complement/compliment).

2. **Grammar errors**: Subject-verb agreement, tense consistency (present for findings, past for procedures), article usage, dangling modifiers, comma splices, run-on sentences, fragments.

3. **Awkward phrasing**: Sentences requiring re-reading. Suggest clearer alternatives.

4. **Style violations** — flag every instance of:
   - Filler phrases: "interestingly", "importantly", "notably", "crucially", "it is worth noting", "needless to say", "obviously", "clearly"
   - Tautologies: "very unique", "absolutely essential", "completely eliminate"
   - "significant" used to mean large/important (reserve for statistical significance)
   - "This paper contributes to the literature by..." -- show, don't tell
   - Passive voice where active is natural ("it is shown that" -> "we show that")
   - Inconsistent first person ("we find" vs. "the paper argues")

5. **Em dashes**: Flag every em dash in the manuscript. Replace with commas, parentheses, colons, or separate sentences. This is a hard rule.

6. **Typographic consistency**: Hyphenation (long-run vs. long run), en-dash for ranges, spacing.

7. **Number formatting**: Numbers below 10 spelled out in prose; percentage format consistent.

8. **Introduction opening**: The first paragraph of the introduction must be grounded in a specific, recent industry event, policy change, or market development (with a citation to an industry report, news article, or practitioner source). Flag if the introduction opens with an abstract literature gap or generic motivation instead.

**Output format:**
```
## Agent 1: Spelling, Grammar & Style
### Critical Issues (must fix)
[numbered: Location | "Problematic text" → "Correction" | Reason]
### Minor Issues
[numbered: same format]
### Style Patterns to Fix Throughout
[recurring patterns with one example each]
```

---

### Agent 2 — Internal Consistency & Cross-Reference Verification

You are a technical reviewer checking whether the paper is internally coherent.

**Check:**

1. **Numerical consistency**: Every number in the text (coefficients, percentages, sample sizes, years) must match the referenced table or figure. Flag discrepancies.

2. **Abstract vs. body**: Numbers, findings, and claims in the abstract must exactly match the main text and tables.

3. **Introduction vs. results**: When the introduction previews results ("we find X"), verify the results section delivers exactly that.

4. **Cross-reference correctness**: For every "as shown in Figure X", "Table Y shows", "see Appendix A" — verify the element exists and shows what is claimed.

5. **Terminology consistency**: Flag any key term used inconsistently or redefined across sections. Check variable names, treatment descriptions, and sample labels.

6. **Sample description consistency**: Do stated sample characteristics (years, N, filters) remain consistent across abstract, data section, and table notes?

7. **Fixed effects and controls consistency**: Do the FE and controls described in the text match what the tables show?

8. **Magnitude consistency**: When the same finding appears in multiple places (abstract, intro, conclusion, results), are direction and magnitude stated consistently?

9. **Citation verification**: For each in-text citation of an external finding, verify (a) the cited author-year appears in the bibliography and (b) the characterization is plausible.

**Output format:**
```
## Agent 2: Internal Consistency
### Critical Inconsistencies
[numbered: Location 1 ↔ Location 2 | What conflicts | Severity]
### Cross-Reference Errors
[numbered: Reference | Target | Issue]
### Terminology Drift
[numbered: Term | How it varies | Standardization]
### Minor Inconsistencies
[numbered: same format]
```

---

### Agent 3 — Unsupported Claims & Identification Integrity

You are a skeptical econometrician enforcing claim discipline — claims must never exceed what the identification allows.

**Check:**

1. **Causal language without causal identification**: Flag every "causes", "leads to", "drives", "determines", "because of", "results in" applied to findings — unless genuine causal identification supports that specific claim.

2. **Generalization beyond the sample**: Claims extending findings beyond the data's scope without explicit reasoning.

3. **Mechanism claims stated as facts**: When an explanation for *why* a result holds is asserted rather than argued as a hypothesis.

4. **Unsupported robustness claims**: "Our results are robust to X" — verify the robustness check actually appears in the paper.

5. **Missing caveats**: Places where a reader would ask "but what about...?" and the paper is silent. Think about the most obvious threats for the specific design.

6. **Literature overclaiming**: "No prior study has examined X" or "We are the first to show Y" — flag if likely false.

7. **Statistical vs. economic significance conflation**: Statistical significance reported without economic magnitude discussion.

8. **Hedging failures**: Both overconfident claims and excessive hedging on strong results.

**Output format:**
```
## Agent 3: Claims & Identification
### Causal Overclaiming (must fix)
[numbered: Section | "Exact text" | Why overclaims | Fix]
### Generalization Issues
[numbered: same format]
### Missing Caveats
[numbered: Topic | Where to address | Suggested text]
### Minor Language Issues
[numbered: same format]
```

---

### Agent 4 — Mathematics, Equations & Notation

You are a mathematical economist reviewing formal content.

**Check:**

1. **Mathematical correctness**: Do derivations follow logically? Algebraic errors? Do regression subscripts and terms match the verbal description?

2. **Notation consistency**: Same symbol for the same quantity throughout. Flag reuse. Subscript conventions consistent ($i$ = individual, $t$ = time, etc.).

3. **Undefined notation**: Every symbol must be defined at or before first use.

4. **Equation numbering**: Numbered equations referenced in text? Numbered equations never referenced?

5. **Regression specification consistency**: Written equation matches (a) verbal description, (b) table column headers, (c) stated controls and fixed effects.

6. **Return/growth rate definitions**: Annualization formulas correct? Percentage vs. percentage-point distinctions? Log approximations flagged?

7. **Statistical notation**: SE, t-stat, and CI formulas correct? Clustering notation consistent with the text?

8. **LaTeX math formatting**: Missing `\left`/`\right`, improper `*` for multiplication, text in math mode not in `\text{}`, alignment issues.

**Output format:**
```
## Agent 4: Mathematics & Notation
### Mathematical Errors
[numbered: Equation/Location | Error | Correction]
### Notation Inconsistencies
[numbered: Symbol | Conflicting uses | Resolution]
### Undefined Notation
[numbered: Symbol | First used | Where to define]
### Regression Specification Issues
[numbered: Table/Spec | Discrepancy]
### LaTeX Math Formatting
[numbered: Location | Issue | Fix]
```

---

### Agent 5 — Tables, Figures & Documentation

You are a journal production editor reviewing completeness and self-containedness.

**For every table, check:**

1. **Float structure**: Does it follow the template format? Caption on top → `\label{}\vspace{-2.5ex}` → `\floatnotes{...}` above the body (not below) → table body. Flag any table where the note appears after `\end{tabular}` instead of before it.
2. **Title/caption**: Accurately describes content? Self-contained without the body text?
3. **Column headers**: Clear, unambiguous? State dependent variable and specification differences?
4. **Notes completeness** — every table needs:
   - Sample definition, time period, restrictions
   - Dependent variable definition and units
   - Controls included
   - Fixed effects included
   - SE computation method and clustering level
   - Significance star definitions
   - Whether reporting SEs, t-stats, or p-values
4. **t-statistics**: Tables should report t-statistics in parentheses below coefficients (not standard errors, not p-values). Flag any table that reports standard errors or p-values instead of t-statistics.
5. **Observations**: N reported in every column?
6. **Cross-referencing**: Every table cited in text?
7. **Formatting consistency**: Consistent notation for FE indicators, decimal places, stars.

**For every figure, check:**

1. **Float structure**: Caption → label → `\floatnotes{...}` above the figure → `\centering` + `\includegraphics`. Flag any figure where the note appears below the image.
2. **Title/caption**: Self-contained?
3. **Axis labels**: Both axes labeled with units?
3. **Legend**: Present if multiple series?
4. **Confidence intervals**: Shown for binscatters, coefficient plots, event studies?
5. **Notes completeness**: Sample, what is plotted, controls absorbed, data source.
6. **Cross-referencing**: Every figure cited in text?

**Output format:**
```
## Agent 5: Tables & Figures
### Tables with Incomplete Notes
[by table: Table X | Missing element | Suggested addition]
### Figures with Incomplete Notes
[by figure: Figure X | Missing element | Suggested addition]
### Cross-Reference Issues
[list: Element | Issue]
### Formatting Inconsistencies
[list: Issue | Where | Recommendation]
```

---

### Agent 6 — Contribution Evaluation (Adversarial Referee)

You are a demanding associate editor at TARGET_JOURNAL. (If `top-field`, apply high general standards.) You have read thousands of papers and have extremely high standards. You are deciding whether to send this to referees or desk reject.

**Part 1 — Central Contribution**
- State the contribution in one sentence.
- Is this genuinely new, or a known result in a new setting?
- What is the closest prior paper? What does this add?
- Does the finding change how economists think about the topic?
- Rate: [Transformative | Significant | Incremental | Insufficient for target journal]

**Part 2 — Identification and Credibility**
- What variation identifies the main result?
- Is it plausibly exogenous? Main threats?
- Is the main finding causal, correlational, or descriptive? Does the paper claim correctly?
- What would a skeptical seminar audience say?

**Part 3 — Required and Suggested Analyses**
- **Required** (3-5 blockers): robustness not performed, alternatives not ruled out, missing falsifications
- **Suggested** (3-5 strengtheners): mechanism tests, subgroups, extensions

**Part 4 — Literature Positioning**
- Right papers cited? Obvious omissions?
- Adequately distinguished from closest work?
- Best framing for the introduction?

**Part 5 — Journal Fit and Recommendation**
- If specific journal: Is this a strong fit? Fit risks?
- If `top-field`: Which journals are realistic targets?
- Recommendation: [Send to referees | Revise before submitting | Desk reject]
- What concretely would it take to reach the target journal's bar?
- Best alternative outlet?

**Part 6 — Pointed Questions**
- 4-7 specific, hard questions a referee would ask. Frame them exactly as a referee report would.

**Output format:**
```
## Agent 6: Contribution & Referee Assessment
### Part 1 — Central Contribution
[assessment + rating]
### Part 2 — Identification and Credibility
[assessment]
### Part 3 — Required and Suggested Analyses
**Required:** [numbered list]
**Suggested:** [numbered list]
### Part 4 — Literature Positioning
[assessment]
### Part 5 — Journal Fit and Recommendation
[recommendation + path]
### Part 6 — Questions to the Authors
[numbered list of 4-7 questions]
```

---

## Phase 3: Consolidate and save

After all 6 agents return, consolidate into a single report saved to:

`PRE_SUBMISSION_REVIEW_[YYYY-MM-DD].md`

**Report structure:**

```markdown
# Pre-Submission Referee Report

**Paper**: [Title]
**Authors**: [Authors]
**Date**: [Today's date]
**Review Standard**: [Journal name or "Leading Field Journal"]

---

## Overall Assessment
[3-4 sentences: what the paper does, principal strength, most critical issue]
**Preliminary Recommendation**: [Send to referees | Revise before submitting | Substantial revision required]

---

## 1. Spelling, Grammar & Style
[Agent 1 output]

## 2. Internal Consistency
[Agent 2 output]

## 3. Claims & Identification Integrity
[Agent 3 output]

## 4. Mathematics & Notation
[Agent 4 output]

## 5. Tables, Figures & Documentation
[Agent 5 output]

## 6. Contribution & Referee Assessment
[Agent 6 output]

---

## Priority Action Items

Triage hierarchy: identification/credibility failures > missing required analyses > internal inconsistencies > table/figure documentation > math errors > style/grammar.

**CRITICAL** (must fix — could cause desk rejection):
1. ...

**MAJOR** (should fix — referees will raise):
4. ...

**MINOR** (polish):
8. ...
```

## Tool integration (Corbis MCP)

Use tools to strengthen the review — especially Agent 6's contribution evaluation:

- `search_papers` (query: the paper's core claim, `matchCount: 10`) → verify whether Agent 6's "closest prior paper" assessment is accurate and complete. Check for papers the agents might have missed.
- `get_paper_details` (paper IDs) → read abstracts of papers cited in the manuscript to verify that in-text characterizations (Agent 2, Agent 3) are accurate.
- `top_cited_articles` (field + topic) → verify that the paper cites the seminal work in its area (Agent 6 Part 4).
- `export_citations` (format: `bibtex`) → export BibTeX entries for any new references recommended by the review, including papers identified as literature gaps by Agent 6. Offer this after the consolidated review report is produced.
- `format_citation` → format individual recommended citations so the user can add them to the bibliography.

## Relationship to other skills

This skill **audits a nearly complete paper**. It is distinct from:
- `referee-revision-response` — handles *incoming* referee reports after submission
- `research-paper-writer` — *drafts* paper sections
- `finance-empirical-analysis` — *plans* the empirical strategy

**Typical workflow**: Use the other skills to build the paper → use `pre-submission-review` as the final quality gate → fix issues → submit.

## Guardrails

- Do not soften the review to be polite. The point is to catch problems before a real referee does.
- Do not fabricate issues — every flagged problem must cite a specific location in the paper.
- If the paper is genuinely strong, say so. Not every paper has critical issues.
- Do not let Agent 6 become a generic literature review — it should focus on the 2-3 biggest contribution and identification concerns.
- If agents disagree (e.g., Agent 3 flags overclaiming but Agent 6 thinks the identification is adequate), note the disagreement in the consolidation.

## Example prompts
- "Run a pre-submission review of my paper targeting JFE."
- "Audit this real-estate paper before I send it to REE."
- "Do a consistency check on my LaTeX manuscript."
- "Simulate a hostile but fair referee report for this corporate-finance paper."
- "Check my paper for overclaiming and missing table notes."
