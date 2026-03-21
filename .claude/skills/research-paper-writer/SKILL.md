---
name: research-paper-writer
description: "Draft and polish every section of a finance or real-estate paper in top-journal style. Use for introductions, literature reviews, data sections, empirical design, results, robustness, mechanism, conclusions, abstracts, titles, and journal-targeted prose."
---

# Research Paper Writer

Draft every section of an empirical finance or real-estate paper: introduction, related literature, institutional background, data, empirical design, results, robustness, mechanism, conclusion, abstract, and internet appendix. Write like a serious empirical researcher aiming at a skeptical editorial process.

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

## Theory and model sections

When the paper includes a theoretical model:
- Lead every discussion of model components with the economic story. Place Greek letters and notation in parentheses after the intuitive explanation.
- BAD: "When $\gamma > \bar{\gamma}$, the equilibrium shifts to full separation."
- GOOD: "When the information precision of informed traders (γ) exceeds a threshold (γ̄), uninformed traders exit the market entirely, and the equilibrium shifts to full separation."
- Introduce each parameter by its economic role before assigning it a symbol.
- State propositions and predictions in plain language first. Reference the formal result (Proposition 1, Equation 3) afterward.
- The reader should be able to follow the model's logic from prose alone. Notation confirms; it does not carry the argument.

## Style rules

- Front-load the contribution. A referee decides whether to engage in the first two pages.
- Use precise, non-promotional language. Replace "novel" with a specific description of what is new. Replace "important" with a specific economic consequence.
- Do not use em dashes. Use commas, parentheses, colons, or separate sentences instead.
- Do not use "crucially," "importantly," "interestingly," or other filler intensifiers.
- Report economic magnitudes, not only sign and significance.
- Make table and figure notes self-contained. A reader who sees only the float should understand it without the body text.
- Follow `references/latex-formatting-reference.md` for all float structure, table templates, figure templates, equation formatting, and custom commands. Read it before writing any LaTeX.
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
3. Quantify the magnitude (use the three-tier approach: statistical units → real-world units → anchored comparison to a familiar quantity the reader already grasps)
4. Interpret cautiously
5. State the limit

Do not narrate columns ("Column 1 shows...Column 2 shows..."). Lead with the economic point. When quantifying magnitude, the reader should immediately understand whether the effect is large or small without looking up sample statistics.

When discussing statistical significance in text, reference the t-statistic: "the coefficient is -0.013 (t = -4.36)" not "the coefficient is -0.013 (SE = 0.003)" or "p < 0.01". Tables should report t-statistics in parentheses below coefficients.

## Conclusion writing

- 1-2 pages maximum.
- Restate the question and main finding, but add something new: the economic lesson, the policy implication, or the open question for future work.
- Do not introduce new results or merely summarize the paper.
- End with the forward-looking implication.

## Related literature section

Organize by strand, disagreement, or mechanism, not by topic label. A literature review is not a bibliography; it is an argument that builds toward the contribution.

**Structure**: 3-5 strands, each covering a coherent line of work. For each strand:
1. Name the strand and its central question or tension
2. Cite the key papers and state what they found (synthesize, do not enumerate)
3. Identify the specific gap, limitation, or disagreement this paper addresses
4. Explain how this paper advances the strand

**Writing rules**:
- Do NOT write "Author (Year) study X. Author (Year) study Y." sequentially. Synthesize: "A growing literature examines X, finding that [summary of collective evidence] (Author 2019; Author 2020; Author 2021). However, these studies share a common limitation: [gap]."
- End each strand by connecting back to the current paper's contribution
- Use "we contribute to" or "we extend," never "we are the first to" unless verified via literature search
- The final strand should be the closest literature, where you make the sharpest differentiation
- If a `literature-positioning-map` deliverable exists (check `notes/project_state.md`), use its closest-papers list and contribution claim as starting inputs

**Length**: Finance track: 2-4 pages. RE track: 2-3 pages. Can be folded into the introduction for shorter papers (common at JF and RFS).

## Institutional background section

Include when the institutional setting is central to identification or unfamiliar to the target audience.

**When to include**:
- Required for most RE papers (RE journals expect institutional detail)
- Required when the design exploits a regulation, policy change, or institutional feature the reader may not know
- Optional for corporate finance if the setting is well-known (e.g., standard SEC filings, NYSE listing rules)
- Optional if the institutional detail fits naturally in the introduction and design sections

**Structure**:
1. Describe the institution, market, or regulation in enough detail that a non-specialist can follow the design
2. Explain why the institution creates useful variation for identification
3. If the design relies on a policy change or shock: include a timeline of key events with dates
4. Connect to the empirical design: "This feature of [institution] allows us to..."

**Writing rules**:
- Cite primary sources (regulatory filings, government reports, statute text) not just other papers that describe the institution
- Use plain language. The institutional section is where you teach the referee about the setting.
- Include a timeline figure or table if the event sequence is complex (reference `research-figure-design` for the figure)
- Do not editorialize about the institution's merits or problems. Describe it factually.

**Length**: Finance track: 1-2 pages. RE track: 2-4 pages.

## Data and variables section

**Structure**: data sources → sample construction → key variable definitions → summary statistics discussion.

### Data sources paragraph
Name each data source, what it provides, the sample period, and how sources are linked. Mention the identifiers used for merging (PERMNO, GVKEY, CUSIP, FIPS, etc.). If a source requires special access or has known limitations, state that.

### Sample construction
Describe filters and exclusions with observation counts at each step. Reference a sample-flow table if one exists (see `python-empirical-code` skill's `SampleTracker`). Justify each filter: "We exclude financial firms (SIC 6000-6999) because their leverage ratios are not comparable to non-financial firms."

### Key variable definitions
Define the treatment variable, outcome variable, and main controls. Provide the exact formula for constructed variables. Reference the codebook or appendix variable-definitions table for the full list: "Complete variable definitions are in Appendix Table A1."

### Summary statistics discussion
Do NOT just say "Table 1 reports summary statistics." Highlight features that matter for the analysis:
- Is the treatment variable balanced? What fraction of the sample is treated?
- Are outcome variables skewed, censored, or zero-inflated?
- How does the sample compare to the universe (e.g., "our sample covers 78% of total market capitalization")?
- Flag anything the reader should know: high missingness, ceiling effects, or unusual distributions

If a `finance-data-construction` plan exists (check `notes/project_state.md`), reference its codebook and merge plan as inputs.

**Length**: Finance track: 3-5 pages. RE track: 4-6 pages (RE journals expect more data detail). For RE papers with spatial data, describe geographic coverage, geocoding method, and spatial resolution.

## Empirical design section

**Structure**: identification challenge → source of variation → specification → threats and how they are addressed.

### Identification challenge
Start by stating what makes the question hard to answer in plain language. Name the specific endogeneity concern: "The main challenge is that firms that choose to [action] differ systematically from firms that do not, so a naive comparison would conflate [confound] with the effect of [treatment]."

### Source of variation
Describe the source of exogenous (or quasi-exogenous) variation and why it is plausible. Be specific: name the shock, the regulation, the natural experiment.

### Specification
Write the main specification as a numbered equation using `\textit{}` for variable names:
```latex
\begin{equation}
\textit{Outcome}_{i,t} = \beta \, \textit{Treatment}_{i,t} + \gamma' X_{i,t} + \alpha_i + \delta_t + \varepsilon_{i,t}
\label{eq:baseline}
\end{equation}
```
After the equation, define every variable and subscript. State what $\beta$ identifies and under what assumptions.

### Threats and diagnostics
Discuss the key identifying assumption and what would violate it. Map each threat to a specific diagnostic that will appear in the robustness section. This creates forward pointers: "We address this concern in Section V.B."

If a `finance-identification-design` memo exists (check `notes/project_state.md`), translate its threat map into prose.

**Design-specific guidance**:
- **DiD**: Explicitly state the parallel-trends assumption. Preview the pretrend test and event-study figure. If staggered, discuss whether TWFE is appropriate or if a modern estimator (Callaway-Sant'Anna, Sun-Abraham) is needed.
- **IV**: State the exclusion restriction in words. Preview the first-stage F-statistic. Discuss instrument relevance and validity separately.
- **RD**: State the continuity assumption. Preview the McCrary density test and bandwidth choice. Specify local polynomial order and kernel.
- **Event study**: Define the event window, estimation window, and any exclusions. State what "normal returns" means in the context.

**Length**: Finance track: 2-4 pages. RE track: 2-4 pages.

## Main results section

**Structure**: baseline result → economic magnitude → secondary results → subsample or extension results.

### Baseline result
Each table gets 1-2 paragraphs. Lead with the economic finding, not the table number.
- BAD: "Table 3 reports the results of our baseline regression."
- GOOD: "Firms experiencing covenant violations reduce R&D spending by 12% relative to the pre-violation mean."

### Per-result protocol
For each result, follow the 5-step interpretation protocol:
1. **State the result**: the sign, magnitude, and significance of the coefficient of interest
2. **Name the specification**: what controls, fixed effects, and clustering are included
3. **Quantify the magnitude** using three tiers:
   - *Statistical units*: "a one-standard-deviation increase in X is associated with a β-unit change in Y"
   - *Real-world units*: "this translates to a $2.3 million reduction in annual R&D spending for the average firm"
   - *Anchored comparison*: "equivalent to 15% of the sample-mean R&D budget, or roughly the annual salary of three research scientists"
4. **Interpret cautiously**: what does the estimate mean economically? What should the reader take away?
5. **State the limit**: what can this specification not rule out?

### Across-column discussion
When multiple columns show the same test with different controls or fixed effects:
- Discuss what adding each control does to the estimate and why
- If the coefficient is stable, say so: "The estimate is stable across specifications, suggesting that [omitted variable] is not driving the result."
- If the coefficient changes, explain: "Adding industry-year fixed effects reduces the estimate from X to Y, consistent with [industry-level confound] explaining part of the association."
- Identify the preferred specification and explain why

### Connecting results to the story
After presenting the baseline, connect back to the mechanism and prediction from the introduction. The results section is not just a table narration; it is part of the paper's argument.

**Length**: Finance track: 4-6 pages. RE track: 4-6 pages.

## Robustness section

Organize by threat, not by table number. Each subsection addresses one specific concern about the baseline result.

**Structure per threat**:
1. Name the threat: "One concern is that [specific confound or alternative explanation]."
2. Explain why it matters: "If [threat], the baseline estimate would be biased [direction] because [logic]."
3. Describe the test: "To address this, we [specific test]."
4. Report the result: "Table X shows that [result], inconsistent with this concern."

**Writing template**: "If [threat], we would expect [pattern]. Table X shows [result], [consistent/inconsistent] with this concern."

**Common subsection order**:
1. Alternative specifications (different controls, fixed effects, functional form)
2. Alternative samples (excluding certain observations, different time periods)
3. Placebo and falsification tests (fake treatment timing, fake treatment groups)
4. Sensitivity to outliers and measurement
5. Additional controls for specific confounds

**Rules**:
- Do NOT present an undifferentiated list of robustness checks with no motivation
- Every check must be tied to a specific threat. If you cannot name the threat, cut the check.
- Keep language crisp. This section should move quickly.
- Move low-priority checks to the Internet Appendix
- If a `finance-empirical-analysis` threat map exists (check `notes/project_state.md`), use its threat-to-diagnostic mapping as the section outline

**Length**: Finance track: 3-5 pages. RE track: 2-4 pages.

## Mechanism and heterogeneity section

### Mechanism tests
Mechanism tests must have clear logic linking the channel to a testable prediction.

**Structure per mechanism test**:
1. State the channel: "If the effect operates through [channel A]..."
2. State the testable implication: "...we expect [specific prediction that distinguishes A from B]."
3. Describe the test: "We test this by [method]."
4. Report the result: "Consistent with [channel A], we find [result]."
5. Assess what it rules out: "This evidence is inconsistent with [channel B] because [logic]."

**Common mechanism approaches**:
- Intermediate outcomes (does the treatment affect a variable on the causal path?)
- Cross-sectional predictions (is the effect stronger where the channel is more relevant?)
- Timing of effects (does the effect appear when the channel predicts it should?)
- Placebo outcomes (is there no effect on outcomes the channel does not predict?)

### Heterogeneity
- Do NOT present heterogeneity as mechanism unless there is an explicit economic reason why the cross-sectional variation maps to the proposed channel
- Every heterogeneity split needs a prior reason stated before the results. "We expect the effect to be stronger for [subgroup] because [economic logic]."
- Do not present every possible sample split. Three to five motivated splits is typical.
- If heterogeneity is the main result (not supporting evidence), structure it as a main results section

**Length**: Finance track: 2-4 pages. RE track: 2-4 pages.

## Internet appendix

**When to use**: The main paper exceeds the target page range, or supplementary material is informative but not essential for the core argument.

**Standard contents**:
- Additional robustness tests not in the main paper
- Variable definitions table (if too long for the main text)
- Data construction details (merge procedures, filter justifications)
- Additional subsamples or time-period splits
- Alternative specifications or variable definitions
- Proofs or model derivations (if a theory section is included)

**Formatting**:
- Number tables as "Table IA.1", "Table IA.2", etc.
- Number figures as "Figure IA.1", etc.
- Reference from the main text: "We report additional results in the Internet Appendix (Table IA.3)."
- The main paper must be self-contained without the IA. A reader who never opens the IA should still find the paper complete and convincing.

## Required deliverables

Produce one or more of:
- manuscript outline
- introduction (using the 7-paragraph structure)
- related literature section (strand-based, contribution-building)
- institutional background section (for RE papers or unfamiliar settings)
- data and variables section (sources, construction, summary stats discussion)
- empirical design section (challenge, variation, specification, threats)
- main results section (using 5-step interpretation protocol)
- robustness section (organized by threat)
- mechanism and heterogeneity section (channel logic, not kitchen-sink splits)
- abstract (journal-targeted word count)
- conclusion
- internet appendix content
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
- "Write the data section for my CRSP-Compustat panel."
- "Draft the empirical design section for my DiD paper."
- "Write the related literature section organized by strand."
- "Draft the mechanism section explaining why the effect operates through information asymmetry."
- "Write the robustness section addressing the three threats from my design memo."
