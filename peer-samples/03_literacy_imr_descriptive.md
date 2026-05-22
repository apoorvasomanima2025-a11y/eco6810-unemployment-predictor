# Example Charter — Female Literacy and Infant Mortality Across NFHS Rounds

> **Worked example for the descriptive project type.** Adapted from a real proposal by **Aalokita Roy Chowdhury and Triparna Dasgupta**, refined into charter form and shared with the class as an exemplar. A descriptive project quantifies patterns *without* making causal claims; its success is measured by the structure, sample discipline, and honesty of its comparisons, not by a coefficient sign.
>
> **Repo-first note.** In a real team project, this content would live in `CHARTER.md` inside the team repo, be revised there until approval, and could then be frozen as `charter_approved.pdf` if the team wants a locked copy.

---

## Header

| Field | Value |
|---|---|
| Team members | Aalokita Roy Chowdhury, Triparna Dasgupta |
| Project type | Descriptive |
| Estimated hours per person | 45 |
| Charter version | v1 |
| Date | 2026-04-18 |

---

## 1. Problem and stakeholder

District-level IMR remains a NITI Aayog Aspirational Districts indicator. NITI's annual district-ranking exercise uses cross-sectional correlates to prioritise interventions, and female-literacy programmes are repeatedly invoked but rarely stratified by baseline IMR level or cross-round comparison. A NITI analyst preparing the FY 2026-27 Aspirational Districts report needs a clear descriptive picture of how the female-literacy / IMR association varies across district baselines, how it has evolved between NFHS-4 and NFHS-5, and how much of the pairwise association persists after adjustment for household wealth, healthcare access, sanitation, and urbanisation.

## 2. Main outcome variable

- **Name:** district-level Infant Mortality Rate
- **Unit:** deaths per 1000 live births (0–200 range)
- **Source:**
  - **NFHS-4:** direct from the IIPS district factsheets (NFHS-4 publishes district-level IMR), accessed via the compiled CSV at https://raw.githubusercontent.com/SaiSiddhardhaKalla/NFHS/main/India.csv (which carries Census 2011 district codes `ST_CEN_CD` / `DT_CEN_CD`).
  - **NFHS-5:** the IIPS district factsheet for NFHS-5 does **not** publish district-level IMR (only state-level). We therefore use the peer-reviewed modelled estimates from Mendeley Data (doi:10.17632/t3s358sfzg.1, CC-BY 4.0), which back-cast district-level IMR from NFHS-5 state-level IMR plus district covariates. Every NFHS-5 IMR figure in our outputs is labelled "modelled (Mendeley 2022)".
- **Population / panel:** the ~640-district NFHS-4 panel mapped to its NFHS-5 counterpart via the `DT_CEN_CD` column attached to the compiled NFHS CSV (name-reconciled to PC11 codes); unmatched districts dropped and documented.

## 3. Main quantitative success threshold

The project delivers all four of:

(a) **Round-specific district heatmaps** of both IMR and female literacy, for NFHS-4 and NFHS-5 (4 maps total), rendered at state + district resolution with sample-size-annotated legends.

(b) **Stratified IMR–literacy pairs across at least 5 literacy quintiles per round**, each quintile containing ≥ 100 districts, with mean, SD, and bootstrapped 95% CI per cell.

(c) A **t-test** comparing mean IMR between high-literacy (top quintile) and low-literacy (bottom quintile) districts, *reported per round*, with effect size (Cohen's d), 95% CI, and a plain-English caveat that the test is associational.

(d) An **adjusted regression** of IMR on female-literacy rate with controls for household wealth index, healthcare access, sanitation, and urbanisation. Reported separately for NFHS-4 and NFHS-5. Standardised partial coefficient with 95% CI in each round.

(e) A documented **district-match rate ≥ 88%** of NFHS-4 districts to NFHS-5.

## 4. Baseline to beat

Existing published cross-sectional correlation estimates between female literacy and IMR at the India district level: the widely cited Kumar & Kumar (2021) cross-sectional correlation of approximately −0.52, pooled across rounds. Our charter is not to beat this number — it is to *improve the resolution* by reporting the correlation separately by round, by literacy stratum, and before-and-after adjustment. The baseline CSV commits the pooled correlation we compute ourselves, for direct comparison to the published figure.

## 5. Falsifiable hypothesis

After adjusting for household wealth, healthcare access, sanitation, and urbanisation, the **standardised partial coefficient of female literacy on IMR is negative in both rounds, and at least 20% larger in absolute magnitude in NFHS-5 than in NFHS-4**. If the NFHS-5 adjusted coefficient is smaller in absolute magnitude than the NFHS-4 coefficient, or indistinguishable from zero, the hypothesis is rejected.

## 6. Data sources and access plan

All sources are open; no DHS microdata registration is required for our design.

- **NFHS district-level compiled CSV (female literacy, IMR-NFHS-4, sanitation, electricity, health-insurance, institutional-births):**
  - https://raw.githubusercontent.com/SaiSiddhardhaKalla/NFHS/main/India.csv — third-party parse of the IIPS district factsheets (35,465 rows, 640 districts × ~104 indicators), with `ST_CEN_CD` and `DT_CEN_CD` Census 2011 codes attached.
  - Backup / validation: https://raw.githubusercontent.com/pratapvardhan/NFHS-5/master/NFHS-5-Districts.csv (pratapvardhan's Harvard Dataverse–published version, CC-BY 4.0, DOI 10.7910/DVN/42WNZF). We spot-check ≥ 20 district cells against the IIPS factsheet PDFs before publishing.
  - Login required: no.
- **NFHS-5 district-level IMR (modelled):**
  - Mendeley dataset, doi:10.17632/t3s358sfzg.1, CC-BY 4.0, https://data.mendeley.com/datasets/t3s358sfzg/1 — district-level NFHS-5 IMR modelled from state IMR plus district covariates. Used because the IIPS NFHS-5 *district factsheet* does not publish IMR directly.
  - Login required: no.
- **Census 2011 Primary Census Abstract (district master + urban share):**
  - Direct .xlsx (India + 36 states/UTs + 640 districts): https://censusindia.gov.in/nada/index.php/catalog/6191/download/9268/DDW_PCA0000_2011_Indiastatedist.xlsx (~1.38 MB).
  - Urban share = `TRU=Urban / TRU=Total` on `TOT_P`. Literacy columns `P_LIT` / `F_LIT` are Census literacy; NFHS female-literacy is pulled separately from the NFHS CSV (not Census).
  - Licence: GODL India; login required: no.
- **District crosswalk (NFHS name ↔ Census PC11 code):**
  - Primary: the `ST_CEN_CD` + `DT_CEN_CD` columns in the compiled NFHS CSV above already serve as the crosswalk. DDL's SHRUG does **not** ship a dedicated NFHS-4 ↔ NFHS-5 module; its COVID build scripts (https://github.com/devdatalab/covid) demonstrate the same name-reconciliation approach.
  - Supplementary: LGD (Local Government Directory) at https://lgdirectory.gov.in/downloadDirectory.do for any codes the CSV misses.
  - Licence: open; login required: no.
- *(Access-probe notebook: `notebooks/00_load_district_file.ipynb` loads one row from each of: the compiled NFHS CSV, the Mendeley modelled-IMR CSV, and the Census PCA xlsx.)*

**Gotcha we will handle in-script:** the IIPS NFHS portal at `https://www.nfhsiips.in/nfhsuser/nfhs5.php` has a broken SSL certificate chain as of 2026-Q1. We do not fetch from IIPS directly in `main.py`; we use the GitHub-hosted compiled CSV and the DHS Program mirror for any factsheet cross-check (`requests.get(..., verify=False)` only if we need a raw IIPS PDF, which is out of scope).

## 7. Scope limits

- We will **not** make causal claims about literacy → IMR. The regression is an *adjustment*, not an identification strategy. Every table headline explicitly says "associational".
- We will **not** run panel / fixed-effects estimators across rounds. Each round is analysed separately.
- We will **not** use DHS microdata or NFHS wealth-quintile distributions. We substitute a factsheet-based wealth proxy (PCA across household electricity, sanitation, health-insurance, and improved-drinking-water indicators) and document the substitution.
- We will **not** treat the Mendeley modelled NFHS-5 district IMR as a direct observation. Every NFHS-5 IMR figure is labelled "modelled" in tables, heatmaps, and the report text.
- We will **not** analyse gender-specific IMR (male vs female infants).
- We will **not** harmonise the ~40 districts with boundary changes we cannot cleanly match — they are dropped and the drop rate is reported.
- We will **not** build an interactive dashboard. Output is a PDF report with committed static heatmaps + CSVs.

## 8. Risks and fallback

- **Risk:** The Mendeley modelled NFHS-5 district IMR introduces model-induced correlation that inflates the literacy–IMR relationship beyond what NFHS-5 direct observation would show. **Fallback:** Report the primary analysis restricted to NFHS-4 (where district IMR is directly observed) as a robustness panel alongside the two-round analysis. If the NFHS-4-only finding contradicts the two-round finding, the report leads with the NFHS-4-only result and flags the modelled-data discrepancy as the headline uncertainty.
- **Risk:** District crosswalk quality turns out worse than expected and the match rate falls below 88%. **Fallback:** Aggregate to state-level analysis, redo all stratified tables and regressions at that level, and document the drop in spatial resolution.
- **Risk:** Covariates are missing for > 10% of districts and the adjusted regression sample shrinks. **Fallback:** Report both the unadjusted correlation (full sample) and the adjusted partial coefficient (restricted sample), with the sample-size gap disclosed per table.

## 9. Reproducibility checklist

- [x] `uv run main.py` regenerates all heatmaps, tables, correlations, t-tests, and regressions in under 3 minutes.
- [x] Writes `outputs/primary_metric.json` with `{"metric_name": "match_rate_pct", "value": <float>, "threshold": 88.0, "passed": <bool>, "n_quintiles_per_round": <int>, "min_cell_n": <int>, "nfhs4_adjusted_beta": <float>, "nfhs5_adjusted_beta": <float>}`.
- [x] Writes `outputs/baseline_metric.json` with the pooled cross-round Pearson correlation for reference against the published figure.
- [x] `README.md` documents the build, output CSVs, and the four heatmap PNGs.
- [x] Every table in the final PDF is written to a committed CSV under `outputs/tables/`; every heatmap to `outputs/figures/`.

---

*Signed:* Aalokita Roy Chowdhury, Triparna Dasgupta
