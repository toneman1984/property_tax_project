"""
Property Tax Pipeline - Entry Point

Loads the raw TCAD export into SQLite -- all 20 tables in one streaming
pass (scripts/load_protax_to_sqlite.py), including the 14 tables found by
a full inventory scan on 2026-08-17 (deeds, sales, owner data, etc. -- see
docs/tcad_eda/). This is currently the only settled pipeline stage -- the
POC (hex aggregation/STR correlation) and Stage 4 ML model that used to run
here were archived the same day (see docs/fraud_model_pivot.md's "Pivot 2"
and archive/ for the moved code) in favor of the EDA-first approach.
scripts/inventory_scan_full.py and scripts/schema_codegen.py stay
standalone (one-off/occasional dev tools, not extraction).

Preflight/output-test logic lives in scripts/checks.py (one registry, not
one file per stage) -- reached here by name.

Usage:
    python main.py
"""

from scripts.checks import run_checkpoint
from scripts.load_protax_to_sqlite import run as load_stage1


if __name__ == "__main__":
    print("\n--- Stage 1: Load TCAD JSON to SQLite ---")
    run_checkpoint("stage1", build_fn=load_stage1)

    print("\nPipeline complete.")
