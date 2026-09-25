# Corbis MCP in Cursor

This starter kit supplies research skills and prompts; it does not package a Cursor plugin. Cursor can still use the Corbis MCP server alongside this repository.

1. In Cursor's MCP settings, add the remote HTTP server at `https://www.corbis.ai/api/mcp/universal`.
2. Complete OAuth sign-in if Cursor offers it for this server. If your account uses a Corbis MCP API key instead, configure the client to send `Authorization: Bearer <key>` through its private credential settings. Do not put the key in the URL or a committed project file.
3. Reload the MCP connection and ask Cursor to search for a paper. Check that a `search_papers` result contains an ID and a source link before relying on it.
4. Open this repository so Cursor can read `AGENTS.md` and the `.agents/skills/` workflows. If the client does not invoke these skills automatically, use the prompt examples in `SKILLS_USE_GUIDE.md`.

Cursor's [MCP documentation](https://prod.cursor.com/help/customization/mcp) describes remote URLs, OAuth, and Authorization headers. For Codex and Claude Code, use the client-specific guides in this repository.
