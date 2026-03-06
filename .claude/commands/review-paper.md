---
description: Run a 6-agent pre-submission audit of an academic paper
---

Run the `pre-submission-review` skill on this paper.

**Target journal**: $ARGUMENTS (if empty, use "top-field" general standards)

Follow the full skill workflow:
1. Phase 1: Parse the target journal and discover all .tex files, figures, and tables in the current project directory.
2. Phase 2: Launch all 6 review agents in parallel (spelling/grammar, internal consistency, claims/identification, math/notation, tables/figures, contribution evaluation).
3. Phase 3: Consolidate into a single report and save to `PRE_SUBMISSION_REVIEW_[YYYY-MM-DD].md`.

Report the top 5 priority action items and the preliminary recommendation when done.
