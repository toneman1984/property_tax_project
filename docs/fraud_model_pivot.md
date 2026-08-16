# Stage 4 Pivot: From STR/Airbnb Signal to Homestead Fraud Revenue Estimation

**Status: decision made, implementation not yet started.** This document
records where the project stood, the evidence that drove this decision, and
what it means going forward. It is a rationale record, not an implementation
plan — the implementation plan follows separately.

---

## Where the Project Stands

**POC (Stages 1–3): complete.** A hex-level (H3 resolution 8) spatial
correlation analysis across 246 hex cells found `homestead_rate` vs.
`airbnb_rate` at r = −0.143 (p = 0.025) — a statistically significant but
weak negative correlation, in the direction the fraud hypothesis predicted.
County-wide: 7,082 active Airbnb entire-home listings against 987 Type 2 STR
permits. Full detail in `archive/pitch.md` (the original POC pitch, archived
during the Stage 4 pivot — see "What Changes Going Forward" below) and
`docs/project_plan.md`.

**Stage 4 (parcel-level ML model): Steps 1–3 of 5 complete.** Owner-level
data (name, entity type, mailing address, appraised value — present in the
raw TCAD export but never loaded into the working database) was added to
build a parcel-level model. `scripts/train_fraud_model.py` trains a
gradient boosting classifier to predict a legally-grounded proxy label
(`has_homestead AND is_entity_owner`) from a feature set that deliberately
excludes ownership-entity signals, so the model can generalize to
individually-owned parcels the deterministic rule can never catch. Current
model: 10 features, ROC-AUC 0.730 / PR-AUC 0.103 against a 0.041 no-skill
baseline.

---

## How We Got Here

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

## Why We're Pivoting

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

## What This Does *Not* Invalidate

The POC (Stages 1–3) remains a valid, complete piece of work on its own
terms — it answered a narrower question (does neighborhood-level STR
density correlate with homestead exemption rates?) under the data
constraints that existed at the time, and found a weak but statistically
significant result in the predicted direction. That result isn't being
retracted. It's being deprioritized as the project's centerpiece in favor
of a stronger, more direct signal that wasn't available until Stage 4's
owner-data ingestion made it possible.

---

## What Changes Going Forward

- **Modeling:** `train_fraud_model.py`'s feature set drops `airbnb_rate`,
  `str_permit_rate`, and `registration_gap`; the model, full-universe
  scoring, SHAP explanations, and revenue-at-risk rollup all need to be
  regenerated on the reduced 7-feature set.
- **Narrative:** the project's headline result shifts from the POC's
  correlation coefficient to Stage 4's estimated revenue-at-risk figure.
  The original `docs/pitch.md` (STR/Airbnb-density-centered) has been
  archived to `archive/pitch.md`, preserving its history; a new pitch
  reflecting the Stage 4 finding is still pending a follow-up pass.
  `docs/project_plan.md` needs no edit — its Stage 0-3 scope and findings
  remain accurate as written (see "What This Does Not Invalidate" above).
- **Assumptions ledger:** `docs/fraud_model_assumptions.md`'s existing
  entries on STR density (item 5) and SHAP prevalence dilution (item 7)
  will need revision once STR features are removed from the model — item 7
  in particular was written to explain why STR/mailing features looked
  underweighted, an issue that mostly disappears once STR features are
  dropped.
- **Verification:** spot-checking (per the plan's verification step) should
  continue against the retrained model — the individually-owned parcels it
  flags will likely look different once STR-driven cases (58% of the prior
  flagged pool) are no longer being flagged.

---

## Next Step

An implementation plan for the retrain/rescore/re-document work described
above. Not started yet.
