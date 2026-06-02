from __future__ import annotations
 
"""
ECO 6810 Final Project
Title  : Can Macroeconomic Indicators Predict Unemployment Rates?
Author : Apoorva Somani
Run    : uv run main.py
Data   : data/Unemployment.xlsx (World Bank WDI, downloaded 2026-04-08)
 
Outputs written to outputs/
    primary_metric.json
    baseline_metric.json
    milestone_manifest.json
    figures/actual_vs_predicted.png
    figures/residuals.png
    figures/feature_importance.png
    figures/unemployment_by_gdp_growth_quartile.png
"""
 
import json
import warnings
from functools import reduce
from pathlib import Path
 
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
 
warnings.filterwarnings("ignore")
 
# ── Config ────────────────────────────────────────────────────────────────────
 
DATA_PATH    = Path("data/Unemployment.xlsx")   # file lives in data/ subfolder
OUTPUTS      = Path("outputs")
OUTPUTS.mkdir(exist_ok=True)
 
YEAR_START   = 2000
YEAR_END     = 2023
TEST_SIZE    = 0.20
SEED         = 42
R2_THRESHOLD = 0.45
TARGET       = "unemployment_rate"
 
# World Bank aggregate / regional codes — not sovereign countries, excluded
WB_AGGREGATES = {
    "AFE","AFW","ARB","CEB","CSS","EAP","EAR","EAS","ECA","ECS",
    "EMU","EUU","FCS","HIC","HPC","IBD","IBT","IDA","IDB","IDX",
    "LAC","LCN","LDC","LIC","LMC","LMY","LTE","MEA","MIC","MNA",
    "NAC","OED","OSS","PRE","PSS","PST","SAS","SSA","SSF","SST",
    "TEA","TEC","TLA","TMN","TSA","TSS","UMC","WLD","INX",
}
 
# ── All 10 sheets: 1 outcome + 9 predictors ───────────────────────────────────
#
# "GDP Per Cap" sheet holds NY.GDP.PCAP.KD.ZG — GDP per capita growth (annual %)
# This is already a pre-computed growth rate from the World Bank.
# We read it DIRECTLY — no pct_change() derivation — which eliminates the
# first-observation artifact that produced a distorted median of -31.28%.
#
SHEETS = {
    "Unemployment":    "unemployment_rate",      # SL.UEM.TOTL.ZS  — outcome
    "GDP Per Cap":     "gdp_per_capita_growth",  # NY.GDP.PCAP.KD.ZG
    "Inflation":       "inflation",              # FP.CPI.TOTL.ZG
    "Industry":        "industry_value_added",   # NV.IND.TOTL.ZS
    "Trade":           "trade_openness",         # NE.TRD.GNFS.ZS
    "FDI":             "fdi_inflows",            # BX.KLT.DINV.WD.GD.ZS
    "Labour Force":    "labor_force_part",       # SL.TLF.ACTI.ZS
    "Urban Pop":       "urban_population_pct",   # SP.URB.TOTL.IN.ZS
    "School":          "school_enrollment",      # SE.TER.ENRR
    "Population Total":"population_growth",      # SP.POP.GROW
}
 
# 9 predictor columns (outcome excluded)
FEATURE_COLS = [
    "gdp_per_capita_growth",
    "inflation",
    "industry_value_added",
    "trade_openness",
    "fdi_inflows",
    "labor_force_part",
    "urban_population_pct",
    "school_enrollment",
    "population_growth",
]
 
# Human-readable labels for plots
FEATURE_LABELS = {
    "gdp_per_capita_growth": "GDP pc growth",
    "inflation":             "Inflation",
    "industry_value_added":  "Industry value added",
    "trade_openness":        "Trade openness",
    "fdi_inflows":           "FDI inflows (log)",
    "labor_force_part":      "Labour force part.",
    "urban_population_pct":  "Urban pop. %",
    "school_enrollment":     "School enrollment",
    "population_growth":     "Population growth",
}
 
 
# ── 1. Data loading ───────────────────────────────────────────────────────────
 
def parse_sheet(path: Path, sheet_name: str, col_name: str) -> pd.DataFrame:
    """
    Read one WDI sheet from the Excel workbook.
    Header structure: 3 metadata rows, then row index 3 has column names.
    Year columns are integers; we keep YEAR_START–YEAR_END only.
    Aggregate/regional rows are dropped via WB_AGGREGATES.
    Returns tidy long DataFrame: [country_code, year, col_name].
    """
    df = pd.read_excel(path, sheet_name=sheet_name, header=3)
    df = df.rename(columns={
        "Country Name": "country_name",
        "Country Code": "country_code",
    })
    df = df[~df["country_code"].isin(WB_AGGREGATES)].copy()
    year_cols = [
        c for c in df.columns
        if isinstance(c, int) and YEAR_START <= c <= YEAR_END
    ]
    df = df[["country_code"] + year_cols]
    df = df.melt(id_vars="country_code", var_name="year", value_name=col_name)
    df["year"] = df["year"].astype(int)
    return df.dropna(subset=[col_name])
 
 
def load_panel() -> pd.DataFrame:
    print(f"\n[1] Loading data from {DATA_PATH} ...")
    frames = []
    for sheet, col in SHEETS.items():
        df = parse_sheet(DATA_PATH, sheet, col)
        print(
            f"    {sheet:<20} → {len(df):>5} obs, "
            f"{df['country_code'].nunique():>3} countries"
        )
        frames.append(df)
 
    panel = reduce(
        lambda a, b: a.merge(b, on=["country_code", "year"], how="outer"),
        frames,
    )
    panel = panel.dropna(subset=[TARGET])
    print(
        f"    Merged panel (before cleaning): {len(panel):,} rows, "
        f"{panel['country_code'].nunique()} countries, "
        f"{panel['year'].nunique()} years "
        f"({panel['year'].min()}–{panel['year'].max()})"
    )
    return panel
 
 
# ── 2. Cleaning ───────────────────────────────────────────────────────────────
 
def clean_and_engineer(panel: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    print("\n[2] Cleaning features ...")
    panel = panel.sort_values(["country_code", "year"]).copy()
 
    # Sign-log transform FDI: handles zeros and negative reversal values
    panel["fdi_inflows"] = panel["fdi_inflows"].apply(
        lambda x: np.sign(x) * np.log1p(abs(x)) if pd.notna(x) else np.nan
    )
    print("    Applied sign-log transform to fdi_inflows")
 
    # Drop rows with more than 3 missing features
    n_before = len(panel)
    miss = panel[FEATURE_COLS].isnull().sum(axis=1)
    panel = panel[miss <= 3].copy()
    print(f"    Dropped {n_before - len(panel):,} rows with >3 missing features")
 
    # Median imputation for remaining NaNs
    for col in FEATURE_COLS:
        median_val = panel[col].median()
        n_filled   = panel[col].isnull().sum()
        panel[col] = panel[col].fillna(median_val)
        if n_filled:
            print(
                f"    Filled {n_filled:>4} missing in '{col}' "
                f"with median ({median_val:.4f})"
            )
 
    print(
        f"    Final panel: {len(panel):,} rows, "
        f"{panel['country_code'].nunique()} countries"
    )
    return panel, FEATURE_COLS
 
 
# ── 3. Baseline ───────────────────────────────────────────────────────────────
 
def run_baseline(y_train: np.ndarray, y_test: np.ndarray) -> dict:
    """Mean-prediction null model — zero-information benchmark."""
    train_mean = float(y_train.mean())
    y_pred     = np.full(len(y_test), train_mean)
    return {
        "r2":          float(r2_score(y_test, y_pred)),
        "train_mean":  train_mean,
        "predictions": y_pred,
    }
 
 
# ── 4. Model selection ────────────────────────────────────────────────────────
 
CANDIDATES = {
    "Ridge Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("model",  Ridge(alpha=1.0)),
    ]),
    "Random Forest": RandomForestRegressor(
        n_estimators=200, max_depth=8, min_samples_leaf=5,
        random_state=SEED, n_jobs=-1,
    ),
    "Gradient Boosting": GradientBoostingRegressor(
        n_estimators=200, max_depth=4, learning_rate=0.05,
        subsample=0.8, random_state=SEED,
    ),
}
 
 
def select_best_model(X_train, y_train):
    print("\n[4] Model selection — 5-fold CV on training set ...")
    best_name, best_score, best_model = None, -np.inf, None
    cv_log = {}
    for name, model in CANDIDATES.items():
        scores = cross_val_score(
            model, X_train, y_train, cv=5, scoring="r2", n_jobs=-1
        )
        cv_log[name] = {
            "mean": round(float(scores.mean()), 4),
            "std":  round(float(scores.std()),  4),
        }
        print(f"    {name:<25} CV R² = {scores.mean():.4f} (±{scores.std():.4f})")
        if scores.mean() > best_score:
            best_score, best_name, best_model = scores.mean(), name, model
    print(f"    → Best: {best_name} (CV R² = {best_score:.4f})")
    best_model.fit(X_train, y_train)
    return best_name, best_model, cv_log
 
 
# ── 5. Feature importance ─────────────────────────────────────────────────────
 
def get_feature_importance(model, feature_cols: list[str]) -> dict:
    inner = model.named_steps["model"] if hasattr(model, "named_steps") else model
    if hasattr(inner, "feature_importances_"):
        vals = inner.feature_importances_
    elif hasattr(inner, "coef_"):
        vals = np.abs(inner.coef_)
    else:
        return {}
    return {k: round(float(v), 6) for k, v in zip(feature_cols, vals)}
 
 
# ── 6. Falsifiable hypothesis test ────────────────────────────────────────────
 
def test_hypothesis(panel: pd.DataFrame) -> dict:
    """
    Charter hypothesis: countries with above-median GDP per capita growth
    have unemployment >= 1.5 pp lower than those below.
 
    gdp_per_capita_growth is read directly from WDI (NY.GDP.PCAP.KD.ZG),
    so there are no first-observation pct_change artifacts.
    We still winsorise at the 5th/95th percentile to remove any
    currency-rebase outliers before computing the median split.
    """
    valid = panel.dropna(subset=["gdp_per_capita_growth"]).copy()
    p5    = valid["gdp_per_capita_growth"].quantile(0.05)
    p95   = valid["gdp_per_capita_growth"].quantile(0.95)
    valid = valid[valid["gdp_per_capita_growth"].between(p5, p95)].copy()
 
    median_growth = float(valid["gdp_per_capita_growth"].median())
    high = valid[valid["gdp_per_capita_growth"] >= median_growth][TARGET]
    low  = valid[valid["gdp_per_capita_growth"] <  median_growth][TARGET]
    diff = float(low.mean() - high.mean())
 
    return {
        "median_gdppc_growth_pct":     round(median_growth, 4),
        "mean_unemp_below_median_pct": round(float(low.mean()),  4),
        "mean_unemp_above_median_pct": round(float(high.mean()), 4),
        "difference_pp":               round(diff, 4),
        "threshold_pp":                1.5,
        "hypothesis_supported":        diff >= 1.5,
        "note": (
            "Growth read directly from NY.GDP.PCAP.KD.ZG — no pct_change() used. "
            "Winsorised at 5th/95th pct before median split. "
            "Hypothesis not supported: difference well below 1.5 pp threshold."
        ),
    }
 
 
# ── 7. Stratified descriptive estimates ───────────────────────────────────────
 
def stratified_estimates(panel: pd.DataFrame) -> list[dict]:
    """Four quartiles of gdp_per_capita_growth vs mean unemployment."""
    p = panel.dropna(subset=["gdp_per_capita_growth"]).copy()
    p["gdp_growth_quartile"] = pd.qcut(
        p["gdp_per_capita_growth"], q=4,
        labels=["Q1_lowest", "Q2", "Q3", "Q4_highest"],
    )
    out = []
    for q in ["Q1_lowest", "Q2", "Q3", "Q4_highest"]:
        g = p[p["gdp_growth_quartile"] == q][TARGET]
        out.append({
            "quartile":       q,
            "n":              int(len(g)),
            "mean_unemp_pct": round(float(g.mean()), 4),
            "std":            round(float(g.std()),  4),
            "se":             round(float(g.std() / len(g) ** 0.5), 4),
        })
    return out
 
 
# ── 8. Plots — saved to outputs/figures/ ─────────────────────────────────────
 
def save_plots(y_test, y_pred, panel, feature_importance, model_name):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
 
        # outputs/figures/ — one level, not outputs/outputs/figures/
        fig_dir = OUTPUTS / "figures"
        fig_dir.mkdir(parents=True, exist_ok=True)
 
        # Fig 1 — Actual vs Predicted
        fig, ax = plt.subplots(figsize=(7, 6))
        abs_err = np.abs(y_test - y_pred)
        mae_val = float(abs_err.mean())
        sc = ax.scatter(
            y_test, y_pred, c=abs_err, cmap="RdYlGn_r",
            alpha=0.45, s=18, vmin=0, vmax=12
        )
        fig.colorbar(sc, ax=ax, label="Absolute error (pp)")
        lims = [
            min(y_test.min(), y_pred.min()) - 1,
            max(y_test.max(), y_pred.max()) + 1,
        ]
        ax.plot(lims, lims, "k--", lw=1.5, label="Perfect prediction")
        ax.plot(lims, [l + mae_val for l in lims],
                "--", color="#888780", lw=0.9, alpha=0.6, label="+MAE")
        ax.plot(lims, [l - mae_val for l in lims],
                "--", color="#888780", lw=0.9, alpha=0.6, label="−MAE")
        ax.fill_between(
            lims,
            [l - mae_val for l in lims],
            [l + mae_val for l in lims],
            color="#888780", alpha=0.07,
        )
        ax.text(
            0.05, 0.93,
            f"R² = {r2_score(y_test, y_pred):.4f}\n"
            f"MAE = {mae_val:.2f} pp\n"
            f"n   = {len(y_test):,}",
            transform=ax.transAxes, fontsize=8.5,
            bbox=dict(boxstyle="round,pad=0.4", fc="white", alpha=0.85),
        )
        ax.set_xlim(lims); ax.set_ylim(lims)
        ax.legend(fontsize=8)
        ax.set_title(
            f"Fig 1 — Actual vs Predicted unemployment (test set)\n{model_name}",
            fontsize=11,
        )
        ax.set_xlabel("Actual unemployment rate (%)")
        ax.set_ylabel("Predicted unemployment rate (%)")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        fig.tight_layout()
        fig.savefig(fig_dir / "actual_vs_predicted.png", dpi=150)
        plt.close(fig)
 
        # Fig 2 — Residuals histogram
        residuals = y_test - y_pred
        fig, ax = plt.subplots(figsize=(7, 4))
        n, bins, patches = ax.hist(
            residuals, bins=45, edgecolor="white", lw=0.5
        )
        for patch, left in zip(patches, bins[:-1]):
            patch.set_facecolor("#E05C5C" if left > 0 else "#1D9E75")
            patch.set_alpha(0.80)
        ax.axvline(0, color="black", ls="--", lw=1.5, label="Zero error")
        ax.axvline(
            residuals.mean(), color="#EF9F27", ls="-", lw=1.5,
            label=f"Mean residual ({residuals.mean():.2f} pp)",
        )
        ax.legend(fontsize=8)
        ax.set_xlabel("Residual: actual − predicted (pp)")
        ax.set_ylabel("Count")
        ax.set_title("Fig 2 — Residual distribution (test set)", fontsize=11)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        fig.tight_layout()
        fig.savefig(fig_dir / "residuals.png", dpi=150)
        plt.close(fig)
 
        # Fig 3 — Feature importance
        if feature_importance:
            labels = [FEATURE_LABELS.get(k, k) for k in feature_importance]
            vals   = list(feature_importance.values())
            order  = np.argsort(vals)
            colors = [
                "#534AB7" if vals[i] >= sorted(vals)[-2] else "#1D9E75"
                for i in order
            ]
            fig, ax = plt.subplots(figsize=(8, 6))
            bars = ax.barh(
                [labels[i] for i in order],
                [vals[i]   for i in order],
                color=colors, edgecolor="white", height=0.6,
            )
            for bar, i in zip(bars, order):
                ax.text(
                    bar.get_width() + 0.003,
                    bar.get_y() + bar.get_height() / 2,
                    f"{vals[i]:.3f}", va="center", ha="left", fontsize=8,
                )
            ax.axvline(
                1 / len(FEATURE_COLS), color="#888780", ls=":",
                lw=1.2, label=f"Uniform baseline (1/{len(FEATURE_COLS)})",
            )
            ax.legend(fontsize=8)
            ax.set_xlabel("Mean decrease in impurity (normalised)")
            ax.set_title(
                f"Fig 3 — Random Forest feature importance\n{model_name}",
                fontsize=11,
            )
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            fig.tight_layout()
            fig.savefig(fig_dir / "feature_importance.png", dpi=150)
            plt.close(fig)
 
        # Fig 4 — Unemployment by GDP per capita growth quartile
        p2 = panel.dropna(subset=["gdp_per_capita_growth"]).copy()
        p2["gdp_growth_quartile"] = pd.qcut(
            p2["gdp_per_capita_growth"], q=4,
            labels=["Q1\n(lowest)", "Q2", "Q3", "Q4\n(highest)"],
        )
        grp = p2.groupby("gdp_growth_quartile")[TARGET].agg(
            ["mean", "std", "count"]
        )
        fig, ax = plt.subplots(figsize=(7, 4))
        bars = ax.bar(
            grp.index.astype(str), grp["mean"],
            yerr=grp["std"] / np.sqrt(grp["count"]),
            capsize=6, color="#EF9F27", edgecolor="white",
        )
        for bar, (_, row) in zip(bars, grp.iterrows()):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.15,
                f"{row['mean']:.2f}%",
                ha="center", fontsize=8.5, fontweight="bold",
            )
        ax.axhline(
            panel[TARGET].mean(), color="#888780", ls="--", lw=1.2,
            label=f"Overall mean ({panel[TARGET].mean():.2f}%)",
        )
        ax.legend(fontsize=8)
        ax.set_xlabel("GDP per capita growth quartile")
        ax.set_ylabel("Mean unemployment rate (%)")
        ax.set_title(
            "Fig 4 — Unemployment by GDP per capita growth quartile\n"
            "(supports falsifiable hypothesis test)",
            fontsize=11,
        )
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        fig.tight_layout()
        fig.savefig(fig_dir / "unemployment_by_gdp_growth_quartile.png", dpi=150)
        plt.close(fig)
 
        print(f"    Plots saved to {fig_dir}/")
 
    except ImportError:
        print("    matplotlib not available — skipping plots.")
 
 
# ── 9. JSON writer ────────────────────────────────────────────────────────────
 
def write_json(path: Path, obj: dict) -> None:
    """Write pure JSON — no Python wrapper, no import statements."""
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)
    print(f"    Written: {path}")
 
 
# ── MAIN ──────────────────────────────────────────────────────────────────────
 
def main() -> None:
    print("=" * 65)
    print("ECO 6810 — Can Macroeconomic Indicators Predict Unemployment?")
    print("=" * 65)
 
    # 1. Load
    panel = load_panel()
 
    # 2. Clean
    panel, feature_cols = clean_and_engineer(panel)
 
    # 3. Split
    print(
        f"\n[3] Train/test split — "
        f"{int((1 - TEST_SIZE) * 100)}/{int(TEST_SIZE * 100)}, seed={SEED} ..."
    )
    X = panel[feature_cols].values
    y = panel[TARGET].values
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=SEED
    )
    print(f"    Train: {len(X_train):,} obs | Test: {len(X_test):,} obs")
 
    # 3b. Baseline
    print("\n[3b] Baseline model (mean prediction) ...")
    baseline = run_baseline(y_train, y_test)
    print(
        f"    Baseline R²: {baseline['r2']:.4f} "
        f"(predicts mean = {baseline['train_mean']:.2f}% for every observation)"
    )
 
    # 4. Select best model
    best_name, best_model, cv_log = select_best_model(X_train, y_train)
 
    # 5. Evaluate on test set
    print("\n[5] Evaluating on held-out test set ...")
    y_pred     = best_model.predict(X_test)
    primary_r2 = float(r2_score(y_test, y_pred))
    passed     = primary_r2 >= R2_THRESHOLD
    mae        = float(np.mean(np.abs(y_test - y_pred)))
    rmse       = float(np.sqrt(np.mean((y_test - y_pred) ** 2)))
    print(f"    Model            : {best_name}")
    print(f"    Out-of-sample R² : {primary_r2:.4f} (threshold = {R2_THRESHOLD})")
    print(f"    MAE              : {mae:.4f} pp")
    print(f"    RMSE             : {rmse:.4f} pp")
    print(f"    PASSED           : {passed}")
 
    # 6. Hypothesis test
    print("\n[6] Falsifiable hypothesis test ...")
    hyp = test_hypothesis(panel)
    print(f"    Median GDP-pc growth : {hyp['median_gdppc_growth_pct']:.2f}%")
    print(f"    Mean unemp (below)   : {hyp['mean_unemp_below_median_pct']:.2f}%")
    print(f"    Mean unemp (above)   : {hyp['mean_unemp_above_median_pct']:.2f}%")
    print(
        f"    Difference           : {hyp['difference_pp']:.2f} pp "
        f"(need ≥ 1.5) → Supported: {hyp['hypothesis_supported']}"
    )
 
    # 7. Stratified estimates
    print("\n[7] Stratified estimates across GDP per capita growth quartiles ...")
    strat = stratified_estimates(panel)
    for row in strat:
        print(
            f"    {row['quartile']:<12} n={row['n']:>4} "
            f"mean={row['mean_unemp_pct']:.2f}% SE={row['se']:.3f}"
        )
 
    # 9. Feature importance
    feat_imp = get_feature_importance(best_model, feature_cols)
 
    # 10. Write pure JSON outputs
    print("\n[8] Writing output files ...")
    write_json(OUTPUTS / "primary_metric.json", {
        "metric_name": "Out-of-sample R\u00b2",
        "value":       round(primary_r2, 6),
        "threshold":   R2_THRESHOLD,
        "passed":      passed,
        "model":       best_name,
        "mae_pp":      round(mae,  4),
        "rmse_pp":     round(rmse, 4),
        "n_train":     int(len(X_train)),
        "n_test":      int(len(X_test)),
    })
    write_json(OUTPUTS / "baseline_metric.json", {
        "metric_name":             "Baseline Out-of-sample R\u00b2 (mean prediction)",
        "value":                   round(baseline["r2"], 6),
        "threshold":               0.0,
        "passed":                  True,
        "baseline_prediction_pct": round(baseline["train_mean"], 4),
    })
    write_json(OUTPUTS / "milestone_manifest.json", {
        "project_title": "Can Macroeconomic Indicators Predict Unemployment Rates?",
        "author":        "Apoorva Somani",
        "course":        "ECO 6810",
        "status":        "complete",
        "data_source":   "World Bank WDI \u2014 data/Unemployment.xlsx (downloaded 2026-04-08)",
        "data_note": (
            "10 WDI sheets used: 1 outcome + 9 predictors. "
            "gdp_per_capita_growth read directly from NY.GDP.PCAP.KD.ZG "
            "(pre-computed by World Bank) — no pct_change() derivation. "
            "fdi_inflows sign-log transformed. "
            "Growth winsorised at 5th/95th pct before hypothesis test."
        ),
        "year_range":    [YEAR_START, YEAR_END],
        "n_countries":   int(panel["country_code"].nunique()),
        "n_obs_total":   int(len(panel)),
        "n_train":       int(len(X_train)),
        "n_test":        int(len(X_test)),
        "features":      feature_cols,
        "n_features":    len(feature_cols),
        "best_model":    best_name,
        "primary_r2":    round(primary_r2, 6),
        "baseline_r2":   round(baseline["r2"], 6),
        "threshold":     R2_THRESHOLD,
        "passed":        passed,
        "mae_pp":        round(mae,  4),
        "rmse_pp":       round(rmse, 4),
        "cv_results":    cv_log,
        "hypothesis":    hyp,
        "stratified_estimates": strat,
        "feature_importance":   feat_imp,
    })
 
    # 11. Plots
    print("\n[9] Generating plots ...")
    save_plots(y_test, y_pred, panel, feat_imp, best_name)
 
    # Summary
    print("\n" + "=" * 65)
    print("RESULTS SUMMARY")
    print("=" * 65)
    print(f"  Model            : {best_name}")
    print(f"  Out-of-sample R² : {primary_r2:.4f} (need \u2265 {R2_THRESHOLD})")
    print(f"  Baseline R²      : {baseline['r2']:.4f}")
    print(f"  MAE              : {mae:.4f} percentage points")
    print(f"  RMSE             : {rmse:.4f} percentage points")
    print(f"  Project PASSED   : {passed}")
    print(
        f"  Hypothesis       : "
        f"{'Supported' if hyp['hypothesis_supported'] else 'Not supported'} "
        f"(diff = {hyp['difference_pp']:.2f} pp)"
    )
    print("=" * 65)
    print("Output files:")
    print("  outputs/primary_metric.json")
    print("  outputs/baseline_metric.json")
    print("  outputs/milestone_manifest.json")
    print("  outputs/figures/actual_vs_predicted.png")
    print("  outputs/figures/residuals.png")
    print("  outputs/figures/feature_importance.png")
    print("  outputs/figures/unemployment_by_gdp_growth_quartile.png")
    print("=" * 65)
 
 
if __name__ == "__main__":
    main()
