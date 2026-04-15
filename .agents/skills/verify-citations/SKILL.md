---
name: verify-citations
description: Audit citations in LaTeX files -- check all \cite keys exist in .bib and verify via literature search
user_invocable: true
---

# Verify Citations Skill

Audit citations for correctness. Checks that every \cite{KEY} has a matching BibTeX entry and verifies each entry against online search.

## Examples
- `/verify-citations` -- auto-detect the .tex and .bib files in the project
- `/verify-citations paper/my_paper.tex` -- audit a specific file
- `/verify-citations --key blume1983` -- verify single entry

## Workflow

1. Find the main `.tex` file: check `paper/`, `latex_template/`, then the project root for files containing `\documentclass`. If multiple candidates exist, ask the user which to audit. Extract all `\cite{KEY}` and `\citep{KEY}` commands.
2. Find the `.bib` file: check the same directory as the `.tex` file, then the project root. Read the full BibTeX database.
3. For each citation key:
   a. Check KEY exists in .bib -- if missing, flag as MISSING
   b. Extract: author, title, year, journal from the BibTeX entry
   c. Use `search_papers` to verify: `"{title}" {first author surname} {year}`
   d. Use `get_paper_details` to confirm details when a match is found
   e. Build comparison table:

      | Field | BibTeX value | Search result | Match? |
      |-------|-------------|---------------|--------|
      | Authors | {from .bib} | {from search} | Y/N/-- |
      | Title | ... | ... | Y/N/-- |
      | Year | ... | ... | Y/N/-- |
      | Journal | ... | ... | Y/N/-- |

      Use Y = confirmed, N = mismatch, -- = not found in search.
      CRITICAL: If search returns blank for a field, write "NOT FOUND IN SEARCH" -- NEVER fill from memory.

4. Classify each citation:
   - **OK**: ALL fields confirmed
   - **PARTIAL**: Authors + title confirmed, journal/volume not found
   - **MISMATCH**: Fields contradict search results
   - **UNVERIFIED**: Cannot find paper online
   - **MISSING**: Key in \cite{} but not in .bib

5. For forthcoming papers: use `search_papers` with additional queries as fallback to check journal placement

6. Output verification report:
   ```
   Citation Audit: [detected .tex file]
   Total: N citations checked
   OK: X | Partial: Y | Mismatch: Z | Missing: W

   --- FLAGGED ENTRIES ---
   [KEY] STATUS: details...
   ```

Process citations in batches of 5 to respect rate limits.
