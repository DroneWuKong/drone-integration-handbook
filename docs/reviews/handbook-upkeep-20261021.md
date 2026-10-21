# Handbook upkeep — 2026-10-21

## Result

The hosted public-maintenance workflow completed its prepare, validation, publication and exact-deployment checks on 2026-10-21. It refreshed all eight configured release feeds, the related-repository observations and the 12-entry emerging-project watchlist. No release feed or emerging-project search reported an error. The generated revision passed 58 Python tests, 30 JavaScript/API tests and the browser checks before publication.

The published release list did not identify a new stable version requiring a handbook section change. The source monitor attempted all 30 registered primary sources. It reported 28 reachable and two unavailable from its execution path: the STMicroelectronics STM32N6 series page and NXP i.MX 95 product page. Both official pages were separately retrieved on 2026-10-21, so the monitor result is an access-path discrepancy rather than evidence that either source was withdrawn. Their existing factual review dates and 2026-11-06 review due dates remain unchanged; no technical statement was altered from a reachability check.

## Related-repository addition

`DroneWuKong/Prismo-Calibration` is a public, non-archived repository whose public revision was observed on 2026-10-21. It is directly relevant to the handbook's sensor placement and calibration material added on 2026-10-18, but it was absent from the scheduled related-repository discovery configuration.

The maintenance configuration now reads only these public paths from that repository:

- `README.md`
- `apb/docs/ORQA_EDITION.md`
- `apb/docs/SENSOR_RECORDINGS.md`
- `apb/docs/MANUAL_ALIGNMENT.md`

Discovery treats their prose as attributed repository candidates. It does not execute the repository, import private files, accept repository metadata as hardware evidence, or bypass the independent exact-statement researcher/verifier gate.

## Independent fact-research status

No automatic factual statement was published in this upkeep. The private fact-research stage is waiting for its existing `self-hosted, prismo` runner; runs created from 2026-10-20 and 2026-10-21 have not reached the private durable ledger. The production status endpoint reports `live_research: false`, consistent with the non-renewing trial being inactive. This audit did not renew the trial, move private credentials to a hosted runner, retry an uncertain paid dispatch, or reset durable progress.

The two existing publication holds remain in place. The hosted public metadata workflow remains independent of this private-stage limitation.
