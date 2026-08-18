# Main Parcel Record: Source Structure and Extraction Status

Companion to `owner_data_structure.md`, same purpose: a complete, standalone
record of what the raw source actually contains and what
`scripts/load_protax_to_sqlite.py` currently extracts from it, written
before any further extraction work so nothing gets lost between sessions.
Intended, longer-term, to anchor code comments back to a documented
structure — see "Extraction plan" at the end.

## Source of origination

Same file as `owner_data_structure.md`:
`data/sources/Travis_protaxExport_20250720.json`, one JSON object per
parcel (~486,859 records). This document covers everything on that
top-level record *except* `owners[]`, which has its own document.

## Structure overview

```
parcel record (pID)
├── (24 scalar fields)              propType, geometry, inactive, pYear, ...  [LOADED — properties]
├── propertyLegalDescription[]      always length 1                          [LOADED — property_legal_description]
├── propertyIdentification[]        always length 1                          [LOADED — property_identification]
├── propertyCharacteristics[]       always length 1                          [LOADED — property_characteristics]
├── propertyProfile[]               always length 1                          [LOADED — property_profile, partially]
├── situses[]                       usually 1, sometimes more                [LOADED — property_situs, missing 1 field]
├── owners[]                        see owner_data_structure.md              [LOADED — property_owner, lossy]
│
├── appeals[]                       ARB protest/appeal records                [NOT LOADED]
├── deeds[]                         recorded ownership transfers              [NOT LOADED]
├── events[]                        internal admin/system event log          [NOT LOADED]
├── inspections[]                   field inspection history                 [NOT LOADED]
├── links[]                         related-parcel links                     [NOT LOADED]
├── notes[]                         free-text case notes                     [NOT LOADED]
├── permits[]                       building permit history                  [NOT LOADED]
├── sales[]                         sale price/transaction history           [NOT LOADED]
├── smartgroups[]                   multi-parcel homestead/limitation groups [NOT LOADED]
├── tags[]                          administrative flags/labels              [NOT LOADED]
├── taxingunits[]                   property-wide taxing-unit associations   [NOT LOADED]
└── valuations{}                    deep nested cost/improvement detail tree [NOT LOADED, deliberately]
```

## Currently loaded tables — fidelity check

Checked by comparing the raw keys on one full example record (pID 100008)
and a 500-record key-union sample against each table's fixed column list in
`load_protax_to_sqlite.py`.

| Table | Raw source | Fidelity |
|---|---|---|
| `properties` | top-level scalar fields | **Full.** All 24 non-array top-level fields have a matching column. Uses `INSERT OR REPLACE` keyed on `pID`; confirmed no duplicate-pID collapse is happening (raw array length matches current row count exactly). |
| `property_legal_description` | `propertyLegalDescription[]` | **Full.** Raw object's 9 fields (+ `pID`) match the table's 9 columns exactly. |
| `property_identification` | `propertyIdentification[]` | **Full.** Raw object's 5 fields (+ `pID`) match the table's 5 columns exactly. |
| `property_characteristics` | `propertyCharacteristics[]` | **Full.** Raw object's 20 fields (+ `pID`) match the table's 20 columns exactly. |
| `property_profile` | `propertyProfile[]` | **Full, but mostly unindexed.** Raw object has ~73 fields (+ `pID`); only 22 get real columns. The other ~51 (`landSizeSqft`, `landTotalAcres`, `imprvQuality`, `imprvStyle`, `imprvStories`, `imprvTotalArea`, `stateCd`, `schoolTaxingUnitID`, `mineralStateCd`, land/improvement classification and pricing-model fields, etc.) are captured but only inside the unparsed `extra_fields` JSON TEXT column — present in the database, not usable in a query without parsing that blob first. |
| `property_situs` | `situses[]` | **Missing one field.** Raw object has `international` (seen alongside the 11 other situs fields); the table has no matching column. Everything else matches. |
| `property_owner` | `owners[]` | **Lossy** — see `owner_data_structure.md`, not repeated here. |

## Not yet loaded — the 12 untouched top-level arrays

None of these were referenced anywhere in the codebase as of 2026-08-17
(now built, or deferred, per the "Extraction plan" section below — this
section is kept as the original discovery record). Population rates below
were originally estimated from a 500-record sample; **superseded
2026-08-17 by a full recursive scan of all 486,859 records**
(`scripts/inventory_scan_full.py` → `full_inventory_scan.md`/`.json`) —
confirmed figures are noted alongside each original estimate, and several
moved substantially (e.g. `deeds` 98%→86.5%, `tags` 95%→81.1%, `links`
14%→23.8%) — a concrete illustration of why the full scan was worth doing
rather than trusting the sample. Field lists below are still the
500-record key-union, except `valuations`, described structurally only
(see note at the end).

### `deeds[]` — 98% populated (490/500) — **confirmed 86.5% (421,336/486,859) on the full population** — recorded ownership transfers

17 fields: `deedID`, `deedType`, `deedDt`, `deedRecordedDt`, `fileDt`,
`book`, `page`, `volume`, `instrumentNum`, `consideration`, `sellerLine`,
`buyerLine`, `exemptionNotes`, `exemptionReset`, `comment`, `pID`,
`properties` (a string-encoded list, e.g. `"[100008]"` — possibly links a
deed to more than one parcel for multi-parcel transfers).

Directly relevant to fraud detection: actual grantor/grantee (`sellerLine`/
`buyerLine`) and transfer date per recorded deed. This is the most direct
raw signal available for "was this property actually sold" — more
authoritative than inferring non-occupancy from owner/mailing proxies.

### `sales[]` — 51% populated (255/500) — **confirmed 35.1% (171,090/486,859)** — sale price/transaction detail

74 fields — richer than `deeds`, includes actual dollar amounts and
financing detail: `saleID`, `deedID` (FK to `deeds`), `saleDt`, `saleType`,
`salePrice`, `salePriceAdjusted`, `saleQualify`, `saleAdjustment*` (type,
reason, amount, pct), `confidentialSale`, `confidentialCode`,
`sellerLine`, `buyerLine`, `sourceOfSale`, `multiProperty`, `notes`,
finance detail (`financeCode`, `financeLoan1/2AmtDown`,
`financeLoan1/2AmtFinanced`, `financeLoan1/2InterestRate`,
`financeLoan1/2FinanceYears`), and a large block of **frozen
characteristics at time of sale** (`charImp*`, `charLand*`,
`charLocation*`) — a snapshot of the property's profile as it existed when
sold, independent of its current profile. Also carries reporting-suppression
flags (`reportSupress*`) suggesting some sales are excluded from official
ratio studies — worth understanding before treating `salePrice` as always
reliable.

### `permits[]` — 85% populated (426/500) — **confirmed 69.3% (337,406/486,859)** — building permit history

49 fields: permit identity/status (`buildingPermitID`, `permitNumber`,
`permitType`, `subType`, `permitStatus`, `cadStatus`,
`permitPropertyCategory`, `active`), dates (`issueDate`, `limitDate`,
`permitDateCompleted`, `dateWorked`, `pcDateComplete`), project detail
(`estimateOfValue`, `projectNotes`, `floors`, `units`, `bedrooms`,
`bathrooms`, `squareFootArea`), builder info (`builder`,
`builderPlanNumber`, `builderPhoneNumber`), situs at time of permit
(`situsPrefix`, `situsStreet`, `situsStreetNum`, `situsStreetSuffix`,
`situsUnitType`, `situsUnitNumber`, `city`, `block`, `lot`, `plat`,
`asCode`), and required-inspection flags. `projectNotes` is free text (the
one example pulled read *"Exterior Remodel to replace Patio Canvas Roofing
with Metal Roofing for existing Restaurant"* — worth checking how often
notes like this reveal commercial/STR-style use on a residentially
homesteaded parcel).

### `appeals[]` — 61% populated (306/500) — **confirmed 42.8% (208,138/486,859)** — ARB protest/appeal records

125 fields — by far the largest of these structures. Broad categories:
appeal identity/status (`appealID`, `appealType`, `appealStatus`,
`appealedByID`, `appealedByAgentID` — links to the `agents` structure in
`owner_data_structure.md`, `appealedByType`), three parallel value
snapshots — **initial**, **notice**, and **final** — each with the same
land/improvement/market/HS-NHS breakdown (`initial/notice/finalLandValue`,
`...ImprovementValue`, `...MarketValue`, `...AppraisedValue`, etc.), formal
and informal hearing detail (dates, times, appraiser comments, board
motions/seconds/votes), and due-diligence tracking fields
(`dueDiligenceTaxesPaid`, `dueDiligenceEvidence*`). Lower fraud-detection
priority than `deeds`/`sales` at first glance, but the appealed-by-agent
link and value-adjustment history could matter for identifying aggressively
managed (investor-style) parcels.

### `taxingunits[]` — 100% populated (500/500) — **confirmed 100% (486,859/486,859)** — property-wide taxing unit shares

14 fields: `taxingUnitID`, `taxingUnitName`, `taxingUnitNum`,
`taxingUnitType`, `taxingUnitCode`, `jurisdictionPct`, and per-category
segment percentages (`segImprovementHSPct`, `segImprovementNHSPct`,
`segLandHSPct`, `segLandNHSPct`, `segLandSUPct`, `segLandSUMktPct`,
`segBppPct`). This is the property-wide counterpart to the owner-level
`ownerTaxable[]` structure documented in `owner_data_structure.md` — that
one carries the dollar values and tax rates per taxing unit per *owner*;
this one carries jurisdiction *percentage* splits per taxing unit for the
*property* as a whole. Always populated (every parcel falls under at least
a county and a school district).

### `inspections[]` — 95% populated (477/500) — **confirmed 93.0% (452,595/486,859)** — field inspection history

10 fields: `inspectionID`, `inspectionActiveDt`, `inspectionReason`,
`inspectionAppraiser`, `inspectionNotes`, `inspectionFieldNotes`,
`inspectionCompleted`, `inspectionCompletedBy`, `inspectionCompleteDt`,
`pID`. `property_profile.fieldInspectionDt`/`fieldInspectionSource`
(already loaded) appears to be a flattened summary of only the most recent
entry here — this array is the full history.

### `events[]` — 64% populated (320/500) — **confirmed 63.2% (307,727/486,859)** — internal admin/system log

13 fields: `eventID`, `eventType`, `eventDescription`, `eventData` (a
JSON-string-encoded sub-object, e.g. `{"Ref1": ..., "UserName": ...,
"EventDate": ..., "LegacyEventID": ...}`), `formID`, `createdBy`,
`createDt`, `updatedBy`, `updateDt`, `inactive`, `inactiveDt`,
`inactiveBy`, `pID`. Looks like a general-purpose audit trail (the sampled
example recorded a parcel merge). Likely lower analytical priority — more
useful for understanding data provenance/history of a specific parcel than
as a fraud signal directly.

### `tags[]` — 95% populated (477/500) — **confirmed 81.1% (394,789/486,859)** — administrative flags/labels

7 fields: `tagID`, `tag` (free-text label, e.g. `"INTERIM USE"` in the
sampled example), `tagYear`, `pYear`, `notification`, `Codefied`, `pID`.
Worth a frequency count of distinct `tag` values early — if TCAD uses a
constrained vocabulary here, some tag values could be a very direct,
already-curated anomaly/review-flag signal rather than something we'd need
to infer.

### `smartgroups[]` — 1% populated (5/500) — **confirmed 1.2% (5,708/486,859)** — multi-parcel homestead/limitation groups

15 fields: `groupID`, `groupType` (`"HS"` in the sampled example),
`groupName`, `groupYr`, `groupComment`, `limitationAmount`,
`limitationFirstYear`, `applicationNumber`, `applicationCounty`,
`applicationProjectName`, `applicationApplicantName`,
`applicationFirstYearQualifying`, `applicationAgreementDate`, `properties`
(string-encoded list of pIDs in the group, e.g. `"[100043, 100051]"`),
`pID`. Rare, but the one example found is explicitly a homestead
limitation group spanning two parcels under one `pID` designated as
"MAIN PID" — i.e. TCAD's own mechanism for legitimate multi-parcel
homestead claims (e.g. a main house and a guest structure on a separate
parcel, both counted under one owner-occupancy claim). High signal value
despite low frequency: this is a case where "homestead claimed" needs to be
evaluated at the group level, not the individual parcel level, to avoid a
false positive.

### `links[]` — 14% populated (71/500) — **confirmed 23.8% (115,724/486,859)** — related-parcel links

3 fields only: `linkID`, `linkedPID`, `pID`. Minimal information (no
link-type/reason field observed) — essentially just "this pID relates to
that pID" with no explanation of why. Comparable in spirit to EARS'
`AJR09 Parent Account Number` concept (`ears_state_reference.md`), but
without a stated reason field, its exact meaning would need to be
cross-checked against parcels known to be economic units (e.g. house +
adjacent vacant lot).

### `notes[]` — 99% populated (493/500) — **confirmed 92.4% (449,771/486,859)** — free-text case notes

4 fields only: `noteID`, `content` (free text, e.g. `"%, DETAILS  //
--- //"` in the sampled example — often terse/coded, not necessarily
prose), `isPrivate`, `pID`. Nearly universal but unstructured; would need
text mining rather than direct field use.

### `valuations{}` — 100% populated (500/500) — deep cost/improvement detail tree

Not a flat array like the others — a nested object,
`valuations.details.cost-local.improvements[]`, itself deeply structured
(the one example pulled showed per-improvement fields like `imprvType`,
`stateCd`, `class`, `quality`, `stories`, `condition`, `deprec`,
`economicAdj`, `functionalAdj`, `physicalAdj`, `pricingModel`, and more,
continuing beyond what was captured in the sample dump). This is the same
structure the original Stage 4 plan (`docs/fraud_model_plan.md`) explicitly
decided to skip when building `property_owner` — *"Skip the deeply-nested
valuations.details.cost-local.* tree entirely — ownerValue already has the
summary figures needed"* — and that reasoning still holds for a first pass
here. Noted for completeness, not recommended as a near-term extraction
target; would need its own dedicated structural exploration given its
depth.

## Extraction plan

**Status: built and verified, 2026-08-17** (superseding the priority
ordering originally sketched here — turned out grouping everything into
one loader pass made prioritization moot; see
`C:\Users\rwrcr\.claude\plans\velvet-wishing-grove.md` for the full design
rationale). All 10 flat arrays plus `smartgroups[]` were built using
columns generated from the full-population inventory scan
(`scripts/schema_codegen.py` → `scripts/table_schemas.py`) rather than
hand-picked. Originally in their own script (`load_ancillary_data_to_sqlite.py`,
kept standalone/out of `main.py` while their shape was still being
verified); merged into `scripts/load_protax_to_sqlite.py` later the same
day once verification confirmed they're just as settled as the original
6 tables — one streaming pass now builds everything:

| Table | Rows (full population) |
|---|---|
| `deeds` | 2,178,541 |
| `sales` | 278,063 |
| `permits` | 1,114,451 |
| `appeals` | 208,263 |
| `taxingunits` | 3,084,561 |
| `inspections` | 646,554 |
| `events` | 623,461 |
| `tags` | 783,242 |
| `links` | 153,617 |
| `notes` | 1,276,315 |
| `smartgroups` | 5,771 |

Every row count matches the full inventory scan's own array-length tallies
exactly — cross-checked, not just asserted.

`valuations{}` was also built, but as a single JSON blob column
(`property_valuations(pID, valuations_json)`, one row per parcel, 486,859
rows) rather than normalized — matches the standing decision from the
original Stage 4 plan to not flatten that tree's depth; nothing is lost,
it's just not queryable as real columns yet.

**Resolved 2026-08-17 (later the same day):** the `property_situs`/
`property_profile` gaps noted above and in the fidelity table were fixed
after all, once `load_protax_to_sqlite.py` itself was converted to the same
schema-driven pattern as everything else. `property_situs` now includes
`international`; `property_profile` went from 22 real columns to 75. See
`docs/project_plan.md`'s Stage 0/1 section for the current state — the
"untouched original loader" framing above is no longer accurate, kept here
only as the historical record of when the gap was first found.

**Still deferred:**
- Normalizing `valuations{}` beyond the blob-column level.
- Flattening string-encoded-JSON sub-fields (`events.eventData`,
  `appeals.claimantEvidence`) into their own columns/tables — left as raw
  TEXT (full fidelity preserved, just not parsed open).
