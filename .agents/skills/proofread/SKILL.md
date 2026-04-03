---
name: proofread
description: Mechanical error scan -- typos, LaTeX formatting, punctuation, spacing
---

# Proofread Skill

Scan for mechanical errors: typos, LaTeX formatting issues, punctuation around equations, and spacing problems.

## Examples
- `/proofread` -- proofread the main .tex file
- `/proofread introduction` -- proofread only the introduction section
- `/proofread path/to/file.tex` -- proofread a specific file

## Input

The user provides an optional section key, file path, or line range. If omitted, scan the project's main `.tex` file.

## Workflow

### Step 1: Extract Target Text
- If a section key is given, extract that section using `%% BEGIN/END` markers
- If a file path is given, read that file
- If no argument, read the main `.tex` file
- Note line numbers for all findings

### Step 2: Spelling & Typo Scan
Search for common typos in prose and math-adjacent text:
- Misspelled words (e.g., "componet", "assigment", "misraking")
- Doubled words ("the the", "is is")
- Common academic misspellings ("accomodate", "occurence", "seperate", "consistant")
- Wrong word usage ("it's" for possessive, "affect/effect" confusion)

### Step 3: LaTeX Formatting
Check for formatting issues per `references/latex-formatting-reference.md`:
- `\ref{eq:...}` where `\eqref{eq:...}` should be used (equation references)
- Missing non-breaking space: `Eq.\eqref` should be `Eq.~\eqref`
- Same for: `Table\ref` -> `Table~\ref`, `Figure\ref` -> `Figure~\ref`, `Section\ref` -> `Section~\ref`
- `Eq,~` instead of `Eq.~` (comma vs period)
- Inconsistent `\citet` vs `\cite` usage
- Unclosed braces or environments

### Step 4: Spacing Issues
- Double spaces in prose (outside of LaTeX commands)
- Missing space after period (except in abbreviations like "e.g." or "i.e.")
- Tab/space mixing in indentation
- Trailing whitespace on lines

### Step 5: Equation Punctuation
For displayed equations (`\[...\]`, `equation`, `align`):
- Check trailing punctuation: equations ending sentences need a period, mid-sentence need a comma
- Consistent punctuation style across the paper

### Step 6: Capitalization
- Section/subsection titles: check for consistent capitalization style
- "Theorem", "Lemma", "Proposition" capitalized when used as proper nouns with numbers
- "equation" lowercase when used generically, but "Eq." when followed by a reference

### Step 7: Banned Words
Check all prose against `references/banned-words.md` for prohibited terms.

### Step 8: Output

```
PROOFREAD REPORT
================

File: [filename]
Scope: [section or full file]
Lines scanned: [count]

TYPOS: [N found]
- Line 109: "componet" -> "component"

LATEX FORMATTING: [N found]
- Line 153: "Eq,~\eqref" -> "Eq.~\eqref" (comma should be period)
- Line 245: "\ref{eq:delay}" -> "\eqref{eq:delay}" (equation reference)

SPACING: [N found]
- Line X: double space between "the  signal"

EQUATION PUNCTUATION: [N found]
- Line X: displayed equation ends sentence but has no period

CAPITALIZATION: [N found]
- Line X: "theorem 1" -> "Theorem 1"

BANNED WORDS: [N found]
- Line X: "[banned word]" -> [suggested replacement]

SUMMARY:
- Total mechanical errors: N
- Typos: A
- LaTeX formatting: B
- Spacing: C
- Punctuation: D
- Capitalization: E
- Banned words: F
```
