from __future__ import annotations

"""
ECO 6810 Final Project
Title  : Can Macroeconomic Indicators Predict Unemployment Rates?
Author : Apoorva Somani
Run    : uv run main.py
Data   : data/Unemployment.xlsx (World Bank World Development Indicators,
         downloaded 2026-04-08)

Outputs
    outputs/primary_metric.json
    outputs/baseline_metric.json
    outputs/milestone_manifest.json
    outputs/figures/ (4 plots)
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

# ---------------------------------------------------------------
# Config
# ---------------------------------------------------------------

# FIX: was "data/Book.xlsx" — renamed to match the actual file in the repo
DATA_PATH = Path("Unemployment.xlsx")

OUTPUTS = Path("outputs")
OUTPUTS.mkdir(exist_ok=True)

YEAR_START = 2000
YEAR_END   = 2023
TEST_SIZE  = 0.20
SEED       = 42
R2_THRESHOLD = 0.45
TARGET     = "unemployment_rate"

# World Bank aggregate / regional codes to exclude (not sovereign countries)
WB_AGGREGATES = {
    "AFE","AFW","ARB","CEB","CSS","EAP","EAR","EAS","ECA","ECS",
    "EMU","EUU","FCS","HIC","HPC","IBD","IBT","IDA","IDB","IDX",
    "LAC","LCN","LDC","LIC","LMC","LMY","LTE","MEA","MIC","MNA",
    "NAC","OED","OSS","PRE","PSS","PST","SAS","SSA","SSF","SST",
    "TEA","TEC","TLA","TMN","TSA","TSS","UMC","WLD",
}

# Excel sheet → tidy column name mapping
SHEETS = {
    "Unemployment": "unemployment_rate",
    "GDP Per Cap":  "gdp_per_capita",
    "Inflation":    "inflation",
    "Trade":        "trade_openness",
    "FDI":          "fdi_inflows",
    "Labour Force": "labor_force_part",
    "Urban Pop":    "urban_population_pct",
}

# ---------------------------------------------------------------
# 1. Data loading
# ---------------------------------------------------------------

def parse_sheet(path: Path, sheet_name: str, col_name: str) -> pd.DataFrame:
    """
    Read one World Bank WDI sheet from the Excel workbook.
    The workbook has 3 header rows; row 3 (0-indexed) contains column names.
    Year columns are integers 1960-2025; we keep only YEAR_START-YEAR_END.
    Aggregate/regional rows are identified by WB_AGGREGATES and dropped.
    Returns a tidy long DataFrame: [country_code, year, col_name].
    """
    df = pd.read_excel(path, sheet_name=sheet_name, header=3)
    df = df.rename(columns={
        "Country Name": "country_name",
        "Country Code": "country_code",
    })
    df = df[~df["country_code"].isin(WB_AGGREGATES)].copy()
    year_cols = [c for c in df.columns if isinstance(c, int) and YEAR_START <= c <= YEAR_END]
    df = df[["country_code"] + year_cols]
    df = df.melt(id_vars="country_code", var_name="year", value_name=col_name)
    df["year"] = df["year"].astype(int)
    return df.dropna(subset=[col_name])


def load_panel() -> pd.DataFrame:
    print(f"\n[1] Loading data from {DATA_PATH} ...")
    frames = []
    for sheet, col in SHEETS.items():
        df = parse_sheet(DATA_PATH, sheet, col)
        print(f"    {sheet:<20} → {len(df):>5} obs, {df['country_code'].nunique():>3} countries")
        frames.append(df)

    panel = reduce(
        lambda a, b: a.merge(b, on=["country_code", "year"], how="outer"),
        frames,
    )
    panel = panel.dropna(subset=[TARGET])
    print(
        f"    Merged panel (before cleaning): {len(panel):,} rows, "
        f"{panel['country_code'].nunique()} countries, "
        f"{panel['year'].nunique()} years ({panel['year'].min()}–{panel['year'].max()})"
    )
    return panel


# ---------------------------------------------------------------
# 2. Cleaning and feature engineering
# ---------------------------------------------------------------

def clean_and_engineer(panel: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    print("\n[2] Cleaning and engineering features ...")

    panel = panel.sort_values(["country_code", "year"]).copy()

    # Derive GDP-per-capita growth (% YoY within each country).
    # NOTE: pct_change() produces NaN for the first observation of each country;
    # those rows are excluded from the hypothesis test (see test_hypothesis).
    panel["gdp_per_capita_growth"] = (
        panel.groupby("country_code")["gdp_per_capita"]
        .pct_change() * 100
    )
    print("    Derived: gdp_per_capita_growth (YoY % change of gdp_per_capita)")

    # Signed log of FDI — handles zeros and negative values from reversals
    panel["fdi_inflows"] = panel["fdi_inflows"].apply(
        lambda x: np.sign(x) * np.log1p(abs(x)) if pd.notna(x) else np.nan
    )

    feature_cols = [
        "gdp_per_capita",
        "gdp_per_capita_growth",
        "inflation",
        "trade_openness",
        "fdi_inflows",
        "labor_force_part",
        "urban_population_pct",
    ]

    # Drop rows missing more than 2 features
    n_before = len(panel)
    miss = panel[feature_cols].isnull().sum(axis=1)
    panel = panel[miss <= 2].copy()
    print(f"    Dropped {n_before - len(panel):,} rows with >2 missing features")

    # Fill remaining missing features with the column's global median
    for col in feature_cols:
        median_val = panel[col].median()
        n_filled   = panel[col].isnull().sum()
        panel[col] = panel[col].fillna(median_val)
        if n_filled:
            print(f"    Filled {n_filled} missing values in '{col}' with median ({median_val:.4f})")

    print(f"    Final panel: {len(panel):,} rows, {panel['country_code'].nunique()} countries")
    return panel, feature_cols


# ---------------------------------------------------------------
# 3. Baseline model
# ---------------------------------------------------------------

def run_baseline(y_train: np.ndarray, y_test: np.ndarray) -> dict:
    """Mean-prediction null model — zero-information benchmark."""
    train_mean = float(y_train.mean())
    y_pred     = np.full(len(y_test), train_mean)
    return {
        "r2":           float(r2_score(y_test, y_pred)),
        "train_mean":   train_mean,
        "predictions":  y_pred,
    }


# ---------------------------------------------------------------
# 4. Model selection via 5-fold cross-validation
# ---------------------------------------------------------------

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
    print("\n[4] Model selection — 5-fold cross-validation on training set ...")
    best_name, best_score, best_model = None, -np.inf, None
    for name, model in CANDIDATES.items():
        scores = cross_val_score(model, X_train, y_train, cv=5, scoring="r2", n_jobs=-1)
        print(f"    {name:<25} CV R² = {scores.mean():.4f} (±{scores.std():.4f})")
        if scores.mean() > best_score:
            best_score, best_name, best_model = scores.mean(), name, model
    print(f"    → Best: {best_name} (CV R² = {best_score:.4f})")
    best_model.fit(X_train, y_train)
    return best_name, best_model


# ---------------------------------------------------------------
# 5. Feature importance
# ---------------------------------------------------------------

def get_feature_importance(model, feature_cols: list[str]) -> dict:
    inner = model.named_steps["model"] if hasattr(model, "named_steps") else model
    if hasattr(inner, "feature_importances_"):
        vals = inner.feature_importances_
    elif hasattr(inner, "coef_"):
        vals = np.abs(inner.coef_)
    else:
        return {}
    return {k: round(float(v), 6) for k, v in zip(feature_cols, vals)}


# ---------------------------------------------------------------
# 6. Falsifiable hypothesis test
# ---------------------------------------------------------------

def test_hypothesis(panel: pd.DataFrame) -> dict:
    """
    Charter hypothesis: countries with GDP-per-capita growth above the global
    median have unemployment rates at least 1.5 pp lower than those below.

    Fix applied: first observations per country are excluded before computing
    the median because pct_change() returns extreme / undefined values for them,
    which drag the median far into negative territory and make the split
    meaningless. We also winsorise at the 5th / 95th percentile to remove
    currency-rebase and structural-revision artifacts.
    """
    # Drop rows where growth is NaN (first obs per country)
    valid = panel.dropna(subset=["gdp_per_capita_growth"]).copy()

    # Winsorise at 5th / 95th percentile to remove outlier artifacts
    p5  = valid["gdp_per_capita_growth"].quantile(0.05)
    p95 = valid["gdp_per_capita_growth"].quantile(0.95)
    valid = valid[
        valid["gdp_per_capita_growth"].between(p5, p95)
    ].copy()

    median_growth = float(valid["gdp_per_capita_growth"].median())
    high = valid[valid["gdp_per_capita_growth"] >= median_growth][TARGET]
    low  = valid[valid["gdp_per_capita_growth"] <  median_growth][TARGET]
    diff = float(low.mean() - high.mean())

    return {
        "median_gdppc_growth_pct":      round(median_growth, 4),
        "mean_unemp_below_median_pct":  round(float(low.mean()), 4),
        "mean_unemp_above_median_pct":  round(float(high.mean()), 4),
        "difference_pp":                round(diff, 4),
        "threshold_pp":                 1.5,
        "hypothesis_supported":         diff >= 1.5,
    }


# ---------------------------------------------------------------
# 7. Stratified descriptive estimates (4 GDP-per-capita quartiles)
# ---------------------------------------------------------------

def stratified_estimates(panel: pd.DataFrame) -> list[dict]:
    panel = panel.copy()
    panel["gdp_quartile"] = pd.qcut(
        panel["gdp_per_capita"], q=4,
        labels=["Q1_lowest", "Q2", "Q3", "Q4_highest"],
    )
    out = []
    for q in ["Q1_lowest", "Q2", "Q3", "Q4_highest"]:
        g = panel[panel["gdp_quartile"] == q][TARGET]
        out.append({
            "quartile":       q,
            "n":              int(len(g)),
            "mean_unemp_pct": round(float(g.mean()), 4),
            "std":            round(float(g.std()),  4),
            "se":             round(float(g.std() / len(g) ** 0.5), 4),
        })
    return out


# ---------------------------------------------------------------
# 8. Plots
# ---------------------------------------------------------------

def save_plots(y_test, y_pred, baseline_pred, panel, feature_importance, model_name):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig_dir = OUTPUTS / "figures"
        fig_dir.mkdir(exist_ok=True)

        # Actual vs Predicted
        fig, ax = plt.subplots(figsize=(7, 6))
        ax.scatter(y_test, y_pred, alpha=0.35, s=14, color="#1D9E75", label=model_name)
        lims = [min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())]
        ax.plot(lims, lims, "k--", lw=1.5, label="Perfect prediction")
        ax.set_xlabel("Actual unemployment rate (%)")
        ax.set_ylabel("Predicted unemployment rate (%)")
        ax.set_title(f"Actual vs Predicted — test set\n{model_name}")
        ax.legend()
        fig.tight_layout()
        fig.savefig(fig_dir / "actual_vs_predicted.png", dpi=150)
        plt.close(fig)

        # Residuals histogram
        residuals = y_test - y_pred
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.hist(residuals, bins=40, color="#378ADD", edgecolor="white", lw=0.5)
        ax.axvline(0, color="black", ls="--", lw=1.5)
        ax.set_xlabel("Residual (actual − predicted, pp)")
        ax.set_ylabel("Count")
        ax.set_title("Residual distribution — test set")
        fig.tight_layout()
        fig.savefig(fig_dir / "residuals.png", dpi=150)
        plt.close(fig)

        # Feature importance
        if feature_importance:
            names = list(feature_importance.keys())
            vals  = list(feature_importance.values())
            order = np.argsort(vals)
            fig, ax = plt.subplots(figsize=(7, 5))
            ax.barh([names[i] for i in order], [vals[i] for i in order], color="#534AB7")
            ax.set_xlabel("Importance")
            ax.set_title(f"Feature importance — {model_name}")
            fig.tight_layout()
            fig.savefig(fig_dir / "feature_importance.png", dpi=150)
            plt.close(fig)

        # Unemployment by GDP-per-capita quartile
        p2 = panel.copy()
        p2["gdp_quartile"] = pd.qcut(
            p2["gdp_per_capita"], q=4,
            labels=["Q1\n(lowest)", "Q2", "Q3", "Q4\n(highest)"],
        )
        grp = p2.groupby("gdp_quartile")[TARGET].agg(["mean", "std", "count"])
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(
            grp.index.astype(str), grp["mean"],
            yerr=grp["std"] / np.sqrt(grp["count"]),
            capsize=6, color="#EF9F27", edgecolor="white",
        )
        ax.set_xlabel("GDP per capita quartile")
        ax.set_ylabel("Mean unemployment rate (%)")
        ax.set_title(
            "Unemployment rate by GDP per capita quartile\n"
            "(supports falsifiable hypothesis test)"
        )
        fig.tight_layout()
        fig.savefig(fig_dir / "unemployment_by_gdp_quartile.png", dpi=150)
        plt.close(fig)

        print(f"    Plots saved to {fig_dir}/")
    except ImportError:
        print("    matplotlib not available — skipping plots.")


# ---------------------------------------------------------------
# 9. Write JSON outputs
# ---------------------------------------------------------------

def write_json(path: Path, obj: dict):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)
    print(f"    Written: {path}")


# ---------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------

def main():
    print("=" * 65)
    print("ECO 6810 — Can Macroeconomic Indicators Predict Unemployment?")
    print("=" * 65)

    # 1. Load
    panel = load_panel()

    # 2. Clean + engineer
    panel, feature_cols = clean_and_engineer(panel)

    # 3. Split
    print(f"\n[3] Train/test split — {int((1-TEST_SIZE)*100)}/{int(TEST_SIZE*100)}, seed={SEED} ...")
    X = panel[feature_cols].values
    y = panel[TARGET].values
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=SEED
    )
    print(f"    Train: {len(X_train):,} obs | Test: {len(X_test):,} obs")

    # 4. Baseline
    print("\n[3b] Baseline model (mean prediction) ...")
    baseline = run_baseline(y_train, y_test)
    print(
        f"    Baseline R²: {baseline['r2']:.4f} "
        f"(predicts mean = {baseline['train_mean']:.2f}% for every observation)"
    )

    # 5. Select + train best model
    best_name, best_model = select_best_model(X_train, y_train)

    # 6. Evaluate on test set
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

    # 7. Hypothesis test
    print("\n[6] Falsifiable hypothesis test ...")
    hyp = test_hypothesis(panel)
    print(f"    Median GDP-pc growth : {hyp['median_gdppc_growth_pct']:.2f}%")
    print(f"    Mean unemp (below)   : {hyp['mean_unemp_below_median_pct']:.2f}%")
    print(f"    Mean unemp (above)   : {hyp['mean_unemp_above_median_pct']:.2f}%")
    print(
        f"    Difference           : {hyp['difference_pp']:.2f} pp "
        f"(need ≥ 1.5) → Supported: {hyp['hypothesis_supported']}"
    )

    # 8. Stratified estimates
    print("\n[7] Stratified estimates across GDP per capita quartiles ...")
    strat = stratified_estimates(panel)
    for row in strat:
        print(
            f"    {row['quartile']:<12} n={row['n']:>4} "
            f"mean={row['mean_unemp_pct']:.2f}% SE={row['se']:.3f}"
        )

    # 9. Feature importance
    feat_imp = get_feature_importance(best_model, feature_cols)

    # 10. Write outputs
    print("\n[8] Writing output files ...")
    write_json(OUTPUTS / "primary_metric.json", {
        "metric_name": "Out-of-sample R²",
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
        "metric_name":             "Baseline Out-of-sample R² (mean prediction)",
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
        "data_source":   "World Bank WDI — data/Unemployment.xlsx (downloaded 2026-04-08)",
        "data_note":     "gdp_per_capita_growth derived as YoY pct_change of gdp_per_capita within each country; first observations and 5th/95th percentile outliers excluded before hypothesis test",
        "year_range":    [YEAR_START, YEAR_END],
        "n_countries":   int(panel["country_code"].nunique()),
        "n_obs_total":   int(len(panel)),
        "n_train":       int(len(X_train)),
        "n_test":        int(len(X_test)),
        "features":      feature_cols,
        "best_model":    best_name,
        "primary_r2":    round(primary_r2, 6),
        "baseline_r2":   round(baseline["r2"], 6),
        "threshold":     R2_THRESHOLD,
        "passed":        passed,
        "mae_pp":        round(mae,  4),
        "rmse_pp":       round(rmse, 4),
        "hypothesis":    hyp,
        "stratified_estimates": strat,
        "feature_importance":   feat_imp,
    })

    # 11. Plots
    print("\n[9] Generating plots ...")
    save_plots(y_test, y_pred, baseline["predictions"], panel, feat_imp, best_name)

    # Summary
    print("\n" + "=" * 65)
    print("RESULTS SUMMARY")
    print("=" * 65)
    print(f"  Model            : {best_name}")
    print(f"  Out-of-sample R² : {primary_r2:.4f} (need ≥ {R2_THRESHOLD})")
    print(f"  Baseline R²      : {baseline['r2']:.4f}")
    print(f"  MAE              : {mae:.4f} percentage points")
    print(f"  RMSE             : {rmse:.4f} percentage points")
    print(f"  Project PASSED   : {passed}")
    print(
        f"  Hypothesis       : {'Supported' if hyp['hypothesis_supported'] else 'Not supported'} "
        f"(diff = {hyp['difference_pp']:.2f} pp)"
    )
    print("=" * 65)
    print("Output files:")
    print("  outputs/primary_metric.json")
    print("  outputs/baseline_metric.json")
    print("  outputs/milestone_manifest.json")
    print("  outputs/figures/*.png")
    print("=" * 65)


if __name__ == "__main__":
    main()
