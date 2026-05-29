from __future__ import annotations

import warnings
from functools import reduce
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches # Added for mpatches
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score, mean_absolute_error # Added mean_absolute_error
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")

# ── Config (adapted from previous cells) ──────────────────────────────────────
DATA_PATH   = Path("Unemployment.xlsx")
FIG_DIR     = Path("outputs/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)

YEAR_START  = 2000
YEAR_END    = 2023
TEST_SIZE   = 0.20
SEED        = 42
R2_THRESHOLD = 0.45
TARGET      = "unemployment_rate"

# Colour palette — consistent across all figures
COL = {
    "rf":        "#1D9E75",   # teal-green  — predictions / RF
    "residuals": "#378ADD",   # blue        — residuals / Ridge
    "gb":        "#534AB7",   # indigo      — feature importance / GB
    "quartile":  "#EF9F27",   # amber       — quartile bars
    "threshold": "#E05C5C",   # coral       — error highlights
    "grey":      "#888780",
    "lr":        "#888780", # Assuming lr (linear regression/ridge) uses grey
    "baseline":  "#888780" # Assuming baseline also uses grey
}

WB_AGGREGATES = {
    "AFE","AFW","ARB","CEB","CSS","EAP","EAR","EAS","ECA","ECS",
    "EMU","EUU","FCS","HIC","HPC","IBD","IBT","IDA","IDB","IDX",
    "LAC","LCN","LDC","LIC","LMC","LMY","LTE","MEA","MIC","MNA",
    "NAC","OED","OSS","PRE","PSS","PST","SAS","SSA","SSF","SST",
    "TEA","TEC","TLA","TMN","TSA","TSS","UMC","WLD","INX",
}

SHEETS = {
    "Unemployment": "unemployment_rate",
    "GDP Per Cap":  "gdp_per_capita",
    "Inflation":    "inflation",
    "Trade":        "trade_openness",
    "FDI":          "fdi_inflows",
    "Labour Force": "labor_force_part",
    "Urban Pop":    "urban_population_pct",
}

FEATURE_COLS = [
    "gdp_per_capita", "gdp_per_capita_growth", "inflation",
    "trade_openness", "fdi_inflows", "labor_force_part", "urban_population_pct",
]

FEATURE_LABELS = {
    "gdp_per_capita":        "GDP per capita",
    "gdp_per_capita_growth": "GDP pc growth",
    "inflation":             "Inflation",
    "trade_openness":        "Trade openness",
    "fdi_inflows":           "FDI inflows",
    "labor_force_part":      "Labour force part.",
    "urban_population_pct":  "Urban pop. %",
}

# ── Data helpers (adapted from previous cells) ────────────────────────────────

def parse_sheet(path, sheet_name, col_name):
    df = pd.read_excel(path, sheet_name=sheet_name, header=3)
    df = df.rename(columns={"Country Name": "country_name", "Country Code": "country_code"})
    df = df[~df["country_code"].isin(WB_AGGREGATES)].copy()
    year_cols = [c for c in df.columns if isinstance(c, int) and YEAR_START <= c <= YEAR_END]
    df = df[["country_code"] + year_cols]
    df = df.melt(id_vars="country_code", var_name="year", value_name=col_name)
    df["year"] = df["year"].astype(int)
    return df.dropna(subset=[col_name])


def load_and_clean():
    print("Loading and cleaning data …")
    frames = [parse_sheet(DATA_PATH, s, c) for s, c in SHEETS.items()]
    panel = reduce(lambda a, b: a.merge(b, on=["country_code", "year"], how="outer"), frames)
    panel = panel.dropna(subset=[TARGET])
    panel = panel.sort_values(["country_code", "year"]).copy()

    panel["gdp_per_capita_growth"] = (
        panel.groupby("country_code")["gdp_per_capita"].pct_change() * 100
    )
    panel["fdi_inflows"] = panel["fdi_inflows"].apply(
        lambda x: np.sign(x) * np.log1p(abs(x)) if pd.notna(x) else np.nan
    )

    miss = panel[FEATURE_COLS].isnull().sum(axis=1)
    panel = panel[miss <= 2].copy()
    for col in FEATURE_COLS:
        panel[col] = panel[col].fillna(panel[col].median())

    print(f"  Final panel: {len(panel):,} rows, {panel['country_code'].nunique()} countries")
    return panel

# ── Helper for plotting (adapted from previous cells) ─────────────────────────

def _save(fig, name):
    path = FIG_DIR / name
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    # print(f"  Saved: {path}") # Suppress print for cleaner output during execution

def _style(ax, title="", xlabel="", ylabel=""):
    ax.set_title(title, fontsize=11, fontweight="bold", pad=8)
    ax.set_xlabel(xlabel, fontsize=9, labelpad=6)
    ax.set_ylabel(ylabel, fontsize=9, labelpad=6)
    ax.tick_params(labelsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

# ── run_models function to generate results for plotting ──────────────────────
def run_models(panel):
    X = panel[FEATURE_COLS].values
    y = panel[TARGET].values
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=SEED
    )

    candidates = {
        "Ridge\n(Baseline)": Pipeline([("scaler", StandardScaler()), ("model", Ridge(alpha=1.0))]),
        "Random\nForest": RandomForestRegressor(n_estimators=200, max_depth=8, min_samples_leaf=5,
                                              random_state=SEED, n_jobs=-1),
        "Gradient\nBoosting": GradientBoostingRegressor(n_estimators=200, max_depth=4, learning_rate=0.05,
                                               subsample=0.8, random_state=SEED),
    }

    results = {}
    for name, model_pipeline in candidates.items():
        print(f"  Training and evaluating {name.replace('\n', ' ')}...")
        model_pipeline.fit(X_train, y_train)
        y_pred = model_pipeline.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)

        cv_scores = cross_val_score(model_pipeline, X_train, y_train, cv=5, scoring="r2", n_jobs=-1)

        results[name] = {
            "pred": y_pred,
            "r2": r2,
            "mae": mae,
            "cv_mean": cv_scores.mean(),
            "cv_std": cv_scores.std()
        }
    
    # Feature importance for Random Forest
    rf_model = candidates["Random\nForest"]
    # Fit again if it's a fresh model, or extract from fitted pipeline if applicable
    # For RandomForestRegressor, feature_importances_ is directly available after fit.
    # If it's a pipeline, get the inner model.
    if isinstance(rf_model, Pipeline):
        rf_estimator = rf_model.named_steps['model']
    else:
        rf_estimator = rf_model
        
    rf_imp = dict(zip(FEATURE_COLS, rf_estimator.feature_importances_))

    return y_test, results, rf_imp


# ── Fig A — Cumulative error curves and R² comparison ────────────────────────

def fig_A(y_te, results):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
    fig.suptitle("Model Comparison: Error Distribution & R² Scores", fontsize=13,
                 fontweight="bold", y=1.01)

    model_order = ["Ridge\n(Baseline)", "Gradient\nBoosting", "Random\nForest"]
    colors      = [COL["lr"], COL["gb"], COL["rf"]] # Assuming specific colors for these models
    thresholds  = np.arange(0, 15.1, 0.5) # Example thresholds

    # ── Left: Cumulative error curves ────────────────────────────────────────
    for name, color in zip(model_order, colors):
        abs_err = np.abs(y_te - results[name]["pred"])
        cov     = [(abs_err <= t).mean() for t in thresholds]
        r2_val  = results[name]["r2"]
        label   = f"{name.replace(chr(10),' ')}  (R²={r2_val:.3f})"
        ax1.plot(thresholds, cov, color=color, lw=2.2, label=label)

    # Adjusted MAE value for the annotation as it's hardcoded in the original snippet
    rf_mae_val = results["Random\nForest"]["mae"]
    ax1.plot([0, 15], [0, 0], color=COL["grey"], lw=0.5, alpha=0)  # spacer
    ax1.axvline(rf_mae_val, color=COL["grey"], ls=":", lw=1.2, alpha=0.7,
                label=f"MAE (Random Forest, {rf_mae_val:.2f} pp)")
    ax1.axhline(0.5,  color=COL["grey"], ls="--", lw=0.8, alpha=0.5)
    ax1.text(0.3, 0.52, "50% of predictions", fontsize=7, color=COL["grey"])
    ax1.set_xlim(0, 15)
    ax1.set_ylim(0, 1.02)
    ax1.legend(fontsize=8.5, loc="lower right")
    ax1.grid(True, alpha=0.15)
    _style(ax1,
           "Cumulative Error Curves: All Models",
           "Error threshold (percentage points)",
           "Proportion of test predictions within threshold")

    # ── Right: R² bar chart ───────────────────────────────────────────────────
    names_short = ["Ridge\n(Baseline)", "Gradient\nBoosting", "Random\nForest"]
    r2_vals  = [results[n]["r2"] for n in names_short]
    cv_vals  = [results[n]["cv_mean"] for n in names_short]
    x        = np.arange(len(names_short))
    width    = 0.38

    bars = ax2.bar(x, r2_vals, width=width, color=colors,
                   edgecolor="white", zorder=2, label="Test R²")
    ax2.bar(x + width, cv_vals, width=width,
            color=colors, alpha=0.45, edgecolor="white", zorder=2,
            hatch="//", label="CV R² (mean)")

    ax2.axhline(R2_THRESHOLD, color=COL["threshold"], ls="--", lw=1.6,
                label=f"Threshold ({R2_THRESHOLD})")
    ax2.axhline(results["Ridge\n(Baseline)"]["r2"], color=COL["lr"],
                ls="dotted", lw=1.4,
                label=f"Ridge baseline ({results['Ridge\n(Baseline)']['r2']:.3f})")

    for bar, val in zip(bars, r2_vals):
        ax2.text(bar.get_x() + bar.get_width() / 2,
                 val + 0.005, f"{val:.3f}",
                 ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax2.set_xticks(x + width / 2)
    ax2.set_xticklabels([n.replace("\n", " ") for n in names_short], fontsize=9)
    ax2.set_ylim(0, 0.75)
    ax2.legend(fontsize=8, loc="upper left")
    ax2.grid(axis="y", alpha=0.15)
    _style(ax2, "Model Comparison: R² Scores",
           "Model", "R²  (out-of-sample test set)")

    fig.tight_layout()
    _save(fig, "figA_cumulative_error_and_r2_comparison.png")


# ── Fig B — Random Forest deep-dive (actual vs predicted + residuals) ─────────

def fig_B(y_te, results):
    pred      = results["Random\nForest"]["pred"]
    residuals = y_te - pred
    r2        = results["Random\nForest"]["r2"]
    mae       = results["Random\nForest"]["mae"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))
    fig.suptitle("Random Forest — Detailed Diagnostics", fontsize=13,
                 fontweight="bold", y=1.01)

    # Left: actual vs predicted coloured by |error|
    sc = ax1.scatter(y_te, pred, c=np.abs(residuals), cmap="RdYlGn_r",
                     alpha=0.45, s=18, vmin=0, vmax=12)
    cb = fig.colorbar(sc, ax=ax1, fraction=0.035, pad=0.02)
    cb.set_label("Absolute error (pp)", fontsize=8)
    cb.ax.tick_params(labelsize=7)
    lims = [min(y_te.min(), pred.min()) - 1, max(y_te.max(), pred.max()) + 1]
    ax1.plot(lims, lims, "k--", lw=1.4, label="Perfect prediction")
    ax1.fill_between(lims, [l - mae for l in lims],
                           [l + mae for l in lims],
                     color=COL["grey"], alpha=0.08)
    ax1.set_xlim(lims); ax1.set_ylim(lims)
    ax1.text(0.05, 0.93,
             f"R²  = {r2:.4f}\nMAE = {mae:.2f} pp\nn   = {len(y_te):,}",
             transform=ax1.transAxes, fontsize=8.5,
             bbox=dict(boxstyle="round,pad=0.4", fc="white", alpha=0.85))
    ax1.legend(fontsize=8)
    _style(ax1, "Actual vs Predicted (test set)",
           "Actual unemployment rate (%)", "Predicted unemployment rate (%)")

    # Right: residuals vs predicted
    ax2.scatter(pred, residuals, alpha=0.35, s=14, color=COL["rf"], zorder=2)
    ax2.axhline(0,     color="black",    ls="--", lw=1.4)
    ax2.axhline( mae,  color=COL["grey"], ls=":",  lw=1.0, alpha=0.7, label=f"+\nMAE ({mae:.2f})")
    ax2.axhline(-mae,  color=COL["grey"], ls=":",  lw=1.0, alpha=0.7, label=f"−MAE")

    # Smoothed |residual| trend
    order    = np.argsort(pred)
    window   = max(1, len(pred) // 20)
    roll_abs = pd.Series(np.abs(residuals[order])).rolling(window, center=True,
                         min_periods=1).mean().values
    ax2b = ax2.twinx()
    ax2b.plot(pred[order], roll_abs, color=COL["baseline"], lw=1.8,
              label="Rolling |residual|")
    ax2b.set_ylabel("Rolling mean |residual| (pp)", fontsize=8, color=COL["baseline"])
    ax2b.tick_params(axis="y", labelcolor=COL["baseline"], labelsize=7)
    ax2b.spines["top"].set_visible(False)
    ax2b.set_ylim(0, roll_abs.max() * 2.8)

    l1, lb1 = ax2.get_legend_handles_labels()
    l2, lb2 = ax2b.get_legend_handles_labels()
    ax2.legend(l1 + l2, lb1 + lb2, fontsize=8, loc="upper left")
    _style(ax2, "Residuals vs Predicted (heteroskedasticity check)",
           "Predicted unemployment rate (%)", "Residual: actual − predicted (pp)")

    fig.tight_layout()
    _save(fig, "figB_random_forest_diagnostics.png")


# ── Fig C — Prediction interval coverage (all 3 models) ──────────────────────

def fig_C(y_te, results):
    """
    For each model: bar chart showing % of test obs within ±1, ±2, ±3, ±5 pp.
    Gives a concrete sense of practical accuracy alongside R².
    """
    model_order = ["Ridge\n(Baseline)", "Gradient\nBoosting", "Random\nForest"]
    colors      = [COL["lr"], COL["gb"], COL["rf"]]
    thresholds  = [1, 2, 3, 5]
    x           = np.arange(len(thresholds))
    width       = 0.25

    fig, ax = plt.subplots(figsize=(9, 5))

    for i, (name, color) in enumerate(zip(model_order, colors)):
        abs_err  = np.abs(y_te - results[name]["pred"])
        coverage = [(abs_err <= t).mean() * 100 for t in thresholds]
        bars     = ax.bar(x + i * width, coverage, width=width, color=color,
                          edgecolor="white", label=name.replace("\n"," "), zorder=2)
        for bar, val in zip(bars, coverage):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.8,
                    f"{val:.0f}%", ha="center", fontsize=7.5)

    ax.set_xticks(x + width)
    ax.set_xticklabels([f"±{t} pp" for t in thresholds], fontsize=10)
    ax.set_ylim(0, 110)
    ax.axhline(100, color=COL["grey"], ls=":", lw=0.8, alpha=0.5)
    ax.legend(fontsize=9, loc="upper left")
    ax.grid(axis="y", alpha=0.15)
    _style(ax,
           "Prediction Interval Coverage — % of test obs within ±X pp",
           "Error tolerance (pp)", "% of test observations within tolerance")

    fig.tight_layout()
    _save(fig, "figC_prediction_interval_coverage.png")


# ── Fig D — Feature importance with cumulative coverage line ──────────────────

def fig_D(rf_imp):
    labels = [FEATURE_LABELS[k] for k in FEATURE_COLS]
    vals   = [rf_imp[k] for k in FEATURE_COLS]
    order  = np.argsort(vals)[::-1]   # descending

    sorted_vals   = [vals[i]   for i in order]
    sorted_labels = [labels[i] for i in order]
    cumulative    = np.cumsum(sorted_vals) * 100

    fig, ax1 = plt.subplots(figsize=(9, 5))
    colors = [COL["rf"] if v >= sorted(vals)[-1] * 3 else COL["grey"]
              for v in sorted_vals]
    bars = ax1.bar(range(len(sorted_labels)), sorted_vals,
                   color=colors, edgecolor="white", width=0.6, zorder=2)
    for bar, val in zip(bars, sorted_vals):
        ax1.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.003,
                 f"{val:.3f}", ha="center", fontsize=8)

    ax2 = ax1.twinx()
    ax2.plot(range(len(sorted_labels)), cumulative,
             color=COL["baseline"], marker="o", ms=5, lw=2,
             label="Cumulative importance (%)")
    ax2.axhline(80, color=COL["threshold"], ls="--", lw=1.2, alpha=0.7,
                label="80% coverage")
    ax2.set_ylim(0, 115)
    ax2.set_ylabel("Cumulative importance (%)", fontsize=9, color=COL["baseline"])
    ax2.tick_params(axis="y", labelcolor=COL["baseline"], labelsize=8)
    ax2.spines["top"].set_visible(False)
    l2, lb2 = ax2.get_legend_handles_labels()

    ax1.axhline(1 / len(FEATURE_COLS), color=COL["grey"], ls=":",
                lw=1.2, label="Uniform baseline (1/7)")
    l1, lb1 = ax1.get_legend_handles_labels()
    ax1.legend(l1 + l2, lb1 + lb2, fontsize=8, loc="center right")

    ax1.set_xticks(range(len(sorted_labels)))
    ax1.set_xticklabels(sorted_labels, fontsize=9, rotation=15, ha="right")
    ax1.grid(axis="y", alpha=0.15)
    _style(ax1,
           "Random Forest Feature Importance with Cumulative Coverage",
           "Feature", "Importance (mean decrease in impurity)")

    fig.tight_layout()
    _save(fig, "figD_feature_importance_cumulative.png")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("Loading data …")
    panel = load_and_clean()

    print("Training models …")
    y_te, results, rf_imp = run_models(panel)

    print("\nGenerating figures …")
    fig_A(y_te, results)
    fig_B(y_te, results)
    fig_C(y_te, results)
    fig_D(rf_imp)

    print(f"\nDone — 4 figures saved to {FIG_DIR}/")
    print("\nR² summary:")
    for name, res in results.items():
        label = name.replace("\n", " ")
        print(f"  {label:<22} test R²={res['r2']:.4f}  CV R²={res['cv_mean']:.4f}±{res['cv_std']:.4f}  MAE={res['mae']:.4f}")


if __name__ == "__main__":
    main()
