---
name: research-idea-generator
description: "Generate novel research ideas in finance and real estate using structured heuristic lenses with internal rejection filtering. Produces a curated Idea Menu of survivors, not a brainstorming list."
---

# Research Idea Generator

Generate a broad set of candidate research ideas, kill the weak ones internally, and present only the survivors. This skill is a generator with a built-in filter. The user sees 10 ranked ideas; the model generates 25-30 and discards the rest.

## The vector-space principle

A good research idea is an arrow from the current literature toward reality. The larger the gap between what economists assume and how the world actually works, the more impactful the idea.

Three idea-source strategies, ranked by effectiveness:

1. **Starting from practitioner reality** (strongest): Real-world observations reveal where reality diverges from what economists assume. These observations mark where reality is, letting you draw the arrow from literature to reality.

2. **Starting from a cool dataset** (risky): A dataset generates many possible directions but no "hook" connecting to a specific literature-reality gap. Without a question, tinkering with data is unproductive. A dataset is a tool, not an idea.

3. **Starting from the literature** (weakest for generation): Reading papers and looking for extensions typically produces marginal additions. Literature knowledge is essential for positioning an idea, but is a poor source of ideas.

## Phase 0: Collect user constraints

Before generating anything, collect and record these as **hard filters** on ranking. An idea that violates a hard constraint cannot rank in the top 5 regardless of its intellectual appeal.

| Constraint | Question to ask | How it binds |
|---|---|---|
| Data access | What databases, proprietary data, or institutional access do you have? | Ideas requiring unavailable data are capped at Medium feasibility |
| Methods comfort | What empirical methods are you comfortable executing? (DiD, RDD, structural, NLP, etc.) | Ideas requiring unfamiliar methods are downranked unless a coauthor fills the gap |
| Field comfort | What literatures do you know well enough to position a paper? | Ideas in unfamiliar fields require more literature work |
| Journal ambition | Are you targeting top-3 (JF/JFE/RFS), strong field (JFQA/RoF), or any good outlet? | Determines contribution bar |
| Coauthor skills | What complementary skills does a coauthor bring? | Relaxes method or field constraints |
| Timeline | How soon do you need a working paper? | Long-horizon structural projects vs. quick empirical exercises |

If the user provides a topic and constraints in their initial message, proceed without asking. Fill defaults for anything not specified (assume broad data access, standard empirical methods, field-journal ambition, solo researcher, 12-month timeline).

## Phase 1: Map the landscape

Run 3-4 Corbis searches to understand the current state of the field:

1. `search_papers` (broad topic query, `matchCount: 15`) to find the core literature
2. `search_papers` (same topic, `minYear: 2023`, `matchCount: 15`) to catch the frontier
3. `search_papers` (topic + "survey" or "review", `matchCount: 10`) to find survey papers

Use `get_paper_details_batch` on the top 5-10 results to read abstracts and understand what has been established. Use `sortBy: "citedByCount"` on search calls to surface the most influential papers first.

Produce a 3-4 sentence internal landscape summary: what is settled, what is actively debated, where the frontier is moving.

## Phase 2: Generate candidates (internal, not shown to user)

Apply all eleven lenses to the topic area. Generate 2-3 rough candidates per lens. Target 25-30 total candidates. Most will be discarded.

### Stage A: Generative lenses (reality-first)

These lenses produce the raw material. Apply these first.

**Lens 1: Practitioner-reality gap**

Start from how real actors behave, and ask whether this conflicts with what economists assume. Use these specific elicitation prompts:

- What do practitioners optimize that theory says they should not?
- What variable do practitioners obsess over that papers ignore?
- What decision rule do people use in practice that would look irrational in a model?
- What do industry participants know that academics have not documented?

Search with `search_papers` for "[topic] survey evidence" or "[topic] practitioner" to find papers documenting real-world behavior. If the user provided anecdotes, use those as the starting point.

The test: can you name a specific assumption in the literature that conflicts with observed behavior? If yes, the idea is well-formed. If not, the observation is interesting but not yet an idea.

**Lens 2: Cross-pollination**

Borrow a well-established concept, method, or finding from a neighboring field (labor, IO, macro, behavioral, urban, computer science) and apply it where it has not been used. The imported concept must generate a genuinely different economic prediction in the new setting, not just "X but in field Y."

**Lens 3: First principles / economic logic**

Start from a fundamental friction (information asymmetry, moral hazard, search costs, limited attention, regulatory distortion, market segmentation) and derive a testable prediction. Then check whether anyone has tested it. The best first-principles ideas feel obvious in retrospect.

**Lens 4: Unification**

Multiple individually documented findings are manifestations of the same underlying economic force. The synthesis is the paper. List 3-5 well-known findings and ask: is there a single mechanism that explains all of them? The unification must generate a new testable prediction.

**Lens 5: Policy / regulatory shock**

A recent policy change creates a natural experiment. The policy is the instrument, not the contribution. The question must be bigger than the policy. Search for recent (past 3-5 years) shocks relevant to the topic.

### Stage B: Refinement lenses (literature-positioned)

These lenses sharpen, reframe, or find angles on existing knowledge. Apply these second, using the landscape from Phase 1.

**Lens 6: Literature gap**

Find questions that survey papers flag as open. The gap must be economically meaningful, not just "nobody has run this regression." Caution: literature-driven ideas tend to produce marginal extensions. This lens should sharpen, not source.

**Lens 7: Conflicting findings**

Two credible papers reach opposite conclusions. The reconciliation is the idea. The moderating variable or identification flaw that explains the conflict becomes the contribution.

**Lens 8: Mechanism decomposition**

Take an established result and ask: what is the economic channel? Can you distinguish competing mechanisms? Many highly cited papers document effects without pinning down why. Include the measurement-error angle: does a canonical variable mismeasure the intended concept in a systematic way that changes interpretation? (Example: the literature thinks it measures financial constraint, but the proxy is contaminated by firm quality.)

**Lens 9: Boundary conditions and equilibrium displacement**

When does a canonical finding break down? The failure must map to a theory. Include the equilibrium-displacement angle: if agents adapt to the original finding, who absorbs the incidence or where does the effect move? In household finance, asset pricing, and real estate, strategic adjustment often produces deeper questions than simple treatment-effect framing.

**Lens 10: New data x old question**

Pair a recently available data source with a classic question. The data must enable a genuinely better answer through new identification, new measurement, or a new population, not just a new time period or higher frequency.

**Hard constraint on this lens:** Ideas from this lens should almost never produce a top-3 idea unless the data changes measurement or identification in a first-order way. If the only contribution is "now we can observe X more granularly," downrank to field-journal tier.

**Lens 11: Model meets data**

Theoretical models make quantitative predictions that have not been tested. The paper tests the prediction. What would rejection mean for the theory?

## Phase 3: Three-part novelty test (internal, not shown)

For every candidate idea (all 25-30), run this test using `search_papers`:

1. **Closest existing paper**: Search for the specific idea. Name the single closest paper.
2. **Not relabeling**: In one sentence, state why this idea is not a relabeling of that paper. What is structurally different: mechanism, prediction, identification, or setting with different economics?
3. **New prediction**: State the one prediction or finding this paper would produce that the closest paper does not.

**If you cannot articulate all three clearly, the idea is discarded.** Do not proceed to the kill test.

## Phase 4: Internal kill test (not shown to user)

For each candidate that survives the novelty test, answer three questions:

1. **Already done?** What search result or combination of papers might already cover this? What would you find if you searched harder?
2. **Identification failure?** What is the most likely reason the causal design fails? (Endogeneity, measurement error, insufficient power, parallel trends violation, weak instrument.)
3. **Seminar indifference?** Why might a skeptical seminar audience shrug? Is the question first-order, or is it a niche exercise that only the authors care about?

**Decision rule:**
- Fails 0 of 3: strong survivor, proceed
- Fails 1 of 3: proceed with the failure noted as a risk
- Fails 2 of 3: discard
- Fails 3 of 3: discard

## Phase 5: Score and rank survivors

For each surviving candidate (~10-15), score on three dimensions:

| Dimension | 1 (Low) | 3 (Medium) | 5 (High) | One-line justification required |
|---|---|---|---|---|
| **Novelty** | Close paper exists, marginal extension | Adjacent work but distinct angle | No close paper, new prediction | Yes |
| **Importance** | Niche, small audience | Active field, moderate audience | First-order question, broad audience | Yes |
| **Executability** | Data unavailable or method beyond reach | Feasible but requires significant investment | Data in hand, method familiar | Yes |

**Composite score** = Novelty + Importance + Executability (max 15). Rank by composite. Break ties in favor of reality-first lenses.

**Apply user constraints as hard filters:**
- If data access is insufficient and no workaround exists: cap Executability at 2
- If method is unfamiliar and no coauthor fills the gap: cap Executability at 3
- If journal ambition is top-3 but Importance < 4: flag as "field-journal tier"

Select the top 10 for the Idea Menu.

## Phase 6: Assign contribution tiers

For each of the 10 survivors, assign one tier:

| Tier | Description | Bar |
|---|---|---|
| **Top-journal** | Broad mechanism, general implications, strong identification | Would change how a wide audience thinks about the topic |
| **Field-journal** | Clean question within an active literature, solid design | Advances the conversation in a specific field |
| **Workshop** | Feasible and interesting but narrower scope | Good execution, useful contribution, limited breadth |

Be honest. Most ideas are field-journal tier. Labeling everything as top-journal quality is a failure mode.

## Phase 7: Produce the Idea Menu

Use `assets/idea-menu-template.md`. Present all 10 ideas with:
- Rank
- One-sentence question (question-first, never "Using X data...")
- Lens that generated it
- Closest paper (from novelty test)
- Novelty / Importance / Executability scores
- Contribution tier
- Key risk (from kill test)

## Phase 8: Expand top 3 into Idea Sketches

For the three highest-ranked ideas, provide an Idea Sketch with:

**One-sentence question**

**Seminar pitch**: "This paper shows that ___ because ___." One sentence that states the real contribution. If you cannot write this sentence, the idea is not formed.

**Core mechanism or friction** (2-3 sentences): Name the economic force. State the testable prediction.

**Question / Mechanism / Prediction / Identification / Data / Why now**: Structure these explicitly as six labeled items. If any one is weak, acknowledge it.

**Theory-to-evidence bridge** (one paragraph): What is the test? What variation is exploited? What would the ideal table or figure show?

**Key data requirements**: Specific datasets, access, coverage.

**Contribution tier**: Top-journal / Field-journal / Workshop, and why.

**Referee vulnerability**: "The hardest challenge is whether ___ is just proxying for ___." One sentence stating the toughest objection.

**Why this idea beats the other top candidates**: One sentence on why this ranks above the alternatives.

**Why this idea is not dominated by a cleaner adjacent project**: One sentence.

## Phase 9: Recommend next steps

Suggest running `/idea` on the most promising candidate for full screening. Note any ideas that would benefit from `/lit-search` to deepen positioning, or `/lit-landscape` to visualize the field structure.

## Tool integration (Corbis MCP)

**Never claim an idea is novel without searching first.**

### Landscape mapping (Phase 1)
1. `search_papers` (broad topic, `matchCount: 15`) — current state
2. `search_papers` (topic, `minYear: 2023`, `matchCount: 15`) — frontier
3. `search_papers` (topic + "survey", `matchCount: 10`) — survey papers
4. `get_paper_details_batch` (top 5-10 paper IDs in one call) — read abstracts, get citation counts

### Per-candidate novelty checks (Phase 3)
- `search_papers` (the specific idea, `matchCount: 10`) — for each candidate
- `get_paper_details_batch` on the closest results across candidates — confirm overlap vs. vocabulary similarity

### Data feasibility
- `search_datasets` (topic keywords) — discover available datasets
- `fred_search` (keywords) — find relevant macro series

### After generation
- `export_citations` (format: `bibtex`) — export BibTeX for closest papers identified during generation

## Guardrails

These are hard bans. Ideas that violate these rules are discarded regardless of their score.

- **Ban "X but in country Y"** unless the new setting generates a genuinely different economic prediction.
- **Ban context-only contributions** where the only novelty is applying a known result to a new industry, time period, or population without new economics.
- **Ban ideas whose identifying variation is more memorable than the question.** If the shock is cleverer than what it identifies, the idea is backwards.
- **Ban pure heterogeneity mining** unless tied to a theory-derived margin that generates a distinct prediction. "The effect is stronger for constrained firms" is not a paper unless you explain why and what it rules out.
- **Ban ideas that cannot be explained to a seminar audience in two sentences.** If the contribution requires a paragraph of caveats to state, it is not a contribution.
- **Do not let a clever dataset or natural experiment substitute for a question.** The question must come first; the design serves the question.
- **Do not generate more than 2 ideas from the same lens.** Breadth of attack across heuristics is the value of this skill.
- **Do not present 10 equally enthusiastic ideas.** Rank honestly. Assign tiers honestly. Some ideas are workshop-tier. Say so.
- **Do not overclaim novelty.** If the search reveals a close paper, note it and adjust or drop the idea.
- **At least 3 of the 10 survivors must come from Stage A (generative) lenses.** Gap-filling and data-driven ideas are easy to generate but often lower impact.
- **An "interesting relationship" is NOT a research idea.** The idea must have a testable tension between theory and reality, not just a correlation to document.

## Preferred outputs

Produce:
1. **Idea Menu** — 10 ranked survivors using `assets/idea-menu-template.md`
2. **Idea Sketches** — expanded treatment of the top 3
3. **Next-step recommendation** — which idea to screen first and why

## Example prompts

- "Brainstorm 10 ideas in behavioral asset pricing."
- "Generate research ideas about climate risk and real estate."
- "I have access to Revelio Labs workforce data — brainstorm ideas in corporate finance."
- "Help me come up with ideas at the intersection of fintech and household finance."
- "Brainstorm ideas about intermediary asset pricing and credit markets."
- "Generate ideas in empirical corporate governance using NLP/LLM methods."
