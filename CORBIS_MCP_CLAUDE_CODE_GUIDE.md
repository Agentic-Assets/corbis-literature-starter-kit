# Corbis MCP Setup Guide for Claude Code

Connect Claude Code to Corbis to give your AI assistant direct access to academic research, economic data, market intelligence, and web search tools — all from your terminal.

---

## Prerequisites

- A [Corbis](https://www.corbis.ai) account (free tier or above)
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and working

---

## Step 1: Generate an API Key

1. Open Corbis and go to **Settings > API Keys**.
2. Under **Create a new key**, enter a name (e.g. "Claude Code").
3. Click **Create key**.
4. **Copy the key immediately** — it is only shown once. The key starts with `corbis_mcp_`.

> Tip: Create one key per device (e.g. "Laptop", "Desktop") so you can revoke a single device without disrupting others.

---

## Step 2: Add the MCP Server to Claude Code

Run this command in your terminal, replacing `YOUR_API_KEY` with the key you just copied:

```bash
claude mcp add corbis --transport http https://www.corbis.ai/api/mcp/universal?apikey=YOUR_API_KEY
```

That's it. Claude Code will connect to Corbis on your next session.

### Verify the Connection

Run `claude mcp list` to confirm `corbis` appears in your server list. You can also start a Claude Code session and ask it to search for papers — if the tools appear, you're connected.

---

## Step 3: Start Using Corbis Tools

Once connected, Claude Code can call Corbis tools automatically when relevant. You can also ask for them directly.

### Available Tools (21 total)

**Research & Papers**
| Tool | What It Does |
|---|---|
| `search_papers` | Hybrid semantic + keyword search across academic papers |
| `get_paper_details` | Full metadata for a specific paper |
| `get_paper_details_batch` | Batch fetch up to 25 papers in one call |
| `literature_search` | Multi-query literature discovery with synthesis* |
| `top_cited_articles` | Highest-cited papers for a topic |
| `search_datasets` | Search research datasets |

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
- Your API key may be invalid or revoked. Generate a new one in **Settings > API Keys**.
- Make sure the key is passed correctly in the URL (`?apikey=YOUR_KEY`).

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

# Re-add with a new key
claude mcp add corbis --transport http https://www.corbis.ai/api/mcp/universal?apikey=NEW_API_KEY
```

To rotate your key, go to **Settings > API Keys**, click **Regenerate** on the existing key, then update your Claude Code config with the new key.

---

## Related Guides

- [Corbis MCP Tool Reference](./CORBIS_MCP_TOOL_REFERENCE.md) — **Detailed parameter reference, output schemas, and recommended workflows for every tool**
- [Corbis MCP Server Guide](./CORBIS_MCP_GUIDE.md) — Full architecture and multi-platform setup (Cursor, Claude Desktop, ChatGPT)
- [Corbis Cursor Plugin](./CORBIS_CURSOR_PLUGIN.md) — Cursor plugin setup and troubleshooting
