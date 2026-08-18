"""
Load Travis County Property Tax Export JSON to SQLite

This script handles 28GB+ JSON files by:
1. Streaming with ijson (never loads full file into memory)
2. Creating normalized tables for nested arrays
3. Inserting in batches with progress tracking
4. Using SQLite optimizations for bulk inserts

One streaming pass per configured export file builds every table this
project extracts from the raw export -- 20 total:

- `properties` -- the root table, hand-declared (pID is its literal primary
  key, not a child array under something)
- 16 single-level child tables, schema-driven (columns generated from a
  full-population inventory scan rather than hand-picked --
  scripts/schema_codegen.py -> scripts/table_schemas.py; see
  docs/tcad_eda/ for how each was discovered): the original 5
  (property_legal_description/identification/characteristics/situs/profile)
  plus 11 more found by the full inventory scan (deeds, sales, permits,
  appeals, taxingunits, inspections, events, tags, links, notes,
  smartgroups)
- `property_owners` / `property_owner_agents` -- full owner fidelity
  (merges each owner's ownerValue onto one row; a proper 1:many agents
  table), superseding the old lossy property_owner table
  (archive/scripts/load_owners_to_sqlite.py, dropped from the live
  database 2026-08-17)
- `property_valuations` -- the deep valuations{} tree stored whole as a
  JSON blob rather than normalized

Merged from two separate scripts (load_protax_to_sqlite.py +
load_ancillary_data_to_sqlite.py) on 2026-08-17: once everything used the
same schema-driven machinery and the full inventory scan verified all of
it, the "core Stage 1" vs. "ancillary Phase 1 EDA" split no longer
reflected a real difference -- both were just raw-JSON-to-SQL extraction,
now done in one pass instead of two. scripts/inventory_scan_full.py and
scripts/schema_codegen.py remain standalone (genuinely one-off/occasional
dev tools, not extraction itself).

Multi-vintage support added the same day: every table is keyed by
(pID, pYear), not pID alone. TCAD reissues the whole export as a new
"vintage" each appraisal cycle (e.g. 2025, 2026), and the same pID
legitimately recurs across years -- pID alone would collide across
vintages, silently overwriting one year with another. `pYear` comes
straight from each record's own `pYear` field (confirmed stable and
present on every record), not from filename/config -- so JSON_FILES below
is just a list of files to process; nothing needs to be manually tagged by
year. Re-running against the SAME file correctly overwrites that file's
own (pID, pYear) rows (INSERT OR REPLACE); a genuinely different vintage
coexists.

Idempotent and self-contained: only ever drops/recreates the 20 tables
listed above, never the whole database file.

Usage:
    python -m scripts.load_protax_to_sqlite
"""

import sqlite3
import os
import json
from datetime import datetime

from scripts.utils import (
    PROJECT_ROOT, format_time, format_size, convert_value, get_value,
    optimize_for_bulk_insert, validate_json_file, stream_json_and_load,
    create_table_from_schema, insert_generic_row, insert_flat_array_rows,
    json_default_decimal,
)
from scripts.table_schemas import TABLE_SCHEMAS


# ============================================================================
# Configuration
# ============================================================================

DATA_RAW = PROJECT_ROOT / "data" / "sources"

# Every export to load, oldest first (order doesn't affect correctness --
# INSERT OR REPLACE means later files just overwrite same-(pID,pYear) rows
# -- but processing oldest-first keeps progress output intuitive). Add a
# new entry here (and download it via scripts/fetch_tcad.py) whenever a
# new vintage becomes available; nothing else needs to change, since pYear
# is read from each record, not this list.
JSON_FILES = [
    DATA_RAW / "Travis_protaxExport_20250720.json",
    DATA_RAW / "Travis_protaxExport_20260731.json",
]
DB_FILE = DATA_RAW / "travis_property_tax.db"

BATCH_SIZE = 10_000  # Records per commit
PROGRESS_INTERVAL = 10_000  # Print progress every N records

# The 16 single-level tables built via the generic insert_flat_array_rows()
# path (each schema's own "source_key", set by scripts/schema_codegen.py,
# gives the raw JSON key to iterate -- no need to duplicate that mapping
# here). "property_owners"/"property_owner_agents" need custom traversal
# (merging owner + ownerValue, iterating agents within each owner) so
# they're handled by their own insert_owners() below instead.
FLAT_TABLES = [
    # Originally Stage 1's 5 "core" child tables
    "property_legal_description",
    "property_identification",
    "property_characteristics",
    "property_situs",
    "property_profile",
    # Found by the full inventory scan, 2026-08-17
    "deeds", "sales", "permits", "appeals", "taxingunits",
    "inspections", "events", "tags", "links", "notes", "smartgroups",
]

CREATE_VALUATIONS_TABLE = """
CREATE TABLE IF NOT EXISTS property_valuations (
    pID INTEGER NOT NULL,
    pYear INTEGER NOT NULL,
    valuations_json TEXT,
    PRIMARY KEY (pID, pYear),
    FOREIGN KEY (pID, pYear) REFERENCES properties(pID, pYear)
);
"""


# ============================================================================
# Schema: properties (root table -- hand-declared, (pID, pYear) is its real PK)
# ============================================================================

CREATE_PROPERTIES_TABLE = """
CREATE TABLE IF NOT EXISTS properties (
    pID INTEGER NOT NULL,
    pYear INTEGER NOT NULL,
    pRollCorr INTEGER,
    pVersion INTEGER,
    propCreateDt TEXT,
    propType TEXT,
    sitProperty INTEGER,
    reactivateDt TEXT,
    reactivateReason TEXT,
    reactivateNotes TEXT,
    rollCorrCode TEXT,
    rollCorrReason TEXT,
    exemptionReset INTEGER,
    exemptionResetReason TEXT,
    geometry TEXT,
    inactive INTEGER,
    inactiveDt TEXT,
    inactiveReason TEXT,
    inactiveNotes TEXT,
    inspectionYr INTEGER,
    lastAppraisalDt TEXT,
    taxingUnitPercentCalculation TEXT,
    taxingUnitPercentCalculationComment TEXT,
    taxingUnitSplitBoundaryLines INTEGER,
    isUDI INTEGER,
    PRIMARY KEY (pID, pYear)
);
"""

# Extra indexes beyond the automatic idx_{table}_pID_pYear that
# create_table_from_schema() already adds for each schema-driven table.
CREATE_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_properties_pYear ON properties(pYear);
CREATE INDEX IF NOT EXISTS idx_properties_propType ON properties(propType);
CREATE INDEX IF NOT EXISTS idx_properties_inactive ON properties(inactive);
CREATE INDEX IF NOT EXISTS idx_situs_zip ON property_situs(zip);
CREATE INDEX IF NOT EXISTS idx_situs_streetName ON property_situs(streetName);
CREATE INDEX IF NOT EXISTS idx_identification_geoID ON property_identification(geoID);
"""


# ============================================================================
# Database Functions
# ============================================================================

def create_database(db_path):
    """
    Create/reset every table this script owns (properties + 16 schema-driven
    flat tables + property_owners/property_owner_agents + the
    property_valuations blob table) -- 20 total, all keyed by (pID, pYear).
    Never touches the database file itself, and doesn't touch any table
    outside this list, so it's safe to re-run.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS properties")
    cursor.execute(CREATE_PROPERTIES_TABLE)

    schemas_by_table = {s["table"]: s for s in TABLE_SCHEMAS}
    for table_name in FLAT_TABLES + ["property_owners", "property_owner_agents"]:
        create_table_from_schema(conn, schemas_by_table[table_name])

    cursor.execute("DROP TABLE IF EXISTS property_valuations")
    cursor.execute(CREATE_VALUATIONS_TABLE)

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


def insert_property(cursor, record, pYear):
    """Insert main property record."""
    sql = """
    INSERT OR REPLACE INTO properties (
        pID, pYear, pRollCorr, pVersion, propCreateDt, propType, sitProperty,
        reactivateDt, reactivateReason, reactivateNotes, rollCorrCode, rollCorrReason,
        exemptionReset, exemptionResetReason, geometry, inactive, inactiveDt,
        inactiveReason, inactiveNotes, inspectionYr, lastAppraisalDt,
        taxingUnitPercentCalculation, taxingUnitPercentCalculationComment,
        taxingUnitSplitBoundaryLines, isUDI
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(sql, (
        get_value(record, 'pID'),
        pYear,
        get_value(record, 'pRollCorr'),
        get_value(record, 'pVersion'),
        get_value(record, 'propCreateDt'),
        get_value(record, 'propType'),
        get_value(record, 'sitProperty'),
        get_value(record, 'reactivateDt'),
        get_value(record, 'reactivateReason'),
        get_value(record, 'reactivateNotes'),
        get_value(record, 'rollCorrCode'),
        get_value(record, 'rollCorrReason'),
        get_value(record, 'exemptionReset'),
        get_value(record, 'exemptionResetReason'),
        get_value(record, 'geometry'),
        get_value(record, 'inactive'),
        get_value(record, 'inactiveDt'),
        get_value(record, 'inactiveReason'),
        get_value(record, 'inactiveNotes'),
        get_value(record, 'inspectionYr'),
        get_value(record, 'lastAppraisalDt'),
        get_value(record, 'taxingUnitPercentCalculation'),
        get_value(record, 'taxingUnitPercentCalculationComment'),
        get_value(record, 'taxingUnitSplitBoundaryLines'),
        get_value(record, 'isUDI'),
    ))


def insert_owners(cursor, schemas_by_table, pID, pYear, owners):
    """
    Full owner fidelity: one row per owner (not just the highest-ownerPct
    "primary" owner), each owner's ownerValue[0] flattened onto the same
    row (confirmed always length 1 across the full population), plus a
    proper 1:many agents table.
    """
    owners_schema = schemas_by_table["property_owners"]
    agents_schema = schemas_by_table["property_owner_agents"]

    for owner in owners or []:
        combined = dict(owner)
        owner_values = owner.get("ownerValue") or []
        if owner_values:
            combined.update(owner_values[0])
        insert_generic_row(cursor, owners_schema, combined, pID, pYear)

        for agent in owner.get("agents") or []:
            insert_generic_row(cursor, agents_schema, agent, pID, pYear)


def insert_valuations(cursor, pID, pYear, record):
    """Store the deep valuations{} tree whole as a JSON blob (not normalized)."""
    valuations = record.get("valuations")
    if valuations:
        cursor.execute(
            "INSERT OR REPLACE INTO property_valuations (pID, pYear, valuations_json) VALUES (?, ?, ?)",
            (pID, pYear, json.dumps(valuations, default=json_default_decimal)),
        )


def process_record(cursor, schemas_by_table, record):
    """Process a single property record and insert into all 20 tables."""
    pID = convert_value(record.get('pID'))
    pYear = convert_value(record.get('pYear'))
    if pID is None or pYear is None:
        return False

    insert_property(cursor, record, pYear)

    for table_name in FLAT_TABLES:
        insert_flat_array_rows(cursor, schemas_by_table[table_name], record, pID, pYear)

    insert_owners(cursor, schemas_by_table, pID, pYear, record.get("owners"))
    insert_valuations(cursor, pID, pYear, record)

    return True


# ============================================================================
# Main Processing
# ============================================================================

def load_json_to_sqlite(json_paths, db_path, batch_size=BATCH_SIZE):
    """
    Stream each JSON file in `json_paths` into the same SQLite database
    (tables created once, up front; each file just contributes more rows,
    keyed by its own records' pYear).
    """
    for p in json_paths:
        validate_json_file(p)

    db_path.parent.mkdir(parents=True, exist_ok=True)

    print("Creating tables (properties + 19 schema-driven/blob tables)...")
    conn = create_database(db_path)
    optimize_for_bulk_insert(conn)
    cursor = conn.cursor()
    schemas_by_table = {s["table"]: s for s in TABLE_SCHEMAS}

    def process_fn(cursor, record):
        return process_record(cursor, schemas_by_table, record)

    total_processed = 0
    total_failed = 0
    total_time = 0.0

    for json_path in json_paths:
        file_size = os.path.getsize(json_path)
        print(f"\n{'='*60}")
        print(f"Input file: {json_path}")
        print(f"File size: {format_size(file_size)}")
        print("Processing records...")
        print("-" * 60)

        processed, failed, elapsed = stream_json_and_load(
            json_path, conn, cursor, process_fn,
            batch_size=batch_size, progress_interval=PROGRESS_INTERVAL,
        )

        print("-" * 60)
        print(f"  Records processed: {processed:,}")
        print(f"  Failed records: {failed:,}")
        print(f"  Time: {format_time(elapsed)}")
        print(f"  Rate: {processed/elapsed:,.0f} records/sec" if elapsed else "")

        total_processed += processed
        total_failed += failed
        total_time += elapsed

    print(f"\n{'='*60}")
    print(f"All files processed!")
    print(f"  Total records processed: {total_processed:,}")
    print(f"  Total failed: {total_failed:,}")
    print(f"  Total time: {format_time(total_time)}")

    create_indexes(conn)

    print("\nTable row counts:")
    all_tables = ['properties'] + FLAT_TABLES + [
        'property_owners', 'property_owner_agents', 'property_valuations'
    ]
    for table in all_tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  {table}: {count:,}")

    cursor.execute("SELECT pYear, COUNT(*) FROM properties GROUP BY pYear ORDER BY pYear")
    print("\nproperties by pYear (vintage):")
    for pyear, count in cursor.fetchall():
        print(f"  {pyear}: {count:,}")

    conn.close()
    db_size = os.path.getsize(db_path)
    print(f"\nDatabase file size: {format_size(db_size)}")

    return total_processed


# ============================================================================
# Entry Point
# ============================================================================

def run():
    print("=" * 60)
    print("Travis County Property Tax Export - JSON to SQLite Loader")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Vintages: {len(JSON_FILES)} file(s)")
    print("=" * 60)

    load_json_to_sqlite(JSON_FILES, DB_FILE)
    print("\nSuccess!")


if __name__ == "__main__":
    run()
