# Review Record — Conflict-Driven Adaptations of Open UAS Firmware

**Article:** `components/military-firmware-forks.md`  
**Draft prepared:** July 31, 2026  
**Publication status:** Draft replacement prepared; export-control, provenance, and publisher review remain required.  
**Automated gate:** Reviewed-replacement validation introduced in PR #51.

## Review objective

Replace the former operational landscape with a public-source historical and software-assurance overview. The draft is intentionally generic and does not name access-controlled packages, provide download/access instructions, identify operating frequencies, list target hardware, describe identification defeat, or explain offensive mission procedures.

## Primary-source record

| Source | Relevant proposition | Accessed |
|---|---|---:|
| BIS EAR Part 734 | Scope of the EAR and exclusion for certain published technology/software | 2026-07-31 |
| BIS EAR Part 744 | End-use, end-user, U.S.-person-support, military, military-intelligence, and UAV-related controls | 2026-07-31 |
| NIST SP 800-218 | Secure Software Development Framework | 2026-07-31 |
| NIST SSDF project | Current SSDF publication status | 2026-07-31 |
| NTIA Minimum Elements for an SBOM | SBOM purpose and minimum-element framework | 2026-07-31 |

## Material corrections from the withdrawn version

- Removed names, versions, package locations, access channels, binding or key details, hardware target lists, and frequency ranges.
- Removed identification-system defeat and manufacturer-control circumvention discussion.
- Removed jammer-location, targeting, hunter-killer, strike, and operational deployment guidance.
- Removed unsupported prevalence and production-scale claims.
- Reframed the page around provenance, secure development, testing, configuration control, SBOMs, maintenance, and export-screening triggers.
- Added a public-information/export-control boundary without representing the article as an export classification.

## Deliberately excluded scope

- No specific conflict package or fork is endorsed, linked, located, or explained.
- No source or binary is classified.
- No transfer, export, reexport, in-country transfer, service, or end user is approved.
- No military end use, military-intelligence use, identification defeat, countermeasure evasion, targeting, or offensive support is described.
- No claim is made that publicly accessible information makes related private assistance lawful.

## Qualified-review checklist

### Export-control review

- [ ] Public scope stays within high-level historical/software-assurance discussion.
- [ ] Part 734 “published” discussion is appropriately limited.
- [ ] Part 744 discussion does not attempt a transaction-specific classification.
- [ ] No implementation assistance or support to a restricted end user is enabled.
- [ ] No controlled or customer-restricted source was used.

### Provenance and licensing review

- [ ] No text, table, source code, binary, screenshot, or diagram was copied from an unlicensed source.
- [ ] All high-level factual claims are supportable from public, unrestricted sources.
- [ ] Future named case studies must use the evidence labels defined in the article.

### Technical review

- [ ] Software-assurance, SBOM, configuration-control, testing, and fleet-management recommendations are technically sound.
- [ ] No section accidentally provides operational circumvention or attack guidance.

## Reviewer disposition

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

```text
Publisher: Jeremiah Wong / Midwest Nice UAS LLC
Decision date:
Exact commit approved:
Decision: APPROVED FOR PUBLICATION / RETAIN HOLD
Reverification date:
```
