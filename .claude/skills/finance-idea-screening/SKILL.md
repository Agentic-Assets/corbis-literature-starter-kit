---
name: finance-idea-screening
description: "Screen and refine research ideas in corporate finance, investments, asset pricing, and real estate. Use for brainstorming, novelty checks, contribution framing, and journal-fit triage."
---

# Finance Idea Screening

Turn rough topics into credible paper ideas or kill weak ideas early.

## What counts as a strong idea

A strong idea scores well on all five dimensions:
1. **Sharp question** — Can you state the research question in one sentence without hedging?
2. **Economic mechanism** — Is there a friction, incentive, or equilibrium force that generates a testable prediction?
3. **Credible design** — Can you sketch an identification strategy that a skeptical referee would take seriously?
4. **Feasible data** — Do the data exist, and are they accessible within a reasonable timeframe?
5. **Audience** — Would a top-journal referee care about the answer? Does it change how we think about something?

## Scoring rubric

Rate each dimension 1-5:
- 5: Publication-grade strength
- 4: Strong but needs minor refinement
- 3: Promising but needs significant work
- 2: Weak — major gap that may be fixable
- 1: Fatal — unlikely to be resolved

**Decision rules:**
- All dimensions >= 3, total >= 18: **Go** — proceed to design
- Any dimension = 1: **Kill** unless you can articulate a specific fix
- Total 13-17 with no 1s: **Revise** — specify exactly what must improve
- Total <= 12: **Kill** or **Pivot** to a stronger version

## Screening workflow

1. Restate the idea in one sentence.
2. Identify the mechanism or friction.
3. Name the closest 3-5 papers (use `search_papers` to verify — do not guess).
4. State what is new relative to the closest papers — be specific about whether the novelty is in mechanism, data, identification, setting, or implication.
5. Sketch the empirical design or theory-to-data bridge.
6. Assess data feasibility (use `search_datasets` if the user's data source is unclear).
7. Identify the likely journal track. Read `references/journal-targets.md` for detailed journal profiles including fit inference, red flags, and development advice.
8. List the two or three biggest fatal risks.
9. Apply the scoring rubric.

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

## Idea generation guidance

When asked to generate ideas (not just screen them):
- Start from frictions, not topics. Ask: what market failure, information asymmetry, behavioral bias, regulatory distortion, or institutional feature creates inefficiency?
- Look for natural experiments, policy changes, or data innovations that create new identification opportunities.
- Consider what new data sources have become available (satellite imagery, web scraping, administrative records, fintech platforms, text/NLP from filings).
- Think about which classic questions have become answerable with modern methods (ML, high-frequency data, granular geographic data).

## Tool integration (Corbis MCP)

**Never claim an idea is novel without searching first.** Use this exact sequence:

### Novelty verification chain
1. `search_papers` (query: the core question in natural language, `matchCount: 15`) → find closest existing work. Corbis uses hybrid semantic+keyword search over 265,000+ papers, so phrase the query like a research question, not keywords.
2. `get_paper_details` (paper IDs from top 3-5 results) → read abstracts to confirm whether they truly overlap or just share vocabulary.
3. `top_cited_articles` (field: e.g., "corporate finance", topic: e.g., "debt covenants") → identify seminal papers the user must know about.
4. `search_papers` (same query, `minYear: 2023`) → catch recent working papers not yet indexed in OpenAlex.

### Data feasibility check
- `search_datasets` (topic keywords) → discover available datasets and their coverage.
- `fred_search` (keywords like "commercial real estate" or "bank lending") → find relevant FRED macro series for context or controls.

### For real-estate ideas specifically
- `get_market_data` (metro name) → current CRE fundamentals to assess whether the phenomenon is economically relevant now.
- `search_markets` (criteria) → find markets with the characteristics needed for the natural experiment.
- `export_citations` (format: `bibtex`) → export BibTeX entries for the 3-5 closest papers identified during the novelty verification chain. Offer this after the Idea Card is produced.
- `format_citation` → format individual references from the screening results for inclusion in notes or memos.

## Preferred outputs

When generating or screening ideas, produce one or more Idea Cards using:
- assets/idea-card-template.md

Also provide:
- a one-sentence contribution claim
- a one-sentence skepticism test from a referee's point of view
- a scoring rubric result
- a go, revise, or kill recommendation with specific reasoning

## Journal-fit logic

**Finance-track ideas** should look capable of a concise, high-powered contribution with credible identification and broad finance relevance. JF/JFE/RFS want a result that changes how the field thinks about something. JFQA and RoF are slightly more receptive to careful empirical work on narrower or cross-disciplinary questions.

**Real-estate-track ideas** can lean more heavily on institutional setting, property-market detail, and spatial or policy structure, but they still need a clean contribution and a strong empirical design. REE and JREFE value institutional knowledge. RSUE and JHE want broader urban/housing economics framing.

Read if needed:
- references/journal-targets.md
- references/empirical-standards.md

## Guardrails

- Never confuse an interesting topic with a publishable question.
- Do not overpraise novelty. If the search reveals close papers, say so.
- If the user gives several ideas, rank them using the scoring rubric.
- Prefer fewer, stronger claims over many diffuse ones.
- Do not let enthusiasm for a topic substitute for identification feasibility.

## Output format

```
# Idea assessment
## Research question (one sentence)
## Mechanism / friction
## Why this could matter
## Closest literature (verified via search)
## What is new (specific dimension of novelty)
## Feasible design (sketch)
## Data needs and feasibility
## Fatal risks
## Scoring rubric (5 dimensions, 1-5 each)
## Best journal track
## Verdict: Go / Revise / Kill
## If Revise: what specifically must improve
```

## Example prompts
- "Give me three corporate-finance ideas using private-credit data."
- "Is this housing-supply idea strong enough for a top real-estate journal?"
- "Turn this empirical asset-pricing anomaly into a better paper idea."
- "I have access to fintech lending data — what could I do with it?"
