---
description: Write a structured literature review on a topic with Corbis-backed searches and BibTeX citations
---

Run the `literature-review` skill for the following topic:

$ARGUMENTS

Use the literature-review skill's defaults when the user provides a topic. Ask only for an input required by a chosen format that cannot be inferred from the project.

Execute the full workflow:
1. Search and collect (~50 papers for comprehensive, ~25 for focused) using the mandatory Corbis search sequence
2. Propose 4-6 thematic strands and wait for user approval before writing
3. Write the review as synthesized prose (not paper-by-paper enumeration)
4. Verify cited paper metadata, export BibTeX using `citations` objects and `formats: ["bibtex"]`, then check the result with `verify_bibtex`
5. Produce a reading list of top 10-15 papers
6. Log to lab notebook and update project state
7. Present a coverage report in chat
