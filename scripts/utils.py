"""
Shared helpers used across multiple pipeline scripts.

Anything here should be general-purpose (formatting, small conversions,
generic file validation) — schema, SQL, and business logic specific to one
script stays in that script.
"""

import json
import re
import sqlite3
import time
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def format_time(seconds: float) -> str:
    """Format seconds into a human-readable string."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}m"
    else:
        return f"{seconds/3600:.1f}h"


def format_size(bytes_size: float) -> str:
    """Format bytes into a human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.1f}{unit}"
        bytes_size /= 1024
    return f"{bytes_size:.1f}TB"


def json_default_decimal(value):
    """
    json.dumps `default=` callback: converts a Decimal found anywhere inside
    a nested structure (list/dict values json.dumps can't serialize on its
    own). Needed because ijson parses JSON numbers as Decimal by default,
    and nested structures (e.g. an owner's leftover `agents`/`ownerTaxable`
    arrays packed into `extra_fields`) can bury Decimals arbitrarily deep.
    """
    if isinstance(value, Decimal):
        return int(value) if value == int(value) else float(value)
    return str(value)


def convert_value(value):
    """Convert Decimal and other unsupported types for SQLite."""
    if value is None:
        return None
    if isinstance(value, Decimal):
        return int(value) if value == int(value) else float(value)
    if isinstance(value, (list, dict)):
        return json.dumps(value, default=json_default_decimal)
    return value


def get_value(record: dict, key: str, default=None):
    """Safely get a value from a record, converting types as needed."""
    value = record.get(key, default)
    return convert_value(value)


def create_table_from_schema(conn, table_schema: dict) -> None:
    """
    Create (or reset) a table from a declarative schema dict:
        {
            "table": "deeds",
            "columns": {"deedID": "INTEGER", "deedDt": "TEXT", ...},
            "extra_fields": True,
        }
    Keyed by (pID, pYear), not pID alone -- multi-vintage support added
    2026-08-17: the same pID can legitimately appear in more than one
    year's export (e.g. 2025 and 2026), and each year's row needs to
    coexist rather than collide. Drops and recreates only this table --
    safe to re-run without touching any other table in the database.
    """
    table = table_schema["table"]
    columns = table_schema["columns"]

    col_defs = [
        "id INTEGER PRIMARY KEY AUTOINCREMENT",
        "pID INTEGER NOT NULL",
        "pYear INTEGER NOT NULL",
    ]
    for name, sql_type in columns.items():
        col_defs.append(f"{name} {sql_type}")
    if table_schema.get("extra_fields", True):
        col_defs.append("extra_fields TEXT")
    col_defs.append("FOREIGN KEY (pID, pYear) REFERENCES properties(pID, pYear)")

    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {table}")
    cursor.execute(f"CREATE TABLE {table} ({', '.join(col_defs)})")
    cursor.execute(f"CREATE INDEX idx_{table}_pID_pYear ON {table}(pID, pYear)")
    conn.commit()


# Keys every nested raw object redundantly carries a copy of (the parent
# parcel's pID/pYear) or that collide with a fixed column
# create_table_from_schema() always adds (the autoincrement `id`) -- never
# worth surfacing in extra_fields, since they're either already captured in
# a dedicated column or add nothing (see scripts/schema_codegen.py's
# ALWAYS_EXCLUDE, which this mirrors so the two stay in sync).
_RESERVED_KEYS = {"pID", "id", "pYear"}


def insert_generic_row(cursor, table_schema: dict, record: dict, pID: int, pYear: int) -> None:
    """
    Insert one row into a table built by create_table_from_schema(), pulling
    each declared column out of `record` and packing any leftover keys into
    `extra_fields` -- the generic replacement for a bespoke insert_X()
    function per nested array. `pYear` comes from the parent parcel record
    (passed down explicitly, not read off `record` itself -- nested arrays
    don't reliably carry their own copy).
    """
    table = table_schema["table"]
    columns = table_schema["columns"]

    values = [pID, pYear] + [get_value(record, col) for col in columns]
    placeholders = ", ".join(["?"] * len(values))
    col_names = ", ".join(columns.keys())

    if table_schema.get("extra_fields", True):
        extra = {
            k: convert_value(v) for k, v in record.items()
            if k not in columns and k not in _RESERVED_KEYS
        }
        values.append(json.dumps(extra) if extra else None)
        cursor.execute(
            f"INSERT INTO {table} (pID, pYear, {col_names}, extra_fields) VALUES ({placeholders}, ?)",
            values,
        )
    else:
        cursor.execute(
            f"INSERT INTO {table} (pID, pYear, {col_names}) VALUES ({placeholders})",
            values,
        )


def insert_flat_array_rows(cursor, table_schema: dict, record: dict, pID: int, pYear: int) -> None:
    """
    Insert one row per element of a single-level array on `record`, e.g.
    record["deeds"] -> one insert_generic_row() call per deed. table_schema
    must carry "source_key" (the raw JSON key to look up on the record) --
    generated by scripts/schema_codegen.py. Not used for nested cases like
    owners/agents, which need custom traversal (merging owner + ownerValue,
    iterating agents per owner) handled by their own loader function.
    """
    source_key = table_schema["source_key"]
    for item in record.get(source_key) or []:
        insert_generic_row(cursor, table_schema, item, pID, pYear)


def preflight_check_tables(db_path: Path, min_row_counts: dict, label: str) -> bool:
    """
    Generic fail-fast preflight: return True if `db_path` exists and every
    table in min_row_counts (name -> minimum row count) exists and meets its
    threshold. Prints PASS/FAIL per table as it goes. Shared by
    stage0_preflight.py and ancillary_data_preflight.py -- the two scripts
    differ only in which tables/thresholds they check.
    """
    print(f"\n=== {label} Preflight: Table Check ===")

    if not db_path.exists():
        print("  No database found.")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = {row[0] for row in cursor.fetchall()}

        all_ok = True
        for table, min_rows in min_row_counts.items():
            if table not in existing_tables:
                print(f"  FAIL  Table '{table}' not found.")
                all_ok = False
                continue
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            if count < min_rows:
                print(f"  FAIL  {table} has only {count:,} rows — expected at least {min_rows:,}.")
                all_ok = False
            else:
                print(f"  PASS  {table}: {count:,} rows")

        conn.close()
        return all_ok

    except sqlite3.DatabaseError as e:
        print(f"  FAIL  Database error: {e}")
        return False


def make_checker():
    """
    Returns a `check(description, condition, detail="")` closure that prints
    PASS/FAIL and tallies results, plus a `counts` dict ({"passed": n,
    "failed": n}) that updates live -- the shared PASS/FAIL tally pattern
    used by every *_output_test.py script.
    """
    counts = {"passed": 0, "failed": 0}

    def check(description, condition, detail=""):
        if condition:
            print(f"  PASS  {description}")
            counts["passed"] += 1
        else:
            print(f"  FAIL  {description}" + (f" - {detail}" if detail else ""))
            counts["failed"] += 1
        return condition

    return check, counts


def check_extra_fields_drift(
    cursor, check, table: str, sample_size: int = 2_000, max_rate: float = 0.05
) -> None:
    """
    Drift-detector check (via a `make_checker()` check() closure): samples
    up to `sample_size` rows and asserts extra_fields is non-null on fewer
    than `max_rate` of them. Since columns are generated from a
    full-population scan rather than a hand-picked guess, extra_fields
    should be near-empty in normal operation -- if it's not, that's a real
    signal (a new/missed field), not expected noise. No-ops if the table
    has no extra_fields column. Shared by every *_output_test.py script
    that uses a schema-driven table.
    """
    cursor.execute(f"PRAGMA table_info({table})")
    cols = {row[1] for row in cursor.fetchall()}
    if "extra_fields" not in cols:
        return

    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    if count == 0:
        return

    cursor.execute(
        f"SELECT COUNT(*) FROM (SELECT extra_fields FROM {table} "
        f"WHERE extra_fields IS NOT NULL LIMIT {sample_size})"
    )
    nonnull_sampled = cursor.fetchone()[0]
    sample_n = min(count, sample_size)
    rate = nonnull_sampled / sample_n if sample_n else 0
    check(
        f"{table}.extra_fields non-null rate is low (<{max_rate:.0%})",
        rate < max_rate,
        f"{rate:.1%} non-null in a sample of {sample_n:,}",
    )


def stream_json_and_load(json_path: Path, conn, cursor, process_fn, batch_size: int = 10_000, progress_interval: int = 25_000):
    """
    Stream a top-level JSON array with ijson, calling
    `process_fn(cursor, record) -> bool` per record (True = processed,
    False/falsy = skipped), batching commits and printing progress --
    the shared main-loop driver behind every load_*_to_sqlite.py script
    (batch commits, progress printing, KeyboardInterrupt handling, and
    per-record exception isolation were previously hand-duplicated in each).

    Returns (processed, failed, elapsed_seconds). Commits on completion,
    on KeyboardInterrupt, and re-raises any other exception after
    committing whatever was processed so far.
    """
    import ijson

    file_size = json_path.stat().st_size
    start_time = time.time()
    processed = 0
    failed = 0

    try:
        with open(json_path, "rb") as f:
            parser = ijson.items(f, "item")

            for record in parser:
                try:
                    if process_fn(cursor, record):
                        processed += 1
                    else:
                        failed += 1
                except Exception as e:
                    failed += 1
                    if failed <= 10:
                        print(f"Error processing record: {e}")

                if processed % batch_size == 0:
                    conn.commit()

                if processed % progress_interval == 0:
                    elapsed = time.time() - start_time
                    rate = processed / elapsed if elapsed > 0 else 0
                    pct_complete = (f.tell() / file_size) * 100
                    print(f"  Processed: {processed:>10,} records | "
                          f"Rate: {rate:>8,.0f}/sec | "
                          f"Progress: {pct_complete:>5.1f}% | "
                          f"Elapsed: {format_time(elapsed)}")

        conn.commit()

    except KeyboardInterrupt:
        print("\n\nInterrupted! Saving progress...")
        conn.commit()

    except Exception as e:
        print(f"\nError during processing: {e}")
        conn.commit()
        raise

    elapsed = time.time() - start_time
    return processed, failed, elapsed


def optimize_for_bulk_insert(conn) -> None:
    """Configure SQLite for fast bulk inserts."""
    cursor = conn.cursor()
    cursor.execute("PRAGMA synchronous = OFF")
    cursor.execute("PRAGMA journal_mode = MEMORY")
    cursor.execute("PRAGMA cache_size = -64000")  # 64MB cache
    cursor.execute("PRAGMA temp_store = MEMORY")
    conn.commit()


def validate_json_file(json_file: Path, min_size_gb: float = 10.0) -> None:
    """
    Check a TCAD JSON source file before loading. Raises on hard failures
    (missing file, implausibly small file); warns on soft ones (stale export)
    without blocking.
    """
    if not json_file.exists():
        raise FileNotFoundError(
            f"Source JSON not found: {json_file}\n"
            f"  Run 'python scripts/fetch_tcad.py' to download it."
        )

    size_gb = json_file.stat().st_size / (1024 ** 3)
    if size_gb < min_size_gb:
        raise ValueError(
            f"JSON file is only {size_gb:.1f} GB — expected ~29 GB.\n"
            f"  This likely indicates an incomplete download.\n"
            f"  Delete the file and run 'python scripts/fetch_tcad.py' to re-download."
        )
    print(f"  JSON file: {json_file.name} ({size_gb:.1f} GB)")

    match = re.search(r'(\d{8})', json_file.name)
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
