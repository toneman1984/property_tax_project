# Texas EARS Manual — State Reference for Appraisal Roll Concepts

**Source:** [Electronic Appraisal Roll Submission (EARS): Record Layout and
Instructions Manual](http://traviscad.org/wp-content/uploads/Electronic-Appraisal-Roll-Submission-Record-Layout-and-Instructions-Manual.pdf),
Texas Comptroller of Public Accounts, Publication #96-1051, June 2019.
Hosted directly on traviscad.org.

## What this document is

EARS is the **state-mandated standard format** every Texas appraisal
district — including TCAD — must use to certify its annual appraisal roll to
the Comptroller's Property Tax Assistance Division (PTAD), per 34 TAC
§9.3059. It is **not** the same schema as the raw
`Travis_protaxExport_20250720.json` export we load into
`travis_property_tax.db` — that JSON appears to come from TCAD's CAMA vendor
(the public portal is hosted at `travis.prodigycad.com`, suggesting
ProdigyCAD), and no public data dictionary for that vendor-specific format
turned up in searching. EARS is a separate, state-facing reporting format.

Even so, EARS is directly useful: it's the authoritative legal/definitional
source for concepts our JSON export encodes but doesn't document (homestead
exemption types, the value cap, ownership percentage), and it gives us a
independent cross-check on field semantics we've been inferring from names
alone.

## Structure of the manual

Three record types, each with a full field layout appendix and a matching
"EDITS" appendix (validation rules):

| Record | Purpose | Relevance to this project |
|---|---|---|
| **AJR** — Account Jurisdiction Record (Appendices 1–2) | One record per account per category per taxing unit — parcel-level value, exemption, and ownership detail | **High** — see below |
| **AUD** — Ag Use Account Detail (Appendices 3–4) | Only generated for Category D1 (qualified open-space ag land); ~150 fields breaking down acreage/value by timber and pasture subtype | **Low** — applies only to agricultural land, not the SFR homestead parcels this project studies. Skimmed, not transcribed in detail. |
| **TU2** — Top-10 Taxpayer (Appendices 5–6) | Up to 10 records per taxing unit, largest taxpayers by value | **None** — jurisdiction-level reporting, not parcel-level |

## AJR fields relevant to fraud/homestead analysis

**Homestead is a stack of exemption types, not one flag.** AJR39 is a
general homestead indicator, but it's accompanied by distinct sub-types each
with their own dollar-amount field and eligibility rules:

- AJR39 Homestead Indicator (Y/N — general flag)
- AJR40 / AJR42 — Over-65 homestead (indicator / state-mandated $ amount, capped at $10,000 for ISD)
- AJR41 / AJR44 — Disabled homestead (indicator / amount)
- AJR45 / AJR46 — Local optional percentage homestead (amount / percentage offered, capped at 20%)
- AJR47 / AJR48 — Local optional over-65 / disabled homestead amounts
- AJR49–AJR54 — Disabled veteran variants (100% disabled veteran, surviving spouse of 100% disabled veteran, surviving spouse of service member killed in action, home donated by charity to disabled vet, partially disabled veteran, surviving spouse of first responder killed in line of duty)
- AJR71 / AJR72 — Tax ceiling ("freeze") indicator and amount, for over-65/disabled homesteads

**Implication for our EDA:** `property_profile.exemptions` (TEXT, unparsed)
almost certainly encodes some subset of this stack, not a single boolean.
Our current `has_homestead` logic (used throughout the POC and Stage 4) may
be collapsing distinctions that matter — e.g. an over-65 homestead has a tax
ceiling attached and very different fraud-risk dynamics than a standard
homestead. Parsing `exemptions` open (already flagged as a Phase 1 target in
`00_overview.md`) should check for these sub-types explicitly.

**The 10% homestead value cap is a defined, named mechanism.** AJR67 "Loss
to Cap on Homestead Increase Amount" = current market value − 110% of prior
year's market value − new construction amount. This is the legal basis for
the `limitationBaseYear`, `limitationMaxAllowedIncrease`,
`limitationLastYearHSValue`, `limitationNewValue` (and related) fields found
in the raw JSON's `ownerValue` object during the earlier owner-schema
exploration — those aren't arbitrary vendor fields, they're this specific,
well-defined statutory cap calculation. Correctly reconstructing cap history
per parcel could be a legitimate fraud signal on its own (e.g. a homestead
cap that keeps resetting/growing in a way inconsistent with continuous
owner-occupancy).

**Ownership percentage is officially "undivided interest," and multi-owner
is a normal, legally anticipated case.** AJR26 "Percent Ownership": *"If
multiple people share ownership of a single property in undivided
interests, report the separate undivided interest percentage for this
owner in this field."* Example given: `.333333` = one-third undivided
interest. This directly supports preserving the full `owners` array (rather
than collapsing to a single "primary" owner per parcel, as the current
`property_owner` table does) when the owner table gets rebuilt.

**Category codes** (AJR31) may be a cleaner, state-standardized cross-check
for property type than whatever TCAD/vendor-specific codes live in
`propType`/`useCd`:
- A = Single-family residential
- B = Multifamily residential
- C1 = Vacant lots and tracts
- E = Rural land not qualified for open-space appraisal + residential improvements
- (full code list in the source PDF, Appendix 1, field AJR31)

**Other fields of possible interest:**
- AJR22 Square Footage of Main Improvement, AJR23 Year Built — cross-check
  candidates for `imprvMainArea` / `imprvActualYearBuilt`.
- AJR13/AJR14 Most/Second-Most Recent Sale Date + AJR82/AJR83 Sale Price —
  sale history isn't currently loaded into our database at all; could be
  useful for detecting recent-sale-but-still-homesteaded patterns.
- AJR09 Parent Account Number — links properties treated as one economic
  unit (e.g. a house + adjacent vacant lot bought together). Not something
  we've considered; could matter for parcel-level rollups.
- AJR30 Owner ID Code — a stable owner identifier separate from name
  matching. Worth checking whether the raw JSON's `owners[].ownerID` field
  (seen during the earlier schema exploration) is this same concept — if
  so, it's a cleaner way to link multiple parcels to the same owner than
  fuzzy name matching.

## What was skimmed but not detailed here

- **AUD (Ag Use) appendix**: ~150 fields of acreage and market/productivity
  value broken out by land subtype (dryland cropland, irrigated cropland,
  native pasture, several timber classes under wildlife-management and
  restricted-use programs, etc.). Exhaustive but not relevant — applies only
  to Category D1 qualified open-space land, not the single-family
  residential population this project studies.
- **TU2 (Top-10 Taxpayer) appendix**: jurisdiction-level "largest taxpayers"
  reporting, no parcel-level content.

## Open questions for later phases

- Does TCAD actually submit through the ProdigyCAD-format JSON we have, or
  is that JSON a separate export product entirely disconnected from their
  EARS submissions? (Doesn't block using EARS as a definitional reference
  either way, but would clarify how authoritative a source it is for *this
  specific* dataset's exact encoding.)
- Once `exemptions` is parsed, check whether its encoding maps cleanly onto
  the AJR39–AJR54 sub-type stack above, or whether TCAD's own system uses a
  different internal taxonomy that only rolls up to these categories at
  EARS-submission time.
