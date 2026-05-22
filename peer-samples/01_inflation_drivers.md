# Example Charter — Drivers of India's 2022–23 Inflation

> **Worked example for the predictive project type.** Adapted from a real proposal by **Hasil Tewari, Sandipan Ganguly, and Parmeet Singh Majethiya**, refined into charter form and shared with the class as an exemplar. Study how every numeric field is an actual number, not an adjective.
>
> **Repo-first note.** In a real team project, this content would live in `CHARTER.md` inside the team repo, be revised there until approval, and could then be frozen as `charter_approved.pdf` if the team wants a locked copy.

---

## Header

| Field | Value |
|---|---|
| Team members | Hasil Tewari, Sandipan Ganguly, Parmeet Singh Majethiya |
| Project type | Predictive |
| Estimated hours per person | 50 |
| Charter version | v1 |
| Date | 2026-04-18 |

---

## 1. Problem and stakeholder

The Reserve Bank of India's Monetary Policy Committee sets the repo rate under a 4% CPI inflation target. During the 2022–23 surge, CPI inflation peaked around 7.8% YoY. The MPC's ex-post communication attributed the surge largely to external supply shocks (oil, wheat, fertiliser). We want to quantify, month-by-month, how much of observed CPI inflation over 2020–2024 is statistically attributable to monetary policy variables, external shocks, and domestic demand — as input to a hypothetical policy retrospective an MPC analyst would present to the board. Prior work (Dua and Goel, 2021) stops in 2017 and therefore omits COVID and the 2022–23 episode; our contribution is to extend this accounting to the post-2017 window with flexible ML methods.

## 2. Main outcome variable

- **Name:** month-over-month CPI inflation, India, all-items
- **Unit:** percentage points (m/m)
- **Source:** MoSPI CPI release, all-India combined series (`CPI_C_GEN`)
- **Population / panel:** monthly observations, Jan 2015 – Dec 2024 (120 months); train on Jan 2015 – Dec 2021, evaluate on Jan 2022 – Dec 2024 (36 months held-out)

## 3. Main quantitative success threshold

Out-of-sample RMSE on the 2022-01 to 2024-12 held-out slice is **≤ 0.35 percentage points per month**, versus an AR(1) baseline whose RMSE on the same slice will be measured first and reported. If the baseline RMSE is already below 0.40 pp, our threshold tightens to baseline − 25%.

## 4. Baseline to beat

AR(1) on m/m CPI inflation, fit on Jan 2015 – Dec 2021, evaluated on Jan 2022 – Dec 2024. We will compute this baseline RMSE before any model building and commit it to `outputs/baseline_metric.json`. A linear VECM (Dua-Goel-style with our variable set) is reported as a secondary baseline.

## 5. Falsifiable hypothesis

In the Q2-2022 to Q1-2023 window, at least **50% of the cumulative m/m inflation assigned by our feature-attribution method is allocated to the external-shock group** (Brent + INR/USD), with the remaining share split between policy (repo rate) and domestic demand (IIP). If external shocks account for < 50%, the hypothesis is rejected and we report whichever group dominates.

## 6. Data sources and access plan

All five sources are fully open: no account, no API key, no registration.

- **MoSPI CPI (all-India combined, monthly):**
  - Landing: https://www.mospi.gov.in/cpi ; machine-readable catalogue: https://esankhyiki.mospi.gov.in/catalogue-main/catalogue?product=CPI
  - Access: direct .xlsx download from the eSankhyiki catalogue (the Jan-2026 release switched the series to base 2024=100; for our Jan 2015 – Dec 2024 window we stay on the legacy 2012=100 series).
  - Login required: no.
  - Probe: `pd.read_excel(<xlsx_link_from_catalogue>)`.
- **RBI repo rate (monthly end-of-period):**
  - DBIE (https://data.rbi.org.in/DBIE/) is the formal source but is query-gated with no stable CSV URL. Our primary path is to hand-build a 25-row CSV from the RBI Monetary Policy press releases (https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx), since the repo rate changes discretely and only ~25 decisions cover the 10-year window.
  - Login required: no.
  - The FRED India discount-rate mirror `INTDSRINM193N` is retained as a cross-check but stops in Jul-2022 and cannot cover the full window on its own.
- **RBI INR/USD reference rate (monthly average):**
  - RBI published its own reference rate until 10 Jul 2018; from 11 Jul 2018 onward the benchmark is FBIL-computed (https://www.fbil.org.in/). For a single continuous Jan 2015 – Dec 2024 monthly series we use FRED `EXINUS` (https://fred.stlouisfed.org/graph/fredgraph.csv?id=EXINUS), which sources from Federal Reserve H.10 and tracks the RBI/FBIL reference.
  - Login required: no (CSV endpoint).
  - Probe: `pd.read_csv("https://fred.stlouisfed.org/graph/fredgraph.csv?id=EXINUS")`.
- **Brent oil price (daily → monthly average):**
  - FRED series `DCOILBRENTEU` (https://fred.stlouisfed.org/graph/fredgraph.csv?id=DCOILBRENTEU). CSV endpoint is open; only the JSON API requires a free FRED key.
  - Missing days are coded `.`; pass `na_values=["."]` when reading.
  - Probe: `pd.read_csv("https://fred.stlouisfed.org/graph/fredgraph.csv?id=DCOILBRENTEU", parse_dates=["observation_date"], na_values=["."])`.
- **MoSPI IIP (general index, monthly):**
  - Landing: https://www.mospi.gov.in/iip ; catalogue: https://esankhyiki.mospi.gov.in/macroindicators?product=iip
  - Base year 2011-12 = 100 (no rebasing through 2026-Q1). Release cadence shortened from 42 to 28 days effective Apr-2025.
  - Login required: no.
- *(A 10-line probe cell per source is in `notebooks/00_data_probe.ipynb`.)*

## 7. Scope limits

- We will **not** estimate a structural causal effect of monetary policy. Any policy-attribution number we report is predictive/associational, not causal.
- We will **not** forecast future inflation past Dec 2024.
- If time permits, we may include a **lightweight exploratory dashboard** for inspecting trends and attribution shares on the held-out window. It is optional, not part of the grading core, and will **not** be production-grade, include user authentication, or update in real time.
- We will **not** model food-price or core CPI sub-indices separately. All-items CPI is the only outcome.

## 8. Risks and fallback

- **Risk:** Double ML requires reliable high-dimensional controls, which monthly macro data does not provide (120 observations). **Fallback:** drop DML; use gradient-boosted regression with permutation feature importance and clearly flag that attribution is associative, not causal.
- **Risk:** MoSPI base-year revision during the analysis window introduces a structural break. **Fallback:** use the spliced series from CMIE if available; otherwise run separate pre- and post-revision models and report both side by side.

## 9. Reproducibility checklist

- [x] `uv run main.py` executes end-to-end in ≤ 10 minutes on a MacBook.
- [x] Writes `outputs/primary_metric.json` with `{"metric_name": "oos_rmse_pp", "value": <float>, "threshold": 0.35, "passed": <bool>}`.
- [x] Writes `outputs/baseline_metric.json` with AR(1) and VECM baseline RMSEs.
- [x] `README.md` documents `uv sync && uv run main.py`.
- [x] All data fetched in-script with committed snapshot under `data/snapshots/` for reproducibility. If the optional dashboard is included, it reads from the same committed `outputs/` directory.

---

*Signed:* Hasil Tewari, Sandipan Ganguly, Parmeet Singh Majethiya
