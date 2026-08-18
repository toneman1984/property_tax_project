# Travis County Homestead Exemption Fraud Analysis

Texas law requires homeowners to use a property as their primary residence to claim a homestead exemption. This project investigates how much Travis County tax revenue is at risk from exemptions claimed on properties that aren't actually primary residences, using TCAD (Travis Central Appraisal District) property tax data.

**Current phase: EDA-first source data investigation** (`docs/tcad_eda/`). Two earlier approaches — a neighborhood-level STR/Airbnb density correlation, then a parcel-level ML risk model — were explored, found real results, and are now archived (`archive/`) in favor of going back to first principles on the raw TCAD export before committing to any modeling approach again. See `docs/fraud_model_pivot.md` for the full decision history of both pivots.

---

## Current Status

A full recursive scan of the raw 29GB TCAD JSON export (`scripts/inventory_scan_full.py`) found that the database was missing far more than initially known — 11 top-level data arrays (`deeds`, `sales`, `permits`, `appeals`, `taxingunits`, `inspections`, `events`, `tags`, `links`, `notes`, `smartgroups`) were never loaded at all, on top of a lossy owner table that collapsed multi-owner parcels and dropped several owner sub-structures. `deeds`/`sales` in particular carry actual recorded ownership-transfer history and sale prices — more direct fraud-detection evidence than anything either prior approach used.

All of this is now loaded into the database with full fidelity, in one streaming pass per export file, driven by a schema generated from the full-population scan rather than hand-written table-by-table (see `docs/tcad_eda/protax_extraction_structure.md` and `owner_data_structure.md` for what's in each table and why). This is now the project's single settled ingestion step — `main.py`'s Stage 1 — since there's no real distinction left between the original 6 "core" tables and the 14 found later; both are just raw-JSON-to-SQL extraction, verified the same way. See `docs/tcad_eda/00_overview.md` for the current documentation map.

**Multi-vintage support added 2026-08-17**: TCAD reissues the full export each appraisal cycle. A 2026 export appeared on traviscad.org (the 2025 one this project started with was 393 days stale by the time this was noticed) — rather than just replace 2025 with 2026, every table is now keyed by `(pID, pYear)` instead of `pID` alone, so multiple appraisal years coexist in the same database and can be compared directly (e.g. `property_owners.ownerMarketValue` for the same parcel, year over year). `pYear` comes from each record's own field, not filename/config, so adding another year later is just: download it, add its path to `scripts/load_protax_to_sqlite.py`'s `JSON_FILES` list, rerun. Currently loaded: 2025 and 2026. Older years (2019–2024) aren't available in this same rich JSON format — traviscad.org only has them in the much thinner state EARS format (`docs/tcad_eda/ears_state_reference.md`), a different parser, not attempted yet.

---

## Prior Work (archived)

Two earlier approaches were built out fully, produced real results, and were then set aside — not deleted. Code lives in `archive/scripts/`, docs in `archive/docs/`, outputs in `archive/data/products/` and `archive/images/`.

**Neighborhood-level STR/Airbnb correlation** (original proof-of-concept): 246 H3 hex cells, homestead rate vs. Airbnb density r = −0.143 (p = 0.025). Diluted by hex-cell averaging — homestead fraud is a parcel-level phenomenon.

**Parcel-level ML fraud risk model**: gradient boosting classifier on owner/mailing/structural features, ROC-AUC 0.717, ~$357.4M estimated revenue at risk across 11,395 flagged parcels. Set aside after a pattern of features/explanations (STR density, a SHAP sign-instability issue) that looked reasonable but didn't hold up under scrutiny — see `docs/fraud_model_pivot.md`'s "Pivot 2" for the full rationale.

---

## Data Sources

| Dataset | Source | Status |
|---|---|---|
| TCAD property tax export (~29GB) | Travis County Appraisal District | Active — primary data source |
| STR permit locations | City of Austin Open Data Portal | Used in archived POC only |
| Airbnb listings | Inside Airbnb | Used in archived POC only |
| Travis County boundary | U.S. Census TIGERweb REST API | Used in archived POC only |

---

## Pipeline

```
python main.py
```

`main.py` currently runs only Stage 1 (raw JSON → SQLite ingestion, all 20 tables, one streaming pass per vintage) — the one settled, validated pipeline step. It self-skips if the database already exists and passes its checks. Preflight/output-test logic lives in one registry, `scripts/checks.py`, reached by checkpoint name (`"stage1"`) rather than one file per stage.

| Stage | Script | Output |
|---|---|---|
| 1 — Ingest | `load_protax_to_sqlite.py` (gated by `scripts/checks.py`'s `"stage1"` checkpoint) | `travis_property_tax.db` (20 tables, keyed by `(pID, pYear)`) |

Run `scripts/fetch_tcad.py` once beforehand to download every configured TCAD export (`EXPORTS`/`SELECTED_EXPORTS` in that script).

**Phase 1 EDA dev tools** (standalone, run by hand only when the schema needs regenerating — see `scripts/schema_codegen.py`'s docstring):

```
python -m scripts.inventory_scan_full  # full-population structural scan
python -m scripts.schema_codegen        # regenerate table_schemas.py from the scan
```

---

## Setup

Requires [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed to the default user directory.

```
git clone <repository-url>
cd property_tax_project
boot_dev_env.bat
```

`boot_dev_env.bat` creates and activates a conda environment from `environment.yml` (Python 3.12). On subsequent runs it just activates the existing environment.

---

## Project Structure

```
property_tax_project/
├── main.py                            # Stage 1 only (see Pipeline above)
├── scripts/
│   ├── fetch_tcad.py                  # One-time data download (run before main.py)
│   ├── checks.py                      # Preflight/output-test registry (currently just "stage1")
│   ├── load_protax_to_sqlite.py       # Stage 1: properties (root) + 19 schema-driven/blob tables, one streaming pass
│   ├── utils.py                       # Shared helpers (see docs/refactor_for_efficiency.md)
│   ├── inventory_scan_full.py         # Dev tool: full-population structural scan (run occasionally, not per-build)
│   ├── schema_codegen.py              # Dev tool: generates table_schemas.py from the scan
│   └── table_schemas.py               # Generated schema config for 18 tables (do not hand-edit)
├── data/
│   ├── sources/                       # Raw inputs and SQLite DB (gitignored)
│   └── products/                      # Pipeline outputs (gitignored) — currently empty, Stage 1 has no derived products yet
├── docs/
│   ├── tcad_eda/                      # Active — Phase 1 EDA documentation (start at 00_overview.md)
│   ├── project_plan.md                # This project's pipeline plan (Stage 1 + EDA)
│   ├── fraud_model_pivot.md           # Full history of both pivots away from prior approaches
│   ├── refactor_for_efficiency.md     # scripts/utils.py's design history
│   └── potential_data_sources.txt     # Candidate future data sources (rental listings, etc.)
├── archive/                            # Superseded code/docs/outputs, gitignored, kept locally
│   ├── scripts/                       # Archived POC + Stage 4 ML scripts
│   ├── docs/                          # Archived POC + Stage 4 planning/assumptions docs
│   ├── data/products/                 # Archived POC + Stage 4 outputs
│   └── images/                        # Archived POC figures
├── environment.yml
└── boot_dev_env.bat
```
