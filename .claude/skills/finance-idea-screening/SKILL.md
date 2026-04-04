---
name: finance-idea-screening
description: "Screen and refine research ideas in corporate finance, investments, asset pricing, and real estate. Use for brainstorming, novelty checks, contribution framing, and journal-fit triage."
---

# Finance Idea Screening

Turn rough topics into credible paper ideas or kill weak ideas early.

## Stage 0: Desk-editor screen

Before running the full literature search and scoring workflow, answer four questions in 1-2 sentences each:

1. **Prior-changing:** What broad finance prior would change if this paper is right?
2. **Zero-result value:** Why would the paper still matter if the main estimate is zero or the sign flips?
3. **Question over method:** Is the question more important than the shock, instrument, or dataset?
4. **Desk read:** Could this clear a JF/JFE/RFS desk read today?

If two or more answers are weak, return **Revise** or **Kill** before investing in the full search chain.

**Framing rule:** If the one-sentence summary starts with "Using a novel dataset..." or "Exploiting a policy shock...", force a rewrite until it starts with the finance question. The question must come first; the data or design is the tool, not the contribution.

## What counts as a strong idea

A strong idea scores well on six dimensions:

1. **Sharp question** — Can you state the research question in one sentence without hedging? Is there a clear dependent variable and a testable prediction?
2. **First-order importance** — Would the answer change priors in a broad finance literature or on a materially important market, policy, or contracting problem? Would a generalist finance editor care even if the estimated effect is zero?
3. **Verified contribution** — Relative to the 3-5 closest papers, is the novelty real and nontrivial? Novelty must be in mechanism, question, identification, measurement, or implication, not just in setting, time period, or data access. "X but in country Y" or "X but with newer data" is not a contribution unless the setting variation generates a genuinely different economic prediction.
4. **Economic mechanism** — Is there a friction, incentive, or equilibrium force that generates a testable prediction? Can you name the channel and distinguish it from obvious alternatives?
5. **Convincing theory-to-evidence bridge** — Is there a persuasive inferential bridge from idea to evidence? This can be a quasi-experiment, field experiment, theory model, structural estimation, validated measurement exercise, sufficient-statistic approach, or out-of-sample asset-pricing test. Judge whether the bridge matches the question, not whether it looks like a standard causal design.
6. **Data, measurement, and replication feasibility** — Three sub-checks:
   - **Access:** Can the data realistically be obtained in time?
   - **Construct validity:** Does the empirical measure actually map to the mechanism? Would a skeptic accept it as a reasonable proxy?
   - **Replication feasibility:** Could the core result be documented and replicated under current top-journal data/code policies (JF data editor review, JFE replication package requirement, RFS Harvard Dataverse deposit)?

## Scoring rubric

Rate each of the six dimensions 1-5:
- 5: Publication-grade strength — among the best you could imagine for this dimension
- 4: Strong — needs only minor refinement, no fundamental concern
- 3: Promising — needs significant work but a clear path exists
- 2: Weak — major gap that may or may not be fixable
- 1: Fatal — unlikely to be resolved

**Calibration guidance:**
- Default to 2 or 3 unless there is a strong, specific case for higher.
- Use 5 sparingly. A 5 means this dimension would survive the toughest referee in the field.
- Never rate an idea as top-3 Go if the only clear strength is data access or a clever shock.
- A paper that is 3 across the board is a plausible working paper or field-journal candidate, not a top-3 finance journal paper.

**Decision rules:**

### Top-3 Go (JF / JFE / RFS track)
- Importance >= 4
- Contribution >= 4
- Bridge >= 4
- No dimension < 3
- At most 3 essential hurdles to publication

### Strong field-journal Go (JFQA / RoF / MS / RE journals)
- All dimensions >= 3
- Total >= 18
- One or more of importance, contribution, or bridge is 3 rather than 4, but the overall package is solid

### Revise
- The question may matter, but at least one of contribution, bridge, or construct validity is underdeveloped
- Total 15-20 with a clear path to improvement on the weak dimensions

### Kill / Pivot
- Importance < 3 (the question is second-order)
- Contribution is mostly setting variation
- The bridge cannot distinguish the proposed mechanism from obvious alternatives
- More than 3 essential hurdles would be needed for publication
- Total <= 14 or any dimension = 1

## Revision-feasibility rule

After scoring, list the essential hurdles a referee would raise. Apply this filter:

- If more than **three essential hurdles** are needed to make the paper publishable, default to **Kill** or **Pivot** unless the question is unusually important (Importance = 5) and the contribution is unusually novel (Contribution >= 4).
- Ask whether a plausible path to publication exists within **one R&R round, or at most two**. If not, the idea is not ready.

## Imaginary abstract test

Before running the full scoring workflow, write a 5-part imaginary abstract for the idea:

1. **Motivation/Tension:** What is the gap between what economists assume and what the world actually looks like? What prior would change?
2. **Empirical Setting and Data:** What is the ideal experiment or setting? What data would you use?
3. **Results:** What would you expect to find? Be specific about magnitudes if possible.
4. **Implications:** What does this mean for theory, practice, or policy?
5. **Conclusion:** One-sentence takeaway.

**Purpose:** The imaginary abstract forces coherence. If you cannot write a plausible 5-part abstract, the idea is not ready. Ideas that sound exciting as a sentence but collapse when spelled out are Type I errors waiting to happen. The goal is not to draft a flawless abstract, but to test whether the idea has substance.

**If the abstract feels impossible to write**, that is diagnostic: the idea lacks a clear question, a plausible test, or a meaningful result. Kill or revise.

## Four quick stress tests

Apply these after scoring. Each should be answerable in one sentence.

1. **Null-result value test:** State what the paper teaches if the main estimate is zero. If the answer is "nothing," the paper is too dependent on a specific result.
2. **Simultaneous-discovery test:** If a similar working paper appeared on SSRN tomorrow, would this paper still deserve publication because it gives the cleanest, most credible, or most important answer? If not, speed-to-market is the only edge, which is fragile.
3. **Syllabus test:** Name one sentence in a PhD finance lecture that would have to change if the paper is right. If you cannot, the paper may not be first-order.
4. **Necessary-conditions test:** Name the one critical first-stage condition that must hold for the project to work (e.g., the shock must show up in the data, the treatment must change behavior, the instrument must have a first stage). Can you check this condition with a few hours of work before committing months? If the necessary condition fails, kill the project early. Treat research like drug development: lab test before clinical trial.

## Kill criteria

Flag the idea as weak if one or more of these dominate:
- It is a minor setting variation with no new mechanism ("X but in country Y").
- The identification is decorative rather than essential — the result does not require the proposed design.
- The data are unavailable, too small, or too noisy for the claim.
- The contribution depends on saying "first" without verification.
- The likely result would be too local or too descriptive for the intended journal.
- The idea needs multiple heroic assumptions to work.
- The question has been answered convincingly and the proposed paper cannot improve on existing answers.
- The mechanism is a just-so story with no way to distinguish it from alternatives.

## Screening workflow

1. **Stage 0:** Run the desk-editor screen (four questions above). If weak, stop early.
2. Restate the idea in one sentence (question-first framing).
3. **Write the imaginary abstract** (5 parts: motivation/tension, setting/data, expected results, implications, takeaway). If you cannot write a coherent abstract, flag the idea as underdeveloped.
4. Identify the mechanism or friction.
5. Name the closest 3-5 papers (use `search_papers` to verify — do not guess).
6. State what is new relative to the closest papers — be specific about whether the novelty is in mechanism, data, identification, setting, or implication. Score contribution honestly.
7. Sketch the theory-to-evidence bridge (quasi-experiment, model, structural, measurement, or asset-pricing test).
8. Assess data, measurement, and replication feasibility (use `search_datasets` if needed).
9. **Necessary-conditions check:** Name the one critical first-stage condition and whether it can be tested quickly.
10. Identify the likely journal track (finance generalist, finance specialist, or real-estate/housing).
11. List the 2-3 biggest fatal risks (these become the essential hurdles).
12. Apply the six-dimension scoring rubric.
13. Run the four stress tests (null-result, simultaneous-discovery, syllabus, necessary-conditions).
14. Apply the revision-feasibility rule (max 3 hurdles).
15. Deliver the verdict with the expanded Idea Card.

## Idea generation guidance

When asked to generate ideas (not just screen them):
- Start from frictions, not topics. Ask: what market failure, information asymmetry, behavioral bias, regulatory distortion, or institutional feature creates inefficiency?
- Look for natural experiments, policy changes, or data innovations that create new identification opportunities.
- Consider what new data sources have become available (satellite imagery, web scraping, administrative records, fintech platforms, text/NLP from filings, alternative workforce data).
- Think about which classic questions have become answerable with modern methods (ML, high-frequency data, granular geographic data, LLMs for text analysis).
- Always ask: is the question more important than the data? If the data is the star, the paper is likely second-order.

## Tool integration (Corbis MCP)

**Never claim an idea is novel without searching first.** Use this exact sequence:

### Novelty verification chain
1. `search_papers` (query: the core question in natural language, `matchCount: 15`) — find closest existing work. Corbis uses hybrid semantic+keyword search over 265,000+ papers, so phrase the query like a research question, not keywords.
2. `get_paper_details` (paper IDs from top 3-5 results) — read abstracts to confirm whether they truly overlap or just share vocabulary.
3. `top_cited_articles` (field: e.g., "corporate finance", topic: e.g., "debt covenants") — identify seminal papers the user must know about.
4. `search_papers` (same query, `minYear: 2023`) — catch recent working papers not yet indexed in OpenAlex.

### Data feasibility check
- `search_datasets` (topic keywords) — discover available datasets and their coverage.
- `fred_search` (keywords like "commercial real estate" or "bank lending") — find relevant FRED macro series for context or controls.

### For real-estate ideas specifically
- `get_market_data` (metro name) — current CRE fundamentals to assess whether the phenomenon is economically relevant now.
- `search_markets` (criteria) — find markets with the characteristics needed for the natural experiment.
- `export_citations` (format: `bibtex`) — export BibTeX entries for the 3-5 closest papers identified during the novelty verification chain. Offer this after the Idea Card is produced.
- `format_citation` — format individual references from the screening results for inclusion in notes or memos.

## Preferred outputs

When generating or screening ideas, produce one or more Idea Cards using:
- assets/idea-card-template.md

Also provide:
- a one-sentence contribution claim
- a one-sentence skepticism test from a referee's point of view
- a scoring rubric result (six dimensions)
- a go, revise, or kill recommendation with specific reasoning
- the three stress-test answers
- the killer exhibit description

## Journal-fit logic

**Top-3 finance ideas** must change how the field thinks about something. JF, JFE, and RFS want a first-order question with a convincing bridge from theory to evidence. The bridge can be causal identification, a structural model, a measurement innovation, or a theoretical contribution — it does not have to be a quasi-experiment. JFQA and RoF are slightly more receptive to careful empirical work on narrower or cross-disciplinary questions.

**Real-estate-track ideas** can lean more heavily on institutional setting, property-market detail, and spatial or policy structure, but they still need a clean contribution and a strong empirical design. REE and JREFE value institutional knowledge. RSUE and JHE want broader urban/housing economics framing.

When assessing journal fit, consider mapping the candidate idea to 2-3 recent papers in the target journal that share the closest structure (question type, method, contribution style). If no recent archetype exists, the fit may be weak.

## Guardrails

- Never confuse an interesting topic with a publishable question.
- Do not overpraise novelty. If the search reveals close papers, say so.
- If the user gives several ideas, rank them using the scoring rubric.
- Prefer fewer, stronger claims over many diffuse ones.
- Do not let enthusiasm for a topic substitute for identification feasibility.
- Do not let enthusiasm for a dataset or shock substitute for question importance.
- Score importance and contribution honestly. Most ideas are 2-3 on these dimensions, not 4-5.

## Output format

Use the template in `assets/idea-card-template.md`. The template includes all required fields.

## Example prompts
- "Give me three corporate-finance ideas using private-credit data."
- "Is this housing-supply idea strong enough for a top real-estate journal?"
- "Turn this empirical asset-pricing anomaly into a better paper idea."
- "I have access to fintech lending data — what could I do with it?"
