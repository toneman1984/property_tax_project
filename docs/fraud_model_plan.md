# Stage 4: Speculative Parcel-Level Homestead Fraud Risk Model

**Status:** Planning complete. Building step-by-step, hands-on — user types and
tests each piece; Claude presents code in segments rather than writing files
directly (see `feedback_learning_approach` memory).

## Progress Tracker

- [ ] 1. Ingest owner/value data — `scripts/load_owners_to_sqlite.py`
- [ ] 2. Parcel-level feature engineering — `scripts/build_fraud_features.py`
- [ ] 3. Model training + scoring — `scripts/train_fraud_model.py`
- [ ] 4. Visualization — `scripts/visualize_fraud_model.py`
- [ ] 5. Pipeline wiring + docs (`main.py`, `stage4_output_test.py`,
      `environment.yml`, `docs/fraud_model_assumptions.md`, `README.md`)

Update the checkboxes above as steps are completed, so any session can see
where we left off at a glance.

## Context

The POC (Stages 1–3) established a hex-level correlation between homestead exemption
rate and Airbnb density (r = −0.143, p = 0.025) but that signal is diluted by
hex-cell averaging — STR-homestead fraud is a parcel-level phenomenon. The original
plan to strengthen the case was to buy proprietary long-term-rental data for
parcel-level matching, but that requires funding, and the funding pitch itself needs
a stronger hook.

Instead: build a speculative, explicitly-labeled parcel-level risk model using data
*already available*, to (a) demonstrate applied ML (proxy-labeled classification,
SHAP interpretation) as a portfolio piece, and (b) produce a concrete "here's what a
model finds even with imperfect data — imagine with verified rental records" pitch
artifact. Every output will be labeled as inferential/illustrative, not a fraud
determination.

**Key discovery during exploration:** the raw 29GB TCAD export
(`data/sources/Travis_protaxExport_20250720.json`) has an `owners` array per parcel
that was never loaded into `travis_property_tax.db`. Each owner record includes:
- `name` / `firstName` / `lastName` — lets us distinguish individual vs. entity
  (LLC/corporate) ownership
- `addrCity` / `addrState` / `addrZip` / `addrDeliveryLine` — owner mailing address,
  comparable against `property_situs` for absentee-owner detection
- `ownerValue[0]` — a value summary per owner including `ownerMarketValue`,
  `ownerAppraisedValue`, `ownerLandHSValue`, `ownerImprovementHSValue` (the
  appraised value currently classified under homestead treatment)

This gives one **legally-grounded, non-speculative** signal: Texas homestead
exemptions require individual owner-occupancy, so an LLC/corporate owner with an
active "HS" exemption is already a strong red flag — not a hand-waved assumption.

**Methodology note (avoiding circularity):** the plan deliberately avoids training a
model to predict a score that was computed from the same inputs (which would just
recover a formula we already wrote and add no real ML value). Instead:
1. Define a **high-confidence proxy positive**: `has_homestead AND is_entity_owner`
   (the deterministic legal red flag).
2. Train a classifier to predict that proxy label using a **disjoint feature set**
   that excludes ownership-entity signals (STR/Airbnb density, absentee mailing
   address, out-of-state owner, property characteristics) — features that are
   *correlated with* but not *definitional of* the label.
3. Apply the trained model to **all** homestead parcels, including individually-owned
   ones that never trip the deterministic rule. High-scoring individually-owned
   parcels are the interesting output: parcels that look like the entity-owned
   red-flag cases along STR/mailing/occupancy dimensions, without tripping the
   simple rule. That's a genuine generalization claim, not restating the label.
4. SHAP explains which features drive each parcel's score.

This is still fundamentally a proxy-labeled, unvalidated model — the assumption
ledger (below) makes that explicit everywhere the results are shown.

## Implementation

### 1. Ingest owner/value data (new, additive — does not touch existing tables)

New script `scripts/load_owners_to_sqlite.py`, following the exact pattern of
`load_protax_to_sqlite.py` (stream with `ijson`, batch commit, progress logging):
- New table `property_owner` (FK `pID`): flattened primary-owner fields (`name`,
  `firstName`, `lastName`, `addrCity`, `addrState`, `addrZip`,
  `addrDeliveryLine`, `ownerPct`) + flattened `ownerValue` fields
  (`ownerMarketValue`, `ownerAppraisedValue`, `ownerLandHSValue`,
  `ownerImprovementHSValue`, `ownerLandNHSValue`, `ownerImprovementNHSValue`).
- Where a parcel has multiple owners, keep the row with the highest `ownerPct`
  (documented tie-break: first occurrence).
- Skip the deeply-nested `valuations.details.cost-local.*` tree entirely —
  `ownerValue` already has the summary figures needed; loading the full
  improvement/cost detail tree is unnecessary volume for this use case.
- Own preflight check (`property_owner` table exists + plausible row count),
  mirroring `stage0_preflight.py`, so re-running `main.py` doesn't force a
  second 29GB pass once loaded.
- Expected runtime: comparable to Stage 1 (single streaming pass over the same file).

### 2. Parcel-level feature engineering

New script `scripts/build_fraud_features.py`:
- Reuse `load_tcad_parcels()` from `aggregate_to_hex.py` for the SFR/active/
  geocoded parcel universe + `has_homestead` + `hex_id` assignment (same H3
  res-8 logic already validated in Stage 2 — no new spatial code needed).
- Reuse `load_str_airbnb()` for hex-level STR/Airbnb counts, but join the
  **unfiltered** hex counts (before Stage 2's `MIN_SFR_TOTAL`/`MIN_AIRBNB_*`
  thresholds) so every parcel gets an `airbnb_rate`/`str_permit_rate`/
  `registration_gap` value, not just the 246 POC cells.
- Join `property_owner` and `property_situs` on `pID` to derive:
  - `is_entity_owner` (regex on `name` for LLC/INC/CORP/LP/LTD/TRUST, or
    `firstName`/`lastName` both null with non-null `name`)
  - `mailing_ne_situs` (owner `addrCity`/`addrZip` vs. situs `city`/`zip`)
  - `out_of_state_owner` (`addrState` != 'TX')
- Join `property_characteristics`/`property_profile` for structural features
  (`imprvActualYearBuilt`, `imprvMainArea`, land size from `extra_fields`,
  `imprvClass`/`imprvCondition`).
- Output: `data/products/parcel_features.csv` (one row per SFR homestead-eligible
  parcel, ~250–500k rows).

### 3. Model training + scoring

New script `scripts/train_fraud_model.py`:
- Proxy label: `has_homestead & is_entity_owner`.
- Feature set for the model: STR/Airbnb hex features, `mailing_ne_situs`,
  `out_of_state_owner`, structural characteristics. **Excludes** `is_entity_owner`
  itself and any owner-name-derived field (leakage prevention — see Context).
- Model: `sklearn.ensemble.HistGradientBoostingClassifier` (handles missing
  values natively, no new heavy dependency like xgboost needed).
- Stratified train/test split, report ROC-AUC / PR-AUC — framed explicitly in
  output text as "ability to reconstruct the proxy definition from indirect
  signals," not real-world fraud detection accuracy.
- SHAP (`shap.TreeExplainer`) for global feature importance + per-parcel
  explanations on the flagged top-N.
- Score all homestead parcels; also keep the simple transparent
  **composite red-flag count** (sum of boolean flags) as an auxiliary baseline
  shown alongside the model score for comparison in the writeup.
- Revenue-at-risk rollup: for parcels above a chosen risk threshold,
  `(ownerLandHSValue + ownerImprovementHSValue) × combined_tax_rate`, using a
  documented, publicly-sourced combined Travis County/Austin ISD rate constant
  (looked up during implementation and cited in the assumptions doc) —
  explicitly an approximation of value currently receiving homestead tax
  treatment, not a precise exemption-dollar calculation.
- Outputs: `data/products/parcel_risk_scores.csv`,
  `data/products/fraud_model_summary.json` (rollup stats), top-N flagged
  parcel list.

### 4. Visualization

Extend the Stage 3 pattern with `scripts/visualize_fraud_model.py`:
- Map of top-risk parcels (point map, colored by risk score) over the county
  boundary (reuse the TIGERweb fetch from `visualize.py`).
- SHAP summary plot (global feature importance).
- Revenue-at-risk bar chart by risk tier.
- Outputs saved to `data/products/`, committed copies to `images/` once
  reviewed (matches existing convention).

### 5. Pipeline wiring + docs

- Add `scripts/stage4_output_test.py` (verification script, matching
  `stage1_output_test.py`/`stage2_output_test.py` conventions) and wire
  Stage 4 into `main.py` after Stage 3.
- Add `scikit-learn` and `shap` to `environment.yml`.
- New `docs/fraud_model_assumptions.md`: explicit, itemized assumption ledger
  (proxy label ≠ ground truth; revenue estimate simplifies real TX exemption
  stacking rules; STR/Airbnb density is a geographic proxy, not parcel-specific
  proof; known ~13–14% geometry-null exclusion carries over from Stage 2).
- Update `README.md` pipeline table (Stage 4 row) and project structure section.
- Leave `docs/pitch.md` / `docs/project_plan.md` narrative updates for a
  follow-up pass once actual results are in hand — not drafted blindly now.

## Verification

- Run `python main.py` end-to-end; confirm Stage 4 scripts execute without
  error and `stage4_output_test.py` passes (row counts, no-null-score checks,
  proxy label prevalence sanity check).
- Manually inspect a handful of top-flagged parcels' feature rows for
  plausibility (e.g., an entity-owned homestead parcel with high STR density
  should score high; spot-check a few via the situs address).
- Confirm SHAP explanations are directionally sensible (e.g., higher
  `airbnb_rate` and `mailing_ne_situs=1` push risk score up).
- Review `fraud_model_summary.json` revenue-at-risk figure for order-of-magnitude
  plausibility against the known ~7,082 active Airbnb / 987 STR-permit gap from
  the Stage 2/3 POC.
