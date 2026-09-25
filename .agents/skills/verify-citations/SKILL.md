---
name: verify-citations
description: Audit every entry in a BibTeX file against the Corbis paper index and cross-check LaTeX citation keys when a manuscript is available
user_invocable: true
---

# Verify Citations

Audit the whole `.bib` file, including entries that a manuscript does not cite. Corbis `verify_bibtex` resolves entries against its paper index and reports field-level corrections. An unresolved entry remains unverified, not false.

## Inputs

- `/verify-citations` finds the project's `.bib` file. If more than one plausible file exists, use the manuscript's `\bibliography{}` or `\addbibresource{}` reference when available; otherwise ask which file to audit.
- `/verify-citations path/to/references.bib` audits that full file without requiring a `.tex` file.
- `/verify-citations path/to/paper.tex` locates its bibliography and also checks in-text citation keys.
- `/verify-citations --key key_name` audits one entry from the selected bibliography.

## Workflow

1. Read the selected `.bib` file. Never send credentials, private notes, or unrelated files with it.
2. Call `verify_bibtex` with `bibtexContent` set to the raw BibTeX content and `maxEntries` large enough for the file (up to 200). For larger bibliographies, split on complete BibTeX entries into batches of at most 200. Check `totalEntries`, `parsedCount`, `parseErrors`, and every returned entry so no record is silently skipped.
3. Report each entry as **OK** (resolved, no corrections), **CORRECTION** (resolved, with field-level differences), **UNVERIFIED** (unresolved), or **PARSE ERROR**. Show the proposed correction and its Corbis basis; do not silently alter the `.bib` file. Verify consequential differences against the publisher, DOI landing page, or paper PDF before applying them.
4. Run `python utils/citation_keys.py path/to/references.bib --tex path/to/main.tex` when a manuscript exists. The helper scans the manuscript and included `.tex` files for natbib commands, including `\cite`, `\citep`, `\citet`, and optional-argument forms. It reports missing keys and unused bibliography entries separately. Without a manuscript, run it with the `.bib` path alone to list every entry. This is a key-coverage check, not metadata verification.
5. Save the report to `output/citation_audit.md` with file paths, total/parsed/resolved/unresolved counts, parse errors, corrections, missing keys, and unused entries. Append a dated entry to `notes/lab_notebook.md`.

If `verify_bibtex` is unavailable for the current connection, say so and verify entries using `search_papers` followed by `get_paper_details_batch` for discovered IDs. Label any entry that still lacks a source **UNVERIFIED**. Never invent a citation or copy unverified supplied metadata into a verified bibliography.
