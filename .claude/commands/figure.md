Plan and generate publication-ready figures for: $ARGUMENTS

Use the `research-figure-design` skill. For the topic above:

1. Identify which figure types are needed (event study, parallel trends, binned scatter, coefficient plot, RD plot, time series, distributions, choropleth, cumulative returns, portfolio bars, Kaplan-Meier, heatmap, sample flow, mechanism diagram)
2. For each figure, specify: message, placement in paper, data requirements
3. Generate Python code using matplotlib with journal defaults (serif fonts, 300 DPI, 6.5x4.5 inches, PDF output)
4. Include figure notes following the template for each figure type
5. If market or macro context is needed, use Corbis tools (fred_series_batch, get_market_data)

Output: figure plan table + Python code for each figure + figure notes
