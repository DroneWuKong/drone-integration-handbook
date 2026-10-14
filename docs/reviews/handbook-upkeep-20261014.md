# Handbook upkeep audit — 14 October 2026

## Publication state

These repairs were validated locally against main commit `9ac80b3dbeda067ea1d78b9ba3312bbe0f319401`. The initial audit could not publish because GitHub write access was unavailable; it preserved a tested patch package. After the publisher restored the GitHub connection, the repairs proceeded through the normal CI and deployment checks. Publication requires those checks to pass.

The live domain matches that main commit and release `79fbc318c281078316c3`; submission, private review, attachments and autonomous-evidence capabilities passed the deployment verifier. The [14 October nightly run](https://github.com/DroneWuKong/drone-integration-handbook/actions/runs/38505274177) completed preparation, validation and publication successfully. The [13 October run](https://github.com/DroneWuKong/drone-integration-handbook/actions/runs/38341253326) published its update but failed deployment verification; the next run recovered. Its exact failure reason could not be inspected without authenticated job-log access.

## Reproduced defects and repairs

1. Betaflight, PX4 and INAV release feeds each exceed the reader's 4 MiB limit when requesting 100 releases. Smaller bounded pages now preserve the same history window. Firmware asset bodies are discarded after each page; the response limit and redirect rejection remain enforced. Live Betaflight verification retrieved 100 releases in 24 requests, taking 120.39 seconds. This increases public GitHub request traffic for large feeds, without creating paid research jobs.
2. The nightly run starts at 03:00 UTC while its self-hosted runner uses a local calendar date. Its 14 October run consequently wrote 13 October observation dates, including rows with 14 October GitHub push timestamps. Source monitoring, discovery, release comparisons and legacy research migration now use UTC dates. A midnight regression test verifies that an already published UTC release is accepted and a future release is excluded.
3. An unavailable emerging-project release check previously erased prior release information and rendered "none observed." It now preserves prior version/date information as a last observation, records check/observation dates separately, and explicitly renders an unavailable check. A first failed check is unknown, not evidence that no release exists; a recovered check replaces the stale state.

## Fresh source research

The official release feeds, checked on 14 October 2026, still identify these stable releases:

| Project | Stable release | Publication date (UTC) | Preview |
|---|---|---|---|
| [Betaflight](https://github.com/betaflight/betaflight/releases) | 2026.6.2 | 2026-09-16 | 2026.6.0-rc3 |
| [PX4](https://github.com/PX4/PX4-Autopilot/releases) | v1.17.0 | 2026-05-13 | v1.18.0-rc1 |
| [INAV](https://github.com/iNavFlight/inav/releases) | 9.1.0 | 2026-07-09 | 10.0.0-rc2 |

The ST STM32N6 and NXP i.MX 95 manufacturer pages were accessible through fresh web retrieval, although the nightly monitor reports them unavailable. This is an access-path discrepancy, not proof that the pages were removed or that their claims were reverified. Their existing factual review dates were preserved.

Related public repository checks found Forge updated on 14 October, while forge-data, the TAK bridge and Field-Kit retain their previously observed push dates. Private material continues to enter only through the existing sanitized public export. No discovered code was run.

## Verification and remaining limits

- 58 Python tests passed, including seven new regressions.
- Python compilation, 384 internal links, two-observer software replay, handbook build, generated-site checks, evidence/hold checks and review-queue generation passed.
- The existing two publication holds and 36 supported records were preserved. The inventory still contains 5,157 unreviewed records; this is not a complete semantic audit.
- Public autonomous status reports 20 abstentions, one contradiction and no accepted factual decisions. The repository-additions chapter and managed registry show no automatic promotions. These outcomes were not reset, relabeled or bypassed. Private packet diagnostics require authorized ledger access.
- No paid research requests were started and the non-renewing trial limits were unchanged.
- The full browser suite was not rerun locally for these Python maintenance changes. The latest deployed maintenance run's validation/browser step passed. CI and exact deployment verification remain required before publishing the patch.

## Future upkeep when access is unavailable

Preserve tested repairs as a patch, check whether main has advanced before resuming, and publish through the existing validation gate. Do not retry paid research without consulting the durable private ledger. Continue the recurring audit; public inspection remains useful while write access is unavailable.

## Deployment timing follow-up

The [post-merge run](https://github.com/DroneWuKong/drone-integration-handbook/actions/runs/38580912121) exhausted its twelve deployment checks at 14:32:44 UTC; Cloudflare completed at 14:32:46 UTC. The failure occurred before discovery or paid dispatch. Both deployment waits now allow twenty-four attempts with the same fifteen-second interval, still requiring the exact commit, public snapshot and durable capabilities. Preparation/publication job timeouts remain fifteen/ten minutes; failed verification cannot publish an unvalidated revision.

## Public inventory isolation

The [next run](https://github.com/DroneWuKong/drone-integration-handbook/actions/runs/38583117502) passed deployment verification, but its self-hosted handbook build was killed with exit code 137 before source discovery or paid dispatch. The public inventory build now runs on hosted Ubuntu and transfers only `site/assets/reference-data.json` to the cluster. The private job checks out that inventory's exact source commit, reads its public records, and retains all ledger credentials, packets and paid orchestration in the existing research pool. Full validation and fast-forward publication remain separate hosted jobs. No private files enter the inventory artifact.

## Metadata availability when the cluster is unavailable

The [inventory-isolated run](https://github.com/DroneWuKong/drone-integration-handbook/actions/runs/38586958744) built its public inventory successfully, but the private preparation job remained queued for over ten minutes. Public release/source/project upkeep now has its own hosted workflow and concurrency group. A separate private fact-research workflow follows successful trusted main-branch public runs and preserves the same research limits and independent exact-statement gate. It receives public snapshots/candidates/source fingerprints only, and publishes eligible factual edits only after full validation. A busy or offline cluster therefore defers fact research without preventing watchlist refreshes.
