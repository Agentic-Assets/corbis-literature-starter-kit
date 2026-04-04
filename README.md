# Corbis Literature Starter Kit

A lightweight [Claude Code](https://docs.anthropic.com/en/docs/claude-code) project for exploring academic literature, brainstorming research ideas, and managing citations. Clone it, connect [Corbis](https://corbis.ai), and start exploring.

Search 265,000+ academic papers, export BibTeX citations, and discover datasets, all from your terminal.

## What you get

**5 slash commands:**

| Command | What it does |
|---|---|
| `/lit-review` | Write a structured literature review on any topic |
| `/lit-search` | Map the closest papers and sharpen your contribution |
| `/brainstorm` | Generate 10 ranked research ideas from a topic area |
| `/idea` | Screen and score a specific research idea |
| `/verify-citations` | Audit your .bib file against the literature |

Plus a **paper-reader agent** that can summarize any academic PDF.

## Setup (2 minutes)

**1. Install Claude Code**

Follow the [Claude Code docs](https://docs.anthropic.com/en/docs/claude-code).

**2. Connect Corbis MCP**

See [`CORBIS_MCP_CLAUDE_CODE_GUIDE.md`](CORBIS_MCP_CLAUDE_CODE_GUIDE.md) for the step-by-step guide. It takes about 2 minutes: generate an API key at [corbis.ai](https://app.corbis.ai), then run one command.

**3. Clone and start**

```bash
git clone <repo-url> my-literature-project
cd my-literature-project
claude
```

That's it. No API keys in `.env`, no Python dependencies, no LaTeX required (unless you want to write a paper).

## Example workflows

**Survey a new field:**
```
/lit-review climate risk and commercial real estate pricing
```

**Brainstorm ideas in a topic area:**
```
/brainstorm behavioral biases in household mortgage decisions
```

**Screen a specific idea:**
```
/idea Do bank branch closures reduce small business lending through relationship destruction?
```

**Position your paper against the literature:**
```
/lit-search how does remote work affect commercial property values?
```

**Check your citations:**
```
/verify-citations
```

## Optional: LaTeX paper

A clean LaTeX template is in `latex_template/`. Copy it when you are ready to write:

```bash
cp -r latex_template/ paper/
```

Requires a LaTeX distribution (MacTeX, TeX Live, or MikTeX).

## Project structure

```
notes/           # Reading lists, idea menus, lab notebook
output/          # Literature reviews, positioning memos
paper/           # Your LaTeX manuscript (when ready)
latex_template/  # Clean article template with natbib citations
references/      # Writing norms and citation formatting
```

## Documentation

| File | Purpose |
|---|---|
| `CLAUDE.md` | Project instructions loaded every session |
| `SKILLS_USE_GUIDE.md` | When to use each skill with example workflows |
| `CORBIS_API_REFERENCE.md` | All 19 Corbis MCP tools with parameters and examples |
| `CORBIS_MCP_CLAUDE_CODE_GUIDE.md` | Step-by-step Corbis setup for Claude Code |

## License

MIT
