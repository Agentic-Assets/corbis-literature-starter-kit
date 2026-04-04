# Corbis Literature Starter Kit

A lightweight toolkit for exploring academic literature, brainstorming research ideas, and managing citations. Powered by [Corbis](https://corbis.ai) MCP for literature search across 265,000+ academic papers.

## Skill routing

Before responding to any research-related prompt, check whether a skill applies.

| User is asking about...                          | Use skill                    |
| ------------------------------------------------ | ---------------------------- |
| Survey a topic, write a literature review         | `literature-review`          |
| Position a paper, find closest work, contribution | `literature-positioning-map` |
| Brainstorm research ideas from a topic area       | `research-idea-generator`    |
| Screen or score a specific research idea          | `finance-idea-screening`     |
| Verify citations in a .bib file                   | `verify-citations`           |

## Corbis tool usage

**Always search before asserting.** Do not guess about novelty, literature, or data availability when you can check.

Available tools:
- `search_papers`, `get_paper_details`, `top_cited_articles` -- literature search
- `export_citations`, `format_citation` -- citation management
- `search_datasets` -- data discovery (for idea screening)
- `fred_search`, `fred_series_batch` -- macro data context

Key principles:
- Use `search_papers` before claiming any idea is novel
- Use `get_paper_details` to verify what a paper actually does before characterizing it
- Use `export_citations` (format: `bibtex`) to generate bibliography entries

See `CORBIS_API_REFERENCE.md` for full tool documentation.

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

## Lab notebook

Every skill that produces a deliverable appends a dated entry to `notes/lab_notebook.md`. If the file does not exist, create it with a header: `# Lab Notebook`.

## Paper-reader agent

The paper-reader agent (`.claude/agents/paper-reader.md`) can read and summarize academic PDFs. Useful for understanding papers found during literature searches.

## Defaults

- **Output format**: Save literature reviews and memos to `output/` as Markdown. Save BibTeX to `.bib` files. When the user is ready for LaTeX, write directly into `.tex` files using the Edit tool.
- **Citations**: Use `\citet{}` and `\citep{}` (natbib). Bibliography style: `plainnat`.
