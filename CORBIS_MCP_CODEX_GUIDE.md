# Corbis MCP Setup Guide for Codex

Connect Codex to Corbis to give the CLI or IDE extension direct access to Corbis research, FRED data, market intelligence, citations, and other MCP tools.

Corbis exposes a streamable HTTP MCP server at `/api/mcp/universal`, and Codex supports HTTP MCP servers through `config.toml`.

---

## Prerequisites

- A Corbis account with MCP connections enabled for your plan
- Codex installed and working
- A Corbis MCP API key from **Settings > API Keys**

Corbis MCP API keys start with `corbis_mcp_` and are shown only once when created.

---

## Recommended Setup

Codex stores MCP servers in `~/.codex/config.toml` for global use, or `.codex/config.toml` for a trusted project.

Add this server entry:

```toml
[mcp_servers.corbis]
url = "https://www.corbis.ai/api/mcp/universal"
bearer_token_env_var = "CORBIS_MCP_API_KEY"
startup_timeout_sec = 20
tool_timeout_sec = 120
```

Then export your key before starting Codex:

```bash
export CORBIS_MCP_API_KEY="corbis_mcp_..."
```

Restart Codex after setting the variable so the MCP server inherits it.

### Why this setup

- It keeps the API key out of `config.toml`
- It uses Codex's native streamable HTTP MCP support
- The same config works for both the Codex CLI and IDE extension

---

## Verify the Connection

Use any of these checks after restarting Codex:

```bash
codex mcp list
```

```bash
codex mcp get corbis
```

Inside the TUI, `/mcp` shows active MCP servers and their status.

If the server initializes correctly, Codex can discover the live Corbis tool list from the MCP endpoint. For the static reference that ships with this starter kit, use [Corbis MCP Tool Reference](./CORBIS_MCP_TOOL_REFERENCE.md).

---

## Example Prompts

Once connected, try prompts like:

```text
Search for recent papers on commercial real estate cap rates
```

```text
Compare the office markets in Austin, Dallas, and Houston
```

```text
Find FRED series for the 10-year Treasury yield and the federal funds rate
```

```text
Get the top cited papers on mortgage default risk
```

---

## Local Development

To connect Codex to a local Corbis dev server instead of production:

```toml
[mcp_servers.corbis]
url = "http://localhost:3000/api/mcp/universal"
bearer_token_env_var = "CORBIS_MCP_API_KEY"
startup_timeout_sec = 20
tool_timeout_sec = 120
```

Use the same environment variable approach for auth.

---

## Troubleshooting

### `codex mcp add` only accepts commands

Some Codex builds expose `codex mcp add` as a stdio-oriented command helper. In that case, editing `config.toml` directly is the correct path for HTTP MCP servers like Corbis.

### `401 Unauthorized`

- Confirm `CORBIS_MCP_API_KEY` is set in the same shell environment that launched Codex
- Confirm the key still exists in Corbis **Settings > API Keys**
- Regenerate the key if needed and restart Codex

### Server appears, but tools do not work

- Make sure the URL is exactly `https://www.corbis.ai/api/mcp/universal`
- Restart Codex after any config or env-var change
- Use `codex mcp get corbis` to confirm Codex loaded the expected server entry

### Premium tools are denied

Corbis gates some MCP tools by subscription tier. The current premium set is `internet_search`, `read_web_page`, `deep_research`, `literature_search`, and `query_corbis`. See [Corbis MCP Tool Reference](./CORBIS_MCP_TOOL_REFERENCE.md) for the tier breakdown in this repo.

### Need a stdio fallback

If your environment cannot use streamable HTTP directly, use a stdio wrapper such as `mcp-remote`. Keep that as a fallback rather than the default for Codex.

---

## API vs. MCP

If you are using Corbis inside Codex, use MCP rather than calling the raw endpoint yourself. Codex gets tool discovery, auth handling, and MCP-native tool calling automatically.

If you are writing your own integration in code, the same backend is the universal MCP JSON-RPC endpoint at `/api/mcp/universal`. See [Corbis MCP Server Guide](./CORBIS_MCP_GUIDE.md).

---

## Related Guides

- [README.md](./README.md) — starter-kit overview and quick setup
- [Corbis MCP Server Guide](./CORBIS_MCP_GUIDE.md) — architecture, auth chain, endpoint behavior, multi-client setup
- [Corbis MCP Tool Reference](./CORBIS_MCP_TOOL_REFERENCE.md) — tool-by-tool params and output shapes
- [Corbis MCP Setup Guide for Claude Code](./CORBIS_MCP_CLAUDE_CODE_GUIDE.md) — Claude-specific setup
