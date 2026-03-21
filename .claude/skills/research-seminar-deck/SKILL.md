---
name: research-seminar-deck
description: "Design finance and real-estate research presentations. Use for seminar decks, conference talks, job talks, slide logic, speaker notes, and backup-slide planning."
---

# Research Seminar Deck

Build a talk that foregrounds the question, design, and economic meaning before details overwhelm the audience.

## Workflow

1. Identify the audience and format:
   - Brown bag / workshop (30-45 min, informal, expect interruptions)
   - Conference presentation (15-20 min, formal, limited Q&A)
   - Invited seminar (60-75 min, deep engagement, extensive Q&A)
   - Job talk (75-90 min, high stakes, hostile-constructive Q&A)
   - Dissertation defense (varies by institution)
2. Write the one-sentence contribution.
3. Decide what the audience must believe before seeing results.
4. Build the main-deck sequence.
5. Move technical depth and robustness density to the appendix.
6. Add likely-question backup slides.

## Time budgets by format

| Format | Total slides | Main deck | Backup | Time per slide |
|---|---|---|---|---|
| Conference (15 min) | 12-15 | 10-12 | 5-8 | ~1 min |
| Conference (20 min) | 15-20 | 13-16 | 8-10 | ~1.2 min |
| Workshop (45 min) | 25-30 | 20-25 | 10-15 | ~1.5-2 min |
| Seminar (75 min) | 35-45 | 28-35 | 15-20 | ~2 min |
| Job talk (90 min) | 40-50 | 30-40 | 20-30 | ~2 min |

## Main-deck logic

Default sequence:
1. **Title and contribution** — one sentence that tells the audience exactly what they will learn
2. **Motivation** — why should the audience care? Real-world context, not literature gap
3. **Research question** — precise, testable
4. **Institutional setting or mechanism** — the economics that generates the prediction
5. **Preview of results** — optional for seminars, essential for conferences
6. **Identification challenge** — what makes this hard to answer?
7. **Research design** — the solution to the identification challenge
8. **Data and sample** — one or two slides maximum
9. **Main result** — the key table or figure, simplified for projection
10. **Economic magnitude** — translate into real units the audience can feel
11. **Mechanism evidence** — why the effect operates through the proposed channel
12. **Key robustness** — two or three checks, not a laundry list
13. **Conclusion** — restate the contribution, the economic lesson, and one forward-looking implication

## Slide-writing rules

- **One message per slide.** If you need two messages, make two slides.
- **Sparse text.** Maximum 4-5 bullet points, each under 10 words.
- **Figures beat tables.** Convert regression results into coefficient plots or event-study graphs.
- **Simplified tables.** Show only the coefficient of interest, key controls listed (not shown), and the specification description.
- **Show magnitudes in real units.** "2.3 percentage points" beats "beta = 0.023 (t = 4.2)."
- **Explain the design before showing estimates.**
- **Use consistent formatting.** Same font sizes, color scheme, and layout throughout.

## Audience-specific adjustments

**Finance seminar**: Will attack identification immediately. Front-load design credibility. Backup slides for alternative specifications, clustering, pretrends.

**Real estate audience**: Values institutional detail. Spend more time on setting, data, and maps. Backup slides with data construction details.

**Job talk**: Testing breadth and depth. Compelling "big picture" motivation, clean design, ability to handle adversarial questions. Prepare 20+ backup slides.

**Conference**: Time is scarce. Motivation, design, result, magnitude, done. Backup slides handle depth.

## Visual design principles

- **Coefficient plots** over regression tables for the main deck
- **Event-study plots** with confidence intervals, clearly labeled pre/post periods
- **Maps** when geography matters
- **Timeline diagrams** for event timing or staggered designs
- **Flow charts** for complex identification strategies
- **Bar charts** for magnitude comparisons across subgroups

## Backup slide planning

Organize by anticipated question type:
1. **Identification**: Alternative specifications, different FE, pretrends, placebo tests
2. **Measurement**: Alternative variable definitions, different data sources
3. **Sample**: Subsamples, outlier sensitivity, different time periods
4. **Mechanism**: Additional channel tests, competing explanations
5. **Data construction**: Merge details, match rates, sample flow
6. **Literature**: How does this compare to [specific paper]?

## Speaker notes guidance

For each slide, prepare:
- The key message in one sentence
- The transition from the previous slide
- One or two anticipated questions and how to handle them
- The time target for this slide

## Beamer slide generation

When the user requests actual slides (not just an outline), generate a complete Beamer LaTeX document. Use the Beamer template at `latex_template/beamer_template.tex` as the starting point.

### Beamer code conventions

- **Theme**: Use `metropolis` (clean, modern, widely available). Fall back to `Madrid` if metropolis is unavailable.
- **Colors**: Navy primary (`{RGB}{0,40,85}`), gray accent (`{RGB}{128,128,128}`). Do not use bright or saturated colors.
- **Fonts**: Serif math, sans-serif text (metropolis default). Do not override font choices.
- **Frame titles**: Sentence case, not title case. Maximum 6 words.
- **Content per frame**: Maximum 4-5 bullet points. Each under 10 words. One message per frame.
- **Figures**: Use `\includegraphics[width=\textwidth]{path}`. Reference files in `output/figures/`.
- **Tables**: Simplified for projection. Maximum 3-4 columns visible. Use `\footnotesize` or `\scriptsize` for table text. Show only the coefficient of interest.
- **Equations**: One equation per frame maximum. Use `\begin{equation*}` (unnumbered) unless cross-referencing is needed.
- **Notes**: Use `\note{}` for speaker notes on each frame.

### Frame templates

#### Title frame
```latex
\begin{frame}[plain]
\titlepage
\end{frame}

\begin{frame}{Contribution}
\begin{center}
\large
[One-sentence contribution statement]
\end{center}
\note{State this clearly in the first 30 seconds. The audience should know exactly what they will learn.}
\end{frame}
```

#### Motivation frame
```latex
\begin{frame}{[Motivating context]}
\begin{itemize}
    \item [Recent event, statistic, or trend]
    \item [Why this matters economically]
    \item [The gap or tension this creates]
\end{itemize}
\vfill
\textcolor{gray}{\scriptsize Source: [citation]}
\note{Connect to something the audience already knows or cares about.}
\end{frame}
```

#### Research question frame
```latex
\begin{frame}{Research question}
\begin{center}
\large
\textbf{[Precise, testable question]}
\end{center}
\vspace{1cm}
\begin{itemize}
    \item Prediction 1: [if mechanism A]
    \item Prediction 2: [if mechanism B]
\end{itemize}
\note{Make sure the audience can hold this question in their head for the rest of the talk.}
\end{frame}
```

#### Design/specification frame
```latex
\begin{frame}{Empirical design}
\begin{equation*}
    \textit{Outcome}_{i,t} = \beta \, \textit{Treatment}_{i,t} + \gamma' X_{i,t} + \alpha_i + \delta_t + \varepsilon_{i,t}
\end{equation*}
\vspace{0.5cm}
\begin{itemize}
    \item $\textit{Treatment}_{i,t}$: [definition]
    \item Fixed effects: [what they control for]
    \item Clustering: [level and rationale]
    \item Identifying variation: [source]
\end{itemize}
\note{This is where skeptics decide whether to trust you.}
\end{frame}
```

#### Results frame (coefficient plot preferred)
```latex
\begin{frame}{Main result: [economic finding]}
\begin{center}
    \includegraphics[width=0.85\textwidth]{output/figures/fig_coef_plot.pdf}
\end{center}
\vspace{-0.5cm}
{\scriptsize Controls: [list]. Fixed effects: [list]. Clustered SEs at [level].}
\note{Show the result, then explain. Do not read the table aloud.}
\end{frame}
```

#### Results frame (simplified table)
```latex
\begin{frame}{Main result: [economic finding]}
\begin{center}
\footnotesize
\begin{tabular}{lcc}
\toprule
 & (1) & (2) \\
 & Baseline & Full controls \\
\midrule
Treatment & $\beta_1$\sym{***} & $\beta_2$\sym{***} \\
 & ($t_1$) & ($t_2$) \\
\midrule
Controls & No & Yes \\
Fixed effects & Firm, Year & Firm, Year \\
Observations & $N_1$ & $N_2$ \\
Adj. $R^2$ & $R_1$ & $R_2$ \\
\bottomrule
\end{tabular}
\end{center}
\note{Highlight the coefficient, the t-stat, and the magnitude in real units.}
\end{frame}
```

#### Magnitude frame
```latex
\begin{frame}{Economic magnitude}
\begin{center}
\large
A one-SD increase in \textit{Treatment} \\[0.5cm]
$\Rightarrow$ \textbf{[Y]\% change} in \textit{Outcome} \\[0.5cm]
$\approx$ \textbf{\$[amount] per [unit]} \\[0.5cm]
{\normalsize (equivalent to [familiar benchmark])}
\end{center}
\note{Translate into units the audience can feel.}
\end{frame}
```

#### Conclusion frame
```latex
\begin{frame}{Takeaway}
\begin{enumerate}
    \item \textbf{Finding}: [main result with magnitude]
    \item \textbf{Mechanism}: [channel with evidence]
    \item \textbf{Implication}: [economic lesson or policy relevance]
\end{enumerate}
\vfill
\begin{center}
{\large [Author email or website]}
\end{center}
\note{Do not end with ``thank you.'' End with the idea.}
\end{frame}
```

#### Backup frame
```latex
\appendix
\begin{frame}[noframenumbering]{Backup: [topic]}
[Content addressing the anticipated question]
\note{Only show if asked.}
\end{frame}
```

### Beamer output rules

- Write the complete `.tex` file to `paper/slides_[format].tex` (e.g., `slides_conference.tex`, `slides_seminar.tex`).
- Include `\usepackage{booktabs}` for tables and `\usepackage{graphicx}` for figures.
- Include `\pgfpagesuselayout{2 on 1}[a4paper]` as a commented-out option for handouts.
- Set `\setbeameroption{show notes on second screen=right}` as a commented-out option for dual-screen presenting.
- If figures referenced in the slides do not exist yet, add a comment `% TODO: generate this figure` next to the includegraphics command.
- The Beamer file should compile without errors even if figures are missing (use `\IfFileExists` wrapper or draft mode).

## Deliverables

Produce:
- a slide-by-slide outline using assets/seminar-deck-outline.md
- suggested visuals (specify figure type and what it should show)
- presenter notes for each slide
- appendix backup-slide plan organized by question type
- anticipated Q&A with suggested responses
- **Beamer LaTeX file** written to `paper/slides_[format].tex` (when the user requests actual slides, not just a blueprint)

When the user asks for "slides," "a deck," or "a presentation," generate the Beamer file by default. When the user asks for an "outline," "blueprint," or "plan," produce the outline only.

## Output format

```
# Seminar deck blueprint
## Audience and format
## Core message (one sentence)
## Slide-by-slide outline (with time targets)
## Figures and tables to create or simplify
## Backup slides (organized by question type)
## Top 10 questions to anticipate (with responses)
## Speaker notes for key slides
```

## Tool integration (Corbis MCP)

- `search_papers` (query: the paper's topic, `matchCount: 5`, `minYear: 2020`) → find recent related work to anticipate "how does this compare to [paper]?" questions and prepare backup slides.
- `top_cited_articles` (journals: target journals) → identify seminal papers the audience is likely to reference, to prepare backup slides and anticipate comparison questions.
- `get_paper_details` (paper IDs) → read abstracts of papers likely to come up in Q&A.
- `get_market_data` / `compare_markets` → for RE presentations, pull current market data for motivation slides or audience-relevant context.
- `fred_series_batch` (relevant series) → pull aggregate trends for motivation slides (e.g., housing starts, mortgage rates, credit spreads).
- `export_citations` (format: `bibtex`) → export BibTeX entries for papers cited in the presentation, including literature-positioning slides and backup slides. Offer this after the deck blueprint is produced.
- `format_citation` → format individual references for slide footnotes or the bibliography slide.

## Reference files
Read if needed:
- references/presentation-norms.md
- references/writing-norms.md

## Guardrails

- Do not transplant the manuscript structure directly onto slides.
- Do not let the deck become a literature review.
- Do not use unreadable tables in the main talk.
- Anticipate the identification question before the audience asks it.
- Do not end with "thank you" as the last slide — end with the contribution and implication.
- For job talks, do not rush the motivation.
- Do not put full regression tables on slides — simplify or use coefficient plots.

## Example prompts
- "Turn my asset-pricing paper into a 15-minute conference deck."
- "Build a job-talk outline for this corporate-finance paper."
- "Create a seminar deck plan for a zoning and housing-supply paper."
- "What backup slides do I need for a hostile identification question?"
- "Convert these regression tables into presentation-ready visuals."
