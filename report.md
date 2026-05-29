# Final Report

Use this as the default shape. Keep it tight. The report should match what the code actually produced.

## 1. Question

What question did you ask, who cares about the answer, and what decision does it inform?
What is the question?
Can a set of country-level macroeconomic and structural indicators — GDP per capita growth, inflation, industry value added, trade openness, FDI inflows, labour force participation, urban population share, tertiary school enrolment, and population growth — predict a country's unemployment rate in the same year?
Who cares?
The International Labour Organization (ILO) Employment Policy Department, which advises member governments on labour market intervention. When a country's macro conditions shift, finance ministries need to anticipate unemployment pressure before it appears in costly household surveys — so they can pre-emptively allocate job-guarantee funding, training budgets, or unemployment insurance.
What decision does it inform?
Whether a country's observed unemployment rate is anomalously high or low relative to what its macro fundamentals would predict — flagging cases that warrant closer policy attention.

## 2. Charter Summary

- Project type: Predictive
- Main metric: Out-of-sample R² on a randomly held-out 20% test set
- Success threshold: R² ≥ 0.45
- Baseline: Mean-prediction null model: predict the training-set mean (8.02%) for every observation

## 3. Data

List the main sources you used. Say how you accessed them. If a source changed or failed, say what you did instead.
Source: World Bank World Development Indicators (WDI), downloaded 2026-04-08.
Access method: Direct bulk download as data/Unemployment.xlsx; no API call or login required at runtime. The file is committed to the repo under data/ with a CC BY 4.0 licence note.
Ten indicators were used across ten sheets:

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
   
Note: gdp_per_capita_growth is read directly from the "GDP Per Cap" sheet (NY.GDP.PCAP.KD.ZG) — it is not derived via pct_change() in the 10-indicator version of the code, which eliminates the first-observation artifact entirely.
No source failed. All ten sheets were present and parseable. World Bank aggregate and regional rows (WLD, HIC, SSA, etc.) were excluded; only sovereign country rows were retained.
Panel construction: The outcome variable (Unemployment, 4,484 obs, 187 sovereign countries) anchors the merge. All other sheets are joined on country_code and year via an outer merge, then rows missing the outcome are dropped. After dropping rows with more than 3 missing features, the final clean panel contains 4,369+ country-year observations across 185 countries. Remaining missing values were filled with each column's global median before modelling (largest gap: school enrolment and trade openness).

## 4. Method

Explain the baseline first. Then explain the main analysis. Keep it readable. If you used a causal design, state the assumptions. If you used a predictive model, state the evaluation split. If you used a descriptive design, state the comparison structure and sample discipline.

Baseline
Baseline
The null model predicts the training-set mean unemployment rate (~8.01%) for every observation in the test set. This produces an out-of-sample R² of approximately −0.0009 by construction. Any model that learns from the features must beat this.
Main analysis
The panel was split 80/20 into train and test sets using a random split with seed 42.
Three candidate models were evaluated by 5-fold cross-validation on the training set:

- Model                   CV R² (mean ± std)
-  Ridge Regression        0.1377 ± 0.0648
-  Gradient Boosting       0.4876 ± 0.0141
-  Random Forest           0.5146 ± 0.0218

Random Forest was selected and re-trained on the full training set before being evaluated once on the held-out test set.
FDI inflows were sign-log transformed (np.sign(x) * np.log1p(abs(x))) to handle heavy right skew and occasional negative values from FDI reversals. All other features were used as-is after median imputation.
## 5. Result

- Main metric value:
-  Out-of-sample R²: 0.5139
- Threshold: 0.45
- Passed: Yes
- MAE:  2.83 percentage points
- RMSE: 4.01 percentage points
- Baseline R² : −0.0009

Give the main number first. Then interpret it in plain English.
The Random Forest model explains approximately 51% of the cross-country variation in unemployment rates on unseen data. The average prediction error of 2.83 pp is meaningful accuracy given that features include no country fixed effects and no lagged unemployment values.
## 6. Evidence

Point to the figures, tables, regressions, or diagnostics that support the result.

Fig 1 — Actual vs Predicted (outputs/figures/fig1_actual_vs_predicted.png)
The scatter plot shows R² = 0.514, MAE = 2.83 pp, n = 874. Points cluster close to the 45° line across the 0–37% range. Predictions are tight in the 0–15% band where most countries sit; larger errors (red points) are concentrated among high-unemployment outliers above 20%.
Fig 3 — Random Forest feature importance (outputs/figures/fig3_feature_importance.png)
Feature importances (mean decrease in impurity, normalised):
FeatureImportanceLabour force participation0.377Urban population share0.329Trade openness0.129Inflation0.066FDI inflows0.057GDP per capita0.027GDP per capita growth0.016
Labour force participation and urbanisation together account for 70.6% of predictive signal, reflecting persistent structural differences between countries.
Fig 7 — Unemployment by income group (outputs/figures/fig7_unemployment_by_income_group.png)
Box plots by World Bank income classification (2000–2023). Low-income countries (median ~3%) and lower-middle-income countries (median ~5%) have substantially lower unemployment rates than high-income and upper-middle-income countries (medians ~6–7%). This non-monotonic pattern is consistent with the absence of a simple income–unemployment gradient and likely reflects differences in labour market formality and measurement.
Table 1 — Stratified unemployment by GDP per capita quartile

- GDP per capita quartile    n     Mean   unemployment (%)SE                     - Q1 (lowest)             1,093   8.50     0.185
- Q2                      1,101   7.59     0.170
- Q3                      1,083   7.99     0.188
- Q4 (highest)            1,090   7.90     0.179
Standard errors are documented for all four strata. The non-monotonic pattern — Q1 highest, Q2 lowest — is consistent with the income group distribution in Fig 7 and with the absence of a linear income–unemployment gradient.

## 7. Limits

What can this project say with confidence, and what can it not say?

What this project can say:

Labour force participation and urbanisation together explain the majority of cross-country predictive power for unemployment.
A Random Forest trained on 9 macro/structural indicators explains ~51% of the cross-country variation in unemployment on unseen data.
CV R² (0.5146) and test R² (0.5139) are within 0.001, indicating no meaningful overfitting.

What this project cannot say:

These are predictive associations, not causal effects.
The model does not control for country fixed effects; some signal may reflect persistent structural differences rather than within-country dynamics.
Results rely on the World Bank's modelled ILO unemployment estimates, which smooth over national measurement differences.
The model was not tested on post-2023 data.

## 8. If The Result Was Null Or Weak

The charter predicted that countries with above-median GDP per capita growth have unemployment ≥ 1.5 pp lower than those below. This hypothesis was not supported. The observed difference between growth groups was 0.08 pp — far below the 1.5 pp threshold.
The 10-indicator version reads GDP growth directly from the WDI "GDP Per Cap" sheet (NY.GDP.PCAP.KD.ZG) rather than deriving it via pct_change(). This eliminates the first-observation artifact that produced a median of −31.28% in earlier runs. Even with a clean, plausible growth variable, the hypothesis is not supported: both above- and below-median growth groups average approximately 8% unemployment in this cross-country panel.

## 9. Reproducibility

- Run command: uv run main.py
- Runtime: ~25–35 seconds on a standard laptop (no internet required)
- Data dependency: data/Unemployment.xlsx must be present under data/ in the repo root
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
