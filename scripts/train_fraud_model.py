"""
Stage 4 (Step 3): Model Training + Scoring

Trains two classifiers to predict a proxy label — is_entity_owner, among
homestead parcels only — from features that exclude ownership-entity signals
themselves (leakage prevention):
  - Logistic regression: transparent baseline, familiar reference point
  - HistGradientBoostingClassifier: captures nonlinear/interaction effects
    the logit can't, without hand-specifying them

Compares the two on ROC-AUC / PR-AUC before deciding which (if either) is
worth scoring the full parcel universe with.

Usage:
    python -m scripts.train_fraud_model
"""

import json
import sqlite3
from pathlib import Path

import pandas as pd
import shap
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# ============================================================================
# Configuration
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
INPUT_PATH = PROJECT_ROOT / "data" / "products" / "parcel_features.csv"
DB_PATH = PROJECT_ROOT / "data" / "sources" / "travis_property_tax.db"

RISK_SCORES_PATH = PROJECT_ROOT / "data" / "products" / "parcel_risk_scores.csv"
SHAP_GLOBAL_PATH = PROJECT_ROOT / "data" / "products" / "shap_global_importance.csv"
SHAP_TOP_PATH = PROJECT_ROOT / "data" / "products" / "shap_top_flagged.csv"
SHAP_FLAGGED_PATH = PROJECT_ROOT / "data" / "products" / "shap_flagged_individually_owned.csv"
SUMMARY_PATH = PROJECT_ROOT / "data" / "products" / "fraud_model_summary.json"

RANDOM_STATE = 42
TEST_SIZE = 0.2

NUMERIC_FEATURES = [
    "mailing_ne_situs", "out_of_state_owner",
    "imprvMainArea", "land_size_sqft"
]
CATEGORICAL_FEATURES = ["imprvClass", "imprvCondition"]

RISK_PERCENTILE = 0.95  # flag the top 5% of scored homestead parcels as "high risk"
TOP_N_SHAP = 25  # number of highest-scoring individually-owned parcels to explain individually
SHAP_SAMPLE_SIZE = 2000  # sample size for the global SHAP importance ranking

# Combined Travis County (FY2026 adopted, $0.3758/$100) + Austin ISD (FY2026,
# $0.9252/$100) tax rate, looked up Aug 2026. Approximation: excludes City of
# Austin, Austin Community College, and other overlapping jurisdictions, so it
# understates a typical Austin property's full combined rate. See
# docs/fraud_model_assumptions.md.
COMBINED_TAX_RATE = 0.01301  # per dollar of taxable value

# ============================================================================
# Data loading
# ============================================================================

def load_training_data(input_path: Path) -> tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
    """
    Load parcel_features.csv, restrict to homestead parcels, and split into
    features (X), the proxy label (y = is_entity_owner), and parcel
    identifiers (ids = pID, hex_id).

    X, y, and ids all come from slicing the same homestead DataFrame, so
    they share its row index and stay aligned through scoring/SHAP without
    needing to be re-merged later.

    Categorical columns are integer-encoded (not left as pandas 'category'
    dtype) so the same numeric X works for both HistGradientBoostingClassifier
    (told which columns are categorical by position in build_hgb_model) and
    SHAP's TreeExplainer, which cannot decode pandas category dtype on its
    own. Missing values are preserved as NaN, not mapped to an integer code,
    so HGB's native missing-value handling still applies to these columns
    exactly as it does to the numeric ones.
    """
    df = pd.read_csv(input_path)
    homestead = df[df["has_homestead"] == 1].copy()

    for col in CATEGORICAL_FEATURES:
        codes = homestead[col].astype("category").cat.codes.astype("float64")
        homestead[col] = codes.where(homestead[col].notna())

    X = homestead[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = homestead["is_entity_owner"]
    ids = homestead[["pID", "hex_id"]]

    return X, y, ids


# ============================================================================
# Model definitions
# ============================================================================

def build_logistic_pipeline() -> Pipeline:
    """
    Logistic regression baseline. Needs explicit preprocessing that
    HistGradientBoostingClassifier gets for free:
      - missing values imputed (median for numeric; a dedicated "missing"
        code for categorical — imprvClass/imprvCondition are ~18-21% null)
      - numeric features scaled (the solver converges faster and more
        reliably when features are on comparable scales)
      - categorical features one-hot encoded (logistic regression needs
        numeric input; it has no native concept of a categorical split)

    Categorical columns arrive as integer-encoded floats (see
    load_training_data), not strings, so the missing-value fill has to be
    a numeric sentinel (-1) rather than a string like "missing" — -1 never
    collides with a real category code, which are always >= 0.
    """
    numeric_transformer = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ])

    categorical_transformer = Pipeline([
        ("impute", SimpleImputer(strategy="constant", fill_value=-1)),
        ("encode", OneHotEncoder(handle_unknown="ignore")),
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_transformer, NUMERIC_FEATURES),
        ("cat", categorical_transformer, CATEGORICAL_FEATURES),
    ])

    return Pipeline([
        ("preprocess", preprocessor),
        ("model", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)),
    ])


def build_hgb_model() -> HistGradientBoostingClassifier:
    """
    Gradient boosting model. No imputation/scaling pipeline needed — it
    handles missing values in both numeric and categorical columns
    natively. categorical_features marks which feature columns (by
    position in NUMERIC_FEATURES + CATEGORICAL_FEATURES) should be treated
    as unordered categories rather than ordered numeric values; those
    columns are already integer-encoded floats (see load_training_data),
    not pandas 'category' dtype, so SHAP's TreeExplainer can read the same
    X directly without special-casing categoricals.
    """
    categorical_mask = [
        col in CATEGORICAL_FEATURES for col in NUMERIC_FEATURES + CATEGORICAL_FEATURES
    ]
    return HistGradientBoostingClassifier(
        categorical_features=categorical_mask,
        random_state=RANDOM_STATE,
    )


# ============================================================================
# Scoring
# ============================================================================

def composite_red_flag_score(X: pd.DataFrame, y: pd.Series) -> pd.Series:
    """
    Naive rule-based baseline: count of red-flag conditions met, out of 3
    (is_entity_owner + mailing_ne_situs + out_of_state_owner).

    This is what a human analyst might build by hand with a spreadsheet, no
    modeling involved. It's the comparison point for the ML score, which is
    deliberately barred from seeing is_entity_owner during training (see
    load_training_data) so it can generalize beyond this composite to
    individually-owned parcels this baseline can never flag on its own.
    """
    return y + X["mailing_ne_situs"] + X["out_of_state_owner"]


def score_parcels(model: HistGradientBoostingClassifier, X: pd.DataFrame) -> pd.Series:
    """
    Predicted probability of the entity-owned-homestead proxy pattern for
    every parcel in X — including individually-owned parcels the model
    never saw as a positive example. A high score on an individually-owned
    parcel is the interesting output: the parcel's mailing/structural
    footprint resembles the confirmed-non-occupied cases without tripping
    the deterministic entity-ownership rule itself.
    """
    return pd.Series(model.predict_proba(X)[:, 1], index=X.index, name="risk_score")


def revenue_at_risk(flagged_pids: pd.Series, db_path: Path, tax_rate: float) -> tuple[pd.DataFrame, float]:
    """
    Pull each flagged parcel's homestead-classified value (ownerLandHSValue +
    ownerImprovementHSValue) from property_owner and apply the combined tax
    rate.

    Approximates the tax dollars currently benefiting from homestead
    treatment on flagged parcels. NOT a precise exemption calculation: real
    Texas homestead exemptions apply flat/percentage reductions with
    statutory caps rather than a rate on the full HS-classified value, and
    COMBINED_TAX_RATE covers only two of several overlapping taxing
    jurisdictions. See docs/fraud_model_assumptions.md.
    """
    con = sqlite3.connect(db_path)

    placeholders = ",".join("?" * len(flagged_pids))
    query = f"""
        SELECT pID, ownerLandHSValue, ownerImprovementHSValue
        FROM property_owner
        WHERE pID IN ({placeholders})
    """
    values = pd.read_sql(query, con, params=flagged_pids.tolist())
    con.close()

    values["hs_value"] = (
        values["ownerLandHSValue"].fillna(0) + values["ownerImprovementHSValue"].fillna(0)
    )
    values["tax_at_risk"] = values["hs_value"] * tax_rate

    return values, values["tax_at_risk"].sum()


# ============================================================================
# SHAP explanation
# ============================================================================

def build_shap_explainer(model: HistGradientBoostingClassifier) -> shap.TreeExplainer:
    """
    Reads the fitted model's tree structure directly — fast and exact for
    gradient boosted trees, unlike SHAP's slower model-agnostic explainers.
    """
    return shap.TreeExplainer(model)


def global_shap_importance(
    explainer: shap.TreeExplainer, X: pd.DataFrame, sample_size: int, random_state: int
) -> pd.DataFrame:
    """
    Mean absolute SHAP value per feature, computed on a random sample rather
    than all ~227k homestead parcels — SHAP's cost scales with rows
    explained, and a few thousand is enough for a stable global ranking.
    """
    sample = X.sample(n=min(sample_size, len(X)), random_state=random_state)
    shap_values = explainer(sample)

    importance = (
        pd.DataFrame(shap_values.values, columns=X.columns)
        .abs()
        .mean()
        .sort_values(ascending=False)
        .rename("mean_abs_shap")
        .reset_index()
        .rename(columns={"index": "feature"})
    )
    return importance


def top_flagged_shap(
    explainer: shap.TreeExplainer, X: pd.DataFrame, risk_score: pd.Series, top_n: int
) -> pd.DataFrame:
    """
    Per-parcel SHAP contributions for the top_n highest-scoring parcels in
    risk_score — which features pushed each individual parcel's score up or
    down. Caller controls which population risk_score covers (e.g. pass
    only individually-owned parcels' scores to explain the generalization
    cases specifically).
    """
    top_idx = risk_score.sort_values(ascending=False).head(top_n).index
    X_top = X.loc[top_idx]

    shap_values = explainer(X_top)

    contributions = pd.DataFrame(shap_values.values, columns=X.columns, index=X_top.index)
    contributions.insert(0, "risk_score", risk_score.loc[top_idx])
    return contributions


# ============================================================================
# Main
# ============================================================================

def main():
    print("=" * 60)
    print("Stage 4: Model Training + Scoring")
    print("=" * 60)

    print("\n[1/7] Loading homestead parcels and building proxy label...")
    X, y, ids = load_training_data(INPUT_PATH)
    print(
        f"  Parcels: {len(X):,}  |  Entity-owned (positive class): {y.sum():,} ({y.mean():.1%})"
    )

    print("\n[2/7] Splitting into train/test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )
    print(f"  Train: {len(X_train):,}  |  Test: {len(X_test):,}")

    print("\n[3/7] Fitting models...")
    logistic_model = build_logistic_pipeline()
    logistic_model.fit(X_train, y_train)

    hgb_model = build_hgb_model()
    hgb_model.fit(X_train, y_train)

    print("\n[4/7] Evaluating on the test set...")
    model_metrics = {}
    for name, model in [("logistic_regression", logistic_model), ("gradient_boosting", hgb_model)]:
        y_score = model.predict_proba(X_test)[:, 1]
        roc_auc = roc_auc_score(y_test, y_score)
        pr_auc = average_precision_score(y_test, y_score)
        model_metrics[name] = {"roc_auc": round(roc_auc, 3), "pr_auc": round(pr_auc, 3)}
        print(f"  {name:22s}  ROC-AUC: {roc_auc:.3f}   PR-AUC: {pr_auc:.3f}")

    print(f"\n  (PR-AUC baseline for a no-skill classifier ~ positive rate: {y_test.mean():.3f})")

    print("\n[5/7] Scoring all homestead parcels with the gradient boosting model...")
    risk_score = score_parcels(hgb_model, X)
    composite = composite_red_flag_score(X, y)

    risk_table = ids.assign(
        is_entity_owner=y,
        risk_score=risk_score,
        composite_red_flag_score=composite,
    )
    risk_table.to_csv(RISK_SCORES_PATH, index=False)
    print(f"  Wrote {len(risk_table):,} scored parcels to {RISK_SCORES_PATH}")

    print("\n[6/7] Computing SHAP explanations...")
    explainer = build_shap_explainer(hgb_model)

    global_importance = global_shap_importance(explainer, X, SHAP_SAMPLE_SIZE, RANDOM_STATE)
    global_importance.to_csv(SHAP_GLOBAL_PATH, index=False)
    print("  Top 5 features by mean |SHAP|:")
    for _, row in global_importance.head(5).iterrows():
        print(f"    {row['feature']:20s} {row['mean_abs_shap']:.4f}")

    individually_owned = y == 0
    top_flagged = top_flagged_shap(explainer, X, risk_score[individually_owned], TOP_N_SHAP)
    top_flagged = ids.join(top_flagged, how="right")
    top_flagged.to_csv(SHAP_TOP_PATH)
    print(
        f"  Wrote SHAP contributions for the {TOP_N_SHAP} highest-scoring "
        f"individually-owned parcels to {SHAP_TOP_PATH}"
    )

    print("\n[7/7] Revenue-at-risk rollup...")
    threshold = risk_score.quantile(RISK_PERCENTILE)
    flagged_mask = risk_score >= threshold
    flagged_pids = ids.loc[flagged_mask, "pID"]

    flagged_individually_owned = flagged_mask & individually_owned
    flagged_shap = top_flagged_shap(
        explainer, X, risk_score[flagged_individually_owned], flagged_individually_owned.sum()
    )
    flagged_shap = ids.join(flagged_shap, how="right")
    flagged_shap.to_csv(SHAP_FLAGGED_PATH)
    print(
        f"  Wrote SHAP contributions for all {flagged_individually_owned.sum():,} flagged "
        f"individually-owned parcels to {SHAP_FLAGGED_PATH}"
    )

    revenue_detail, total_tax_at_risk = revenue_at_risk(flagged_pids, DB_PATH, COMBINED_TAX_RATE)

    summary = {
        "total_homestead_parcels": int(len(X)),
        "entity_owned_count": int(y.sum()),
        "entity_owned_pct": round(float(y.mean()), 4),
        "model_metrics": model_metrics,
        "risk_percentile": RISK_PERCENTILE,
        "risk_score_threshold": round(float(threshold), 4),
        "flagged_parcel_count": int(flagged_mask.sum()),
        "flagged_entity_owned_count": int(y[flagged_mask].sum()),
        "flagged_individually_owned_count": int((flagged_mask & individually_owned).sum()),
        "combined_tax_rate": COMBINED_TAX_RATE,
        "total_hs_value_at_risk": round(float(revenue_detail["hs_value"].sum()), 2),
        "total_tax_at_risk": round(float(total_tax_at_risk), 2),
        "top_shap_features": global_importance.head(5)["feature"].tolist(),
    }
    with open(SUMMARY_PATH, "w") as f:
        json.dump(summary, f, indent=2)

    print(
        f"  Flagged {summary['flagged_parcel_count']:,} parcels (top "
        f"{(1 - RISK_PERCENTILE):.0%}) -> ${summary['total_tax_at_risk']:,.0f} "
        f"estimated tax at risk"
    )
    print(
        f"    of which {summary['flagged_individually_owned_count']:,} are "
        f"individually-owned (the generalization claim beyond the "
        f"deterministic entity-ownership rule)"
    )
    print(f"  Wrote summary to {SUMMARY_PATH}")


run = main


if __name__ == "__main__":
    main()
