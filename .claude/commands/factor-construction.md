---
description: Factor construction audit for look-ahead bias
---

Run the `factor-construction` skill to audit or construct factors.

$ARGUMENTS

Steps:
1. Run the LAB (look-ahead bias) audit checklist: signal timing, universe definition, breakpoints, return alignment, output dating.
2. If constructing a new factor: use the monthly or annual rebalancing template with gap checks and proper date alignment.
3. Confirm breakpoint convention with user (all-stock quantiles vs NYSE-only).
4. After construction, run post-construction diagnostics: monotonicity, t-statistics, portfolio sizes, date coverage, benchmark correlation.
5. Flag any look-ahead bias violations.
