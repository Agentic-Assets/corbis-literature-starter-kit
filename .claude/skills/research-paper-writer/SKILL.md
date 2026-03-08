---
name: research-paper-writer
description: "Draft and polish finance or real-estate papers in a top-journal style. Use for abstracts, introductions, results sections, conclusions, titles, and journal-targeted prose."
---

# Research Paper Writer

Write like a serious empirical researcher aiming at a skeptical editorial process.

## Core mandate

Convert a design and set of results into prose that is concise, credible, and journal-aware. Every sentence should earn its place.

## First move

Determine the target track and, if possible, the target journal:
- Finance track: JF, JFE, RFS, JFQA, RoF
- Real-estate track: REE, JREFE, JRER, JHE, RSUE

If the target is not named, infer the most likely track and say what assumption you made. Read `references/journal-targets.md` for detailed journal profiles including fit inference, red flags, and development advice.

## Starting from exploration notes (discovery-to-paper bridge)

If the user has a lab notebook (`notes/lab_notebook.md`) or similar exploration notes with results and a narrative, use that as the starting input. The bridge workflow is:

1. **Read the lab notebook.** Look for: the emerging narrative section, the table/figure candidates list, and the "what didn't work" section.
2. **Extract the story spine** from the narrative: question, mechanism, main finding, supporting evidence, what was ruled out.
3. **Map table candidates to the standard table sequence** (summary stats → baseline → robustness → mechanism → heterogeneity → extensions). Reorder or consolidate if needed. Flag gaps (e.g., "you have mechanism tests but no robustness table addressing [threat]").
4. **Draft the paper outline** as a structured plan: section-by-section with the table/figure each section references and the key point each section makes.
5. **Copy the LaTeX template** into `paper/` if it doesn't exist, then start writing sections directly into the `.tex` file.

The lab notebook's "what didn't work" section is valuable: null results often sharpen the contribution by showing what the effect is *not*. Use these to inform the robustness and mechanism discussion.

If there is no lab notebook but the user has a loose set of results and notes, ask them to provide: (a) the main finding in one sentence, (b) the list of tables/figures they want in the paper, and (c) the economic story they believe is emerging. That is enough to start.

## Writing workflow

1. Build the story spine:
   - question
   - mechanism
   - design
   - main finding
   - contribution
   - implication
2. Draft the introduction around that spine (use assets/introduction-skeleton.md).
3. Draft paragraph-level writeups for main tables.
4. Tighten the abstract after the body logic is clear.
5. Draft a short, high-information conclusion.
6. Check every claim against the design's limits.
7. Generate 3-5 title options.

## Introduction structure (expanded)

**Paragraph 1 — Question and stakes (grounded in recent events)**: Open with a specific, recent industry event, policy change, or market development that directly motivates the research question. Cite the source (industry report, news article, regulatory filing, Fed report, practitioner white paper). Then pivot to the economic question. The reader should immediately see why this question matters *now*, not just in the abstract. Avoid "despite the importance of X, little is known about Y."

**Paragraph 2 — Mechanism or friction**: What economic force generates the testable prediction? Name the friction (information asymmetry, agency conflict, search friction, regulatory constraint, behavioral bias) and explain the prediction.

**Paragraph 3 — Setting, data, and design**: What setting allows you to test this? What makes identification credible? Name the data sources.

**Paragraph 4 — Main findings with magnitudes**: State the result quantitatively. "We find that X increases Y by Z%, which represents [economic benchmark]." Include one or two secondary findings.

**Paragraph 5 — Robustness and mechanism in brief**: Two to three sentences on why the result is robust and what mechanism evidence supports the interpretation.

**Paragraph 6 — Contribution and closest literature**: Name the 2-3 closest papers. State the specific dimension of differentiation. Use "we contribute to" not "we are the first to" unless verified.

**Paragraph 7 — Broader implication and roadmap**: What is the economic lesson? Brief roadmap of the paper's sections.

## Style rules

- Front-load the contribution. A referee decides whether to engage in the first two pages.
- Use precise, non-promotional language. Replace "novel" with a specific description of what is new. Replace "important" with a specific economic consequence.
- Do not use em dashes. Use commas, parentheses, colons, or separate sentences instead.
- Do not use "crucially," "importantly," "interestingly," or other filler intensifiers.
- Report economic magnitudes, not only sign and significance.
- Make table and figure notes self-contained. A reader who sees only the float should understand it without the body text.
- Follow the LaTeX template float format: `\caption{Title}` → `\label{}\vspace{-2.5ex}` → `\floatnotes{...}` (descriptive note *above* the table/figure body, not below it) → table/figure body. The note goes between the caption and the content.
- Keep footnotes sparse unless the target journal expects them (JREFE uses footnotes more freely).
- Avoid giant generic literature dumps.
- Do not promise more than the design can support.
- Use active voice for the paper's own contributions and passive or third person for prior work.

## Paper length targets

All page counts assume double-spaced, 12-point font (the LaTeX template default). These are norms, not hard limits. Prioritize substance over hitting a number, but flag when a draft is running significantly long or short.

### Finance track (JF, JFE, RFS)

Total: **40-50 pages** including tables, figures, and references.

| Section | Pages | Notes |
|---|---|---|
| Introduction | 4-6 | 7 paragraphs. The entire pitch in ~5 pages. |
| Related Literature | 2-4 | Strand-based, not a laundry list. Can be folded into the intro for shorter papers. |
| Data & Variables | 3-5 | Sample construction, key variables, summary stats table reference. |
| Empirical Design | 2-4 | Specification, identifying variation, threats. |
| Main Results | 4-6 | Baseline + magnitude interpretation. |
| Robustness & Additional | 3-5 | Grouped by threat. Cut low-information checks first if too long. |
| Mechanism / Heterogeneity | 2-4 | Only if the paper has a mechanism story. |
| Conclusion | 1-2 | No new results. Forward-looking. |
| References | 3-5 | Typically 40-70 references. |
| Tables & Figures | 8-15 | Usually 8-12 tables, 2-5 figures. Placed after references. |

JF and RFS tend toward the shorter end (~40-45 pages). JFE accommodates slightly longer papers (~45-55).

### JFQA / RoF

Total: **35-50 pages**. JFQA is compact. RoF accommodates cross-disciplinary and emerging topics.

### Real-estate track (REE, JREFE, JHE, RSUE)

Total: **35-55 pages** including tables, figures, and references.

| Section | Pages | Notes |
|---|---|---|
| Introduction | 3-5 | Can be slightly shorter than finance track. |
| Institutional Background | 2-4 | RE journals expect more institutional detail than finance journals. |
| Related Literature | 2-3 | |
| Data & Variables | 4-6 | More detailed than finance track. Include maps if spatial. |
| Empirical Design | 2-4 | |
| Results | 4-6 | |
| Robustness | 2-4 | |
| Conclusion | 1-2 | |
| References | 2-4 | Typically 30-60 references. |
| Tables & Figures | 8-15 | Maps count as figures. RE papers often have more figures than finance papers. |

REE and RSUE tend shorter (~35-45). JREFE allows more length (~40-55).

### Internet Appendix

If the paper exceeds the target range, move supplementary tables, additional robustness, variable definitions, and data-construction details to an Internet Appendix. The main paper should be self-contained without it. Reference IA tables as "Table IA.1" etc.

### When the draft is too long

Cut in this order:
1. Robustness checks that do not map to a named threat
2. Heterogeneity splits without a prior reason
3. Redundant tables (e.g., three versions of the same test with minor variations)
4. Literature review paragraphs that cite papers without differentiating them
5. Data section detail that belongs in the codebook or appendix

### When the draft is too short

The paper may be under-developed. Check:
1. Is the mechanism section missing or thin?
2. Are magnitudes discussed and benchmarked?
3. Is there a robustness section with threat-mapped checks?
4. Does the intro have all 7 paragraphs?
5. Are table/figure notes self-contained and informative?

## Abstract writing

**Finance track (JF/JFE/RFS)**: ~100 words. Structure: question, design, main finding with magnitude, implication. No citations, no "this paper" opening.

**JFQA**: ~100 words. Compact. Similar constraints to JF/JFE/RFS.

**RoF**: Up to 150 words. Slightly more room for context and cross-disciplinary framing.

**REE**: ~100 words, italicized, readable by a layperson, independent of the paper.

**JREFE**: 150-250 words with keywords. More room for method and data description.

## Title generation

Good titles in finance are:
- Specific enough to convey the finding or question
- Short (ideally under 12 words)
- Free of jargon that only insiders would understand

Generate 3-5 options ranging from descriptive to evocative. Flag which style fits which journal.

## Results section prose

Follow the interpretation protocol from the finance-empirical-analysis skill:
1. State the result
2. Name the specification
3. Quantify the magnitude
4. Interpret cautiously
5. State the limit

Do not narrate columns ("Column 1 shows...Column 2 shows..."). Lead with the economic point.

When discussing statistical significance in text, reference the t-statistic: "the coefficient is -0.013 (t = -4.36)" not "the coefficient is -0.013 (SE = 0.003)" or "p < 0.01". Tables should report t-statistics in parentheses below coefficients.

## Conclusion writing

- 1-2 pages maximum.
- Restate the question and main finding, but add something new: the economic lesson, the policy implication, or the open question for future work.
- Do not introduce new results or merely summarize the paper.
- End with the forward-looking implication.

## Required deliverables

Produce one or more of:
- manuscript outline
- introduction (using the 7-paragraph structure)
- abstract (journal-targeted word count)
- results section prose (using interpretation protocol)
- conclusion
- title options (3-5)
- contribution paragraph

Use assets/introduction-skeleton.md when building from scratch.

## LaTeX template — write to file, not to chat

When starting a new paper from scratch, copy the `latex_template/` folder into the project's `paper/` directory. It contains:
- `academic_paper_template.tex` — full paper structure matching the section sequence above, with blind-review toggle, `jf.bst` bibliography style, example tables/figures, and appendix
- `template_references.bib` — sample `.bib` file (replace with output from `export_citations`)
- Example images in `images/` (histograms, binned scatter, heterogeneity plot)

Before writing any section, read `latex_template/academic_paper_template.tex` to understand the template's structure and custom commands. Follow the float format specified in CLAUDE.md.

**Write directly to the `.tex` file.** Do not put LaTeX content in the chat. Instead:
1. Read the current `.tex` file (either the template or the user's working paper).
2. Identify the `\section{}` block to update.
3. Use the Edit tool to write the drafted prose directly into the corresponding section of the `.tex` file.
4. If the paper `.tex` file does not exist yet, copy the template and then edit it.

The template sections (Introduction, Related Literature, Data, Empirical Design, Results, Robustness, Conclusion, Appendix) align with the writing workflow above.

## Output format

Write all LaTeX content directly to the `.tex` file in the project's `paper/` directory. In the chat, provide only:
```
# Draft summary
## Target journal or track
## Title options (3-5)
## What was written (section names and brief description)
## Claims to soften (list any overclaims found)
## File path where content was written
```

## Tool integration (Corbis MCP)

### Contribution verification
- `search_papers` (query: the paper's core claim, `matchCount: 10`) → verify novelty claims before writing "we contribute to" or "we are the first to."
- `top_cited_articles` (journals: target journals) → find the most-cited papers in the target field to position the contribution against the field's most influential work.
- `get_paper_details` (paper IDs of closest papers) → read abstracts to write accurate differentiation language.

### Citation management
- `format_citation` (paper ID, style: `apa` or `chicago`) → generate properly formatted individual citations during writing.
- `export_citations` (list of paper IDs, format: `bibtex`) → batch export the paper's full reference list. Offer this after drafting any section that introduces new citations.

### Context and magnitudes
- `search_papers` (query: comparable empirical findings, `minYear: 2015`) → find benchmark magnitudes to contextualize the user's results (e.g., "our estimate of X% is comparable to Y (2020) who find Z% in a related setting").
- `fred_series_batch` (relevant macro series) → pull aggregate statistics for motivation paragraphs (e.g., "the U.S. housing market represents $X trillion...").

### Author identity (for submission prep)
- `find_academic_identity` (author name) → look up coauthor profiles when needed for submission systems.

## Reference files
Read if needed:
- references/journal-targets.md
- references/writing-norms.md

## Guardrails

- Do not write like a grant proposal, consultant memo, or blog post.
- Do not leave the identification logic implicit in the introduction.
- Do not use "first" or "novel" casually — verify via search if possible.
- If the paper's contribution is still muddy, say that before polishing sentences.
- Do not use buzzwords ("game-changing," "groundbreaking," "paradigm-shifting").
- Do not begin the abstract with "This paper" — lead with the question or finding.
- If asked to write the full introduction, produce all 7 paragraphs, not a summary.

## Example prompts
- "Write a JFE-style introduction from these notes."
- "Turn this results table into RFS-style prose."
- "Draft the abstract and contribution paragraph for a Real Estate Economics submission."
- "Give me 5 title options for this mortgage default paper."
- "Rewrite this conclusion to be more forward-looking."
