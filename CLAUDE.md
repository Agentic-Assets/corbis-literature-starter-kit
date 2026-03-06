# Project: Academic Finance & Real Estate Research — Powered by Corbis

This project is a template and toolkit for producing empirical research papers targeting top finance journals (JF, JFE, RFS, JFQA, MS) and real-estate journals (REE, JREFE, JRER, JUE, JHE). Corbis MCP tools (corbis.ai) provide literature search, economic data, CRE market intelligence, and citation management throughout the research pipeline.

## Skill routing — read this first

Before responding to any research-related prompt, check whether one or more of the 15 installed skills (`.claude/skills/`) applies. If a skill matches, follow its workflow, deliverables, guardrails, and tool integration instructions. Multiple skills can be combined in a single response.

**Routing quick reference:**

| User is asking about...                     | Use skill                          |
| ------------------------------------------- | ---------------------------------- |
| Research idea, brainstorming, novelty check | `finance-idea-screening`         |
| Literature, contribution, related work      | `literature-positioning-map`     |
| Identification, DiD, IV, RD, threats        | `finance-identification-design`  |
| Real estate design, spatial, hedonic, CRE   | `real-estate-empirical-design`   |
| Data sources, merges, codebook, sample      | `finance-data-construction`      |
| Python code for data, regressions, figures  | `python-empirical-code`          |
| Table plan, robustness, mechanism tests     | `finance-empirical-analysis`     |
| Anomalies, factors, portfolio sorts, alphas | `asset-pricing-test-suite`       |
| Writing: intro, abstract, results, titles   | `research-paper-writer`          |
| Pre-submission audit, consistency check     | `pre-submission-review`          |
| Presentation slides, talk outline           | `research-seminar-deck`          |
| R&R, referee response, revision plan        | `referee-revision-response`      |
| Figure planning and design for the paper     | `research-figure-design`         |
| Full project roadmap, stage diagnosis       | `research-pipeline-orchestrator` |

If unsure which skill applies, use `research-pipeline-orchestrator` to diagnose the stage.

**Invoke-only skill (not auto-routed — use `/debate` only):**

| Stress-test a design, method, or decision    | `research-debate`                |

This skill is token-heavy (7+ agent calls). Do not trigger it automatically. Only activate when the user explicitly invokes `/debate`.

See `SKILLS_USE_GUIDE.md` for detailed guidance, example cases, and multi-skill workflows.

## Research tool usage

Corbis MCP tools are available for literature search, data discovery, market data, and citations. **Always search before asserting** — do not guess about novelty, literature, or data availability when you can check. See `CORBIS_API_REFERENCE.md` for the full API and tier details.

**All tiers:** `search_papers`, `get_paper_details`, `top_cited_articles`, `search_datasets`, `fred_search`, `fred_series_batch`, `get_national_macro`, `get_market_data`, `compare_markets`, `search_markets`, `export_citations`, `format_citation`, `find_academic_identity`, `confirm_academic_identity`

**Enterprise only:** `literature_search`, `internet_search`, `read_web_page`, `deep_research`, `query_corbis`. If unavailable, fall back to multiple `search_papers` queries or ask the user for specific URLs.

Key principles:

- Use `search_papers` before claiming any idea is novel
- Use `get_paper_details` to verify what a paper actually does before characterizing it
- Use `export_citations` (format: `bibtex`) to generate bibliography entries
- Use `fred_series_batch` for macro controls and context
- Use `get_market_data` / `compare_markets` for CRE market intelligence

## Defaults

- **WRDS access**: Set `WRDS_USERNAME` in `.env`. Credentials in `~/.pgpass`. Connect with `wrds.Connection(wrds_username=os.getenv('WRDS_USERNAME'))`. Available: crsp, comp, ibes, tfn, dealscan, tr_dealscan, trace, optionm, boardex, ciq, risk, ff, frb, bank, wrdsapps. Not available: fisd, kld, mfl, rpna, taq.
- **Public data APIs**: API keys in `.env` (copy from `.env.example`). Packages installed: `fredapi`, `pandas-datareader`, `yfinance`, `sec-edgar-downloader`. Load keys with `from dotenv import load_dotenv; load_dotenv()`. If a key is missing, point user to `.env.example`.
- **Language**: Python (using `linearmodels`, `statsmodels`, `pandas`, `matplotlib`). See `python-empirical-code` skill for stack and conventions.
- **LaTeX template**: `latex_template/` — copy this folder when starting a new paper. Uses `jf.bst` bibliography style.
- **Output format**: LaTeX tables (`.tex`) and 300 DPI figures (`.pdf` or `.png`) ready for the paper template. All floats must follow the template format: `\caption{Title}` → `\label{}\vspace{-2.5ex}` → `\floatnotes{descriptive note}` *above* the body → table/figure body. Notes go between the caption and the content, not below.
- **Statistical significance**: Report t-statistics (in parentheses) as the primary measure of statistical significance in tables and text. Not standard errors, not p-values. t-statistics in parentheses below coefficients in regression tables.
- **Standard errors**: Cluster at the level of treatment variation. Do not default to heteroskedasticity-robust only.
- **Econometric methods**: Use modern estimators when appropriate (Callaway-Sant'Anna for staggered DiD, Roth pretrends sensitivity, Oster bounds). Flag when TWFE is inappropriate.

## Writing standards

- Write like a serious empirical researcher, not a grant proposal or blog post.
- Front-load the contribution. A referee decides whether to engage in the first two pages.
- Report economic magnitudes, not only sign and significance.
- Use precise, non-promotional language. No "novel," "groundbreaking," "importantly," or "crucially."
- Do not use em dashes. Use commas, parentheses, colons, or separate sentences instead.
- Do not claim "first" or "to our knowledge" without verifying via literature search.
- Every claim must be supported by the identification strategy — do not overclaim.

### Introduction paragraph 1 rule

The opening paragraph of every introduction must be grounded in a recent, concrete industry event, policy change, or market development that directly motivates the research question. Cite industry reports, news articles, regulatory filings, or practitioner sources (e.g., Fed reports, NBER digests, Wall Street Journal, Financial Times, industry white papers). Do not open with an abstract literature gap. The reader should immediately see why this question matters *now*. Use `internet_search` to find recent motivating events when drafting introductions.

## Project structure

When generating code or organizing files for a research project, follow this structure:

```
project/
  raw/           # Untouched source data (read-only)
  build/         # Cleaning and merge scripts + intermediate data
  analysis/      # Scripts producing tables and figures
  output/
    tables/      # .tex files
    figures/     # .pdf or .png
  codebook/      # Variable definitions
  utils/         # Shared helper functions
  paper/         # LaTeX manuscript (copy of latex_template/)
```

## What not to do

- Do not speculate about the literature when you can search.
- Do not generate regression code without specifying clustering and fixed effects.
- Do not recommend robustness checks that don't map to specific threats.
- Do not write literature reviews as topic-label laundry lists.
- Do not present heterogeneity as mechanism without explicit logic.
- Do not use TWFE with staggered treatment timing without checking for bias.
- Do not promise changes a paper cannot credibly deliver.
- Do not treat statistical significance as economic importance.
