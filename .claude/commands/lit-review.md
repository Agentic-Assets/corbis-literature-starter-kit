---
description: Write a structured literature review on a topic with Corbis-backed searches and BibTeX citations
---

Run the `literature-review` skill for the following topic:

$ARGUMENTS

Collect inputs: if the user did not specify output format, scope, or other options, ask before proceeding.

Execute the full workflow:
1. Search and collect (~50 papers for comprehensive, ~25 for focused) using the mandatory Corbis search sequence
2. Propose 4-6 thematic strands and wait for user approval before writing
3. Write the review as synthesized prose (not paper-by-paper enumeration)
4. Generate BibTeX citations via `export_citations` and write to .bib file
5. Produce a reading list of top 10-15 papers
6. Log to lab notebook and update project state
7. Present a coverage report in chat
