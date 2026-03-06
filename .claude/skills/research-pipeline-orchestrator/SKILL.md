---
name: research-pipeline-orchestrator
description: "Plan academic finance or real-estate projects from idea to submission and presentation. Use for end-to-end roadmaps, stage plans, and journal-targeted research workflows."
---

# Research Pipeline Orchestrator

Use this skill as the front door for the full suite. Locate the user's current stage, identify the target domain, and produce a concrete next-step roadmap that matches top finance or real-estate journal standards.

## Stage classification

First classify the project along four dimensions:
- Domain: corporate finance, investments, empirical asset pricing, household finance, real estate, or urban economics
- Stage: idea, literature positioning, design, data, analysis, writing, revision, or presentation
- Output needed now: memo, code plan, table plan, manuscript text, response letter, or deck
- Journal track: finance (JF/JFE/RFS/JFQA/MS), real estate (REE/JREFE/JUE/JHE), or undecided

If the user is vague, infer the most likely stage from the request instead of stalling.

## Default stage sequence

1. Idea screening
2. Literature positioning
3. Identification and design
4. Data construction
5. Baseline analysis
6. Specialty analysis if needed
   - asset pricing tests for signal or factor papers
   - real-estate design checks for property, mortgage, urban, or spatial papers
7. Paper drafting
8. Revision and referee-response preparation
9. Seminar or conference deck

## Tool integration (Corbis MCP)

At every stage, actively use Corbis tools to provide concrete, evidence-based guidance. Do not speculate when you can search. Do not guess about data or literature when you can check.

### Stage-specific tool chains

**Idea stage:**
- `search_papers` (query: the core question, `matchCount: 10`) → verify novelty
- `top_cited_articles` (field + topic) → map the intellectual neighborhood
- `search_datasets` (topic keywords) → assess data feasibility early

**Literature positioning stage:**
- `search_papers` (multiple queries covering the topic) → comprehensive sweep across 265,000+ papers
- `get_paper_details` (paper IDs from search results) → read abstracts of close competitors
- `export_citations` (paper IDs, format: `bibtex`) → generate bibliography entries for LaTeX

**Design and data stage:**
- `search_papers` (method-specific query, e.g., "staggered difference-in-differences housing") → find design precedents
- `fred_search` (keywords like "house price index" or "mortgage rate") → identify relevant macro series
- `fred_series_batch` (series IDs, e.g., `["CSUSHPISA","MORTGAGE30US","UNRATE"]`) → pull macro context data
- `search_datasets` (data source keywords) → discover available datasets

**Real-estate projects — additional tools:**
- `get_market_data` (metro name) → current CRE market conditions (cap rates, vacancy, rent growth)
- `compare_markets` (metro list) → cross-market comparison for motivation or external validity
- `search_markets` (criteria like "highest cap rate office") → find markets matching research criteria

**Analysis and writing stage:**
- `search_papers` (query: specific empirical pattern, `minYear: 2020`) → find comparable magnitudes in recent literature
- `format_citation` (paper ID, style: `apa` or `chicago`) → generate formatted citations
- `export_citations` (paper IDs, format: `bibtex`) → batch export references


## What to produce

Always give the user:
- a current-stage diagnosis with specific evidence for why you placed them there
- the highest-value immediate deliverable
- a short list of follow-on deliverables with dependencies mapped
- a kill-risk list that could sink the paper if ignored, ranked by severity
- a journal-track recommendation with reasoning tied to the paper's strengths and weaknesses
- explicit guidance on which specialized skill should handle the next deep dive

## Output format

```
# Project roadmap
## Current stage
## Immediate objective
## Deliverable to create now
## 2-week plan (with concrete milestones)
## 6-week plan (with decision gates)
## Key risks (ranked by severity)
## Journal-track recommendation
## Which specialized skill should do the next deep dive
```

## Routing logic

**Finance track** (JF, JFE, RFS, JFQA, Management Science): Sharp question, credible identification, disciplined theory-mechanism connection, concise exposition. The contribution must generalize beyond the specific setting.

**Real-estate track** (REE, JREFE, JUE, JHE): Can lean more heavily on institutional setting, property-market detail, spatial or policy structure, but still needs a clean contribution and strong empirical design. JUE and JHE reward broader urban/housing economics framing.

**Cross-track papers**: Some papers (e.g., mortgage finance, housing and household portfolios, REIT pricing) could target either track. In these cases, lay out both paths with the trade-offs of each.

Read `references/journal-targets.md` for per-journal profiles including fit inference, red flags, and development advice.

## Decision gates

Build explicit go/no-go checkpoints into every roadmap:
- After idea screening: Is the question sharp enough and the mechanism clear?
- After literature positioning: Is there genuinely something new to say?
- After design: Can the identification actually support the claim?
- After data construction: Is the sample large and clean enough for the design?
- After baseline analysis: Do the results tell a coherent economic story?
- Before submission: Does every claim match what the design can support?

## Guardrails

- Do not let the roadmap become generic productivity advice.
- Tie every stage recommendation to the actual paper idea, data, and target journal logic.
- If the user asks for the whole pipeline, prioritize the next decision that most improves publishability.
- If the paper is not yet viable, say so clearly and explain why.
- When suggesting timelines, be realistic about the pace of academic research.
- Flag when a project needs coauthor expertise the user may not have (e.g., structural estimation, spatial econometrics, machine learning).

## LaTeX template

When a project reaches the writing stage, copy `latex_template/` from the project root to start the manuscript. The template includes a full paper structure (blind-review toggle, `jf.bst` style, example tables/figures) that aligns with the `research-paper-writer` skill's section sequence.

Read these references as needed:
- references/journal-targets.md
- references/empirical-standards.md

## Example prompts
- "Take this housing-finance idea from brainstorming to R&R."
- "I have a corporate-finance draft. What should happen next before submission?"
- "Map a workflow for an empirical asset-pricing project."
- "I'm stuck between targeting REE and JFE — help me decide."
