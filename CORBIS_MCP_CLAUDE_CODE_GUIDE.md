# Corbis MCP Setup Guide for Claude Code

Connect Claude Code to Corbis to give your AI assistant direct access to academic research, economic data, market intelligence, and web search tools — all from your terminal.

If you are using Codex instead, see [`CORBIS_MCP_CODEX_GUIDE.md`](./CORBIS_MCP_CODEX_GUIDE.md). Both clients use the same endpoint and tool set, with client-specific setup.

---

## Prerequisites

- A [Corbis](https://www.corbis.ai) account (free tier or above)
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and working

---

## Step 1: Connect with OAuth

This repository's `.mcp.json` contains the Corbis HTTP URL without credentials. Open Claude Code from the repository root and complete the OAuth sign-in when prompted:

```bash
claude
```

No Corbis MCP API key is required for this path.

### Optional API-key connection

If you prefer a key, create one under Corbis **Settings > API Keys**. It starts with `corbis_mcp_` and is shown only once. Put it in your secret store or shell environment as `CORBIS_MCP_API_KEY`, then create a local-scope override that sends it in an Authorization header:

```bash
claude mcp add-json --scope local corbis '{"type":"http","url":"https://www.corbis.ai/api/mcp/universal","headers":{"Authorization":"Bearer ${CORBIS_MCP_API_KEY}"}}'
```

The single quotes keep the placeholder literal in the saved configuration. Set the environment variable before launching Claude Code. Do not put the key in a URL or a committed file.

### Verify the Connection

Run `claude mcp list` to confirm `corbis` appears in your server list. You can also start a Claude Code session and ask it to search for papers — if the tools appear, you're connected.

---

## Step 2: Start Using Corbis Tools

Once connected, Claude Code can call Corbis tools automatically when relevant. You can also ask for them directly.

### Available Tools

**Research & Papers**
| Tool | What It Does |
|---|---|
| `search_papers` | Hybrid semantic + keyword search across academic papers |
| `get_paper_details` | Full metadata for a specific paper |
| `get_paper_details_batch` | Batch fetch up to 25 papers in one call |
| `literature_search` | Multi-query literature discovery with synthesis* |
| `top_cited_articles` | Highest-cited papers for a topic |
| `search_datasets` | Search research datasets |
| `verify_bibtex` | Check complete BibTeX content against the paper index, when available to the connection |

**Economic Data (FRED)**
| Tool | What It Does |
|---|---|
| `fred_search` | Search the Federal Reserve Economic Database for series |
| `fred_series_batch` | Fetch actual data for one or more FRED series |

**Market Intelligence**
| Tool | What It Does |
|---|---|
| `get_market_data` | Retrieve data for a specific market/metro |
| `compare_markets` | Side-by-side comparison of multiple markets |
| `search_markets` | Find markets matching criteria |
| `get_national_macro` | National-level macroeconomic indicators |
| `get_market_trends` | Metro-level historical time series (BLS, Zillow, BEA, etc.) |

**Web & Deep Research**
| Tool | What It Does |
|---|---|
| `internet_search` | Search the live web for recent information* |
| `read_web_page` | Extract and read content from a URL* |
| `deep_research` | Multi-step web research with synthesis* |

**Citations**
| Tool | What It Does |
|---|---|
| `format_citation` | Format a paper citation in APA, MLA, Chicago, etc. |
| `export_citations` | Export multiple citations in bulk |

**Academic Identity**
| Tool | What It Does |
|---|---|
| `find_academic_identity` | Discover an author's OpenAlex profile |
| `confirm_academic_identity` | Link/confirm an academic identity |

**General**
| Tool | What It Does |
|---|---|
| `query_corbis` | Open-ended questions answered by Corbis AI* |

*Tools marked with \* are **enterprise-only**. See [Tool Access by Tier](#tool-access-by-tier) below.

---

## Tool Access by Tier

Not all tools are available on every plan. Tools are split into two tiers:

| Tier | Available To | Tools |
|---|---|---|
| **Tier 1** (Standard) | All users (Free, Starter, Basic, Academic, Pro, Enterprise) | `search_papers`, `get_paper_details`, `get_paper_details_batch`, `top_cited_articles`, `search_datasets`, `get_market_data`, `compare_markets`, `search_markets`, `get_national_macro`, `get_market_trends`, `fred_search`, `fred_series_batch`, `find_academic_identity`, `confirm_academic_identity`, `export_citations`, `format_citation` |
| **Tier 2** (Premium) | Enterprise only | `internet_search`, `read_web_page`, `deep_research`, `literature_search`, `query_corbis` |

If you call a premium tool on a non-enterprise plan, you'll receive an access denied error.

### Credit Cost

Every MCP tool call costs **1 credit**, regardless of which tool. Credits are deducted from your monthly allowance:

| Plan | Monthly Credits | Price |
|---|---|---|
| Free | 50 (one-time, no reset) | Free |
| Starter | 250 | $20/mo |
| Basic | 1,000 | $49/mo |
| Academic | 1,000 | $30/mo |
| Pro | 5,000 | $199/mo |
| Enterprise | Unlimited | Custom |

---

## Example Prompts

Once connected, try these in Claude Code:

```
Search for recent papers on commercial real estate cap rates
```

```
Get FRED data for the 10-year Treasury rate and plot it
```

```
Compare the office markets in New York, Chicago, and Los Angeles
```

```
Find the top cited articles on machine learning in finance
```

```
Get national macro indicators for the US housing market
```

---

## Troubleshooting

### "401 Unauthorized" errors
- For OAuth, use `/mcp` in Claude Code to reconnect and complete sign-in.
- For the optional API-key override, confirm `CORBIS_MCP_API_KEY` is set in the environment that launched Claude Code and the key still exists under Corbis **Settings > API Keys**.

### Tools not appearing
- Run `claude mcp list` to verify the server is registered.
- Try removing and re-adding: `claude mcp remove corbis` then re-run the add command.
- Restart your Claude Code session.

### "429 Rate Limit" errors
- The MCP server allows **200 requests per hour** and **10 concurrent requests**.
- Wait for the cooldown indicated in the error, or check your credit balance in **Settings > Billing**.

### Connection timeouts
- Verify your network can reach `https://www.corbis.ai`.
- If you're behind a corporate proxy, ensure it allows outbound HTTPS to this domain.

---

## Managing Your Connection

```bash
# List all MCP servers
claude mcp list

# Remove the Corbis server
claude mcp remove corbis

# The repository's URL-only .mcp.json uses OAuth; no key rotation is needed for that path
```

To rotate your key, go to **Settings > API Keys**, click **Regenerate** on the existing key, then update `CORBIS_MCP_API_KEY` in your secret store or shell environment and restart Claude Code.

---

## Related Guides

- [README.md](./README.md) — Starter-kit overview, workflows, and quick setup
- [Corbis MCP Setup Guide for Codex](./CORBIS_MCP_CODEX_GUIDE.md) — Codex-specific `config.toml` setup and troubleshooting
- [Corbis MCP Tool Reference](./CORBIS_MCP_TOOL_REFERENCE.md) — **Detailed parameter reference, output schemas, and recommended workflows for every tool**
- [Corbis Cursor MCP Setup](./CORBIS_CURSOR_PLUGIN.md) — Cursor connection guidance
- [Corbis MCP Server Guide](./CORBIS_MCP_GUIDE.md) — Full architecture and multi-platform setup (Codex, Cursor, Claude, ChatGPT)
