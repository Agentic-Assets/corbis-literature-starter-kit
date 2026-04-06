# Skills Guide

How to use the 6 research workflows in this starter kit. All workflows search [Corbis](https://www.corbis.ai) (250,000+ papers) before making claims and export BibTeX citations automatically.

In Claude Code, these are available as slash commands. In Codex, Cursor, and other MCP clients, use the same workflow names and examples below as prompt templates.

## Which skill to use

| I want to... | Skill / Command |
|---|---|
| Survey what a field knows about a topic | `/lit-review` |
| Find the closest papers to my idea and sharpen the contribution | `/lit-search` |
| Generate research ideas in a topic area | `/brainstorm` |
| Evaluate whether a specific idea is worth pursuing | `/idea` |
| Check that my citations are correct and complete | `/verify-citations` |
| Visualize trends, gaps, and methods in a literature | `/lit-landscape` |

## Common workflows

**Starting from scratch:**
1. `/lit-review [your topic]` -- understand the field
2. `/brainstorm [your topic]` -- generate ideas from gaps you found
3. `/idea [best idea]` -- screen it rigorously

**Positioning an existing idea:**
1. `/lit-search [your paper's question]` -- find closest work
2. `/idea [your idea]` -- score and stress-test it

**Visualizing a literature:**
1. `/lit-review [your topic]` -- build the paper set
2. `/lit-landscape [your topic]` -- generate trend and gap figures

**Polishing citations:**
1. `/verify-citations` -- audit your .bib against Corbis

**Reading a paper:**

If your assistant supports repo-defined agents, use the paper-reader prompt:
> "Read and summarize the paper at ~/Downloads/fama_french_1993.pdf"

## Notes

- Literature reviews produce BibTeX citations automatically via `export_citations`
- Results are saved to `notes/` and `output/` with lab notebook entries
- If your client reads `CLAUDE.md` and `.claude/` directly, it can route requests automatically. Otherwise, use the table above as the manual workflow guide.
