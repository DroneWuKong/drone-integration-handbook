# Maintenance recovery review — 2026-11-25

## Findings and repair

The public metadata workflow and private factual workflow both completed successfully in the inspected runs (`45538061680` and `45538845642`). Successful workflow execution did not mean the overdue factual reviews had been verified: ten source reviews were still due from 2026-11-06, and the private preparation stage started no paid jobs under the existing non-renewing trial gate.

The backend and audit CLI already supported recovery of existing jobs, but `evidence-facts.yml` did not call that recovery route. The private workflow now reconciles existing work before factual promotion, checks that paid reservations are unchanged, and skips new paid dispatch when the original trial/configuration/workload gate is closed. No paid replacement requests, reservation refunds, trial renewal or new credentials are introduced. Retrieval failures remain visible and unresolved rather than being converted into verified evidence.

Regression coverage verifies call order, the existing-only confirmation, unchanged reservation totals, redaction of response IDs and closed-gate behavior. Existing backend recovery/adjudication tests remain required.

## Release-review additions

- ArduCopter 4.7.3 was published on 2026-11-19; the handbook's covered version remains 4.7.1. Added the [tagged release notes](https://github.com/ArduPilot/ardupilot/blob/Copter-4.7.3/ArduCopter/ReleaseNotes.txt) as a research lead. The notes' internal release heading date and GitHub publication timestamp are distinct observations.
- PX4 v1.18.0 was published on 2026-11-24; the handbook's covered version remains v1.17. Added the [versioned v1.18 release page](https://docs.px4.io/v1.18/en/releases/1.18) and [covered-version Offboard documentation](https://docs.px4.io/v1.17/en/flight_modes/offboard) as comparison sources.

These leads now reach specifications for affected chapters and are shown in the published status chapter. They do not advance factual verification dates or bypass the independent exact-statement gate. No hardware performance claims were inferred from release or repository metadata.

## Retrieval diagnostics and remaining limits

The source monitor now records successful retrieval dates and precise HTTP/error classes while preserving previous digests on failures. It clears stale HTTP codes after a different failure or recovery. ST/NXP retrieval failures and overdue source reviews are not marked resolved merely because the workflow or a browser can access other pages.

Public repository discovery remains public-only. Private material continues through the existing sanitized export route; publication holds and exact-statement policies are unchanged. The public release and emerging-project feeds were healthy in the inspected run, so no speculative hardware capability or unverified project endorsement was added.

Primary release metadata: [ArduCopter 4.7.3](https://github.com/ArduPilot/ardupilot/releases/tag/Copter-4.7.3), [PX4 v1.18.0](https://github.com/PX4/PX4-Autopilot/releases/tag/v1.18.0). This repair does not authorize renewed paid research or claim that all overdue content is fact-checked.
