---
description: Build a seminar or conference presentation outline
---

Run the `research-seminar-deck` skill:

$ARGUMENTS

If format is not specified, ask: conference (15-20 min), workshop (45 min), seminar (75 min), or job talk (90 min)?

Read `notes/project_state.md` if it exists to pick up the research question, design, key results, and closest papers from prior skill invocations.

Produce:
- **Beamer LaTeX file** written to `paper/slides_[format].tex` using the template at `latex_template/beamer_template.tex` (metropolis theme, navy/gray scheme, 16:9 aspect ratio, frame templates for every slide type)
- Slide-by-slide outline with time targets per slide
- Core message in one sentence
- Suggested visuals (figure type and what each should show)
- Speaker notes for key slides (via `\note{}` in Beamer)
- Backup slides organized by anticipated question type
- Top 10 questions to anticipate with suggested responses

When the user asks for "slides" or "a deck," generate the Beamer file by default. When the user asks for an "outline" or "blueprint," produce the outline only.

Use `search_papers` to identify papers likely to come up in Q&A. For RE presentations, use `get_market_data` for current market context on motivation slides.
