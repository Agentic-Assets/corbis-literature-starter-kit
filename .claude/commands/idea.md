---
description: Screen a research idea with scoring and novelty check
---

Run the `finance-idea-screening` skill on this idea:

$ARGUMENTS

Steps:
1. Restate the idea in one sentence.
2. Search for closest papers using `search_papers` and `literature_search` (do not skip this).
3. Score on 5 dimensions (question, mechanism, design, data, audience) using the 1-5 rubric.
4. Apply decision rules: Go (>=18, no 1s) / Revise (13-17) / Kill (<=12 or any 1).
5. Identify the 2-3 biggest fatal risks.
6. Recommend journal track.

Produce a complete Idea Card.
