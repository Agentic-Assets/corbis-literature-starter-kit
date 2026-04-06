# Corbis MCP Server Guide

The Corbis MCP (Model Context Protocol) server exposes Corbis research, economic data, market intelligence, and AI tools to external AI agents including Codex, Cursor, Claude Code, ChatGPT, and custom clients. This guide covers both the internal architecture and user-facing setup.

---

## Part 1: How It Works on the Inside

### Architecture Overview

The Corbis MCP server is a **universal endpoint** built with `mcp-handler` v1.0.7. It serves:

- **Tools** (21): Functions agents can call (search papers, fetch FRED data, web search, etc.)
- **Resources**: Read-only documentation and setup context for MCP clients
- **Transports**: Streamable HTTP (JSON-RPC) and SSE (Server-Sent Events)

Protocol versions: `2024-11-05`, `2025-03-26`, `2025-06-18`.

### Key File References

| Layer | Path | Purpose |
|-------|------|---------|
| **API route** | `app/api/mcp/universal/route.ts` | Main MCP handler; GET (discovery/SSE), POST (JSON-RPC), DELETE (session cleanup) |
| **Tool registry** | `lib/mcp/tools/registry.ts` | Central export of all 21 tools via `MCP_TOOLS` array |
| **Tool definitions** | `lib/mcp/tools/*.ts` | Individual tools (e.g. `search-papers.ts`, `fred-search.ts`, `query-corbis.ts`) |
| **Resources** | `lib/mcp/resources/docs.ts` | `MCP_RESOURCES` and `RESOURCE_REGISTRY` for documentation URIs such as `docs://system`, `docs://tools`, `docs://auth`, and related setup docs |
| **Auth** | `lib/mcp/auth.ts` | `authenticateMCPRequest`, `verifyToken`, `extractToken`, rate limiter |
| **Guidance** | `lib/mcp/guidance.ts` | Extra prompts appended to tool responses only for MCP clients |
| **OAuth** | `app/api/mcp/oauth/register/route.ts`, `app/api/mcp/oauth/token/route.ts` | Dynamic client registration and token exchange |

### Tool Structure (Zod-based)

Each tool follows a consistent pattern:

```typescript
// lib/mcp/tools/search-papers.ts
export const SearchPapersSchema = z.object({
  query: z.string().min(1).max(500).describe('...'),
  matchCount: z.number().int().min(1).max(20).default(10).optional(),
  // ...
});

export const searchPapersTool = {
  name: 'search_papers',
  description: 'Search academic papers using hybrid semantic-keyword search...',
  schema: SearchPapersSchema,
  execute: async (input, session: AuthSession) => { /* business logic */ },
};
```

- **Schema**: Zod schema → converted to JSON Schema for MCP (`zodToJsonSchema`)
- **Execute**: Receives `(input, session)`; session comes from auth resolution
- **Business logic**: Often delegates to shared logic in `lib/mcp/business-logic/` or `lib/ai/tools/`

### Request Flow

1. **Discovery** (unauthenticated): `initialize`, `tools/list`, `resources/list`—no auth required per MCP spec.
2. **Tool call** (`tools/call`): Auth required. Token extracted from:
   - `Authorization: Bearer <token>`
   - `?apikey=` or `?token=` query params
3. **Auth chain**: Custom OAuth JWT → personal MCP API key (`corbis_mcp_*`) → global `MCP_API_KEYS` → Supabase OAuth → Supabase JWT.
4. **Scope enforcement**: Each tool maps to scopes (e.g. `search_papers` → `read:papers`). OAuth tokens must include required scopes.
5. **Rate limit**: 200 req/hour per user, 10 concurrent; headers `X-RateLimit-*`.

### Tool-to-Scope Mapping

Defined in `app/api/mcp/universal/route.ts` (TOOL_SCOPES):

| Scope | Tools |
|-------|-------|
| `read:papers` | search_papers, get_paper_details, literature_search, export_citations, top_cited_articles, format_citation, search_datasets |
| `read:economic_data` | fred_search, fred_series_batch |
| `read:market_data` | get_market_data, compare_markets, search_markets, get_national_macro |
| `read:web` | internet_search, read_web_page, deep_research |
| `read:profile` | find_academic_identity, confirm_academic_identity |
| `read:corbis` | query_corbis |

---

## Part 2: How It Works from the Outside

### What Users Get

When you connect an AI agent (Codex, Cursor, Claude Code, ChatGPT, or another MCP client) to the Corbis MCP server, the agent gains access to:

- **21 tools** for research, economic data, market intel, web search, citations, and open-ended queries
- **read-only documentation resources** for setup, tool reference, pricing, and workflow guidance

Agents use tools by name (e.g. `search_papers`, `fred_search`, `query_corbis`) and receive JSON results. Some tools also return inline guidance to help the agent use the output correctly.

### Authentication Options

1. **Personal MCP API Key** (recommended for Codex, Cursor, Claude Code, and Claude Desktop):
   - Generate in Corbis: **Settings → API Keys → Create MCP Key**
   - Format: `corbis_mcp_xxxxxxxxxxxx` (displayed once at creation)
   - Include via `Authorization: Bearer <key>` or `?apikey=<key>`

2. **OAuth 2.1** (for external platforms like ChatGPT):
   - Register client at `POST /api/mcp/oauth/register`
   - User approves scopes at consent URL
   - Exchange code for JWT at `POST /api/mcp/oauth/token`
   - Use JWT in `Authorization: Bearer <token>`

3. **Supabase JWT** (web app context):
   - Active session token from `auth.users`
   - Supports internal Corbis web flows

### Connecting from Cursor IDE

1. Open **Cursor Settings → MCP** (or edit `.cursor/mcp.json`).
2. Add the Corbis server:

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

Replace `YOUR_MCP_API_KEY` with your personal key from Corbis.

3. Restart Cursor or reload MCP servers.
4. In chat, the agent can call tools when relevant (e.g. “Search for papers on commercial real estate cap rates”).

**Note**: For local development, use `http://localhost:3000/api/mcp/universal?apikey=YOUR_KEY` instead.

If you want the plugin-oriented setup that ships with this starter kit, see [CORBIS_CURSOR_PLUGIN.md](./CORBIS_CURSOR_PLUGIN.md).

### Connecting from Codex

Codex supports streamable HTTP MCP servers through `config.toml`. For Corbis-specific setup, environment-variable auth, verification steps, and troubleshooting, see [CORBIS_MCP_CODEX_GUIDE.md](./CORBIS_MCP_CODEX_GUIDE.md).

### Connecting from Claude Code and Claude Desktop

For Claude Code, the quickest path is:

```bash
claude mcp add corbis --transport http "https://www.corbis.ai/api/mcp/universal?apikey=YOUR_MCP_API_KEY"
```

For Claude Desktop-style JSON configuration, use:

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

For a fuller Claude Code walkthrough, see [CORBIS_MCP_CLAUDE_CODE_GUIDE.md](./CORBIS_MCP_CLAUDE_CODE_GUIDE.md).

### Tool Usage Patterns

| Use Case | Recommended Tool(s) |
|----------|---------------------|
| Academic paper search | `search_papers`, `literature_search` |
| Full paper metadata | `get_paper_details` |
| Economic / FRED data | `fred_search` → `fred_series_batch` (create fresh code artifact after) |
| Market comparison | `get_market_data`, `compare_markets`, `search_markets` |
| National macro | `get_national_macro` |
| Web / recent info | `internet_search`, `read_web_page`, `deep_research` |
| Format citations | `format_citation`, `export_citations` |
| Open-ended questions | `query_corbis` |
| Academic identity | `find_academic_identity`, `confirm_academic_identity` |

### Rate Limits and Errors

- **200 requests/hour** per authenticated user
- **10 concurrent** requests
- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- **401**: Missing/invalid token
- **429**: Rate limit exceeded; check `X-RateLimit-Reset` for retry time

### Resources Available to Agents

Agents can read these resources for context:

- `docs://system` – System overview, tool summaries, auth notes
- `docs://tools` – Per-tool reference (params, return shapes)
- `docs://auth` – Authentication setup and API key usage
- `docs://quickstart` – 5-minute getting started guide
- `docs://data-sources` – Market data sources (BLS, Census, FHFA, HUD, BEA, IRS)
- `docs://workflows` – Research workflows and deliverable patterns
- `docs://mcp-guide` – Multi-platform MCP integration guide
- `docs://pricing` – Subscription tiers and credit details

---

## Related Documentation

- [README.md](./README.md) – Starter-kit overview and workflow tour
- [CORBIS_MCP_CODEX_GUIDE.md](./CORBIS_MCP_CODEX_GUIDE.md) – Codex-specific setup and troubleshooting
- [CORBIS_MCP_CLAUDE_CODE_GUIDE.md](./CORBIS_MCP_CLAUDE_CODE_GUIDE.md) – Claude Code setup
- [CORBIS_CURSOR_PLUGIN.md](./CORBIS_CURSOR_PLUGIN.md) – Cursor plugin and direct MCP setup notes
- [CORBIS_MCP_TOOL_REFERENCE.md](./CORBIS_MCP_TOOL_REFERENCE.md) – Tool-by-tool params, outputs, and workflow guidance
