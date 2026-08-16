"""
Stage 4: Exploratory Data Analysis on the fraud-model feature set

Standalone diagnostic — not wired into main.py. Meant to be read by a human
before training a model on a feature set, not as an automated pass/fail
gate. Checks each candidate feature's raw relationship to the proxy label
(is_entity_owner, among homestead parcels) *before* any model gets fit to
it: prevalence, missingness, correlation, and — critically — a decile
dose-response table for continuous features, which is the specific check
that would have caught airbnb_rate's non-monotonic zero/nonzero SHAP
artifact before ever training a model on it (see docs/fraud_model_pivot.md).

Usage:
    python scripts/eda_fraud_features.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).parent.parent
INPUT_PATH = PROJECT_ROOT / "data" / "products" / "parcel_features.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "products" / "eda_fraud_features_summary.csv"

BINARY_FEATURES = ["mailing_ne_situs", "out_of_state_owner"]
NUMERIC_FEATURES = ["imprvActualYearBuilt", "imprvMainArea", "land_size_sqft"]
CATEGORICAL_FEATURES = ["imprvClass", "imprvCondition"]
LABEL_COL = "is_entity_owner"

LOW_SIGNAL_THRESHOLD = 0.02  # |correlation| below this gets flagged as a WARNING
SMALL_CATEGORY_N = 200  # categories with fewer rows than this get flagged as unstable
N_DECILES = 10


def load_homestead_data(input_path: Path) -> pd.DataFrame:
    """Restrict to the same population train_fraud_model.py trains on."""
    df = pd.read_csv(input_path)
    return df[df["has_homestead"] == 1].copy()


def summarize_binary_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prevalence, missingness, correlation with the label, and the label rate
    at flag=1 vs flag=0 (lift) for each binary feature.
    """
    rows = []
    for col in BINARY_FEATURES:
        s = df[col]
        missing_pct = s.isna().mean()
        prevalence = (s == 1).mean()
        corr = s.corr(df[LABEL_COL])
        rate_0 = df.loc[s == 0, LABEL_COL].mean()
        rate_1 = df.loc[s == 1, LABEL_COL].mean()
        lift = rate_1 / rate_0 if rate_0 else np.nan
        rows.append({
            "feature": col, "type": "binary",
            "prevalence": round(prevalence, 4),
            "missing_pct": round(missing_pct, 4),
            "correlation": round(corr, 4),
            "label_rate_flag0": round(rate_0, 4),
            "label_rate_flag1": round(rate_1, 4),
            "lift": round(lift, 2) if pd.notna(lift) else np.nan,
        })
    return pd.DataFrame(rows)


def summarize_numeric_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Distribution stats, missingness, Pearson + Spearman correlation, and a
    decile dose-response table for each continuous feature. Prints a
    non-monotonicity warning directly (the dose-response shape doesn't fit
    neatly into the single-row summary table returned to the caller).
    """
    rows = []
    for col in NUMERIC_FEATURES:
        s = df[col]
        missing_pct = s.isna().mean()
        pearson = s.corr(df[LABEL_COL], method="pearson")
        spearman = s.corr(df[LABEL_COL], method="spearman")
        rows.append({
            "feature": col, "type": "numeric",
            "missing_pct": round(missing_pct, 4),
            "mean": round(s.mean(), 2), "std": round(s.std(), 2),
            "min": round(s.min(), 2), "median": round(s.median(), 2), "max": round(s.max(), 2),
            "pearson_corr": round(pearson, 4),
            "spearman_corr": round(spearman, 4),
        })

        print(f"\n  Decile dose-response - {col}:")
        try:
            deciles = pd.qcut(s, N_DECILES, duplicates="drop")
            dose_response = df.groupby(deciles, observed=True)[LABEL_COL].mean()
            for interval, rate in dose_response.items():
                print(f"    {str(interval):30s} label rate = {rate:.4f}")
            rates = dose_response.to_numpy()
            is_monotonic = np.all(np.diff(rates) >= 0) or np.all(np.diff(rates) <= 0)
            if not is_monotonic:
                print(f"    WARNING: label rate is NOT monotonic across {col} deciles - "
                      f"check for a step-function/threshold artifact like the one found in airbnb_rate.")
        except ValueError as e:
            print(f"    Could not bin into deciles ({e}) - likely too many repeated values.")

    return pd.DataFrame(rows)


def summarize_categorical_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Value counts, missingness, and label-rate crosstab for each categorical
    feature. Warns on categories with too few rows for a stable estimate.
    Also reports a rough correlation using the same integer-code encoding
    train_fraud_model.py uses internally, for comparability with the
    numeric/binary features above.
    """
    rows = []
    for col in CATEGORICAL_FEATURES:
        s = df[col]
        missing_pct = s.isna().mean()
        codes = s.astype("category").cat.codes.astype("float64")
        codes = codes.where(s.notna())
        corr = codes.corr(df[LABEL_COL])

        rows.append({
            "feature": col, "type": "categorical",
            "missing_pct": round(missing_pct, 4),
            "n_categories": s.nunique(),
            "correlation": round(corr, 4),
        })

        print(f"\n  Label rate by category - {col}:")
        crosstab = df.groupby(col, observed=True)[LABEL_COL].agg(["mean", "count"])
        crosstab = crosstab.sort_values("count", ascending=False)
        for cat, row in crosstab.iterrows():
            flag = "  (small n, unstable)" if row["count"] < SMALL_CATEGORY_N else ""
            print(f"    {str(cat):15s} label rate = {row['mean']:.4f}  n={int(row['count']):,}{flag}")

    return pd.DataFrame(rows)


def cross_feature_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Multicollinearity check across all 7 candidate features. Categorical
    columns are integer-coded (same convention as train_fraud_model.py) so
    they can sit in the same matrix as the numeric/binary ones.
    """
    cols = {}
    for col in BINARY_FEATURES + NUMERIC_FEATURES:
        cols[col] = df[col]
    for col in CATEGORICAL_FEATURES:
        codes = df[col].astype("category").cat.codes.astype("float64")
        cols[col] = codes.where(df[col].notna())

    matrix_df = pd.DataFrame(cols)
    return matrix_df.corr()


def print_low_signal_warnings(summary: pd.DataFrame) -> None:
    corr_col = summary["correlation"].fillna(summary.get("pearson_corr"))
    low_signal = summary[corr_col.abs() < LOW_SIGNAL_THRESHOLD]
    if len(low_signal) == 0:
        print("\n  No features fell below the low-signal threshold "
              f"(|correlation| < {LOW_SIGNAL_THRESHOLD}).")
        return
    print(f"\n  WARNING: {len(low_signal)} feature(s) below the low-signal threshold "
          f"(|correlation| < {LOW_SIGNAL_THRESHOLD}) - don't trust these just because "
          f"they're in the feature list:")
    for _, row in low_signal.iterrows():
        print(f"    {row['feature']}")


def run():
    print("=" * 60)
    print("Stage 4: EDA on Fraud Model Feature Set")
    print("=" * 60)

    df = load_homestead_data(INPUT_PATH)
    print(f"\nHomestead parcels: {len(df):,}  |  "
          f"Entity-owned (label=1): {df[LABEL_COL].sum():,} ({df[LABEL_COL].mean():.1%})")

    print("\n--- Binary features ---")
    binary_summary = summarize_binary_features(df)
    print(binary_summary.to_string(index=False))

    print("\n--- Numeric features ---")
    numeric_summary = summarize_numeric_features(df)
    print("\n" + numeric_summary.to_string(index=False))

    print("\n--- Categorical features ---")
    categorical_summary = summarize_categorical_features(df)
    print("\n" + categorical_summary.to_string(index=False))

    print("\n--- Cross-feature correlation matrix (multicollinearity check) ---")
    corr_matrix = cross_feature_correlation_matrix(df)
    print(corr_matrix.round(3).to_string())

    full_summary = pd.concat([binary_summary, numeric_summary, categorical_summary], ignore_index=True)
    print_low_signal_warnings(full_summary)

    full_summary.to_csv(OUTPUT_PATH, index=False)
    print(f"\nWrote summary to {OUTPUT_PATH}")


if __name__ == "__main__":
    run()
