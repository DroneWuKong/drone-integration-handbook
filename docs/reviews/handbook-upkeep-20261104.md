# Autonomous maintenance audit — 2026-11-04

## Observed state

- [Public maintenance run 41765346221](https://github.com/DroneWuKong/drone-integration-handbook/actions/runs/41765346221) passed preparation, full validation and exact-deployment publication. Eight release feeds and twelve emerging projects were checked on 2026-11-04; no discovery search errors were recorded. These remain metadata observations, not hardware acceptance.
- [Private fact run 41766059824](https://github.com/DroneWuKong/drone-integration-handbook/actions/runs/41766059824) completed on `node2-gupb-uas-handbook`. The previous runner-queue blocker is resolved. It connected to the durable private ledger, read 27 existing specifications, applied zero factual changes and started zero background jobs. Its research summary explicitly deferred work because the existing trial was expired, disabled or at its workload limit; this aggregate message does not establish which condition applies. No renewal or paid retry was performed.
- Production was independently checked against main commit `692ebcbc8f1c8b57bc6de540937f0a1fe2546a5b`, release `cb40a49366a24b3b49c1`, with reference snapshot, reference page, durable review/submission and attachment capabilities consistent.

## Repairs

1. Multi-file repository discovery enforced its three-candidate budget only inside each file. Later files could add further candidates. The budget now spans all paths and repeated entries for the same repository. A fixture verifies that other repositories retain their own independent budget and source scopes still disclaim hardware acceptance.
2. Private inventory previously checked sources from a fresh state and later saved that snapshot under the same cache prefix used by public maintenance. This could replace retained fingerprints and open-task history. Private inventory now restores the shared source-review cache before monitoring, carrying that history through its existing artifact/save route. A workflow regression test checks ordering and cache identity. This prevents future resets; it does not reconstruct any history already lost from the latest cache.

The public run reported 16 open monitoring tasks. Because of the cache-reset defect, a lower count must not be interpreted as completed factual review. No review task was marked factually resolved by this audit.

## Primary-source and related-repository checks

- [Betaflight releases](https://github.com/betaflight/betaflight/releases): the API still reports stable `2026.6.2`, published 2026-09-16, and preview `2026.6.0-rc3`, published 2026-07-23. A planned November release-candidate date is not evidence that a release has been published. Covered chapter versions are not silently advanced.
- The [STM32N6](https://www.st.com/en/microcontrollers-microprocessors/stm32n6-series.html) and [i.MX 95](https://www.nxp.com/products/i.MX95) primary product pages remain available to independent web retrieval but unavailable through the runner's direct monitor. Prior verification/access dates remain 2026-10-07 and due dates remain 2026-11-06. Availability is not full claim verification, so those dates were not advanced.
- The public [Orqa Betaflight Ports README](https://github.com/DroneWuKong/Orqa_Betaflight_Ports/blob/b868a56f43923c17bd50187f76ed033e06b57289/README.md) now documents downloadable board/sensor-specific images and explicitly labels them experimental and hardware-unvalidated. Its declarations remain candidates, not verified flight performance or a firmware recommendation.
- The emerging [DroneC2 README](https://github.com/hsb020524/DroneC2/blob/f37503e3ccad0e64e7f904720fe9b64ef242e5e0/README.md) was inspected as documentation for a receive/display-only Unity/MAVLink simulation viewer. Its self-reported test and accuracy figures were not promoted to handbook facts.

## Unchanged boundaries

Independent exact-statement researcher/verifier agreement and source-snapshot validation remain required for automatic factual publication. Publication holds, revision history, sanitized `forge-data` private-export routing, exact-commit deployment gates and non-renewing research/cost limits are unchanged. Private packets and credentials were not exported or moved to hosted orchestration. New paid research remains blocked by the existing gate; metadata upkeep and consumption of already eligible evidence continue independently.
