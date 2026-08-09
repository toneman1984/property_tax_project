"""
Stage 4 (Step 2): Parcel-Level Feature Engineering

Builds one row per SFR homestead-eligible parcel, combining:
  - has_homestead, hex_id, and hex-level airbnb_rate / str_permit_rate /
    registration_gap (reused from aggregate_to_hex.py, unfiltered — every
    parcel gets a rate, not just the 246 POC cells)
  - is_entity_owner, mailing_ne_situs, out_of_state_owner (derived from
    property_owner + property_situs)
  - structural characteristics from property_profile

Output: data/products/parcel_features.csv

Usage:
    python -m scripts.build_fraud_features
"""

import json
import re
import sqlite3
from pathlib import Path

import pandas as pd

from scripts.aggregate_to_hex import (
    DB_PATH,
    STR_PATH,
    AIRBNB_PATH,
    load_tcad_parcels,
    aggregate_tcad_to_hex,
    load_str_airbnb,
    merge_all_counts,
)

# ============================================================================
# Configuration
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_PATH = PROJECT_ROOT / "data" / "products" / "parcel_features.csv"


def load_owner_features(db_path: Path) -> pd.DataFrame:
    """
    Join property_owner and property_situs on pID, and derive three
    ownership red-flag features:
      - is_entity_owner:    owner name looks like a business entity, not a person
      - mailing_ne_situs:   owner's mailing zip differs from the property's zip
                             (city dropped — 51% null and inconsistently
                             spelled in property_situs)
      - out_of_state_owner: owner's mailing state isn't Texas

    NOTE on is_entity_owner: the plan originally also flagged owners with
    firstName AND lastName both null as entities. Checked against the real
    data — that's true for 72.8% of ALL owners, individuals included (TCAD
    stores most names as a single "LAST FIRST MIDDLE" string in `name`
    regardless of owner type, so firstName/lastName just aren't reliably
    populated either way). Dropped that heuristic; keyword match on `name`
    alone gives ~20.3%, consistent with a manual spot check.
    """
    conn = sqlite3.connect(db_path)

    df = pd.read_sql_query("""
        SELECT
            o.pID,
            o.name,
            o.firstName,
            o.lastName,
            o.addrZip   AS owner_zip,
            o.addrState AS owner_state,
            s.zip       AS situs_zip,
            s.primarySitus
        FROM property_owner o
        LEFT JOIN property_situs s ON o.pID = s.pID
    """, conn)
    conn.close()

    # Some parcels have multiple situs (address) records — keep the one
    # flagged primary. Same "pick one row per parcel" idea as
    # pick_primary_owner() in load_owners_to_sqlite.py, written here with
    # pandas instead of a manual loop.
    df = df.sort_values("primarySitus", ascending=False).drop_duplicates(subset="pID", keep="first")

    # --- is_entity_owner ---
    entity_keywords = r"\bLLC\b|\bINC\b|\bCORP\b|\bL\s?P\b|\bLTD\b|\bTRUST\b"
    df["is_entity_owner"] = df["name"].str.contains(entity_keywords, case=False, na=False, regex=True).astype(int)

    # --- mailing_ne_situs (zip only — see docstring) ---
    owner_zip5 = df["owner_zip"].str[:5]
    situs_zip5 = df["situs_zip"].str[:5]
    df["mailing_ne_situs"] = (owner_zip5 != situs_zip5).astype(int)

    # --- out_of_state_owner ---
    df["out_of_state_owner"] = (df["owner_state"] != "TX").astype(int)

    return df[["pID", "is_entity_owner", "mailing_ne_situs", "out_of_state_owner"]]


def load_structural_features(db_path: Path) -> pd.DataFrame:
    """
    Pull structural characteristics per parcel from property_profile:
      - imprvActualYearBuilt, imprvMainArea, imprvClass, imprvCondition
        (real columns)
      - land_size_sqft: pulled out of extra_fields, a JSON blob holding
        fields (like landSizeSqft) that don't have their own column

    Unlike property_situs, property_profile is already one row per pID —
    no duplicate handling needed here.
    """
    conn = sqlite3.connect(db_path)

    df = pd.read_sql_query("""
        SELECT pID, imprvActualYearBuilt, imprvMainArea, imprvClass,
               imprvCondition, extra_fields
        FROM property_profile
    """, conn)
    conn.close()

    def extract_land_size(extra_json):
        if extra_json is None:
            return None
        fields = json.loads(extra_json)
        return fields.get("landSizeSqft")

    df["land_size_sqft"] = df["extra_fields"].apply(extract_land_size)
    df = df.drop(columns=["extra_fields"])

    return df


def load_parcel_universe_with_hex_rates(db_path: Path, str_path: Path, airbnb_path: Path) -> pd.DataFrame:
    """
    Build the base parcel universe (SFR, active, geocoded — same definition
    used in the POC) and attach each parcel's hex-level STR/Airbnb rates.

    Unlike aggregate_to_hex.py's POC output, this keeps rates for EVERY hex
    cell, not just the 246 cells that passed the POC's stability thresholds
    (MIN_SFR_TOTAL, MIN_AIRBNB_*) — every SFR parcel needs a rate value here,
    so we reuse the counting/merging logic but skip the filtering step.
    """
    sfr_df = load_tcad_parcels(db_path)          # pID, hex_id, has_homestead
    tcad_hex = aggregate_tcad_to_hex(sfr_df)     # hex_id, sfr_total, sfr_homestead

    str_counts, airbnb_counts = load_str_airbnb(str_path, airbnb_path)
    hex_df = merge_all_counts(tcad_hex, str_counts, airbnb_counts)

    hex_df["airbnb_rate"]      = (hex_df["airbnb_entire_home"] / hex_df["sfr_total"]).round(4)
    hex_df["str_permit_rate"]  = (hex_df["str_permits_type2"]  / hex_df["sfr_total"]).round(4)
    hex_df["registration_gap"] =  hex_df["airbnb_entire_home"] - hex_df["str_permits_type2"]

    hex_rates = hex_df[["hex_id", "airbnb_rate", "str_permit_rate", "registration_gap"]]

    # Broadcast each hex cell's rates onto every parcel inside it
    return sfr_df.merge(hex_rates, on="hex_id", how="left")


# ============================================================================
# Main
# ============================================================================

def main():
    print("=" * 60)
    print("Stage 4: Parcel-Level Feature Engineering")
    print("=" * 60)

    print("\n[1/4] Loading parcel universe and hex-level STR/Airbnb rates...")
    parcel_universe = load_parcel_universe_with_hex_rates(DB_PATH, STR_PATH, AIRBNB_PATH)
    print(f"  Parcels: {len(parcel_universe):,}")

    print("\n[2/4] Loading owner-derived red-flag features...")
    owner_features = load_owner_features(DB_PATH)

    print("\n[3/4] Loading structural characteristics...")
    structural_features = load_structural_features(DB_PATH)

    print("\n[4/4] Merging and saving...")
    features = parcel_universe.merge(owner_features, on="pID", how="left")
    features = features.merge(structural_features, on="pID", how="left")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    features.to_csv(OUTPUT_PATH, index=False)
    print(f"  Saved {len(features):,} parcels x {features.shape[1]} columns -> {OUTPUT_PATH}")

    proxy_positive = (features["has_homestead"] & features["is_entity_owner"]).sum()

    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  Total parcels:                          {len(features):,}")
    print(f"  Homestead parcels:                      {features['has_homestead'].sum():,}")
    print(f"  Entity-owned parcels:                   {features['is_entity_owner'].sum():,}")
    print(f"  Proxy positive (homestead AND entity):  {proxy_positive:,}")
    print("=" * 60)
    print("Done.")


run = main


if __name__ == "__main__":
    main()
