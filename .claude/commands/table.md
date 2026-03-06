---
description: Generate a LaTeX regression table from specifications
---

Using the `python-empirical-code` skill, generate a publication-ready LaTeX regression table.

$ARGUMENTS

Requirements:
- t-statistics in parentheses below coefficients (not standard errors)
- Significance stars: *** p<0.01, ** p<0.05, * p<0.10
- Table note stating "t-statistics in parentheses" and the clustering level
- Fixed effects indicators (Yes/No rows)
- Observations and Adjusted R-squared
- Compatible with the `latex_template/` format (uses `\sym{}` macro, `booktabs`, `tabularx`)

If the user provides regression output or data, generate the complete Python code to produce the table. If the user provides a description, generate the LaTeX table directly.
