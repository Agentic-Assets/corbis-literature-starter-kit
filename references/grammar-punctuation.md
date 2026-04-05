# Grammar and Punctuation

> **Authority**: Chicago Manual of Style (CMS 17th ed.) as baseline. These conventions are standard across academic journals in economics and finance.

---

## Quick Reference

**Serial comma**: Always ("data, models, and results")
**Which/that**: "that" restricts (no commas); "which" adds info (commas)
**Semicolons**: Only between independent clauses
**Equation punctuation**: Equations are part of the sentence; punctuate accordingly
**Compound modifiers**: Hyphenate before nouns ("well-known result"); not after ("the result is well known")
**Numbers**: Spell out one through nine; digits for 10+; always digits with units or statistics
**Latin phrases**: Do NOT italicize (standard academic style): "ex post" not "\textit{ex post}"

---

## 1. Comma Rules

### Serial (Oxford) Comma
Always use in lists of three or more:
- Good: "momentum, value, and reversal"
- Bad: "momentum, value and reversal"

### Restrictive vs Nonrestrictive Clauses
| Clause type | Pronoun | Commas | Example |
|-------------|---------|--------|---------|
| Restrictive (essential) | **that** | No | "Bonds that trade frequently have lower spreads." |
| Nonrestrictive (extra info) | **which** | Yes | "Corporate bonds, which trade OTC, have higher spreads." |

**Test**: Remove the clause. If the sentence changes meaning, it is restrictive (use "that", no commas). If the sentence still makes sense, it is nonrestrictive (use "which", add commas).

### Introductory Elements
Comma after introductory phrases of four or more words, dependent clauses, and transitional words:
- "After adjusting for measurement error, the premium falls to zero."
- "However, the result does not hold in investment-grade bonds."
- Short prepositional phrases (under four words) may omit: "In Table 3 the coefficients are..."

### Comma Before "and" Joining Independent Clauses
Use a comma before coordinating conjunctions (and, but, or, yet) joining two independent clauses:
- "The premium vanishes after adjustment, and the t-statistic falls below 1.65."

Do NOT use a comma when the second element is not an independent clause:
- "The premium vanishes after adjustment and falls below significance."

---

## 2. Semicolons and Colons

### Semicolons
Use ONLY to join two **complete independent clauses** that are closely related:
- Good: "The bias is 91% for reversal; it is 47% for value."
- Bad: "The bias is 91% for reversal; which is the largest in our sample." (dependent clause)

Use before conjunctive adverbs (however, therefore, moreover) joining independent clauses:
- "Short-term reversal has the largest bias; however, this reflects high $\rho$, not a theoretical prediction."

Use in complex lists where items contain internal commas:
- "We examine momentum (Jostova et al., 2013); idiosyncratic volatility (Bai, Bali, and Wen, 2019); and credit spreads."

### Colons
Use after an independent clause to introduce an explanation, list, or elaboration:
- Good: "The results point to one conclusion: most anomalies are artifacts."
- Bad: "The three biases are: LIB, LAB, and NSE." (no colon after "are")

**Rule**: Never place a colon after a verb or preposition that grammatically connects to what follows.

---

## 3. Compound Modifier Hyphenation

### Before a Noun: Hyphenate
- "well-known result", "long-short portfolio", "cross-sectional regression"
- "high-yield bonds", "within-firm sort", "signal-adjusted return"

### After a Verb: Do Not Hyphenate
- "The result is well known." (not "well-known")
- "The portfolio is long short." (not "long-short")

### Adverb + Adjective: Do Not Hyphenate (Standard Academic Style)
When the first word is an adverb ending in -ly, never hyphenate:
- "actively managed fund" (not "actively-managed")
- "statistically significant result" (not "statistically-significant")
- "newly issued bonds" (not "newly-issued")

### Permanent Compounds
Some compounds are always hyphenated regardless of position: "well-being", "self-selection", "re-examine".

---

## 4. Equation Punctuation

Displayed equations are part of the sentence. Punctuate them as if the equation were a word:

```latex
% Equation ending a sentence — period after:
The bias equals
\begin{equation}
  \text{Bias} = 2\kappa\rho\sigma_\delta.
\end{equation}

% Equation mid-sentence — comma after:
Given the decomposition
\begin{equation}
  \hat{r}_{i,t+1} = r_{i,t+1} + \epsilon_{i,t+1},
\end{equation}
where $\epsilon_{i,t+1}$ is the return measurement error.

% Equation followed by conditions — no punctuation or comma:
Under Assumption~\ref{assum:iid},
\begin{equation}
  \Cov(\delta_{i,t-\Delta}, \delta_{i,t}) = 0
\end{equation}
for all $\Delta \geq 1$.
```

**Test**: Read the sentence aloud, replacing the equation with "blah." If you would pause for a comma or stop for a period, add the punctuation to the equation.

---

## 5. Abbreviations in Running Text (Standard Academic Style)

### Spell Out in Text, Abbreviate in Parentheses

| In running text | In parentheses |
|----------------|---------------|
| "See, for example, Smith (2020)" | "(see, e.g., Smith (2020))" |
| "..., that is, the bias vanishes" | "(i.e., the bias vanishes)" |

Never use "e.g." or "i.e." in running text without parentheses.

### Percentage
Use the % symbol, not the word "percent" (standard academic style):
- "The bias is 91%." (not "91 percent")

---

## 6. Latin Phrases (Standard Academic Style)

**Do NOT italicize Latin** in academic submissions:
- "ex post" not "\textit{ex post}"
- "ex ante" not "\textit{ex ante}"
- "ceteris paribus" not "\textit{ceteris paribus}"

**Note**: `latex-conventions.md` has been updated to match (see its Common LaTeX Patterns section).

---

## 7. Possessives

### Names Ending in S: Add 's (CMS Standard)
- "Keynes's General Theory", "Fama and French's model"
- "Dickerson, Mueller, and Robotti's framework"

### Abbreviations: Plural vs Possessive
| Form | Example |
|------|---------|
| Plural | "GMMs", "CAPMs", "OLS estimates" |
| Possessive | "the CAPM's predictions", "the AEA's guidelines" |

No apostrophe for plurals. Apostrophe + s for possessives.

---

## 8. Commonly Confused Words

| Word | Meaning | Example |
|------|---------|---------|
| **that** | restrictive clause | "Bonds that trade frequently..." |
| **which** | nonrestrictive clause | "Bonds, which trade OTC,..." |
| **affect** (verb) | influence | "Measurement error affects the premium." |
| **effect** (noun) | result | "The effect of measurement error is large." |
| **effect** (verb) | bring about (rare) | "to effect a change" |
| **comprise** | consist of (whole comprises parts) | "The factor zoo comprises 108 signals." |
| **compose** | make up (parts compose whole) | "108 signals compose the factor zoo." |
| **between** | two items | "between investment-grade and high-yield" |
| **among** | three or more | "among the nine signal clusters" |
| **fewer** | countable | "fewer bonds", "fewer factors" |
| **less** | uncountable | "less liquidity", "less bias" |
| **ensure** | make certain | "to ensure robustness" |
| **insure** | financial coverage | (avoid in academic writing unless literal) |

---

## 9. Dangling Modifiers

The subject of the main clause must be the agent of the introductory modifier:

- Bad: "Using a signal gap of five days, the bias is reduced." (the bias didn't use the gap)
- Good: "Using a signal gap of five days, we reduce the bias."
- Bad: "After filtering extreme returns, the sample contains 52,656 bonds." (the sample didn't filter)
- Good: "After we filter extreme returns, the sample contains 52,656 bonds."

---

## 10. Parallel Structure

Items in a list or series must share the same grammatical form:

- Bad: "We (i) compute returns, (ii) sorting bonds into portfolios, and (iii) the alphas are estimated."
- Good: "We (i) compute returns, (ii) sort bonds into portfolios, and (iii) estimate alphas."

This applies to bullet points, enumerated lists, and items joined by correlative conjunctions (both...and, either...or, neither...nor, not only...but also).

---

## 11. Sentence Boundaries

### Do Not Start a Sentence with a Variable (Standard Academic Style)
- Bad: "$\rho$ controls the noise share."
- Good: "The noise share $\rho$ controls..."

### Run-On Sentences
Two independent clauses cannot be joined by a comma alone (comma splice):
- Bad: "The premium vanishes, the t-statistic falls below 1.65."
- Good: "The premium vanishes, and the t-statistic falls below 1.65."
- Good: "The premium vanishes; the t-statistic falls below 1.65."
- Good: "The premium vanishes. The t-statistic falls below 1.65."

---

## 12. Number Formatting

Spell out **one through nine**; use digits for **10 and above** (CMS):
- "three approaches", "nine clusters", "108 signals", "52,656 bonds"

Always use **digits** with units, statistics, or technical quantities:
- "5 days", "3%", "a $t$-statistic of 2.3", "quintile 1", "top 30%"

Spell out a number that starts a sentence, or restructure to avoid it:
- Bad: "108 signals span nine clusters."  (fine — 108 is mid-sentence)
- Bad: "3 approaches are compared." → "Three approaches are compared." or "We compare three approaches."

Use the **% symbol**, not the word "percent" (standard academic style). Use **commas** as thousands separators: "52,656" not "52656".

**Date ranges in text**: "1980 to 1990" (standard academic style). In tables: "1980--1990" is acceptable.

---

## 13. Quotation Marks

Use **double quotes** (American/CMS convention). In LaTeX, use `` ` `` ` `` and `''` (backticks and apostrophes), never straight quotes.

**Punctuation placement** (CMS American style):
- Periods and commas go **inside** closing quotes: We call this "look-ahead bias."
- Colons and semicolons go **outside**: The authors define "LIB"; however, they do not test it.

**Introducing terms**: Use quotes on first use to flag a new term, then drop them:
- First use: We call this bias "latent implementation bias" (LIB).
- Subsequent: The LIB adjustment reduces the premium by 90 basis points.

Single quotes only for quotes within quotes: He noted that "the so-called 'momentum effect' vanishes."

---

## Sources

- **Chicago Manual of Style**, 17th ed. (2017). Baseline for academic writing.
- **Journal of Finance Style Guidelines** (Feb 2017). Referenced for academic writing conventions.
- **Cochrane, J.** (2005). "Writing Tips for Ph.D. Students." Equation punctuation, concision.
- **Dupré, L.** (1998). *BUGS in Writing*. Compound modifiers, dangling modifiers, parallel structure.
