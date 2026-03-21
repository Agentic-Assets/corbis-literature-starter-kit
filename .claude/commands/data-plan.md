---
description: Plan data sourcing, merges, and variable construction
---

Run the `finance-data-construction` skill for this project:

$ARGUMENTS

Produce:
1. Raw data sources with access paths and vintage dates
2. Join logic with keys and expected match rates
3. Sample flow diagram with observation counts at each filter stage
4. Core variable definitions with exact formulas
5. Identifier mapping plan with known pitfalls
6. Missingness, outlier, and winsorization rules (with justification)
7. Reproducible folder and script architecture
8. FRED series needed (use `fred_search` to identify)
9. Data appendix outline

Use `search_datasets` to discover available data. Read `references/wrds-recipes.md` for WRDS table schemas, standard queries, identifier crosswalk, and known data gotchas per database.
