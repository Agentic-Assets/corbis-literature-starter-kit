# Seminar and Conference Presentation Norms

## Slide design
- One message per slide. If you need two messages, make two slides.
- Use coefficient plots, event-study graphs, and simplified tables — not dense manuscript tables.
- Keep text sparse and verbs active. Maximum 4-5 bullet points per slide, each under 10 words.
- Put the contribution sentence on the title slide or slide 2.
- Move robustness depth to the appendix. Show 2-3 key checks in the main deck.
- Use consistent formatting: same font sizes, colors, and layout throughout.

## Talk logic
1. Question and motivation (why should the audience care?)
2. Institutional setting or mechanism (the economics)
3. Identification challenge (what makes this hard?)
4. Design and data (the solution)
5. Main result (with economic magnitude, not just t-statistics)
6. Mechanism or cross-sectional evidence
7. Robustness and limits (brief)
8. Economic implication (the forward-looking takeaway)

## Finance and real estate audiences
- Anticipate questions about identification before showing coefficient estimates.
- Make clustering, fixed effects, and comparison groups easy to see on design slides.
- Show magnitudes in real units, not only t-statistics or standardized coefficients.
- Use one backup slide per likely objection.
- Finance audiences will ask about endogeneity within the first 10 minutes.
- Real estate audiences will ask about institutional detail, spatial issues, and data construction.

## Visual best practices
- Coefficient plots with confidence intervals over regression tables
- Event-study plots with clear pre/post labeling and a vertical line at treatment
- Maps when geography is part of the story
- Timeline diagrams for staggered treatments or policy rollouts
- Simplified 2-3 column tables if you must show a table (highlight the key coefficient)
- Use color purposefully: highlight the key series or coefficient, mute everything else

## Time management
- Conference (15 min): 10-12 main slides, ~1 min each. No time for tangents.
- Seminar (75 min): 28-35 main slides, ~2 min each. Allow for interruptions.
- Job talk (90 min): 30-40 main slides. Budget 30+ min for Q&A and interruptions.
- Practice the talk at least twice. Time yourself.

## Common mistakes
- Too much literature in the main deck (move to backup or cut entirely)
- Showing unreadable regression tables (use coefficient plots instead)
- Spending too long on data cleaning minutiae before the actual question
- Ending without an economic takeaway (do not end with "thank you" — end with the idea)
- Not having backup slides for obvious objections
- Reading slides verbatim instead of talking to the audience
- Rushing the motivation to get to results faster (the audience needs motivation to care about results)

---

## The Three Laws of Presentation Design

### Law 1: Beauty Is Function
- Every element earns its presence.
- Nothing distracts from the point.
- The eye knows where to go.
- The most beautiful slide may be three words on a blank background.

### Law 2: Cognitive Load Is the Enemy
- One idea per slide. ONE. Not a guideline, the law.
- Too many points = zero points retained.
- Dense text = nothing read.
- Complex charts = confusion, not insight.

### Law 3: The Slide Serves the Spoken Word
- The slide is the visual anchor, not the content itself.
- If slides can be understood without you speaking, you wrote a document.
- If you must read slides aloud, you failed twice.

---

## Assertion-based slide titles

Slide titles should state the finding, not label the category. If someone reads only slide titles in sequence, they should understand your argument.

| Weak (label) | Strong (assertion) |
|------|--------|
| "Results" | "Transaction costs eliminate half of momentum alpha" |
| "Literature Review" | "Prior work assumes costless, instantaneous execution" |
| "Data" | "CRSP covers 26,000 stocks over 60 years" |
| "Methodology" | "Double sorts on size and book-to-market isolate the value premium" |
| "Robustness" | "Results survive alternative breakpoints, weighting, and sample periods" |

---

## The MB/MC framework

Optimal rhetoric equalizes marginal benefit to marginal cognitive cost across all slides:

MB_1/MC_1 = MB_2/MC_2 = ... = MB_n/MC_n

- **Overloaded slides** (MB/MC too low): Text in footer, competing ideas, audience gives up.
- **Underloaded slides** (MB/MC too high): Wasted attention, captured but unused.

Walk through the deck asking: "If I added one more element, would the benefit justify the cognitive cost?"

---

## The Aristotelian Balance for Finance Seminars

| Mode | Weight | How It Appears |
|------|--------|----------------|
| **Logos** (logic) | 45% | Data, econometrics, formal results, tables |
| **Pathos** (stakes) | 35% | Why the question matters, impact on investors, real-world costs |
| **Ethos** (credibility) | 20% | Reproducibility, acknowledging limitations, data quality |

---

## Beamer preamble and custom commands

### Professional academic palette

```latex
% Muted, authoritative house palette
\definecolor{navy}{HTML}{1A365D}        % Primary text, headers
\definecolor{darkgray}{HTML}{2D3748}    % Secondary text
\definecolor{crimson}{HTML}{9B2335}     % Emphasis, key results
\definecolor{forest}{HTML}{276749}      % Positive/adjusted values
\definecolor{steel}{HTML}{4A5568}       % Tertiary, captions
\definecolor{warmgray}{HTML}{E2D8CC}    % Background tint (sparingly)
\definecolor{lightgray}{HTML}{F7FAFC}   % Slide background
```

### Beamer setup

```latex
\documentclass[aspectratio=169,11pt]{beamer}
\usetheme{default}
\usecolortheme{default}

% Strip navigation chrome
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{footline}[frame number]

% Professional frame styling
\setbeamercolor{frametitle}{fg=navy,bg=white}
\setbeamercolor{title}{fg=navy}
\setbeamercolor{normal text}{fg=darkgray}
\setbeamercolor{itemize item}{fg=steel}
\setbeamercolor{alerted text}{fg=crimson}

% Clean typography
\setbeamerfont{frametitle}{series=\bfseries,size=\large}
\setbeamerfont{title}{series=\bfseries,size=\Large}
```

### Custom commands

```latex
% Highlight a number (crimson, bold)
\newcommand{\emphnum}[1]{{\color{crimson}\textbf{#1}}}

% Positive result (forest green)
\newcommand{\goodnum}[1]{{\color{forest}\textbf{#1}}}

% Full-slide transition
\newcommand{\transitionslide}[1]{
  \begin{frame}[plain]
  \vfill\centering
  {\Large\color{navy}\textbf{#1}}
  \vfill
  \end{frame}
}

% Takeaway box
\newcommand{\takeaway}[1]{
  \begin{center}
  \colorbox{lightgray}{\parbox{0.85\textwidth}{
    \centering\color{navy}\textbf{#1}
  }}
  \end{center}
}

% Full-page figure
\newcommand{\fullpage}[2]{
  \begin{frame}[plain]
  \begin{tikzpicture}[remember picture,overlay]
    \node[at=(current page.center)]{\includegraphics[width=\paperwidth,height=\paperheight,keepaspectratio]{#1}};
  \end{tikzpicture}
  \begin{tikzpicture}[remember picture,overlay]
    \node[anchor=south,fill=white,opacity=0.8,text opacity=1] at (current page.south) {\footnotesize #2};
  \end{tikzpicture}
  \end{frame}
}
```

### Backup slide conventions

Use `\backupbegin` and `\backupend` to exclude backup slides from the frame count:

```latex
\newcommand{\backupbegin}{
  \newcounter{framenumberappendix}
  \setcounter{framenumberappendix}{\value{framenumber}}
}
\newcommand{\backupend}{
  \addtocounter{framenumberappendix}{-\value{framenumber}}
  \addtocounter{framenumber}{\value{framenumberappendix}}
}
```

Usage:
```latex
\backupbegin

\begin{frame}{Alternative Specification}
% Backup content here
\end{frame}

\backupend
```

Rules for backup slides:
- One backup slide per likely objection.
- Title each backup slide with the question it answers.
- Include full regression tables, extended robustness, data details, and alternative specifications.
- Finance audiences will ask about endogeneity within the first 10 minutes; have the backup ready.

---

## The Devil's Advocate Slide

Before your conclusion, present the strongest objection:

**Title**: "The strongest objection: [state it clearly]"

Content:
- The critique, stated fairly and forcefully.
- Your response, with evidence.
- What residual uncertainty remains (honesty builds ethos).

---

## Working vs. external decks

| Dimension | External (seminar/conference) | Working (coauthors) |
|-----------|-------------------------------|---------------------|
| Density | Sparse, one idea per slide | Can be more detailed |
| Titles | Assertions only | Can include descriptive titles |
| Tables | Key rows only | Can show full tables |
| Tone | Performative, polished | Documentary, preserves uncertainty |
| Content | 30 slides / 45 min | No limit |
