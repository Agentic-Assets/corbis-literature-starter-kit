# Corbis Literature Starter Kit (Cursor plugin)

Cursor plugin that bundles skills, commands, an agent, project rules, and the **Corbis Universal MCP** endpoint for the [Corbis Literature Starter Kit](https://github.com/csirmans/corbis-literature-starter-kit).

## Install (local plugin directory)

1. Clone or copy the starter kit repository.
2. Copy or symlink this folder to your Cursor local plugins directory as `corbis-literature-starter-kit`:

**Windows (PowerShell)**

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.cursor\plugins\local"
Copy-Item -Recurse -Force "PATH\TO\corbis-literature-starter-kit\cursor-plugin" "$env:USERPROFILE\.cursor\plugins\local\corbis-literature-starter-kit"
```

**macOS / Linux**

```bash
mkdir -p ~/.cursor/plugins/local
cp -R path/to/corbis-literature-starter-kit/cursor-plugin ~/.cursor/plugins/local/corbis-literature-starter-kit
# or: ln -s "$(pwd)/cursor-plugin" ~/.cursor/plugins/local/corbis-literature-starter-kit
```

3. Enable the plugin in Cursor (Settings → Plugins) and reload the window if needed.
4. Open the **starter kit repository** as your workspace so paths like `references/` and `output/` match the skills.

## Corbis authentication

This plugin ships `.mcp.json` with the Universal MCP URL only. You must authenticate Corbis separately:

- **Query parameter:** append `?apikey=YOUR_KEY` to the MCP URL in Cursor’s MCP server settings for `corbis`, **or**
- **Bearer token:** set `Authorization: Bearer YOUR_KEY` if your Cursor version supports custom headers for MCP.

Keys are created in the [Corbis app](https://app.corbis.ai) (Settings → API Keys). See the repository root `CORBIS_MCP_GUIDE.md` for modes and troubleshooting.

## What’s included

| Component | Role |
| --- | --- |
| `skills/` | Literature review, positioning, ideas, screening, citations, landscape |
| `commands/` | Prompt wrappers that invoke those skills |
| `agents/paper-reader.md` | Academic paper reading and summarization |
| `rules/corbis-literature.mdc` | Routing and Corbis usage reminders |
| `.mcp.json` | `corbis` → `https://www.corbis.ai/api/mcp/universal` |

## Maintenance: Claude Code vs Cursor

Workflow source for **Claude Code** lives in the repo under `.claude/`. This plugin’s `skills/` (and related files) are a **mirror** for Cursor. If you change a workflow, update both trees or follow a sync checklist so behavior stays aligned.

## Version

See `CHANGELOG.md` and `.cursor-plugin/plugin.json`.
