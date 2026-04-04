---
name: literature-landscape
description: "Generate figures that visualize patterns in an academic literature: publication trends, citation landmarks, journal distributions, thematic evolution, method timelines, and coverage gap maps. Uses Corbis search data and Python/matplotlib."
---

# Literature Landscape

Generate publication-ready figures that visualize the structure and evolution of an academic literature. These figures appear in survey papers, dissertation chapters, grant proposals, and paper introductions to motivate research gaps.

## When to use

- The user wants to visualize trends in a field (publication volume, citation patterns, thematic shifts)
- The user has completed a literature search (via `/lit-review` or `/lit-search`) and wants figures
- The user wants to identify research gaps visually (the coverage gap map)
- The user is writing a survey or lit review chapter and needs landscape figures

## Prerequisites

Requires Python with `matplotlib`, `pandas`, and `numpy`. If not installed:

```bash
pip install matplotlib pandas numpy
```

## Available figure types

| Key | Figure | What it shows |
|---|---|---|
| `timeline` | Publication timeline | Papers per year, optionally stacked by journal |
| `citations` | Citation landmark chart | Scatter of year vs. citations, top papers labeled |
| `journals` | Journal distribution | Horizontal bars: which outlets publish most on the topic |
| `themes` | Thematic evolution heatmap | Keyword frequency across year bins, showing focus shifts |
| `methods` | Methods timeline | Stacked bar of identification strategies over time |
| `gapmap` | Coverage gap map | Matrix: settings x methods, empty cells = research gaps |

## Inputs to collect

| Input | Required? | Default |
|---|---|---|
| Topic or research question | Yes (if no existing data) | — |
| Existing paper data (JSON file, bib file, or reading list) | No | Run fresh Corbis searches |
| Which figures to generate | Yes (propose, user selects) | All 6 |
| Gap map row dimension | No | Geographic setting (auto-detected) |
| Gap map column dimension | No | Research method (auto-detected) |

If the user provides a topic but no existing data, run searches to build the dataset. If they point to an existing reading list or bib file from a prior `/lit-review`, use that as the starting point and enrich with `get_paper_details` to fill in missing citation counts and abstracts.

## Workflow

### Phase 1: Build the paper dataset

**Option A — Fresh search (no existing data):**

Run 4-5 `search_papers` queries with `matchCount: 20` each, varying keywords and year ranges to cover the topic broadly. Goal: 80-100 papers with metadata. For each paper, ensure you have: title, authors, year, journal, citedByCount, abstract.

Call `get_paper_details` on any papers missing citation counts or abstracts (batch by importance: prioritize high-citation and recent papers).

Deduplicate by title similarity or OpenAlex ID.

**Option B — Existing data:**

If the user points to a JSON file, reading list markdown, or .bib file from a prior `/lit-review`:
1. Parse the existing data
2. Identify papers missing citedByCount or abstract
3. Call `get_paper_details` to fill gaps
4. Add more papers if the existing set is small (<40): run 2-3 supplementary `search_papers` queries

**Save the dataset:**

Write the paper data to a JSON file at `output/lit_landscape_data.json` (or a topic-specific name). Format:

```json
[
  {
    "title": "Paper Title",
    "authors": ["Author One", "Author Two"],
    "year": 2005,
    "journal": "Journal Name",
    "citedByCount": 1234,
    "abstract": "Full abstract text..."
  }
]
```

This file is the input to `utils/lit_landscape.py`.

### Phase 2: Propose figures

Analyze the dataset and propose which figures would be most informative. Use these heuristics:

| Condition | Recommendation |
|---|---|
| Papers span 10+ years | Timeline is valuable |
| Papers span <10 years | Skip timeline or use 1-year bins |
| Citation range varies widely (max/min > 50) | Citation landmark chart is valuable |
| Papers come from 4+ journals | Journal distribution is valuable |
| Papers come from 1-2 journals | Skip journal distribution |
| Abstracts contain identifiable method keywords | Methods timeline is valuable |
| Abstracts lack method keywords | Skip methods timeline |
| Papers cover multiple settings/countries | Gap map is valuable |
| Topic is narrow/single-country | Propose custom gap map dimensions instead of setting x methods |

**For the gap map**, propose specific row and column dimensions based on the topic. Examples:

- **Political connections**: rows = settings (US, China, Europe, etc.), cols = methods (event study, DiD, RDD, etc.)
- **Housing prices**: rows = mechanisms (supply, demand, credit, regulation), cols = data sources (HMDA, CoreLogic, Zillow, Census)
- **Corporate governance**: rows = governance mechanisms (board, ownership, compensation, activism), cols = outcomes (performance, risk, investment, payout)

Present the proposal and wait for user approval.

**Deliver this proposal:**

```
# Literature Landscape — Figure Proposal

## Dataset: [N] papers, [min_year]-[max_year]

## Recommended figures:

1. ✅ Publication timeline — [reason]
2. ✅ Citation landmark chart — [reason]
3. ✅ Journal distribution — [reason]
4. ⬜ Thematic evolution — [reason to include or skip]
5. ⬜ Methods timeline — [reason to include or skip]
6. ✅ Coverage gap map — [proposed rows] x [proposed cols]

## Gap map dimensions:
- Rows: [list, e.g., "US, China, Europe, Emerging, Cross-country"]
- Columns: [list, e.g., "Event study, DiD, RDD, Panel/FE, Structural"]

Select which figures you want (or say "all"), and I'll generate them.
```

**Checkpoint**: Wait for user approval. Do not generate figures until the user confirms.

### Phase 3: Generate figures

Run the Python utility:

```bash
python utils/lit_landscape.py output/lit_landscape_data.json \
  --figures timeline citations journals themes methods gapmap \
  --outdir output/figures \
  --group-timeline-by journal \
  --bin-size 3 \
  --label-top-n 8
```

If the user specified custom gap map dimensions:

```bash
python utils/lit_landscape.py output/lit_landscape_data.json \
  --figures gapmap \
  --outdir output/figures \
  --gapmap-rows "US,China,Europe,Emerging,Cross-country" \
  --gapmap-cols "Event study,DiD,RDD,Panel/FE"
```

**Verify each figure** after generation:
- Check the output file exists and is non-empty
- Read any error messages from the script
- If a figure was skipped (not enough data), report it to the user

### Phase 4: Present results

For each generated figure, provide a 2-3 sentence interpretation of what it shows. Example:

```
## Figure Results

### Publication timeline (fig_timeline.pdf)
Publication on this topic accelerated sharply after 2005, with output tripling
between 2010-2015 and 2015-2020. The Journal of Finance and JFE account for
the largest shares.

### Coverage gap map (fig_gapmap.pdf)
Three cells show zero papers: RDD studies in emerging markets, structural
models in the US, and DiD designs in cross-country samples. The RDD gap in
emerging markets may reflect data limitations rather than a true research
opportunity.
```

### Phase 5: Log and output

**Lab notebook**: Append an entry to `notes/lab_notebook.md`:

```markdown
---

### [DATE] — Literature Landscape: [Topic]

**What was done**: Generated [N] landscape figures from [M] papers on [topic].

**Figures generated**:
- [fig_timeline.pdf]: [1-sentence finding]
- [fig_citations.pdf]: [1-sentence finding]
- ...

**Gaps identified** (from gap map):
- [Gap 1]
- [Gap 2]

**Output files**:
- Data: output/lit_landscape_data.json
- Figures: output/figures/fig_*.pdf

**Next steps**: [e.g., use gap map to inform /brainstorm, or include figures in paper]
```

## Guardrails

- **Do not fabricate data.** Every paper in the JSON must come from a Corbis search result or an existing reading list. Do not invent papers to fill the dataset.
- **Respect the checkpoint.** Do not generate figures until the user approves the proposal.
- **Interpret, do not overclaim.** A gap in the gap map does not mean no one has studied it. It means the Corbis search did not find papers matching both dimensions. Note this limitation.
- **The gap map dimensions matter.** Bad dimensions produce uninformative figures. Propose dimensions that reflect real intellectual distinctions in the field, not arbitrary categories.
- **Push work to Python.** The AI collects data and writes the JSON. Python does the feature extraction, keyword analysis, method detection, and figure rendering. Do not attempt to generate figures by describing them in text.

## Example prompts

- "Visualize the landscape of the political connections literature" (fresh search)
- "Generate landscape figures from my literature review reading list at notes/reading_list_housing.md"
- "Make a gap map for the climate finance literature with mechanisms on rows and asset classes on columns"
- "/lit-landscape corporate governance and firm performance"
- "I just ran /lit-review on fintech lending. Now make landscape figures from those results."
