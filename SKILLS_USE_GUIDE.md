# Skills Use Guide

How to use the 15 Claude research skills across the lifecycle of a finance or real-estate paper.

---

## LaTeX paper template

The `latex_template/` folder contains a ready-to-use LaTeX template for empirical finance papers. When starting a new paper, copy the entire folder and begin filling it in.

**What's included:**
- `academic_paper_template.tex` — full paper structure: title page with blind-review toggle (`\blindtrue`/`\blindfalse`), abstract, JEL codes, introduction, literature review, data section, empirical design, results, robustness, conclusion, appendix, and post-reference tables/figures
- `template_references.bib` — sample BibTeX file (replace with your own; use `export_citations` from Corbis to generate entries)
- `jf.bst` — Journal of Finance bibliography style
- `images/` — example figures (histograms, binned scatter, heterogeneity plot, appendix diagnostic)
- `academic_paper_template.pdf` — compiled preview

**How to start a new paper:**
1. Copy `latex_template/` to a new folder (e.g., `my-paper/`)
2. Open `academic_paper_template.tex` and replace the metadata (title, authors, affiliations, JEL codes, keywords, abstract)
3. Set `\blindtrue` for submission or `\blindfalse` for working-paper circulation
4. Use the `research-paper-writer` skill to draft each section — it follows the same structure as the template
5. Use `export_citations` (BibTeX format) from literature searches to populate your `.bib` file
6. Compile: `pdflatex → bibtex → pdflatex → pdflatex`

**Template sections map to skills:**

| Template section | Skill that drafts it |
|---|---|
| Abstract | `research-paper-writer` (journal-specific word count) |
| Introduction | `research-paper-writer` (7-paragraph structure) |
| Related Literature | `literature-positioning-map` → `research-paper-writer` |
| Data and Variables | `finance-data-construction` (codebook) → `research-paper-writer` |
| Empirical Design | `finance-identification-design` (design memo) → `research-paper-writer` |
| Main Results | `finance-empirical-analysis` (table plan + interpretation) → `research-paper-writer` |
| Robustness | `finance-empirical-analysis` (threat-mapped checks) |
| Conclusion | `research-paper-writer` |
| Appendix variable table | `finance-data-construction` (codebook template) |
| Tables and figures | `finance-empirical-analysis` (table plan) + `research-figure-design` (figure code) |

---

## Quick reference: which skill when

| You want to... | Use this skill |
|---|---|
| Brainstorm or vet a research idea | `finance-idea-screening` |
| Map the literature and sharpen your contribution | `literature-positioning-map` |
| Design or stress-test your identification strategy | `finance-identification-design` |
| Handle spatial, hedonic, repeat-sales, or CRE-specific design | `real-estate-empirical-design` |
| Plan data sourcing, merges, and codebooks | `finance-data-construction` |
| Write Python code for data, regressions, tables, or figures | `python-empirical-code` |
| Plan your table sequence, robustness, and mechanism tests | `finance-empirical-analysis` |
| Design portfolio sorts, alphas, and factor tests | `asset-pricing-test-suite` |
| Draft an introduction, abstract, or results section | `research-paper-writer` |
| Build a seminar, conference, or job-talk deck | `research-seminar-deck` |
| Handle an R&R or draft referee responses | `referee-revision-response` |
| Audit a paper before submission (simulated referee) | `pre-submission-review` |
| Plan and generate publication-ready figures | `research-figure-design` |
| Plan the full project from idea to submission | `research-pipeline-orchestrator` |
| Stress-test a design or decision via structured debate | `research-debate` (invoke-only: `/debate`) |

---

## The research lifecycle and skill sequence

Most papers move through these stages. The skills are designed to be used in roughly this order, though you'll loop back often.

```
 1. Idea          -->  finance-idea-screening
 2. Literature    -->  literature-positioning-map
 3. Design        -->  finance-identification-design
                       (+ real-estate-empirical-design if RE)
                       (+ asset-pricing-test-suite if AP)
 4. Data          -->  finance-data-construction
                       (+ python-empirical-code for implementation)
 5. Analysis      -->  finance-empirical-analysis
                       (+ python-empirical-code for implementation)
                       (+ asset-pricing-test-suite if AP)
 5b. Figures      -->  research-figure-design
                       (+ python-empirical-code for implementation)
 6. Writing       -->  research-paper-writer
 7. Pre-submit    -->  pre-submission-review
 7. Presenting    -->  research-seminar-deck
 8. Revision      -->  referee-revision-response
```

Use `research-pipeline-orchestrator` at any point to get a full roadmap or figure out what stage you're in.

### Structured debate (any stage)

**Skill:** `research-debate` (invoke-only via `/debate`)

**When to invoke:**
- You want to stress-test an identification strategy before committing
- You're choosing between two empirical approaches and want both argued at full strength
- You want to evaluate whether a contribution is strong enough for a target journal
- You're debating mechanism interpretations and want adversarial pushback
- Any decision where you'd benefit from hearing both sides argued rigorously

**What it does:**
- Launches two agents with opposing positions (Skeptic vs. Advocate, or one agent per option)
- Runs 2-3 rounds of structured debate where each agent responds to the other's arguments
- Pauses between rounds so you can inject information or steer the discussion
- Produces a synthesis report: agreed positions, unresolved disagreements, prioritized action items, required diagnostics

**Example prompts:**
- `/debate Is the leave-one-out tenant mean a valid IV for lease term effects on cap rates?`
- `/debate DiD vs. synthetic control for studying opportunity zone effects`
- `/debate Should we target JFE or Real Estate Economics with this paper?`
- `/debate Is our mechanism evidence sufficient or just relabeled heterogeneity?`

**Note:** This skill is token-heavy (7+ agent calls). It is not auto-routed. Use `/debate` only when you want a full adversarial analysis.

---

## Detailed guidance by stage

### Stage 1: Idea screening

**Skill:** `finance-idea-screening`

**When to invoke:**
- You have a rough topic and want to know if it's publishable
- You want to generate ideas from a dataset, friction, or policy change
- You need to decide between multiple ideas
- A coauthor pitches something and you want a quick assessment

**What it does:**
- Scores the idea on 5 dimensions (question, mechanism, design, data, audience)
- Searches the literature to verify novelty (uses Corbis `search_papers` and `top_cited_articles`)
- Produces a Go / Revise / Kill verdict with specific reasoning
- Identifies the 2-3 fatal risks that could sink the paper

**Example prompts:**
- "I have access to fintech lending data — what could I do with it?"
- "Is this housing-supply idea strong enough for REE?"
- "Screen these three corporate-finance ideas and rank them."
- "Generate ideas that exploit the 2023 banking stress as a natural experiment."

---

### Stage 2: Literature positioning

**Skill:** `literature-positioning-map`

**When to invoke:**
- You need to write the related-literature section
- You need a contribution paragraph for the introduction
- A referee says "how is this different from [paper]?"
- You want to check whether your idea has been scooped

**What it does:**
- Runs a systematic search sequence (inner ring → middle ring → outer ring → recent working papers)
- Builds a literature matrix with specific differentiation for each close paper
- Produces a contribution paragraph and related-literature outline
- Exports citations in BibTeX format for your .bib file

**Example prompts:**
- "Position this corporate-finance paper against the payout and investment literatures."
- "What is the nearest paper to this anomaly paper, and how do I differentiate mine?"
- "Search for any recent working papers on mortgage forbearance and housing supply."
- "Build a literature matrix for a climate risk and property values paper."

**Tip:** Use this skill early and again before submission. The literature changes — new working papers appear constantly.

---

### Stage 3: Identification and design

**Skill:** `finance-identification-design`

**When to invoke:**
- You're choosing between identification strategies (DiD vs. IV vs. RD)
- You have a design and want it stress-tested
- You need to map threats to diagnostics
- A referee attacks your identification and you need to respond

**What it does:**
- Produces a full identification memo with estimand, specification, and threat map
- Provides method-specific guidance (staggered DiD, IV, RD, shift-share) with modern references
- Maps every threat to a specific diagnostic or remedy
- Flags when the design is outdated (e.g., TWFE with staggered treatment)

**Example prompts:**
- "Stress-test my DiD design for a debt covenant shock paper."
- "Is TWFE appropriate for my staggered adoption design?"
- "Design the identification strategy for a boundary discontinuity around school districts."
- "How should I cluster standard errors in this state-level policy study?"

#### For real-estate papers: add `real-estate-empirical-design`

**When to invoke:**
- The paper involves property transactions, mortgages, CRE, zoning, or spatial data
- Spatial dependence, boundary designs, or hedonic models are central
- You need to think about appraisal smoothing, repeat-sales bias, or geographic join errors

**What it does (beyond the general design skill):**
- Design-method guidance for 7 RE settings (hedonic, repeat-sales, boundary RD, spatial DiD, mortgage, commercial, climate)
- Measurement-issue table specific to real-estate data
- Spatial inference plan (Conley SEs, two-way clustering, Moulton correction)
- Pulls current CRE market data via Corbis (`get_market_data`, `compare_markets`, `search_markets`)

**Example prompts:**
- "How should I handle spatial correlation in a commercial-real-estate vacancy study?"
- "Design a boundary discontinuity around opportunity zone boundaries."
- "What's the right way to study climate risk capitalization in housing prices?"

#### For asset-pricing papers: add `asset-pricing-test-suite`

**When to invoke:**
- The paper proposes a new signal, anomaly, or factor
- You need portfolio sorts, alpha tests, or Fama-MacBeth regressions
- You need to assess implementability (turnover, capacity, microcap exposure)

**What it does:**
- Designs the full test suite: sorts, alphas against 9 factor models, spanning tests, Fama-MacBeth
- Mandatory implementability section (turnover, capacity, trading costs, short-leg feasibility)
- Checks signal novelty against the Chen-Zimmermann anomaly zoo
- Addresses data snooping (Harvey-Liu-Zhu thresholds)

**Example prompts:**
- "Design the full empirical test suite for this new characteristic."
- "Is my signal just a relabeled version of profitability?"
- "Assess the implementability of this high-turnover strategy."

---

### Stage 4: Data construction

**Skill:** `finance-data-construction`

**When to invoke:**
- You're planning merges across multiple databases (CRSP, Compustat, IBES, etc.)
- You need a codebook or variable dictionary
- You want to ensure reproducibility with proper folder structure
- You're unsure about identifier mapping (PERMNO-GVKEY, ICLINK, etc.)

**What it does:**
- Catalogs 20+ finance and 15+ real-estate data sources with access paths and known issues
- Identifier mapping table with specific pitfalls per merge
- Variable construction standards (winsorization, scaling, date alignment)
- Reproducible folder and script architecture
- FRED series reference table for macro controls

**Example prompts:**
- "Help me merge Compustat, CRSP, and bond data for a capital-structure paper."
- "Build a sample-construction plan for MLS, assessor, and zoning data."
- "What's the right way to link HMDA to property-level data?"
- "Design the data pipeline for a paper using TRACE corporate bond data."

---

### Code implementation (stages 4-5)

**Skill:** `python-empirical-code`

**When to invoke:**
- You need Python code for data cleaning, merges, or variable construction
- You need panel regressions with fixed effects and clustered standard errors
- You need publication-ready LaTeX tables or journal-quality figures
- You want to port Stata or R code to Python
- You need portfolio sorts, Fama-MacBeth, or event-study code
- You need spatial operations for real-estate data (geocoding, distance, Conley SEs)
- You want to scaffold a full project directory structure

**What it does:**
- Generates clean, runnable Python code using `linearmodels`, `statsmodels`, `pandas`, `matplotlib`
- Includes finance-specific recipes: CCM merges, CRSP-Compustat linking, TRACE cleaning, date alignment to avoid look-ahead bias, NYSE breakpoints for portfolio sorts
- Produces LaTeX regression tables and summary statistics tables ready for the paper template
- Creates journal-quality figures (event-study plots, coefficient plots, binned scatters) with proper fonts, sizing, and 300 DPI
- Handles real-estate spatial operations: GeoDataFrame creation, spatial joins, distance calculations, Conley standard errors, repeat-sales indices
- Scaffolds reproducible project structure (`raw/` → `build/` → `analysis/` → `output/`)

**Example prompts:**
- "Write the Python code to merge CRSP and Compustat via CCM."
- "Generate an event-study plot from these regression results."
- "Create a LaTeX regression table from these three specifications."
- "Port this Stata DiD code to Python using linearmodels."
- "Build the full portfolio-sort pipeline for this anomaly paper."
- "Set up the project structure for a corporate-finance paper."

**Tip:** Use `finance-data-construction` to *plan* the data pipeline (which sources, which merges, which variables), then use `python-empirical-code` to *implement* it. Use `finance-empirical-analysis` to *plan* the table sequence and robustness strategy, then use `python-empirical-code` to *write the code*.

---

### Stage 5: Empirical analysis

**Skill:** `finance-empirical-analysis`

**When to invoke:**
- You need a table and figure plan
- You have regression output and need to interpret it properly
- You want to structure robustness checks by threat category
- You need mechanism and heterogeneity test strategy

**What it does:**
- Standard table sequence (summary stats → baseline → robustness → mechanism → heterogeneity)
- 5-step interpretation protocol (result → specification → magnitude → caution → limit)
- Robustness-to-threat mapping (every check tied to a specific concern)
- Code generation guidance (Stata, R, or Python)

**Example prompts:**
- "Plan the results section for this corporate-finance paper."
- "Convert these regression coefficients into economically meaningful magnitudes."
- "Design the mechanism tests for a paper about lending discrimination."
- "Write paragraph-ready interpretations of Tables 2 through 4."

---

### Stage 5b: Figure design

**Skill:** `research-figure-design`

**When to invoke:**
- You need to plan which figures belong in the paper and where
- You want publication-ready Python code for event-study plots, binned scatters, coefficient plots, RD plots, maps, or other standard figure types
- You need figure notes that match journal conventions
- You're unsure which figure types best convey your results

**What it does:**
- Catalogs 13 standard figure types for empirical finance and real-estate papers, each with full Python code
- Provides figure note templates for each type (sample, controls, CI construction, data source)
- Maps standard figure sets by paper type (corporate finance, asset pricing, real estate, descriptive)
- Enforces journal defaults: serif fonts, 300 DPI, 6.5x4.5 inches, PDF output, no chartjunk
- Integrates with Corbis (`fred_series_batch`, `get_market_data`) for time-series context and market data in figures

**Example prompts:**
- "Plan all the figures for my DiD paper on bank lending."
- "Generate an event-study plot with confidence intervals from these coefficients."
- "Create a choropleth map of treatment intensity by county."
- "What figures should a real-estate boundary-RD paper include?"
- "Build a mechanism diagram showing the causal chain in my paper."

**Tip:** Use `finance-empirical-analysis` to plan the *table and figure sequence*, then use `research-figure-design` for the *strategic design and Python code* for each figure. Use `python-empirical-code` if you need the underlying regression or data-processing code that feeds into the figures.

---

### Stage 6: Writing

**Skill:** `research-paper-writer`

**When to invoke:**
- You need an introduction, abstract, conclusion, or results prose
- You want title options
- You need journal-specific formatting (JF vs. REE vs. JREFE abstract style)
- You want a contribution paragraph

**What it does:**
- 7-paragraph introduction structure with paragraph-by-paragraph guidance
- Journal-specific abstract specs (JF/JFE/RFS: ~100 words; JREFE: 150-250 words)
- Results prose following the 5-step interpretation protocol
- Title generation (3-5 options, descriptive to evocative)
- Citation formatting and BibTeX export via Corbis

**Example prompts:**
- "Write a JFE-style introduction from these notes."
- "Draft the abstract and contribution paragraph for a Real Estate Economics submission."
- "Give me 5 title options for this mortgage default paper."
- "Rewrite this conclusion to be more forward-looking."

---

### Stage 7: Pre-submission audit

**Skill:** `pre-submission-review`

**When to invoke:**
- The paper is nearly complete and you want a final quality gate before submission
- You want to catch consistency errors, overclaiming, and missing table documentation
- You want a simulated referee report to anticipate objections
- You want a journal-specific evaluation of contribution and fit

**What it does:**
Launches 6 specialized review agents in parallel, each reading the full LaTeX manuscript:

| Agent | Focus |
|---|---|
| 1 | Spelling, grammar, and academic style |
| 2 | Internal consistency and cross-reference verification |
| 3 | Unsupported claims and identification integrity |
| 4 | Mathematics, equations, and notation |
| 5 | Tables, figures, and their documentation |
| 6 | Contribution evaluation (adversarial journal-specific referee) |

Produces a consolidated report saved to `PRE_SUBMISSION_REVIEW_[date].md` with prioritized action items.

**Example prompts:**
- "Run a pre-submission review of my paper targeting JFE."
- "Audit this real-estate paper before I send it to REE."
- "Simulate a hostile but fair referee report for this corporate-finance paper."
- "Check my paper for overclaiming and missing table notes."

**Tip:** Run this *after* using `research-paper-writer` to draft/polish, but *before* submitting. Fix the critical issues, then submit. If you later get an R&R, use `referee-revision-response` to handle the actual referee reports.

---

### Stage 8: Presenting

**Skill:** `research-seminar-deck`

**When to invoke:**
- You need a conference presentation (15-20 min)
- You're preparing a job talk (75-90 min)
- You want to convert manuscript content into slide logic
- You need backup slides organized by anticipated question type

**What it does:**
- Time budgets by format (conference, workshop, seminar, job talk)
- Main-deck sequence optimized for finance/RE audiences
- Audience-specific adjustments (finance seminars attack ID; RE audiences want institutional detail)
- Backup slide organization by question type
- Speaker notes for each slide

**Example prompts:**
- "Turn my asset-pricing paper into a 15-minute conference deck."
- "Build a job-talk outline for this corporate-finance paper."
- "What backup slides do I need for a hostile identification question?"

---

### Stage 9: Revision

**Skill:** `referee-revision-response`

**When to invoke:**
- You received an R&R and need to plan the revision
- You need to draft point-by-point responses
- Referees disagree with each other
- You need a cover letter to the editor

**What it does:**
- Parses referee reports into classified issues with severity ratings
- Response strategy decision tree (concede / partially concede / disagree with evidence / explain infeasibility)
- Critical-issue triage (identifies the 2-3 issues that determine acceptance)
- Comment-action matrix, response language, cover letter draft
- Fact-checks referee claims about the literature via Corbis

**Example prompts:**
- "Turn these referee reports into a revision matrix."
- "Draft the response to Referee 2 on identification and pretrends."
- "The referees disagree on whether I should add a structural model — how do I handle this?"
- "Write the cover letter for this second-round revision."

---

## Example cases: full skill chains

### Case 1: Corporate-finance paper from scratch

> "I think debt covenant violations affect R&D spending. Help me turn this into a paper."

| Step | Skill | What you get |
|---|---|---|
| 1 | `finance-idea-screening` | Idea card with scoring, novelty check (Chava & Roberts 2008 will surface), Go/Revise/Kill |
| 2 | `literature-positioning-map` | Closest papers, contribution paragraph, BibTeX export |
| 3 | `finance-identification-design` | RD or DiD design memo, threat map, modern methods check |
| 4 | `finance-data-construction` | CRSP-Compustat-Dealscan merge plan, codebook, script architecture |
| 4b | `python-empirical-code` | Python scripts for CCM merge, variable construction, project scaffold |
| 5 | `finance-empirical-analysis` | Table plan, baseline interpretation, robustness by threat |
| 5b | `python-empirical-code` | Regression code, LaTeX tables |
| 5c | `research-figure-design` | Event-study plots, coefficient plots, binned scatters, mechanism diagrams |
| 6 | `research-paper-writer` | Copy `latex_template/`, draft JFE-style introduction, abstract, title options, populate `.bib` via `export_citations` |
| 7 | `pre-submission-review` | 6-agent audit: consistency, overclaiming, table notes, simulated JFE referee report |
| 8 | `research-seminar-deck` | Conference deck blueprint with backup slides |

### Case 2: Real-estate paper on opportunity zones

> "I want to study how opportunity zone designation affects property values."

| Step | Skill | What you get |
|---|---|---|
| 1 | `finance-idea-screening` | Novelty check, scoring, journal-track recommendation (REE vs. JUE) |
| 2 | `literature-positioning-map` | Closest papers (Arefeva et al., Chen et al.), differentiation |
| 3 | `finance-identification-design` | Boundary RD design memo, spatial inference plan |
| 3b | `real-estate-empirical-design` | RE-specific: hedonic vs. repeat-sales, measurement issues, CRE market data for treated zones |
| 4 | `finance-data-construction` | Assessor + deeds + Census merge plan, geocoding strategy |
| 4b | `python-empirical-code` | Spatial join code (geopandas), distance calculations, Conley SEs |
| 5 | `finance-empirical-analysis` | Table sequence, heterogeneity by zone characteristics |
| 5b | `research-figure-design` | Choropleth maps, event-study plots, RD plots for boundary design |
| 6 | `research-paper-writer` | Copy LaTeX template, draft REE-style introduction and abstract, export BibTeX references |

### Case 3: Asset-pricing anomaly paper

> "I found that firms with high customer concentration have lower future returns."

| Step | Skill | What you get |
|---|---|---|
| 1 | `finance-idea-screening` | Novelty check against anomaly zoo, mechanism assessment |
| 2 | `asset-pricing-test-suite` | Full test plan: quintile sorts, alphas vs. FF5/q-factor/q5, Fama-MacBeth, implementability |
| 3 | `literature-positioning-map` | Position against supply-chain finance and concentration literatures |
| 4 | `finance-data-construction` | Compustat segment data + CRSP merge, customer concentration variable construction |
| 5 | `research-paper-writer` | RFS-style introduction, ~100-word abstract |
| 6 | `research-seminar-deck` | 15-minute conference deck with coefficient plots |

### Case 4: Handling an R&R

> "I got an R&R at JFE. Referee 1 attacks my identification. Referee 2 wants more mechanism tests."

| Step | Skill | What you get |
|---|---|---|
| 1 | `referee-revision-response` | Triage (ID concern is critical), comment-action matrix, response language |
| 2 | `finance-identification-design` | Redesigned robustness battery addressing Referee 1's specific concern |
| 3 | `finance-empirical-analysis` | New mechanism test plan for Referee 2 |
| 4 | `literature-positioning-map` | Verify Referee 1's literature claims, find new citations |
| 5 | `research-paper-writer` | Revised introduction with narrowed claims |
| 6 | `referee-revision-response` | Final response letter and cover letter draft |

### Case 5: Job market paper preparation

> "I'm going on the job market with my housing-finance paper. I need everything polished."

| Step | Skill | What you get |
|---|---|---|
| 1 | `research-pipeline-orchestrator` | Full assessment: what's ready, what needs work, timeline |
| 2 | `literature-positioning-map` | Updated literature check for recent working papers that could overlap |
| 3 | `research-paper-writer` | Polished introduction, abstract, and conclusion for JFE/RFS targeting |
| 4 | `research-seminar-deck` | 90-minute job talk blueprint with 25+ backup slides |
| 5 | `research-seminar-deck` | 15-minute conference version for AFA/AREUEA |

---

## Combining skills in a single conversation

You don't need to invoke skills one at a time. Common multi-skill requests:

- **"Take this from idea to design"** — triggers `finance-idea-screening` → `literature-positioning-map` → `finance-identification-design`
- **"Plan the full empirical section"** — triggers `finance-empirical-analysis` + `finance-data-construction` if data questions arise
- **"Help me respond to this R&R and rewrite the intro"** — triggers `referee-revision-response` + `research-paper-writer`
- **"I need a design memo and a deck for a workshop next week"** — triggers `finance-identification-design` + `research-seminar-deck`

Use `research-pipeline-orchestrator` when you're unsure which skill to start with — it will diagnose your stage and route you.

---

## Finance track vs. real-estate track

Most skills work for both tracks. The key differences:

| Dimension | Finance track (JF/JFE/RFS/JFQA/MS) | Real-estate track (REE/JREFE/JUE/JHE) |
|---|---|---|
| Contribution style | Must generalize beyond the setting | Can lean on institutional detail |
| Identification | Sharp causal design expected | Spatial designs, boundary RD more common |
| Data section | Brief in the paper | More detailed, often with maps |
| Abstract length | ~100 words (JF/JFE/RFS) | 100-250 words depending on journal |
| Additional skill | — | `real-estate-empirical-design` |
| Corbis CRE tools | Rarely needed | `get_market_data`, `compare_markets`, `search_markets` |

**Cross-track papers** (mortgage finance, REITs, housing + household portfolios) can target either track. Use `research-pipeline-orchestrator` to evaluate both paths.

---

## Corbis tools across skills

Every skill integrates Corbis MCP tools. The most commonly used:

| Tool | When you'll use it | Which skills use it most |
|---|---|---|
| `search_papers` | Novelty checks, finding close papers, design precedents | All skills |
| `get_paper_details` | Reading abstracts of specific papers | literature-positioning-map, referee-revision-response |
| `top_cited_articles` | Finding seminal papers in a field | idea-screening, literature-positioning-map |
| `export_citations` | BibTeX export for your .bib file | literature-positioning-map, research-paper-writer |
| `fred_series_batch` | Macro controls and context | finance-data-construction, real-estate-empirical-design |
| `get_market_data` | CRE market fundamentals | real-estate-empirical-design |
| `compare_markets` | Cross-metro comparisons | real-estate-empirical-design |
| `search_datasets` | Discovering available data | finance-data-construction, idea-screening |
| `literature_search`* | Comprehensive literature sweeps | literature-positioning-map, idea-screening |
| `internet_search`* | SSRN/NBER working papers, policy docs | All skills |
| `deep_research`* | Complex or fragmented literatures | literature-positioning-map, pipeline-orchestrator |

*\* Enterprise only. If unavailable, use multiple `search_papers` queries as a fallback. See `CORBIS_API_REFERENCE.md` for full details and tier availability.*
