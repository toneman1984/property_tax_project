# Full-Population TCAD JSON Inventory Scan

Generated 2026-08-17 19:28:28 by `scripts/inventory_scan_full.py`. Scanned 486,859 of 486,859 top-level parcel records in 9.0m using the `yajl2_c` ijson backend.

This supersedes any 500-record-sample population percentages quoted in `protax_extraction_structure.md` / `owner_data_structure.md` -- these numbers are from the full population, not a sample.

## Fields by top-level array/group

### `appeals`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `appeals` | 100.0% | — |  |
| `appeals[]` | 100.0% | — |  |
| `appeals[].appealAssignedTo` | 13.9% | str(28848) | ;  |
| `appeals[].appealID` | 100.0% | int(208263) | 1871059; 1871060 |
| `appeals[].appealStatus` | 100.0% | str(208263) | ORDT; ORDT |
| `appeals[].appealType` | 100.0% | str(208263) | P; P |
| `appeals[].appealedByAgentID` | 86.2% | int(179565) | 1556593; 1556593 |
| `appeals[].appealedByID` | 13.8% | int(28698) | 1402213; 1618882 |
| `appeals[].appealedByType` | 100.0% | str(208263) | A; A |
| `appeals[].claimantComments` | 98.8% | str(205844) | "Protest Other: any other action of the appraisal district, chief appraiser or ARB that applies to and adversely affects the property owner.
Pursuant  |
| `appeals[].claimantEvidence` | 93.6% | str(194873) | [{"s3ID": "travis/72e2ebae-197d-11f0-87b8-0242ac110003.xlsx", "addedBy": "arica.chambers@ryan.com", "dateAdded": "2025-04-14 17:11:43.928805", "descri |
| `appeals[].claimantEvidence.→json` | 100.0% | — |  |
| `appeals[].claimantEvidence.→json[]` | 100.0% | — |  |
| `appeals[].claimantEvidence.→json[].addedBy` | 100.0% | str(385169) | arica.chambers@ryan.com; cesser@tcadcentral.org |
| `appeals[].claimantEvidence.→json[].dateAdded` | 100.0% | str(385169) | 2025-04-14 17:11:43.928805; 2025-05-05 17:17:37.411847 |
| `appeals[].claimantEvidence.→json[].description` | 100.0% | str(385169) | 3File Appeals (51) - corrected parcel number added.xlsx; img0001.pdf |
| `appeals[].claimantEvidence.→json[].imageType` | 100.0% | str(82745) | Image; Image |
| `appeals[].claimantEvidence.→json[].portalUpload` | 100.0% | int(385107) | 1; 0 |
| `appeals[].claimantEvidence.→json[].s3ID` | 100.0% | str(385169) | travis/72e2ebae-197d-11f0-87b8-0242ac110003.xlsx; travis/bfc511a4-29fe-11f0-bf0b-0242ac110002.pdf |
| `appeals[].claimantEvidence.→json[].uploadedFileName` | 100.0% | str(385169) | 3File Appeals (51) - corrected parcel number added.xlsx; img0001.pdf |
| `appeals[].claimantOpinionOfValue` | 100.0% | int(208263) | 0; 0 |
| `appeals[].decision` | 86.4% | str(179911) | N/A; N/A |
| `appeals[].decisionAuthority` | 86.4% | str(179911) | N/A; N/A |
| `appeals[].decisionReason` | 86.4% | str(179911) | N/A; N/A |
| `appeals[].docketDt` | 82.0% | str(170678) | 2025-06-04 13:15:00; 2025-07-11 15:30:00 |
| `appeals[].docketEndTime` | 0.7% | str(1453) | 2025-07-09 08:15:00; 2025-07-18 15:30:00 |
| `appeals[].docketID` | 0.7% | int(1453) | 91240; 91246 |
| `appeals[].docketStartTime` | 82.0% | str(170678) | 2025-06-04 13:15:00; 2025-07-11 15:30:00 |
| `appeals[].docketTimeSlotID` | 0.7% | int(1453) | 795932; 792763 |
| `appeals[].dueDiligenceEvidenceAdditional` | 100.0% | int(208263) | 0; 0 |
| `appeals[].dueDiligenceEvidenceDeliveryDt` | 98.2% | str(204457) | 2025-04-22 21:24:18; 2025-07-03 11:07:56 |
| `appeals[].dueDiligenceEvidenceRequest` | 100.0% | int(208263) | 1; 1 |
| `appeals[].dueDiligenceEvidenceRequestDt` | 92.0% | str(191572) | 2025-04-14 00:00:00; 2025-04-14 00:00:00 |
| `appeals[].dueDiligenceEvidenceStaff` | 0.0% | — |  |
| `appeals[].dueDiligenceEvidenceWaiver` | 100.0% | int(208263) | 0; 0 |
| `appeals[].dueDiligencePreliminaryDistrictComments` | 1.1% | str(2369) | ORD M - 3 & 5; EVIDENCE MAILED VIA POST OFFICE_20250606 ANH// |
| `appeals[].dueDiligenceTaxesPaid` | 100.0% | int(208263) | 0; 0 |
| `appeals[].dueDiligenceTaxesPaidVerifiedBy` | 0.0% | — |  |
| `appeals[].dueDiligenceTaxesPaidVerifiedDt` | 0.0% | — |  |
| `appeals[].finalAppraisedValue` | 100.0% | int(208263) | 4332066; 62490000 |
| `appeals[].finalImprovementHSValue` | 100.0% | int(208263) | 0; 0 |
| `appeals[].finalImprovementNHSValue` | 100.0% | int(208263) | 99906; 44022563 |
| `appeals[].finalImprovementValue` | 100.0% | int(208263) | 99906; 44022563 |
| `appeals[].finalLandHSValue` | 100.0% | int(208263) | 0; 0 |
| `appeals[].finalLandNHSValue` | 100.0% | int(208263) | 4232160; 18467437 |
| `appeals[].finalLandValue` | 100.0% | int(208263) | 4232160; 18467437 |
| `appeals[].finalLetterName` | 0.0% | — |  |
| `appeals[].finalLetterPrintDt` | 0.0% | — |  |
| `appeals[].finalLetterPrinted` | 98.6% | int(205430) | 0; 0 |
| `appeals[].finalMarketValue` | 100.0% | int(208263) | 4332066; 62490000 |
| `appeals[].finalSUExclusionValue` | 100.0% | int(208263) | 0; 0 |
| `appeals[].finalSULandMktValue` | 100.0% | int(208263) | 0; 0 |
| `appeals[].finalSUValue` | 100.0% | int(208263) | 0; 0 |
| `appeals[].finalized` | 100.0% | int(208263) | 1; 1 |
| `appeals[].finalizedBy` | 87.0% | str(181102) | lmann@tcadcentral.org; lmann@tcadcentral.org |
| `appeals[].finalizedDt` | 87.0% | str(181102) | 2025-06-02 13:53:25; 2025-07-11 08:44:12 |
| `appeals[].formalAgDecision` | 100.0% | int(208263) | 0; 0 |
| `appeals[].formalAgDecisionComment` | 0.0% | str(1) |  |
| `appeals[].formalAppraiser` | 7.1% | str(14855) | jgarza@tcadcentral.org; tostone@tcadcentral.org |
| `appeals[].formalAppraiserEquityComments` | 0.0% | str(2) | ;  |
| `appeals[].formalAppraiserMarketComments` | 7.1% | str(14895) | ARB: 2,055,000; ARB: 2,812,500 |
| `appeals[].formalArrivalTime` | 0.0% | str(10) | 2025-07-02 16:01:34; 2025-07-02 16:01:34 |
| `appeals[].formalBoardEquityComments` | 0.0% | str(1) |  |
| `appeals[].formalBoardFinalInstructions` | 0.0% | str(3) | ARB: 862,303
TCAD 862,303
OWNER: 760,000;  |
| `appeals[].formalBoardMarketComments` | 0.0% | str(4) | ;  |
| `appeals[].formalClaimantEquityComments` | 0.0% | str(1) |  |
| `appeals[].formalClaimantMarketComments` | 0.0% | str(4) | INTERIOR IMAGES AT HTTPS://WWW.JWSTODDARD.COM/WESTBROOK?PGID=M6SFA3T8-784C3935-7220-4C4C-B4ED-B980762353E4;  |
| `appeals[].formalDecisionAdjustmentValue` | 99.1% | int(206467) | 0; 0 |
| `appeals[].formalDecisionAppraiserAdjustmentReason` | 0.0% | str(5) | ; ARB ENTERED DECISION INCORRECTLY IN DEC SHEET APP; CORRECTED TO $3.4B- LHM |
| `appeals[].formalDecisionValueAdjustment` | 100.0% | str(208263) | NC; NC |
| `appeals[].formalEndMeeting` | 7.6% | str(15812) | 2025-06-23 13:12:42; 2025-06-18 12:03:25 |
| `appeals[].formalFirstMotion` | 100.0% | int(208263) | 0; 0 |
| `appeals[].formalFirstMotionBy` | 0.0% | str(1) |  |
| `appeals[].formalFirstMotionPasses` | 100.0% | int(208263) | 0; 0 |
| `appeals[].formalFirstMotionSecondedBy` | 0.0% | str(1) |  |
| `appeals[].formalHearingRecordings` | 0.0% | — |  |
| `appeals[].formalSecondMotion` | 100.0% | int(208263) | 0; 0 |
| `appeals[].formalSecondMotionBy` | 0.0% | str(1) |  |
| `appeals[].formalSecondMotionPasses` | 100.0% | int(208263) | 0; 0 |
| `appeals[].formalSecondMotionSecondedBy` | 0.0% | str(1) |  |
| `appeals[].formalStartMeeting` | 7.2% | str(14969) | 2025-06-23 13:01:00; 2025-06-18 11:48:38 |
| `appeals[].formalThirdMotion` | 100.0% | int(208263) | 0; 0 |
| `appeals[].formalThirdMotionBy` | 0.0% | str(1) |  |
| `appeals[].formalThirdMotionPasses` | 100.0% | int(208263) | 0; 0 |
| `appeals[].formalThirdMotionSecondedBy` | 0.0% | str(1) |  |
| `appeals[].hearingLetterDt` | 79.9% | str(166373) | 2025-05-17 14:44:39; 2025-06-02 11:04:49 |
| `appeals[].hearingLetterName` | 79.9% | str(166373) | ARB_Notice of Hearing_2025; ARB_Notice of Hearing_2025 |
| `appeals[].informal` | 100.0% | int(208263) | 0; 1 |
| `appeals[].informalAppraiser` | 18.2% | str(37976) | NMcGaughy@tcadcentral.org; mhoese@tcadcentral.org |
| `appeals[].informalAppraiserComment` | 12.5% | str(25985) | CONSIDERATION FOR SHAPE AND TOPOGRAPHY OF THE LOT.; PER FURTHER DISCUSSION,VALUE WAS ROLLED BACK TO 2024 DUE TO MMA NOT CHANGING. JN 5/15/25
 |
| `appeals[].informalArrivalTime` | 0.2% | str(455) | 2025-07-16 15:50:12; 2025-07-16 15:50:12 |
| `appeals[].informalClaimantComment` | 1.0% | str(2023) | ;  |
| `appeals[].informalDecisionAdjustmentValue` | 100.0% | int(208263) | 4332066; 62490000 |
| `appeals[].informalDecisionAppraiserAdjustmentReason` | 75.8% | str(157900) | Taxpayer accepted recommendation from appraiser; Taxpayer accepted recommendation from appraiser |
| `appeals[].informalDecisionSupportingDocuments` | 0.2% | str(429) | [{"s3ID": "travis/3573a8de-4c6e-11f0-9e17-0242ac110003.pdf", "addedBy": "sfoye@tcadcentral.org", "dateAdded": "2025-06-18 13:01:08.373104", "descripti |
| `appeals[].informalDecisionSupportingDocuments.→json` | 100.0% | — |  |
| `appeals[].informalDecisionSupportingDocuments.→json[]` | 100.0% | — |  |
| `appeals[].informalDecisionSupportingDocuments.→json[].addedBy` | 100.0% | str(489) | sfoye@tcadcentral.org; sfoye@tcadcentral.org |
| `appeals[].informalDecisionSupportingDocuments.→json[].dateAdded` | 100.0% | str(489) | 2025-06-18 13:01:08.373104; 2025-06-10 12:50:53.488294 |
| `appeals[].informalDecisionSupportingDocuments.→json[].description` | 100.0% | str(489) | 6_18 ownwell commercial toplines.pdf; ownwell commercial 6_9 Topline.pdf |
| `appeals[].informalDecisionSupportingDocuments.→json[].s3ID` | 100.0% | str(489) | travis/3573a8de-4c6e-11f0-9e17-0242ac110003.pdf; travis/739fb284-4623-11f0-bfa7-0242ac110007.pdf |
| `appeals[].informalDecisionSupportingDocuments.→json[].uploadedFileName` | 100.0% | str(489) | 6_18 ownwell commercial toplines.pdf; ownwell commercial 6_9 Topline.pdf |
| `appeals[].informalDecisionValueAdjustment` | 100.0% | str(208263) | A; A |
| `appeals[].informalDt` | 0.0% | — |  |
| `appeals[].informalEndMeeting` | 9.2% | str(19167) | 2025-05-23 16:00:04; 2025-05-29 14:33:09 |
| `appeals[].informalStartMeeting` | 8.5% | str(17663) | 2025-05-23 16:00:03; 2025-05-29 14:31:27 |
| `appeals[].initialAppraisedValue` | 100.0% | int(208263) | 4332066; 63354012 |
| `appeals[].initialImprovementHSValue` | 100.0% | int(208263) | 0; 0 |
| `appeals[].initialImprovementNHSValue` | 100.0% | int(208263) | 0; 0 |
| `appeals[].initialImprovementValue` | 100.0% | int(208263) | 99906; 44886575 |
| `appeals[].initialLandHSValue` | 100.0% | int(208263) | 0; 0 |
| `appeals[].initialLandNHSValue` | 100.0% | int(208263) | 0; 0 |
| `appeals[].initialLandValue` | 100.0% | int(208263) | 4232160; 18467437 |
| `appeals[].initialMarketValue` | 100.0% | int(208263) | 4332066; 63354012 |
| `appeals[].initialSUExclusionValue` | 100.0% | int(208263) | 0; 0 |
| `appeals[].initialSULandMktValue` | 100.0% | int(208263) | 0; 0 |
| `appeals[].initialSUValue` | 100.0% | int(208263) | 0; 0 |
| `appeals[].massCreateID` | 100.0% | int(208263) | 22024; 22024 |
| `appeals[].noticeAppraisedValue` | 100.0% | int(208263) | 0; 0 |
| `appeals[].noticeImprovementHSValue` | 100.0% | int(208263) | 0; 0 |
| `appeals[].noticeImprovementNHSValue` | 100.0% | int(208263) | 0; 0 |
| `appeals[].noticeImprovementValue` | 100.0% | int(208263) | 0; 0 |
| `appeals[].noticeLandHSValue` | 100.0% | int(208263) | 0; 0 |
| `appeals[].noticeLandNHSValue` | 100.0% | int(208263) | 0; 0 |
| `appeals[].noticeLandValue` | 100.0% | int(208263) | 0; 0 |
| `appeals[].noticeMarketValue` | 100.0% | int(208263) | 0; 0 |
| `appeals[].noticeSUExclusionValue` | 100.0% | int(208263) | 0; 0 |
| `appeals[].noticeSULandMktValue` | 100.0% | int(208263) | 0; 0 |
| `appeals[].noticeSUValue` | 100.0% | int(208263) | 0; 0 |
| `appeals[].pID` | 100.0% | int(208263) | 100008; 100012 |
| `appeals[].pYear` | 100.0% | int(208263) | 2025; 2025 |
| `appeals[].panelID` | 7.1% | int(14761) | 36; 36 |
| `appeals[].panelMembers` | 7.2% | str(15015) | ["Marshall McDade", "Lynn Wilkinson", "Michael Fracasso"]; ["Mary Lopez", "Lisa Roberts", "Elise Ferreira"]  [json-string-decoded x15015] |
| `appeals[].panelMembers.→json` | 100.0% | — |  |
| `appeals[].panelMembers.→json[]` | 100.0% | str(37160) | Marshall McDade; Lynn Wilkinson |
| `appeals[].presentationPublished` | 100.0% | int(208263) | 1; 1 |
| `appeals[].presentationPublishedBy` | 98.3% | str(204637) | mmills@tcadcentral.org; NMcGaughy@tcadcentral.org |
| `appeals[].presentationPublishedDt` | 98.3% | str(204637) | 2025-04-22 21:24:18; 2025-07-03 11:07:56 |
| `appeals[].presentationS3ID` | 98.3% | str(204637) | travis/0e69c38c-1fea-11f0-b993-0242ac110008.pdf; travis/e13535c4-5827-11f0-bd90-0242ac110008.pdf |
| `appeals[].protesterScheduled` | 100.0% | int(208263) | 0; 0 |
| `appeals[].protesterScheduledCount` | 100.0% | int(208263) | 0; 0 |
| `appeals[].protesterScheduledDt` | 0.0% | — |  |
| `appeals[].reservationID` | 0.7% | int(1453) | 1916519; 1909610 |
| `appeals[].valueDecisionAdjustmentType` | 100.0% | str(208263) | I; I |
| `appeals[].valueDecisionDistributionRule` | 83.1% | str(172994) | RI; RI |

### `deeds`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `deeds` | 100.0% | — |  |
| `deeds[]` | 100.0% | — |  |
| `deeds[].book` | 1.1% | str(23857) | ;  |
| `deeds[].buyerLine` | 88.9% | str(1936332) | BRIZENDINE CHARLES DAVID; FEDERAL DEPOSIT INSURANCE CORP |
| `deeds[].comment` | 11.4% | str(247797) | REFILED TO CORRECT GRANTEES NAME ON DOC #2005173685TR; CORRECTING GRANTEE |
| `deeds[].consideration` | 22.9% | str(497992) | $2,395,000; $10,000 |
| `deeds[].deedDt` | 93.4% | str(2035620) | 1993-07-07 00:00:00; 1993-03-02 00:00:00 |
| `deeds[].deedID` | 100.0% | int(2178541) | 25; 26 |
| `deeds[].deedRecordedDt` | 87.1% | str(1898436) | 1993-07-07 00:00:00; 1993-03-02 00:00:00 |
| `deeds[].deedType` | 93.2% | str(2030316) | SW; ST |
| `deeds[].exemptionNotes` | 8.2% | str(177987) | Reset Exemptions;  |
| `deeds[].exemptionReset` | 8.2% | int(177987) | 1; 0 |
| `deeds[].fileDt` | 8.2% | str(177986) | 2023-08-17;  |
| `deeds[].instrumentNum` | 51.1% | str(1112342) | 2012207435TR; 2014035621TR |
| `deeds[].pID` | 100.0% | int(2178541) | 100008; 100008 |
| `deeds[].page` | 57.1% | str(1244274) | 00251; 00232 |
| `deeds[].properties` | 100.0% | str(2178541) | [100008]; [100008]  [json-string-decoded x2178541] |
| `deeds[].properties.→json` | 100.0% | — |  |
| `deeds[].properties.→json[]` | 100.0% | int(6733058) | 100008; 100008 |
| `deeds[].sellerLine` | 76.5% | str(1667774) | FEDERAL DEPOSIT INSURANCE CORP; BEVERLY GENE |
| `deeds[].volume` | 57.1% | str(1244264) | 11978; 11883 |

### `events`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `events` | 100.0% | — |  |
| `events[]` | 100.0% | — |  |
| `events[].createDt` | 100.0% | str(623461) | 2012-08-09 00:00:00; 2017-12-26 00:00:00 |
| `events[].createdBy` | 100.0% | str(623461) | ntorrez; nlawlor |
| `events[].eventData` | 79.1% | str(492923) | {"Ref1": "0", "Ref2": "0", "Ref3": "0", "Ref4": "0", "Ref5": "0", "Ref6": "0", "RefYear": null, "UserName": "ntorrez", "EventDate": "2012-08-09", "Eve |
| `events[].eventData.→json` | 100.0% | — |  |
| `events[].eventData.→json.EventDate` | 100.0% | str(296702) | 2012-08-09; 2017-12-26 |
| `events[].eventData.→json.EventDesc` | 99.8% | str(290332) | MERGE/DELE 100009-100011 (0100030106-0108) OW/PES FOR 2013; EXEMPT STATUS GRANTED FOR 2017 |
| `events[].eventData.→json.LegacyEventID` | 100.0% | int(290877) | 10008513; 15279782 |
| `events[].eventData.→json.OwnerID` | 100.0% | int(15) | 185429; 186681 |
| `events[].eventData.→json.Ref1` | 98.8% | str(287515) | 0; 0 |
| `events[].eventData.→json.Ref2` | 98.8% | str(287515) | 0; 0 |
| `events[].eventData.→json.Ref3` | 98.8% | str(287515) | 0; 0 |
| `events[].eventData.→json.Ref4` | 98.8% | str(287515) | 0; 0 |
| `events[].eventData.→json.Ref5` | 98.8% | str(287515) | 0; 0 |
| `events[].eventData.→json.Ref6` | 98.8% | str(287515) | 0; 0 |
| `events[].eventData.→json.RefEventType` | 0.0% | — |  |
| `events[].eventData.→json.RefNumber` | 98.8% | str(287516) | 0; 0 |
| `events[].eventData.→json.RefYear` | 0.0% | str(1) | 2021 |
| `events[].eventData.→json.SystemType` | 100.0% | str(290878) | A; A |
| `events[].eventData.→json.UserName` | 100.0% | str(290879) | ntorrez; nlawlor |
| `events[].eventData.→json.dtEvent` | 100.0% | str(1591) | 2021-08-09 15:55:50; 2021-07-23 15:40:35 |
| `events[].eventData.→json.lCaseID` | 100.0% | int(1591) | 108497; 118367 |
| `events[].eventData.→json.lEventID` | 100.0% | int(1591) | 17691173; 17543860 |
| `events[].eventData.→json.lPacsUserID` | 100.0% | int(1591) | 497; 497 |
| `events[].eventData.→json.lPropID` | 100.0% | int(1591) | 305041; 112916 |
| `events[].eventData.→json.lYear` | 100.0% | int(1591) | 2021; 2021 |
| `events[].eventData.→json.pid` | 100.0% | int(60839), str(641) | 100040; 100041 |
| `events[].eventData.→json.szARBType` | 100.0% | str(1591) | AP; AP |
| `events[].eventData.→json.szEventCode` | 100.0% | str(1591) | CMNT; CMNT |
| `events[].eventData.→json.szEventComment` | 100.0% | str(1591) | RTN- NOTICE OF BOARD ORDER. NOT DELIVERABLE AS ADDRESSED, UNABLE TO FORWARD.; Notice of Final Order returned. 7/23/2021 TMD// |
| `events[].eventDescription` | 99.9% | str(622857) | MERGE/DELE 100009-100011 (0100030106-0108) OW/PES FOR 2013; EXEMPT STATUS GRANTED FOR 2017 |
| `events[].eventID` | 100.0% | int(623461) | 880645; 6105991 |
| `events[].eventType` | 100.0% | str(623461) | CMNT_LAND; ABS_CMNT |
| `events[].formID` | 100.0% | int(623461) | 212; 212 |
| `events[].inactive` | 100.0% | int(623461) | 0; 0 |
| `events[].inactiveBy` | 0.0% | str(72) | TPaul@tcadcentral.org; TPaul@tcadcentral.org |
| `events[].inactiveDt` | 0.0% | str(72) | 2024-08-21 12:25:13; 2024-08-21 12:33:31 |
| `events[].pID` | 100.0% | int(623461) | 100012; 100026 |
| `events[].updateDt` | 53.5% | str(333877) | 2021-09-28 16:32:25; 2021-09-28 16:32:25 |
| `events[].updatedBy` | 50.9% | str(317679) | TP Conv - importEvents; TP Conv - importEvents |

### `exemptionReset`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `exemptionReset` | 100.0% | int(486859) | 0; 0 |

### `exemptionResetReason`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `exemptionResetReason` | 27.3% | str(132821) | ;  |

### `geometry`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `geometry` | 100.0% | str(486859) | [30.2545186553, -97.7620645363]; [30.2541233655, -97.7617866403]  [json-string-decoded x486859] |
| `geometry.→json` | 100.0% | — |  |
| `geometry.→json[]` | 77.1% | float(750944) | 30.2545186553; -97.7620645363 |

### `inactive`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `inactive` | 100.0% | int(486859) | 0; 0 |

### `inactiveDt`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `inactiveDt` | 2.6% | str(12681) | 2021-10-14 11:11:40; 2021-10-14 11:11:40 |

### `inactiveNotes`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `inactiveNotes` | 0.4% | str(2028) | DELE/MERGE W/109618/JASON RULEY REQ FOR 2023; INTO TRAVIS SETTLEMENT SEC 2 AMD LOTS 137 & 138 FOR 2022 - SEE 958842 & 958843 |

### `inactiveReason`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `inactiveReason` | 0.4% | str(2015) | DELETE; DELETE |

### `inspectionYr`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `inspectionYr` | 16.3% | int(79474) | 2025; 2025 |

### `inspections`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `inspections` | 100.0% | — |  |
| `inspections[]` | 100.0% | — |  |
| `inspections[].inspectionActiveDt` | 98.8% | str(639064) | 2013-10-17 00:00:00; 2027-09-01 00:00:00 |
| `inspections[].inspectionAppraiser` | 94.2% | str(608844) | DAMON DAUGHTRY; DMazziotti@tcadcentral.org |
| `inspections[].inspectionCompleteDt` | 27.5% | str(177755) | 2022-02-14 16:31:16; 2022-02-07 |
| `inspections[].inspectionCompleted` | 100.0% | int(646554) | 1; 0 |
| `inspections[].inspectionCompletedBy` | 27.5% | str(177755) | BOsborn@tcadcentral.org; TP - ZD6917 |
| `inspections[].inspectionFieldNotes` | 13.3% | str(85990) | ;  |
| `inspections[].inspectionID` | 100.0% | int(646554) | 37305; 943377 |
| `inspections[].inspectionNotes` | 100.0% | str(646554) | UNSPECIFIED; PHYSICAL INSPCTION |
| `inspections[].inspectionReason` | 100.0% | str(646552) | RECHECK; PI |
| `inspections[].pID` | 100.0% | int(646554) | 100008; 100008 |

### `isUDI`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `isUDI` | 100.0% | int(486859) | 0; 0 |

### `lastAppraisalDt`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `lastAppraisalDt` | 16.3% | str(79475) | 2024-10-04 15:37:41; 2024-10-04 15:33:33 |

### `links`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `links` | 100.0% | — |  |
| `links[]` | 100.0% | — |  |
| `links[].linkID` | 100.0% | int(153617) | 2491920; 2491921 |
| `links[].linkedPID` | 100.0% | int(153617) | 825083; 723876 |
| `links[].pID` | 100.0% | int(153617) | 100008; 100012 |

### `notes`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `notes` | 100.0% | — |  |
| `notes[]` | 100.0% | — |  |
| `notes[].content` | 100.0% | str(1276315) | %, DETAILS  // --- //; NCDR 1/27/16 HAA  //  CHG TO 100% COMP, ADD SF TO DTLS, UPDT DBA 2/10/14 LBC  //  NEW IMP SET UP @ 1% PER FC, C14 2/11/13 DWD   |
| `notes[].isPrivate` | 100.0% | int(1276315) | 1; 0 |
| `notes[].noteID` | 100.0% | int(1276315) | 1; 2 |
| `notes[].pID` | 100.0% | int(1276315) | 100008; 100008 |

### `owners`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `owners` | 100.0% | — |  |
| `owners[]` | 100.0% | — |  |
| `owners[].addrCity` | 99.9% | str(486508) | WOODCREEK; SAN FRANCISCO |
| `owners[].addrCountry` | 37.8% | str(183944) | US; US |
| `owners[].addrDeliveryLine` | 100.0% | str(486704) | 41 DOOLITTLE DR; 400 HOWARD ST |
| `owners[].addrFreeForm` | 100.0% | int(486936) | 0; 0 |
| `owners[].addrFreeForm1` | 29.6% | str(144161) | % SDC LEASING & MANAGEMENT; ATTN AV TAX DEPT #34252 |
| `owners[].addrFreeForm2` | 74.8% | str(364258) | 41 DOOLITTLE DR; 601 N LAMAR BLVD STE 301 |
| `owners[].addrFreeForm3` | 17.9% | str(87198) | ;  |
| `owners[].addrInternational` | 100.0% | int(486936) | 0; 0 |
| `owners[].addrState` | 100.0% | str(486711) | TX; CA |
| `owners[].addrUnitDesignator` | 21.0% | str(102170) | ;  |
| `owners[].addrZip` | 99.9% | str(486452) | 78676-2530; 94105-2618 |
| `owners[].agents` | 100.0% | — |  |
| `owners[].agents[]` | 100.0% | — |  |
| `owners[].agents[].agentID` | 100.0% | int(213018) | 2024; 1556593 |
| `owners[].agents[].applicationDt` | 94.4% | str(201105) | 2021-06-14 00:00:00; 2025-05-09 00:00:00 |
| `owners[].agents[].authorityConfidential` | 100.0% | int(213018) | 0; 1 |
| `owners[].agents[].authorityOther` | 100.0% | int(213018) | 1; 0 |
| `owners[].agents[].authorityProtest` | 100.0% | int(213018) | 1; 1 |
| `owners[].agents[].authorityResolveTaxMatters` | 100.0% | int(213018) | 1; 1 |
| `owners[].agents[].companyName` | 100.0% | str(213018) | BRECK BOSTWICK & ASSOC; RYAN LLC - AUSTIN COMMERCIAL |
| `owners[].agents[].contactName` | 35.3% | str(75266) | ;  |
| `owners[].agents[].contactPhone` | 98.8% | str(210481) | 512-418-0027; 512-476-0022 |
| `owners[].agents[].effectiveDt` | 94.4% | str(201074) | 2021-06-12 00:00:00; 2025-05-09 00:00:00 |
| `owners[].agents[].expirationDt` | 10.5% | str(22301) | 2025-05-09 00:00:00; 2025-05-08 00:00:00 |
| `owners[].agents[].firstName` | 30.4% | str(64846) | JOHN A PELAYO CCIM, CMI; JOHN A PELAYO CCIM, CMI |
| `owners[].agents[].lastName` | 10.5% | str(22365) | BODDY;  |
| `owners[].agents[].mailingsARB` | 100.0% | int(213018) | 0; 1 |
| `owners[].agents[].mailingsCAD` | 100.0% | int(213018) | 0; 1 |
| `owners[].agents[].mailingsTaxingUnit` | 100.0% | int(213018) | 0; 0 |
| `owners[].agents[].pAccountID` | 100.0% | int(213018) | 8119581; 8119581 |
| `owners[].agents[].propertyAccountAgentID` | 100.0% | int(213018) | 2332347; 2576179 |
| `owners[].applyPctExemptions` | 100.0% | int(486936) | 0; 0 |
| `owners[].autoCass` | 100.0% | int(486736) | 1; 1 |
| `owners[].carrierRoute` | 95.9% | str(466915) | R012; C017 |
| `owners[].cassValidationBy` | 97.6% | str(475188) | aalbers@tcadcentral.org; sbrittner@tcadcentral.org |
| `owners[].cassValidationDt` | 97.6% | str(475188) | 2025-03-24 17:20:44; 2025-05-15 13:22:03 |
| `owners[].cassValidationService` | 97.6% | str(475188) | Smarty; Smarty Streets |
| `owners[].deliveryPoint` | 95.8% | str(466393) | 41; 00 |
| `owners[].deliveryPointCheckDigit` | 95.8% | str(466342) | 1; 4 |
| `owners[].exemptions` | 100.0% | — |  |
| `owners[].exemptions[]` | 100.0% | — |  |
| `owners[].exemptions[].additionalAmountCalculationBaseYear` | 100.0% | int(374916) | 0; 0 |
| `owners[].exemptions[].applicationID` | 2.8% | int(10421) | 12648; 9713 |
| `owners[].exemptions[].applyPctExemptions` | 100.0% | int(374916) | 0; 0 |
| `owners[].exemptions[].beginDt` | 8.4% | str(31596) | 2021-06-23 05:00:00; 2023-03-01 06:00:00 |
| `owners[].exemptions[].calculationRule` | 100.0% | str(374916) | Standard; Standard |
| `owners[].exemptions[].deferralEndDt` | 0.0% | — |  |
| `owners[].exemptions[].deferralStartDt` | 0.0% | str(1) | 2023-03-22 00:00:00 |
| `owners[].exemptions[].exemptionCode` | 100.0% | str(374916) | EX-XV; HS |
| `owners[].exemptions[].exemptionComment` | 31.3% | str(117324) | Add Exemption HS KH 6/29/23;  |
| `owners[].exemptions[].expirationDt` | 0.0% | str(57) | 2025-03-01 00:00:00; 2023-01-20 06:00:00 |
| `owners[].exemptions[].grantedDt` | 27.5% | str(102923) | 2023-06-29 12:49:06; 2023-01-11 08:32:31 |
| `owners[].exemptions[].newExemptionIndicator` | 100.0% | int(374916) | 0; 0 |
| `owners[].exemptions[].newExemptionYear` | 6.2% | int(23347) | 0; 0 |
| `owners[].exemptions[].pAccountID` | 100.0% | int(374916) | 8119592; 8745341 |
| `owners[].exemptions[].pExemptionID` | 100.0% | int(374916) | 6701978; 7246629 |
| `owners[].exemptions[].pctExemption` | 100.0% | float(374916) | 0.0; 100.0 |
| `owners[].exemptions[].qualifyYr` | 96.8% | int(362798) | 2021; 2017 |
| `owners[].exemptions[].useBaseYearForAdditionalAmountCalculation` | 100.0% | int(374916) | 0; 0 |
| `owners[].firstName` | 27.2% | str(132465) | ;  |
| `owners[].lastName` | 27.2% | str(132461) | ;  |
| `owners[].latitude` | 28.9% | str(140780) | 37.78877; 30.30105 |
| `owners[].longitude` | 28.9% | str(140780) | -122.3959; -98.01291 |
| `owners[].name` | 100.0% | str(486936) | DJB INVESTMENT PROPERTY LLC; 1219 SOUTH LAMAR VENTURE LLC |
| `owners[].nameSecondary` | 30.0% | str(146039) | % BLACKROCK REALTY ADVISORS JENNIFER FREEDMAN; % SDC LEASING & MANAGEMENT |
| `owners[].ownerID` | 100.0% | int(486936) | 1600885; 1518342 |
| `owners[].ownerPct` | 100.0% | float(486936) | 100.0; 100.0 |
| `owners[].ownerTaxable` | 100.0% | — |  |
| `owners[].ownerTaxable[]` | 100.0% | — |  |
| `owners[].ownerTaxable[].appraisedValue` | 100.0% | int(3085085) | 4332066; 4332066 |
| `owners[].ownerTaxable[].bppLateInterstateAllocationValue` | 100.0% | int(3085085) | 0; 0 |
| `owners[].ownerTaxable[].exemptions` | 100.0% | — |  |
| `owners[].ownerTaxable[].exemptions[]` | 100.0% | — |  |
| `owners[].ownerTaxable[].exemptions[].allocationFactor` | 100.0% | float(5030917) | 100.0; 100.0 |
| `owners[].ownerTaxable[].exemptions[].calculationType` | 100.0% | str(5030917) | EX-XV; EX-XV-PRORATED |
| `owners[].ownerTaxable[].exemptions[].exemptionAmount` | 100.0% | int(5030917) | 1099844; 0 |
| `owners[].ownerTaxable[].exemptions[].exemptionCode` | 100.0% | str(5030917) | EX-XV; EX-XV |
| `owners[].ownerTaxable[].exemptions[].includeExemptionCount` | 100.0% | int(5030917) | 1; 0 |
| `owners[].ownerTaxable[].exemptions[].localExemptionAmount` | 100.0% | int(5030917) | 0; 0 |
| `owners[].ownerTaxable[].exemptions[].pPropertyAccountTaxingUnitExemptionID` | 100.0% | int(5030917) | 8117215582; 8117215583 |
| `owners[].ownerTaxable[].exemptions[].pPropertyAccountTaxingUnitID` | 100.0% | int(5030917) | 4399404293; 4399404293 |
| `owners[].ownerTaxable[].exemptions[].totalExemptionAmount` | 100.0% | int(5030917) | 1099844; 0 |
| `owners[].ownerTaxable[].hsGroupPct` | 100.0% | float(3085085) | 100.0; 100.0 |
| `owners[].ownerTaxable[].improvementHSValue` | 100.0% | int(3085085) | 0; 0 |
| `owners[].ownerTaxable[].improvementNHSValue` | 100.0% | int(3085085) | 99906; 99906 |
| `owners[].ownerTaxable[].landHSValue` | 100.0% | int(3085085) | 0; 0 |
| `owners[].ownerTaxable[].landNHSValue` | 100.0% | int(3085085) | 4232160; 4232160 |
| `owners[].ownerTaxable[].limitationAmt` | 100.0% | float(3085085) | 0.0; 0.0 |
| `owners[].ownerTaxable[].limitationExemptionCode` | 100.0% | str(3085085) | ;  |
| `owners[].ownerTaxable[].limitationNetAppraisedValue` | 100.0% | int(3085085) | 0; 0 |
| `owners[].ownerTaxable[].limitationPresent` | 100.0% | int(3085085) | 0; 0 |
| `owners[].ownerTaxable[].limitationPreviousTaxDue` | 100.0% | float(3085085) | 0.0; 0.0 |
| `owners[].ownerTaxable[].limitationPreviousTaxDueNoLimit` | 100.0% | float(3085085) | 0.0; 0.0 |
| `owners[].ownerTaxable[].limitationTaxAmt` | 100.0% | float(3085085) | 0.0; 0.0 |
| `owners[].ownerTaxable[].limitationTaxRate` | 100.0% | float(3085085) | 0.0; 0.0 |
| `owners[].ownerTaxable[].limitationTaxableValue` | 100.0% | int(3085085) | 0; 0 |
| `owners[].ownerTaxable[].limitationTransfer` | 100.0% | int(3085085) | 0; 0 |
| `owners[].ownerTaxable[].limitationTransferDt` | 0.0% | str(171) | 2025-01-01 00:00:00; 2025-01-01 00:00:00 |
| `owners[].ownerTaxable[].limitationTransferPct` | 100.0% | float(3085085) | 0.0; 0.0 |
| `owners[].ownerTaxable[].limitationValue` | 100.0% | int(3085085) | 0; 0 |
| `owners[].ownerTaxable[].limitationYr` | 100.0% | int(3085085) | 0; 0 |
| `owners[].ownerTaxable[].marketValue` | 100.0% | int(3085085) | 4332066; 4332066 |
| `owners[].ownerTaxable[].netAppraisedValue` | 100.0% | int(3085085) | 4332066; 4332066 |
| `owners[].ownerTaxable[].newBppValue` | 100.0% | int(3085085) | 0; 0 |
| `owners[].ownerTaxable[].newImprovementHSValue` | 100.0% | int(3085085) | 0; 0 |
| `owners[].ownerTaxable[].newImprovementNHSValue` | 100.0% | int(3085085) | 0; 0 |
| `owners[].ownerTaxable[].newImprovementValue` | 100.0% | int(3085085) | 0; 0 |
| `owners[].ownerTaxable[].newLandHSValue` | 100.0% | int(3085085) | 0; 0 |
| `owners[].ownerTaxable[].newLandNHSValue` | 100.0% | int(3085085) | 0; 0 |
| `owners[].ownerTaxable[].newLandValue` | 100.0% | int(3085085) | 0; 0 |
| `owners[].ownerTaxable[].newValue` | 100.0% | int(3085085) | 0; 0 |
| `owners[].ownerTaxable[].newValueTaxable` | 100.0% | int(3085085) | 0; 0 |
| `owners[].ownerTaxable[].omittedImprovementHSValue` | 100.0% | int(3085085) | 0; 0 |
| `owners[].ownerTaxable[].omittedImprovementNHSValue` | 100.0% | int(3085085) | 0; 0 |
| `owners[].ownerTaxable[].pAccountID` | 100.0% | int(3085085) | 8119581; 8119581 |
| `owners[].ownerTaxable[].pPropertyAccountTaxingUnitID` | 100.0% | int(3085085) | 4399404227; 4399404228 |
| `owners[].ownerTaxable[].suExclusionValue` | 100.0% | int(3085085) | 0; 0 |
| `owners[].ownerTaxable[].suExempt` | 100.0% | int(3085085) | 0; 0 |
| `owners[].ownerTaxable[].suLandMktValue` | 100.0% | int(3085085) | 0; 0 |
| `owners[].ownerTaxable[].suNonExempt` | 100.0% | int(3085085) | 0; 0 |
| `owners[].ownerTaxable[].suValue` | 100.0% | int(3085085) | 0; 0 |
| `owners[].ownerTaxable[].taxIncrementImprovementValue` | 100.0% | int(3085085) | 0; 0 |
| `owners[].ownerTaxable[].taxIncrementLandValue` | 100.0% | int(3085085) | 0; 0 |
| `owners[].ownerTaxable[].taxIncrementPresent` | 100.0% | int(3085085) | 0; 0 |
| `owners[].ownerTaxable[].taxIncrementZone` | 100.0% | str(3085085) | ;  |
| `owners[].ownerTaxable[].taxableValue` | 100.0% | int(3085085) | 4332066; 4332066 |
| `owners[].ownerTaxable[].taxingUnitID` | 100.0% | int(3085085) | 1001; 1002 |
| `owners[].ownerTaxable[].taxingUnitPct` | 100.0% | float(3085085) | 100.0; 100.0 |
| `owners[].ownerTaxable[].weedTaxableAcres` | 100.0% | float(3085085) | 0.0; 0.0 |
| `owners[].ownerValue` | 100.0% | — |  |
| `owners[].ownerValue[]` | 100.0% | — |  |
| `owners[].ownerValue[].hsGroupPct` | 100.0% | float(486936) | 100.0; 100.0 |
| `owners[].ownerValue[].hsGroupValue` | 100.0% | int(486936) | 0; 0 |
| `owners[].ownerValue[].limitationAllowedIncrease` | 100.0% | int(486936) | 0; 0 |
| `owners[].ownerValue[].limitationBaseYear` | 100.0% | int(486936) | 0; 0 |
| `owners[].ownerValue[].limitationBaseYearDate` | 0.0% | str(13) | 2006-08-14 00:00:00; 2006-11-21 00:00:00 |
| `owners[].ownerValue[].limitationBaseYearOverride` | 100.0% | int(486936) | 0; 0 |
| `owners[].ownerValue[].limitationBaseYearOverrideReason` | 0.0% | str(78) | ;  |
| `owners[].ownerValue[].limitationLastYearHSValue` | 100.0% | int(486936) | 0; 0 |
| `owners[].ownerValue[].limitationLastYearHSValueOverride` | 100.0% | int(486936) | 0; 0 |
| `owners[].ownerValue[].limitationLastYearHSValueOverrideReason` | 92.0% | str(447885) | ;  |
| `owners[].ownerValue[].limitationMaxAllowedIncrease` | 100.0% | int(486936) | 0; 0 |
| `owners[].ownerValue[].limitationNewValue` | 100.0% | int(486936) | 0; 0 |
| `owners[].ownerValue[].limitationNewValueOverride` | 100.0% | int(486936) | 0; 0 |
| `owners[].ownerValue[].limitationNewValueOverrideReason` | 92.0% | str(447872) | ;  |
| `owners[].ownerValue[].ownerAppraisedValue` | 100.0% | int(486936) | 4332066; 62490000 |
| `owners[].ownerValue[].ownerHSImprovementPct` | 100.0% | float(486936) | 1.0; 1.0 |
| `owners[].ownerValue[].ownerHSLandPct` | 100.0% | float(486936) | 1.0; 1.0 |
| `owners[].ownerValue[].ownerImprovementHSValue` | 100.0% | int(486936) | 0; 0 |
| `owners[].ownerValue[].ownerImprovementNHSValue` | 100.0% | int(486936) | 99906; 44022563 |
| `owners[].ownerValue[].ownerImprovementValue` | 100.0% | int(486936) | 99906; 44022563 |
| `owners[].ownerValue[].ownerLandHSValue` | 100.0% | int(486936) | 0; 0 |
| `owners[].ownerValue[].ownerLandNHSValue` | 100.0% | int(486936) | 4232160; 18467437 |
| `owners[].ownerValue[].ownerLandValue` | 100.0% | int(486936) | 4232160; 18467437 |
| `owners[].ownerValue[].ownerMarketValue` | 100.0% | int(486936) | 4332066; 62490000 |
| `owners[].ownerValue[].ownerNetAppraisedValue` | 100.0% | int(486936) | 4332066; 62490000 |
| `owners[].ownerValue[].ownerNewBppValue` | 100.0% | int(486936) | 0; 0 |
| `owners[].ownerValue[].ownerNewImprovementHSValue` | 100.0% | int(486936) | 0; 0 |
| `owners[].ownerValue[].ownerNewImprovementNHSValue` | 100.0% | int(486936) | 0; 0 |
| `owners[].ownerValue[].ownerNewImprovementValue` | 100.0% | int(486936) | 0; 0 |
| `owners[].ownerValue[].ownerNewLandHSValue` | 100.0% | int(486936) | 0; 0 |
| `owners[].ownerValue[].ownerNewLandNHSValue` | 100.0% | int(486936) | 0; 0 |
| `owners[].ownerValue[].ownerNewLandValue` | 100.0% | int(486936) | 0; 0 |
| `owners[].ownerValue[].ownerNewValue` | 100.0% | int(486936) | 0; 0 |
| `owners[].ownerValue[].ownerSULandMktValue` | 100.0% | int(486936) | 0; 0 |
| `owners[].ownerValue[].ownerSUValue` | 100.0% | int(486936) | 0; 0 |
| `owners[].ownerValue[].ownerTaxLimitationValue` | 100.0% | int(486936) | 0; 0 |
| `owners[].ownerValue[].pAccountID` | 100.0% | int(486936) | 8119581; 8119582 |
| `owners[].pAccountID` | 100.0% | int(486936) | 8119581; 8119582 |
| `owners[].pID` | 100.0% | int(486936) | 100008; 100012 |
| `owners[].plus4Code` | 95.7% | str(465871) | 2530; 2618 |
| `owners[].referenceID` | 4.1% | str(20170) | 0; 0 |
| `owners[].regTag` | 0.0% | — |  |
| `owners[].source` | 35.4% | str(172452) | Just Appraised; Just Appraised |
| `owners[].spouseFirstName` | 28.0% | str(136174) | ;  |
| `owners[].spouseLastName` | 27.9% | str(135932) | ;  |

### `pID`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `pID` | 100.0% | int(486859) | 100008; 100012 |

### `pRollCorr`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `pRollCorr` | 100.0% | int(486859) | 0; 0 |

### `pVersion`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `pVersion` | 100.0% | int(486859) | 0; 0 |

### `pYear`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `pYear` | 100.0% | int(486859) | 2025; 2025 |

### `permits`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `permits` | 100.0% | — |  |
| `permits[]` | 100.0% | — |  |
| `permits[].active` | 100.0% | int(1114451) | 0; 0 |
| `permits[].asCode` | 27.0% | str(300688) | COMMERCIAL SQUARE RESUBD.; RADIO/TELEVISION/CELLULAR TELEPHONE COMMUNI |
| `permits[].assignedAppraiser` | 47.7% | str(531816) | DAMON DAUGHTRY; DAWN BRADY |
| `permits[].bathrooms` | 16.1% | float(179721) | 0.0; 0.0 |
| `permits[].bedrooms` | 16.1% | float(179722) | 0.0; 0.0 |
| `permits[].block` | 29.4% | str(328175) | C;  |
| `permits[].builder` | 31.6% | str(352698) | JEFF  BLAKE; SOUTHWEST CONSTRUCTORS, |
| `permits[].builderPhoneNumber` | 20.5% | str(228942) | 785; 836 |
| `permits[].builderPlanNumber` | 9.1% | str(101444) | ;  |
| `permits[].buildingPermitID` | 100.0% | int(1114451) | 904298; 714768 |
| `permits[].buildingPermitPropertiesID` | 100.0% | int(1114451) | 60879; 184283 |
| `permits[].cadStatus` | 68.9% | str(767995) | C; C |
| `permits[].city` | 11.0% | str(122508) | ;  |
| `permits[].dateWorked` | 49.3% | str(549572) | 2016-01-27 00:00:00; 2013-02-11 00:00:00 |
| `permits[].estimateOfValue` | 100.0% | int(1114450) | 14000; 400000 |
| `permits[].floors` | 98.3% | float(1095583) | 1.0; 0.0 |
| `permits[].issueDate` | 86.6% | str(965498) | 2015-11-30 00:00:00; 2012-08-14 00:00:00 |
| `permits[].issuedTo` | 33.1% | str(369327) | JEFF BLAKE; AVERA DEVELOPMENT |
| `permits[].issuer` | 56.6% | str(631342) | 50010; 50010 |
| `permits[].limitDate` | 9.0% | str(100437) | 2000-07-11 00:00:00; 1998-02-05 00:00:00 |
| `permits[].lot` | 30.4% | str(339118) | 4; 4 |
| `permits[].ownerPhoneNumber` | 21.8% | str(242353) | (512)472-6110; ()- |
| `permits[].pID` | 100.0% | int(1114451) | 100008; 100008 |
| `permits[].pcDateComplete` | 0.5% | str(5855) | 1969-12-31 00:00:00; 1969-12-31 12:00:00 |
| `permits[].pctComplete` | 15.0% | float(167443) | 0.0; 0.0 |
| `permits[].permitDateCompleted` | 29.5% | str(329374) | 2013-12-06 00:00:00; 2014-01-02 00:00:00 |
| `permits[].permitNumber` | 99.9% | str(1113718) | 2015-139485 BP; 2012-081921 BP |
| `permits[].permitPropertyCategory` | 94.3% | str(1050783) | C; C |
| `permits[].permitStatus` | 66.4% | str(739697) | C; C |
| `permits[].permitType` | 58.3% | str(650139) | BP; BP |
| `permits[].plat` | 23.2% | str(258712) | 109; 109 |
| `permits[].projectNotes` | 96.9% | str(1079986) | Exterior Remodel to replace Patio Canvas Roofing with Metal Roofing for existing Restaurant; New Construction (2981sf) Retail. |
| `permits[].refImportDate` | 59.0% | str(657385) | 2016-11-21 00:00:00; 2014-01-07 00:00:00 |
| `permits[].refLegacyPermitNumber` | 95.7% | str(1066699) | 2015-139485 BP; 2012-081921 BP |
| `permits[].refPropertyRoll` | 50.7% | str(564706) | 0100030105; 0100030105 |
| `permits[].refSource` | 32.0% | str(356407) | P;  |
| `permits[].requiredBuildingInspection` | 100.0% | int(1114451) | 1; 1 |
| `permits[].requiredElectricalInspection` | 100.0% | int(1114451) | 0; 1 |
| `permits[].requiredMechanicalInspection` | 100.0% | int(1114451) | 0; 0 |
| `permits[].requiredPlumbingInspection` | 100.0% | int(1114451) | 0; 1 |
| `permits[].situsPrefix` | 16.2% | str(180166) | S; S |
| `permits[].situsStreet` | 81.7% | str(910726) | LAMAR; LAMAR |
| `permits[].situsStreetNum` | 80.2% | str(893251) | 1201; 1201 |
| `permits[].situsStreetSuffix` | 42.8% | str(476777) | BLVD; BLVD |
| `permits[].situsUnitNumber` | 18.4% | str(205268) | 3; 3 |
| `permits[].situsUnitType` | 18.2% | str(202624) | Bldg; Bldg |
| `permits[].squareFootArea` | 98.9% | int(1102092) | 0; 0 |
| `permits[].subType` | 21.6% | str(240515) | 50280; 50280 |
| `permits[].units` | 98.3% | float(1095584) | 1.0; 0.0 |

### `propCreateDt`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `propCreateDt` | 40.4% | str(196556) | 1996-02-12 00:00:00; 1993-12-29 00:00:00 |

### `propType`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `propType` | 100.0% | str(486859) | R; R |

### `propertyCharacteristics`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `propertyCharacteristics` | 100.0% | — |  |
| `propertyCharacteristics[]` | 100.0% | — |  |
| `propertyCharacteristics[].altDBA` | 0.3% | str(1650) | HOLLAND PHOTO; TRUE COLOR SALON |
| `propertyCharacteristics[].condoPct` | 2.0% | float(9796) | 0.0; 0.0 |
| `propertyCharacteristics[].condoUnit` | 2.3% | str(11334) | ;  |
| `propertyCharacteristics[].dba` | 12.0% | str(58621) | ODD DUCK; GIBSON FLATS |
| `propertyCharacteristics[].irrigationAcres` | 100.0% | int(486859) | 0; 0 |
| `propertyCharacteristics[].irrigationCapacity` | 100.0% | int(486859) | 0; 0 |
| `propertyCharacteristics[].irrigationGPM` | 100.0% | int(486859) | 0; 0 |
| `propertyCharacteristics[].irrigationWells` | 100.0% | int(486859) | 0; 0 |
| `propertyCharacteristics[].marketArea` | 90.4% | str(440144) | CEN; SC |
| `propertyCharacteristics[].openBusinessDate` | 0.0% | str(104) | 2023-02-15 19:18:28; 2023-11-29 16:19:00 |
| `propertyCharacteristics[].pID` | 100.0% | int(486859) | 100008; 100012 |
| `propertyCharacteristics[].region` | 83.9% | str(408410) | 4; 4 |
| `propertyCharacteristics[].roadAccess` | 0.0% | str(2) | 5115172; 5198053 |
| `propertyCharacteristics[].sicCd` | 8.1% | str(39291) | 4225A; 4225A |
| `propertyCharacteristics[].subType` | 97.6% | str(474966) | COM; COM |
| `propertyCharacteristics[].subset` | 78.4% | str(381621) | 1SC2; 1SC2 |
| `propertyCharacteristics[].topography` | 0.0% | str(3) | 5115172; 5198053 |
| `propertyCharacteristics[].useCd` | 5.5% | str(26950) | 32; 08 |
| `propertyCharacteristics[].utilities` | 0.0% | str(38) | -; 5115172 |
| `propertyCharacteristics[].view` | 0.0% | — |  |
| `propertyCharacteristics[].zoning` | 32.1% | str(156166) | CS; CS |

### `propertyIdentification`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `propertyIdentification` | 100.0% | — |  |
| `propertyIdentification[]` | 100.0% | — |  |
| `propertyIdentification[].geoID` | 92.3% | str(449460) | 0100030105; 0100030109 |
| `propertyIdentification[].mapID` | 89.6% | str(436386) | 010208; 010208 |
| `propertyIdentification[].mapsco` | 0.2% | str(1182) | 614H; 614F |
| `propertyIdentification[].pID` | 100.0% | int(486859) | 100008; 100012 |
| `propertyIdentification[].refID1` | 7.7% | str(37680) | WR024685; WR381808 |
| `propertyIdentification[].refID2` | 100.0% | str(486859) | 01000301050000; 01000301090000 |

### `propertyLegalDescription`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `propertyLegalDescription` | 100.0% | — |  |
| `propertyLegalDescription[]` | 100.0% | — |  |
| `propertyLegalDescription[].additionalLegal` | 2.2% | str(10577) | ; (1.140A IN TRAVIS CO) |
| `propertyLegalDescription[].asCode` | 91.5% | str(445235) | S13671; S03168 |
| `propertyLegalDescription[].block` | 66.1% | str(321767) | A; 18 |
| `propertyLegalDescription[].effectiveSizeAcres` | 66.4% | float(323382) | 0.5399; 2.3553 |
| `propertyLegalDescription[].legalAcreage` | 78.2% | float(380598) | 0.5399; 2.3553 |
| `propertyLegalDescription[].legalDescription` | 100.0% | str(486859) | LOT 1-4 TEMPLER LOTS; LOT 1A COMMERCIAL SQUARE RESUB & LOTS 5-7 OF TEMPLER LOTS |
| `propertyLegalDescription[].lot` | 85.4% | str(415862) | 1-4; 1A, 5-7 |
| `propertyLegalDescription[].mhSpaceNum` | 2.1% | str(10139) | LOT;  |
| `propertyLegalDescription[].pID` | 100.0% | int(486859) | 100008; 100012 |
| `propertyLegalDescription[].tract` | 6.1% | str(29559) | ;  |

### `propertyProfile`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `propertyProfile` | 100.0% | — |  |
| `propertyProfile[]` | 100.0% | — |  |
| `propertyProfile[].activeFieldInspection` | 100.0% | int(486859) | 0; 0 |
| `propertyProfile[].activePermit` | 100.0% | int(486859) | 0; 0 |
| `propertyProfile[].bppStateCd` | 100.0% | str(486859) | ;  |
| `propertyProfile[].centralAirHeat` | 100.0% | int(486859) | 0; 0 |
| `propertyProfile[].cityTaxingUnitCode` | 100.0% | str(486859) | 02; 02 |
| `propertyProfile[].cityTaxingUnitID` | 100.0% | int(486859) | 1002; 1002 |
| `propertyProfile[].cityTaxingUnitName` | 100.0% | str(486859) | CITY OF AUSTIN; CITY OF AUSTIN |
| `propertyProfile[].exemptions` | 100.0% | str(486859) | ;  |
| `propertyProfile[].fieldInspectionDt` | 16.3% | str(79388) | 2024-10-04 15:37:41; 2024-10-04 15:33:33 |
| `propertyProfile[].fieldInspectionSource` | 100.0% | str(486859) | P; P |
| `propertyProfile[].imprvActualYearBuilt` | 100.0% | int(486859) | 2013; 2013 |
| `propertyProfile[].imprvAge` | 100.0% | int(486859) | 0; 0 |
| `propertyProfile[].imprvClass` | 100.0% | str(486859) | C; WV |
| `propertyProfile[].imprvClasses` | 100.0% | str(486859) | AA,C; B,SO,WV |
| `propertyProfile[].imprvCondition` | 100.0% | str(486859) | *; G |
| `propertyProfile[].imprvDeprec` | 100.0% | float(486859) | 100.0; 95.0 |
| `propertyProfile[].imprvDeprecGood` | 100.0% | float(486859) | 100.0; 95.0 |
| `propertyProfile[].imprvEconomicAdj` | 100.0% | float(486859) | 10.0; 100.0 |
| `propertyProfile[].imprvEffYearBuilt` | 100.0% | int(486859) | 2013; 2013 |
| `propertyProfile[].imprvFactor` | 100.0% | float(486859) | 10.0; 100.0 |
| `propertyProfile[].imprvFunctionalAdj` | 100.0% | float(486859) | 100.0; 100.0 |
| `propertyProfile[].imprvMABaseUnitPrice` | 100.0% | float(486859) | 252.87; 183.16 |
| `propertyProfile[].imprvMAUnitPrice` | 100.0% | float(486859) | 268.04; 203.86 |
| `propertyProfile[].imprvMainArea` | 100.0% | float(486859) | 2986.0; 162757.0 |
| `propertyProfile[].imprvOnly` | 100.0% | int(486859) | 0; 0 |
| `propertyProfile[].imprvPctComplete` | 100.0% | float(486859) | 100.0; 100.0 |
| `propertyProfile[].imprvPhysicalAdj` | 100.0% | float(486859) | 100.0; 100.0 |
| `propertyProfile[].imprvQuality` | 100.0% | str(486859) | 5; 6 |
| `propertyProfile[].imprvStateCd` | 100.0% | str(486859) | F1; B1 |
| `propertyProfile[].imprvStories` | 100.0% | int(486859) | 1; 1 |
| `propertyProfile[].imprvStyle` | 100.0% | str(486859) | ;  |
| `propertyProfile[].imprvTotalArea` | 100.0% | float(486859) | 23776.0; 575107.0 |
| `propertyProfile[].imprvType` | 100.0% | str(486859) | 32; 08 |
| `propertyProfile[].imprvUnits` | 100.0% | int(486859) | 0; 0 |
| `propertyProfile[].landClass` | 100.0% | str(486859) | ;  |
| `propertyProfile[].landClasses` | 100.0% | str(486859) | ;  |
| `propertyProfile[].landFactor` | 100.0% | float(486859) | 100.0; 100.0 |
| `propertyProfile[].landHomesitePct` | 100.0% | float(486859) | 0.0; 0.0 |
| `propertyProfile[].landInfluence` | 100.0% | str(486859) | ;  |
| `propertyProfile[].landMktClass` | 100.0% | str(486859) | SPECIAL SF; SPECIAL SF |
| `propertyProfile[].landMktEconomicAdj` | 100.0% | float(486859) | 100.0; 100.0 |
| `propertyProfile[].landMktFunctionalAdj` | 100.0% | float(486859) | 100.0; 100.0 |
| `propertyProfile[].landMktMethod` | 100.0% | str(486859) | SF; SF |
| `propertyProfile[].landMktModel` | 100.0% | int(486859) | 52; 52 |
| `propertyProfile[].landMktModelUnitPrice` | 100.0% | float(486859) | 0.0; 0.0 |
| `propertyProfile[].landMktPhysicalAdj` | 100.0% | float(486859) | 100.0; 100.0 |
| `propertyProfile[].landMktSpecialUnitPrice` | 100.0% | float(486859) | 180.0; 180.0 |
| `propertyProfile[].landMktUnitPriceSelection` | 100.0% | str(486859) | S; S |
| `propertyProfile[].landOnly` | 100.0% | int(486859) | 0; 0 |
| `propertyProfile[].landSizeAcres` | 100.0% | float(486859) | 0.5398; 2.3553 |
| `propertyProfile[].landSizeDepthLeft` | 100.0% | float(486859) | 0.0; 0.0 |
| `propertyProfile[].landSizeDepthRight` | 100.0% | float(486859) | 0.0; 0.0 |
| `propertyProfile[].landSizeEffectiveDepth` | 100.0% | float(486859) | 0.0; 0.0 |
| `propertyProfile[].landSizeEffectiveFront` | 100.0% | float(486859) | 0.0; 0.0 |
| `propertyProfile[].landSizeLot` | 100.0% | int(486859) | 1; 1 |
| `propertyProfile[].landSizeSqft` | 100.0% | float(486859) | 23512.0; 102596.87 |
| `propertyProfile[].landSizeUseableAcres` | 100.0% | float(486859) | 0.5398; 2.3553 |
| `propertyProfile[].landSizeUseableSqft` | 100.0% | float(486859) | 23512.0; 102596.87 |
| `propertyProfile[].landSizeWidthBack` | 100.0% | float(486859) | 0.0; 0.0 |
| `propertyProfile[].landSizeWidthFront` | 100.0% | float(486859) | 0.0; 0.0 |
| `propertyProfile[].landStateCd` | 100.0% | str(486859) | F1; B1 |
| `propertyProfile[].landTotalAcres` | 100.0% | float(486859) | 0.5398; 2.3553 |
| `propertyProfile[].landTotalLots` | 100.0% | int(486859) | 1; 1 |
| `propertyProfile[].landTotalSqft` | 100.0% | float(486859) | 23512.0; 102596.87 |
| `propertyProfile[].landTotalUseableAcres` | 100.0% | float(486859) | 0.5398; 2.3553 |
| `propertyProfile[].landTotalUseableSqft` | 100.0% | float(486859) | 23512.0; 102596.87 |
| `propertyProfile[].landType` | 100.0% | str(486859) | LAND; LAND |
| `propertyProfile[].mineralStateCd` | 100.0% | str(486859) | ;  |
| `propertyProfile[].mobileHomeNumbers` | 0.0% | — |  |
| `propertyProfile[].pID` | 100.0% | int(486859) | 100008; 100012 |
| `propertyProfile[].schoolTaxingUnitCode` | 100.0% | str(486859) | 01; 01 |
| `propertyProfile[].schoolTaxingUnitID` | 100.0% | int(486859) | 1001; 1001 |
| `propertyProfile[].schoolTaxingUnitName` | 100.0% | str(486859) | AUSTIN ISD; AUSTIN ISD |
| `propertyProfile[].stateCd` | 100.0% | str(486859) | F1; B1 |
| `propertyProfile[].stateCodes` | 100.0% | str(486859) | F1; B1,F1 |
| `propertyProfile[].taxingUnits` | 100.0% | str(486859) | 01,02,03,0A,2J,68; 01,02,03,0A,2J,68 |

### `reactivateDt`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `reactivateDt` | 0.1% | str(457) | 2024-03-12 09:27:23; 2023-02-16 11:39:26 |

### `reactivateNotes`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `reactivateNotes` | 0.1% | str(457) | DELE IN ERROR FOR 2024; MERGED IN ERROR FOR 2023 |

### `reactivateReason`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `reactivateReason` | 0.1% | str(457) | DEL_ERROR; DEL_ERROR |

### `rollCorrCode`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `rollCorrCode` | 53.6% | str(260849) | EEXC; EEXC |

### `rollCorrReason`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `rollCorrReason` | 53.6% | str(260849) | UPDATE HS EXEMPTION AMOUNT TO $140,000 AND OV65, OV65S, DP AND DPS EXEMPTION TO $60,000; UPDATE HS EXEMPTION AMOUNT TO $140,000 AND OV65, OV65S, DP AN |

### `sales`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `sales` | 100.0% | — |  |
| `sales[]` | 100.0% | — |  |
| `sales[].buyerLine` | 91.9% | str(255652) | BRIZENDINE CHARLES DAVID; AVERA DEVELOPMENT L L C |
| `sales[].charAnnualIncome` | 19.1% | int(53071) | 0; 0 |
| `sales[].charDBA` | 6.2% | str(17342) | TOWNHOLLOW APTS; 0 |
| `sales[].charDaysOnMarket` | 6.3% | int(17483) | 0; 0 |
| `sales[].charImpClass` | 20.1% | str(55794) | C; WW |
| `sales[].charImpLivingArea` | 29.8% | int(82793) | 6341; 49585 |
| `sales[].charImpNumUnits` | 6.3% | int(17454) | 3; 0 |
| `sales[].charImpPctComplete` | 6.3% | float(17454) | 100.0; 0.0 |
| `sales[].charImpQuality` | 0.0% | str(84) | ;  |
| `sales[].charImpStateCd` | 25.0% | str(69395) | F1; F1 |
| `sales[].charImpType` | 20.2% | str(56084) | 53; 07 |
| `sales[].charImpUnitPrice` | 29.8% | float(82792) | 66.95; 68.95 |
| `sales[].charImpYearBuilt` | 29.8% | int(82810) | 1965; 1982 |
| `sales[].charLandSizeAcres` | 29.5% | float(82176) | 1.0734; 1.73 |
| `sales[].charLandSizeEffectiveDepth` | 29.5% | float(82097) | 0.0; 0.0 |
| `sales[].charLandSizeEffectiveFront` | 29.5% | float(82097) | 0.0; 0.0 |
| `sales[].charLandSizeLot` | 6.9% | int(19171) | 0; 1 |
| `sales[].charLandSizeSqft` | 28.9% | float(80322) | 46757.0; 75358.8 |
| `sales[].charLandType` | 24.9% | str(69273) | LAND; LAND |
| `sales[].charLandUnitPrice` | 100.0% | float(278063) | 0.0; 7.0 |
| `sales[].charListingDate` | 3.9% | str(10726) | 2024-11-12 00:00:00; 2024-03-27 00:00:00 |
| `sales[].charListingPrice` | 17.5% | int(48788) | 0; 0 |
| `sales[].charLocationCity` | 24.5% | int(68096) | 1002; 1002 |
| `sales[].charLocationMarketArea` | 0.0% | str(114) | ;  |
| `sales[].charLocationPropertyCategory` | 0.0% | — |  |
| `sales[].charLocationPropertyUse` | 0.0% | str(84) | ;  |
| `sales[].charLocationRegion` | 0.0% | — |  |
| `sales[].charLocationSchool` | 25.0% | int(69613) | 1001; 1001 |
| `sales[].charLocationSubdivision` | 0.0% | str(82) | MOUNTAIN CREEK LAKES SEC 1; FOREST AT WESTLAKE THE |
| `sales[].charLocationSubset` | 20.1% | str(55785) | 4; 4 |
| `sales[].charLocationZoning` | 0.1% | str(203) | CS; CS |
| `sales[].charMonthlyIncome` | 19.1% | int(53071) | 0; 0 |
| `sales[].comparableUseSaleData` | 100.0% | int(278063) | 1; 0 |
| `sales[].confidentialCode` | 5.7% | str(15910) | Q; Q |
| `sales[].confidentialSale` | 100.0% | int(278063) | 0; 0 |
| `sales[].deedID` | 93.9% | int(261075) | 25; 1642721 |
| `sales[].financeCode` | 52.9% | str(147191) | $; C |
| `sales[].financeComment` | 0.0% | str(123) | AMOUNT DOWN WAS CALCULATED, OWNER STATED 20%; PER OWNER CASH/OTHER FINANCE |
| `sales[].financeLoan1AmtDown` | 97.8% | int(272000) | 0; 0 |
| `sales[].financeLoan1AmtFinanced` | 91.6% | int(254731) | 46700; 1145000 |
| `sales[].financeLoan1FinanceYears` | 97.8% | int(272000) | 0; 0 |
| `sales[].financeLoan1InterestRate` | 97.8% | float(272000) | 0.0; 0.0 |
| `sales[].financeLoan2AmtDown` | 100.0% | int(278063) | 0; 0 |
| `sales[].financeLoan2AmtFinanced` | 22.5% | int(62677) | 1250000; 0 |
| `sales[].financeLoan2FinanceYears` | 28.7% | int(79940) | 0; 0 |
| `sales[].financeLoan2InterestRate` | 28.7% | float(79940) | 0.0; 0.0 |
| `sales[].frozenCharacteristics` | 100.0% | int(278063) | 0; 1 |
| `sales[].landOnlySale` | 100.0% | int(278063) | 0; 0 |
| `sales[].multiProperty` | 100.0% | int(278063) | 0; 0 |
| `sales[].notes` | 63.1% | str(175537) | PER CONFIRMED PUBLICATION
Imported Sale Confirmation Details: [confirmed by - ] [confirmation date - 1993-07-07] [confirmation source - PUBLICATION] [ |
| `sales[].outlier` | 100.0% | int(278063) | 0; 0 |
| `sales[].pID` | 100.0% | int(278063) | 100008; 100012 |
| `sales[].properties` | 100.0% | str(278063) | [100008]; [100012]  [json-string-decoded x278063] |
| `sales[].properties.→json` | 100.0% | — |  |
| `sales[].properties.→json[]` | 100.0% | int(312456) | 100008; 100012 |
| `sales[].realtor` | 1.9% | str(5160) | S3; S3 |
| `sales[].reportIncludeReportNoCalculation` | 100.0% | int(278063) | 0; 0 |
| `sales[].reportIncludeReportNoCalculationReason` | 0.1% | str(170) | NEW CONSTRUCTION AFTER SALE; per letter not arms length |
| `sales[].reportSupressCode` | 0.0% | — |  |
| `sales[].reportSupressFromReport` | 100.0% | int(278063) | 0; 0 |
| `sales[].reportSupressFromReportReason` | 2.4% | str(6718) | System; NAME CHANGE ONLY |
| `sales[].saleAdjustmentAmount` | 100.0% | int(278063) | 0; 0 |
| `sales[].saleAdjustmentPct` | 100.0% | float(278063) | 100.0; 100.0 |
| `sales[].saleAdjustmentReason` | 6.2% | str(17216) | ;  |
| `sales[].saleAdjustmentReasonCode` | 6.2% | str(17179) | ;  |
| `sales[].saleAdjustmentType` | 100.0% | str(278063) | P; P |
| `sales[].saleDt` | 100.0% | str(278060) | 1993-07-07 00:00:00; 2006-04-28 00:00:00 |
| `sales[].saleExported` | 100.0% | int(278063) | 0; 1 |
| `sales[].saleID` | 100.0% | int(278063) | 446076; 254552 |
| `sales[].salePrice` | 100.0% | int(278063) | 80001; 2394000 |
| `sales[].salePriceAdjusted` | 100.0% | int(278063) | 80001; 2394000 |
| `sales[].saleQualify` | 6.2% | str(17179) | ;  |
| `sales[].saleRatioType` | 7.4% | str(20604) | 08;  |
| `sales[].saleType` | 100.0% | str(277959) | S; VL |
| `sales[].sellerLine` | 89.5% | str(248869) | FEDERAL DEPOSIT INSURANCE CORP; HOLLAND PETER HENRY & MARGARET |
| `sales[].sourceOfSale` | 63.6% | str(176741) | PUBLICATION; PUBLICATION |

### `sitProperty`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `sitProperty` | 100.0% | int(486859) | 0; 0 |

### `situses`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `situses` | 100.0% | — |  |
| `situses[]` | 100.0% | — |  |
| `situses[].city` | 49.0% | str(241745) | ; AUSTIN |
| `situses[].country` | 9.3% | str(45828) | ;  |
| `situses[].international` | 9.3% | int(45828) | 0; 0 |
| `situses[].pID` | 100.0% | int(493410) | 100008; 100012 |
| `situses[].primarySitus` | 100.0% | int(493410) | 1; 1 |
| `situses[].situsAddressID` | 100.0% | int(493410) | 7912250; 7912251 |
| `situses[].state` | 96.8% | str(477717) | TX; TX |
| `situses[].streetName` | 100.0% | str(493287) | LAMAR; LAMAR |
| `situses[].streetNum` | 95.7% | str(472143) | 1201; 1219 |
| `situses[].streetPrefix` | 17.8% | str(87853) | S; S |
| `situses[].streetSecondary` | 22.9% | str(113227) | ;  |
| `situses[].streetSuffix` | 94.0% | str(463829) | BLVD; BLVD |
| `situses[].zip` | 96.7% | str(477294) | 78704; 78704 |

### `smartgroups`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `smartgroups` | 100.0% | — |  |
| `smartgroups[]` | 100.0% | — |  |
| `smartgroups[].applicationAgreementDate` | 0.2% | str(9) | 2020-06-03 00:00:00; 2020-06-03 00:00:00 |
| `smartgroups[].applicationApplicantName` | 0.2% | str(9) | Colorado River Project; Colorado River Project |
| `smartgroups[].applicationCounty` | 0.2% | str(9) | TRAVIS; TRAVIS |
| `smartgroups[].applicationFirstYearQualifying` | 0.2% | int(9) | 2021; 2021 |
| `smartgroups[].applicationNumber` | 0.0% | — |  |
| `smartgroups[].applicationProjectName` | 0.2% | str(9) | Colorado River Project; Colorado River Project |
| `smartgroups[].groupComment` | 100.0% | str(5771) | MAIN PID IS 100051; Legacy Homestead Group |
| `smartgroups[].groupID` | 100.0% | int(5771) | 25500; 26530 |
| `smartgroups[].groupName` | 100.0% | str(5771) | HS GROUP; Legacy Group 98 |
| `smartgroups[].groupType` | 100.0% | str(5771) | HS; HS |
| `smartgroups[].groupYr` | 100.0% | int(5771) | 2025; 2025 |
| `smartgroups[].limitationAmount` | 58.2% | float(3361) | 0.0; 0.0 |
| `smartgroups[].limitationFirstYear` | 0.2% | int(9) | 2022; 2022 |
| `smartgroups[].pID` | 100.0% | int(5771) | 100051; 100111 |
| `smartgroups[].properties` | 100.0% | str(5771) | [100043, 100051]; [100111, 100112]  [json-string-decoded x5771] |
| `smartgroups[].properties.→json` | 100.0% | — |  |
| `smartgroups[].properties.→json[]` | 100.0% | int(18084) | 100043; 100051 |

### `tags`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `tags` | 100.0% | — |  |
| `tags[]` | 100.0% | — |  |
| `tags[].Codefied` | 100.0% | str(783242) | CODIFIED; CODIFIED |
| `tags[].notification` | 3.4% | str(26795) | 1; 1 |
| `tags[].pID` | 100.0% | int(783242) | 100008; 100008 |
| `tags[].pYear` | 100.0% | int(783242) | 2025; 2025 |
| `tags[].tag` | 100.0% | str(783242) | INTERIM USE ; INTERIM USE  |
| `tags[].tagID` | 100.0% | int(783242) | 2916817; 2916817 |
| `tags[].tagYear` | 100.0% | int(783242) | 2025; 2025 |

### `taxingUnitPercentCalculation`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `taxingUnitPercentCalculation` | 100.0% | str(486859) | T; T |

### `taxingUnitPercentCalculationComment`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `taxingUnitPercentCalculationComment` | 0.0% | str(168) | ;  |

### `taxingUnitSplitBoundaryLines`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `taxingUnitSplitBoundaryLines` | 100.0% | int(486859) | 0; 0 |

### `taxingunits`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `taxingunits` | 100.0% | — |  |
| `taxingunits[]` | 100.0% | — |  |
| `taxingunits[].jurisdictionPct` | 100.0% | float(3084561) | 100.0; 100.0 |
| `taxingunits[].pID` | 100.0% | int(3084561) | 100008; 100008 |
| `taxingunits[].segBppPct` | 100.0% | float(3084561) | 100.0; 100.0 |
| `taxingunits[].segImprovementHSPct` | 100.0% | float(3084561) | 100.0; 100.0 |
| `taxingunits[].segImprovementNHSPct` | 100.0% | float(3084561) | 100.0; 100.0 |
| `taxingunits[].segLandHSPct` | 100.0% | float(3084561) | 100.0; 100.0 |
| `taxingunits[].segLandNHSPct` | 100.0% | float(3084561) | 100.0; 100.0 |
| `taxingunits[].segLandSUMktPct` | 100.0% | float(3084561) | 100.0; 100.0 |
| `taxingunits[].segLandSUPct` | 100.0% | float(3084561) | 100.0; 100.0 |
| `taxingunits[].taxingUnitCode` | 100.0% | str(3084561) | 01; 02 |
| `taxingunits[].taxingUnitID` | 100.0% | int(3084561) | 1001; 1002 |
| `taxingunits[].taxingUnitName` | 100.0% | str(3084561) | AUSTIN ISD; CITY OF AUSTIN |
| `taxingunits[].taxingUnitNum` | 100.0% | str(3084561) | 227-901-02; 227-104-03 |
| `taxingunits[].taxingUnitType` | 100.0% | str(3084561) | School; City |

### `valuations`

| Path | Population % | Type(s) | Examples |
|---|---|---|---|
| `valuations` | 100.0% | — |  |
| `valuations[]` | 100.0% | — |  |
| `valuations[].amtAllocation` | 100.0% | float(486858) | 0.0; 0.0 |
| `valuations[].assocID` | 100.0% | int(486858) | 20335045; 20531463 |
| `valuations[].bppNewValue` | 100.0% | int(486858) | 0; 0 |
| `valuations[].details` | 100.0% | — |  |
| `valuations[].details.cost-local` | 100.0% | — |  |
| `valuations[].details.cost-local.age` | 100.0% | int(275728) | 0; 0 |
| `valuations[].details.cost-local.effYearBuilt` | 100.0% | int(275728) | 0; 0 |
| `valuations[].details.cost-local.grossLivingArea` | 100.0% | int(275728) | 0; 0 |
| `valuations[].details.cost-local.improvementHSValue` | 100.0% | int(275728) | 0; 0 |
| `valuations[].details.cost-local.improvementNHSValue` | 100.0% | int(275728) | 110310; 0 |
| `valuations[].details.cost-local.improvementNewHSValue` | 100.0% | int(275728) | 0; 0 |
| `valuations[].details.cost-local.improvementNewNHSValue` | 100.0% | int(275728) | 0; 0 |
| `valuations[].details.cost-local.improvementNewValue` | 100.0% | int(275728) | 0; 0 |
| `valuations[].details.cost-local.improvements` | 100.0% | — |  |
| `valuations[].details.cost-local.improvements[]` | 100.0% | — |  |
| `valuations[].details.cost-local.improvements[].actualYearBuilt` | 98.9% | int(435465) | 1984; 2013 |
| `valuations[].details.cost-local.improvements[].adjustedValue` | 100.0% | int(251356) | 110310; 135072 |
| `valuations[].details.cost-local.improvements[].adjustments` | 100.0% | — |  |
| `valuations[].details.cost-local.improvements[].adjustments[]` | 100.0% | — |  |
| `valuations[].details.cost-local.improvements[].adjustments[].adjustAmount` | 100.0% | str(3692) | 0; 0 |
| `valuations[].details.cost-local.improvements[].adjustments[].adjustDescription` | 100.0% | str(9720) | MKT AREA; MKT AREA |
| `valuations[].details.cost-local.improvements[].adjustments[].adjustPct` | 100.0% | float(9720) | 150.0; 132.0 |
| `valuations[].details.cost-local.improvements[].adjustments[].adjustResidualPct` | 100.0% | float(9720) | 0.0; 0.0 |
| `valuations[].details.cost-local.improvements[].adjustments[].adjustType` | 100.0% | str(9720) | user defined percent; user defined percent |
| `valuations[].details.cost-local.improvements[].adjustments[].adjustYrTerm` | 100.0% | int(9720) | 0; 0 |
| `valuations[].details.cost-local.improvements[].adjustments[].modelAdjustID` | 100.0% | int(9720) | 2767; 2767 |
| `valuations[].details.cost-local.improvements[].adjustments[].pAdjustmentID` | 100.0% | int(9720) | 119226; 116973 |
| `valuations[].details.cost-local.improvements[].adjustments[].pImprovementID` | 100.0% | int(9720) | 6960821; 6960823 |
| `valuations[].details.cost-local.improvements[].adjustments[].segmentType` | 100.0% | str(9720) | improvement; improvement |
| `valuations[].details.cost-local.improvements[].age` | 100.0% | int(440441) | 0; 0 |
| `valuations[].details.cost-local.improvements[].applyImprvAreaModifier` | 100.0% | int(440441) | 1; 1 |
| `valuations[].details.cost-local.improvements[].class` | 100.0% | str(440415) | AA; C |
| `valuations[].details.cost-local.improvements[].costLocalValue` | 100.0% | int(251356) | 110310; 102327 |
| `valuations[].details.cost-local.improvements[].deprec` | 100.0% | float(440441) | 100.0; 100.0 |
| `valuations[].details.cost-local.improvements[].deprecGood` | 100.0% | float(440441) | 0.0; 0.0 |
| `valuations[].details.cost-local.improvements[].details` | 100.0% | — |  |
| `valuations[].details.cost-local.improvements[].details[]` | 100.0% | — |  |
| `valuations[].details.cost-local.improvements[].details[].actualYearBuilt` | 3.9% | int(126064) | 2013; 2018 |
| `valuations[].details.cost-local.improvements[].details[].adjOverride` | 100.0% | int(3262366) | 0; 0 |
| `valuations[].details.cost-local.improvements[].details[].adjustedValue` | 100.0% | int(1748734) | 53781; 30658 |
| `valuations[].details.cost-local.improvements[].details[].adjustments` | 100.0% | — |  |
| `valuations[].details.cost-local.improvements[].details[].adjustments[]` | 100.0% | — |  |
| `valuations[].details.cost-local.improvements[].details[].adjustments[].adjustAmount` | 100.0% | str(24) | 0; 0 |
| `valuations[].details.cost-local.improvements[].details[].adjustments[].adjustDescription` | 100.0% | str(59) | Market Percentage; Market Percentage |
| `valuations[].details.cost-local.improvements[].details[].adjustments[].adjustPct` | 100.0% | float(59) | 0.0; 0.0 |
| `valuations[].details.cost-local.improvements[].details[].adjustments[].adjustResidualPct` | 100.0% | float(59) | 0.0; 0.0 |
| `valuations[].details.cost-local.improvements[].details[].adjustments[].adjustType` | 100.0% | str(59) | user defined percent; user defined percent |
| `valuations[].details.cost-local.improvements[].details[].adjustments[].adjustYrTerm` | 100.0% | int(59) | 0; 0 |
| `valuations[].details.cost-local.improvements[].details[].adjustments[].modelAdjustID` | 100.0% | int(59) | 2766; 2766 |
| `valuations[].details.cost-local.improvements[].details[].adjustments[].pAdjustmentID` | 100.0% | int(59) | 2521; 2522 |
| `valuations[].details.cost-local.improvements[].details[].adjustments[].pDetailID` | 100.0% | int(59) | 56219123; 56219124 |
| `valuations[].details.cost-local.improvements[].details[].adjustments[].segmentType` | 100.0% | str(59) | improvement; improvement |
| `valuations[].details.cost-local.improvements[].details[].age` | 100.0% | int(3262366) | 2; 2 |
| `valuations[].details.cost-local.improvements[].details[].arcs` | 100.0% | int(3262366) | 0; 0 |
| `valuations[].details.cost-local.improvements[].details[].area` | 100.0% | float(3262366) | 17100.0; 2986.0 |
| `valuations[].details.cost-local.improvements[].details[].areaSource` | 100.0% | str(3262366) | M; S |
| `valuations[].details.cost-local.improvements[].details[].characteristicOverride` | 100.0% | int(3262366) | 1; 0 |
| `valuations[].details.cost-local.improvements[].details[].class` | 7.6% | str(249088) | AA; A |
| `valuations[].details.cost-local.improvements[].details[].conditionOverride` | 100.0% | int(3262366) | 0; 0 |
| `valuations[].details.cost-local.improvements[].details[].deprec` | 100.0% | float(3262366) | 0.0; 100.0 |
| `valuations[].details.cost-local.improvements[].details[].deprecGood` | 100.0% | float(3262366) | 0.0; 100.0 |
| `valuations[].details.cost-local.improvements[].details[].deprecNote` | 2.0% | str(63815) | ;  |
| `valuations[].details.cost-local.improvements[].details[].dimensionLength` | 100.0% | float(3262366) | 0.0; 0.0 |
| `valuations[].details.cost-local.improvements[].details[].dimensionWidth` | 100.0% | float(3262366) | 0.0; 0.0 |
| `valuations[].details.cost-local.improvements[].details[].economicAdj` | 100.0% | float(3262366) | 20.0; 100.0 |
| `valuations[].details.cost-local.improvements[].details[].economicNote` | 0.5% | str(15438) | INCOME DOES NOT SUPPORT LAND, INTERIM CONDITION - CFH 12.13.23; INCOME DOES NOT SUPPORT LAND, INTERIM CONDITION - CFH 12.13.23 |
| `valuations[].details.cost-local.improvements[].details[].effYearBuilt` | 3.9% | int(126328) | 2013; 2018 |
| `valuations[].details.cost-local.improvements[].details[].exteriorWall` | 0.4% | str(14415) | ;  |
| `valuations[].details.cost-local.improvements[].details[].features` | 100.0% | — |  |
| `valuations[].details.cost-local.improvements[].details[].features[]` | 100.0% | — |  |
| `valuations[].details.cost-local.improvements[].details[].features[].featureCode` | 100.0% | str(3498897) | 1ST; A |
| `valuations[].details.cost-local.improvements[].details[].features[].featureCodeID` | 100.0% | int(3498897) | 4748; 4776 |
| `valuations[].details.cost-local.improvements[].details[].features[].featureName` | 100.0% | str(3498897) | Floor Factor; Grade Factor |
| `valuations[].details.cost-local.improvements[].details[].features[].featurePct` | 100.0% | float(3498897) | 0.0; 0.0 |
| `valuations[].details.cost-local.improvements[].details[].features[].featurePresent` | 100.0% | int(3498897) | 1; 1 |
| `valuations[].details.cost-local.improvements[].details[].features[].featureType` | 100.0% | str(3498897) | present; present |
| `valuations[].details.cost-local.improvements[].details[].features[].featureValue` | 100.0% | float(3498897) | 1.0; 1.0 |
| `valuations[].details.cost-local.improvements[].details[].features[].modelFeatureID` | 100.0% | int(3498897) | 1653; 1652 |
| `valuations[].details.cost-local.improvements[].details[].features[].modelID` | 100.0% | int(3498897) | 10508; 10508 |
| `valuations[].details.cost-local.improvements[].details[].features[].pDetailID` | 100.0% | int(3498897) | 58839290; 58839290 |
| `valuations[].details.cost-local.improvements[].details[].features[].pFeatureID` | 100.0% | int(3498897) | 51208036; 51209219 |
| `valuations[].details.cost-local.improvements[].details[].features[].sortFeatureCode` | 100.0% | str(3498897) | 1ST; A |
| `valuations[].details.cost-local.improvements[].details[].features[].sortFeatureName` | 100.0% | str(3498897) | Floor Factor; Grade Factor |
| `valuations[].details.cost-local.improvements[].details[].finishoutPct` | 100.0% | float(3262366) | 100.0; 100.0 |
| `valuations[].details.cost-local.improvements[].details[].flatValue` | 100.0% | int(1748734) | 39005; 14842 |
| `valuations[].details.cost-local.improvements[].details[].functionalAdj` | 100.0% | float(3262366) | 100.0; 30.0 |
| `valuations[].details.cost-local.improvements[].details[].functionalNote` | 0.6% | str(18195) | ;  |
| `valuations[].details.cost-local.improvements[].details[].height` | 2.0% | float(64381) | 0.0; 0.0 |
| `valuations[].details.cost-local.improvements[].details[].improvementDetailComment` | 1.9% | str(63401) | ;  |
| `valuations[].details.cost-local.improvements[].details[].improvementDetailValue` | 100.0% | int(1748734) | 53781; 30658 |
| `valuations[].details.cost-local.improvements[].details[].imprvCondition` | 3.9% | str(125908) | G; A |
| `valuations[].details.cost-local.improvements[].details[].imprvDetailModifier` | 100.0% | float(3262366) | 0.0; 0.1 |
| `valuations[].details.cost-local.improvements[].details[].imprvDetailType` | 100.0% | str(3262359) | 551; 1ST |
| `valuations[].details.cost-local.improvements[].details[].length` | 2.3% | float(76352) | 0.0; 0.0 |
| `valuations[].details.cost-local.improvements[].details[].loadingDockHeight` | 100.0% | float(3262366) | 0.0; 0.0 |
| `valuations[].details.cost-local.improvements[].details[].manualArea` | 99.9% | float(3257428) | 17100.0; 0.0 |
| `valuations[].details.cost-local.improvements[].details[].manualPerimeter` | 0.0% | int(135) | 9843; 385 |
| `valuations[].details.cost-local.improvements[].details[].newValue` | 100.0% | int(1748734) | 0; 0 |
| `valuations[].details.cost-local.improvements[].details[].newValueIndicator` | 100.0% | int(3262366) | 0; 0 |
| `valuations[].details.cost-local.improvements[].details[].newValueOverrideIndicator` | 100.0% | int(3262366) | 0; 0 |
| `valuations[].details.cost-local.improvements[].details[].nodes` | 100.0% | int(3262366) | 0; 0 |
| `valuations[].details.cost-local.improvements[].details[].overrideDeprec` | 100.0% | int(3262366) | 0; 0 |
| `valuations[].details.cost-local.improvements[].details[].overridePricingModel` | 100.0% | int(3262366) | 1; 0 |
| `valuations[].details.cost-local.improvements[].details[].pDetailID` | 100.0% | int(3262366) | 58839289; 58839290 |
| `valuations[].details.cost-local.improvements[].details[].pImprovementID` | 100.0% | int(3262366) | 6960812; 6960813 |
| `valuations[].details.cost-local.improvements[].details[].pctComplete` | 100.0% | float(3262366) | 100.0; 100.0 |
| `valuations[].details.cost-local.improvements[].details[].pctCompleteNote` | 1.1% | str(36535) | Set to 1% $1 for 15, see images, 02/12/2015, MAK //; Set to 1% $1 for 15, see images, 02/12/2015, MAK // |
| `valuations[].details.cost-local.improvements[].details[].perimeter` | 99.9% | int(3259861) | 0; 0 |
| `valuations[].details.cost-local.improvements[].details[].perimeterSource` | 17.3% | str(563246) | S; S |
| `valuations[].details.cost-local.improvements[].details[].physicalAdj` | 100.0% | float(3262366) | 100.0; 100.0 |
| `valuations[].details.cost-local.improvements[].details[].physicalNote` | 0.6% | str(18924) | CRACKS IN WALL, FOUNDATION, SIDING DMG; 1% OBS FOR STIGMA |
| `valuations[].details.cost-local.improvements[].details[].pricingMethod` | 100.0% | str(3262366) | M; M |
| `valuations[].details.cost-local.improvements[].details[].pricingModel` | 10.5% | int(341886) | 10472; 10471 |
| `valuations[].details.cost-local.improvements[].details[].pricingModelNote` | 100.0% | str(3262366) | ;  |
| `valuations[].details.cost-local.improvements[].details[].pricingUnitPrice` | 100.0% | float(1748734) | 179.15; 67.38 |
| `valuations[].details.cost-local.improvements[].details[].quality` | 7.6% | str(247345) | *; * |
| `valuations[].details.cost-local.improvements[].details[].replacementCostNew` | 100.0% | int(3262366) | 75411; 800367 |
| `valuations[].details.cost-local.improvements[].details[].sequence` | 0.0% | — |  |
| `valuations[].details.cost-local.improvements[].details[].sketchArea` | 100.0% | float(3262366) | 0.0; 2986.0 |
| `valuations[].details.cost-local.improvements[].details[].sketchPerimeter` | 17.2% | int(561059) | 182; 158 |
| `valuations[].details.cost-local.improvements[].details[].specialUnitPrice` | 98.0% | float(1712897) | 0.0; 0.0 |
| `valuations[].details.cost-local.improvements[].details[].specialUnitPriceNote` | 100.0% | str(3262366) | ;  |
| `valuations[].details.cost-local.improvements[].details[].stories` | 58.9% | int(1922738) | 1; 1 |
| `valuations[].details.cost-local.improvements[].details[].structure` | 100.0% | str(3262358) | ;  |
| `valuations[].details.cost-local.improvements[].details[].style` | 7.6% | str(248875) | ;  |
| `valuations[].details.cost-local.improvements[].details[].units` | 97.3% | int(3174705) | 0; 1 |
| `valuations[].details.cost-local.improvements[].details[].useUpForPctBase` | 100.0% | int(3262366) | 0; 1 |
| `valuations[].details.cost-local.improvements[].details[].valueSource` | 100.0% | str(1748665) | A; A |
| `valuations[].details.cost-local.improvements[].details[].wallHeightExterior` | 100.0% | float(3262366) | 0.0; 0.0 |
| `valuations[].details.cost-local.improvements[].details[].wallHeightInterior` | 100.0% | float(3262366) | 0.0; 0.0 |
| `valuations[].details.cost-local.improvements[].details[].width` | 2.3% | float(76329) | 0.0; 0.0 |
| `valuations[].details.cost-local.improvements[].economicAdj` | 100.0% | float(440441) | 10.0; 10.0 |
| `valuations[].details.cost-local.improvements[].economicNote` | 1.8% | str(7788) | HBU; HBU |
| `valuations[].details.cost-local.improvements[].effYearBuilt` | 99.9% | int(440042) | 1984; 2013 |
| `valuations[].details.cost-local.improvements[].exteriorWall` | 1.1% | str(4956) | ;  |
| `valuations[].details.cost-local.improvements[].finishoutPct` | 100.0% | float(440441) | 100.0; 100.0 |
| `valuations[].details.cost-local.improvements[].flatValue` | 100.0% | int(251356) | 75371; 83771 |
| `valuations[].details.cost-local.improvements[].functionalAdj` | 100.0% | float(440441) | 100.0; 100.0 |
| `valuations[].details.cost-local.improvements[].functionalNote` | 2.1% | str(9069) | ;  |
| `valuations[].details.cost-local.improvements[].homesite` | 100.0% | int(440441) | 0; 0 |
| `valuations[].details.cost-local.improvements[].homesiteOverride` | 100.0% | int(440441) | 0; 0 |
| `valuations[].details.cost-local.improvements[].homesitePct` | 100.0% | float(440441) | 100.0; 100.0 |
| `valuations[].details.cost-local.improvements[].improvementValue` | 100.0% | int(251356) | 110310; 135072 |
| `valuations[].details.cost-local.improvements[].imprvAreaModifier` | 100.0% | float(440441) | 1.0; 1.0 |
| `valuations[].details.cost-local.improvements[].imprvComment` | 32.6% | str(143417) | SET UP PER SITE PLAN, DRAWINGS FROM PLANS ARE USE TYPE 19 (SKETCH ONLY) JDR. POOL AREA IS ESTIMATED.; COMMERCIAL RETAIL/RESTAURANT SPACE WITHIN APARTM |
| `valuations[].details.cost-local.improvements[].imprvCondition` | 100.0% | str(440234) | *; * |
| `valuations[].details.cost-local.improvements[].imprvDescription` | 76.3% | str(336172) | MIXED USE, APTS W/RETAIL; COMMERCIAL SPACE |
| `valuations[].details.cost-local.improvements[].imprvModifier` | 100.0% | float(440441) | 1.0; 1.0 |
| `valuations[].details.cost-local.improvements[].imprvType` | 100.0% | str(440440) | 00; 32 |
| `valuations[].details.cost-local.improvements[].mhHud1` | 4.4% | str(19372) | ;  |
| `valuations[].details.cost-local.improvements[].mhHud2` | 2.7% | str(11872) | ;  |
| `valuations[].details.cost-local.improvements[].mhHud3` | 0.9% | str(3921) | ;  |
| `valuations[].details.cost-local.improvements[].mhMake` | 3.8% | str(16697) | ;  |
| `valuations[].details.cost-local.improvements[].mhModel` | 3.7% | str(16196) | ;  |
| `valuations[].details.cost-local.improvements[].mhSerial1` | 4.2% | str(18371) | ;  |
| `valuations[].details.cost-local.improvements[].mhSerial2` | 2.4% | str(10523) | ;  |
| `valuations[].details.cost-local.improvements[].mhSerial3` | 0.9% | str(3914) | ;  |
| `valuations[].details.cost-local.improvements[].mhTitleNumber` | 1.8% | str(8005) | ;  |
| `valuations[].details.cost-local.improvements[].newHSValue` | 100.0% | int(251356) | 0; 0 |
| `valuations[].details.cost-local.improvements[].newNHSValue` | 100.0% | int(251356) | 0; 0 |
| `valuations[].details.cost-local.improvements[].newValue` | 100.0% | int(251356) | 0; 0 |
| `valuations[].details.cost-local.improvements[].newValueDetail` | 100.0% | int(440441) | 0; 0 |
| `valuations[].details.cost-local.improvements[].newValueImprovement` | 100.0% | int(440441) | 0; 0 |
| `valuations[].details.cost-local.improvements[].newValueIndicator` | 100.0% | int(440441) | 0; 0 |
| `valuations[].details.cost-local.improvements[].newValueOverride` | 99.8% | int(439339) | 0; 0 |
| `valuations[].details.cost-local.improvements[].newValueSource` | 100.0% | str(440441) | I; I |
| `valuations[].details.cost-local.improvements[].newValueType` | 0.5% | str(2369) | Full; Full |
| `valuations[].details.cost-local.improvements[].pCostID` | 100.0% | int(440441) | 7262008; 7262008 |
| `valuations[].details.cost-local.improvements[].pImprovementID` | 100.0% | int(440441) | 6960812; 6960813 |
| `valuations[].details.cost-local.improvements[].pctComplete` | 100.0% | float(440441) | 100.0; 100.0 |
| `valuations[].details.cost-local.improvements[].pctCompleteNote` | 4.2% | str(18549) | Set to 1% $1 for 15, see images, 02/12/2015, MAK //;  |
| `valuations[].details.cost-local.improvements[].physicalAdj` | 100.0% | float(440441) | 100.0; 100.0 |
| `valuations[].details.cost-local.improvements[].physicalNote` | 3.2% | str(14026) | ; 1% OBS FOR STIGMA |
| `valuations[].details.cost-local.improvements[].pricingModel` | 98.8% | int(435252) | 11205; 10508 |
| `valuations[].details.cost-local.improvements[].quality` | 99.6% | str(438669) | *; 5 |
| `valuations[].details.cost-local.improvements[].selectedCostValue` | 100.0% | int(251356) | 110310; 102327 |
| `valuations[].details.cost-local.improvements[].sequence` | 0.0% | — |  |
| `valuations[].details.cost-local.improvements[].sketchStatus` | 1.1% | str(5061) | prodigy; prodigy |
| `valuations[].details.cost-local.improvements[].sketches` | 100.0% | — |  |
| `valuations[].details.cost-local.improvements[].stateCd` | 100.0% | str(440441) | F1; F1 |
| `valuations[].details.cost-local.improvements[].stories` | 100.0% | int(440441) | 1; 1 |
| `valuations[].details.cost-local.improvements[].structure` | 100.0% | str(440438) | ;  |
| `valuations[].details.cost-local.improvements[].style` | 100.0% | str(440434) | ;  |
| `valuations[].details.cost-local.improvements[].units` | 100.0% | int(440441) | 0; 0 |
| `valuations[].details.cost-local.improvements[].useImprvDeprec` | 100.0% | int(440441) | 0; 0 |
| `valuations[].details.cost-local.improvements[].valueSource` | 100.0% | str(251336) | A; A |
| `valuations[].details.cost-local.land` | 100.0% | — |  |
| `valuations[].details.cost-local.landHSValue` | 100.0% | int(275728) | 0; 0 |
| `valuations[].details.cost-local.landNHSValue` | 100.0% | int(275728) | 15489873; 2812500 |
| `valuations[].details.cost-local.landNewHSValue` | 100.0% | int(275728) | 0; 0 |
| `valuations[].details.cost-local.landNewNHSValue` | 100.0% | int(275728) | 0; 0 |
| `valuations[].details.cost-local.landNewValue` | 100.0% | int(275728) | 0; 0 |
| `valuations[].details.cost-local.landValue` | 100.0% | int(275728) | 15489873; 2812500 |
| `valuations[].details.cost-local.land[]` | 100.0% | — |  |
| `valuations[].details.cost-local.land[].adjustments` | 100.0% | — |  |
| `valuations[].details.cost-local.land[].adjustments[]` | 100.0% | — |  |
| `valuations[].details.cost-local.land[].adjustments[].adjustAmount` | 100.0% | int(115346) | 0; 0 |
| `valuations[].details.cost-local.land[].adjustments[].adjustDescription` | 100.0% | str(115346) | Terrain; Land Shape |
| `valuations[].details.cost-local.land[].adjustments[].adjustPct` | 100.0% | float(115346) | 75.0; 85.0 |
| `valuations[].details.cost-local.land[].adjustments[].adjustResidualPct` | 100.0% | float(115346) | 0.0; 0.0 |
| `valuations[].details.cost-local.land[].adjustments[].adjustType` | 100.0% | str(115346) | user defined percent; user defined percent |
| `valuations[].details.cost-local.land[].adjustments[].adjustTypeCd` | 100.0% | str(115346) | P; SH |
| `valuations[].details.cost-local.land[].adjustments[].adjustYrTerm` | 100.0% | int(115346) | 0; 0 |
| `valuations[].details.cost-local.land[].adjustments[].modelAdjustID` | 100.0% | int(115346) | 2916; 2924 |
| `valuations[].details.cost-local.land[].adjustments[].pAdjustmentID` | 100.0% | int(115346) | 3474238; 3474239 |
| `valuations[].details.cost-local.land[].adjustments[].pLandID` | 100.0% | int(115346) | 6937409; 6937409 |
| `valuations[].details.cost-local.land[].adjustments[].segmentType` | 100.0% | str(115346) | land; land |
| `valuations[].details.cost-local.land[].applyLandAreaModifier` | 100.0% | int(438956) | 1; 1 |
| `valuations[].details.cost-local.land[].class` | 6.7% | str(29453) | ;  |
| `valuations[].details.cost-local.land[].effectiveGroupAcresOverride` | 100.0% | int(438956) | 0; 0 |
| `valuations[].details.cost-local.land[].effectiveGroupSqftOverride` | 100.0% | int(438956) | 0; 0 |
| `valuations[].details.cost-local.land[].homesite` | 100.0% | int(438956) | 0; 0 |
| `valuations[].details.cost-local.land[].homesiteOverride` | 100.0% | int(438956) | 0; 0 |
| `valuations[].details.cost-local.land[].homesitePct` | 29.2% | float(128066) | 100.0; 100.0 |
| `valuations[].details.cost-local.land[].influence` | 6.7% | str(29453) | ;  |
| `valuations[].details.cost-local.land[].landDescription` | 100.0% | str(438956) | Land; Land |
| `valuations[].details.cost-local.land[].landType` | 100.0% | str(438951) | LAND; LAND |
| `valuations[].details.cost-local.land[].mktAdjValue` | 100.0% | int(266238) | 15489873; 2812500 |
| `valuations[].details.cost-local.land[].mktCalculatedValue` | 100.0% | int(266238) | 17210970; 2812500 |
| `valuations[].details.cost-local.land[].mktEconomicAdj` | 100.0% | float(438956) | 100.0; 100.0 |
| `valuations[].details.cost-local.land[].mktEconomicNote` | 100.0% | str(438956) | ;  |
| `valuations[].details.cost-local.land[].mktFlatValue` | 100.0% | int(266238) | 6365654; 1875000 |
| `valuations[].details.cost-local.land[].mktFlatValueNote` | 100.0% | str(266238) | ;  |
| `valuations[].details.cost-local.land[].mktFunctionalAdj` | 100.0% | float(438956) | 100.0; 100.0 |
| `valuations[].details.cost-local.land[].mktFunctionalNote` | 100.0% | str(438956) | ;  |
| `valuations[].details.cost-local.land[].mktLandAreaModifier` | 100.0% | float(438956) | 1.0; 1.0 |
| `valuations[].details.cost-local.land[].mktLandModifier` | 100.0% | float(438956) | 1.0; 1.0 |
| `valuations[].details.cost-local.land[].mktMethod` | 100.0% | str(438920) | SF; SF |
| `valuations[].details.cost-local.land[].mktModel` | 99.9% | int(438279) | 52; 52 |
| `valuations[].details.cost-local.land[].mktModelUnitPrice` | 100.0% | float(266238) | 0.0; 0.0 |
| `valuations[].details.cost-local.land[].mktNewHSValue` | 100.0% | int(266238) | 0; 0 |
| `valuations[].details.cost-local.land[].mktNewNHSValue` | 100.0% | int(266238) | 0; 0 |
| `valuations[].details.cost-local.land[].mktNewValue` | 100.0% | int(266238) | 0; 0 |
| `valuations[].details.cost-local.land[].mktNewValueIndicator` | 100.0% | int(438956) | 0; 0 |
| `valuations[].details.cost-local.land[].mktNewValueOverride` | 100.0% | int(438956) | 0; 0 |
| `valuations[].details.cost-local.land[].mktNewValueYear` | 1.3% | int(5854) | 0; 0 |
| `valuations[].details.cost-local.land[].mktPhysicalAdj` | 100.0% | float(438956) | 100.0; 100.0 |
| `valuations[].details.cost-local.land[].mktPhysicalNote` | 100.0% | str(438956) | ;  |
| `valuations[].details.cost-local.land[].mktSpecialUnitPrice` | 94.7% | float(252126) | 170.0; 180.0 |
| `valuations[].details.cost-local.land[].mktUnitPriceSelection` | 100.0% | str(266238) | S; S |
| `valuations[].details.cost-local.land[].mktValue` | 100.0% | int(266238) | 15489873; 2812500 |
| `valuations[].details.cost-local.land[].mktValueMethod` | 100.0% | str(266238) | A; A |
| `valuations[].details.cost-local.land[].notes` | 100.0% | — |  |
| `valuations[].details.cost-local.land[].notes[]` | 100.0% | — |  |
| `valuations[].details.cost-local.land[].notes[].content` | 100.0% | str(243500) | ASSEMBLED WITH ADJOINING TRACTS TO ENHANCE VALUE AND GBA, RAM 4-12-12; Base lot value to $500k/lot per land analysis, TDW, 02/13/18 |
| `valuations[].details.cost-local.land[].notes[].pLandID` | 100.0% | int(243500) | 7284336; 7453598 |
| `valuations[].details.cost-local.land[].notes[].pNoteID` | 100.0% | int(243500) | 3846032; 4131841 |
| `valuations[].details.cost-local.land[].pCostID` | 100.0% | int(438956) | 7262008; 7262009 |
| `valuations[].details.cost-local.land[].pLandID` | 100.0% | int(438956) | 7284336; 7225793 |
| `valuations[].details.cost-local.land[].sequence` | 0.0% | — |  |
| `valuations[].details.cost-local.land[].sizeAcres` | 100.0% | float(438956) | 0.5398; 2.3553 |
| `valuations[].details.cost-local.land[].sizeDepthLeft` | 96.5% | float(423810) | 0.0; 0.0 |
| `valuations[].details.cost-local.land[].sizeDepthRight` | 96.5% | float(423811) | 0.0; 0.0 |
| `valuations[].details.cost-local.land[].sizeEffectiveDepth` | 96.5% | float(423811) | 0.0; 0.0 |
| `valuations[].details.cost-local.land[].sizeEffectiveFront` | 96.5% | float(423814) | 0.0; 0.0 |
| `valuations[].details.cost-local.land[].sizeEffectiveGroupAcresOverride` | 96.5% | float(423810) | 0.0; 0.0 |
| `valuations[].details.cost-local.land[].sizeEffectiveGroupSqftOverride` | 100.0% | float(438956) | 0.0; 0.0 |
| `valuations[].details.cost-local.land[].sizeLot` | 100.0% | int(438956) | 1; 1 |
| `valuations[].details.cost-local.land[].sizeSqft` | 100.0% | float(438956) | 23512.0; 102596.87 |
| `valuations[].details.cost-local.land[].sizeUseableAcres` | 100.0% | float(438814) | 0.5398; 2.3553 |
| `valuations[].details.cost-local.land[].sizeUseableSqft` | 100.0% | float(438814) | 23512.0; 102596.87 |
| `valuations[].details.cost-local.land[].sizeWidthBack` | 96.5% | float(423814) | 0.0; 0.0 |
| `valuations[].details.cost-local.land[].sizeWidthFront` | 96.5% | float(423814) | 0.0; 0.0 |
| `valuations[].details.cost-local.land[].stateCd` | 100.0% | str(438956) | F1; B1 |
| `valuations[].details.cost-local.land[].su78Value` | 100.0% | int(266238) | 0; 0 |
| `valuations[].details.cost-local.land[].su78ValuePct` | 100.0% | float(266238) | 0.0; 0.0 |
| `valuations[].details.cost-local.land[].suApply` | 100.0% | int(438956) | 0; 0 |
| `valuations[].details.cost-local.land[].suApplyYr` | 7.4% | int(32462) | 2023; 2023 |
| `valuations[].details.cost-local.land[].suCalculatedValue` | 100.0% | int(266238) | 0; 0 |
| `valuations[].details.cost-local.land[].suConvertDt` | 0.0% | — |  |
| `valuations[].details.cost-local.land[].suExclusionValue` | 100.0% | int(266238) | 0; 0 |
| `valuations[].details.cost-local.land[].suFlatValue` | 100.0% | int(266238) | 0; 0 |
| `valuations[].details.cost-local.land[].suHarvestDt` | 0.0% | — |  |
| `valuations[].details.cost-local.land[].suLate` | 100.0% | int(438956) | 0; 0 |
| `valuations[].details.cost-local.land[].suMethod` | 8.0% | str(35083) | AG; AG |
| `valuations[].details.cost-local.land[].suModel` | 2.5% | int(11096) | 540; 542 |
| `valuations[].details.cost-local.land[].suModelUnitPrice` | 100.0% | float(266238) | 0.0; 0.0 |
| `valuations[].details.cost-local.land[].suNewValue` | 100.0% | int(266238) | 0; 0 |
| `valuations[].details.cost-local.land[].suNewValueIndicator` | 100.0% | int(438956) | 0; 0 |
| `valuations[].details.cost-local.land[].suNewValueOverride` | 100.0% | int(438956) | 0; 0 |
| `valuations[].details.cost-local.land[].suNewValueYear` | 1.3% | int(5854) | 0; 0 |
| `valuations[].details.cost-local.land[].suPreRestrictedUseValue` | 8.0% | int(21281) | 0; 0 |
| `valuations[].details.cost-local.land[].suPrevType` | 0.8% | str(3561) | 2NP1; 2NP2 |
| `valuations[].details.cost-local.land[].suRestrictedUse` | 8.0% | str(21281) | ;  |
| `valuations[].details.cost-local.land[].suRestrictedUseValue` | 8.0% | int(21281) | 0; 0 |
| `valuations[].details.cost-local.land[].suSoilType` | 6.7% | str(29453) | ;  |
| `valuations[].details.cost-local.land[].suSpecialUnitPrice` | 8.1% | float(21636) | 700.0; 50.0 |
| `valuations[].details.cost-local.land[].suType` | 8.0% | str(35076) | 2WP1; 2WP2 |
| `valuations[].details.cost-local.land[].suUnitPriceSelection` | 8.3% | str(36523) | T; T |
| `valuations[].details.cost-local.land[].suUseCd` | 8.0% | str(35079) | 1D1; 1D1 |
| `valuations[].details.cost-local.land[].suValue` | 100.0% | int(266238) | 0; 0 |
| `valuations[].details.cost-local.land[].suValueMethod` | 100.0% | str(266238) | F; F |
| `valuations[].details.cost-local.livingArea` | 100.0% | int(275728) | 0; 0 |
| `valuations[].details.cost-local.pCostID` | 100.0% | int(275728) | 7262013; 7262016 |
| `valuations[].details.cost-local.pEconValuationID` | 100.0% | int(275728) | 0; 0 |
| `valuations[].details.cost-local.pValuationID` | 100.0% | int(275728) | 22853321; 22853324 |
| `valuations[].details.cost-local.propCondition` | 100.0% | int(275728) | 0; 0 |
| `valuations[].details.cost-local.propUse` | 0.0% | — |  |
| `valuations[].details.cost-local.quality` | 100.0% | int(275728) | 0; 0 |
| `valuations[].details.cost-local.stateCd` | 0.0% | — |  |
| `valuations[].details.cost-local.structureValue` | 100.0% | int(275728) | 110310; 0 |
| `valuations[].details.cost-local.suExclusionValue` | 100.0% | int(275728) | 0; 0 |
| `valuations[].details.cost-local.suLandMktValue` | 100.0% | int(275728) | 0; 0 |
| `valuations[].details.cost-local.suValue` | 100.0% | int(275728) | 0; 0 |
| `valuations[].details.cost-local.yearBuilt` | 100.0% | int(275728) | 0; 0 |
| `valuations[].econID` | 0.2% | int(827) | 139359; 136737 |
| `valuations[].econRollCorr` | 0.2% | int(827) | 0; 0 |
| `valuations[].econVersion` | 0.2% | int(827) | 0; 0 |
| `valuations[].econYear` | 0.2% | int(827) | 2025; 2025 |
| `valuations[].flatNewValueIndicator` | 100.0% | int(486858) | 0; 0 |
| `valuations[].flatValueReason` | 3.2% | str(15398) | Current Year Valuation; Current Year Valuation |
| `valuations[].flatValueSource` | 3.3% | str(15943) | External; External |
| `valuations[].improvementHSValue` | 100.0% | int(486858) | 0; 0 |
| `valuations[].improvementNHSValue` | 100.0% | int(486858) | 99906; 44022563 |
| `valuations[].improvementNewHSValue` | 100.0% | int(486858) | 0; 0 |
| `valuations[].improvementNewNHSValue` | 100.0% | int(486858) | 0; 0 |
| `valuations[].improvementNewValue` | 100.0% | int(486858) | 0; 0 |
| `valuations[].incomeMethod` | 0.0% | — |  |
| `valuations[].isPrimary` | 100.0% | int(486858) | 1; 1 |
| `valuations[].landHSValue` | 100.0% | int(486858) | 0; 0 |
| `valuations[].landHomesitePct` | 100.0% | float(486858) | 0.0; 0.0 |
| `valuations[].landNHSValue` | 100.0% | int(486858) | 4232160; 18467437 |
| `valuations[].landNewHSValue` | 100.0% | int(486858) | 0; 0 |
| `valuations[].landNewNHSValue` | 100.0% | int(486858) | 0; 0 |
| `valuations[].landNewValue` | 100.0% | int(486858) | 0; 0 |
| `valuations[].landValue` | 100.0% | int(486858) | 4232160; 18467437 |
| `valuations[].newValue` | 100.0% | int(486858) | 0; 0 |
| `valuations[].newValueHomesitePct` | 100.0% | float(486858) | 0.0; 0.0 |
| `valuations[].notes` | 42.9% | str(209053) | ;  |
| `valuations[].pID` | 100.0% | int(486858) | 100008; 100012 |
| `valuations[].pValuationID` | 100.0% | int(486858) | 24392850; 24524351 |
| `valuations[].pctAllocation` | 100.0% | float(486858) | 0.0; 0.0 |
| `valuations[].structureHomesitePct` | 100.0% | float(486858) | 0.0; 0.0 |
| `valuations[].structureValue` | 100.0% | int(486858) | 99906; 44022563 |
| `valuations[].suExclusionValue` | 100.0% | int(486858) | 0; 0 |
| `valuations[].suLandMktValue` | 100.0% | int(486858) | 0; 0 |
| `valuations[].suValue` | 100.0% | int(486858) | 0; 0 |
| `valuations[].value` | 100.0% | int(486858) | 4332066; 62490000 |
| `valuations[].valueType` | 100.0% | str(486858) | appeals; appeals |
