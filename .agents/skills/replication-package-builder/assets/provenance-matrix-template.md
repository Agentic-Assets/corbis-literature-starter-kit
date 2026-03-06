# Provenance Matrix Template

Map every paper output to its originating script. Every table, figure, and appendix exhibit must appear here.

| Paper output | Script | Key inputs | Key parameters | Notes |
|---|---|---|---|---|
| Table 1: Summary Statistics | `analysis/01_summary_stats.py` | `build/final_panel.parquet` | Winsorization: 1%/99% | |
| Table 2: Baseline Regression | `analysis/02_baseline_reg.py` | `build/final_panel.parquet` | FE: firm + year; cluster: firm | |
| Table 3: Heterogeneity | `analysis/04_heterogeneity.py` | `build/final_panel.parquet` | Subsample splits defined in script | |
| Figure 1: Event Study | `analysis/03_event_study.py` | `build/event_panel.parquet` | Window: [-5, +10] | |
| Figure 2: Binned Scatter | `analysis/05_binscatter.py` | `build/final_panel.parquet` | 20 bins, residualized | |
| Table IA.1: Alt. FE | `analysis/06_robustness.py` | `build/final_panel.parquet` | Industry + year FE | Internet Appendix |
| Figure IA.1: Placebo | `analysis/07_placebo.py` | `build/placebo_panel.parquet` | 500 random assignments | Internet Appendix |

## Validation checklist

- [ ] Every table in the paper appears in this matrix
- [ ] Every figure in the paper appears in this matrix
- [ ] Every Internet Appendix exhibit appears in this matrix
- [ ] Every script listed here exists in the project
- [ ] Every input file listed here is either in the package or documented in the data access matrix
