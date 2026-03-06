---
name: research-seminar-deck
description: "Design finance and real-estate research presentations. Use for seminar decks, conference talks, job talks, slide logic, speaker notes, and backup-slide planning."
---

# Research Seminar Deck

Build a talk that foregrounds the question, design, and economic meaning before details overwhelm the audience.

## Workflow

1. Identify the audience and format:
   - Brown bag / workshop (30-45 min, informal, expect interruptions)
   - Conference presentation (15-20 min, formal, limited Q&A)
   - Invited seminar (60-75 min, deep engagement, extensive Q&A)
   - Job talk (75-90 min, high stakes, hostile-constructive Q&A)
   - Dissertation defense (varies by institution)
2. Write the one-sentence contribution.
3. Decide what the audience must believe before seeing results.
4. Build the main-deck sequence.
5. Move technical depth and robustness density to the appendix.
6. Add likely-question backup slides.

## Time budgets by format

| Format | Total slides | Main deck | Backup | Time per slide |
|---|---|---|---|---|
| Conference (15 min) | 12-15 | 10-12 | 5-8 | ~1 min |
| Conference (20 min) | 15-20 | 13-16 | 8-10 | ~1.2 min |
| Workshop (45 min) | 25-30 | 20-25 | 10-15 | ~1.5-2 min |
| Seminar (75 min) | 35-45 | 28-35 | 15-20 | ~2 min |
| Job talk (90 min) | 40-50 | 30-40 | 20-30 | ~2 min |

## Main-deck logic

Default sequence:
1. **Title and contribution** — one sentence that tells the audience exactly what they will learn
2. **Motivation** — why should the audience care? Real-world context, not literature gap
3. **Research question** — precise, testable
4. **Institutional setting or mechanism** — the economics that generates the prediction
5. **Preview of results** — optional for seminars, essential for conferences
6. **Identification challenge** — what makes this hard to answer?
7. **Research design** — the solution to the identification challenge
8. **Data and sample** — one or two slides maximum
9. **Main result** — the key table or figure, simplified for projection
10. **Economic magnitude** — translate into real units the audience can feel
11. **Mechanism evidence** — why the effect operates through the proposed channel
12. **Key robustness** — two or three checks, not a laundry list
13. **Conclusion** — restate the contribution, the economic lesson, and one forward-looking implication

## Slide-writing rules

- **One message per slide.** If you need two messages, make two slides.
- **Sparse text.** Maximum 4-5 bullet points, each under 10 words.
- **Figures beat tables.** Convert regression results into coefficient plots or event-study graphs.
- **Simplified tables.** Show only the coefficient of interest, key controls listed (not shown), and the specification description.
- **Show magnitudes in real units.** "2.3 percentage points" beats "beta = 0.023 (t = 4.2)."
- **Explain the design before showing estimates.**
- **Use consistent formatting.** Same font sizes, color scheme, and layout throughout.

## Audience-specific adjustments

**Finance seminar**: Will attack identification immediately. Front-load design credibility. Backup slides for alternative specifications, clustering, pretrends.

**Real estate audience**: Values institutional detail. Spend more time on setting, data, and maps. Backup slides with data construction details.

**Job talk**: Testing breadth and depth. Compelling "big picture" motivation, clean design, ability to handle adversarial questions. Prepare 20+ backup slides.

**Conference**: Time is scarce. Motivation, design, result, magnitude, done. Backup slides handle depth.

## Visual design principles

- **Coefficient plots** over regression tables for the main deck
- **Event-study plots** with confidence intervals, clearly labeled pre/post periods
- **Maps** when geography matters
- **Timeline diagrams** for event timing or staggered designs
- **Flow charts** for complex identification strategies
- **Bar charts** for magnitude comparisons across subgroups

## Backup slide planning

Organize by anticipated question type:
1. **Identification**: Alternative specifications, different FE, pretrends, placebo tests
2. **Measurement**: Alternative variable definitions, different data sources
3. **Sample**: Subsamples, outlier sensitivity, different time periods
4. **Mechanism**: Additional channel tests, competing explanations
5. **Data construction**: Merge details, match rates, sample flow
6. **Literature**: How does this compare to [specific paper]?

## Speaker notes guidance

For each slide, prepare:
- The key message in one sentence
- The transition from the previous slide
- One or two anticipated questions and how to handle them
- The time target for this slide

## Deliverables

Produce:
- a slide-by-slide outline using assets/seminar-deck-outline.md
- suggested visuals (specify figure type and what it should show)
- presenter notes for each slide
- appendix backup-slide plan organized by question type
- anticipated Q&A with suggested responses

If the environment supports presentation-file creation (LaTeX Beamer, PowerPoint), build the actual deck. Otherwise produce a blueprint.

## Output format

```
# Seminar deck blueprint
## Audience and format
## Core message (one sentence)
## Slide-by-slide outline (with time targets)
## Figures and tables to create or simplify
## Backup slides (organized by question type)
## Top 10 questions to anticipate (with responses)
## Speaker notes for key slides
```

## Tool integration (Corbis MCP)

- `search_papers` (query: the paper's topic, `matchCount: 5`, `minYear: 2020`) → find recent related work to anticipate "how does this compare to [paper]?" questions and prepare backup slides.
- `top_cited_articles` (journals: target journals) → identify seminal papers the audience is likely to reference, to prepare backup slides and anticipate comparison questions.
- `get_paper_details` (paper IDs) → read abstracts of papers likely to come up in Q&A.
- `get_market_data` / `compare_markets` → for RE presentations, pull current market data for motivation slides or audience-relevant context.
- `fred_series_batch` (relevant series) → pull aggregate trends for motivation slides (e.g., housing starts, mortgage rates, credit spreads).
- `export_citations` (format: `bibtex`) → export BibTeX entries for papers cited in the presentation, including literature-positioning slides and backup slides. Offer this after the deck blueprint is produced.
- `format_citation` → format individual references for slide footnotes or the bibliography slide.

## Reference files
Read if needed:
- references/presentation-norms.md
- references/writing-norms.md

## Guardrails

- Do not transplant the manuscript structure directly onto slides.
- Do not let the deck become a literature review.
- Do not use unreadable tables in the main talk.
- Anticipate the identification question before the audience asks it.
- Do not end with "thank you" as the last slide — end with the contribution and implication.
- For job talks, do not rush the motivation.
- Do not put full regression tables on slides — simplify or use coefficient plots.

## Example prompts
- "Turn my asset-pricing paper into a 15-minute conference deck."
- "Build a job-talk outline for this corporate-finance paper."
- "Create a seminar deck plan for a zoning and housing-supply paper."
- "What backup slides do I need for a hostile identification question?"
- "Convert these regression tables into presentation-ready visuals."
