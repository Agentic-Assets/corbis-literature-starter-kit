# Corbis Literature Starter Kit

A lightweight toolkit for exploring academic literature, brainstorming research ideas, and managing citations. Powered by [Corbis](https://corbis.ai) MCP for literature search across 400,000+ academic papers.

## Skill routing

Before responding to any research-related prompt, check whether a skill applies.

| User is asking about...                          | Use skill                    |
| ------------------------------------------------ | ---------------------------- |
| Survey a topic, write a literature review         | `literature-review`          |
| Position a paper, find closest work, contribution | `literature-positioning-map` |
| Brainstorm research ideas from a topic area       | `research-idea-generator`    |
| Screen or score a specific research idea          | `finance-idea-screening`     |
| Verify citations in a .bib file                   | `verify-citations`           |
| Visualize literature trends, gaps, methods          | `literature-landscape`       |

## Corbis tool usage

**Always search before asserting.** Do not guess about novelty, literature, or data availability when you can check.

Available tools:
- `search_papers`, `get_paper_details`, `get_paper_details_batch`, `top_cited_articles` -- literature search
- `export_citations`, `format_citation` -- citation management
- `search_datasets` -- data discovery (for idea screening)
- `fred_search`, `fred_series_batch` -- macro data context
- `get_market_data`, `compare_markets`, `search_markets`, `get_market_trends` -- CRE market intelligence

Key principles:
- Use `search_papers` before claiming any idea is novel
- Use `compact: true` on `search_papers` when you only need titles and metadata (saves ~80% payload)
- Use `sortBy: "citedByCount"` to find the most influential papers on a topic
- Use `get_paper_details_batch` (up to 25 IDs) instead of repeated `get_paper_details` calls
- Use `top_cited_articles` with the `query` parameter to find highly cited papers on a specific topic within journals
- Use `export_citations` (format: `bibtex`) to generate bibliography entries

See `CORBIS_MCP_TOOL_REFERENCE.md` for full tool documentation.
See `CORBIS_MCP_GUIDE.md` for MCP server architecture and authentication.
See `CORBIS_MCP_CODEX_GUIDE.md` for Codex setup.
See `CORBIS_MCP_CLAUDE_CODE_GUIDE.md` for Claude Code setup.
See `CORBIS_CURSOR_PLUGIN.md` for Cursor plugin setup.

## Writing quality

When producing literature reviews or research prose:
- Read `references/writing-norms.md` and `references/banned-words.md`
- Synthesize by theme, do not enumerate paper by paper
- No filler intensifiers ("crucially," "importantly," "interestingly")
- No em dashes. Use commas, parentheses, colons, or separate sentences
- No promotional language ("novel," "groundbreaking")
- Cite to support claims, not to name-drop

## Project structure

```
notes/           # Lab notebook, reading lists, idea menus
output/          # Literature reviews, positioning memos, idea cards
paper/           # LaTeX manuscript (copy latex_template/ to start)
latex_template/  # Clean article template with natbib citations
references/      # Writing norms, citation formatting
```

## Shared data files

Skills produce composable outputs that later skills can reuse. This avoids redundant searches.

### `output/paper_set.json`

Canonical paper dataset. Every skill that searches for papers writes results here. Every skill that needs papers reads this first before running new searches.

Format: JSON array of paper objects:
```json
[
  {
    "id": "W2002030205",
    "title": "...",
    "authors": ["..."],
    "year": 2001,
    "journal": "...",
    "citedByCount": 2962,
    "abstract": "...",
    "fullText": "...",
    "doi": "...",
    "source_queries": ["query1", "query2"],
    "tier": "foundational"
  }
]
```

Rules:
- If `output/paper_set.json` exists when a skill starts, read it and merge new results (deduplicate by `id`). Do not overwrite.
- The `fullText` field is included when available from `get_paper_details`. Use it for deeper analysis (method detection, contribution assessment) when present.
- The `source_queries` field tracks which search queries surfaced this paper (for hub detection).
- The `tier` field is assigned after collection using relative tiering (see below).

### `output/search_log.md`

Search transparency log. Every skill appends its searches here so the user can see exactly what was queried.

Format per entry:
```markdown
### [DATE] — [Skill name]
| # | Query | Params | Results | Kept |
|---|-------|--------|---------|------|
| 1 | "political connections firm value" | sortBy: citedByCount, matchCount: 15 | 15 | 12 |
| 2 | "political connections finance" | minYear: 2020, matchCount: 15 | 15 | 8 |
Dedup: removed 5 duplicates. Final set: 35 papers.
```

### Relative citation tiering

Citation thresholds vary by field. Instead of fixed cutoffs (500/100), use relative ranking within the collected paper set:

| Tier | Label | Rule | Treatment |
|---|---|---|---|
| 1 | **Foundational** | Top 10% by `citedByCount` within the collected set | Named and discussed individually (3-5 sentences) |
| 2 | **Established** | Next 30% by `citedByCount` | Synthesized claims, 1-2 sentences or grouped parenthetically |
| 3 | **Emerging** | Bottom 60%, especially recent papers | Grouped into frontier paragraphs, cited parenthetically |

A paper that appears in 3+ different search queries (`source_queries` length >= 3) is promoted one tier regardless of citation rank.

## Lab notebook

Every skill that produces a deliverable appends a dated entry to `notes/lab_notebook.md`. If the file does not exist, create it with a header: `# Lab Notebook`.

## Paper-reader agent

The paper-reader agent (`.claude/agents/paper-reader.md`) can read and summarize academic PDFs. After a literature search identifies the top 3-5 most central papers, recommend that the user run the paper-reader on those papers for deeper understanding before writing synthesis claims.

## Defaults

- **Output format**: Save literature reviews and memos to `output/` as Markdown. Save BibTeX to `.bib` files. When the user is ready for LaTeX, write directly into `.tex` files using the Edit tool.
- **Citations**: Use `\citet{}` and `\citep{}` (natbib). Bibliography style: `plainnat`.
