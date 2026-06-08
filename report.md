# Final Report

Use this as the default shape. Keep it tight. The report should match what the code actually produced.

## 1. Question

What question did you ask, who cares about the answer, and what decision does it inform?
What is the question?
Can a set of country-level macroeconomic and structural indicators — GDP per capita growth, inflation, industry value added, trade openness, FDI inflows, labour force participation, urban population share, tertiary school enrolment, and population growth — predict a country's unemployment rate in the same year?
Who cares?
The International Labour Organization (ILO) Employment Policy Department, which advises member governments on labour market intervention. When a country's macro conditions shift, finance ministries need to anticipate unemployment pressure before it appears in costly household surveys — so they can pre-emptively allocate job-guarantee funding, training budgets, or unemployment insurance.
What decision does it inform?
Whether a country's observed unemployment rate is anomalously high or low relative to what its macro fundamentals would predict — flagging cases that warrant closer policy attention. The model is a screening tool, not a causal explanation.
## 2. Charter Summary

- Project type: Predictive
- Main metric: Out-of-sample R² on a randomly held-out 20% test set
- Success threshold: R² ≥ 0.45
- Baseline: Mean-prediction null model: predict the training-set mean (8.04%) for every observation
- Additional validation: Temporal split  train on 2000–2018, test on 2019–2023

## 3. Data

List the main sources you used. Say how you accessed them. If a source changed or failed, say what you did instead.
Source: World Bank World Development Indicators (WDI), downloaded 2026-04-08.
Access method: Direct bulk download as data/Unemployment.xlsx; no API call or login required at runtime. The file is committed to the repo under data/ with a CC BY 4.0 licence note.
Ten indicators were used across ten sheets:

 Sheet                Indicator                                     WB Code 
 - Unemployment     Unemployment rate, total (% of labour force)   SL.UEM.TOTL.ZS
                        — outcome
 - GDP Per Cap      GDP per capita growth (annual %)              NY.GDP.PCAP.CD 
 - Inflation        CPI inflation (annual %)                      FP.CPI.TOTL.ZG 
 - Trade            Trade openness (% of G                        NE.TRD.GNFS.ZS
 - FDI              FDI net inflows (BoP, current USD)            BX.KLT.DINV.CD.WD
 - Labour Force     Labour force participation rate (%)           SL.TLF.ACTI.ZS  
 - Urban Pop        Urban population (% of total)                 SP.URB.TOTL.IN.Z 
 - School           School enrollment, tertiary (% gross)         SE.TER.ENRR
 - Population Total Population growth (annual %)                  SP.POP.GROW
 - Industry         Industry value added (% of GDP)               NV.IND.TOTL.ZS
   
gdp_per_capita_growth is read directly from the "GDP Per Cap" sheet (NY.GDP.PCAP.KD.ZG), which the World Bank already publishes as a pre-computed annual % growth rate. No pct_change() derivation is used, which eliminates the first-observation
artifact that previously produced a distorted median of −31.28%.
No source failed. All ten sheets were present and parseable. World Bank aggregate and regional rows (WLD, HIC, SSA, etc.) were excluded using a fixed exclusion list; only sovereign country rows were retained. Panel construction: The outcome variable (Unemployment, 4,484 obs, 187 countries) anchors the merge. All other sheets are joined on country_code and year via an outer merge, then rows missing the outcome are dropped. After dropping 151 rows with more than 3 missing features, the final clean panel contains 4,333 country-year observations across 183 countries. 
Remaining missing values were filled with each column's global median before modelling:
- %Feature                  Missing filled       Median used
- %gdp_per_capita_growth       29                   2.2088
- %inflation                   28                   43.6979
- %industry_value_added        142                  25.0306
- %trade_openness              436                  74.4142
- %fdi_inflows                 90                   1.3300
- %school_enrollment           1,410                38.2059
  
labor_force_part, urban_population_pct, and population_growth required
no imputation. fdi_inflows was sign-log transformed (np.sign(x) * np.log1p(abs(x))) before modelling to handle heavy right skew
and occasional negative values from FDI reversals.

## 4. Method

Explain the baseline first. Then explain the main analysis. Keep it readable. If you used a causal design, state the assumptions. If you used a predictive model, state the evaluation split. If you used a descriptive design, state the comparison structure and sample discipline.

Baseline
The null model predicts the training-set mean unemployment rate — 8.04% — for every observation in the test set, regardless of any feature values. This produces an out-of-sample R² of −0.0009 by construction. Any model that learns from the features must beat this.
Primary validation — random 80/20 split
The panel was split 80/20 into train (3,466 obs) and test (867 obs) using a random split with seed 42. Three candidate models were evaluated by 5-fold CV:
Main analysis
The panel was split 80/20 into train and test sets using a random split with seed 42.
Three candidate models were evaluated by 5-fold cross-validation on the training set:

-  Model                     CV R² (mean ± std)
-  Ridge Regression         0.2157 (±0.0307)
-  Gradient Boosting        0.6287 ± 0.0228
-  Random Forest            0.6482 ± 0.0172

Random Forest was selected and re-trained on the full training set, then evaluated once on the held-out test set.

Additional validation — temporal split
To provide a more credible out-of-time check, the model was also trained on all country-years up to and including 2018 (3,438 obs) and tested on 2019–2023 (895 obs). This is a harder test: the model has never seen any data from the test period, including the 2020 COVID-19 shock. Results are reported alongside the primary metric but do not replace it.
## 5. Result

- Main metric value:
-  Out-of-sample R²: 0.6841
- Threshold: 0.45
- Passed: Yes
- MAE:  2.34 percentage points
- RMSE: 3.30 percentage points
- Baseline R² : −0.0009

- Temporal validation (train 2000–2018 / test 2019–2023)
- Metric                 Value
- Temporal R²            0.3612
- Temporal MAE           3.40 pp
- Temporal RMSE          4.69 pp
- Temporal baseline R²   −0.0132

The temporal R² falls from 0.68 to 0.36 — a drop of 32 points. This is expected and should be read as honest, not as failure. The test period (2019–2023) includes the 2020 COVID-19 shock, which produced unemployment spikes with no precedent in the 2000–2018 training data. Crucially, the temporal baseline R² is also near zero (−0.013), so the model still explains substantially more variance than the naive mean prediction on those years.
## 6. Evidence

Point to the figures, tables, regressions, or diagnostics that support the result.

- Figure 1 — Actual vs Predicted (outputs/figures/actual_vs_predicted.png) Points cluster close to the 45° line across the full range of unemployment rates (0–37%). Predictions are tight in the 0–15% range where most countries sit, and somewhat more dispersed for high-unemployment outliers above 25%, which are predominantly Sub-Saharan African and MENA country-years.
- Figure 2 — Residual distribution (outputs/figures/residuals.png) Residuals are centred near zero and roughly symmetric. The bulk fall within ±5 percentage points. A modest right tail reflects underprediction of a small number of very high unemployment country-years.
- Figure 3 — Feature importance (outputs/figures/feature_importance.png) Labour force participation rate and urban population share are the two dominant features, together accounting for the majority of predictive signal. Trade openness is third. School enrollment, industry value added, inflation, FDI, population growth, and GDP per capita growth contribute the remainder. The addition of the three new indicators (Industry, School, Population Total) relative to the 7-feature version raised test R² from 0.51 to 0.68.
Table 1 — Stratified unemployment by GDP per capita quartile

- GDP per capita quartile    n     Mean   unemployment (%)SE
- Q1 (lowest)         1,084    8.45    0.187
- Q2                       1,097    7.78    0.179
- Q3                       1,069    7.87    0.189
- Q4 (highest)             1,083    7.90    0.180
Standard errors are documented for all four strata. The pattern is non-monotonic — Q1 has the highest mean unemployment, Q2 the lowest, with Q3 and Q4 in between — consistent with the absence of a simple growth–unemployment gradient in cross-country data.

Three independent methods were used to assess which features drive predictions. All three return the same top-three ranking, which provides strong evidence that the ranking is real and not an artifact of the method.

- Feature                   RF Gini (MDI)     RF Permutation          GB Gini            Bootstrap mean ± std
- Labour force part.        0.2552             0.6390                 0.2702             0.2710 ± 0.0230
- Urban pop. %              0.2377             0.4145                 0.2470             0.2191 ± 0.0124
- Population growth         0.1889             0.3168                 0.1807             0.1835 ± 0.0173
- Industry value added      0.1123             0.1403                 0.1074             0.0997 ± 0.0155
- Trade openness            0.0723             0.0909                 0.0686             0.0690 ± 0.0063
- School enrollment         0.0623             0.0732                 0.0572             0.0623 ± 0.0104
- Inflation                 0.0281             0.0177                 0.0324             0.0368 ± 0.0055
- FDI inflows (log)         0.0278             0.0257                 0.0221             0.0356 ± 0.0078
- GDP pc growth             0.0155             0.0109                 0.0143             0.0231 ± 0.0038
Key finding: GDP per capita growth is consistently the least important
predictor across all three methods. Labour force participation, urbanisation,
and demographic structure (population growth) dominate. The bootstrap standard
deviations are small relative to the gaps between tiers, confirming the ranking
is stable across different draws of the training data.


## 7. Limits

What this project can say with confidence:

A country's unemployment rate is, in this cross-country panel, primarily determined by structural features — the share of the working-age population actively participating in the labour market, the degree of urbanisation, and demographic dynamics — rather than by its short-run macroeconomic cycle.
Labour force participation alone accounts for roughly 26–64% of total importance across methods; the top three features together explain more than 60% of total predictive power by any measure.
This makes intuitive economic sense. In cross-country data spanning 24 years and 183 countries, the variation in unemployment is overwhelmingly explained by where countries sit on long-run structural trajectories — the formality of the labour market, whether the economy is urban or agricultural, how fast the population is entering the labour force — not by whether last year's GDP
ticked up or down.
What the GDP growth result means
The falsifiable hypothesis — that countries with above-median GDP per capita growth have unemployment at least 1.5 pp lower — was not supported. The observed difference is −0.29 pp (below-median growth: 7.77% unemployment; above-median growth: 8.06%). Not only is the difference below the 1.5 pp threshold, it runs in the opposite direction.
This is not a failure. It is an economically meaningful finding. Okun's Law — the empirical relationship between GDP growth and unemployment — is well established within individual countries over time. But it does not replicate cleanly in cross-sectional data, because the structural features that make some countries chronically high-unemployment are not the same as the cyclical forces that drive unemployment up or down in a given year. 
A country with weak labour force participation and low urbanisation will have high unemployment whether GDP grows at 1% or 6%. Cross-country regression conflates these two dimensions, and our model confirms that the structural dimension dominates.
Practical use of the model 
The model's appropriate use is as a screening tool: given a country's macro and structural indicators, it predicts what unemployment "should" be. Countries where actual unemployment substantially exceeds the model prediction are candidates for closer investigation — either something unusual is happening in the labour market, or a structural factor not captured in these nine features is at work. The temporal validation (R² = 0.36 on 2019–2023) means users should apply an additional uncertainty margin when applying the model to post-2018 data, particularly for countries hit hard by COVID.
## 8. If The Result Was Null Or Weak

This project is explicitly predictive, not causal.

We cannot say that raising labour force participation causes unemployment to fall. Labour force participation and unemployment are simultaneously determined; higher participation can raise measured unemployment if new entrants cannot find work.
The model does not control for country fixed effects. Some of the predictive signal reflects persistent cross-country structural differences that are correlated with our features, not causal effects of those features.
The World Bank's modelled ILO unemployment estimates smooth over national measurement differences. Countries with informal economies may have systematically mismeasured unemployment.
The temporal gap (0.68 → 0.36) is a caution: macro shocks not anticipated in training data materially degrade prediction accuracy.
GDP growth is a weak predictor in this cross-country panel. This does not mean growth policy is ineffective; it means Okun's Law operates mainly at the within-country, time-series level, which this panel cannot cleanly identify.
## 9. Reproducibility

- Run command: uv run main.py
- Runtime: ~60–90 seconds on a Google Colab (permutation importance adds time)
- Data dependency: data/Unemployment.xlsx must be present under data/ in the repo root
- Output files written:
outputs/primary_metric.json
outputs/baseline_metric.json
outputs/milestone_manifest.json
outputs/figures/actual_vs_predicted.png
outputs/figures/residuals.png
outputs/figures/feature_importance.png
outputs/figures/unemployment_by_gdp_growth_quartile.png

## 10. AI Usage

Summarize the main places AI helped and what the team checked manually. Point to [AI_USAGE_LOG.md](./AI_USAGE_LOG.md) for the detailed log.

Summary: Claude was used for code generation throughout the project. All code was run on Google Colab and outputs were verified against the actual printed console output and JSON files. The hypothesis null result, the median anomaly explanation, and the feature importance interpretation were written based on the actual numbers — not accepted from AI output without checking.
