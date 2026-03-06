---
name: research-debate
description: "Run a structured multi-round debate between two AI agents on a research question. Use for stress-testing identification strategies, choosing between methods, evaluating contributions, debating mechanisms, or any decision where adversarial reasoning sharpens thinking."
---

# Research Debate

Force rigorous adversarial deliberation on research decisions by running two agents with opposing positions through multiple rounds of structured debate, then synthesize the convergence.

## When to use

- Stress-testing an identification strategy (attack vs. defend)
- Choosing between two empirical approaches (DiD vs. IV, hedonic vs. repeat-sales)
- Evaluating whether a contribution is strong enough for a target journal
- Debating mechanism vs. alternative explanations
- Deciding between journal targets (JFE vs. REE)
- Assessing whether a robustness check is necessary or performative
- Any research decision where you want both sides argued at full strength before deciding

## Persona detection

Detect the debate structure from the user's prompt and assign personas accordingly.

**Single-claim prompts** (one position to stress-test):
- "Is the leave-one-out approach a good IV?"
- "Is our contribution strong enough for JFE?"
- "Can we claim this is causal?"
- Assign: **Skeptic** (attacks the claim) vs. **Advocate** (defends the claim)

**Two-sided prompts** (choosing between alternatives):
- "DiD vs. IV for this staggered adoption setting"
- "Should we target JFE or REE?"
- "Is the mechanism information asymmetry or moral hazard?"
- Assign: **Agent A** (champions option 1) vs. **Agent B** (champions option 2)

**Evaluation prompts** (assessing quality or readiness):
- "Is this paper ready for submission?"
- "Are our robustness checks sufficient?"
- Assign: **Optimist** (argues it's ready, highlights strengths) vs. **Critic** (argues it's not, identifies gaps)

Name the personas explicitly when launching each agent so the user can follow the exchange.

## Round structure

### Default: 3 rounds

| Round | What happens |
|---|---|
| **Round 1** | Both agents make their opening cases independently (launched in parallel). Each argues their position at full strength with specific evidence, threats, or reasoning. |
| **Pause** | Present both Round 1 positions to the user. Ask: "Want to inject any information or steer the debate before Round 2? Or should I continue?" If the user says continue (or if running uninterrupted), proceed. |
| **Round 2** | Each agent receives the other's Round 1 argument and responds directly. They must: (a) acknowledge points they concede, (b) identify what was dodged or understated, (c) refine their own position. Launched in parallel. |
| **Pause** | Present both Round 2 responses. Ask again if the user wants to inject. |
| **Round 3** | Final round. Each agent receives the other's Round 2 response and delivers a final assessment: what they're now convinced by, what remains unresolved, and their bottom-line recommendation. Launched in parallel. |
| **Synthesis** | A separate synthesis agent reads all 6 outputs and produces the structured convergence report. |

### Calibrating round count

- **2 rounds** -- simpler decisions with a clear trade-off (clustering choice, variable definition, subsample restriction). Skip the user pauses, run all rounds, then synthesize.
- **3 rounds** (default) -- identification strategies, contribution evaluation, method selection. Include user pauses.
- **4+ rounds** -- deep methodological debates or when the user explicitly asks for more depth. Rare.

If the prompt is short and specific (under ~50 words, clear binary choice), suggest 2 rounds. If the prompt describes a full empirical design or complex trade-off, default to 3. If the user specifies a round count, use it.

## Context injection

Before launching the debate, check whether the user references files, data, or prior work in the project. If so:

1. Read the relevant files (paper draft, code, design memo, skill output).
2. Include the relevant context in both agents' prompts so they argue from the actual paper, not hypotheticals.
3. If the user pastes text directly into the prompt (as with an IV description), use that as the primary context.

If no context is provided and the question is about a general methodological issue, the agents argue from general principles and the empirical finance/real estate literature.

## Agent prompt templates

### Round 1 prompts

**Skeptic / Critic / Agent B:**
```
You are a [Skeptic / Critic / Agent championing Option B]. You are a rigorous empirical
researcher reviewing a [research design / contribution / method choice].

YOUR TASK: [Attack the claim / Argue for Option B / Identify every gap].

Be specific: name exact threats, cite methodological standards, and suggest what evidence
would change your mind. Do not be polite -- be rigorous. Structure your response with
clear numbered points.

CONTEXT:
[User's description + any file contents]

Be exhaustive in Round 1. This is your opening case.
```

**Advocate / Optimist / Agent A:**
```
You are an [Advocate / Optimist / Agent championing Option A]. You are a rigorous empirical
researcher defending [the claim / Option A / the paper's readiness].

YOUR TASK: [Defend the claim / Argue for Option A / Make the strongest case].

Anticipate the most common objections and preemptively address them. Be honest about
limitations but firm where the position is strong. Structure your response with clear
numbered points.

CONTEXT:
[User's description + any file contents]

Make your strongest case in Round 1. Do not hold back arguments for later rounds.
```

### Round 2 prompts

Each agent receives the other's Round 1 output and is instructed:
```
You have now read [the other agent's] opening argument. Respond directly:

1. Which of their points do you concede? Be specific.
2. Which points did they dodge, understate, or get wrong? Explain why.
3. What new weaknesses does their argument reveal?
4. What is your updated position?

Do not repeat your Round 1 arguments. Only address what is new or contested.
```

### Round 3 prompts

Each agent receives the other's Round 2 output and is instructed:
```
This is your FINAL round. Give your final assessment:

1. What are you now convinced by? (List specific points you've moved on.)
2. What 2-3 concerns remain genuinely unresolved?
3. What is your bottom-line recommendation?
4. What specific evidence or diagnostics would resolve the remaining disagreements?

Be fair. Acknowledge where the other side made you a better thinker.
```

### Synthesis prompt

A separate agent reads all outputs from both agents across all rounds:
```
You are a neutral synthesizer. You have read a [N]-round structured debate between
[Agent A name] and [Agent B name] on the following question:

[Original user question]

Read all [2N] debate outputs below and produce a structured convergence report.

[All agent outputs, labeled by round and agent]

PRODUCE THIS EXACT STRUCTURE:

## Debate summary
One paragraph: what was debated, how positions evolved across rounds.

## Agreed
Numbered list of positions both agents converged on by the final round. For each,
state the agreed position clearly and note which round produced convergence.

## Unresolved
Numbered list of genuine remaining disagreements. For each, state both sides'
best final argument in one sentence each.

## Action items
Numbered list of concrete things to do, ranked by priority. Each item should be
specific enough to execute (not "think more about X" but "add tenant credit rating
controls and report coefficient stability").

## Diagnostics required
If the debate involved an empirical strategy, list the specific tests that must
pass for the proposed approach to be credible. State what "pass" and "fail" look
like for each.

## Recommended next steps
Which skills or slash commands to use next based on the debate outcome.
(e.g., "Use finance-identification-design to implement the agreed diagnostic battery"
or "Use python-empirical-code to run the balance tests").

Be concise. The action items and diagnostics are the most valuable part of this output.
```

## User interjection

When pausing between rounds, present both agents' outputs and ask:

> "Round [N] complete. Want to add information, correct either agent, or steer the debate? Or type 'continue' to proceed to Round [N+1]."

If the user provides input:
- Append it to both agents' prompts for the next round as "ADDITIONAL CONTEXT FROM THE RESEARCHER"
- Flag it clearly so agents treat it as ground truth about the paper's data, methods, or institutional setting

If the user says "continue," "go," "next," or similar, proceed immediately.

If the user asked to run the full debate without pauses (e.g., "run all rounds"), skip pauses entirely.

## Output format

The final deliverable is the synthesis report. Save it as `DEBATE_[topic_slug]_[date].md` in the project root.

```
# Research Debate: [Topic]
**Date:** [date]
**Rounds:** [N]
**Personas:** [Agent A name] vs. [Agent B name]
**Question:** [Original user prompt]

## Debate summary
[One paragraph]

## Agreed
1. [Position]
2. [Position]
...

## Unresolved
1. [Disagreement + both sides' best argument]
2. [Disagreement + both sides' best argument]
...

## Action items
1. [Highest priority concrete action]
2. [Next priority]
...

## Diagnostics required
| # | Test | Pass | Fail |
|---|------|------|------|
| 1 | ... | ... | ... |

## Recommended next steps
- [Skill or command to use next]
```

## Tool integration (Corbis MCP)

Debate agents should ground their arguments in evidence, not just parametric knowledge. The orchestrator should use Corbis tools to supply context before and during the debate.

**Before Round 1 (context gathering):**
- `search_papers` (query: the core claim or method under debate, `matchCount: 10-15`) -- find papers that support or challenge the position being debated. Include relevant results in both agents' Round 1 prompts.
- `top_cited_articles` (target journals, `minYear` as appropriate) -- find the seminal papers in the relevant field. Especially valuable for contribution-evaluation and journal-targeting debates.
- `get_paper_details` (IDs of the most relevant papers from the search) -- get full abstracts so agents can engage with what papers actually do, not just their titles.

**During rounds (agent-level):**
- Instruct agents that they may request specific paper searches to support their arguments. When an agent cites a paper by name, verify the claim with `get_paper_details` before passing the argument to the other agent.
- `search_datasets` -- when debating data feasibility or alternative empirical approaches, check what datasets actually exist rather than arguing hypothetically.
- `fred_search` / `fred_series_batch` -- when debating macro-related designs or instruments, pull actual data properties (frequency, coverage, volatility) to settle factual disputes.
- `get_market_data` / `compare_markets` / `search_markets` -- for real-estate debates, ground market claims in actual CRE data.

**After synthesis:**
- `export_citations` (format: `bibtex`) -- export BibTeX entries for all papers cited during the debate so the user has them ready for the manuscript.

## Guardrails

- Do not let agents strawman each other. If an agent mischaracterizes the other's argument, flag it in the next round's prompt.
- Do not let the synthesis paper over disagreements. If the agents did not converge, say so clearly.
- Do not run more than 5 rounds. Debates that haven't converged by round 4-5 have a genuine unresolvable disagreement, which is itself a useful finding.
- Agents should argue from the empirical finance/real estate literature and current methodological standards (not abstract philosophy).
- If the debate touches on identification, apply the same standards as `finance-identification-design`: modern estimators, proper inference, named threats.
- The user's injected context is ground truth. Agents should not contradict factual claims the user makes about their data or setting.

## Example prompts

- "Is the leave-one-out tenant mean a valid IV for lease term effects on cap rates?"
- "DiD vs. synthetic control for studying opportunity zone effects on property values"
- "Should we target JFE or Real Estate Economics with this housing supply paper?"
- "Is our mechanism evidence sufficient, or is it just heterogeneity relabeled as mechanism?"
- "Debate whether our staggered DiD needs Callaway-Sant'Anna or if TWFE is fine here"
- "Is this paper's contribution incremental or does it change how we think about mortgage default?"
- "Clustering at MSA vs. state for this bank branching paper"
- "Should we include the Internet Appendix robustness or is it overkill?"
