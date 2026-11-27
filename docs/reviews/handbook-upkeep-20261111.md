# Autonomous maintenance audit — 2026-11-11

The [public workflow](https://github.com/DroneWuKong/drone-integration-handbook/actions/runs/42950879621) passed prepare, validation and exact deployment. Its November 11 snapshot recorded eight release feeds, twelve emerging projects without search errors, 25 repository candidates and 33 open source-monitor tasks. Production independently matched main commit `80e552fa9334726d1482c721d6a6ebf606d959e1`, release `65a685f9bb47efe8b36a`, with review and attachment capabilities available.

The [private fact workflow](https://github.com/DroneWuKong/drone-integration-handbook/actions/runs/42951674644) passed and read 27 durable specs. It applied no factual changes and started zero background jobs. Its reported deferral was “Existing research trial expired, disabled or at its workload limit”; that aggregate message does not distinguish the exact condition. No trial renewal, paid retry, or private export was attempted.

## Overdue source reviews

Ten source reviews were due November 6. Eight sources were reachable to the runner; the [ST STM32N6](https://www.st.com/en/microcontrollers-microprocessors/stm32n6-series.html) and [NXP i.MX 95](https://www.nxp.com/products/i.MX95) product pages still failed its direct fetch but were retrieved independently. Their published family descriptions did not warrant changing the handbook's existing model scope. The [Hailo-8](https://hailo.ai/products/ai-accelerators/hailo-8-ai-accelerator/) chip specification and [Benewake](https://en.benewake.com/TFminiS/index.html) variant-weight entries still support the cited narrow values; neither establishes installed performance. The MAVLink, Betaflight, OpenHD and version-scoped PX4 references were checked for availability; those checks are not complete revalidation of all associated claims.

The watchlist now separates overdue and due-today reviews from fetch availability, relative to the published UTC snapshot. Source access dates, review deadlines, claims and revision history were not advanced. A reachable source or manual spot check is not an independent exact-statement decision.

## Discovery and publication boundaries

[MAVLink SITL Assurance Lab](https://github.com/JasonStys/mavlink-sitl-assurance-lab) is a public, simulator-only candidate, not an observed hardware result or a published release. It remains watch-only. No new facts qualified for automatic publication. The exact-statement research/verifier gate, publication holds, sanitized private-export path, durable ledger and non-renewing trial limits remain unchanged.

## Validation follow-up

The [initial PR check](https://github.com/DroneWuKong/drone-integration-handbook/actions/runs/43042060726) passed the build and evidence checks but could not install browser dependencies: the hosted runner failed to resolve `security.ubuntu.com`. The three hosted validation jobs run the same browser checks in the official, digest-pinned Playwright image matching the lockfile. The image supplies Chromium and its libraries; Python, Node setup and builds stay on the host. The browser container needs only loopback networking.

Subsequent direct probes from a separate environment returned HTTP 200 for both vendor URLs using the monitor's request headers. That does not establish recovery on the hosted runner; its own next observation controls the watchlist. No vendor URLs or evidence dates were changed.
