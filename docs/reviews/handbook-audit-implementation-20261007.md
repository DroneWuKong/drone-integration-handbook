# Handbook audit implementation — 7 October 2026

## Outcome

Correct the factual and procedural errors found in the October audit, add eight practical integration references, and maintain the handbook through scheduled source checks, repository discovery, independent research and deterministic publication. Routine verified facts do not require a recurring human approval queue.

## Work sequence

1. Correct the preflight, RF, GNSS, MAVLink and autonomy-health errors first. Remove unsupported numerical promises rather than replace them with different unsupported promises.
2. Update firmware, OpenHD, mesh, latency, power, sensor and compute references against primary documentation. Record exact versions, models, dates and measurement boundaries.
3. Add firmware recovery, simulation/failure testing, CAN protocols, video diagnostics, time/coordinates, telemetry ownership, workload selection and evidence-record references using unused stable chapter IDs.
4. Separate research identity from deployment identity; use the private durable ledger to skip completed/in-progress work. Revisit claims when their evidence or policy changes, or their review interval expires.
5. Discover additions from the publisher's public repositories and a sanitized private export. Treat repo assertions as candidates; distinguish implementation facts from field performance, availability and certification.
6. Automatically promote independently supported scoped facts into managed claims, preserving the previous statement, sources and correction history. Build and test the exact revision before publication. Conflicts, protected content and unverifiable assertions remain exceptions.
7. Verify the custom domain against the merged commit and retain reproducible software evidence.

## Audit disposition checklist

| Findings | Work |
|---|---|
| F01, F17 | Separate props-off bench checks from flight preparation; remove universal autonomy permission thresholds |
| F02 | Correct 915 MHz / 10 km free-space loss; remove range promises and universal channel separation |
| F03, F10 | Correct versioned GPS/serial parameters; distinguish NTRIP from OPUS; add datum, timing and checkpoint provenance |
| F04, F05 | Correct MAVLink v2 header, signing trailer, acknowledgements, flags, states and altitude frames |
| F06, F07 | Update Betaflight capabilities/app and exact OpenHD adapter/image compatibility |
| F08, F09 | Scope latency measurements and proprietary mesh interfaces; remove inferred vendor internals |
| F11 | Calculate power over time and by voltage rail; remove universal BEC sizing |
| F12 | Replace nationality-based compliance conclusions with item/authority/configuration-specific evidence |
| F13, F14 | Durable claim research identity, qualitative inventory, source monitoring and automatic publication |
| F15 | Reconcile roadmap, release documentation and actual two publication holds |
| F16, F18 | Correct exact sensor variants and compute categories; distinguish neural inference from classical estimation |

## Publication rules

Promoted factual statements carry an evidence category, exact scope, primary source, check date and permanent identity. Legacy statements retain their unresolved status until checked. Manufacturer specifications are identified as manufacturer-reported. Software results describe the executed software/configuration; they do not certify a flight system. Facts about source code do not establish operational performance.

Independent research roles must check the same exact proposed statement, retrieve cited passages and agree on scope. A changed proposal goes through verification as a new statement. Mathematical claims require software reproduction. The publisher authorizes routine factual maintenance through the 7 October instruction; exceptional material and the two existing publication holds retain their existing handling.

Repository discovery never publishes raw private files, credentials, customer records or proprietary configurations. Public source content is treated as untrusted data, never as instructions to change pipeline policy. New evidence cannot expand paid research beyond the existing non-renewing trial limits.

## Acceptance

- An unrelated deploy does not duplicate research; changed evidence or an expired review can reopen it.
- Two software observers, replay and failure cases are reproducible without hardware.
- Missing sources, unsupported passages, conflicting scopes, stale proposals and held content cannot auto-publish.
- A verified managed correction updates prose and evidence history together; repeating a cycle is idempotent.
- Scheduled maintenance discovers public repo changes, checks managed sources and applies eligible verified facts without routine approval.
- Required source, generated-site, API, browser and deployment checks pass.

## Evidence and limits

Primary-source URLs and locators accompany the corrected chapters and managed registry. The initial audit covered a finite set of high-impact errors; this change does not certify every legacy claim. Recurring maintenance continues through the remaining inventory within the existing cost limits.
