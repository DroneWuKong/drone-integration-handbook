# Publication Review Holds

**Established:** July 31, 2026  
**Owner:** Jeremiah Wong / Midwest Nice UAS LLC  
**Private source of record:** `DroneWuKong/Ai-Project`

A publication hold removes current operational or legal guidance while preserving the repository path, stable handbook anchor, correction history, and evidence trail. A hold is not a determination that the prior text was unlawful or false. It means the material is not reliable or appropriately scoped enough for present public use.

Detailed evidence, reviewer notes, claim ledgers, permissions, configuration records, and publisher decisions are maintained privately. This public repository contains only the released text and nonprivileged review summaries. See [`PRIVATE_SOURCE_OF_RECORD.md`](PRIVATE_SOURCE_OF_RECORD.md).

## Current holds and draft replacements

| Path | Public state | Primary review | Release condition |
|---|---|---|---|
| `field/ew-countermeasures.md` | Hold; civil-safety replacement proposed in PR #49 | Spectrum/FCC, flight safety, privacy, export/public scope, technical measurement | Lawful interference recognition, safe recovery, self-interference troubleshooting, evidence preservation, and authorized reporting only; no targeting, electronic attack, pursuit, unauthorized retuning, or evasion instructions |
| `field/intercept-ops.md` | Hold; civil encounter/safety replacement proposed in PR #50 | Aviation/criminal counter-UAS, public safety, privacy/evidence, export/public scope | Permanent retirement of the operational intercept playbook; public replacement limited to civilian safety, reporting, evidence preservation, and non-interference |
| `field/elint-operators.md` | Hold; lawful survey replacement proposed in PR #49 | Spectrum/FCC, privacy/communications, export/public scope, technical measurement | Passive ambient survey, self-interference testing of owned systems, lawful coordination, minimal-data records, and authorized reporting only; no third-party content collection, tracking, localization, intelligence support, or targeting |
| `components/military-firmware-forks.md` | Hold; software-assurance replacement proposed in PR #48 | Export controls, source provenance/licensing, technical public-scope review | High-level public-source history and defensive software assurance only; no access, circumvention, restricted-band, ID-defeat, countermeasure-evasion, targeting, or offensive details |
| `components/ndaa-compliance.md` | Hold; federal procurement screening replacement proposed in PR #47 | Federal procurement counsel and technical configuration review | Dated preliminary screening workflow separating official sources, manufacturer claims, solicitation/configuration evidence, exceptions/waivers, Blue List evidence, and authorized decisions; no universal vendor certification |
| `components/orqa-hardware-guide.md` | Hold; no replacement PR | Independent technical, provenance/permission, procurement/compliance, conflict review | Claim-level records, independent reviewer, close relationship disclosure, removal of unsupported legal classifications, and separation of public specifications from relationship-derived/private material |
| `integration/wingman-apb.md` | Hold; no replacement PR | Independent flight-controls/safety, authority-boundary verification, export/public scope, provenance/permission, conflict review | Tested authority boundaries, failure behavior, versioned evidence, relationship disclosure, clear prototype/validated distinction, and removal of unreviewed terminal-guidance or confidential detail |

## Released or changed state

| Path | State | Public record | Private-record follow-up |
|---|---|---|---|
| `components/remote-id-custom-builds.md` | Replacement merged August 1, 2026 | PR #46; merge commit `1dbdcd40116edbf1d50c4493746cd1504d359b52` | Import or confirm the actual FAA/UAS reviewer disposition and Jeremiah Wong publisher decision in the private review register; merge history alone is not proof that those reviews occurred |

## Required review record

Before a held page returns to substantive publication, record:

- internal article and private record IDs;
- reviewer identity and competence;
- exact commit/blob reviewed;
- scope and date of review;
- source and evidence ledger;
- configuration and software version where relevant;
- legal/regulatory regimes considered;
- foreseeable misuse and safety controls;
- provenance, rights, and permission status;
- conflicts and material relationships;
- approved public scope;
- explicitly excluded private scope;
- unresolved limitations;
- Jeremiah Wong publisher release decision;
- public merge and production-verification record.

Do not paste confidential legal advice, controlled technical data, privileged communications, customer-restricted information, private configurations, or personal information into this public file. Maintain private records in the Ai-Project source-of-record system or a more-restricted approved system.

## Approval sequence

```text
private evidence complete
  → applicable qualified review
  → exact public commit identified
  → Jeremiah Wong publisher approval
  → public PR ready/merge
  → generated-site validation
  → production verification
  → private manifest/register update
```

CI validates structure and known regression markers; it does not provide legal, export, regulatory, safety, technical, provenance, or publisher approval.

## Contact

Corrections, right of reply, documentary evidence, or review proposals: [jeremiah@midwestniceuas.com](mailto:jeremiah@midwestniceuas.com).
