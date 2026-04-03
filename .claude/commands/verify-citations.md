---
description: Verify all citations against bibliography
---

Run the `verify-citations` skill on this paper.

$ARGUMENTS

Steps:
1. Read `main.tex` and extract all `\cite{KEY}` and `\citep{KEY}` commands.
2. Read the `.bib` file to get the full BibTeX database.
3. For each citation key, check it exists in `.bib` and verify author, title, year, journal via `search_papers` and `get_paper_details`.
4. Classify each citation: OK, PARTIAL, MISMATCH, UNVERIFIED, or MISSING.
5. Output a verification report with flagged entries.

Process citations in batches of 5 to respect rate limits.
