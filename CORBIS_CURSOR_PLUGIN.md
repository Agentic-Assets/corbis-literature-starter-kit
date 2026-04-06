# Corbis Cursor plugin

Use Cursor with **Corbis MCP** and the **Corbis Literature Starter Kit** workflows (skills, commands, rules, and a paper-reader agent).

If you use **Codex** instead of Cursor, start with [`CORBIS_MCP_CODEX_GUIDE.md`](./CORBIS_MCP_CODEX_GUIDE.md). The same Corbis MCP endpoint powers both clients.

## Recommended: bundled plugin in this repository

The Cursor plugin that matches this starter kit lives in **[`cursor-plugin/`](./cursor-plugin/)** (versioned with the repo).

| Field | Value |
| --- | --- |
| **Plugin ID** | `corbis-literature-starter-kit` |
| **Author** | Agentic Assets |
| **Version** | See [`cursor-plugin/.cursor-plugin/plugin.json`](./cursor-plugin/.cursor-plugin/plugin.json) |
| **Install path** | Copy or symlink `cursor-plugin/` → `~/.cursor/plugins/local/corbis-literature-starter-kit/` |

Full install steps, authentication, and maintenance notes: [`cursor-plugin/README.md`](./cursor-plugin/README.md).

### What it includes

- **Skills**: literature review, positioning map, idea generator, idea screening, verify citations, literature landscape (mirrored from `.claude/skills/` for Cursor).
- **Commands**: wrappers that invoke those skills (same names as the Claude Code slash workflows).
- **Agents**: `paper-reader` for academic PDFs and summaries.
- **Rules**: `corbis-literature.mdc` for routing and Corbis usage reminders.
- **MCP**: `.mcp.json` registers the Corbis Universal endpoint (`https://www.corbis.ai/api/mcp/universal`). You still add your API key via URL query or headers in Cursor (see plugin README).

Open the **cloned starter kit** as your workspace so paths like `references/`, `output/`, and `utils/` match the skills.

### Disabling or troubleshooting

If you see errors such as "Rate limit exceeded for client registration" or duplicate MCP registrations, disable the plugin or rename the folder:

```bash
mv ~/.cursor/plugins/local/corbis-literature-starter-kit ~/.cursor/plugins/local/corbis-literature-starter-kit.disabled
```

Restart Cursor or reload the window. To re-enable:

```bash
mv ~/.cursor/plugins/local/corbis-literature-starter-kit.disabled ~/.cursor/plugins/local/corbis-literature-starter-kit
```

If you also added Corbis manually under **Settings → MCP Servers**, use **either** the plugin’s bundled MCP **or** the manual entry, not both with the same server name, to avoid conflicts.

## Direct MCP setup (no plugin)

If you only want Corbis tools without the starter-kit skills and commands, add the server in Cursor:

```json
{
  "mcpServers": {
    "corbis": {
      "url": "https://www.corbis.ai/api/mcp/universal?apikey=YOUR_MCP_API_KEY",
      "headers": {}
    }
  }
}
```

You still get the same research tools; use repo docs ([`SKILLS_USE_GUIDE.md`](./SKILLS_USE_GUIDE.md), [`CLAUDE.md`](./CLAUDE.md)) as prompt context.

## Related documentation

- [README.md](./README.md) — Starter-kit overview and workflow tour.
- [CORBIS_MCP_CODEX_GUIDE.md](./CORBIS_MCP_CODEX_GUIDE.md) — Codex setup using `config.toml`.
- [CORBIS_MCP_GUIDE.md](./CORBIS_MCP_GUIDE.md) — MCP architecture and authentication.
- [CORBIS_MCP_TOOL_REFERENCE.md](./CORBIS_MCP_TOOL_REFERENCE.md) — Tool parameters, outputs, and workflow tips.
