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
