---
description: Mechanical proofread for typos, spacing, and formatting
---

Run the `proofread` skill on this paper.

**Target**: $ARGUMENTS (if empty, proofread the main .tex file)

Steps:
1. Extract the target text (section, file, or full main.tex).
2. Scan for typos, doubled words, and common academic misspellings.
3. Check LaTeX formatting per `references/latex-formatting-reference.md` (equation references, non-breaking spaces, unclosed environments).
4. Check spacing issues, equation punctuation, and capitalization consistency.
5. Check for banned words per `references/banned-words.md`.
6. Output a proofread report with line numbers and suggested fixes.
