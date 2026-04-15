# Task Todo

## 2026-04-15 — Add Codex Plugin Support

- [x] Inspect the repo metadata, existing MCP config, and available skill directories
- [x] Create a root Codex plugin manifest at `.codex-plugin/plugin.json`
- [x] Point the plugin at `.agents/skills/` and the existing `.mcp.json`
- [x] Validate the JSON files parse cleanly and the manifest shape matches the Codex plugin spec
- [x] Add a short review section with what changed and verification results

## Review

- Added `.codex-plugin/plugin.json` so the repository can be used as a Codex plugin with its bundled research skills.
- Wired the plugin to `./.agents/skills/` and `./.mcp.json`.
- Normalized `.mcp.json` to use the `corbis` server name and `${CORBIS_MCP_API_KEY}` placeholder, matching the repo's Codex setup guide.
- Verified both JSON files parse successfully with `python3`.
