---
description: Draft a journal-targeted introduction for a paper
---

Run the `research-paper-writer` skill to draft a full introduction.

$ARGUMENTS

Read `notes/project_state.md` if it exists to pick up the research question, mechanism, design, closest papers, and key results from prior skill invocations.

Follow the 7-paragraph structure:
1. **Question and stakes** — grounded in a recent industry event or policy change. Cite the source.
2. **Mechanism or friction** — the economic force generating the prediction.
3. **Setting, data, and design** — what makes identification credible.
4. **Main findings with magnitudes** — quantitative results.
5. **Robustness and mechanism in brief**.
6. **Contribution and closest literature** — name 2-3 closest papers (verify via `search_papers`).
7. **Broader implication and roadmap**.

Also produce:
- 3-5 title options
- A journal-targeted abstract (ask which journal if not specified)

Note: The `research-paper-writer` skill can also draft every other paper section (related literature, institutional background, data, empirical design, results, robustness, mechanism, conclusion, internet appendix). Ask for any section directly.
