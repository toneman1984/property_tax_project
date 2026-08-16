"""
Output verification tests for Stage 4 (Parcel-Level Fraud Risk Model).

Usage:
    python scripts/stage4_output_test.py
"""

import json
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).parent.parent
FEATURES_PATH = PROJECT_ROOT / "data" / "products" / "parcel_features.csv"
RISK_SCORES_PATH = PROJECT_ROOT / "data" / "products" / "parcel_risk_scores.csv"
SHAP_GLOBAL_PATH = PROJECT_ROOT / "data" / "products" / "shap_global_importance.csv"
SHAP_TOP_PATH = PROJECT_ROOT / "data" / "products" / "shap_top_flagged.csv"
SHAP_FLAGGED_PATH = PROJECT_ROOT / "data" / "products" / "shap_flagged_individually_owned.csv"
SUMMARY_PATH = PROJECT_ROOT / "data" / "products" / "fraud_model_summary.json"

MIN_FEATURE_ROWS = 300_000  # parcel_features.csv covers the broader SFR/geocoded universe

# NOTE: airbnb_rate/str_permit_rate/registration_gap legitimately still exist
# here — build_fraud_features.py is unchanged by the STR-feature pivot, only
# train_fraud_model.py's feature *selection* changed. Only the trained
# model's own feature set (checked below via shap_global_importance.csv)
# should no longer include them.
EXPECTED_FEATURE_COLUMNS = [
    "pID", "hex_id", "has_homestead", "airbnb_rate", "str_permit_rate",
    "registration_gap", "is_entity_owner", "mailing_ne_situs",
    "out_of_state_owner", "imprvActualYearBuilt", "imprvMainArea",
    "imprvClass", "imprvCondition", "land_size_sqft",
]

# Features dropped from the trained model during the Stage 4 pivot
# (see docs/fraud_model_pivot.md) — must never reappear in model outputs.
DROPPED_MODEL_FEATURES = ["airbnb_rate", "str_permit_rate", "registration_gap", "imprvActualYearBuilt"]
EXPECTED_MODEL_FEATURE_COUNT = 6


def run():
    passed = 0
    failed = 0

    def check(description, condition, detail=""):
        nonlocal passed, failed
        if condition:
            print(f"  PASS  {description}")
            passed += 1
        else:
            print(f"  FAIL  {description}" + (f" - {detail}" if detail else ""))
            failed += 1

    print("\n=== Stage 4: Parcel-Level Fraud Risk Model ===")

    check("parcel_features.csv exists", FEATURES_PATH.exists(), f"expected at {FEATURES_PATH}")
    if FEATURES_PATH.exists():
        features_df = pd.read_csv(FEATURES_PATH)
        check(
            f"parcel_features.csv has at least {MIN_FEATURE_ROWS:,} rows",
            len(features_df) >= MIN_FEATURE_ROWS,
            f"found {len(features_df):,}",
        )
        for col in EXPECTED_FEATURE_COLUMNS:
            check(f"Column '{col}' present in parcel_features.csv", col in features_df.columns)

    check("parcel_risk_scores.csv exists", RISK_SCORES_PATH.exists(), f"expected at {RISK_SCORES_PATH}")
    if RISK_SCORES_PATH.exists():
        risk_df = pd.read_csv(RISK_SCORES_PATH)
        check("parcel_risk_scores.csv is non-empty", len(risk_df) > 0)
        check("composite_red_flag_score column present", "composite_red_flag_score" in risk_df.columns)
        if "risk_score" in risk_df.columns:
            check(
                "risk_score values are bounded [0, 1]",
                risk_df["risk_score"].between(0, 1).all(),
            )
        else:
            check("risk_score column present", False)

    check("shap_global_importance.csv exists", SHAP_GLOBAL_PATH.exists(), f"expected at {SHAP_GLOBAL_PATH}")
    if SHAP_GLOBAL_PATH.exists():
        global_shap_df = pd.read_csv(SHAP_GLOBAL_PATH)
        check(
            f"shap_global_importance.csv has exactly {EXPECTED_MODEL_FEATURE_COUNT} rows",
            len(global_shap_df) == EXPECTED_MODEL_FEATURE_COUNT,
            f"found {len(global_shap_df)}",
        )
        if "feature" in global_shap_df.columns:
            reappeared = [f for f in DROPPED_MODEL_FEATURES if f in global_shap_df["feature"].tolist()]
            check(
                "No dropped STR/year-built features reappear in shap_global_importance.csv",
                len(reappeared) == 0,
                f"found: {reappeared}",
            )

    check("shap_top_flagged.csv exists and is non-empty", SHAP_TOP_PATH.exists() and SHAP_TOP_PATH.stat().st_size > 0)
    check(
        "shap_flagged_individually_owned.csv exists and is non-empty",
        SHAP_FLAGGED_PATH.exists() and SHAP_FLAGGED_PATH.stat().st_size > 0,
    )

    check("fraud_model_summary.json exists", SUMMARY_PATH.exists(), f"expected at {SUMMARY_PATH}")
    if SUMMARY_PATH.exists():
        with open(SUMMARY_PATH) as f:
            summary = json.load(f)

        expected_keys = [
            "total_homestead_parcels", "entity_owned_count", "entity_owned_pct",
            "model_metrics", "risk_percentile", "risk_score_threshold",
            "flagged_parcel_count", "flagged_entity_owned_count",
            "flagged_individually_owned_count", "combined_tax_rate",
            "total_hs_value_at_risk", "total_tax_at_risk", "top_shap_features",
        ]
        for key in expected_keys:
            check(f"Summary key '{key}' present", key in summary)

        gb_metrics = summary.get("model_metrics", {}).get("gradient_boosting", {})
        check(
            "gradient_boosting.roc_auc is between 0 and 1",
            0 <= gb_metrics.get("roc_auc", -1) <= 1,
        )
        check(
            "gradient_boosting.pr_auc is between 0 and 1",
            0 <= gb_metrics.get("pr_auc", -1) <= 1,
        )

        top_features = summary.get("top_shap_features", [])
        reappeared = [f for f in DROPPED_MODEL_FEATURES if f in top_features]
        check(
            "No dropped STR/year-built features reappear in top_shap_features",
            len(reappeared) == 0,
            f"found: {reappeared}",
        )

    print(f"\n{'='*40}")
    print(f"Results: {passed} passed, {failed} failed")
    if failed == 0:
        print("All checks passed - Stage 4 outputs look good.")
    else:
        print("Some checks failed - review output above.")
    print()


if __name__ == "__main__":
    run()
