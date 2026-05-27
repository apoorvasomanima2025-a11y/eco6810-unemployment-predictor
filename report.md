# Final Report

Use this as the default shape. Keep it tight. The report should match what the code actually produced.

## 1. Question

What question did you ask, who cares about the answer, and what decision does it inform?
- What is the question?
Can a set of country-level macroeconomic and structural indicators — GDP per capita, GDP per capita growth, inflation, industry value added, trade openness, FDI inflows, labour force participation, urban population share, school enrolment, and total population — predict a country's unemployment rate in the same year?
- Who cares?
The International Labour Organization (ILO) Employment Policy Department, which advises member governments on labour market intervention. When a country's macro conditions shift, finance ministries need to anticipate unemployment pressure before it appears in costly household surveys — so they can pre-emptively allocate job-guarantee funding, training budgets, or unemployment insurance.
- What decision does it inform?
Whether a country's observed unemployment rate is anomalously high or low relative to what its macro fundamentals would predict — flagging cases that warrant closer policy attention.
## 2. Charter Summary

- Project type: Predictive
- Main metric: Out-of-sample R² on a randomly held-out 20% test set
- Success threshold: R² ≥ 0.45
- Baseline: Mean-prediction null model: predict the training-set mean (8.02%) for every observation

## 3. Data

List the main sources you used. Say how you accessed them. If a source changed or failed, say what you did instead.
Source: World Bank World Development Indicators (WDI), downloaded 2026-04-08.
Access method: Direct bulk download as data/Book.xlsx; no API call or login required at runtime. The file is committed to the repo under data/ with a CC BY 4.0 licence note.
Seven indicators were used:

 Sheet                Indicator                                     WB Code 
 - Unemployment     Unemployment rate, total (% of labour force)  SL.UEM.TOTL.ZS
 - GDP Per Cap      GDP per capita growth (annual %)             NY.GDP.PCAP.CD 
 - Inflation       CPI inflation (annual %)                      FP.CPI.TOTL.ZG 
 - Trade           Trade openness (% of G                        NE.TRD.GNFS.ZS
 - FDI             FDI net inflows (BoP, current USD)           BX.KLT.DINV.CD.WD
 - Labour Force    Labour force participation rate (%)           SL.TLF.ACTI.ZS  
 - Urban Pop        Urban population (% of total)                SP.URB.TOTL.IN.Z 
 - School           School enrollment, tertiary (% gross)        SE.TER.ENRR
 - Population Total  Population growth (annual %)                SP.POP.GROW
 - Industry          Industry value added (% of GDP)             NV.IND.TOTL.ZS
   
gdp_per_capita_growth (the variable in the falsifiable hypothesis) is derived in code as the year-on-year percentage change of gdp_per_capita within each country — it is not fetched separately.
No source failed. All ten sheets were present and parseable in the downloaded file. World Bank aggregate and regional rows (e.g. WLD, HIC, SSA) were excluded using a fixed exclusion list; only sovereign country rows were retained.
Panel construction: The outcome variable (Unemployment, 4,484 obs, 187 countries) anchors the merge. All other sheets are joined on country_code and year via an outer merge, then rows missing the outcome are dropped, giving a starting panel of 4,484 rows across 187 countries for 2000–2023. After dropping 115 rows with more than 2 missing features, the final clean panel contains 4,369 country-year observations across 185 countries. Remaining missing values were filled with each column's global median before modelling (largest fill: 438 values in trade openness).

## 4. Method

Explain the baseline first. Then explain the main analysis. Keep it readable. If you used a causal design, state the assumptions. If you used a predictive model, state the evaluation split. If you used a descriptive design, state the comparison structure and sample discipline.

Baseline
The null model predicts the training-set mean unemployment rate — 8.02% — for every observation in the test set, regardless of any feature values. This produces an out-of-sample R² of approximately 0.00 by construction. Any model that learns from the features must beat this.
Main analysis
The panel was split 80/20 into train (3,495 obs) and test (874 obs) sets using a random split with seed 42. The split is across country-year observations, not along a time boundary, so the test set contains real country-years the model has never seen.
Three candidate models were evaluated by 5-fold cross-validation on the training set:

- Model                   CV R² (mean ± std)
-  Ridge Regression        0.138 ± 0.065
-  Gradient Boosting       0.488 ± 0.014
-  Random Forest           0.515 ± 0.022

Random Forest was selected as the best model. It was then re-trained on the full training set and evaluated once on the held-out test set to produce the primary metric.
FDI inflows were sign-log transformed before modelling (signed log₁p) to handle the heavy right skew and occasional negative values from FDI reversals. All other features were used as-is after median imputation.
## 5. Result

- Main metric value:
-  Out-of-sample R²: 0.514
- Threshold: 0.45
- Passed: Yes
- MAE:  2.83 percentage points
- RMSE: 4.01 percentage points
- Baseline R² : −0.0002

Give the main number first. Then interpret it in plain English.
The Random Forest model explains approximately 51% of the cross-country variation in unemployment rates on data it was never trained on. In practical terms, the model's average prediction error is 2.83 percentage points — so for a country with a true unemployment rate of 8%, a typical prediction lands between 5.2% and 10.8%. That is meaningful accuracy given that the features include no country fixed effects and no historical unemployment lags.
The improvement over baseline is large and unambiguous: the baseline R² is essentially zero (−0.0002), while the model R² is 0.514.
## 6. Evidence

Point to the figures, tables, regressions, or diagnostics that support the result.

Figure 1 — Actual vs Predicted (outputs/figures/actual_vs_predicted.png)
Points cluster reasonably close to the 45° line across the full range of unemployment rates (0–37%). Predictions are tighter in the 0–15% range where most countries sit, and more dispersed for high-unemployment outliers above 25%.
Figure 2 — Residual distribution (outputs/figures/residuals.png)
Residuals are centred near zero and roughly symmetric, with the bulk within ±5 percentage points. A modest right tail reflects underprediction of a small number of very high unemployment country-years.
Figure 3 — Feature importance (outputs/figures/feature_importance.png)
Labour force participation rate and urban population share are the two dominant features, together accounting for the majority of predictive signal. Trade openness is third. GDP per capita level and growth carry relatively little weight individually. Inflation, FDI, industry value added, school enrolment, and population contribute the remainder.
Table 1 — Stratified unemployment by GDP per capita quartile

- GDP per capita quartile    n     Mean   unemployment (%)SE                     - Q1 (lowest)             1,093   8.50     0.185
- Q2                      1,101   7.59     0.170
- Q3                      1,083   7.99     0.188
- Q4 (highest)            1,090   7.90     0.179
Standard errors are documented for all four strata as required by the descriptive component of the charter. The pattern is non-monotonic — Q1 has the highest mean unemployment, Q2 the lowest, with Q3 and Q4 in between — which is consistent with the absence of a simple linear income–unemployment gradient in cross-country data.

## 7. Limits

What can this project say with confidence, and what can it not say?

What this project can say with confidence:

Labour force participation and urbanisation together account for the majority of cross-country predictive power for unemployment in this dataset.
A Random Forest trained on ten macro and structural indicators explains roughly half the cross-country variation in unemployment on unseen data.
The predictive relationship is stable: CV R² (0.515) and test R² (0.514) are within 0.001 of each other, indicating no meaningful overfitting.

What this project cannot say:

These are predictive associations, not causal effects. We cannot say that raising labour force participation causes unemployment to fall.
The model captures cross-country and year-to-year variation jointly. It does not control for country fixed effects, so some of the signal may reflect persistent structural differences between countries rather than within-country dynamics.
The panel uses the World Bank's modelled ILO unemployment estimates, which smooth over differences in how countries define and measure unemployment. Results may not generalise to national statistical definitions.
The model was not tested on data beyond 2023.

## 8. If The Result Was Null Or Weak

Say so directly. Do not force a story onto the data.

The primary metric passed (R² = 0.514 ≥ 0.45), so the predictive result is not null.
However, the falsifiable hypothesis was not supported. The charter predicted that countries with above-median GDP per capita growth would have unemployment rates at least 1.5 percentage points lower than countries with below-median growth.
GDP per capita growth variable — fix applied: The raw pct_change() derivation produces extreme values for the first observation per country (where no prior year exists in the panel) and for countries with structural GDP revisions or currency rebasings. In the original code these extreme values dragged the global median to −31.5%, making the above/below-median split meaningless — both groups ended up with unemployment near 8.00%.
The fix: first observations per country (where pct_change() returns NaN) are excluded before computing the median, and the remaining values are winsorised at the 5th and 95th percentiles to remove rebase artifacts. With this clean variable the median GDP-per-capita growth is a plausible positive figure, and the hypothesis test is a meaningful comparison of genuinely high-growth versus low-growth country-years.
Even after the fix, the hypothesis is not supported: the observed unemployment difference between growth groups remains well below the 1.5 pp threshold. This is reported directly and without adjustment. The overall model still predicts well (R² = 0.549), but Okun's Law, as operationalised with this cross-country panel, does not hold with the expected magnitude.

## 9. Reproducibility

- Run command: uv run main.py
- Runtime: ~25–35 seconds on a standard laptop (no internet required)
- Data dependency: data/Book.xlsx must be present in the repo (committed)
- Output files written:
outputs/primary_metric.json
outputs/baseline_metric.json
outputs/milestone_manifest.json
outputs/figures/actual_vs_predicted.png
outputs/figures/residuals.png
outputs/figures/feature_importance.png
outputs/figures/unemployment_by_gdp_quartile.png

## 10. AI Usage

Summarize the main places AI helped and what the team checked manually. Point to [AI_USAGE_LOG.md](./AI_USAGE_LOG.md) for the detailed log.

Summary: Claude was used for code generation throughout the project. All code was run on Google Colab and outputs were verified against the actual printed console output and JSON files. The hypothesis null result, the median anomaly explanation, and the feature importance interpretation were written based on the actual numbers — not accepted from AI output without checking.
