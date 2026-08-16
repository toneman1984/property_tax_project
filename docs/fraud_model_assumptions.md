# Stage 4 Fraud Model — Assumptions & Limitations Ledger

Everything produced by `scripts/train_fraud_model.py` (and, later,
`scripts/visualize_fraud_model.py`) is **inferential and illustrative** — a
demonstration of what a model finds using data already on hand, not a fraud
determination about any specific parcel or owner. This document itemizes the
simplifications and limitations behind those outputs so they aren't
overstated in the pitch or misread by anyone reviewing the results later.

## 1. The training label is a legal proxy, not verified ground truth

The model is trained to predict `has_homestead AND is_entity_owner` — chosen
because an LLC/corporate owner with an active homestead exemption is a
legally unambiguous violation (Texas homestead exemptions require individual
owner-occupancy), not because it's the actual object of interest. The real
target — a homestead exemption on a property that isn't the owner's genuine
primary residence — also includes individually-owned parcels that are
non-owner-occupied, which the proxy label cannot capture directly. The model
is deliberately trained on features that exclude ownership-entity signals so
it can be applied to individually-owned parcels too; a high score there is a
generalization claim ("this parcel's behavioral footprint resembles the
confirmed-non-occupied cases"), not a verified finding. No ground truth
exists to check that generalization against.

## 2. The model is a real but weak signal, not a detector

On held-out data: ROC-AUC 0.717, PR-AUC 0.098 against a 0.041 no-skill
baseline (~2.4x lift) for the gradient boosting model (6-feature set, post
Stage-4-pivot — see `docs/fraud_model_pivot.md`). Concretely: at the top
5%-by-score threshold used for the revenue-at-risk rollup, only 1,784 of the
9,197 known entity-owned parcels (19%) are captured — even though
entity-ownership is exactly what the model was trained to predict. Read
results as "meaningfully better than random," not "finds most fraud."

## 3. The risk threshold is a percentile, not a calibrated probability

Parcels are flagged as "high risk" by being in the top 5% of predicted
scores (`RISK_PERCENTILE = 0.95` in `scripts/train_fraud_model.py`), not by
crossing a fixed probability like 0.5. With a 4.1% base rate, `predict_proba`
output isn't a calibrated real-world probability — a fixed 0.5 cutoff would
flag almost nothing. The percentile threshold is a defensible relative
claim ("riskiest 5%"), not an absolute one ("50% likely to be fraudulent").

## 4. Revenue-at-risk is an order-of-magnitude approximation

`(ownerLandHSValue + ownerImprovementHSValue) × COMBINED_TAX_RATE`, where
`COMBINED_TAX_RATE = 1.301%` is the sum of Travis County's FY2026 adopted
rate ($0.3758/$100) and Austin ISD's FY2026 rate ($0.9252/$100). This
simplifies in two ways: (a) it covers only two of several overlapping taxing
jurisdictions — City of Austin, Austin Community College, and other special
districts are excluded, so it understates a typical Austin property's full
combined rate; and (b) it applies a flat rate to the full HS-classified
value rather than modeling Texas's actual exemption mechanics (flat/percentage
reductions with statutory caps). Treat the resulting dollar figure as
order-of-magnitude, not a precise exemption calculation.

## 5. STR/Airbnb density was tested and removed — not part of this model

Earlier versions of this model included `airbnb_rate`, `str_permit_rate`,
and `registration_gap` (hex-level STR/Airbnb signals carried over from the
Stage 1–3 POC). They were removed after EDA and an ablation test found no
incremental predictive value at the parcel level: raw correlation with the
proxy label ≈ 0.001, a non-monotonic zero/nonzero SHAP dependence pattern
with no dose-response, and no change in ROC-AUC/PR-AUC when the three
features were dropped from the model entirely. Full evidence trail and
rationale: `docs/fraud_model_pivot.md`. `airbnb_rate`/`str_permit_rate`/
`registration_gap` still exist as columns in `data/products/parcel_features.csv`
for provenance/EDA purposes — they are simply not selected as model inputs
by `scripts/train_fraud_model.py`.

## 6. Geometry-null exclusion carries over from Stage 2

The same ~13–14% of parcels excluded from the POC hex analysis for missing
or unparseable geometry are excluded here too (no `hex_id` assignment is
possible without a location). The model universe is parcels with usable
geometry, not all Travis County homestead parcels.

## 7. SHAP sign for `mailing_ne_situs`/`out_of_state_owner` cannot be trusted — use raw correlation for direction instead

Both features have a real, sensible, positive raw relationship with the
label (`mailing_ne_situs`: 3.9% label rate at flag=0 vs. 8.75% at flag=1;
`out_of_state_owner`: ~3.8–4.0% vs. ~10–11.7%; consistent across every
check run against this data). But SHAP's *sign* for these two features is
inverted relative to that true relationship, and the inversion doesn't
resolve cleanly: with the default `tree_path_dependent` attribution, both
features show flag=1 (the actual red flag) getting a *negative* mean SHAP
contribution and flag=0 a *positive* one — backwards. Switching to
`feature_perturbation="interventional"` (the standard fix for correlated
predictors) fixed `out_of_state_owner`'s sign but made `mailing_ne_situs`'s
*more* inverted, not less (mean SHAP dropped from −0.25 to −1.36 at flag=1).
Two attribution methods disagreeing rather than converging is evidence of a
genuine instability — most likely driven by the 0.346 correlation between
these two features — not a bug with one clean fix.

**Practical rule:** do not state SHAP *direction* for `mailing_ne_situs` or
`out_of_state_owner` in any writeup. SHAP *magnitude* is still fine to cite
for these two (they clearly matter a lot to the model — see item 8's global
ranking). For direction, cite the raw label-rate/lift numbers above instead,
which are stable across every check performed. The other four features
(`land_size_sqft`, `imprvMainArea`, `imprvClass`, `imprvCondition`) did not
show this pathology in the checks run this session and can be described
with SHAP sign normally — though this has not been exhaustively verified
the way `mailing_ne_situs`/`out_of_state_owner` have been.

## 8. Current global SHAP importance ranking (6-feature model)

By mean |SHAP| on the retrained model: `land_size_sqft` (1.38),
`mailing_ne_situs` (1.36), `imprvClass` (0.20), `imprvCondition` (0.14),
`out_of_state_owner` (0.13). `land_size_sqft` and `mailing_ne_situs` now
dominate by an order of magnitude over the other four — a different
ranking than the retired 10-feature model, where `imprvMainArea` and
`airbnb_rate` led. See item 7 for why `mailing_ne_situs`'s ranking here
should be read as "clearly influential" but not "influential in this
direction."

## 9. Near-zero univariate correlation does not guarantee a feature is safe to drop

`imprvActualYearBuilt` was dropped from the model on the same basis
`airbnb_rate` was — a correlation with the label indistinguishable from
zero (−0.0086) and a non-monotonic decile dose-response. But unlike
`airbnb_rate` (which cost nothing when removed via ablation, confirming it
was pure noise), removing `imprvActualYearBuilt` cost real performance:
ROC-AUC dropped from 0.728 (7-feature, STR removed) to 0.717, and PR-AUC
from 0.102 to 0.098. Likely explanation: unlike a correlation check, an
ablation test can capture value a feature contributes only through
*interaction* with other features (e.g. "older AND large" as a joint
pattern), which a univariate check cannot see. The decision to drop it was
made anyway — the model still performs well above the no-skill baseline —
but the lesson generalizes: EDA (univariate correlation/dose-response) and
ablation (does removing it change performance) catch different failure
modes and neither is sufficient alone. Do both before dropping a feature
based on either one in isolation.
