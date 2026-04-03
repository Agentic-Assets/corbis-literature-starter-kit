---
description: Quick cross-section consistency check
---

Run the `check-consistency` skill on this paper.

**Focus**: $ARGUMENTS (if empty, run full scan; options: "numbers", "terminology")

Steps:
1. Load reference values from `notes/project_state.md` (if it exists).
2. Check quantitative consistency across all sections (percentages, sample periods, counts).
3. Check terminology consistency and banned words per `references/banned-words.md`.
4. Verify cross-reference integrity (all `\ref` and `\eqref` targets exist, equations use `\eqref`).
5. Verify section cross-references ("As shown in Section X", "Table Y reports").
6. Run `/audit-captions` for caption-level consistency.
7. Output a consistency check report with critical issues and warnings.
