# Top Journal Writing Norms

## Baseline stance
Write like an experienced empirical finance or real estate researcher addressing skeptical referees. Every sentence should earn its place.

## Tone
- Be precise, not dramatic.
- Prefer concrete nouns and verbs over promotional adjectives.
- Avoid inflated novelty claims.
- Do not say a result is "important" without explaining the economic mechanism or quantitative magnitude.
- Distinguish clearly between association, causal interpretation, and mechanism evidence.
- Do not use em dashes. Use commas, parentheses, colons, or separate sentences instead.
- Do not use "crucially," "importantly," "interestingly," or other filler intensifiers.

## Introduction spine
Answer these questions early:
1. What is the question?
2. Why does it matter in economics or finance?
3. What is the mechanism or friction?
4. What is the empirical design?
5. What is the main finding?
6. What literatures are affected?
7. What are the economic implications?

## Theory and model exposition
- When discussing a theoretical model, lead with the economic story and intuition. Place Greek letters and formal notation in parentheses after the plain-language explanation.
- BAD: "An increase in $\alpha$ raises $\pi$ through the complementarity channel."
- GOOD: "An increase in the firm's AI adoption intensity ($\alpha$) raises operating profit ($\pi$) because AI-augmented workers complete tasks faster, reducing per-unit costs."
- Every model parameter should be introduced with its economic meaning first. The reader should understand the mechanism from the prose alone; the notation confirms the mapping.
- For model predictions, state the testable implication in words before referencing the proposition or equation number.

## Results writing protocol
- Lead each paragraph with the empirical point, not with a table number.
- BAD: "Table 3, Column 2 shows that the coefficient on X is 0.023 (t = 4.2)."
- GOOD: "Firms exposed to the shock reduce investment by 2.3 percentage points (Table 3, Column 2), equivalent to one-third of the sample standard deviation."
- Then identify the specification and sample.
- Then quantify the magnitude in economically meaningful units.
- Then interpret cautiously: what is the result consistent with?
- Then explain what remains uncertain or what the design cannot claim.

## Magnitude reporting
- Always report economic magnitudes alongside statistical significance.
- Translate into real-world units: dollars, percentage points, standard deviations, relative to the mean.
- Compare to benchmarks when available: "This effect is comparable in magnitude to [known effect from prior literature]."
- Do not rely on stars alone. Report t-statistics alongside coefficients.

### Making magnitudes intuitive (tiered translation)

A magnitude translation is only useful if the reader immediately grasps whether the effect is large or small. Use a three-tier approach:

1. **Statistical units** (minimum): SD change, percentage-point change relative to the sample mean.
2. **Real-world units** (standard): dollars per firm, basis points of return, square feet, months of rent.
3. **Anchored comparison** (best): compare to a familiar quantity the reader already understands.

- BAD (mechanical): "A one-standard-deviation increase in AI adoption is associated with a 0.8 percentage-point increase in NOI margin."
- BETTER (real-world units): "A one-standard-deviation increase in AI adoption is associated with a 0.8 percentage-point increase in NOI margin, equivalent to roughly $1.2 million in additional annual operating income for the median REIT."
- BEST (anchored): "A one-standard-deviation increase in AI adoption is associated with roughly $1.2 million in additional annual operating income for the median REIT, comparable to the cost savings from a typical energy retrofit (Eichholtz, Kok, and Quigley, 2013)."

The anchored version works because it connects to something the reader already knows. Good anchors include: known effects from prior literature, familiar policy changes, typical firm decisions, or household-scale equivalents.

## Related literature
- Do not dump a long neutral summary.
- Organize by disagreement, mechanism, method, or setting.
- State exactly how the present paper differs from the closest papers.

## Tables and figures
- Each should have a single reason to exist. If you cannot state it in one sentence, reconsider.
- Titles and notes should allow a reader to understand the object, sample, variables, and inference method without reading the text.
- Prefer clean, readable, economically interpretable displays over decorative visuals.
- Table notes should specify: dependent variable, sample, fixed effects, clustering, and observation count.

## Robustness discussion
- Name the threat, name the check, report the result, move on.
- Do not narrate every column of a robustness table.
- Group checks by category and summarize.
- If a check fails, discuss what it means rather than ignoring it.

## Discussion and conclusion
- Narrow the claim to what the design can support.
- Explain external validity limits and the conditions under which the result may not generalize.
- End with the economic lesson, not a generic restatement.

## Common failure modes
- Narrating columns instead of making economic arguments
- Vague contribution language or excessive throat-clearing
- Treating statistical significance as the economic result
- Excessive robustness discussion that obscures the main finding
- Hiding the identifying assumption or being vague about what FE absorb
- Claiming mechanism without addressing competing channels
- Using "consistent with" as a universal hedge without being specific

---

## Section-specific writing guidance

### Introduction
- Start with the contribution, not the literature (Cochrane: "put the punchline right up front").
- Three pages is a good upper limit (Cochrane).
- Omit or minimize roadmap paragraphs ("Section 2 sets out the model..."). The reader will figure it out (Cochrane). If included, limit to two sentences maximum.
- Do not start with philosophy ("Financial economists have long wondered...") or abstract literature gaps. Ground paragraph 1 in a concrete, recent event (see CLAUDE.md intro paragraph 1 rule).

### Literature review
- Place after the contribution is explained, not before. The reader cannot assess differentiation before understanding your paper.
- Focus on the 2-3 closest papers and give proper credit (Cochrane).
- Do not write a Journal of Economic Literature style review. Keep it targeted.
- Be generous in citations. You do not have to say everyone else did it wrong for your approach to be interesting.

### Data and methodology
- Describe what you do first, then explain why, then compare to alternatives (Cochrane: "first describe, then explain, then compare").
- Start with the main specification. Do not do warmup exercises, extensive description of well-known datasets, or preliminary estimates before the main result.
- The theory or model should be the minimum required for the reader to understand the empirical results. Do not write a "general" model and then specialize it.

### Results
- Start each results section with the main finding, not with table descriptions.
- Nothing should precede the main result that the reader does not need to understand the main result (Cochrane).
- Give stylized facts in the data that drive your result, not just estimates and p-values.
- Follow the main result with robustness, not the other way around.

### Robustness
- Summarize checks rather than narrating every column.
- Most robustness details belong in an appendix (Cochrane).
- If a check fails, discuss what it means rather than burying it.

### Conclusion
- Keep it short. Do not restate all findings (Cochrane: "one statement in the abstract, one in the introduction, once more in the body should be enough").
- A short paragraph acknowledging limitations and suggesting implications is appropriate.
- Do not speculate or write a grant application for future research.
- End with the economic lesson, not a generic restatement.

---

## Structural AI tells checklist

Use this checklist during revision to catch patterns that flag AI-generated text. These complement the structural tells listed in `references/banned-words.md`.

- [ ] **Paragraph opener variety**: No two consecutive paragraphs begin with the same grammatical construction. Vary: subject-verb, prepositional phrase, dependent clause.
- [ ] **Sentence length variation**: Mix short declarative sentences (8-12 words) with longer compounds (25-40 words). Five consecutive sentences of similar length is an AI tell.
- [ ] **Reflexive pronoun check**: Max 2 uses of "itself/themselves" per paper. When the pronoun adds emphasis but no semantic distinction, delete it.
- [ ] **Gerund density**: Max one gerund-phrase opener ("Using a large dataset, we...") per paragraph.
- [ ] **Meta-announcements**: Delete any sentence that announces the next topic without providing content ("We now turn to X"). Exception: one orienting sentence at section start if it names the specific question.
- [ ] **Enumeration overuse**: Max one "First...Second" structure per subsection. For causal chains, use prose.
- [ ] **Closing-summary paragraphs**: Do not end a section with a paragraph that merely restates. Summary belongs in Conclusion only.
- [ ] **Symmetric hedges**: Replace "can be positive or negative, depending on..." with the empirical answer when data exist.
- [ ] **Padding appositives**: Define a concept once. After definition, use the name without restating the definition.
- [ ] **Uniform paragraph length**: Vary paragraph length (some 2-sentence, some 6-sentence).

See also `references/banned-words.md` for the complete hard-ban and soft-ban word lists with empirical evidence.
