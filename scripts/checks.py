"""
Single registry of pipeline "checkpoints" -- consolidates what used to be
four separate files (stage0_preflight.py, stage1_output_test.py,
ancillary_data_preflight.py, ancillary_data_output_test.py) into one place.

Each checkpoint pairs a preflight check (should this stage's build step
run?) with an output test (did the build actually work?) via a small config
dict in CHECKPOINTS below, both built on the shared helpers in
scripts/utils.py (preflight_check_tables, make_checker,
check_extra_fields_drift).

main.py reaches a checkpoint and calls into this module by name, rather
than importing per-stage functions directly:

    from scripts.checks import run_checkpoint
    from scripts.load_protax_to_sqlite import run as load_stage1
    run_checkpoint("stage1", build_fn=load_stage1)

run_checkpoint() only rebuilds+reverifies when preflight fails -- if the
checkpoint's tables already look right, it's a no-op, matching the
original main.py behavior of only re-running the output test right after a
fresh build, not on every skip-because-already-built run.

There was previously a second "ancillary" checkpoint for the 14 tables
discovered by the full inventory scan, kept deliberately separate from
"stage1" and out of main.py while that data's shape was still being
verified. Merged back into "stage1" on 2026-08-17 once
load_protax_to_sqlite.py itself was merged into one script covering all 20
tables -- the "core" vs. "ancillary" split no longer reflected a real
difference (see that script's docstring). scripts/inventory_scan_full.py
and scripts/schema_codegen.py remain standalone (one-off/occasional dev
tools, not extraction).

CLI:
    python -m scripts.checks preflight stage1
    python -m scripts.checks test stage1
    python -m scripts.checks run stage1
"""

import sqlite3

from scripts.utils import PROJECT_ROOT, preflight_check_tables, make_checker, check_extra_fields_drift

DB_PATH = PROJECT_ROOT / "data" / "sources" / "travis_property_tax.db"


# ============================================================================
# Checkpoint-specific extra checks (beyond the shared row-count/drift checks)
# ============================================================================

def _stage1_extra_checks(cursor, check):
    # Multi-vintage support (2026-08-17): every table is keyed by
    # (pID, pYear), so counts now scale with however many vintages are
    # loaded rather than a single fixed number. Check ratios/uniqueness
    # relative to `properties` (the source of truth for "how many
    # (pID, pYear) rows should exist") instead of a hardcoded range.
    cursor.execute("SELECT COUNT(*) FROM properties")
    properties_count = cursor.fetchone()[0]

    cursor.execute("SELECT pYear, COUNT(*) FROM properties GROUP BY pYear ORDER BY pYear")
    by_year = cursor.fetchall()
    check(
        f"properties spans at least 1 vintage (found {len(by_year)}: "
        + ", ".join(f"{y}={c:,}" for y, c in by_year) + ")",
        len(by_year) >= 1,
    )

    # Known multiplicity for owners, confirmed by a full-population scan
    # (see docs/tcad_eda/owner_data_structure.md): ~1.00015 owners per
    # parcel in the 2025 vintage (only 30 of 486,859 parcels have >1 owner).
    # Should hold per-vintage, so the ratio over ALL loaded vintages should
    # still land just above 1.0 regardless of how many years are loaded.
    cursor.execute("SELECT COUNT(*) FROM property_owners")
    owner_count = cursor.fetchone()[0]
    ratio = owner_count / properties_count if properties_count else 0
    check(
        "property_owners count is ~1x properties count (1.0-1.01)",
        properties_count > 0 and 1.0 <= ratio <= 1.01,
        f"{owner_count:,} owners / {properties_count:,} properties = {ratio:.4f}",
    )

    cursor.execute("SELECT COUNT(DISTINCT pID || '-' || pYear) FROM property_valuations")
    distinct_pid_year = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM property_valuations")
    total_rows = cursor.fetchone()[0]
    check(
        "property_valuations has one row per (pID, pYear) (no duplicates)",
        distinct_pid_year == total_rows,
        f"{distinct_pid_year:,} distinct (pID, pYear) pairs vs {total_rows:,} rows",
    )


# ============================================================================
# Registry
# ============================================================================

CHECKPOINTS = {
    "stage1": {
        "label": "Stage 1: TCAD Ingestion",
        "min_size_gb": 0.5,  # guards against a truncated 29GB build
        # Conservative minimums for the 11 tables found by the full
        # inventory scan (halved from the 500-record population-rate
        # sample in docs/tcad_eda/protax_extraction_structure.md, for
        # safety margin against sample noise) -- just enough to catch an
        # empty/truncated load, not an exact expected count. The original
        # 6 "core" tables use a much lower floor since they're always
        # ~1:1 or better with parcel count.
        "min_row_counts": {
            "properties": 100_000,
            "property_profile": 1,
            "property_characteristics": 1,
            "property_situs": 1,
            "property_legal_description": 1,
            "property_identification": 1,
            "property_owners": 400_000,
            "property_owner_agents": 100_000,
            "deeds": 300_000,
            "sales": 100_000,
            "permits": 200_000,
            "appeals": 150_000,
            "taxingunits": 400_000,
            "inspections": 200_000,
            "events": 100_000,
            "tags": 200_000,
            "links": 10_000,
            "notes": 200_000,
            "smartgroups": 1_000,
            "property_valuations": 400_000,
        },
        # property_owners deliberately carries agents/ownerValue/ownerTaxable/
        # exemptions in extra_fields (excluded from real columns on purpose --
        # see docs/tcad_eda/owner_data_structure.md), so it's expected to be
        # ~100% non-null by design, not drift. properties itself has no
        # extra_fields column at all; check_extra_fields_drift() no-ops on it.
        "extra_fields_exempt": {"property_owners"},
        "extra_checks": _stage1_extra_checks,
    },
}


# ============================================================================
# Preflight
# ============================================================================

def preflight(checkpoint: str) -> bool:
    """
    Return True if this checkpoint's tables already exist with plausible
    row counts (and, if configured, a plausible database file size).
    """
    cfg = CHECKPOINTS[checkpoint]
    label = cfg["label"]

    if cfg["min_size_gb"] is not None:
        if not DB_PATH.exists():
            print(f"\n=== {label} Preflight ===")
            print("  No database found.")
            return False
        size_gb = DB_PATH.stat().st_size / (1024 ** 3)
        if size_gb < cfg["min_size_gb"]:
            print(f"\n=== {label} Preflight ===")
            print(f"  FAIL  Database too small ({size_gb:.2f} GB < {cfg['min_size_gb']} GB) — likely incomplete.")
            return False

    ok = preflight_check_tables(DB_PATH, cfg["min_row_counts"], label)
    print("  All preflight checks passed." if ok else "  Preflight failed — rebuild needed.")
    return ok


# ============================================================================
# Output test
# ============================================================================

def output_test(checkpoint: str) -> bool:
    """
    Verify this checkpoint's tables: existence, non-empty, extra_fields
    drift, plus any checkpoint-specific extra checks. Returns True if every
    check passed.
    """
    cfg = CHECKPOINTS[checkpoint]
    check, counts = make_checker()

    print(f"\n=== {cfg['label']}: Output Verification ===")
    check("Database exists", DB_PATH.exists(), f"expected at {DB_PATH}")

    if DB_PATH.exists():
        size_gb = DB_PATH.stat().st_size / (1024 ** 3)
        print(f"  Database size: {size_gb:.2f} GB")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        for table in cfg["min_row_counts"]:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            check(f"Table '{table}' exists and has rows", count > 0, f"row count: {count:,}")
            if table not in cfg["extra_fields_exempt"]:
                check_extra_fields_drift(cursor, check, table)

        if cfg["extra_checks"] is not None:
            cfg["extra_checks"](cursor, check)

        conn.close()

    print(f"\n{'='*40}")
    print(f"Results: {counts['passed']} passed, {counts['failed']} failed")
    print("All checks passed." if counts["failed"] == 0 else "Some checks failed — review output above.")
    print()

    return counts["failed"] == 0


# ============================================================================
# Orchestration
# ============================================================================

def run_checkpoint(checkpoint: str, build_fn=None) -> bool:
    """
    Reach a checkpoint: if preflight already passes, skip entirely (no
    rebuild, no reverification). Otherwise call build_fn() (if given), then
    run the output test to verify the fresh build. Returns the output
    test's pass/fail (or True, if preflight already passed and nothing ran).
    """
    if preflight(checkpoint):
        return True
    if build_fn is not None:
        build_fn()
    return output_test(checkpoint)


# ============================================================================
# CLI
# ============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3 or sys.argv[1] not in ("preflight", "test", "run") or sys.argv[2] not in CHECKPOINTS:
        print(f"Usage: python -m scripts.checks <preflight|test|run> <{'|'.join(CHECKPOINTS)}>")
        sys.exit(1)

    action, checkpoint = sys.argv[1], sys.argv[2]

    if action == "preflight":
        preflight(checkpoint)
    elif action == "test":
        output_test(checkpoint)
    elif action == "run":
        from scripts.load_protax_to_sqlite import run as load_stage1
        build_fns = {"stage1": load_stage1}
        run_checkpoint(checkpoint, build_fn=build_fns[checkpoint])
