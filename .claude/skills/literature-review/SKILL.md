---
name: literature-review
description: "Write a comprehensive, structured literature review on a topic. Searches the literature via Corbis, organizes into thematic strands, writes synthesized prose (not paper-by-paper enumeration), and outputs as Markdown, LaTeX section, or standalone LaTeX document with proper BibTeX citations."
---

# Literature Review

Write a comprehensive, structured literature review on a user-specified topic. This skill produces a standalone review of what the field knows, where it disagrees, and what remains open. It is not for positioning a specific paper's contribution (use `literature-positioning-map` for that) or for writing a related-literature section within a manuscript (use `research-paper-writer` for that).

## When to use

- The user wants to survey a topic or research area
- The user wants a literature review for a dissertation chapter, qualifying exam, survey paper, or personal reference
- The user wants to understand the state of knowledge on a question before starting a project

## Inputs to collect

Before starting, confirm these with the user:

| Input | Required? | Default |
|---|---|---|
| Topic or research question | Yes | — |
| Output format: `markdown` / `latex-section` / `latex-standalone` | Yes | `markdown` |
| Scope: `focused` (~25 papers) / `comprehensive` (~50 papers) | No | `comprehensive` |
| Target `.tex` file (if `latex-section`) | If applicable | — |
| Existing `.bib` file path | No | Auto-detect or create new |
| Known key papers to include | No | — |
| Time period filter | No | All years |
| Specific journals to emphasize | No | — |

If the user provides a topic and format in their initial message, proceed without asking. Fill defaults for anything not specified.

## Workflow

### Phase 1: Search and collect

Target ~50 unique papers for comprehensive scope, ~25 for focused scope. Execute searches in this order:

**Step 1 — Foundational work:**
- `top_cited_articles` (field: the broad field name, topic: the specific topic) to find seminal papers.

**Step 2 — Main body of work:**
- `search_papers` (query: the core topic as a natural-language research question, `matchCount: 20`) to find the central literature.

**Step 3 — Thematic angles:**
- `search_papers` (query: first sub-question or thematic angle, `matchCount: 15`)
- `search_papers` (query: second sub-question or thematic angle, `matchCount: 15`)
- If the topic has a third distinct angle, add a third search.

**Step 4 — Recent frontier:**
- `search_papers` (query: core topic, `minYear: 2023`, `matchCount: 15`) to find the latest published and working papers.

**Step 5 — Adjacent or methodological:**
- `search_papers` (query: methodological approach or adjacent field angle, `matchCount: 10`) for breadth.

**Step 6 — Verify and enrich:**
- `get_paper_details` on the top 30-40 unique papers to read abstracts, confirm relevance, and extract key findings.
- Deduplicate across all searches.
- If the user provided known key papers, verify they appear. If not found via search, include them manually and use `get_paper_details` to confirm details.

**Citation-based tiering:** After deduplication, sort all collected papers by `citedByCount` and assign influence tiers:

| Tier | Label | Rule | Treatment in the review |
|---|---|---|---|
| 1 | **Foundational** | Top 5 papers by `citedByCount` OR any paper with 500+ citations | 3-5 sentences each. Describe what they found, how, and why it mattered. These anchor the review. |
| 2 | **Established** | Next 10-15 papers by `citedByCount` OR 100-499 citations | 1-2 sentences each, or grouped into synthesized claims with 2-3 papers per sentence. |
| 3 | **Emerging** | Papers with < 100 citations, especially those published in the last 3 years | Grouped into frontier paragraphs. Cited parenthetically to support collective findings. |

A paper that appears across 3+ separate search queries is likely a network hub. Promote it one tier (e.g., Established to Foundational) regardless of raw citation count.

**Ranking criteria** (for deciding which papers to keep when cutting to target count):
1. Direct relevance to the topic
2. Influence tier (Foundational papers are never cut)
3. Recency (recent work that shifts the field gets priority over older low-citation work)
4. Methodological contribution (papers that changed how the field studies the topic)

### Phase 2: Propose strand structure

After collecting papers, propose 4-6 thematic strands. Present to the user for approval before writing.

**Deliver this structure:**

```
# Proposed Literature Review Structure

## Topic: [user's topic]
## Scope: [focused/comprehensive] — [N] unique papers collected
## Influence tiers: [X] Foundational / [Y] Established / [Z] Emerging

### Proposed strands:

1. **[Strand name]** — [1-sentence description]
   Key papers: [3-5 author-year citations]
   Narrative arc: [what story this strand tells, from early work to current state]

2. **[Strand name]** — [1-sentence description]
   Key papers: [3-5 author-year citations]
   Narrative arc: [story]

3. ...

### Cross-cutting themes:
- [e.g., methodological evolution from X to Y]
- [e.g., a key empirical debate between findings A and B]

### Identified gaps:
- [Gap 1: what the literature has not addressed]
- [Gap 2: where findings conflict without resolution]

### Papers that don't fit neatly:
- [Paper] — could go in strand X or Y; recommend [placement]
```

**Strand organization principles** (in order of preference):
1. **By debate or tension** — group papers by which side of a disagreement they support
2. **By mechanism or channel** — group papers by the economic force they emphasize
3. **By methodology** — group papers by empirical approach when methodology drives different answers
4. **Chronological within strands** — within each strand, order foundational work first, then development, then frontier

Never organize by topic label alone ("this literature relates to X, Y, and Z" with no internal structure).

**Checkpoint**: Wait for user approval or modifications. Do not proceed to writing until the user confirms the strand structure.

### Phase 3: Write the review

#### Per-strand writing protocol

For each strand, write in this order:

1. **Opening frame** (1-2 sentences): State the strand's central question or contribution to understanding the topic. Why does this line of work exist?

2. **Foundational work** (Tier 1 papers, 3-5 sentences each): Describe the key papers that anchor this strand. These get the most individual attention. State what they found, how they found it, and why it mattered. Do not mention citation counts in the review prose; let the depth of treatment signal the paper's importance. Citation counts belong in the reading list, not in the narrative.

3. **Established evidence** (Tier 2 papers, synthesized, not enumerated): Group the body of work by finding, not by author. Write about what the literature collectively shows, with citations supporting claims. Example:
   - GOOD: "Subsequent work established that credit constraints amplify housing cycles, with effects concentrated among low-income borrowers (Author 2015; Author 2017) and in regions with inelastic housing supply (Author 2016; Author 2019)."
   - BAD: "Author (2015) studies credit constraints and housing. Author (2016) studies housing supply elasticity. Author (2017) also studies credit constraints."

4. **Recent frontier** (Tier 3 papers, 2-3 sentences): What has the last 2-3 years added? New data, new methods, new findings that shift understanding? These papers may have low citation counts simply because they are new.

5. **Gaps, tensions, or open questions** (1-2 sentences): What does this strand leave unresolved? Where do findings conflict? What has not been studied?

6. **Transition** (1 sentence): Connect to the next strand.

#### Cross-strand synthesis section

After all strands, write a synthesis section covering:
- What the literature collectively establishes (the consensus, if any)
- Where findings conflict or remain ambiguous (unresolved debates)
- Methodological limitations shared across studies
- Open questions and promising directions for future work

#### Writing rules

Follow all project writing norms (`references/writing-norms.md`, `references/banned-words.md`):

- **Synthesize, do not enumerate.** The review should read as a narrative about a field, not as a list of papers.
- **Cite to support claims, not to name-drop.** Every citation should back a specific point.
- **No filler intensifiers.** Do not use "importantly," "crucially," "interestingly," "notably."
- **No em dashes.** Use commas, parentheses, colons, or separate sentences.
- **No promotional language.** Do not use "novel," "groundbreaking," "seminal" (even for truly seminal papers, describe what they did instead of labeling them).
- **Precise language.** Replace vague claims ("many papers study X") with specific ones ("a large body of work, beginning with Author (Year), examines X").
- **Gap claims require evidence.** Do not write "no one has studied X" or "the literature is silent on X" unless the search results support this. Prefer "to our knowledge, based on [N] papers reviewed" or simply describe what has been studied and let the gap speak for itself.
- **Seminal papers get more space.** 2-4 sentences for foundational work. Supporting papers get grouped into synthesized claims with parenthetical citations.
- **Conflict is valuable.** When papers disagree, describe both sides fairly and note what might explain the disagreement (different samples, methods, time periods, settings).

### Phase 4: Citations and output

#### Citation handling

After writing the review:

1. Collect all paper IDs cited in the review.
2. `export_citations` (list of paper IDs, format: `bibtex`) to generate BibTeX entries.
3. Check for an existing `.bib` file:
   - If the user specified one, read it and append new entries (skip duplicates by checking cite keys).
   - If none specified, look for `*.bib` files in the project. If found, ask the user which to use.
   - If no `.bib` exists, create one:
     - `markdown` format: `notes/literature_review_references.bib`
     - `latex-section` format: same directory as the `.tex` file
     - `latex-standalone` format: `paper/literature_review/references.bib`
4. Write the `.bib` file.

For papers where `export_citations` does not return a result (e.g., the paper was mentioned by the user but not found in Corbis), construct a manual BibTeX entry from known information and flag it for the user to verify.

#### Output by format

**Markdown** (`markdown`):
- Write to `notes/literature_review_[topic_slug].md`
- Use standard Markdown headers for strands
- Use parenthetical author-year citations: (Author, Year)
- Include the reading list (see below) at the end
- Append the `.bib` file path at the bottom for reference

**LaTeX section** (`latex-section`):
- Read the target `.tex` file
- Insert the review at the location specified by the user (or find an appropriate `\section{}` marker)
- Use `\citet{}` for textual citations ("Author (Year) finds...") and `\citep{}` for parenthetical citations ("...as shown in prior work \citep{author2020}")
- Append new entries to the existing `.bib` file
- Use Edit tool, not Write tool, to insert into existing files

**LaTeX standalone** (`latex-standalone`):
- Copy `latex_template/` to `paper/literature_review/` if it does not exist
- Read the template `.tex` file to understand its structure
- Replace the title with "Literature Review: [Topic]"
- Replace the abstract with a 100-word summary of the review's scope and key findings
- Write the review body into the appropriate sections
- Create `references.bib` in the same directory
- Ensure `\bibliography{references}` points to the correct file

#### Reading list

For all output formats, also produce a reading list using `assets/reading-list-template.md`. This is a curated table of the 10-15 most important papers with one-line descriptions of their key contributions.

- Write to `notes/reading_list_[topic_slug].md`
- Organize into: Foundational papers (5-7), Recent frontier (4-5), Methodological advances (2-3)

### Phase 5: Log and state

**Lab notebook**: Append an entry to `notes/lab_notebook.md`:
```markdown
---

### [DATE] — Literature Review: [Topic]

**What was done**: Comprehensive literature review on [topic]. Searched [N] papers via Corbis, reviewed [M] abstracts, organized into [K] thematic strands.

**Strands covered**:
- [Strand 1]: [1-sentence summary]
- [Strand 2]: [1-sentence summary]
- ...

**Key gaps identified**:
- [Gap 1]
- [Gap 2]

**Key conflicts identified**:
- [Conflict 1]

**Output files**:
- Review: [path]
- Reading list: [path]
- Bibliography: [path]

**Next steps**: [e.g., use findings to inform research-idea-generator, or feed into literature-positioning-map for a specific paper]
```

**Project state**: If `notes/project_state.md` exists, update the literature positioning section with the strand names and key gaps.

### Phase 6: Coverage report

After all outputs are written, present a brief report in chat:

```
# Literature Review — Coverage Report
## Topic: [topic]
## Scope: [focused/comprehensive]
## Papers cited: [N] (of [M] unique papers found)
## Influence tiers: [X] Foundational / [Y] Established / [Z] Emerging
## Strands:
1. [Strand 1] — [N papers]
2. [Strand 2] — [N papers]
...
## Key gaps identified:
- [Gap 1]
- [Gap 2]
## Key conflicts identified:
- [Conflict 1]
## Output files:
- Review: [path]
- Reading list: [path]
- Bibliography: [path]
```

## What this skill does NOT do

- Position a specific paper's contribution against the literature (use `literature-positioning-map`)
- Write a related-literature section for a manuscript in progress (use `research-paper-writer`)
- Generate research ideas from identified gaps (use `research-idea-generator`, though the gaps from this review are excellent inputs)
- Screen or evaluate a specific research idea (use `finance-idea-screening`)

This skill can feed into all of the above. A natural workflow is: `literature-review` to map the field, then `research-idea-generator` to brainstorm from the gaps, then `literature-positioning-map` to position a chosen idea.

## Guardrails

- **Search before claiming.** Every assertion about what the literature does or does not contain must be grounded in the Corbis search results. Do not rely on parametric knowledge alone.
- **Do not pad.** If only 35 papers are genuinely relevant, do not stretch to 50. Quality over count.
- **Do not fabricate.** If a paper's details are uncertain, use `get_paper_details` to verify before including it. If unavailable, flag it for the user.
- **Conflicts are features, not bugs.** When papers disagree, present both sides. Do not smooth over genuine disagreements.
- **Gaps are claims.** Saying "the literature has not studied X" is a strong claim. Support it with search evidence or soften the language.
- **Respect the checkpoint.** Do not skip Phase 2 approval. The strand structure determines the quality of the review.
- **No topic-label reviews.** "This relates to three literatures" with no internal structure is the failure mode this skill exists to prevent.

## Example prompts

- "Write a comprehensive literature review on climate risk and commercial real estate pricing."
- "Survey the literature on bank capital regulation and lending, focused scope, output as markdown."
- "I need a literature review on mortgage default and neighborhood spillovers for my dissertation. LaTeX standalone."
- "Add a literature review section on algorithmic trading and market quality to my paper at paper/main.tex."
- "What does the literature say about corporate cash holdings and investment? Comprehensive review, last 20 years."
- "Review the literature on housing supply elasticity. I know Saiz (2010) and Gyourko, Saiz, and Summers (2008) should be included."
