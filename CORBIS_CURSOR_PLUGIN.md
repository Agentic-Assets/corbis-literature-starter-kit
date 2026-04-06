# Corbis Cursor Plugin (coming soon)

The **Corbis** Cursor plugin (ID: `corbis`) is a unified toolkit for Cursor users, providing documentation-first guidance, specialized agents, and runnable MCP tool integration.

If you are using Codex instead of Cursor, start with [`CORBIS_MCP_CODEX_GUIDE.md`](./CORBIS_MCP_CODEX_GUIDE.md). The same Corbis MCP endpoint powers both clients.

- **Author**: Agentic Assets
- **Local Path**: `~/.cursor/plugins/local/corbis/` (when enabled)
- **Version**: 0.1.0

### Disabling the Plugin

If the plugin causes "Rate limit exceeded for client registration" or other OAuth/DCR errors, disable it by renaming the folder:

```bash
mv ~/.cursor/plugins/local/corbis ~/.cursor/plugins/local/corbis.disabled
```

Restart Cursor or reload the window. To re-enable later:

```bash
mv ~/.cursor/plugins/local/corbis.disabled ~/.cursor/plugins/local/corbis
```

## Key Components

### 1. Agents
- **corbis-general**: A specialized agent for Corbis architecture guidance, MCP tool selection, and implementation workflows.

### 2. Skills
- **corbis-core-guidance**: Provides logic-first guidance on using Corbis MCP tools, authentication/scopes, and platform integration patterns.

### 3. MCP Servers
- **corbis**: Pre-configured connection to the Corbis Universal MCP endpoint (`https://www.corbis.ai/api/mcp/universal`).
- Requires `CORBIS_MCP_API_KEY` for authenticated tool access.

## Local Setup & Development

The plugin is currently scaffolded in the user's local plugin directory. To modify or extend:

1. Navigate to `~/.cursor/plugins/local/corbis/`.
2. Edit `.cursor-plugin/plugin.json` to add new components.
3. Reload Cursor or use the plugin discovery mechanism to pick up changes.

## Direct MCP Setup in Cursor

If you do not want the local plugin, you can connect Corbis directly from Cursor's MCP settings:

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

That setup gives Cursor direct access to the same Corbis research tools described throughout this repo.

## Future Roadmap

The plugin is architected for expansion:
- **commands/**: Planned slash commands for common tasks.
- **hooks/**: Lifecycle hooks for automated context injection.
- **rules/**: Domain-specific persistent guidance rules (.mdc).

## Related Documentation

- [README.md](./README.md) - Starter-kit overview and workflow tour.
- [CORBIS_MCP_CODEX_GUIDE.md](./CORBIS_MCP_CODEX_GUIDE.md) - Codex setup using `config.toml`.
- [CORBIS_MCP_GUIDE.md](./CORBIS_MCP_GUIDE.md) - Technical guide for the MCP server architecture.
- [CORBIS_MCP_TOOL_REFERENCE.md](./CORBIS_MCP_TOOL_REFERENCE.md) - Tool-by-tool parameters, output shapes, and usage tips.
- `PUBLISHING_GUIDE.md` (inside plugin folder) - Steps for future public distribution.
