"""
Load owner records from the Travis County Property Tax Export JSON into SQLite.

Adds a new `property_owner` table to the existing database built by
load_protax_to_sqlite.py, without modifying any of its tables. Follows the
same approach:
1. Streams the JSON with ijson (never loads the full 29GB file into memory)
2. Picks one "primary" owner per parcel (highest ownerPct; ties keep the
   first owner listed in the record)
3. Inserts in batches with progress tracking

Usage:
    python scripts/load_owners_to_sqlite.py
"""

import re
import sqlite3
import ijson
import time
import os
from pathlib import Path
from datetime import datetime, date
from decimal import Decimal


# ============================================================================
# Configuration
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
JSON_FILE = PROJECT_ROOT / "data" / "sources" / "Travis_protaxExport_20250720.json"
DB_FILE = PROJECT_ROOT / "data" / "sources" / "travis_property_tax.db"

BATCH_SIZE = 10000  # Records per commit
PROGRESS_INTERVAL = 25000  # Print progress every N records


# ============================================================================
# Schema Definitions
# ============================================================================

CREATE_OWNER_TABLE = """
CREATE TABLE IF NOT EXISTS property_owner (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pID INTEGER NOT NULL,
    name TEXT,
    firstName TEXT,
    lastName TEXT,
    addrCity TEXT,
    addrState TEXT,
    addrZip TEXT,
    addrDeliveryLine TEXT,
    ownerPct REAL,
    ownerMarketValue REAL,
    ownerAppraisedValue REAL,
    ownerLandHSValue REAL,
    ownerImprovementHSValue REAL,
    ownerLandNHSValue REAL,
    ownerImprovementNHSValue REAL,
    FOREIGN KEY (pID) REFERENCES properties(pID)
);
"""

CREATE_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_owner_pID ON property_owner(pID);
"""


# ============================================================================
# Helper Functions
# ============================================================================

def format_time(seconds):
    """Format seconds into a human-readable string."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}m"
    else:
        return f"{seconds/3600:.1f}h"


def format_size(bytes_size):
    """Format bytes into a human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.1f}{unit}"
        bytes_size /= 1024
    return f"{bytes_size:.1f}TB"


def convert_value(value):
    """Convert Decimal and other unsupported types for SQLite."""
    if value is None:
        return None
    if isinstance(value, Decimal):
        # Convert to int if it's a whole number, otherwise float
        return int(value) if value == int(value) else float(value)
    return value


def get_value(record, key, default=None):
    """Safely get a value from a record, converting types as needed."""
    value = record.get(key, default)
    return convert_value(value)


def pick_primary_owner(owners: list[dict]) -> dict | None:
    """
    Given a parcel's `owners` list, return the record for the owner with the
    highest ownerPct. Ties keep whichever owner appears first in the list
    (documented tie-break, per the plan).
    """
    if not owners:
        return None

    primary = owners[0]
    for owner in owners[1:]:
        if owner.get('ownerPct', 0) > primary.get('ownerPct', 0):
            primary = owner

    return primary


def get_owner_value(owner: dict) -> dict:
    """Return the first entry in an owner's ownerValue list, or an empty dict if missing."""
    owner_values = owner.get('ownerValue') or []
    return owner_values[0] if owner_values else {}


# ============================================================================
# Database Functions
# ============================================================================

def create_owner_table(db_path):
    """
    Create (or reset) the property_owner table in the existing database.

    Unlike load_protax_to_sqlite.py, this does NOT delete the database file —
    property_owner is one additional table alongside the tables that script
    already built. We only drop and recreate our own table, so re-running
    this script doesn't duplicate rows on top of a previous run.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS property_owner")
    cursor.execute(CREATE_OWNER_TABLE)
    conn.commit()
    return conn


def create_indexes(conn):
    """Create indexes after data load for better performance."""
    print("\nCreating indexes...")
    cursor = conn.cursor()
    for statement in CREATE_INDEXES.strip().split(';'):
        if statement.strip():
            cursor.execute(statement)
    conn.commit()
    print("Indexes created.")


def optimize_for_bulk_insert(conn):
    """Configure SQLite for fast bulk inserts."""
    cursor = conn.cursor()
    cursor.execute("PRAGMA synchronous = OFF")
    cursor.execute("PRAGMA journal_mode = MEMORY")
    cursor.execute("PRAGMA cache_size = -64000")  # 64MB cache
    cursor.execute("PRAGMA temp_store = MEMORY")
    conn.commit()


def insert_owner(cursor, pID, owner: dict):
    """Insert the flattened primary-owner row for a parcel."""
    value = get_owner_value(owner)

    sql = """
    INSERT INTO property_owner (
        pID, name, firstName, lastName, addrCity, addrState, addrZip,
        addrDeliveryLine, ownerPct, ownerMarketValue, ownerAppraisedValue,
        ownerLandHSValue, ownerImprovementHSValue, ownerLandNHSValue,
        ownerImprovementNHSValue
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(sql, (
        pID,
        get_value(owner, 'name'),
        get_value(owner, 'firstName'),
        get_value(owner, 'lastName'),
        get_value(owner, 'addrCity'),
        get_value(owner, 'addrState'),
        get_value(owner, 'addrZip'),
        get_value(owner, 'addrDeliveryLine'),
        get_value(owner, 'ownerPct'),
        get_value(value, 'ownerMarketValue'),
        get_value(value, 'ownerAppraisedValue'),
        get_value(value, 'ownerLandHSValue'),
        get_value(value, 'ownerImprovementHSValue'),
        get_value(value, 'ownerLandNHSValue'),
        get_value(value, 'ownerImprovementNHSValue'),
    ))


# ============================================================================
# Main Processing
# ============================================================================

def load_owners_to_sqlite(json_path, db_path, batch_size=BATCH_SIZE):
    """
    Stream the JSON export and populate property_owner with one row per
    parcel — the primary owner, chosen by pick_primary_owner().
    """
    file_size = os.path.getsize(json_path)
    print(f"Input file: {json_path}")
    print(f"File size: {format_size(file_size)}")
    print(f"Output database: {db_path}")
    print(f"Batch size: {batch_size:,} records")
    print()

    print("Creating property_owner table...")
    conn = create_owner_table(db_path)
    optimize_for_bulk_insert(conn)
    cursor = conn.cursor()

    print("\nProcessing records...")
    print("-" * 60)

    start_time = time.time()
    records_processed = 0
    records_skipped = 0

    try:
        with open(json_path, 'rb') as f:
            parser = ijson.items(f, 'item')

            for record in parser:
                pID = get_value(record, 'pID')
                owner = pick_primary_owner(record.get('owners') or [])

                # Skip records with no pID or no owner data at all
                if pID is None or owner is None:
                    records_skipped += 1
                    continue

                insert_owner(cursor, pID, owner)
                records_processed += 1

                # Commit in batches
                if records_processed % batch_size == 0:
                    conn.commit()

                # Progress update
                if records_processed % PROGRESS_INTERVAL == 0:
                    elapsed = time.time() - start_time
                    rate = records_processed / elapsed if elapsed > 0 else 0
                    pct_complete = (f.tell() / file_size) * 100

                    print(f"  Processed: {records_processed:>10,} records | "
                          f"Rate: {rate:>8,.0f}/sec | "
                          f"Progress: {pct_complete:>5.1f}% | "
                          f"Elapsed: {format_time(elapsed)}")

        # Final commit
        conn.commit()

    except KeyboardInterrupt:
        print("\n\nInterrupted! Saving progress...")
        conn.commit()

    except Exception as e:
        print(f"\nError during processing: {e}")
        conn.commit()
        raise

    # Summary
    end_time = time.time()
    total_time = end_time - start_time

    print("-" * 60)
    print(f"\nProcessing complete!")
    print(f"  Rows inserted: {records_processed:,}")
    print(f"  Skipped (no pID / no owner data): {records_skipped:,}")
    print(f"  Total time: {format_time(total_time)}")
    print(f"  Average rate: {records_processed/total_time:,.0f} records/sec")

    # Create indexes
    create_indexes(conn)

    # Final row count
    cursor.execute("SELECT COUNT(*) FROM property_owner")
    count = cursor.fetchone()[0]
    print(f"\nTotal rows in property_owner: {count:,}")

    conn.close()
    return records_processed


# ============================================================================
# Entry Point
# ============================================================================

def _validate_json_file():
    """Check JSON source file before loading. Raises on hard failures, warns on soft ones."""

    # Check 1 — file existence
    if not JSON_FILE.exists():
        raise FileNotFoundError(
            f"Source JSON not found: {JSON_FILE}\n"
            f"  Run 'python scripts/fetch_tcad.py' to download it."
        )

    # Check 2 — file size (full export is ~29GB; below 10GB likely a partial download)
    size_gb = JSON_FILE.stat().st_size / (1024 ** 3)
    MIN_SIZE_GB = 10.0
    if size_gb < MIN_SIZE_GB:
        raise ValueError(
            f"JSON file is only {size_gb:.1f} GB — expected ~29 GB.\n"
            f"  This likely indicates an incomplete download.\n"
            f"  Delete the file and run 'python scripts/fetch_tcad.py' to re-download."
        )
    print(f"  JSON file: {JSON_FILE.name} ({size_gb:.1f} GB)")

    # Check 3 — stale file warning (soft, does not block)
    match = re.search(r'(\d{8})', JSON_FILE.name)
    if match:
        try:
            file_date = datetime.strptime(match.group(1), '%Y%m%d').date()
            age_days = (date.today() - file_date).days
            if age_days > 180:
                print(f"  WARNING: Export is {age_days} days old (dated {file_date}).")
                print("  A newer TCAD export may be available at traviscad.org.")
                print("  Update SELECTED_EXPORT in fetch_tcad.py and re-run it to refresh.")
        except ValueError:
            pass


def _validate_db_file():
    """
    Check that the database this script adds a table to already exists.

    Unlike load_protax_to_sqlite.py, this script doesn't build the database
    from scratch — it depends on the properties table load_protax_to_sqlite.py
    creates, since property_owner has a foreign key back to it.
    """
    if not DB_FILE.exists():
        raise FileNotFoundError(
            f"Database not found: {DB_FILE}\n"
            f"  Run 'python scripts/load_protax_to_sqlite.py' (or 'python main.py') first."
        )
    print(f"  Database file: {DB_FILE.name}")


def run():
    """
    Run the full owner load. A full pass over the 29GB export — comparable
    in runtime to Stage 1.
    """
    print("=" * 60)
    print("Travis County Property Tax Export - Owner Loader")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

    _validate_json_file()
    _validate_db_file()

    load_owners_to_sqlite(JSON_FILE, DB_FILE)
    print("\nSuccess!")


if __name__ == "__main__":
    run()
