---
description: Screen a research idea with scoring and novelty check
---

Run the `finance-idea-screening` skill on this idea:

$ARGUMENTS

Steps:
1. Run Stage 0 desk-editor screen (four quick questions). If weak, stop early with Revise/Kill.
2. Restate the idea in one sentence (question-first framing — not "Using X data...").
3. Search for closest papers using `search_papers` (do not skip this).
4. Score on 6 dimensions (question, importance, contribution, mechanism, bridge, data) using the 1-5 rubric.
5. Apply decision rules: Top-3 Go (importance>=4, contribution>=4, bridge>=4, no dim<3, <=3 hurdles) / Field-journal Go (all>=3, total>=18) / Revise / Kill.
6. Run the three stress tests (null-result value, simultaneous-discovery, syllabus sentence).
7. Identify the 2-3 essential hurdles and apply the revision-feasibility rule.
8. Recommend journal track and describe the killer exhibit.

Produce a complete Idea Card.
