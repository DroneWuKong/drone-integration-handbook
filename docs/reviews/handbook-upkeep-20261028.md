# Autonomous handbook upkeep audit — 2026-10-28

## Outcome

The hosted public metadata pipeline is operating and its exact-commit publication gate is healthy. This audit repaired two reliability defects without changing factual handbook claims: duplicate source-review tasks are now superseded into one open task per source and reason while retaining their history, and transient source/GitHub failures receive three bounded attempts. Permanent errors, oversized responses, redirects and unverified content still fail closed.

Three active, relevant public repositories were added to bounded discovery: `Orqa_Betaflight_Ports`, `Orqa_ArduPilot_Ports`, and `betaflight-improvements`. Their repository statements remain research candidates only. Repository metadata and documentation are not hardware-performance evidence.

## Evidence reviewed

- The 2026-10-28 [`evidence-review-queue` run](https://github.com/DroneWuKong/drone-integration-handbook/actions/runs/40625306840) completed its prepare, validation and exact-deployment jobs successfully.
- The source-review cache grew from 203 open tasks on 2026-10-22 to 284 on 2026-10-28 while the monitored source set remained 30. The former task identity included the page revision, so repeated dynamic page changes created new open tasks. The replacement identity uses source plus reason, records the latest revision and observation count, and preserves older task objects as `superseded`.
- Eight configured release feeds and twelve emerging-project entries were inspected. Betaflight's retained stable release [`2026.6.2`](https://github.com/betaflight/betaflight/releases/tag/2026.6.2) (published 2026-09-16) matches its official GitHub release page; the feed's `RemoteDisconnected` status was a transport failure, not evidence of a version change.
- The first-party [STM32N6](https://www.st.com/en/microcontrollers-microprocessors/stm32n6-series.html) and [i.MX 95](https://www.nxp.com/products/i.MX95) product pages remained unavailable to the workflow's direct fetch path. Their prior fingerprints are retained and review remains due 2026-11-06. Reachability was not treated as factual verification.
- Public repository discovery now covers nine explicitly configured repositories plus the bounded emerging-project sample. Inactive tracking hubs were not added.

## Boundaries preserved

- Automatic factual publication still requires independent researcher and verifier packets for the exact statement and source snapshot.
- Publication holds remain in force and no held content was promoted.
- Private material remains excluded except through the existing sanitized `forge-data` public route.
- No paid research was started or renewed. The non-renewing trial and durable private ledger rules are unchanged.
- The private fact-research stage remains blocked waiting for the `prismo` self-hosted runner. It was not retried because an uncertain retry could duplicate paid work outside the durable-ledger check.
