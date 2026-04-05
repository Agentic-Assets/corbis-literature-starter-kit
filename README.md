<div align="center">

# Corbis Literature Starter Kit

**Search 250,000+ academic papers. Brainstorm ideas. Write literature reviews. All from your terminal.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Corbis](https://img.shields.io/badge/Powered%20by-Corbis-purple)](https://corbis.ai)
[![Claude Code](https://img.shields.io/badge/Works%20with-Claude%20Code-orange)](https://docs.anthropic.com/en/docs/claude-code)
[![Cursor](https://img.shields.io/badge/Works%20with-Cursor-green)](https://cursor.sh)

[Get Started](#quick-setup) | [Examples](#see-it-in-action) | [Get a Corbis Key](https://app.corbis.ai)

</div>

---

## What is this?

A starter kit that turns your AI coding assistant into a research co-pilot. Clone this repo, connect [Corbis](https://corbis.ai), and you get 6 research workflows that search the academic literature, brainstorm ideas, write reviews, and generate figures.

Works with **Claude Code**, **Cursor**, and any **MCP-compatible agent**.

## 6 Research Workflows

```
/lit-review      Write a structured literature review on any topic
/lit-search      Map the closest papers and sharpen your contribution
/brainstorm      Generate ranked research ideas (with internal rejection filtering)
/idea            Screen and score a specific research idea
/verify-citations   Audit your .bib file against the literature
/lit-landscape   Visualize literature trends, gaps, and methods
```

Plus a **paper-reader agent** that summarizes any academic PDF you throw at it.

## Quick Setup

> **You need two things:** an AI coding assistant and a Corbis API key.

### 1. Get a Corbis API key (free)

Go to **[corbis.ai](https://app.corbis.ai)** > Settings > API Keys > Create a key.

It starts with `corbis_mcp_` and you'll use it in step 2.

### 2. Connect and start

<details>
<summary><b>Claude Code</b></summary>

```bash
claude mcp add corbis --transport http https://app.corbis.ai/api/mcp/universal?apikey=YOUR_KEY
git clone https://github.com/csirmans/corbis-literature-starter-kit.git my-project
cd my-project && claude
```
</details>

<details>
<summary><b>Cursor</b></summary>

```bash
git clone https://github.com/csirmans/corbis-literature-starter-kit.git my-project
```
Then in Cursor: **Settings > MCP Servers > Add**
- Name: `corbis`
- URL: `https://app.corbis.ai/api/mcp/universal?apikey=YOUR_KEY`

Open the project. Cursor reads `CLAUDE.md` automatically.
</details>

<details>
<summary><b>Codex / Other MCP Agents</b></summary>

Connect to the Corbis MCP endpoint:
```
https://app.corbis.ai/api/mcp/universal?apikey=YOUR_KEY
```
Clone this repo. The `CLAUDE.md` file provides instructions most agents read automatically.
</details>

That's it. No Python required. No LaTeX required. Just clone, connect, go.

---

## See It In Action

**Survey a new field in minutes:**
```
/lit-review climate risk and commercial real estate pricing
```
> Searches Corbis, collects ~50 papers, proposes thematic strands, writes a synthesized review with BibTeX citations. Not a list of papers. A real narrative.

**Brainstorm research ideas:**
```
/brainstorm behavioral biases in household mortgage decisions
```
> Generates 25-30 candidates internally, runs a novelty test and kill test on each, shows you only the 10 survivors ranked by novelty, importance, and executability. Includes 3 rejected ideas so you can see what failed and why.

**Screen a specific idea:**
```
/idea Do bank branch closures reduce small business lending through relationship destruction?
```
> Searches for the closest existing papers, scores on 6 dimensions, runs stress tests, and delivers a verdict: Go, Revise, or Kill.

**Visualize the structure of a literature:**
```
/lit-landscape corporate governance and firm performance
```
> Generates publication timelines, citation landmark charts, journal distributions, thematic evolution heatmaps, method timelines, and coverage gap maps. All rendered as publication-ready PDFs.

**Get oriented fast:**
```
/lit-review housing supply elasticity --scope quick
```
> Returns 10 must-read papers, 3 main debates, 3 dominant methods, 3 common datasets, and 5 frontier questions. A 5-minute field orientation.

---

## How Skills Work Together

Skills share data through `output/paper_set.json`. Run one, and the next picks up where it left off:

```
/lit-review [topic]       -->  Builds the paper set (50 papers with metadata)
/lit-landscape [topic]    -->  Reads paper_set.json, generates figures
/brainstorm [topic]       -->  Reads paper_set.json, checks novelty against it
/idea [specific idea]     -->  Reads paper_set.json, finds closest papers
```

Every search is logged to `output/search_log.md` for full transparency.

---

## Optional Extras

| Dependency | What for | Install |
|---|---|---|
| Python 3.10+ | `/lit-landscape` figures | `pip install -r requirements.txt` |
| LaTeX | Writing papers | Copy `latex_template/` to `paper/` |

Neither is required to use the literature search and brainstorming workflows.

## Project Structure

```
.claude/skills/     6 research workflow definitions
.claude/commands/   6 slash commands (shortcuts)
.claude/agents/     Paper-reader agent
notes/              Lab notebook (auto-populated)
output/             Reviews, memos, figures, paper_set.json
latex_template/     Clean article template (natbib + plainnat)
utils/              Python figure generator
references/         Writing norms, citation formatting
```

## Documentation

| File | What it covers |
|---|---|
| [`SKILLS_USE_GUIDE.md`](SKILLS_USE_GUIDE.md) | When to use each workflow, with examples |
| [`CORBIS_MCP_TOOL_REFERENCE.md`](CORBIS_MCP_TOOL_REFERENCE.md) | All 21 Corbis tools: params, outputs, tips |
| [`CORBIS_MCP_CLAUDE_CODE_GUIDE.md`](CORBIS_MCP_CLAUDE_CODE_GUIDE.md) | Claude Code setup (2 min) |
| [`CORBIS_CURSOR_PLUGIN.md`](CORBIS_CURSOR_PLUGIN.md) | Cursor plugin setup |
| [`CORBIS_MCP_GUIDE.md`](CORBIS_MCP_GUIDE.md) | MCP server architecture (for developers) |

---

<div align="center">

**Built by [Corbis](https://corbis.ai)**

[Get Started](#quick-setup) | [Get a Corbis Key](https://app.corbis.ai) | [MIT License](LICENSE)

</div>
