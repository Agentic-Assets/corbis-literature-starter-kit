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

## 2026-04-15 — Codex Plugin Discovery Audit

- [x] Audit the existing Codex plugin manifest, MCP wiring, and skill inventory
- [x] Add missing discovery artifacts for marketplace-style plugin discovery without restructuring the repo
- [x] Validate every discovery JSON file and document the final discovery paths

## Review

- Kept the existing repo-root Codex plugin manifest in place for direct use from the repository root.
- Added `.agents/plugins/marketplace.json` so the repo now exposes a marketplace-style discovery index.
- Added `plugins/corbis-literature-starter-kit/.codex-plugin/plugin.json` as a lightweight packaged wrapper that points back to the repo's shared `.agents/skills/` directory and `.mcp.json`.
- Verified JSON parsing for `.codex-plugin/plugin.json`, `.mcp.json`, `.agents/plugins/marketplace.json`, and `plugins/corbis-literature-starter-kit/.codex-plugin/plugin.json`.
- Verified the packaged plugin resolves its `skills` path to `./.agents/skills/` and its `mcpServers` path to `./.mcp.json` successfully.
