# Example Charter — PMUY and Clean-Fuel Adoption

> **Worked example for the causal project type.** Adapted from a real proposal by **Tanisha Aggarwal, Neha Rana, and Jaswathi Lalitha R**, refined into charter form and shared with the class as an exemplar. Notice the falsifiable hypothesis is a signed magnitude on a specific coefficient, not a vague claim about impact.
>
> **Repo-first note.** In a real team project, this content would live in `CHARTER.md` inside the team repo, be revised there until approval, and could then be frozen as `charter_approved.pdf` if the team wants a locked copy.

---

## Header

| Field | Value |
|---|---|
| Team members | Tanisha Aggarwal, Neha Rana, Jaswathi Lalitha R |
| Project type | Causal |
| Estimated hours per person | 55 |
| Charter version | v1 |
| Date | 2026-04-18 |

---

## 1. Problem and stakeholder

The Pradhan Mantri Ujjwala Yojana (PMUY), launched in May 2016, subsidises LPG connections for women from poor households. In 2025 the Ministry of Petroleum and Natural Gas approved an additional 25 lakh connections under Ujjwala 2.0 and extended refill subsidies. The Ministry's FY 2026-27 budget memorandum requires a quantitative statement on whether the scheme has caused faster clean-fuel adoption in the states most dependent on solid fuel before the rollout. Our charter targets that specific decision point and packages the evidence into a reproducible policy-facing analysis that a Ministry analyst could actually inspect and reuse.

## 2. Main outcome variable

- **Name:** share of households using clean cooking fuel (LPG, electricity, biogas, or natural gas as primary)
- **Unit:** percentage points, 0–100
- **Source:** NFHS-4 (2015-16) and NFHS-5 (2019-21) state-level household files; variable `HV226` recoded into a clean-fuel binary, aggregated by state-round using sample weights.
- **Population / panel:** 28 Indian states (excluding UTs for comparability), two rounds; 56 state-round observations.

## 3. Main quantitative success threshold

The Difference-in-Differences coefficient β₃ on `Post × HighExposure` in the two-way fixed-effects model below has:
(a) a 95% confidence interval that excludes zero, and
(b) a point estimate of at least **+3.0 percentage points** in favour of high-exposure states.

Model: `Y_st = α + β₁·Post_t + β₂·HighExposure_s + β₃·(Post_t × HighExposure_s) + δ_s + λ_t + γ·X_st + ε_st`, with `HighExposure` defined as below-median clean-fuel share in NFHS-4, standard errors clustered at the state level.

## 4. Baseline to beat

Unadjusted pre-post difference in national clean-fuel share (NFHS-5 mean − NFHS-4 mean, pooled across all states). Based on official summary statistics, this is expected to be roughly +15 pp. Our DiD estimate for the high-exposure subset must exceed this unadjusted national difference, otherwise the policy effect is indistinguishable from the country-wide trend. Baseline is computed and committed to `outputs/baseline_metric.json` before any DiD estimation.

## 5. Falsifiable hypothesis

States in the bottom half of pre-policy clean-fuel access (below the NFHS-4 median) experienced a larger jump in clean-fuel share between NFHS-4 and NFHS-5 than states in the top half, by at least **3 percentage points** after controlling for state and time fixed effects. If β̂₃ < 3 pp or its CI crosses zero, the hypothesis is rejected.

## 6. Data sources and access plan

All four sources are open. No DHS microdata registration is required — the state-level clean-fuel share needed for the DiD is served directly by the DHS aggregated API.

- **NFHS-4 and NFHS-5 state-level clean-fuel share (main outcome):**
  - DHS Program aggregated API — no registration: https://api.dhsprogram.com/rest/dhs/data
  - Parameters: `countryIds=IA` (India), `indicatorIds=HC_CKFL_H_CLN` (clean fuel composite), `surveyIds=IA2020DHS` (NFHS-5) or `IA2015DHS` (NFHS-4), `breakdown=all` (returns ~49 rows: national + urban/rural + wealth quintile + 28 states / 8 UTs).
  - Probe: `requests.get("https://api.dhsprogram.com/rest/dhs/data", params={"countryIds":"IA","indicatorIds":"HC_CKFL_H_CLN","surveyIds":"IA2020DHS","breakdown":"all","f":"json"})` → `.json()["Data"]`.
  - Secondary/cross-check: compiled NFHS CSV at https://raw.githubusercontent.com/pratapvardhan/NFHS-5/master/NFHS-5-States.csv (CC-BY 4.0, DOI 10.7910/DVN/42WNZF). Row "Households using clean fuel for cooking (%)" carries both NFHS-4 and NFHS-5 values side by side.
- **PMUY administrative data (state-wise connections):**
  - PPAC landing: https://ppac.gov.in/consumption/state-wise-pmuy-data
  - The .xlsx filename is timestamp-versioned (e.g. `1747729722_pumy-connection.xlsx` as of Apr-2026) and refreshes server-side, so we re-scrape the landing page for the current `.xlsx` link at pipeline runtime rather than hardcoding it.
  - Backup: data.gov.in resource https://www.data.gov.in/resource/stateut-wise-number-pradhan-mantri-ujjwala-yojana-pmuy-connections-2018-2023 (requires a free instant API key at https://data.gov.in/user/register).
  - Login required: no for PPAC; free instant key for data.gov.in backup.
- **PPAC state-wise LPG consumption (treatment-intensity cross-validation):**
  - Landing: https://ppac.gov.in/consumption/state-wise
  - Public .xlsx (statewise sales, POL consumption) is direct-download; filename is again timestamp-versioned and re-scraped at runtime.
  - Monthly granularity requires free PPAC member-portal login, which we will not use — the public annual + latest-month snapshots are sufficient for our treatment definition.
  - Login required: no for the public file.
- **NFHS factsheet triangulation (diagnostic only):**
  - IIPS migrated from the legacy `rchiips.org` URLs (now 404) to https://www.nfhsiips.in/nfhsuser/nfhs5.php and `.../nfhs4.php`. These are referenced for indicator-definition cross-checks; they are not the primary data source.
  - MoHFW compendium (both phases) mirrored at https://dhsprogram.com/pubs/pdf/OF43/NFHS-5_India_and_State_Factsheet_Compendium_Phase-I.pdf and `..._Phase-II.pdf`.
- *(Access-probe notebook: `notebooks/00_fetch_one_state.ipynb` hits the DHS API for one state in each round.)*

## 7. Scope limits

The core deliverable is a reproducible analysis repo plus a short policy-facing write-up. If time permits, the team may also include a small read-only Streamlit explainer. Specifically:

- We will **not** claim causal identification beyond the parallel-trends assumption for the DiD. Event-study plots are diagnostic, not inferential.
- We will **not** analyse refill intensity or health outcomes (blood-pressure, respiratory) even though they are in the NFHS files. Those appear in the Performance Index as a composite metric only, not as primary outcomes.
- The **State PMUY Performance Index** (40% clean-fuel improvement, 30% connection coverage, 20% refill usage, 10% rural inclusion) is a presentational ranking, not a causal or inferential estimate. It will be labelled clearly as descriptive if included.
- Any short AI-assisted explainer will be templated from the actual regression output. It explains the model; it does **not** replace the model and does **not** fabricate numbers.
- We will **not** build a production-grade app, mobile-responsive version, or user authentication.
- We will **not** use UTs or disaggregate to district-level adoption.

## 8. Risks and fallback

- **Risk:** Parallel-trends assumption cannot be visually supported with only two NFHS rounds (one pre, one post). **Fallback:** Supplement with IHDS-II (2011-12) as a pseudo-pre-period to anchor the pre-trend; report both DiD-only and DiD-with-IHDS-anchor estimates side by side.
- **Risk:** The high-vs-low exposure split produces only 14 states in each group; SEs may be too wide to reject null. **Fallback:** Pre-commit an alternative continuous-treatment specification (`β · (1 − baseline_clean_share) × Post`) and report both.

## 9. Reproducibility checklist

- [x] `uv run main.py` runs top-to-bottom in under 8 minutes (all regressions, plots, and final output files).
- [x] Writes `outputs/primary_metric.json` with `{"metric_name": "did_coefficient_pp", "value": <float>, "ci_lower": <float>, "ci_upper": <float>, "threshold": 3.0, "passed": <bool>}`.
- [x] Writes `outputs/baseline_metric.json` with the unadjusted national pre-post difference.
- [x] `README.md` documents the environment and exact commands.
- [x] NFHS extract SQL or `rdhs` query is committed; the aggregated state-round panel is written to `data/panel.parquet`.

---

*Signed:* Tanisha Aggarwal, Neha Rana, Jaswathi Lalitha R
