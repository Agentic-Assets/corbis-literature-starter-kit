---
description: Audit mathematical proofs and derivations in the paper
---

Run the `audit-math` skill on this paper.

**Target section**: $ARGUMENTS (if empty, scan main.tex for the first section with formal environments)

Follow the full skill workflow:
1. Load context from the project's notation file and `notes/project_state.md` (if they exist).
2. Inventory all formal environments (definitions, assumptions, lemmas, propositions, corollaries, theorems, proofs, remarks).
3. Audit assumption dependencies, proof completeness, sign analysis, boundary cases, notation consistency, cross-references, and interpretive prose.
4. Classify each finding by severity (CRITICAL, IMPORTANT, MINOR, NICE-TO-HAVE).

Report the severity summary and top priority fixes.
