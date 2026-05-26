# Final Report

Use this as the default shape. Keep it tight. The report should match what the code actually produced.

## 1. Question

What question did you ask, who cares about the answer, and what decision does it inform?
What is the question?
Can a small set of country-level macroeconomic indicators — GDP per capita growth, inflation, trade openness, FDI inflows, tertiary school enrollment, labour force participation, total population, and urban population share — predict a country's unemployment rate in the same year?
Who cares?
The International Labour Organization (ILO) Employment Policy Department, which advises member governments on labour market intervention. When a country's macro conditions shift, finance ministries need to anticipate unemployment pressure before it appears in costly household surveys — so they can pre-emptively allocate job-guarantee funding, training budgets, or unemployment insurance.
What decision does it inform?
Whether a country's observed unemployment rate is anomalously high or low relative to what its macro fundamentals would predict — flagging cases that warrant closer policy attention.
## 2. Charter Summary

- Project type: Predictive
- Main metric: Out-of-sample R² on a randomly held-out 20% test set
- Success threshold: R² ≥ 0.45
- Baseline: Mean-prediction null model: predict the training-set mean (8.01%) for every observation

## 3. Data

List the main sources you used. Say how you accessed them. If a source changed or failed, say what you did instead.
Source: World Bank World Development Indicators (WDI), downloaded 2026-04-08.
Access method: Direct bulk download as data/Book.xlsx; no API call or login required at runtime. The file is committed to the repo under data/ with a CC BY 4.0 licence note.
Seven indicators were used:

Sheet               Indicator                                 WB Code
Unemployment  Unemployment rate, total (% of labour force)  SL.UEM.TOTL.ZS
GDP Per Cap   GDP per capita (current USD)                  NY.GDP.PCAP.CD
Inflation     CPI inflation (annual %)                      FP.CPI.TOTL.ZG
Trade         Trade openness (% of GDP)                     NE.TRD.GNFS.ZS        FDI           FDI net inflows (BoP, current USD)            BX.KLT.DINV.CD.WD Labour Force  Labour force participation rate (%)S          L.TLF.ACTI.ZS    Urban Pop     Urban population (% of total)                 SP.URB.TOTL.IN.Z

gdp_per_capita_growth (the variable in the falsifiable hypothesis) is derived in code as the year-on-year percentage change of gdp_per_capita within each country — it is not fetched separately.
No source failed. All seven sheets were present and parseable in the downloaded file. World Bank aggregate and regional rows (e.g. WLD, HIC, SSA) were excluded using a fixed exclusion list; only sovereign country rows were retained.
Panel after cleaning: 4,358 country-year observations across 185 countries, 2000–2023.
126 rows dropped for having more than 2 missing features. Remaining missing values (at most 438 in a single column) were filled with the column's global median before modelling.

## 4. Method

Explain the baseline first. Then explain the main analysis. Keep it readable. If you used a causal design, state the assumptions. If you used a predictive model, state the evaluation split. If you used a descriptive design, state the comparison structure and sample discipline.

Baseline
The null model predicts the training-set mean unemployment rate — 8.01% — for every observation in the test set, regardless of any feature values. This produces an out-of-sample R² of approximately 0.00 by construction. Any model that learns from the features must beat this.
Main analysis
The panel was split 80/20 into train (3,486 obs) and test (872 obs) sets using a random split with seed 42. The split is across country-year observations, not along a time boundary, so the test set contains real country-years the model has never seen.
Three candidate models were evaluated by 5-fold cross-validation on the training set:

Model                   CV R² (mean ± std)                                        Ridge Regression        0.170 ± 0.018                                      Gradient Boosting       0.468 ± 0.029Random                                  Forest                  0.508 ± 0.028

Random Forest was selected as the best model. It was then re-trained on the full training set and evaluated once on the held-out test set to produce the primary metric.
FDI inflows were sign-log transformed before modelling (signed log₁p) to handle the heavy right skew and occasional negative values from FDI reversals. All other features were used as-is after median imputation.
## 5. Result

- Main metric value: Out-of-sample R²0.549
- Threshold: 0.45
- Passed: Yes
- MAE:  2.77 percentage points
- RMSE: 3.93 percentage points
- Baseline R² : −0.001

Give the main number first. Then interpret it in plain English.
The Random Forest model explains approximately 55% of the cross-country variation in unemployment rates on data it was never trained on. In practical terms, the model's average prediction error is 2.77 percentage points — so for a country with a true unemployment rate of 8%, a typical prediction lands between 5.2% and 10.8%. That is meaningful accuracy given that the features include no country fixed effects and no historical unemployment lags.
The improvement over baseline is large and unambiguous: the baseline R² is essentially zero (−0.001), while the model R² is 0.549.

## 6. Evidence

Point to the figures, tables, regressions, or diagnostics that support the result.

Figure 1 — Actual vs Predicted (outputs/figures/actual_vs_predicted.png)
Points cluster reasonably close to the 45° line across the full range of unemployment rates (0–37%). Predictions are tighter in the 0–15% range where most countries sit, and more dispersed for high-unemployment outliers above 25%.
Figure 2 — Residual distribution (outputs/figures/residuals.png)
Residuals are centred near zero and roughly symmetric, with the bulk within ±5 percentage points. A modest right tail reflects underprediction of a small number of very high unemployment country-years.
Figure 3 — Feature importance (outputs/figures/feature_importance.png)
The two dominant features are labour force participation rate (37.8%) and urban population share (31.7%). Trade openness (13.7%) is third. GDP per capita level (2.9%) and growth (1.7%) carry relatively little weight. Inflation and FDI together account for 12.2%.
Table 1 — Stratified unemployment by GDP per capita quartile

GDP per capita quartile    n      Mean   unemployment (%)SE                         Q1 (lowest)             1,090   8.51     0.19         
  Q2                      1,093   7.52     0.17
  Q3                      1,085   7.99     0.19
  Q4 (highest)            1,090   7.91     0.18
Standard errors are documented for all four strata as required by the descriptive component of the charter.

## 7. Limits

What can this project say with confidence, and what can it not say?

What this project can say with confidence:

Labour force participation and urbanisation together account for the majority of cross-country predictive power for unemployment in this dataset.
A Random Forest trained on seven macro indicators explains roughly half the cross-country variation in unemployment on unseen data.
The predictive relationship is stable enough to generalise beyond the training set (CV and test R² are within 4 points of each other: 0.508 vs 0.549).

What this project cannot say:

These are predictive associations, not causal effects. We cannot say that raising labour force participation causes unemployment to fall.
The model captures cross-country and year-to-year variation jointly. It does not control for country fixed effects, so some of the signal may reflect persistent structural differences between countries rather than within-country dynamics.
The panel uses the World Bank's modelled ILO unemployment estimates, which smooth over differences in how countries define and measure unemployment. Results may not generalise to national statistical definitions.
The model was not tested on data beyond 2023. Application to 2024+ data would require the World Bank to publish those years and would carry additional uncertainty.

## 8. If The Result Was Null Or Weak

Say so directly. Do not force a story onto the data.

The primary metric passed (R² = 0.549 ≥ 0.45), so the predictive result is not null.
However, the falsifiable hypothesis was not supported. The charter predicted that countries with above-median GDP per capita growth would have unemployment rates at least 1.5 percentage points lower than countries with below-median growth. The actual difference was 0.04 percentage points — essentially zero.
This is reported directly and without adjustment.
The most likely explanation is a data artefact in the derived variable: the median of gdp_per_capita_growth across the full panel is −31.6%, which is unusually negative and suggests that the pct_change derivation produced extreme values for countries with structural GDP revisions, currency rebasings, or first-year observations where the prior year is missing. The binary median split therefore did not meaningfully separate high-growth from low-growth country-years. The overall model still predicts well, but the specific Okun's Law hypothesis — as tested here — is not supported by this data and this derivation approach. A cleaner test would winsorise the growth variable or exclude the first observation per country before computing the median split.

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

Summary: Claude was used heavily for code generation throughout the project. All code was run locally and outputs were verified against the actual JSON files and printed console output. The hypothesis null result, the median anomaly explanation, and the feature importance interpretation were written based on the actual numbers — not accepted from AI output without checking.
