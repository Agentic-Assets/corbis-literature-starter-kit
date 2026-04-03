---
description: Panel data quality checks and safe lagging rules
---

Run the `panel-data-rules` skill for financial panel data work.

$ARGUMENTS

Key rules enforced:
1. **Safe lagging/leading**: Every `groupby().shift()` must have a date gap check with source-appropriate thresholds (CRSP monthly: 31 days, Compustat quarterly: 100 days, etc.).
2. **Accounting data timing**: Compustat 4-month availability lag, RDQ for earnings, staleness filters.
3. **CCM linking**: `lpermno` not `permno`, linktype LC/LU, null `linkenddt` sentinel handling.
4. **Stock universe filters**: Never apply by default -- present options and ask.
5. **Missing values**: Fill Compustat zeros per convention, NaN for invalid denominators.
6. **Book equity**: Davis-Fama-French hierarchy (SEQ -> CEQ+PSTK -> AT-LT).
7. **Winsorization**: Ask user first, never default.
8. **CRSP month-end normalization**: Always normalize dates before gap checks or merges.
