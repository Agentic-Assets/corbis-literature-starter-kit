---
description: Parse referee reports and draft a revision response
---

Run the `referee-revision-response` skill:

$ARGUMENTS

Workflow:
1. Parse the editor letter and referee reports into distinct issues.
2. Classify each issue (identification, contribution, measurement, writing, analysis request, scope).
3. Triage: identify the 2-3 issues that determine acceptance.
4. Decide response strategy for each (concede / partially concede / disagree with evidence / explain infeasibility).
5. Map every issue to a specific manuscript change.
6. Draft point-by-point response language.

Use `search_papers` and `get_paper_details` to verify any literature claims referees make.

Produce:
- Revision strategy memo
- Comment-action matrix
- Draft response language for each comment
- Cover letter draft
- List of claims to narrow
- Manuscript revision checklist
