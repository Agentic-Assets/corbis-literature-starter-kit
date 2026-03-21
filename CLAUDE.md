# Project: Academic Finance & Real Estate Research — Powered by Corbis

This project is a template and toolkit for producing empirical research papers targeting top finance journals (JF, JFE, RFS, JFQA, RoF) and real-estate journals (REE, JREFE, JRER, JHE, RSUE). Corbis MCP tools (corbis.ai) provide literature search, economic data, CRE market intelligence, and citation management throughout the research pipeline.

## Skill routing — read this first

Before responding to any research-related prompt, check whether one or more of the 17 installed skills (`.claude/skills/`) applies. If a skill matches, follow its workflow, deliverables, guardrails, and tool integration instructions. Multiple skills can be combined in a single response.

**Routing quick reference:**

| User is asking about...                     | Use skill                          |
| ------------------------------------------- | ---------------------------------- |
| Idea generation, brainstorming from a topic  | `research-idea-generator`        |
| Screen/evaluate a specific research idea     | `finance-idea-screening`         |
| Literature, contribution, related work      | `literature-positioning-map`     |
| Identification, DiD, IV, RD, threats        | `finance-identification-design`  |
| Real estate design, spatial, hedonic, CRE   | `real-estate-empirical-design`   |
| Data sources, merges, codebook, sample      | `finance-data-construction`      |
| Python code for data, regressions, figures  | `python-empirical-code`          |
| Table plan, robustness, mechanism tests     | `finance-empirical-analysis`     |
| Anomalies, factors, portfolio sorts, alphas | `asset-pricing-test-suite`       |
| Writing: any paper section, prose, titles    | `research-paper-writer`          |
| Pre-submission audit, consistency check     | `pre-submission-review`          |
| Presentation slides, talk outline           | `research-seminar-deck`          |
| R&R, referee response, revision plan        | `referee-revision-response`      |
| Figure planning and design for the paper     | `research-figure-design`         |
| Replication package, provenance, archiving  | `replication-package-builder`    |
| Full project roadmap, stage diagnosis       | `research-pipeline-orchestrator` |

If unsure which skill applies, use `research-pipeline-orchestrator` to diagnose the stage.

**Invoke-only skill (not auto-routed — use `/debate` only):**

| Stress-test a design, method, or decision    | `research-debate`                |

This skill is token-heavy (7+ agent calls). Do not trigger it automatically. Only activate when the user explicitly invokes `/debate`.

See `SKILLS_USE_GUIDE.md` for detailed guidance, example cases, and multi-skill workflows.

## Journal targeting

When recommending a journal target or shaping a paper for submission, read `references/journal-targets.md` for detailed per-journal profiles (editors, fees, fit inference, red flags, development advice) and `references/journal-profiles.json` for structured data.

**Routing logic:**

1. Classify the paper's true contribution (not just its data source): broad finance, specialized finance, broad real estate, real estate finance/economics, business-facing real estate, housing economics/policy, or urban/spatial economics.
2. Apply hard filters first:
   - No broad finance contribution → do not force JF, JFE, or RFS
   - Core housing economics/policy → prefer JHE before RE specialty journals
   - Core urban/spatial economics → prefer RSUE before RE specialty journals
3. Score candidates on: topic fit, audience fit, novelty fit, method fit, contribution breadth, data/code readiness.
4. Always output: top 3 targets ranked, rationale for each, 5 revisions to improve fit for the top target, 3 desk-reject risks, and mutable submission details to verify manually.

**Quick routing:**
- **JF**: first-order contribution, broad finance importance
- **JFE**: strong financial economics core, mechanism or theory angle
- **RFS**: major question + especially clean execution + broad implications
- **JFQA**: rigorous finance with quantitative or specialized edge
- **RoF**: innovative, cross-disciplinary, or emerging finance topics
- **REE**: strongest broad real estate papers with general implications
- **JREFE**: real estate grounded in finance or economics (mortgages, REITs, valuation)
- **JRER**: real estate business relevance and decision-making audience
- **JHE**: housing economics, affordability, zoning, rental markets, policy
- **RSUE**: urban, spatial, regional economics with clear spatial dimension

## Research tool usage

Corbis MCP tools are available for literature search, data discovery, market data, and citations. **Always search before asserting** — do not guess about novelty, literature, or data availability when you can check. See `CORBIS_API_REFERENCE.md` for the full API and tier details.

**Available tools:** `search_papers`, `get_paper_details`, `top_cited_articles`, `search_datasets`, `fred_search`, `fred_series_batch`, `get_national_macro`, `get_market_data`, `compare_markets`, `search_markets`, `export_citations`, `format_citation`, `find_academic_identity`, `confirm_academic_identity`

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
- **LaTeX template**: `latex_template/` — copy this folder when starting a new paper. Uses `jf.bst` bibliography style. **Before writing any LaTeX output, read `references/latex-formatting-reference.md`** for the complete formatting specification (float structure, table/figure templates, custom commands, equations, citations). Follow it exactly.
- **Output format**: Write LaTeX tables to `output/tables/*.tex` files and figure float wrappers to `output/figures/*.tex` files. Do not put LaTeX content in the chat for the user to copy-paste. Save figures as 300 DPI `.pdf` or `.png`. Paper prose should be written directly into the `.tex` file using the Edit tool.
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
- **Theory and model exposition**: When discussing theoretical models, lead with the economic intuition and story. Place Greek letters and formal notation in parentheses after the plain-language explanation. The reader should grasp the mechanism from the prose alone; notation confirms the mapping, it does not carry the argument.

### Introduction paragraph 1 rule

The opening paragraph of every introduction must be grounded in a recent, concrete industry event, policy change, or market development that directly motivates the research question. Cite industry reports, news articles, regulatory filings, or practitioner sources (e.g., Fed reports, NBER digests, Wall Street Journal, Financial Times, industry white papers). Do not open with an abstract literature gap. The reader should immediately see why this question matters *now*. Use `search_papers` with recent year filters to find academic papers that reference motivating events. For news, trade press, or practitioner sources that `search_papers` cannot retrieve, ask the user to provide the source or URL.

## Project structure

When generating code or organizing files for a research project, follow this structure:

```
project/
  raw/           # Untouched source data (read-only)
  build/         # Cleaning and merge scripts + intermediate data
  explore/       # Throwaway exploration scripts (delete freely)
  analysis/      # Promoted scripts producing final tables and figures
  output/
    tables/      # .tex files
    figures/     # .pdf or .png
  notes/         # Lab notebook and working notes (.md)
  codebook/      # Variable definitions
  utils/         # Shared helper functions
  paper/         # LaTeX manuscript (copy of latex_template/)
```

**Workflow**: Exploration scripts go in `explore/`. When a test produces a keeper, move the script to `analysis/` and log the result in `notes/lab_notebook.md`. Once the table/figure set is complete, use the lab notebook to transition to writing the paper.

## Lab notebook automation

Every skill that produces a deliverable must append a dated entry to `notes/lab_notebook.md`. This creates a continuous research audit trail that is invaluable for writing the paper, responding to referees, and resuming work after a break.

**When to log**: After completing any skill invocation that produces a deliverable (design memo, table plan, lit search, figure plan, code output, writing draft, review report, etc.).

**Entry format**:

```markdown
---

### YYYY-MM-DD — [Skill name]: [Brief description]

**What was done**: [1-2 sentences describing the task]

**Key findings**:
- [Finding 1]
- [Finding 2]

**Decisions made**: [What was decided and why]

**Output files**: [List of files created or modified]

**Next steps**: [What should happen next]
```

**Rules**:
- Use the actual date, not relative dates.
- If `notes/lab_notebook.md` does not exist, create it with a header: `# Lab Notebook — [Project Name]`.
- Append at the bottom. Do not overwrite or reorder existing entries.
- Keep entries concise. The notebook is a log, not a report.
- Log null results and dead ends too. These inform the paper's robustness discussion and help avoid revisiting failed approaches.
- When promoting an exploration script to `analysis/`, log the promotion and what the script produces.

## Project state (cross-skill context)

Skills should read and update `notes/project_state.md` to pass context between invocations. This prevents the user from re-explaining decisions that were already made in a prior skill invocation.

**When to read**: At the start of any skill invocation, check whether `notes/project_state.md` exists. If it does, read it to understand the current state of the project before proceeding.

**When to update**: After completing a skill invocation, update the relevant section(s) of `notes/project_state.md` with any new decisions, findings, or outputs.

**File structure**:

```markdown
# Project State

## Paper metadata
- **Working title**:
- **Target journal**:
- **Track**: [finance / real-estate]
- **Stage**: [idea / literature / design / data / analysis / writing / pre-submission / revision]
- **Last updated**: YYYY-MM-DD

## Research question
[One-sentence question]

## Mechanism and predictions
[The economic mechanism and testable predictions]

## Identification strategy
- **Method**: [DiD / IV / RD / portfolio sorts / etc.]
- **Source of variation**:
- **Key threats**:
- **Design memo file**: [path if exists]

## Literature positioning
- **Closest papers**: [2-3 papers with differentiation]
- **Contribution claim**: [one sentence]
- **Literature matrix file**: [path if exists]

## Data
- **Sources**: [list]
- **Sample period**:
- **Key variables**:
- **Known issues**:
- **Build scripts**: [paths]

## Analysis status
- **Table plan**: [path if exists]
- **Completed tables**: [list]
- **Completed figures**: [list]
- **Key results**: [1-2 sentence summary of main finding]

## Writing status
- **Sections drafted**: [list]
- **Paper file**: [path]

## Open questions
- [Question 1]
- [Question 2]
```

**Rules**:
- If `notes/project_state.md` does not exist when a skill needs to update it, create it with the template above and fill in what is known.
- Only update sections relevant to the current skill. Do not overwrite sections populated by other skills unless the information has changed.
- Keep entries factual and brief. This is a coordination file, not a narrative.
- The `Stage` field should reflect the earliest incomplete stage, not the most recent activity.
- When the user starts a new project, the first skill invoked should initialize this file.

## What not to do

- Do not speculate about the literature when you can search.
- Do not generate regression code without specifying clustering and fixed effects.
- Do not recommend robustness checks that don't map to specific threats.
- Do not write literature reviews as topic-label laundry lists.
- Do not present heterogeneity as mechanism without explicit logic.
- Do not use TWFE with staggered treatment timing without checking for bias.
- Do not promise changes a paper cannot credibly deliver.
- Do not treat statistical significance as economic importance.
