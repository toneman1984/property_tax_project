"""
Stage 4 preflight check — runs before main.py decides whether to reload owner data.

Checks if the property_owner table already exists with a plausible row count
and the expected columns. If all checks pass, the ~29GB owner-load pass
(comparable runtime to Stage 1) is skipped.

Usage:
    python scripts/stage4_preflight.py
"""

import sqlite3
from pathlib import Path

PROJECT_ROOT  = Path(__file__).parent.parent
DB_PATH       = PROJECT_ROOT / "data" / "sources" / "travis_property_tax.db"
MIN_ROW_COUNT = 100_000  # minimum plausible row count for property_owner

REQUIRED_COLUMNS = [
    "pID", "name", "firstName", "lastName", "addrCity", "addrState",
    "addrZip", "addrDeliveryLine", "ownerPct",
    "ownerMarketValue", "ownerAppraisedValue",
    "ownerLandHSValue", "ownerImprovementHSValue",
    "ownerLandNHSValue", "ownerImprovementNHSValue",
]


def owner_table_ready() -> bool:
    """
    Return True if property_owner exists and passes all preflight checks.
    Prints a summary of what was found either way.
    """
    print("\n=== Stage 4 Preflight: property_owner Table Check ===")

    if not DB_PATH.exists():
        print("  No database found - owner load will run.")
        return False

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='property_owner'")
        if cursor.fetchone() is None:
            print("  Table 'property_owner' not found - owner load will run.")
            conn.close()
            return False

        cursor.execute("SELECT COUNT(*) FROM property_owner")
        count = cursor.fetchone()[0]
        if count < MIN_ROW_COUNT:
            print(f"  FAIL  property_owner has only {count:,} rows — expected at least {MIN_ROW_COUNT:,}.")
            conn.close()
            print("  Owner load will run.")
            return False
        print(f"  PASS  property_owner: {count:,} rows")

        cursor.execute("PRAGMA table_info(property_owner)")
        existing_columns = {row[1] for row in cursor.fetchall()}
        missing = [c for c in REQUIRED_COLUMNS if c not in existing_columns]
        if missing:
            print(f"  FAIL  property_owner missing columns: {missing}")
            conn.close()
            print("  Owner load will run.")
            return False
        print(f"  PASS  All {len(REQUIRED_COLUMNS)} expected columns present")

        conn.close()

    except sqlite3.DatabaseError as e:
        print(f"  FAIL  Database error: {e}")
        print("  Owner load will run.")
        return False

    print("  All preflight checks passed - skipping owner load.")
    return True


if __name__ == "__main__":
    owner_table_ready()
