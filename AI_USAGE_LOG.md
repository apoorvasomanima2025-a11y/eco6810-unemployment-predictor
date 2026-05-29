# AI Usage Log

Keep this short and honest.

The point is not to confess that you used AI. Of course you used AI. The point is to show where it helped, what you trusted, and what you checked yourself.

## Log

| Date | Tool | What you used it for | What you verified yourself |
|---|---|---|---|
| YYYY-MM-DD | Claude / ChatGPT / Gemini / Copilot / other | Drafted a data-cleaning function | Re-ran the code, checked the output on 20 rows, fixed one wrong column mapping |
| 2026-05-24 | Claude | Asked for a starting template to read a multi-sheet World Bank Excel file into a tidy long-format panel. It suggested using pd.read_excel with header=3 and a melt() call. | Opened the actual workbook, confirmed the header is on row 4 (index 3), checked that row counts per sheet matched what the WDI portal shows. Fixed the column rename — Claude used "Country Code" but the sheet had a trailing space; caught that by printing df.columns.|
| 2026-05-25 | Claude | Asked for a one-liner to sign-log transform FDI inflows.| Checked a sample of negative FDI values (reversals) by hand to confirm the transform preserves sign and handles zero correctly. Verified the distribution before and after in a histogram.|
| 2026-05-26| Claude | Asked it to sketch a 5-fold CV loop structure for three sklearn estimators.| Re-read the sklearn docs on cross_val_score to confirm scoring="r2" returns the correct sign convention. Ran the loop myself and compared CV scores against a manual train/val split to sanity-check.|
| 2026-05-27| Claude | Asked it to suggest matplotlib code for a horizontal bar chart of feature importances. | Inspected the actual feature_importances_ array printed from the fitted model. The bar ordering in Claude's suggestion was ascending; changed it to descending to match standard presentation. Labels were generic — replaced with the actual WDI indicator names.|
| 2026-05-28| Claude | Asked for help spotting why the hypothesis median was −31.28%. It flagged that pct_change() on levels produces NaN and extreme values for the first observation per country.| Traced this myself in a Colab cell: printed panel.groupby("country_code")["gdp_per_capita_growth"].head(2) and confirmed the first row per country was always NaN or extreme. Decided to fix it by reading NY.GDP.PCAP.KD.ZG directly from the WDI sheet instead of deriving growth from levels — Claude did not suggest this fix; I worked it out from reading the sheet indicator codes.|
| 2026-05-29| Claude | Asked it to regenerate the JSON manifest template after the 10-indicator rewrite.| Compared every field against the actual console output line by line. Corrected n_obs_total, n_train, n_test, and baseline_r2 which did not match the printed run.|

## Things To Avoid

- "used AI for coding"
- "used ChatGPT for analysis"
- "AI helped with debugging"

What was NOT taken from AI without verification

The hypothesis null result and its interpretation were written after checking the actual printed median value (−31.5% in the original code).
The explanation of the pct_change artifact was reasoned through independently and then confirmed with Claude as a consistency check.
Feature importance rankings were read directly from the printed console output, not from Claude's suggested narrative.
All metric values in the report (R², MAE, RMSE) were copied from the actual JSON output files, not from AI-generated text.

## Better

- "Claude suggested the first version of the FRED fetch helper; we changed the parsing after checking the missing-value handling"
- "ChatGPT proposed a DiD specification; we kept the controls but rewrote the treatment definition after reading the data"
- "Gemini rewrote the report summary; we replaced two claims that overstated causality"
