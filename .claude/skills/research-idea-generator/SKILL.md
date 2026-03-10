---
name: research-idea-generator
description: "Generate novel research ideas in finance and real estate using ten structured heuristic lenses. Use for brainstorming sessions, topic exploration, and creative idea development."
---

# Research Idea Generator

Generate 10 ranked research ideas from a topic area using structured heuristic lenses. This skill is a generator, not a filter. Use `finance-idea-screening` (via `/idea`) to evaluate the best candidates after generation.

## Ten idea-generation lenses

Each lens is a distinct heuristic for producing ideas. Apply all ten to the user's topic area. Not every lens will yield a strong candidate for every topic; that is expected. The goal is breadth of attack, not uniformity.

### Lens 1: Literature gap

Find questions that survey papers, handbook chapters, or literature reviews flag as open, understudied, or needing new data. The gap must be economically meaningful, not just "nobody has run this regression."

- Search for recent surveys or reviews in the topic area.
- Read "future research" directions and "open questions" sections.
- Ask: is the gap real, or has it been filled since the survey was published?

### Lens 2: Conflicting findings

Two credible papers reach opposite conclusions on the same question. The reconciliation is the idea. The moderating variable, sample difference, or identification flaw that explains the conflict becomes the contribution.

- Search for the core empirical finding in the topic.
- Look for papers that challenge or contradict the finding.
- Ask: what explains the disagreement? Is it a sample, method, or mechanism difference?

### Lens 3: Cross-pollination

Borrow a well-established concept, method, or finding from one field and apply it to another where it has not been used. The best cross-pollination ideas generate a genuinely different economic prediction in the new setting, not just "X but in field Y."

- Identify a powerful insight from a neighboring field (labor, IO, macro, behavioral, urban).
- Ask: does this insight have an untested analog in the user's topic area?
- The test: does the imported concept generate a new prediction that insiders in the target field have not considered?

### Lens 4: First principles / economic logic

Start from a fundamental friction (information asymmetry, moral hazard, search costs, limited attention, regulatory distortion, market segmentation) and derive a testable prediction. Then check whether anyone has tested it.

- Name the friction explicitly.
- State the prediction in one sentence.
- Search to verify the prediction has not been tested.
- The best first-principles ideas feel obvious in retrospect but have not been documented.

### Lens 5: New data x old question

Pair a recently available or underexploited data source with a classic question that was previously hard to answer. The data must enable a genuinely better answer, not just a replication with shinier data.

- Identify new or expanding data sources: satellite imagery, web-scraped data, administrative records, fintech/neobank transaction data, NLP/LLM-processed text from filings, alternative workforce data (Revelio, Burning Glass), high-frequency geolocation data, social media signals.
- Identify a classic question in the topic area that lacked the right data.
- Ask: does this data source enable a new identification strategy, a new measurement, or a new population, not just a new time period?

### Lens 6: Mechanism decomposition

Take an established empirical result and ask: what is the economic channel? Can you distinguish between competing mechanisms? Many highly cited papers document effects without pinning down why. The mechanism paper is often higher-impact than the documentation paper.

- Use `top_cited_articles` to find seminal papers in the topic.
- Read the paper's mechanism discussion: is it hand-wavy or well-identified?
- Ask: what test would distinguish mechanism A from mechanism B? Is that test feasible?

### Lens 7: Boundary conditions

When does a canonical finding break down? The failure of a well-known result in an economically meaningful dimension IS the idea. Heterogeneity that maps to a theory is a contribution; heterogeneity that is just subsample analysis is not.

- Identify the canonical finding in the topic area.
- Ask: does it hold across market conditions (bull/bear, high/low volatility, crisis/calm), firm types (constrained/unconstrained, public/private), investor types (retail/institutional), or institutional settings (countries, regulatory regimes)?
- The boundary condition must connect to an economic explanation, not just be an empirical fact.

### Lens 8: Policy / regulatory shock

A recent policy change, regulatory reform, or institutional event creates a natural experiment for a question that was previously unidentifiable. The policy is the instrument, not the contribution. The question must be bigger than the policy.

- Identify recent (past 3-5 years) policy changes relevant to the topic: Dodd-Frank amendments, SEC rule changes, tax reforms, ESG disclosure mandates, CFPB actions, Fed facility changes, zoning reforms, Opportunity Zones, TCJA provisions, EU regulations.
- Ask: what economic question does this shock help answer? Is the question first-order?
- Search to see whether the shock has already been exploited.

### Lens 9: Model meets data

Theoretical or structural models make quantitative predictions that have not been tested empirically. The paper tests the prediction, potentially rejecting or refining the model.

- Search for theory papers in the topic (especially recent ones from top-5 journals).
- Identify predictions that are stated in the model but absent from the empirical record.
- Ask: is the prediction testable with available data? What would rejection mean for the theory?

### Lens 10: Unification

Multiple individually documented findings are manifestations of the same underlying economic force. The synthesis is the paper. This lens produces the highest-impact ideas but requires the deepest knowledge of the literature.

- List 3-5 individually well-known findings in the topic area.
- Ask: is there a single friction, mechanism, or equilibrium force that explains all of them?
- The unification must generate a new testable prediction that none of the individual papers delivers.

## Screening workflow

1. **Gather user input.** The user provides a topic area and optional constraints (data access, method preferences, journal target, coauthor expertise). If the topic is too broad (e.g., "finance"), ask the user to narrow to a subfield.

2. **Map the landscape.** Run 3-4 initial Corbis searches to understand the current state of the field:
   - `top_cited_articles` (field and topic) to identify seminal papers
   - `search_papers` (broad topic query, `matchCount: 15`) to find recent work
   - `search_papers` (same topic, `minYear: 2023`) to catch the current frontier
   - `search_papers` (topic + "survey" or "review") to find survey papers

3. **Apply all ten lenses.** For each lens, generate 1-2 candidate ideas. Use additional `search_papers` calls as needed to verify novelty. Not every lens will produce a viable idea for every topic; skip lenses that yield nothing and note why.

4. **Quick-screen each candidate.** For each idea, provide:
   - One-sentence question (question-first framing, never "Using X data...")
   - Lens used to generate it
   - Closest existing paper (from Corbis search)
   - Why it matters (one sentence on the economic importance)
   - Biggest risk (one sentence)
   - Quick viability: **High** / **Medium** / **Low**

5. **Rank and select.** Rank the candidates by (impact potential) x (feasibility). Select the top 10 for the Idea Menu. Break ties in favor of ideas that use non-obvious lenses (cross-pollination, unification, first principles) over straightforward gap-filling.

6. **Produce the Idea Menu.** Use `assets/idea-menu-template.md`. All 10 ideas on one page with the quick-screen fields.

7. **Expand top 3 into Idea Sketches.** For the three highest-ranked ideas, provide a half-page Idea Sketch:
   - One-sentence question
   - Core mechanism or friction (2-3 sentences)
   - Theory-to-evidence bridge (one paragraph: what is the test?)
   - Key data requirements
   - Likely journal track (top-3, strong field, or RE journals)
   - One-sentence skepticism test (what would the toughest referee say?)

8. **Offer next steps.** Suggest running `/idea` on the most promising candidate for full screening, or `/lit-search` to deepen the literature positioning.

## Tool integration (Corbis MCP)

**Never claim an idea is novel without searching first.** Use this sequence:

### Landscape mapping (Step 2)
1. `top_cited_articles` (field: e.g., "corporate finance", topic: e.g., "capital structure") — identify seminal papers the user must know about.
2. `search_papers` (query: broad topic in natural language, `matchCount: 15`) — find the current state of the field.
3. `search_papers` (same query, `minYear: 2023`) — catch the frontier and recent working papers.

### Per-lens novelty checks (Step 3)
- `search_papers` (query: the specific idea in natural language, `matchCount: 10`) — for each candidate idea, verify it has not been done.
- `get_paper_details` (paper IDs from closest results) — read abstracts to confirm overlap vs. vocabulary similarity.

### Data feasibility (Lens 5 and general)
- `search_datasets` (topic keywords) — discover available datasets and coverage.
- `fred_search` (keywords) — find relevant FRED macro series for context or controls.

### After generation
- `export_citations` (format: `bibtex`) — export BibTeX for the closest papers identified during generation. Offer after the Idea Menu is produced.

## Quality standards for generated ideas

A strong generated idea must have ALL of the following:
- A **testable question** stated in one sentence, question-first
- A **named friction or mechanism** (not just a topic or dataset)
- A **plausible theory-to-evidence bridge** (what is the test? what variation is exploited?)
- **Verified novelty** (Corbis search confirms no close existing paper)
- **Data feasibility** (at least one plausible data source identified)

An idea that lacks any of these should be flagged as Low viability or excluded.

## Guardrails

- Do not generate "X but in country Y" or "X but with newer data" ideas. These are setting variations, not contributions, unless the new setting generates a genuinely different economic prediction.
- Do not let a clever dataset or natural experiment substitute for a question. The question must come first.
- Do not generate more than 2 ideas from the same lens. The value of the skill is breadth of attack across multiple heuristics.
- Do not present 10 equally enthusiastic ideas. Rank honestly. Some ideas will be stronger than others. Say so.
- Do not overclaim novelty. If the search reveals a close paper, note it and adjust the contribution claim or drop the idea.
- At least 3 of the 10 ideas must come from non-obvious lenses (cross-pollination, unification, first principles, model meets data). Gap-filling and data-driven ideas are easy to generate but often lower impact.
- Every idea must pass a minimal plausibility check: could this be a seminar paper that changes how people think, or is it just an incremental exercise?

## Preferred outputs

Produce:
1. **Idea Menu** — 10 ranked ideas using `assets/idea-menu-template.md`
2. **Idea Sketches** — expanded treatment of the top 3 ideas
3. **Next-step recommendation** — which idea to screen first and why

## Reference files

Read if needed:
- `references/journal-targets.md` — journal profiles for track recommendations
- `references/empirical-standards.md` — methodological baselines

## Example prompts

- "Brainstorm 10 ideas in behavioral asset pricing."
- "Generate research ideas about climate risk and real estate."
- "I have access to Revelio Labs workforce data — brainstorm ideas in corporate finance."
- "Help me come up with ideas at the intersection of fintech and household finance."
- "Brainstorm ideas about intermediary asset pricing and credit markets."
- "Generate ideas in empirical corporate governance using NLP/LLM methods."
