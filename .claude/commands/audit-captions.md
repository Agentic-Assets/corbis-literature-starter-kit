---
description: Audit table and figure captions for consistency
---

Run the `audit-captions` skill on this paper.

**Scope**: $ARGUMENTS (if empty, audit all captions in main.tex)

Steps:
1. Load context from the project's notation file, `references/writing-norms.md`, and `notes/project_state.md`.
2. Extract all `\caption{}` blocks and build a numbered registry.
3. Check language consistency (sample periods, return descriptions, methodology descriptions, variable definitions).
4. Check notation consistency, terminology compliance, structural consistency, number formatting, and abbreviation usage.
5. Cross-reference captions against body text claims.
6. Detect copy-paste drift between similar captions.
7. Output a caption audit report with severity summary and standardization recommendations.
