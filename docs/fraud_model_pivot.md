# Project Pivot History

This document records the project's major methodology pivots in order: the
evidence that drove each decision, and what it means going forward. It is a
rationale record, not an implementation plan.

**Current status:** Pivot 1 (below) is fully implemented and committed.
Pivot 2 (below) is a decision in progress — the project's overall shape is
changing again, more fundamentally than Pivot 1 did, and implementation has
not started.

---

## Pivot 1 (2026-08-16): STR/Airbnb Signal → Owner-Occupancy Signal

**Status: implemented.** `train_fraud_model.py` was retrained on the
6-feature set described below, wired into `main.py`, and committed. See
Pivot 2 below for why this model is now itself being deprioritized.

### Where the Project Stood

**POC (Stages 1–3): complete.** A hex-level (H3 resolution 8) spatial
correlation analysis across 246 hex cells found `homestead_rate` vs.
`airbnb_rate` at r = −0.143 (p = 0.025) — a statistically significant but
weak negative correlation, in the direction the fraud hypothesis predicted.
County-wide: 7,082 active Airbnb entire-home listings against 987 Type 2 STR
permits. Full detail in `archive/pitch.md` (the original POC pitch, archived
during the Stage 4 pivot — see "What Changes Going Forward" below) and
`docs/project_plan.md`.

**Stage 4 (parcel-level ML model): Steps 1–3 of 5 complete at the time this
pivot started.** Owner-level data (name, entity type, mailing address,
appraised value — present in the raw TCAD export but never loaded into the
working database) was added to build a parcel-level model.
`scripts/train_fraud_model.py` trains a gradient boosting classifier to
predict a legally-grounded proxy label (`has_homestead AND
is_entity_owner`) from a feature set that deliberately excludes
ownership-entity signals, so the model can generalize to individually-owned
parcels the deterministic rule can never catch. Model at the time: 10
features, ROC-AUC 0.730 / PR-AUC 0.103 against a 0.041 no-skill baseline.

---

### How We Got Here

**The POC's premise.** At the time of the original POC, STR/Airbnb density
was adopted as the fraud proxy because it was the best available signal
under real data constraints: City of Austin STR permit addresses are
obfuscated to block level, and no owner-occupancy or long-term-rental data
was accessible. Airbnb listing density was a legitimate, defensible choice
given what was on hand — but it was always a stand-in for the real thing
(non-occupancy), not the real thing itself.

**Stage 4 changed what was on hand.** Loading the owner data unlocked
direct, parcel-level occupancy-adjacent signals for the first time: whether
the owner's mailing address matches the property's situs address, whether
the owner is out of state, and the property's own structural/value profile
— none of which depend on Airbnb or STR data at all.

**Spot-checking surfaced a pattern the STR hypothesis didn't predict.** The
first batch of manual spot-checks (the five highest-scoring
individually-owned flagged parcels, per the plan's verification step) found
a coherent cluster: luxury homes ($2.9M–$8.4M, 6,882–9,471 sqft) with
`airbnb_rate`/`str_permit_rate` near zero, but out-of-state mailing
addresses (KY, NV, UT, NJ) mismatching the situs address in 4 of 5 cases.
This is what first prompted the idea of de-emphasizing the STR narrative —
the model's strongest individual cases weren't STR-related at all.

**A second, stratified batch clarified — then complicated — the picture.**
Sampling across SHAP "dominant driver" categories (not just top overall
score) found that, across the full pool of 9,491 flagged individually-owned
parcels, `airbnb_rate` is actually the single largest SHAP driver for 58%
of them — the luxury/out-of-state cluster was a small outlier group at the
extreme top of the distribution, not representative of the flagged
population as a whole.

**But checking the direction of that relationship changed the conclusion
entirely.** `airbnb_rate`'s SHAP contribution turned out not to track "more
STR activity → more risk." It's a step function: `airbnb_rate == 0` exactly
→ mean SHAP ≈ +1.41 (strong positive push); any nonzero value, however
large → mean SHAP ≈ −0.085 (flat, no further gradation by magnitude). The
raw correlation between `airbnb_rate` and the proxy label across all
226,676 homestead parcels is 0.001 — statistically indistinguishable from
zero, and entity-owned rate barely differs between zero-Airbnb hexes (4.24%)
and nonzero-Airbnb hexes (3.90%), if anything in the opposite direction from
the original hypothesis.

**An ablation test confirmed the feature isn't pulling real weight.**
Refitting the model without `airbnb_rate`/`str_permit_rate`/
`registration_gap`:

| Feature set | # features | ROC-AUC | PR-AUC |
|---|---|---|---|
| Full (original) | 10 | 0.730 | 0.103 |
| Owner/mailing/structural only (no STR) | 7 | 0.728 | 0.102 |
| STR/Airbnb features only | 3 | 0.602 | 0.059 |

Removing the STR features costs essentially nothing (a difference within
noise). The STR features do carry weak standalone signal in isolation
(0.602 ROC-AUC, better than random), but none of it is incremental once
owner/mailing/structural features are already in the model — whatever those
three features capture on their own is redundant with what the owner and
structural data already explain.

---

### Why We're Pivoting

Three independent pieces of evidence — near-zero raw correlation, a
non-monotonic zero/nonzero SHAP pattern with no dose-response relationship,
and an ablation showing zero incremental predictive value — point the same
direction: at the parcel level, `airbnb_rate` is not functioning as a real
fraud signal in this model. Continuing to foreground STR/Airbnb density as
the project's central signal after specifically testing it and finding it
unsupported would not be honest to the evidence.

More fundamentally: the STR/Airbnb angle was never the actual research
question. It was the best available proxy for the real one, adopted under
the specific data constraints of the original POC. The real object of
interest has always been **estimating revenue lost to improperly claimed
homestead exemptions.** Stage 4's owner-level data gives a more direct route
to that question than the STR proxy ever did, and now that both are in
hand and can be compared directly, the evidence says the owner/occupancy
signals — not STR density — are carrying the model's real predictive power.

This is a genuine pivot, not an incremental adjustment: the project's
headline moves from "Airbnb density correlates with lower homestead rates"
(a neighborhood-level association) to "estimated dollar revenue at risk
from homestead exemption fraud" (a parcel-level, owner-occupancy-driven
estimate) as the central deliverable.

---

### What This Does *Not* Invalidate

The POC (Stages 1–3) remains a valid, complete piece of work on its own
terms — it answered a narrower question (does neighborhood-level STR
density correlate with homestead exemption rates?) under the data
constraints that existed at the time, and found a weak but statistically
significant result in the predicted direction. That result isn't being
retracted. It's being deprioritized as the project's centerpiece in favor
of a stronger, more direct signal that wasn't available until Stage 4's
owner-data ingestion made it possible.

---

### What Changed (implemented)

- **Modeling:** `train_fraud_model.py` retrained on 6 features (also
  dropped `imprvActualYearBuilt` after EDA found near-zero correlation
  with the label, on top of the 3 STR features — see
  `docs/fraud_model_assumptions.md` item 9). Full-universe scoring, SHAP,
  and revenue-at-risk rollup all regenerated: ROC-AUC 0.717 / PR-AUC 0.098,
  $357.4M estimated revenue at risk across 11,395 flagged parcels.
- **Narrative:** `docs/pitch.md` archived to `archive/pitch.md`; a new
  pitch draft remained pending when Pivot 2 (below) started, and is now
  further deferred pending Pivot 2's outcome. `docs/project_plan.md`
  received no edit, as anticipated.
- **Assumptions ledger:** `docs/fraud_model_assumptions.md` expanded from
  7 to 9 items — item 5 rewritten as a historical note, item 7 rewritten
  entirely around a SHAP sign-instability finding (see Pivot 2 below) that
  turned out to be more consequential than the dilution issue it
  originally described.
- **Verification:** stratified spot-checking of the retrained model's
  flagged population is what surfaced the SHAP sign instability that
  helped motivate Pivot 2.

---

## Pivot 2 (2026-08-16): ML-Centered Stage 4 → EDA-First Descriptive Estimation

**Status: decision made, implementation not started.**

### Where Stage 4 Stood

Pivot 1's retrained model (6 features, ROC-AUC 0.717/PR-AUC 0.098, $357.4M
headline revenue-at-risk figure) was complete, verified, wired into
`main.py`, and committed. But one loose end never resolved cleanly:
`mailing_ne_situs` and `out_of_state_owner` — real, meaningful features
with a genuine positive correlation to the label — showed a SHAP *sign*
inverted relative to that true relationship, and switching from
`tree_path_dependent` to `interventional` attribution didn't fix it
(it fixed `out_of_state_owner` but made `mailing_ne_situs` worse).
Two attribution methods disagreeing rather than converging pointed to a
real instability, not a bug with a clean fix — documented in
`docs/fraud_model_assumptions.md` item 7.

### What Changed

A pattern repeated across this project's history became hard to ignore:
`airbnb_rate` (Pivot 1), `imprvActualYearBuilt` (found during Pivot 1's own
EDA-first check), and now the SHAP sign instability — each time, a
feature or explanation method that looked reasonable didn't hold up under
closer scrutiny, and each problem was caught mostly by chance (an
odd-looking spot-check) rather than by systematic upfront investigation.
That eroded confidence in "build a model, understand the data as problems
surface" as the right sequence for this project.

The user made an explicit, larger call: **set aside the ambition to build
an ML model, for now** — not abandoned, deprioritized. Before committing to
any statistical methodology, do deep, comprehensive exploratory analysis of
the source TCAD data — not just the handful of fields used in Stage 4, but
a full re-exploration of what TCAD's tables actually contain, plus
potentially new datasets not yet considered. Establish basic summary
statistics and dollar estimates describing the full "universe" of the
research *before* deciding how to model anything.

### New Project Structure (going forward)

1. **Foundational descriptive layer.** Comprehensive EDA on TCAD source
   data (`properties`, `property_profile`, `property_characteristics`,
   `property_situs`, `property_legal_description`, `property_owner`, and
   potentially new datasets not yet pulled) — basic summary statistics,
   testing candidate fraud-signal hypotheses empirically, before any
   methodology commitment.
2. **Known-population dollar estimate.** The deterministic entity-owned-
   homestead case becomes the project's headline number — legally
   unambiguous, no proxy-label reasoning required — rather than an
   auxiliary comparison baseline as it was in Stage 4's
   `composite_red_flag_score`.
3. **Profile + statistical population expansion.** Characterize the known
   high-risk population's profile, then use unsupervised techniques —
   PCA (for dimensionality reduction/multicollinearity, likely needed once
   the full TCAD re-exploration surfaces many correlated fields), paired
   with either clustering or Mahalanobis-distance matching (PCA alone
   doesn't complete a similarity-matching task) — to find individually-
   owned parcels statistically similar to that profile, expanding the
   estimate. Mahalanobis-distance matching in particular is methodologically
   close to propensity-score matching from causal inference, a stronger
   portfolio fit than PCA alone given the user's stated interest in causal
   ML. Mixed continuous/categorical data from the full TCAD re-exploration
   will likely need FAMD or a Gower-distance-based approach rather than
   vanilla PCA — a decision for when Phase 1 shows the actual candidate
   feature set, not now.
4. **ML as a later, optional refinement layer**, sitting on top of 1–3
   once that foundation is solid — not the project's primary deliverable.
5. **MLS long-term/short-term rental data — parallel, independent track,
   not started.** Actual rental listing data would identify non-occupancy
   from a completely different evidentiary axis than owner/mailing/
   structural proxies, expanding or corroborating the estimate
   independently whenever that data becomes accessible. This reinstates an
   idea from the original POC's deferred next step (see
   `archive/pitch.md`'s "Case for Investment" section) that got shelved
   when the STR-density proxy approach took over instead.

### What Gets Set Aside (not deleted)

- H3 hex-aggregation / STR-correlation POC (Stages 2–3:
  `aggregate_to_hex.py`, `visualize.py`, `hex_ratios.geojson` and related
  products) — explored, not currently the path.
- ML Stage 4 apparatus (`build_fraud_features.py`, `train_fraud_model.py`,
  `eda_fraud_features.py`, `stage4_preflight.py`, `stage4_output_test.py`,
  and the Stage 4 block in `main.py`) — explored, not currently the path;
  may resurface as the "ML refinement layer" in a later phase (item 4
  above).

### What Stays Active

The SQL ingestion/database layer — `load_protax_to_sqlite.py`,
`load_owners_to_sqlite.py`, `scripts/utils.py`, the SQLite database itself
— is the substrate for the new Phase 1 EDA work and is not affected by
this pivot.

### What This Does *Not* Invalidate

Every finding from Pivot 1 remains true, just repositioned: the POC's
hex-level correlation, the STR-feature ablation results, the
`imprvActualYearBuilt` interaction lesson, and the SHAP sign-instability
finding are all still accurate and still inform what *not* to trust going
forward — including a reminder to re-test the owner/mailing signals in the
new EDA-first framework rather than assuming they're clean just because
they survived Pivot 1's scrutiny. The $357.4M ML-derived revenue-at-risk
figure isn't retracted, but it's no longer the project's headline number —
that will be the deterministic-population dollar estimate (item 2 above)
once computed, likely smaller in scope but more directly defensible.

### Next Step

Not yet started: Phase 1 — comprehensive EDA of TCAD source data, scoping
which existing tables/fields to dig into first and which additional
datasets to consider pulling.
