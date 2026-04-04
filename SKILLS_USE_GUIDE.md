# Skills Guide

How to use the 5 literature and idea skills. All skills search [Corbis](https://corbis.ai) (250,000+ papers) before making claims and export BibTeX citations automatically.

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

Ask Claude to use the paper-reader agent:
> "Read and summarize the paper at ~/Downloads/fama_french_1993.pdf"

## Notes

- Literature reviews produce BibTeX citations automatically via `export_citations`
- Results are saved to `notes/` and `output/` with lab notebook entries
- You do not need to invoke skills manually. Claude routes your request automatically based on `CLAUDE.md`. The slash commands are shortcuts.
