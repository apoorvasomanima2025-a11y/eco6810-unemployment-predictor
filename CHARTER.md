# Project Charter — ECO 6810 Final Project

> Need the big picture first? Read the [Final Project brief](./FINAL_PROJECT.md) before you fill this out.
>
> **What this is.** Your short approved project plan. It tells me what you are trying to do, what data you will use, what your main metric is, and what a good result would look like.
>
> **What this is not.** A brainstorm or a long proposal. Keep it short, specific, and concrete.
>
> **Why we use it.** It keeps the project focused. Once this is approved, the milestone and the final submission are judged against this plan, not against shifting expectations later.
>
> **How to fill it.** Copy this file. Answer every field. Keep it under two pages. If a field asks for a number, give a real number with a unit.
>
> **Where this lives.** Fill this out inside your team GitHub repo. That repo is where we will review and approve the charter.
>
> **How approval works.** Revise `CHARTER.md` in the repo until it is approved. Do not treat the charter as a separate detached file living somewhere else.
>
> **Simplest editing path.** Open `CHARTER.md` on GitHub, click the pencil icon, edit the file, and commit the change.
>
> **After approval.** One teammate can freeze the approved version as a PDF with:
> `pandoc CHARTER.md -o charter_approved.pdf`
> Then commit that PDF to the repo as the locked approved copy.

---

## Header

| Field | Value |
|---|---|
| Team members | Apoorva Somani|
| Project type |  Predictive|
| Estimated hours per person | 60 |
| Charter version | v1 |
| Date | 2026-05-23|

**Project type notes.** Predictive = you are trying to forecast or predict a quantity. Causal = you are trying to estimate the effect of a policy or intervention. Descriptive = you are measuring patterns or disparities without making a causal claim. The success threshold looks different for each type, so pick the one that fits your main question.

---

## 1. Problem and stakeholder

One paragraph. Who is the specific person, institution, or policy body that would care about the answer, and what decision does the answer inform? Generic "policymakers" is not a stakeholder; "the Ministry of Petroleum and Natural Gas deciding whether to extend PMUY subsidies in FY 2026-27" is.

*Write here:*

The primary stakeholder is the International Labour Organization (ILO) Employment Policy Department, specifically its analysts who advise member governments on labour market intervention. When a country's macroeconomic conditions shift — GDP contracts, FDI dries up, or urbanisation accelerates — finance ministries need to anticipate unemployment pressure before it shows up in quarterly surveys, so they can pre-emptively activate job guarantee schemes, training budgets, or unemployment insurance. This project asks whether a country's unemployment rate in a given year can be reliably predicted from its macroeconomic indicators in that same year, giving policymakers a cross-country benchmark to flag when a country's observed unemployment is anomalously high or low relative to what its macro fundamentals would predict.

## 2. Main outcome variable

The single number your project centres on. State:

- **Name** of the variable
- **Unit** (percentage, Rs/month, points, deaths per 1000, etc.)
- **Source table/column/field**
- **Population / panel** (which rows: which years, which geographies, which people)

Only one main outcome. Secondary outcomes go under "Scope limits" as things you *may* report but will not be graded on.

*Write here:*
Name: Unemployment rate, total
Unit: Percentage of total labour force (%)
Source indicator code: SL.UEM.TOTL.ZS — fetchable via the World Bank API
Population / panel: Worldwide country-year panel, approximately 180 countries × years 2000–2023, where each row is one country observed in one year. 

## 3. Main quantitative success threshold

A single numeric bar. Your project is a success if the delivered metric crosses this bar, and a failure if it does not. Pick one form:

- **Predictive:** "Out-of-sample [metric] on [held-out slice] is at most X, versus baseline Y."
- **Causal:** "Point estimate of [parameter] has 95% CI excluding zero, and |estimate| ≥ X [unit]."
- **Descriptive:** "Produce stratified estimates of [outcome] across [N ≥ __] strata, each with sample size ≥ __ and documented standard error."

If you cannot write a number, you do not yet have a project — you have a topic. Go back to Section 2.

*Write here:*
Predictive: Out-of-sample R² on a randomly held-out test set (20% of all country-year observations from 2000–2023) is at least 0.45, versus a baseline model R² of approximately 0.00.
This threshold is deliberately modest — an R² of 0.45 means the model explains nearly half the cross-country variation in unemployment using only macro indicators, which would be a meaningful and publishable empirical result.
---

## 4. Baseline to beat

The naive or prior number your threshold is measured against. Examples:

- A previous study's coefficient or error.
- A simple AR(1) or last-value forecast.
- An unadjusted before-after difference.

State **what the baseline produces numerically** if you know it, or how you will compute it before the checkpoint if you do not. You must compute the baseline *before* you build anything fancy.

*Write here:*

The baseline model predicts the global mean unemployment rate (computed on the training set) for every country-year observation in the test set, regardless of GDP, FDI, urbanisation, or any other predictor. This is a zero-information forecast.

Expected baseline out-of-sample R²: ≈ 0.00 (by construction of the mean-prediction baseline)
The exact value will be computed and written to outputs/baseline_metric.json before any regression or machine learning model is built.

## 5. Falsifiable hypothesis

One sentence the data can prove wrong. A sign, a threshold, or a rank ordering. Not "we will analyse X" — "X will be greater than Y by at least Z".

*Write here:*
Countries with GDP per capita growth above the global median in a given year will have unemployment rates at least 1.5 percentage points lower than countries with GDP per capita growth below the global median in that same year, after controlling for year fixed effects.
This is a directional, threshold-based, falsifiable claim grounded in Okun's Law — the well-established empirical relationship between output growth and unemployment. If the data show a difference smaller than 1.5 pp, or the wrong sign, the hypothesis is falsified.

## 6. Data sources and access plan

For each source:

- **Name and URL/API endpoint**
- **Licence or permission to use**
- **Access method** (direct download, API call, authenticated portal)
- **A 10-line script or notebook cell** that fetches one row and prints it

If any source requires manual scraping, permissions, or a login you do not yet have, flag it here with a mitigation plan.

*Write here:*

All indicators below are available  under the World Bank's open data terms.
Unemployment rateSL.UEM.TOTL.ZS
GDP growth (annual %)NY.GDP.MKTP.KD.ZG
GDP per capita (current USD)NY.GDP.PCAP.CD
Inflation, consumer pricesFP.CPI.TOTL.ZG
Trade openness (% of GDP)NE.TRD.GNFS.ZS
Labour force participation rateSL.TLF.ACTI.ZS
FDI net inflows (BoP, USD)BX.KLT.DINV.CD.WD
Urban population (% of total)SP.URB.TOTL.IN.ZS

Probe script (fetches one row, prints it):
pythonimport requests, pandas as pd

BASE = "https://api.worldbank.org/v2/country/all/indicator/"
indicator = "SL.UEM.TOTL.ZS"
url = f"{BASE}{indicator}?format=json&per_page=5&mrv=1"

r = requests.get(url)
data = r.json()
df = pd.json_normalize(data[1])
print(df[["country.value", "date", "value"]].head(1))
Access method: direct unauthenticated API call. No login, no scraping, no manual download needed.

## 7. Scope limits

Bullet list of things you are **not** claiming and **not** responsible for. Examples:

- "We will not estimate a structural causal effect of monetary policy."
- "We will not harmonise district boundaries across NFHS rounds; analysis is at state level."
- "We will not ship a mobile version of the app."

This section protects you at grading time. If you clearly say "we are not doing X," you will not be graded on X.

*Write here:*
We will not estimate a causal effect of any macroeconomic variable on unemployment; all relationships are predictive associations only.
We will not model country-specific time-series dynamics (no VAR, no ARIMA, no country-level AR(1)); the unit of analysis is the cross-sectional country-year observation.
We will not harmonise or adjust for differences in how countries measure unemployment (ILO vs. national definitions); we use the World Bank's modelled ILO estimate as-is.
We will not include high-frequency or quarterly data; the panel is annual.
We will not forecast future unemployment beyond the 2000–2023 data window.
We will not produce a web application, dashboard, or public-facing interface.
We will not analyse informal-sector employment, underemployment, or youth unemployment as primary outcomes; those may be reported descriptively but are not graded outcomes.
We will not make country-specific policy recommendations beyond what the cross-country evidence directly supports.
We will not claim that the selected macro indicators are the only or primary determinants of unemployment; institutional, political, and structural factors are acknowledged but excluded.

## 8. Risks and fallback

One named failure mode, and the fallback analysis you will run if it materialises. Examples:

- "If the 2022-23 PPAC data is not released by the checkpoint, we will use the FY 2021-22 panel and document the truncation."
- "If DiD parallel-trends fails visually, we fall back to a state-fixed-effects panel regression with year trends and report both."

One risk is enough. Two is fine. Zero means you have not thought hard enough.

*Write here:*
Failure mode: The World Bank API returns substantial missing values for inflation (FP.CPI.TOTL.ZG) or trade openness (NE.TRD.GNFS.ZS) for low-income countries and small states, reducing the usable panel to fewer than 100 countries and degrading model performance below the 0.45 R² threshold.
Fallback: Drop the two indicators with the most missingness and re-run the model on the remaining predictors (GDP growth, GDP per capita, labour force participation rate, and urbanisation), which have much better coverage in the World Bank data. Report both the full-feature and reduced-feature results side by side, document the sample size drop, and compare out-of-sample R² across both specifications. If the reduced model still fails the threshold, fall back to a descriptive analysis producing stratified unemployment estimates across GDP-per-capita quartiles with documented standard errors.

## 9. Reproducibility checklist

Your final repo must satisfy all of these:

- [ ] `uv run main.py` runs end-to-end in under 10 minutes on a clean machine with no manual intervention.
- [ ] It writes `outputs/primary_metric.json` containing a single JSON object with at least `{"metric_name": "...", "value": <number>, "threshold": <number>, "passed": <bool>}`.
- [ ] It writes `outputs/baseline_metric.json` in the same shape.
- [ ] A `README.md` documents the commands and expected outputs in ≤ 20 lines.
- [ ] All data sources are either fetched in-script or committed under `data/` with a licence note.

If you cannot commit to this, your project is probably still too broad. Talk to the instructor before proceeding.

 uv run main.py will fetch all data from the World Bank API, merge indicators, split 80/20 train/test, fit the baseline and primary models, and write outputs — end-to-end in under 10 minutes on a clean machine.
outputs/primary_metric.json will contain:

json{"metric_name": "Out-of-sample R²", "value": 0.00, "threshold": 0.45, "passed": false}
(placeholder — real value computed at runtime)

outputs/baseline_metric.json will contain:

json{"metric_name": "Baseline Out-of-sample R²", "value": 0.00, "threshold": 0.00, "passed": true}

README.md will document the single command (uv run main.py) and list the five expected output files in under 20 lines.
All data is fetched in-script from the World Bank API at runtime. No manual downloads required. A data/ folder with a LICENSE.txt noting World Bank open data terms will be committed for reference.

## Sign-off

By submitting this charter, the team agrees that this is the plan the project will be graded against. The instructor will not penalize you just because the topic turns out to be difficult, as long as the project stays honest and within the approved scope.

*Signed:* Apoorva Somani 
