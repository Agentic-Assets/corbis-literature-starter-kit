---
name: lit-landscape
description: Generate figures visualizing literature trends, citation patterns, and research gaps
---

Run the `literature-landscape` skill for the following topic or data:

$ARGUMENTS

Steps:
1. Build a paper dataset: use existing data if provided, or run 4-5 Corbis searches to collect ~80-100 papers with metadata (title, authors, year, journal, citedByCount, abstract).
2. Save the dataset to `output/lit_landscape_data.json`.
3. Analyze the data and propose which figures to generate (timeline, citations, journals, themes, methods, gapmap). Propose gap map dimensions. Wait for user approval.
4. Run `python utils/lit_landscape.py` to generate the approved figures.
5. Present each figure with a 2-3 sentence interpretation.
6. Log to lab notebook.
