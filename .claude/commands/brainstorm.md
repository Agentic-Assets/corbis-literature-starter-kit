---
description: Generate 10 ranked research ideas from a topic area using structured heuristic lenses
---

Run the `research-idea-generator` skill on this topic:

$ARGUMENTS

Steps:
1. Map the landscape with 3-4 Corbis searches (top cited, recent work, surveys).
2. Apply all 10 idea-generation lenses to the topic area.
3. For each lens, generate 1-2 candidate ideas and verify novelty via `search_papers`.
4. Quick-screen each candidate (question, lens, closest paper, importance, risk, viability).
5. Rank by (impact potential) x (feasibility). Select top 10.
6. Produce the Idea Menu (10 ranked ideas).
7. Expand the top 3 into Idea Sketches (mechanism, bridge, data, journal track).
8. Recommend which idea to screen first with `/idea`.

Produce a complete Idea Menu with Idea Sketches for the top 3.
