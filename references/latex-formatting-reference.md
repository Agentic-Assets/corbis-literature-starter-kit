# LaTeX Formatting Reference

This document codifies every formatting convention from `latex_template/academic_paper_template.tex`. **Read this before writing any LaTeX output.** All tables, figures, equations, and paper prose must follow these conventions exactly.

## Required packages and preamble

The template uses these packages. Do not add packages that conflict with or duplicate them.

```latex
\documentclass[hidelinks,12pt]{article}

\usepackage{graphicx}
\usepackage{setspace}
\usepackage[svgnames]{xcolor}
\usepackage[colorlinks=true,citecolor=DarkBlue,linkcolor=Maroon]{hyperref}
\usepackage{fancyhdr}
\usepackage{natbib}
\usepackage[format=hang,font=large,labelfont=bf]{caption}
\usepackage{tabularx}
\usepackage{booktabs,multicol,multirow}
\usepackage[margin=2cm]{geometry}
\usepackage{array}
\usepackage{amsmath}
\usepackage{enumitem}
\usepackage[toc,page]{appendix}
```

## Custom commands (always available in the template)

### `\floatnotes{text}`

Renders descriptive notes in `\scriptsize` inside a `quotation` environment. Used for table and figure notes. Always placed **above** the body (between caption and content), never below.

```latex
\newcommand{\floatnotes}[1]{%
\begin{quotation}
\noindent \scriptsize #1
\end{quotation}
}
```

### `\sym{symbol}`

Produces superscript significance markers that work in both text and math mode.

```latex
\def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\fi}
```

Usage: `0.042\sym{***}` renders as 0.042***

### Custom column types

```latex
\newcolumntype{Y}{>{\raggedleft\arraybackslash}X}     % Right-aligned tabularx column (for numbers)
\newcolumntype{L}[1]{>{\raggedright\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}  % Left-aligned fixed-width column
```

### Caption setup

Period after caption label (e.g., "Table 1." not "Table 1:"):

```latex
\captionsetup[table]{labelsep=period}
\captionsetup[figure]{labelsep=period}
```

## Float structure (non-negotiable ordering)

Every table and figure must follow this exact sequence:

```
1. \clearpage
2. \begin{table}[!htbp]  or  \begin{figure}[!htbp]
3. \centering             (for tables; for figures, place before \includegraphics)
4. \caption{Title}
5. \label{tab:name}\vspace{-2.5ex}   or   \label{fig:name}\vspace{-2.5ex}
6. \floatnotes{Self-contained descriptive note.}
7. [table or figure body]
8. \end{table}  or  \end{figure}
```

Key rules:
- `\caption` always comes first inside the float
- `\label` immediately after `\caption`, on the same line or the next, followed by `\vspace{-2.5ex}`
- `\floatnotes` always between caption/label and the body (above the content, not below)
- Float notes must be **self-contained**: a reader who sees only the float should understand it without the body text
- Use `[!htbp]` placement for all floats
- Use `\clearpage` before each float to force a new page

---

## Table templates

### Summary statistics table

```latex
\clearpage
\begin{table}[!htbp]
\centering
\caption{Summary Statistics}
\label{tab:summary}\vspace{-2.5ex}
\floatnotes{This table reports summary statistics for the main variables. The sample consists of [N] [unit]-[period] observations from [start] to [end]. [Define any non-obvious variables or transformations.]}
\setlength{\tabcolsep}{5pt}
\small

\textbf{Panel A. Descriptive Statistics}
\begin{tabularx}{\textwidth}{@{}Xrrrrrr@{}}
\\
\toprule
\textbf{Variable} & \textbf{Mean} & \textbf{SD} & \textbf{P25} & \textbf{Median} & \textbf{P75} & \textbf{N} \\
\midrule
Variable One (\%) & 5.87 & 1.12 & 5.08 & 5.83 & 6.61 & 2,400 \\
Variable Two & 61.40 & 14.20 & 51.00 & 62.00 & 72.00 & 2,400 \\
\bottomrule
\\
\end{tabularx}

\end{table}
```

Conventions:
- `\setlength{\tabcolsep}{5pt}` for compact column spacing
- `\small` for table body font size
- `@{}` removes outer padding on both sides
- Use `tabularx` with `X` (left-aligned text) and `r` (right-aligned numbers) columns
- Use `Y` column type (right-aligned tabularx) when the table needs to fill `\textwidth` with numeric columns
- `\toprule`, `\midrule`, `\bottomrule` from `booktabs` (no vertical rules, no `\hline`)
- Bold column headers with `\textbf{}`
- Multi-panel tables: `\textbf{Panel A. Title}` before each panel's tabular, separated by `\medskip`
- Second panel can use `\footnotesize` if needed for space

### Regression table

```latex
\clearpage
\begin{table}[!htbp]
\centering
\caption{Main Results: [Outcome] and [Treatment]}
\label{tab:baseline}\vspace{-2.5ex}
\floatnotes{This table reports OLS estimates of [equation reference]. The dependent variable is [name] measured in [units]. [Key variable] is [definition]. Controls include [list]. Standard errors are clustered by [level]. t-statistics in parentheses.}
\small
\begin{tabular}{lcccc}
\toprule
 & \multicolumn{4}{c}{Dependent Variable: [Name] ([units])} \\
\cmidrule(lr){2-5}
 & (1) & (2) & (3) & (4) \\
\midrule
Treatment Variable & -0.018\sym{***} & -0.015\sym{***} & -0.013\sym{***} & -0.011\sym{***} \\
 & (-5.41) & (-4.98) & (-4.36) & (-3.92) \\
[0.5ex]
Control One &  & -0.072\sym{***} & -0.065\sym{***} & -0.049\sym{**} \\
 &  & (-3.11) & (-2.88) & (-2.14) \\
[0.5ex]
Control Two &  & 0.684\sym{***} & 0.611\sym{***} & 0.573\sym{***} \\
 &  & (4.29) & (3.98) & (3.75) \\
\midrule
Firm Fixed Effects & No & No & Yes & Yes \\
Year Fixed Effects & No & Yes & Yes & Yes \\
Observations & 2,400 & 2,400 & 2,400 & 2,400 \\
Adjusted \(R^2\) & 0.096 & 0.184 & 0.361 & 0.409 \\
\bottomrule
\multicolumn{5}{l}{\footnotesize \sym{*} $p<0.10$, \sym{**} $p<0.05$, \sym{***} $p<0.01$.}
\end{tabular}
\end{table}
```

Conventions:
- **t-statistics in parentheses** directly below coefficients (not standard errors, not p-values)
- `[0.5ex]` vertical spacing between variable blocks
- `\cmidrule(lr){2-5}` under spanning column headers (with left/right padding)
- `\multicolumn{N}{c}{Header}` for spanning headers
- Fixed effects and controls rows: Yes/No categorical, no t-stats
- Observations row with comma-separated thousands
- Significance footnote as the last line before `\end{tabular}`: `\multicolumn{N}{l}{\footnotesize \sym{*} $p<0.10$, ...}`
- Use `tabular` (not `tabularx`) for regression tables with centered numeric columns (`c`)
- Use `l` for the first (variable name) column

### Heterogeneity / interaction table

Same structure as regression table, with interaction terms and their constitutive parts. See the template's `tab:heterogeneity` for the exact pattern.

### Variable definitions table (appendix)

```latex
\begin{tabularx}{\textwidth}{@{}L{3.0cm}X@{}}
\toprule
\textbf{Variable} & \textbf{Definition} \\
\midrule
Variable Name & Precise definition with source, transformation, and units. \\
\bottomrule
\end{tabularx}
```

Uses the `L{width}` custom column type for the variable name column.

---

## Figure templates

### Single figure

```latex
\clearpage
\begin{figure}[!htbp]
\caption{Descriptive Title}
\label{fig:name}\vspace{-2.5ex}
\floatnotes{This figure plots [what]. The sample includes [N observations / period]. [Method: residualized, smoothed, binned, etc.]. [CI/SE details if applicable]. Data source: [source].}
\centering
\includegraphics[width=15.24cm,height=10.16cm]{./images/figname.pdf}
\end{figure}
```

Conventions:
- Full-width figures: `width=15.24cm,height=10.16cm`
- Narrower figures: `width=12.8cm,height=8.5cm`
- Save as PDF for LaTeX compilation, PNG at 300 DPI as backup
- Images stored in `./images/` subdirectory (relative to `.tex` file) or `./output/figures/` (relative to project root)

### Multi-panel figure

```latex
\clearpage
\begin{figure}[!htbp]
\caption{Title Covering Both Panels}
\label{fig:panels}\vspace{-2.5ex}
\floatnotes{This figure plots [what] in two panels. Panel A shows [X]. Panel B shows [Y]. [Sample, method, source details.]}
\centering
\textbf{Panel A. First Panel Title}\\
\includegraphics[width=10.16cm,height=6.77cm]{./images/fig_a.pdf}\\
\textbf{Panel B. Second Panel Title}\\
\includegraphics[width=10.16cm,height=6.77cm]{./images/fig_b.pdf}
\end{figure}
```

Conventions:
- Panel labels in bold above each subgraph: `\textbf{Panel A. Title}\\`
- `\\` separates panels vertically
- No individual captions on panels (single caption covers all)
- Panel dimensions smaller than full-width: `10.16cm x 6.77cm`

---

## Equation formatting

```latex
\begin{equation}
\label{eq:baseline}
\begin{aligned}
\textit{OutcomeVariable}_{i,t}
&= \alpha + \beta\,\textit{TreatmentVariable}_{i,t-1} + \Gamma'X_{i,t-1} \\
&\quad + \mu_i + \lambda_t + \varepsilon_{i,t},
\end{aligned}
\end{equation}
```

Conventions:
- Variable names in `\textit{}` (italic), not raw math-mode identifiers
- Greek letters for parameters: `\alpha`, `\beta`, `\Gamma`, `\mu`, `\lambda`, `\varepsilon`
- Subscripts for unit and time: `_{i,t}` or `_{i,t-1}`
- Use `aligned` environment inside `equation` for multi-line alignment
- Thin space `\,` between coefficient and variable
- Comma after the last term, period at end of equation block
- Define each term immediately after the equation in prose

## Hypothesis formatting

```latex
\noindent \textbf{Hypothesis 1.} Plain-language testable prediction.
```

- Bold label, no indent, plain-language statement (not formal notation)

---

## Cross-references

```latex
Table~\ref{tab:summary}          % non-breaking space before \ref
Figure~\ref{fig:binned_scatter}
Equation~\eqref{eq:baseline}     % \eqref for equations (adds parentheses)
Section~\ref{sec:results}
```

Always use `~` (non-breaking space) before `\ref` and `\eqref`.

## Citation commands

Uses `natbib` with `jf.bst`:

```latex
\citet{author2020title}   % "Author (2020)"  — noun form, use as subject
\citep{author2020title}   % "(Author 2020)"  — parenthetical form
```

Bibliography:
```latex
\bibliographystyle{jf}
\bibliography{references}
```

---

## Document-level formatting

| Element | Setting |
|---|---|
| Base font | 12pt |
| Line spacing | `\renewcommand{\baselinestretch}{1.9}` (double-spaced) |
| Abstract spacing | `\setstretch{1.15}` (tighter) |
| Table body | `\small` |
| Float notes | `\scriptsize` (via `\floatnotes`) |
| Column spacing | `\setlength{\tabcolsep}{5pt}` |
| Margins | 2cm (geometry package) |
| Header | Bold running title (left), page number (right), 0.4pt rule |
| Title page | `\thispagestyle{empty}` (no header/page number) |
| Body pages start | `\setcounter{page}{1}` after title page |

## Blind review toggle

```latex
\newif\ifblind
\blindfalse  % \blindtrue for anonymized submission
```

Controls display of author names, affiliations, and emails on the title page.

---

## File output conventions

| Content | Write to | Format |
|---|---|---|
| Individual tables | `output/tables/tab_[name].tex` | One `.tex` file per table float |
| Individual figures | `output/figures/fig_[name].tex` | One `.tex` file per figure float wrapper |
| Figure images | `output/figures/[name].pdf` or `.png` | 300 DPI minimum, PDF preferred |
| Paper prose | `paper/[paper_name].tex` | Edit directly via the Edit tool |

Include standalone table/figure files in the paper with `\input{output/tables/tab_summary}`.

**Never put LaTeX content in the chat for the user to copy-paste.** Always write to files.

---

## Quick checklist

Before writing any LaTeX float, verify:

- [ ] `\clearpage` before the float
- [ ] `\begin{table}[!htbp]` or `\begin{figure}[!htbp]`
- [ ] `\centering` (for tables, place after `\begin{table}`; for figures, place before `\includegraphics`)
- [ ] `\caption{Descriptive title}`
- [ ] `\label{tab: or fig:}\vspace{-2.5ex}`
- [ ] `\floatnotes{Self-contained note with sample, method, clustering, significance convention}`
- [ ] Body uses `\small`, `\setlength{\tabcolsep}{5pt}`, `booktabs` rules
- [ ] t-statistics in parentheses (not SEs, not p-values)
- [ ] Significance footnote: `\multicolumn{N}{l}{\footnotesize \sym{*} $p<0.10$, ...}`
- [ ] `\end{table}` or `\end{figure}`
- [ ] Written to file, not displayed in chat
