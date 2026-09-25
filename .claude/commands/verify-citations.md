---
description: Verify every BibTeX entry and check manuscript citation keys when available
---

Run the `verify-citations` skill for the following file or project:

$ARGUMENTS

Audit the complete `.bib` file with `verify_bibtex`, including uncited entries. If a manuscript is present, check its citation keys, including `\citet`, against that bibliography. Report corrections, unresolved entries, parse errors, missing keys, and unused entries. Do not silently change references.
