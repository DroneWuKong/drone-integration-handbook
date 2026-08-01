# Review Record — Remote ID Decision Guide for Custom UAS

**Article:** `components/remote-id-custom-builds.md`  
**Stable component reference:** Generated from the component registry  
**Draft prepared:** July 31, 2026  
**Publication status:** Draft replacement prepared; qualified review and publisher release decision remain required.

## Review objective

Replace the prior custom-build article with a U.S.-specific decision guide grounded in current FAA and regulatory sources. The draft intentionally does not prescribe product-specific wiring or firmware commands.

## Primary-source record

| Source | Relevant proposition | Accessed |
|---|---|---:|
| 14 CFR Part 89 | Controlling Remote ID requirements and definitions | 2026-07-31 |
| FAA Remote Identification of Drones | Applicability; Standard Remote ID, broadcast-module, and FRIA paths; VLOS limitation; registration treatment; DoC and LOA process | 2026-07-31 |
| FAA Remote Identification Compliance | Registration must use the Standard Remote ID aircraft or broadcast-module serial number when applicable | 2026-07-31 |
| FAA Recreational Flyers | Recreational registration threshold at 250 g and distinction between recreational and Part 107 operations | 2026-07-31 |
| FAA Commercial Operators | Part 107 registration requirement | 2026-07-31 |
| FAA Remote ID for Industry | Manufacturers, rather than individual operators, submit Remote ID Declarations of Compliance | 2026-07-31 |
| FAA Declaration of Compliance system | Product-specific accepted declarations; must be checked at purchase and registration time | Dynamic source |

## Material corrections from the withdrawn version

- Removed the blanket statement that aircraft under 250 g do not require Remote ID.
- Distinguished qualifying limited recreation from Part 107; all Part 107 aircraft require registration.
- Removed the claim that an FAA registration number substitutes for a Remote ID serial number.
- Distinguished the recreational inventory procedure from individual Part 107 registration.
- Removed unverified Betaflight, ArduPilot, iNav, and module-specific commands.
- Removed product recommendations that were not tied to a current accepted Declaration of Compliance.
- Added the FAA's VLOS limitation for broadcast-module operations.
- Added FRIA boundary and VLOS limitations.
- Added the FAA Letter of Authorization path without implying automatic eligibility.

## Deliberately excluded scope

- No product is represented as currently accepted without checking the live FAA DoC system.
- No flight-controller firmware is represented as independently creating Standard Remote ID compliance.
- No wiring diagram or CLI command is approved.
- No advice is given for BVLOS, public-aircraft, complex Part 91, foreign registration, or operation-specific waiver questions.
- The article does not determine compliance for a particular aircraft or operation.

## Qualified-review checklist

### FAA/UAS regulatory review

- [ ] Applicability statement is accurate for Part 107 and limited recreation.
- [ ] Under-250-g language is appropriately qualified.
- [ ] Registration and serial-number distinctions are accurate.
- [ ] Recreational inventory and Part 107 procedures are accurately separated.
- [ ] Broadcast-module VLOS and FRIA limitations are complete.
- [ ] LOA language does not imply automatic authorization.
- [ ] No material Part 89 requirement is misstated or omitted for the intended scope.

### Technical review

- [ ] The draft correctly avoids treating generic firmware support as a compliance declaration.
- [ ] The preflight checklist does not promise that a receiver app proves legal compliance.
- [ ] No untested command, wiring, hardware recommendation, or configuration remains.

## Reviewer disposition

Complete after review:

```text
Reviewer identity:
Reviewer qualifications:
Review date:
Exact commit reviewed:
Approved public scope:
Required changes:
Unresolved limitations:
Private record ID, if applicable:
Disposition: APPROVE / REQUEST CHANGES / DO NOT PUBLISH
```

## Publisher release decision

Complete only after qualified review and passing CI:

```text
Publisher: Jeremiah Wong / Midwest Nice UAS LLC
Decision date:
Exact commit approved:
Decision: APPROVED FOR PUBLICATION / RETAIN HOLD
Reverification date:
```
