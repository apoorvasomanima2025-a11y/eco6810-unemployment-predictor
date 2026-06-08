# AI Usage Log

Keep this short and honest.

The point is not to confess that you used AI. Of course you used AI. The point is to show where it helped, what you trusted, and what you checked yourself.

## Log

| Date | Tool | What you used it for | What you verified yourself |
|---|---|---|---|
| YYYY-MM-DD | Claude / ChatGPT / Gemini / Copilot / other | Drafted a data-cleaning function | Re-ran the code, checked the output on 20 rows, fixed one wrong column mapping |
| 2026-05-24 | Claude | AAsked for a starting template to read a multi-sheet World Bank Excel file into a tidy long-format panel — specifically pd.read_excel with header=3 and a melt() call. | Opened the actual workbook and confirmed the header sits on row 4 (index 3). Checked printed row counts per sheet against the WDI portal. Found and fixed a column rename issue: the sheet had a trailing space in "Country Code" that Claude's template missed — caught by printing df.columns.|
| 2026-05-25 | Claude | Asked for a one-liner to sign-log transform FDI inflows to handle zeros and negative reversal values.| Sampled five negative FDI rows by hand to confirm the transform preserves sign and handles zero correctly. Plotted the distribution before and after to confirm skew reduction.|
| 2026-05-26| Claude | Asked it to outline a 5-fold CV loop for three sklearn estimators (Ridge, Random Forest, Gradient Boosting).| Re-read the sklearn docs on cross_val_score to confirm scoring="r2" uses the correct sign convention. Ran the loop and spot-checked one fold manually to confirm the scores were plausible.|
| 2026-05-27| Claude | Asked it to suggest matplotlib code for a horizontal bar chart of feature importances. | Pulled the actual feature_importances_ array from the fitted model and confirmed values myself. Claude's version ordered bars ascending — changed to ascending-toward-top so the longest bar appears at the top. Replaced generic feature names with actual WDI indicator labels.|
| 2026-05-28| Claude | Asked for help understanding why the hypothesis median was −31.28%. Claude identified that pct_change() on GDP levels returns NaN for the first country-year and extreme values for rebasings.| Traced it in Colab by printing panel.groupby("country_code")["gdp_per_capita_growth"].head(2) — confirmed first obs per country was always NaN or implausible. The fix — reading NY.GDP.PCAP.KD.ZG directly from the WDI sheet instead of deriving growth from levels — was my own decision after reading the sheet's indicator code. Claude did not suggest it. New median after fix: 2.21%.|
| 2026-05-29| Claude | Asked it to regenerate the JSON manifest skeleton after expanding from 7 to 10 indicators.| Compared every field against the actual console output line by line. Found and corrected n_countries (185→183), n_obs_total (4,369→4,333), n_train (3,495→3,466), n_test (874→867), and baseline_r2. Added the cleaning block with exact median fills — school enrollment (1,410 filled) was absent from the first draft.|

## Things To Avoid

- "used AI for coding"
- "used ChatGPT for analysis"
- "AI helped with debugging"

What was NOT taken from AI without verification

The decision to add temporal validation, and the framing of the 2020 COVID shock as the reason for the R² drop (0.68 → 0.36), was made independently after reading the instructor feedback — not suggested by Claude.
The economic interpretation — that Okun's Law is a within-country time-series relationship that does not replicate in cross-section — was written from first principles after seeing the −0.29 pp hypothesis result.
Claude was not asked to interpret this.
The final R² of 0.6841, MAE 2.34 pp, temporal R² 0.3612, and all stratified estimates were copied from the console output and JSON files, not from AI-generated text.
The ranking of features (labour force part. → urban pop. → population growth) was read from the bar chart and importance tables, verified across all three methods, not from any AI summary.
The choice of Random Forest over Gradient Boosting was based on comparing CV R² numbers (0.6482 vs 0.6287) in the console.
## Better

- "Claude suggested the first version of the FRED fetch helper; we changed the parsing after checking the missing-value handling"
- "ChatGPT proposed a DiD specification; we kept the controls but rewrote the treatment definition after reading the data"
- "Gemini rewrote the report summary; we replaced two claims that overstated causality"
