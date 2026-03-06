---
name: referee-revision-response
description: "Plan revisions and draft referee responses for finance or real-estate papers. Use for R&Rs, editor letters, comment matrices, claim narrowing, and response letters."
---

# Referee Revision Response

Handle revision like an argument-mapping problem, not a public-relations exercise.

## Workflow

1. Parse the editor letter and referee reports into distinct issues.
2. Classify each issue using the taxonomy below.
3. Assess severity: which issues threaten acceptance?
4. Decide the response strategy for each issue.
5. Map every issue to specific manuscript changes.
6. Draft the response language.
7. Narrow claims where the design is weaker than the original text implied.
8. Write the cover letter to the editor.

## Issue taxonomy

| Category | Severity | Typical response |
|---|---|---|
| Central identification concern | Critical | Must address substantively with new analysis or honest concession |
| Contribution / positioning | High | Rewrite contribution claims, sharpen differentiation |
| Missing analysis | Medium-High | Add the analysis if feasible; explain if not |
| Measurement concern | Medium | Alternative measures, robustness, or acknowledged limitation |
| Writing / exposition | Low-Medium | Fix it; no defense needed |
| Scope / claim narrowing | Medium | Narrow the claim; this is often the right move |
| Literature omission | Low | Add the citations with positioning language |
| Formatting / presentation | Low | Fix it |

## Response strategy decision tree

For each comment:
1. **Is the referee right?** If yes, concede and fix.
2. **Is the referee partially right?** Concede the valid part, address the rest.
3. **Is the referee wrong but reasonable?** Disagree respectfully with evidence.
4. **Is the referee asking for something infeasible?** Explain why clearly and offer the best alternative.
5. **Is the referee asking for something that would make the paper worse?** Rare, but disagree respectfully and explain the cost.

**Default stance**: Concede more than you think you should. Referees who feel heard are more likely to recommend acceptance.

## Critical-issue triage

Before drafting any response, identify the **top 2-3 issues that determine acceptance**:
- The central identification concern (every finance paper gets this)
- The contribution claim that the referee finds unconvincing
- The data or measurement issue that undermines the main result

Address these first and most thoroughly.

## Response writing rules

### Tone
- Appreciative but not submissive
- Direct rather than verbose
- Specific about what changed and where
- Explicit when a requested analysis is not feasible
- Respectful when disagreeing, with evidence rather than attitude

### Structure for each comment
```
Referee comment: [quoted or paraphrased]

Response: [action-first]
- What we did: [specific change]
- Where: [page, table, or section reference]
- What it shows: [result or implication]
```

### Language patterns
- "We have revised the manuscript to..." (action-first)
- "The referee raises an important point about X. We address this in three ways..."
- "We agree that this concern is valid and have [specific action]."
- "We have considered this carefully and believe [evidence-based argument]."
- Avoid: "We respectfully disagree" (overused). Instead, present the evidence.

## Cover letter to the editor

Write a 1-page cover letter that:
1. Thanks the editor and referees.
2. Summarizes the 3-4 most important changes.
3. Highlights where you conceded and where you maintained your position.
4. States that the revised manuscript addresses the concerns.

## Manuscript revision checklist

- [ ] Every referee comment is addressed in the response letter
- [ ] Every change claimed in the response is actually in the manuscript
- [ ] Page/table references match the revised manuscript
- [ ] New analyses are discussed in the text, not just added to a table
- [ ] Claims have been narrowed where referees identified valid weaknesses
- [ ] The abstract reflects any changes to the main results
- [ ] The introduction reflects any changes to the contribution claim
- [ ] New references are cited and positioned, not just listed

## Default deliverables

Produce:
- a revision strategy memo (triage the critical issues first)
- a comment-action matrix using assets/response-matrix-template.md
- suggested manuscript changes (specific text edits)
- point-by-point response language
- a cover letter draft
- a list of claims to narrow

## Output format

```
# Revision package
## Editorial diagnosis (accept likely, risky, or uphill battle)
## Highest-risk issues (the 2-3 that determine acceptance)
## Action plan (ordered by importance)
## Comment-by-comment matrix
## Draft response language
## Cover letter draft
## Claims to narrow
## New tables or appendices needed
## Manuscript revision checklist
```

## Tool integration (Corbis MCP)

Referees often cite papers or make literature claims that need verification. Use tools to fact-check and strengthen responses:

- `search_papers` (query: the referee's specific claim or suggested paper, `matchCount: 10`) → verify whether a referee's literature claim is accurate. Find the actual paper they may be referencing.
- `get_paper_details` (paper IDs) → read the abstract of a paper a referee mentions to confirm what it actually does (referees sometimes mischaracterize papers).
- `search_papers` (query: the new analysis the referee requests, e.g., "instrumental variable [topic]", `minYear: 2018`) → find published examples of the requested analysis to determine feasibility and best practice.
- `top_cited_articles` (field + topic) → when a referee says "the literature has shown X," verify which papers they likely mean and whether the claim holds.
- `format_citation` / `export_citations` → generate properly formatted citations for new references added during revision.

## Reference files
Read if needed:
- references/journal-targets.md
- references/writing-norms.md

## Guardrails

- Do not bury the main concern in a long response.
- Do not promise changes that the paper cannot credibly deliver.
- If the cleanest fix is to narrow the claim, recommend that.
- If the revision request points to a fatal design flaw, say so honestly.
- Do not be defensive. The goal is acceptance, not winning an argument.
- If Referee 1 and Referee 2 contradict each other, address this transparently.
- Track the total revision scope — do not let it balloon into a different paper.

## Example prompts
- "Turn these referee reports into a revision matrix."
- "Draft the response to Referee 2 on identification and pretrends."
- "How should I revise this real-estate paper after a hostile but fair R&R?"
- "Write the cover letter for this second-round revision."
- "The referees disagree on whether I should add a structural model — how do I handle this?"
