# AI Usage Log

Keep this short and honest.

The point is not to confess that you used AI. Of course you used AI. The point is to show where it helped, what you trusted, and what you checked yourself.

## Log

| Date | Tool | What you used it for | What you verified yourself |
|---|---|---|---|
| YYYY-MM-DD | Claude / ChatGPT / Gemini / Copilot / other | Drafted a data-cleaning function | Re-ran the code, checked the output on 20 rows, fixed one wrong column mapping |
| 2026-05-24 | Claude | Task: Initial project scaffolding and data loading. Prompt summary: Asked Claude to write a function to parse a multi-sheet World Bank WDI Excel file into a tidy long-format panel, merging sheets on country_code and year. Output used: parse_sheet() and load_panel() functions (sections 1 of main.py). | Verification: Ran in Colab, printed row counts per sheet, confirmed against raw Excel file.|
| 2026-05-26 | Claude | Task: Feature engineering and cleaning. Prompt summary: Asked Claude to add YoY pct_change() derivation for GDP growth, signed-log transform for FDI, median imputation, and a row-drop rule for observations missing more than 2 features. Output used: clean_and_engineer() function (section 2 of main.py).| Verification: Checked fill counts and final panel shape against printed console output.|
| 2026-05-27| Claude | Task: Model selection pipeline and cross-validation. Prompt summary: Asked Claude to set up a 5-fold CV loop over Ridge, Random Forest, and Gradient Boosting, selecting the best by mean CV R². Output used: CANDIDATES dict and select_best_model() function (section 4 of main.py).| Verification: CV scores were printed and match the values reported in the report.|
| 2026-05-28| Claude | Task: Hypothesis test and stratified estimates. Prompt summary: Asked Claude to implement the above/below-median GDP growth split and the four-quartile descriptive table with standard errors. Output used: test_hypothesis() and stratified_estimates() (sections 6–7 of main.py). | Verification: Numbers checked against printed output; the implausible −31.5% median was noticed at this stage.|
| 2026-05-29| Claude | Task: Plotting. Prompt summary: Asked Claude to write the four matplotlib figures (actual vs predicted, residuals, feature importance bar, quartile bar with error caps). Output used: save_plots() function (section 8 of main.py).| Verification: Figures inspected visually in Colab.|
| 2026-05-30| Claude | Task: JSON output writers and main() orchestration. Prompt summary: Asked Claude to write the JSON serialisation functions and wire up the full main() function. Output used: write_json() and main() (sections 9 and MAIN of main.py).| Verification: Output JSON files opened and values confirmed against console output.|
| 2026-05-31| Claude | Task: JSON output writers and main() orchestration. Prompt summary: Asked Claude to write the JSON serialisation functions and wire up the full main() function. Output used: write_json() and main() (sections 9 and MAIN of main.py).| Verification: Output JSON files opened and values confirmed against console output.|
| 2026-06-01| Claude | Task: Responding to instructor feedback. Prompt summary: Asked Claude to (a) fix DATA_PATH from data/Book.xlsx to data/Unemployment.xlsx, (b) winsorise the GDP growth variable at the 5th/95th percentile and exclude first observations before the hypothesis test, (c) align REPORT.md metrics with the manifest, and (d) produce a real data source probe file. Output used: Revised main.py, REPORT.md, milestone_manifest.json, data_source_probe.md. | Verification: All changes reviewed line by line; numeric values in the report confirmed against the manifest JSON.|





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
