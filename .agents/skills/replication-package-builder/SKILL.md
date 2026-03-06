---
name: replication-package-builder
description: "Build replication packages for journal submission, coauthor handoff, or public archiving. Use for provenance mapping, data classification, environment capture, and replication READMEs."
---

# Replication Package Builder

Turn a working research project into a rerunnable, auditable package for coauthors, referees, journal data editors, and future-you.

This skill sits downstream of data construction, empirical code, and paper writing. It is complementary to `pre-submission-review` — that skill audits the paper; this skill packages the code and data.

## When to use this skill

- The paper is nearly complete and needs a replication package for journal submission
- The user is preparing a coauthor handoff or lab archive
- The user wants to build a public GitHub companion repo
- Referees or data editors asked for exact construction details during an R&R
- The user wants to freeze a versioned archive before major revisions

## Workflow

Execute these steps in order. Do not skip steps. Each step produces a concrete artifact.

### Step 1 — Inventory the project

Scan the project directory structure. Identify and classify every file:

| Category | Typical location | Examples |
|---|---|---|
| Raw data | `raw/` | Downloaded CSVs, WRDS extracts, shapefiles |
| Build scripts | `build/` | Cleaning, merging, variable construction |
| Analysis scripts | `analysis/` | Regressions, portfolio sorts, event studies |
| Output: tables | `output/tables/` | `.tex` files |
| Output: figures | `output/figures/` | `.pdf` or `.png` files |
| Codebook | `codebook/` | Variable definitions, data dictionaries |
| Utilities | `utils/` | Shared helper functions |
| Paper | `paper/` | LaTeX manuscript, `.bib`, `.bst` |
| Intermediate data | `build/` | Cleaned panels, merged datasets |

Flag any files that do not fit these categories. Flag any outputs with no apparent originating script.

### Step 2 — Classify data by shareability

For each data input, assign one of these shareability tiers:

| Tier | Meaning | Package action |
|---|---|---|
| **Public** | Freely downloadable (FRED, Census, BLS, SEC EDGAR) | Include in package or provide download script |
| **Licensed-reproducible** | Requires institutional access but query is reproducible (WRDS/CRSP, WRDS/Compustat) | Include the exact query script + expected schema; do not include the data |
| **Licensed-restricted** | Vendor prohibits redistribution (CoStar, CoreLogic, ATTOM, NCREIF, ICE/Black Knight, Zillow ZTRAX) | Document access path, provide schema-only placeholder, describe sample construction |
| **Confidential** | IRB-restricted, proprietary firm data, NDA-covered | Document variable definitions and summary statistics only |
| **Generated** | Created by project scripts from upstream inputs | Do not include; rerunning the pipeline recreates it |

Produce a **data access matrix** (see `assets/data-access-matrix-template.md`).

### Step 3 — Build the dependency graph

Map the rerun order across all scripts:

1. Which scripts must run first (data downloads, cleaning)?
2. Which scripts depend on outputs of earlier scripts?
3. Which scripts are independent and could run in parallel?
4. Which script produces each table, figure, and appendix exhibit?

Produce a **rerun order memo** — a numbered list of scripts in the exact order needed to reproduce all outputs from raw data.

### Step 4 — Map provenance

For every table, figure, and appendix exhibit in the paper, record:

| Paper output | Script | Key inputs | Key parameters |
|---|---|---|---|
| Table 1: Summary Stats | `analysis/01_summary_stats.py` | `build/final_panel.parquet` | Winsorization: 1%/99% |
| Figure 2: Event Study | `analysis/03_event_study.py` | `build/event_panel.parquet` | Window: [-5, +10] |
| Table IA.1 | `analysis/05_robustness.py` | `build/final_panel.parquet` | Alt. FE specification |

Produce a **provenance matrix** (see `assets/provenance-matrix-template.md`). This is the highest-value artifact — it lets a referee or data editor trace any result back to code.

### Step 5 — Capture the environment

Generate an environment specification:

```python
# Generate requirements
import subprocess
subprocess.run(["pip", "freeze"], stdout=open("requirements.txt", "w"))
```

Also document:
- Python version
- Operating system used for final runs
- Any non-pip dependencies (LaTeX distribution, system libraries, database drivers)
- Random seeds used anywhere in the pipeline
- WRDS connection method (`wrds` package version, PostgreSQL driver)

If the project uses `conda`, generate `environment.yml` instead of `requirements.txt`.

### Step 6 — Scrub and sanitize

Check the entire project for:

- [ ] Hardcoded local paths (e.g., `/Users/username/...`, `C:\Users\...`)
- [ ] Credentials, API keys, tokens, `.env` contents
- [ ] Machine-specific assumptions (drive letters, mount points)
- [ ] Personal information in comments or metadata
- [ ] Data files that should not be shared (check against Step 2 classifications)
- [ ] Notebook cell outputs that leak data or paths
- [ ] Git history containing sensitive files (warn the user; do not force-clean)

Replace hardcoded paths with relative paths or environment variables. Generate a `.env.example` template for any required credentials.

### Step 7 — Generate the replication README

Produce a standalone `README.md` for the replication package using the template in `assets/replication-readme-template.md`. It must include:

1. **Paper title and authors**
2. **Data availability statement** — exactly which data are included, which require institutional access, and how to obtain each
3. **Software requirements** — Python version, key packages, LaTeX distribution
4. **Rerun instructions** — numbered steps from raw data to final paper PDF
5. **Provenance matrix** — mapping from paper outputs to scripts
6. **Expected runtime** — approximate time for full replication
7. **Contact** — who to reach for questions

The README must be self-contained. A reader should be able to replicate without consulting the paper.

### Step 8 — Dry-run validation

Generate a script that verifies the package is self-consistent:

- All scripts referenced in the rerun order exist
- All input files referenced in scripts either exist in the package or are documented as requiring external access
- All outputs referenced in the provenance matrix have a corresponding script
- No hardcoded absolute paths remain in any `.py` file
- `requirements.txt` or `environment.yml` exists
- README exists and covers all sections

Report any gaps as a checklist the user must resolve before submission.

## Journal-specific replication norms

Read `references/journal-targets.md` at the project root for current journal policies. Key requirements by journal:

| Journal | Archive | Data editor review? | Key requirement |
|---|---|---|---|
| **JF** | Not specified | Yes — data-editor reviews package | Code + data; Replications & Corrigenda section exists |
| **JFE** | Mendeley Data or domain repo | Yes | Code + data + documentation; pseudo data for restricted sources |
| **RFS** | Journal-managed | Yes — reproduces in virtual env | Code + data + documentation; synthetic data accepted |
| **JFQA** | Harvard Dataverse | Implied | Code required since Jan 2024; raw data or pseudo data; request exceptions at initial submission |
| **REE** | Verify on Wiley pages | Verify | Check current policy before submission |
| **JREFE** | Verify on Springer pages | Verify | Check current policy before submission |

When the target journal has a specific archive (Mendeley Data, Harvard Dataverse), structure the package to match that platform's expectations.

## Finance and real estate data handling

### WRDS-dependent builds

- Include the exact SQL query or `wrds` library call that pulls each table
- Document the WRDS library, schema, and table name (e.g., `crsp.msf`, `comp.funda`)
- Record the date range and any filters applied at query time
- Note the date the extract was pulled (data vintages matter)
- Provide expected row counts and key variable ranges as a sanity check

### Restricted vendor data

For CoStar, CoreLogic, ATTOM, NCREIF, ICE/Black Knight, Zillow ZTRAX, and similar:

- Document the exact data product, vintage, and geographic coverage
- Provide a schema file showing variable names, types, and descriptions
- Include summary statistics (means, medians, counts) for key variables
- Describe any sample restrictions or filters applied
- State the vendor's redistribution policy
- Provide a contact path for data access requests

### Geographic data

- Note the source and vintage of any shapefiles (Census TIGER, FEMA flood maps, zoning maps)
- Document the coordinate reference system (CRS/EPSG code)
- Note any license restrictions on redistribution

## Guardrails

- Do not claim "fully reproducible" if core data are proprietary. Say "reproducible conditional on data access" and list the access requirements.
- Do not leave manual steps undocumented. If the user manually edited a file, renamed a column, or ran a query in a GUI, document it.
- Do not ship credentials, tokens, `.env` files, or `.pgpass` files.
- Do not include outputs with no script lineage. Every table and figure must trace to a script.
- Do not rely on notebook execution order. If notebooks are used, convert critical steps to `.py` scripts or document the exact cell execution order.
- Do not package confidential data just because it is already in the project directory.
- Do not leave variable definitions, sample filters, or table notes undocumented if they are needed to interpret results.
- Flag if git history may contain sensitive files that were later removed.

## Required deliverables

Every invocation must produce:

1. **Replication README** — standalone, self-contained (Step 7)
2. **Rerun order memo** — numbered script execution sequence (Step 3)
3. **Provenance matrix** — every paper output mapped to its script and inputs (Step 4)
4. **Data access matrix** — every data source classified by shareability tier (Step 2)
5. **Environment specification** — `requirements.txt` or `environment.yml` (Step 5)
6. **Sanitization checklist** — results of the scrub check (Step 6)
7. **Dry-run report** — validation results and unresolved gaps (Step 8)

## Output format

```
# Replication Package Report

## Project inventory
[file tree with classifications]

## Data access matrix
[table: source | tier | package action | access instructions]

## Rerun order
[numbered script list with dependencies]

## Provenance matrix
[table: paper output | script | inputs | key parameters]

## Environment
[Python version, key packages, non-pip dependencies]

## Sanitization results
[checklist with pass/fail for each item]

## Dry-run validation
[checklist with pass/fail, unresolved gaps flagged]

## Replication README
[complete standalone README ready to include in package]
```

Read these references as needed:
- references/journal-targets.md
