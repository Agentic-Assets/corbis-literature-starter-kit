# Corbis Literature Starter Kit

A starter kit for exploring academic literature, brainstorming research ideas, and managing citations with AI coding assistants. Powered by [Corbis](https://corbis.ai) MCP.

Works with **Claude Code**, **Cursor**, and **Codex**. Clone it, connect Corbis, and start exploring 250,000+ academic papers from your terminal or IDE.

## What you get

**6 research workflows** (slash commands in Claude Code, natural language in Cursor/Codex):

| Command | What it does |
|---|---|
| `/lit-review` | Write a structured literature review on any topic |
| `/lit-search` | Map the closest papers and sharpen your contribution |
| `/brainstorm` | Generate ranked research ideas with internal rejection filtering |
| `/idea` | Screen and score a specific research idea |
| `/verify-citations` | Audit your .bib file against the literature |
| `/lit-landscape` | Visualize literature trends, gaps, and methods (Python figures) |

Plus a **paper-reader agent** that can summarize any academic PDF.

## Quick setup

### Claude Code

```bash
# 1. Install Claude Code (https://docs.anthropic.com/en/docs/claude-code)
# 2. Connect Corbis MCP (takes 2 min — see CORBIS_MCP_CLAUDE_CODE_GUIDE.md)
claude mcp add corbis --transport http https://app.corbis.ai/api/mcp/universal?apikey=YOUR_API_KEY
# 3. Clone and start
git clone https://github.com/csirmans/corbis-literature-starter-kit.git my-project
cd my-project
claude
```

### Cursor

```bash
# 1. Clone the repo
git clone https://github.com/csirmans/corbis-literature-starter-kit.git my-project
cd my-project
# 2. Add Corbis MCP in Cursor Settings > MCP Servers:
#    Name: corbis
#    URL: https://app.corbis.ai/api/mcp/universal?apikey=YOUR_API_KEY
# 3. Open the project in Cursor — it reads CLAUDE.md automatically
```

See [`CORBIS_CURSOR_PLUGIN.md`](CORBIS_CURSOR_PLUGIN.md) for the full Cursor plugin setup.

### Codex / other agents

Any MCP-compatible agent can use the Corbis tools. Connect to the endpoint:
```
https://app.corbis.ai/api/mcp/universal?apikey=YOUR_API_KEY
```

The `CLAUDE.md` file provides project instructions that most agents will read automatically. The skills in `.claude/skills/` define the research workflows.

## Get a Corbis API key

1. Go to [corbis.ai](https://app.corbis.ai) and create an account (free tier available)
2. Navigate to **Settings > API Keys**
3. Create a key (starts with `corbis_mcp_`)
4. Use it in the setup commands above

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

**Visualize a literature's structure:**
```
/lit-landscape corporate governance and firm performance
```

## Optional dependencies

**LaTeX** (for writing papers): Copy `latex_template/` to `paper/` and compile with any LaTeX distribution (MacTeX, TeX Live, MikTeX).

**Python** (for `/lit-landscape` figures only):
```bash
pip install -r requirements.txt
```

## Project structure

```
notes/           # Lab notebook (auto-populated by skills)
output/          # Literature reviews, positioning memos, figures
paper/           # Your LaTeX manuscript (copy from latex_template/)
latex_template/  # Clean article template with natbib citations
utils/           # Python utilities (lit_landscape.py)
references/      # Writing norms and citation formatting
.claude/
  skills/        # 6 research workflow definitions
  commands/      # 6 slash commands
  agents/        # Paper-reader agent
  settings.json  # Pre-approved permissions
```

## Documentation

| File | Purpose |
|---|---|
| `CLAUDE.md` | Project instructions (loaded every session by Claude/Cursor) |
| `SKILLS_USE_GUIDE.md` | When to use each workflow, with examples |
| `CORBIS_MCP_TOOL_REFERENCE.md` | All 21 Corbis MCP tools: parameters, outputs, tips |
| `CORBIS_MCP_CLAUDE_CODE_GUIDE.md` | Claude Code setup guide |
| `CORBIS_CURSOR_PLUGIN.md` | Cursor plugin setup guide |
| `CORBIS_MCP_GUIDE.md` | MCP server architecture (for developers) |

## License

[MIT](LICENSE)
