---
name: verify-citations
description: Verify all citations against bibliography
---

Run the `verify-citations` skill on this paper.

$ARGUMENTS

Steps:
1. Find the main `.tex` file in the project (check `paper/`, `latex_template/`, or the root directory). If multiple `.tex` files exist, ask the user which one to audit. Extract all `\cite{KEY}` and `\citep{KEY}` commands.
2. Find the `.bib` file (check the same directory as the `.tex` file, then the project root). Read the full BibTeX database.
3. For each citation key, check it exists in `.bib` and verify author, title, year, journal via `search_papers` and `get_paper_details`.
4. Classify each citation: OK, PARTIAL, MISMATCH, UNVERIFIED, or MISSING.
5. Output a verification report with flagged entries.

Process citations in batches of 5 to respect rate limits.
