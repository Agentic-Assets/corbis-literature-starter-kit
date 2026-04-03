---
description: Load WRDS schema knowledge
---

Run the `wrds-schema` skill to pre-load schema knowledge before writing queries.

**Databases**: $ARGUMENTS (options: crsp, optionm, comp, jkp, all; default: all)

Workflow:
1. For each requested database, query WRDS to retrieve current table structures.
2. Compile results into a compact Schema Reference (table names, key columns, data types, date ranges).
3. Include known gotchas (Decimal types, column naming, strike_price scaling, Compustat filters).

This eliminates exploratory round-trips and prevents column-name errors.
