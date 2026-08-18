# Owner Data: Source Structure and Extraction Status

Full documentation of the `owners` nested structure in the raw TCAD export,
what's currently extracted into the database, and what a full-fidelity
extraction requires. Written before building anything, so the record exists
independent of what gets implemented first.

## Source of origination

Every top-level parcel record in
`data/sources/Travis_protaxExport_20250720.json` (the raw ~29GB TCAD export,
one JSON object per parcel, ~486,859 records total) carries an `owners`
array. This is the sole source for all owner-related data in the project —
nothing about ownership is derived from any other file. It has never been
fully extracted; only a small, flattened subset has been loaded to date (see
"Current local extraction state" below).

This is a different thing from the Texas Comptroller's EARS format discussed
in `ears_state_reference.md` — EARS is the standardized state-facing
submission format; this document describes the actual raw structure TCAD's
own export uses locally, which is vendor/TCAD-specific and undocumented
publicly (see `ears_state_reference.md`'s note on the ProdigyCAD portal).
Where a raw field's real-world meaning was unclear from its name alone, the
EARS manual was used as a cross-reference — noted inline below.

## Structure overview

```
parcel record (pID)
└── owners[]                     one entry per owner on the parcel
    ├── (34 scalar fields)       name, mailing address, ownerPct, ownerID, ...
    ├── exemptions[]             owner-level exemptions (structure not yet explored)
    ├── ownerValue[]             ALWAYS exactly 1 entry (confirmed across all 486,859 parcels)
    ├── agents[]                 0 to many; tax-representation-firm relationships
    └── ownerTaxable[]           one entry per taxing unit (county/school/city/etc.)
        └── exemptions[]         per-taxing-unit exemptions (structure not yet explored)
```

**Multiplicity, confirmed against the full population** — superseded
2026-08-17 by a proper recursive full-file inventory scan
(`scripts/inventory_scan_full.py`, 486,859/486,859 records, 9.0 minutes
after fixing a slow ijson backend — see `full_inventory_scan.md`/`.json`
for the complete field-by-field results):
- `owners[]` length: `{1: 486,829, 2: 15, 3: 3, 4: 2, 6: 10}` — 30 parcels
  (0.006%) have more than one owner. (Matches the earlier shallow full-scan
  exactly.)
- `ownerValue[]` length: always exactly 1, no exceptions (486,936 owner
  records checked).
- `agents[]`: **39.4%** of owners have at least one entry (191,920 of
  486,936) — common, not an edge case, but notably lower than the earlier
  20,000-record sample's 56% estimate. Length distribution: mostly 0 or 1
  (173,061 owners with exactly 1), up to 6 for a handful of owners.
- `ownerTaxable[]`: **100%** of owners have at least one entry (every owner
  falls under at least one taxing unit, as expected). Length distribution
  peaks at 6 (341,004 owners) and 7 (96,038), consistent with the
  county+school+city+special-district pattern seen in the pID 100008
  example below.

## Current local extraction state

`scripts/load_owners_to_sqlite.py` builds `property_owner` — **lossy** on
every axis above:
- Keeps only the highest-`ownerPct` owner per parcel (ties: first in list),
  discarding the other 30 parcels' extra owners entirely.
- Keeps only `ownerValue[0]` (harmless in practice since it's always length
  1, but not by design — the code doesn't check).
- Does not touch `agents` or `ownerTaxable` at all — not loaded, not
  referenced anywhere in the codebase.
- Of the owner's ~34 scalar fields, only 8 are kept (`name`, `firstName`,
  `lastName`, `addrCity`, `addrState`, `addrZip`, `addrDeliveryLine`,
  `ownerPct`), plus 6 of `ownerValue`'s ~35 fields.

## Full field inventory (from a real example record, pID 100008)

Field lists below are what was observed on one real, fully-populated
example record. Field *presence* (all keys exist on every owner object,
per the JSON schema) is confirmed by the earlier 3,000-record key-union
scan; field *population rate* (how often each is non-null) is not yet
checked and should be part of the eventual extraction script's own EDA
pass, not assumed from a single example.

### Owner scalar fields (34)

Identity/ownership: `ownerID`, `pAccountID`, `pID` (redundant — always
equals the parent parcel's `pID`, not a distinct concept), `ownerPct`,
`applyPctExemptions`, `referenceID`

Name: `name`, `nameSecondary`, `firstName`, `lastName`, `spouseFirstName`,
`spouseLastName`

Mailing address: `addrDeliveryLine`, `addrUnitDesignator`, `addrCity`,
`addrZip`, `addrState`, `addrCountry`, `addrFreeForm`, `addrFreeForm1`,
`addrFreeForm2`, `addrFreeForm3`, `addrInternational`

Address validation (CASS — USPS Coding Accuracy Support System):
`cassValidationDt`, `cassValidationBy`, `cassValidationService`,
`plus4Code`, `deliveryPoint`, `deliveryPointCheckDigit`, `carrierRoute`,
`autoCass`

Geocoding: `latitude`, `longitude` (both null in the example record — check
population rate before relying on these)

Other/unclear: `regTag`, `source` (both null in the example; purpose not
yet determined — check EARS manual's `AJR30 Owner ID Code` field
description or population rate before assuming meaning)

### `ownerValue[0]` fields (35) — the appraisal-cap value snapshot

Value breakdown: `ownerLandValue`, `ownerLandHSValue`, `ownerLandNHSValue`,
`ownerSULandMktValue`, `ownerSUValue`, `ownerImprovementValue`,
`ownerImprovementNHSValue`, `ownerImprovementHSValue`, `ownerMarketValue`,
`ownerAppraisedValue`, `ownerTaxLimitationValue`, `ownerNetAppraisedValue`

Homestead cap ("limitation") tracking — see `ears_state_reference.md`'s
AJR67 note for the legal basis (110%-of-prior-year cap):
`limitationBaseYear`, `limitationBaseYearOverride`,
`limitationBaseYearOverrideReason`, `limitationBaseYearDate`,
`limitationLastYearHSValue`, `limitationLastYearHSValueOverride`,
`limitationLastYearHSValueOverrideReason`, `limitationAllowedIncrease`,
`limitationNewValue`, `limitationNewValueOverride`,
`limitationNewValueOverrideReason`, `limitationMaxAllowedIncrease`

New-construction value: `ownerNewValue`, `ownerNewBppValue`,
`ownerNewImprovementValue`, `ownerNewImprovementHSValue`,
`ownerNewImprovementNHSValue`, `ownerNewLandValue`, `ownerNewLandHSValue`,
`ownerNewLandNHSValue`

Homestead percentage/group: `ownerHSLandPct`, `ownerHSImprovementPct`,
`hsGroupPct`, `hsGroupValue`

Key: `pAccountID`

### `agents[]` fields (18) — tax-representation relationships

`propertyAccountAgentID`, `agentID`, `companyName`, `contactName`,
`contactPhone`, `firstName`, `lastName`, `applicationDt`, `effectiveDt`,
`expirationDt`, `mailingsARB`, `mailingsCAD`, `mailingsTaxingUnit`,
`authorityProtest`, `authorityResolveTaxMatters`, `authorityConfidential`,
`authorityOther`, `pAccountID`

Each entry represents one agent-of-record relationship (e.g. a tax
consulting firm authorized to file protests). `effectiveDt`/`expirationDt`
mean an owner can have both current and historical agent relationships in
the same array — no separate "is this the active one" flag observed, so
"currently represented" would need to be derived by comparing
`expirationDt` (or its absence) against the current date.

### `ownerTaxable[]` fields (~50) — deferred, saved for later

**Not being extracted in this pass** per 2026-08-17 decision — noted here so
nothing is lost, to be picked up as a follow-on table later.

One entry per taxing unit the parcel falls under (county, school district,
city, and any special districts — e.g. the example parcel had 6, for
taxing unit IDs 1000, 1001, 1002, 1003, 1034, 1097). Structurally, this is
the raw-data equivalent of the EARS "AJR" record type (`ears_state_reference.md`) —
EARS explicitly defines "1 per account per category per taxing unit," and
this array's grain matches exactly.

Notable: this is the **first place actual per-taxing-unit tax rates and
dollar amounts appear** anywhere in the raw export
(`limitationTaxRate`, `limitationTaxAmt`, `taxableValue`) — everywhere else
in the codebase so far (including Stage 4's revenue-at-risk calculation)
had to approximate using a publicly-sourced combined rate constant instead
of a real per-parcel rate. This is the most direct lead toward a precise
(not approximated) dollar estimate once picked back up.

Fields observed: `pPropertyAccountTaxingUnitID`, `pAccountID`,
`taxingUnitID`, `taxingUnitPct`, `marketValue`, `improvementHSValue`,
`improvementNHSValue`, `landHSValue`, `landNHSValue`, `suLandMktValue`,
`suValue`, `suExclusionValue`, `appraisedValue`, `limitationValue`,
`netAppraisedValue`, `taxableValue`, `newValue`, `newBppValue`,
`newImprovementValue`, `newImprovementHSValue`, `newImprovementNHSValue`,
`newLandValue`, `newLandHSValue`, `newLandNHSValue`, `newValueTaxable`,
`suNonExempt`, `suExempt`, `taxIncrementPresent`,
`taxIncrementImprovementValue`, `taxIncrementLandValue`,
`taxIncrementZone`, `weedTaxableAcres`, `omittedImprovementHSValue`,
`omittedImprovementNHSValue`, `bppLateInterstateAllocationValue`,
`hsGroupPct`, `limitationNetAppraisedValue`, `limitationTaxableValue`,
`limitationTaxRate`, `limitationTaxAmt`, `limitationPresent`,
`limitationExemptionCode`, `limitationYr`, `limitationAmt`,
`limitationTransfer`, `limitationTransferDt`, `limitationPreviousTaxDue`,
`limitationPreviousTaxDueNoLimit`, `limitationTransferPct`, `exemptions[]`

### `exemptions` appears in three separate places — not yet reconciled

1. `property_profile.exemptions` (already loaded, TEXT, format unparsed —
   flagged in `00_overview.md`)
2. `owners[].exemptions` — an array (empty `[]` in the example record),
   structure/contents not yet explored
3. `owners[].ownerTaxable[].exemptions` — also an array, per taxing unit
   (empty `[]` in the example record)

All three need to be parsed and compared before assuming any one of them is
"the" homestead-status source of truth. Given `ears_state_reference.md`'s
finding that homestead is really a stack of ~13 sub-types
(AJR39–AJR54-equivalent), it's plausible each of these three locations
carries a different slice (e.g. property-wide vs. owner-specific vs.
per-taxing-unit exemption applicability) — this needs its own investigation
pass once the higher-priority tables are built.

## Extraction plan

**Status: built and verified, 2026-08-17.** After the `deeds[]`/`sales[]`
discovery (see `protax_extraction_structure.md`) prompted a full rethink of
the ingestion approach (`docs/tcad_eda/00_overview.md`'s companion-doc
list, and the plan at the time,
`C:\Users\rwrcr\.claude\plans\velvet-wishing-grove.md`), the original plan
of a hand-written, separately-named owner script was superseded by a
single generic, schema-driven loader covering both full owner fidelity and
the 11 other newly-discovered arrays in one pass. That loader
(`scripts/load_ancillary_data_to_sqlite.py`) was itself merged into
`scripts/load_protax_to_sqlite.py` later the same day, once it was clear
the "core Stage 1" vs. "ancillary" split no longer reflected a real
difference — see `load_protax_to_sqlite.py`'s docstring. The old
`load_owners_to_sqlite.py` / `property_owner` were left untouched during
the ancillary-loader build, per the non-breaking-pipeline reasoning
active at the time, but `property_owner` was dropped from the live
database shortly after (fully superseded by `property_owners`).

Built:
- `property_owners` — one row per owner per parcel (486,936 rows, matching
  the confirmed full-population owner count exactly), all owner scalar
  fields + all `ownerValue[0]` fields flattened onto the same row (columns
  generated from the full-population inventory scan, not hand-picked —
  70 columns).
- `property_owner_agents` — one row per agent relationship per owner
  (213,018 rows), 18 columns, FK back to `pID`.
- Both tables carry an `extra_fields` catch-all. For `property_owners`
  specifically this is *expected* to stay populated (not a drift signal,
  see below) — it's where `agents` (redundant with the dedicated table
  above), `exemptions`, `ownerValue` (the original nested key, redundant
  with the flattened columns), and, notably, the full **`ownerTaxable`
  array is preserved verbatim**, even though no dedicated table for it was
  built this pass. That data isn't lost — it's queryable right now via
  SQLite's `json_extract`/`json_each` against `property_owners.extra_fields`,
  just not yet flattened into its own indexed table.

**Deferred** (still true, unchanged):
- A dedicated table for `ownerTaxable[]` (~50 fields, 1:many per taxing
  unit, confirmed 100% of owners have at least one entry, full-population
  scan) — the per-taxing-unit tax rate/amount table described above. Raw
  data already sitting in `property_owners.extra_fields` in the meantime.
- Parsing/reconciling the three `exemptions[]` locations.
- Per-field population-rate checks beyond what the full inventory scan
  already provides in `full_inventory_scan.md`/`.json` — those numbers are
  now the full-population ground truth, not a sample, for every field this
  document lists above.
