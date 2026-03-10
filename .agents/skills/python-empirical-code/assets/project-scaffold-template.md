# Project Scaffold

## Project: [paper title]
## Date initialized: [date]

## Directory structure

```
[project_name]/
  raw/                       # Source data (read-only after download)
  build/                     # Cleaning and merge scripts + intermediate datasets
    01_[source1].py
    02_[source2].py
    03_merge.py
    04_variables.py
  explore/                   # Throwaway exploration scripts (delete freely)
  analysis/                  # Promoted scripts producing final tables and figures
    01_summary_stats.py
    02_baseline.py
    03_robustness.py
    04_mechanism.py
    05_heterogeneity.py
  output/
    tables/                  # .tex files for LaTeX
    figures/                 # .pdf or .png at 300 DPI
    logs/                    # Console output and diagnostics
  notes/
    lab_notebook.md          # Running log: what worked, what didn't, emerging narrative
  codebook/
    variables.md             # Variable definitions with formulas
    sample_flow.md           # Observation counts at each filter stage
  utils/
    data_utils.py            # winsorize(), merge helpers, date alignment
    table_utils.py           # reg_to_latex(), summary_stats_latex()
    figure_utils.py          # Plot defaults, event_study_plot(), coef_plot()
  paper/                     # LaTeX manuscript (copy of latex_template/)
  run_all.py                 # Master pipeline script
  requirements.txt           # Pinned package versions
  README.md                  # What the project does and how to run it
```

## Workflow

Exploration scripts go in `explore/`. Run many tests quickly to discover what works. When a test produces a result worth keeping, move the script to `analysis/` and log it in `notes/lab_notebook.md`. Once the table/figure set is complete and the lab notebook narrative is coherent, transition to writing the paper in `paper/`.

## Data sources

| Source | Access | Files | Key variables |
|---|---|---|---|
| [e.g., CRSP Monthly] | [WRDS] | [raw/crsp_msf.parquet] | permno, date, ret, prc, shrout |
| [e.g., Compustat Annual] | [WRDS] | [raw/comp_funda.parquet] | gvkey, datadate, at, ceq, sale |
| | | | |

## Merge plan

| Step | Input | Output | Key | Expected match rate |
|---|---|---|---|---|
| 1 | CRSP + CCM | crsp_with_gvkey | permno, linkdt range | ~95% |
| 2 | Step 1 + Compustat | merged_panel | gvkey, jdate | ~85% |
| | | | | |

## Variable construction

| Variable | Formula | Source | Notes |
|---|---|---|---|
| | | | |
| | | | |

## Analysis plan

| Script | Table/Figure | Purpose |
|---|---|---|
| 01_summary_stats.py | Table 1 | Summary statistics |
| 02_baseline.py | Table 2 | Baseline regression |
| | | |

## Requirements

```
pandas>=2.0
numpy>=1.24
matplotlib>=3.7
seaborn>=0.12
statsmodels>=0.14
linearmodels>=5.3
wrds>=3.1
```
