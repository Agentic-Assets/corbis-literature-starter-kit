---
name: research-figure-design
description: "Design and generate publication-ready figures for finance and real-estate papers. Use for figure planning, plot selection, visual design, maps, diagrams, and journal-quality Python code for every common figure type."
---

# Research Figure Design

Every figure must earn its place. A figure that restates what a table already shows is a wasted slot. A figure that reveals a pattern no table can convey is worth more than three robustness tables.

## When to use this skill

- Deciding which figures the paper should include
- Python code for a specific figure type
- Converting a table into a visual for a talk or paper
- Maps, diagrams, or conceptual figures
- Improving existing figures for journal submission

## Figure planning workflow

1. Identify the paper's key messages (main result, mechanism, heterogeneity, dynamics).
2. For each message, ask: is a figure or a table the better vehicle?
3. Assign each figure a specific job from the catalog below.
4. Decide placement: main paper vs. appendix vs. presentation only.
5. Generate the code with journal-quality defaults.
6. Write self-contained figure notes.

### When to use a figure instead of a table

| Use a figure when... | Use a table when... |
|---|---|
| The pattern is nonlinear or dynamic | The reader needs exact coefficients |
| Spatial variation matters | Multiple specifications need comparison |
| You want to show a distribution or trend | Precision of individual estimates matters |
| The result is best seen as a comparison | The result is a set of heterogeneous effects |
| A talk audience needs to grasp it in seconds | The referee needs to verify the numbers |

## Standard figure set by paper type

### Corporate finance / causal inference paper
1. **Motivating trend** (time series showing the phenomenon)
2. **Event-study plot** (main result, pre/post with CIs)
3. **Parallel trends** (DiD validity)
4. **Binned scatter** (key relationship, residualized)
5. **Coefficient plot** (heterogeneity across subgroups)
6. **Mechanism bar chart** (channel decomposition)

### Asset pricing paper
1. **Cumulative return plot** (long-short portfolio over time)
2. **Portfolio sort bar chart** (mean returns across quintiles/deciles)
3. **Factor exposure heatmap** (loadings across models)
4. **Time-series alpha plot** (rolling or expanding window)
5. **Turnover/capacity plot** (implementability)

### Real estate paper
1. **Choropleth map** (treatment geography, price variation)
2. **Boundary RD plot** (outcome vs. distance to boundary)
3. **Event-study or spatial DiD plot** (main result)
4. **Binned scatter** (hedonic relationship)
5. **Density map** (transaction locations, treatment intensity)

### Descriptive / measurement paper
1. **Distribution plots** (histograms, KDEs of key variables)
2. **Time-series trends** (evolution of the measure)
3. **Correlation heatmap** (relationship to existing measures)
4. **Cross-sectional scatter** (new measure vs. existing proxies)

## Figure code catalog

For complete Python code for all 13 figure types, read `assets/figure-code-catalog.md`. It includes:
- Global defaults (rcParams, color palette, save function)
- Event-study plot (with CIs, shading, reference period)
- Parallel trends plot
- Binned scatter plot (with residualization, fit line, CIs)
- Coefficient plot (horizontal, with group separators)
- RD plot (with local polynomial fits)
- Time-series trend plot (with recession shading)
- Distribution plots (histogram, KDE, panel layout)
- Choropleth map (with boundary overlay)
- Portfolio return plots (cumulative returns, bar chart)
- Kaplan-Meier survival curves
- Heatmap (correlation, factor exposure)
- Sample flow diagram
- Mechanism / conceptual diagram

Each function includes a figure note template for self-contained documentation.

## Design rules

- **One message per figure.** If you need two messages, make two figures.
- **No chartjunk.** Remove gridlines, unnecessary borders, redundant labels.
- **Consistent style across all figures.** Same fonts, colors, line widths throughout the paper.
- **Colorblind-safe.** The default palette works. Test with a simulator if adding colors.
- **Text must be readable at print size.** Minimum 9pt after scaling to journal column width.
- **Axis labels with units.** Never leave an axis unlabeled.
- **Save as PDF for LaTeX.** PNG at 300 DPI as backup. Never use JPG for plots.
- **Figure size: 6.5 x 4.5 inches** for single journal column. 7 x 4.5 for wider figures.

## Figure notes standard

Every figure must have a self-contained note including:
1. What is plotted (outcome variable, conditioning, residualization)
2. Sample used (time period, filters, N)
3. Estimation details (equation reference, controls, FE)
4. Statistical details (CI level, SE clustering, bandwidth)
5. Data source

## LaTeX float format

Write each figure's LaTeX float wrapper to `output/figures/*.tex`. Do not put float LaTeX in the chat. Before generating any float, read `latex_template/academic_paper_template.tex`.

Structure: caption on top, descriptive note between caption and figure, figure below:
```latex
\begin{figure}[!htbp]
\caption{Descriptive Title}
\label{fig:name}\vspace{-2.5ex}
\floatnotes{This figure plots [what]. [Sample]. [Method]. [CI/SE details].}
\centering
\includegraphics[width=\textwidth]{./output/figures/name.pdf}
\end{figure}
```

## Tool integration (Corbis MCP)

- `fred_series_batch` → pull FRED data for time-series motivation figures
- `get_market_data` / `compare_markets` → CRE data for RE motivation figures
- `search_papers` (query: "figure [type] [topic]", `minYear: 2020`) → find published visual precedents
- `export_citations` (format: `bibtex`) → export references for design benchmarks

## Guardrails

- Do not generate a figure that simply restates a table.
- Do not use 3D charts, pie charts, or stacked bar charts in academic finance papers.
- Do not use rainbow color schemes or more than 4-5 colors in a single figure.
- Do not forget confidence intervals on coefficient, event-study, or RD plots.
- Do not use raw (non-residualized) binned scatters when the paper includes controls.
- Do not leave axis labels as raw variable names from the DataFrame.
- For maps, always include a scale indicator or recognizable geographic context.
