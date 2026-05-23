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
| Project type |  descriptive |
| Estimated hours per person | 60 |
| Charter version | v1 |
| Date | 2026-05-23|

**Project type notes.** Predictive = you are trying to forecast or predict a quantity. Causal = you are trying to estimate the effect of a policy or intervention. Descriptive = you are measuring patterns or disparities without making a causal claim. The success threshold looks different for each type, so pick the one that fits your main question.

---

## 1. Problem and stakeholder

One paragraph. Who is the specific person, institution, or policy body that would care about the answer, and what decision does the answer inform? Generic "policymakers" is not a stakeholder; "the Ministry of Petroleum and Natural Gas deciding whether to extend PMUY subsidies in FY 2026-27" is.

*Write here:*

The stakeholder for this project could be the Ministry of Environment, Forest and Climate Change working together with the NITI Aayog while designing future development and climate strategies. These institutions would care whether rising income levels are associated with higher pollution because the findings can inform decisions on balancing economic expansion with environmental sustainability. If the analysis shows that growth initially increases emissions but later slows or reduces them, it could influence decisions on green investment incentives, industrial regulations, and the allocation of funding toward cleaner technologies in future development plans.

## 2. Main outcome variable

The single number your project centres on. State:

- **Name** of the variable
- **Unit** (percentage, Rs/month, points, deaths per 1000, etc.)
- **Source table/column/field**
- **Population / panel** (which rows: which years, which geographies, which people)

Only one main outcome. Secondary outcomes go under "Scope limits" as things you *may* report but will not be graded on.

*Write here:*
Name of variable:
CO₂ emissions per capita
Unit:
Metric tons of CO₂ per person
Source table/column/field:
World Bank indicator EN.ATM.CO2E.PC (CO₂ emissions, metric tons per capita)
Population / panel:
Worldwide country-year panel data from approximately 2004–2023, where each row represents a country observed in a specific year.


## 3. Main quantitative success threshold

A single numeric bar. Your project is a success if the delivered metric crosses this bar, and a failure if it does not. Pick one form:

- **Predictive:** "Out-of-sample [metric] on [held-out slice] is at most X, versus baseline Y."
- **Causal:** "Point estimate of [parameter] has 95% CI excluding zero, and |estimate| ≥ X [unit]."
- **Descriptive:** "Produce stratified estimates of [outcome] across [N ≥ __] strata, each with sample size ≥ __ and documented standard error."

If you cannot write a number, you do not yet have a project — you have a topic. Go back to Section 2.

*Write here:*
Predictive: Out-of-sample R² on a held-out test sample (20% of worldwide country-year observations from 2000–2023) is at least 0.50, versus a baseline model R² of 0.00.
---

## 4. Baseline to beat

The naive or prior number your threshold is measured against. Examples:

- A previous study's coefficient or error.
- A simple AR(1) or last-value forecast.
- An unadjusted before-after difference.

State **what the baseline produces numerically** if you know it, or how you will compute it before the checkpoint if you do not. You must compute the baseline *before* you build anything fancy.

*Write here:*

The baseline model will predict the mean CO₂ emissions per capita for all observations in the training dataset, regardless of GDP per capita, urbanization, or industrial output. The baseline model's out-of-sample R² is expected to be approximately 0.00, and the exact value will be computed before building the predictive model using the training data.

## 5. Falsifiable hypothesis

One sentence the data can prove wrong. A sign, a threshold, or a rank ordering. Not "we will analyse X" — "X will be greater than Y by at least Z".

*Write here:*

---

## 6. Data sources and access plan

For each source:

- **Name and URL/API endpoint**
- **Licence or permission to use**
- **Access method** (direct download, API call, authenticated portal)
- **A 10-line script or notebook cell** that fetches one row and prints it

If any source requires manual scraping, permissions, or a login you do not yet have, flag it here with a mitigation plan.

*Write here:*

---

## 7. Scope limits

Bullet list of things you are **not** claiming and **not** responsible for. Examples:

- "We will not estimate a structural causal effect of monetary policy."
- "We will not harmonise district boundaries across NFHS rounds; analysis is at state level."
- "We will not ship a mobile version of the app."

This section protects you at grading time. If you clearly say "we are not doing X," you will not be graded on X.

*Write here:*

---

## 8. Risks and fallback

One named failure mode, and the fallback analysis you will run if it materialises. Examples:

- "If the 2022-23 PPAC data is not released by the checkpoint, we will use the FY 2021-22 panel and document the truncation."
- "If DiD parallel-trends fails visually, we fall back to a state-fixed-effects panel regression with year trends and report both."

One risk is enough. Two is fine. Zero means you have not thought hard enough.

*Write here:*

---

## 9. Reproducibility checklist

Your final repo must satisfy all of these:

- [ ] `uv run main.py` runs end-to-end in under 10 minutes on a clean machine with no manual intervention.
- [ ] It writes `outputs/primary_metric.json` containing a single JSON object with at least `{"metric_name": "...", "value": <number>, "threshold": <number>, "passed": <bool>}`.
- [ ] It writes `outputs/baseline_metric.json` in the same shape.
- [ ] A `README.md` documents the commands and expected outputs in ≤ 20 lines.
- [ ] All data sources are either fetched in-script or committed under `data/` with a licence note.

If you cannot commit to this, your project is probably still too broad. Talk to the instructor before proceeding.

---

## Sign-off

By submitting this charter, the team agrees that this is the plan the project will be graded against. The instructor will not penalize you just because the topic turns out to be difficult, as long as the project stays honest and within the approved scope.

*Signed:* _(team member names)_
