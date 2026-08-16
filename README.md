# Travis County Homestead Exemption Fraud Analysis

Texas law requires homeowners to use a property as their primary residence to claim a homestead exemption. This project estimates how much Travis County tax revenue is at risk from exemptions likely claimed on properties that aren't primary residences, using a parcel-level model built from TCAD ownership and structural data — owner mailing-address mismatches, out-of-state ownership, and property characteristics. It began as a neighborhood-level proof-of-concept testing whether short-term rental (STR) density predicted the same thing; that signal turned out not to hold up at the parcel level (see `docs/fraud_model_pivot.md`), and the owner-occupancy signals below are now the project's central finding.

---

## Key Findings

### Parcel-Level Fraud Risk Model

| Metric | Value |
|---|---|
| Homestead parcels scored | 226,676 |
| Flagged as high-risk (top 5% by model score) | 11,395 |
| ...of which individually-owned, not caught by the deterministic entity-ownership rule alone | 9,611 (84%) |
| Estimated tax revenue at risk | ~$357.4M |
| Model performance (gradient boosting, held-out test set) | ROC-AUC 0.717 / PR-AUC 0.098 (vs. 0.041 no-skill baseline) |

This is a proxy-labeled, illustrative model, not a fraud determination for any specific parcel — see `docs/fraud_model_assumptions.md` for the full limitations ledger, including a caveat on SHAP directionality for two of the six model features.

### Neighborhood-Level STR/Airbnb Correlation (original proof-of-concept)

![Registration Gap by Hex Cell](images/map_registration_gap.png)

| Metric | Value |
|---|---|
| Hex cells analyzed | 246 |
| Homestead rate vs. Airbnb density | r = −0.143 (p = 0.025) |
| Largest registration gap (single cell) | 242 unregistered listings |
| Airbnb listings vs. STR permits (county-wide) | 7,082 vs. 987 |

The aggregate spatial signal is weak by design — homestead fraud is a parcel-level phenomenon that hex-cell averaging dilutes, and STR density itself turned out not to carry incremental predictive value once parcel-level owner data was available (see `docs/fraud_model_pivot.md`). This analysis remains valid as a neighborhood-level finding and was the original motivation for building the parcel-level model above.

![Homestead Rate vs. Airbnb Density](images/scatter_homestead_vs_airbnb.png)

---

## Data Sources

| Dataset | Source |
|---|---|
| TCAD property tax export (~29GB) | Travis County Appraisal District |
| STR permit locations | City of Austin Open Data Portal |
| Airbnb listings | Inside Airbnb |
| Travis County boundary | U.S. Census TIGERweb REST API |

---

## Pipeline

```
python main.py
```

| Stage | Script | Output |
|---|---|---|
| 0 — Preflight | `stage0_preflight.py` | Checks SQLite DB is ready |
| 1 — Ingest | `load_protax_to_sqlite.py` | `travis_property_tax.db` (~1.1GB) |
| 2 — Aggregate | `aggregate_to_hex.py` | `hex_ratios.geojson` (246 cells) |
| 3 — Visualize | `visualize.py` | 3 figures + 2 CSVs |
| 4 — Fraud Model | `load_owners_to_sqlite.py`, `build_fraud_features.py`, `train_fraud_model.py` | `parcel_risk_scores.csv`, `shap_*.csv`, `fraud_model_summary.json` |

Stage 1 is skipped automatically if the database already exists; Stage 4's owner-data load is skipped the same way if `property_owner` is already populated (`stage4_preflight.py`). Run `scripts/fetch_tcad.py` once beforehand to download the raw TCAD export.

---

## Outputs

| File | Description |
|---|---|
| `map_homestead_airbnb.png` | Side-by-side choropleth: homestead rate vs. Airbnb density |
| `map_registration_gap.png` | Unregistered STR listings per hex cell |
| `scatter_homestead_vs_airbnb.png` | Scatter with OLS fit; point size = registration gap |
| `correlation_summary.csv` | Pearson + Spearman correlations: homestead rate vs. Airbnb rate, homestead rate vs. registration gap, Airbnb rate vs. registration gap |
| `candidate_neighborhoods.csv` | Top 25 hex cells by registration gap |

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
├── main.py                        # Full pipeline entry point
├── scripts/
│   ├── fetch_tcad.py              # One-time data download (run before main.py)
│   ├── stage0_preflight.py        # Stage 0: DB check, gates Stage 1
│   ├── load_protax_to_sqlite.py   # Stage 1
│   ├── stage1_output_test.py      # Stage 1 output verification (auto-runs)
│   ├── aggregate_to_hex.py        # Stage 2
│   ├── stage2_output_test.py      # Stage 2 output verification (auto-runs)
│   ├── visualize.py               # Stage 3
│   ├── stage4_preflight.py        # Stage 4: owner-table check, gates owner load
│   ├── load_owners_to_sqlite.py   # Stage 4: owner/value data ingest
│   ├── build_fraud_features.py    # Stage 4: parcel-level feature engineering
│   ├── train_fraud_model.py       # Stage 4: model training, scoring, SHAP
│   ├── stage4_output_test.py      # Stage 4 output verification (auto-runs)
│   └── eda_fraud_features.py      # Standalone: EDA on model features (run manually)
├── images/                        # Committed output figures
├── archive/                       # Superseded docs, preserved for history
│   └── pitch.md                   # Original STR-focused pitch (superseded — see docs/fraud_model_pivot.md)
├── data/
│   ├── sources/                   # Raw inputs and SQLite DB (gitignored)
│   └── products/                  # Pipeline outputs (gitignored)
├── docs/
│   ├── project_plan.md            # Stages 0-3 pipeline implementation reference
│   ├── fraud_model_plan.md        # Stage 4 plan and progress tracker
│   ├── fraud_model_assumptions.md # Stage 4 assumptions/limitations ledger
│   └── fraud_model_pivot.md       # Stage 4 pivot rationale and evidence
├── environment.yml
└── boot_dev_env.bat
```
