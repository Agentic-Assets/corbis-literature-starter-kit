# Academic Finance & Real Estate Research Template

A Claude Code project template for producing empirical research papers targeting top finance journals (JF, JFE, RFS, JFQA, MS) and real-estate journals (REE, JREFE, JRER, JUE, JHE).

This template turns Claude Code into a research co-pilot that understands the full lifecycle of an academic paper: from idea screening through literature review, identification design, data construction, empirical analysis, writing, pre-submission review, presentations, and referee responses.

## What's included

```
ResearchTemplate/
  CLAUDE.md                  # Project instructions (loaded every session)
  SKILLS_USE_GUIDE.md        # When and how to use each skill
  CORBIS_API_REFERENCE.md    # Corbis MCP tool documentation
  latex_template/            # Publication-ready LaTeX paper template
  .env.example               # API keys and WRDS credentials template
  .gitignore                 # Configured for academic projects
  .claude/
    skills/                  # 14 research skills (see below)
    commands/                # 14 slash commands for quick access
    settings.json            # Pre-approved permissions and hooks
```

### 15 research skills

| Skill | What it does |
|---|---|
| `finance-idea-screening` | Score and vet research ideas with novelty checks |
| `literature-positioning-map` | Systematic literature search, contribution sharpening |
| `finance-identification-design` | Design and stress-test causal identification (DiD, IV, RD) |
| `real-estate-empirical-design` | RE-specific: hedonic, repeat-sales, boundary RD, spatial |
| `finance-data-construction` | Data sourcing, merges, codebooks, reproducibility |
| `python-empirical-code` | Python code for regressions, tables, figures, WRDS access |
| `finance-empirical-analysis` | Table plans, robustness structure, interpretation |
| `asset-pricing-test-suite` | Portfolio sorts, alphas, Fama-MacBeth, signal novelty |
| `research-paper-writer` | Draft introductions, abstracts, results prose |
| `research-figure-design` | Plan and generate all common academic figure types |
| `research-debate` | Multi-round adversarial debate (invoke-only via `/debate`) |
| `pre-submission-review` | 6-agent parallel audit simulating a hostile referee |
| `research-seminar-deck` | Conference, seminar, and job-talk presentation design |
| `referee-revision-response` | Parse referee reports, plan revisions, draft responses |
| `research-pipeline-orchestrator` | Full project roadmap and stage diagnosis |
| `research-debate` | Multi-round adversarial debate on any research decision |

### 14 slash commands

Type these directly in Claude Code for quick access:

| Command | Action |
|---|---|
| `/idea` | Screen a research idea |
| `/lit-search` | Search literature and build a positioning memo |
| `/design` | Design or stress-test an identification strategy |
| `/data-plan` | Plan data sourcing and merges |
| `/wrds` | Query WRDS databases |
| `/data-fetch` | Fetch data from public APIs (FRED, BLS, Census, BEA) |
| `/table` | Generate a LaTeX regression table |
| `/figure` | Plan and generate publication-ready figures |
| `/intro` | Draft a 7-paragraph introduction |
| `/deck` | Build a presentation outline |
| `/review-paper` | Run a 6-agent pre-submission audit |
| `/referee` | Parse referee reports and draft responses |
| `/roadmap` | Diagnose project stage and build a roadmap |
| `/debate` | Run a structured multi-round debate on a research question |

### Built-in automation

- **LaTeX auto-compile**: `.tex` files are compiled to PDF automatically when edited
- **Python auto-format**: `.py` files are formatted with ruff/black on save
- **Pre-approved permissions**: Read/search files, run Python, compile LaTeX, and use git without prompts

## Setup

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and configured
- Python 3.10+
- A LaTeX distribution (MacTeX, TeX Live, or MikTeX) for paper compilation
- [Corbis MCP](https://corbis.ai) connected to Claude Code for literature search, economic data, and citations

### 1. Clone or copy the template

```bash
git clone <repo-url> my-paper
cd my-paper
```

### 2. Set up credentials

```bash
cp .env.example .env
```

Edit `.env` and fill in:
- `WRDS_USERNAME` -- your institutional WRDS login
- `FRED_API_KEY` -- free at [fred.stlouisfed.org](https://fred.stlouisfed.org/docs/api/api_key.html)
- `BLS_API_KEY` -- free at [data.bls.gov](https://data.bls.gov/registrationEngine/)
- `CENSUS_API_KEY` -- free at [api.census.gov](https://api.census.gov/data/key_signup.html)
- `BEA_API_KEY` -- free at [apps.bea.gov](https://apps.bea.gov/API/signup/)

For WRDS, you also need PostgreSQL credentials in `~/.pgpass`:
```
wrds-pgdata.wharton.upenn.edu:9737:wrds:YOUR_USERNAME:YOUR_PASSWORD
```

### 3. Install Python packages

```bash
pip install wrds linearmodels statsmodels pandas matplotlib numpy scipy \
  fredapi pandas-datareader yfinance sec-edgar-downloader python-dotenv \
  geopandas ruff
```

### 4. Start a new paper

Copy the LaTeX template into your project:

```bash
cp -r latex_template/ paper/
```

Then open Claude Code and start working:

```bash
claude
```

## Usage

### Starting a new project

Ask Claude to diagnose where you are and what to do next:

```
/roadmap I have an idea about how bank branch closures affect small business lending
```

Or go straight to idea screening:

```
/idea Bank branch closures reduce small business lending through relationship destruction
```

### Example workflows

**From idea to design:**
```
/idea [describe your idea]
/lit-search [your topic]
/design [your identification strategy]
```

**Building the empirical pipeline:**
```
/data-plan I need HMDA mortgage data merged with Census tract demographics
/wrds download CRSP monthly stock file for 2010-2023
/table Generate a baseline regression table with firm and year FE
/figure Create an event-study plot from these coefficients
```

**Writing and polishing:**
```
/intro [paste your notes and key findings]
/review-paper targeting JFE
/referee [paste referee reports]
```

### How skills work

You don't need to invoke skills manually. Claude reads `CLAUDE.md` at the start of every session and automatically routes your request to the right skill based on what you're asking. The slash commands are shortcuts for common tasks, but natural language works just as well:

> "Help me design the identification strategy for a staggered DiD around state-level marijuana legalization and commercial property values"

Claude will activate `finance-identification-design` + `real-estate-empirical-design` and produce a full design memo with threat mapping.

### Writing conventions

The template enforces several conventions from top finance journals:

- **t-statistics** (not standard errors or p-values) as the primary significance measure
- **No em dashes** in prose
- **No filler words** like "crucially," "importantly," or "interestingly"
- **Introduction paragraph 1** must be grounded in a recent industry event with a citation
- **Table/figure format** follows the LaTeX template: caption on top, descriptive note between caption and body, then the content
- **Standard errors** clustered at the level of treatment variation
- **Modern econometrics** by default (Callaway-Sant'Anna for staggered DiD, Roth pretrends)

### Corbis MCP tools

Most Corbis tools are available on all plans. Five tools require an enterprise subscription:

| All tiers | Enterprise only |
|---|---|
| `search_papers`, `get_paper_details`, `top_cited_articles` | `literature_search` |
| `search_datasets`, `fred_search`, `fred_series_batch` | `internet_search`, `read_web_page` |
| `get_market_data`, `compare_markets`, `search_markets` | `deep_research`, `query_corbis` |
| `export_citations`, `format_citation` | |

When enterprise tools are unavailable, skills automatically fall back to all-tier alternatives (e.g., multiple `search_papers` queries instead of `literature_search`).

See `CORBIS_API_REFERENCE.md` for full documentation.

## Project structure for your paper

When you start building your research project, Claude will organize files like this:

```
my-paper/
  raw/           # Untouched source data (read-only, gitignored)
  build/         # Cleaning and merge scripts + intermediate data
  analysis/      # Scripts producing tables and figures
  output/
    tables/      # .tex files
    figures/     # .pdf or .png
  codebook/      # Variable definitions
  utils/         # Shared helper functions
  paper/         # LaTeX manuscript (copy of latex_template/)
```

## Documentation

| File | Purpose |
|---|---|
| `CLAUDE.md` | Project instructions loaded every session (skill routing, defaults, writing rules) |
| `SKILLS_USE_GUIDE.md` | Detailed guide: when to use each skill, example cases, multi-skill workflows |
| `CORBIS_API_REFERENCE.md` | All 19 Corbis MCP tools with parameters, tier availability, and recommended chains |

## License

MIT
