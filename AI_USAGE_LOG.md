# AI Usage Log

Keep this short and honest.

The point is not to confess that you used AI. Of course you used AI. The point is to show where it helped, what you trusted, and what you checked yourself.

## Log

| Date | Tool | What you used it for | What you verified yourself |
|---|---|---|---|
| YYYY-MM-DD | Claude / ChatGPT / Gemini / Copilot / other | Drafted a data-cleaning function | Re-ran the code, checked the output on 20 rows, fixed one wrong column mapping |
| 2026-05-24 | Claude | Implemented the gdp_per_capita_growth derivation (pct_change within country groups) in response to professor feedback about the hypothesis–data-source mismatch | Checked the derived column for 5 countries manually; noticed the median of −31.6% was anomalous; traced this to missing prior-year values producing extreme first-observation pct_change values; documented this honestly in Section 8 of the report|
| 2026-05-26 | Claude | Generated the 4 matplotlib figures (actual vs predicted, residuals, feature importance, quartile bar chart)| Opened each PNG and verified axis labels, units, and that the feature importance bar chart matched the values in milestone_manifest.json|
| 2026-05-31| Claude | Drafted REPORT.md using the actual output numbers from primary_metric.json, baseline_metric.json, and milestone_manifest.json| Checked every number in the report against the JSON files; rewrote the hypothesis null-result paragraph (Section 8) because the first draft understated the severity of the median anomaly; verified the feature importance percentages sum to ~1.0 (they do: 0.380 + 0.317 + 0.137 + 0.065 + 0.057 + 0.029 + 0.017 = 1.002, rounding)|



## Things To Avoid

- "used AI for coding"
- "used ChatGPT for analysis"
- "AI helped with debugging"

Those lines are too vague to be useful.

- The decision to use data/Book.xlsx instead of the API (made after confirming network access was restricted)
- The observation that the hypothesis median split was distorted by first-observation pct_change values — this was noticed by reading the printed output (median_gdppc_growth_pct: -31.55) and reasoning about why it was implausible
- The exclusion of 2024–2025 columns from the panel (confirmed by checking the actual R² drop when those years were included with their sparse data)
- The final feature importance interpretation: that labour force participation and urbanisation dominate because they capture structural cross-country differences, not short-run macro shocks — this inference was made from the numbers, not from AI explanation

## Better

- "Claude suggested the first version of the FRED fetch helper; we changed the parsing after checking the missing-value handling"
- "ChatGPT proposed a DiD specification; we kept the controls but rewrote the treatment definition after reading the data"
- "Gemini rewrote the report summary; we replaced two claims that overstated causality"
