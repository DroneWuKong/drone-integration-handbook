# RTK versus PPK — Evidence and Workflow

RTK estimates corrected GNSS positions in real time. PPK processes recorded rover observations with suitable reference observations afterward. The choice depends on correction availability, recording capability, event timing, processing support and the project's accuracy requirements.

## Distinguish solution quality from deliverable quality

A fixed ambiguity solution is a receiver/processor state, not independent proof of final map accuracy. Correction loss, multipath, observation gaps, reference-coordinate error and camera timing can degrade the result. PPK can use observations unavailable to a real-time solution, but it cannot recover measurements that were never recorded or guarantee recovery through every blockage.

| Workflow | Evidence required |
|---|---|
| RTK | Correction source and age, receiver/firmware, epoch-by-epoch quality and camera event linkage |
| PPK | Overlapping rover/base raw observations, supported formats and processor version/settings |
| Combined | Confirm that the exact aircraft actually records exportable raw data while applying corrections |
| Absolute survey | Reference frame/datum, epoch, coordinate provenance, height/geoid model and independent checkpoints |

Logging rates need to meet the receiver/processor's requirements; equal base and rover sample rates are not a universal prerequisite. Initialization time and usable baseline depend on receiver, satellite geometry, environment and solver. The former universal duration/baseline thresholds, unsourced Matrice 4E diagnosis and software-price recommendations are withdrawn.

## Camera timing and geometry

An illustrative timing error of **50 ms at 10 m/s** produces **0.5 m** of along-track position discrepancy (`speed × time`). This is a dimensional example, not an assertion about a particular camera. Establish exposure/event timing from the exact hardware and logs; EXIF time alone does not establish that alignment. Apply the measured antenna-to-camera lever arm in the appropriate attitude/frame.

[claim:survey-timing-example]

Preserve raw observations, event records, coordinate metadata, processing settings and residuals. Validate against independent checkpoints under the project standard, rather than rely solely on FIX percentages. See [GNSS integration](rtk-ppk-gps-integration.md) and [time/coordinate provenance](../integration/time-and-coordinate-provenance.md).

Primary references checked 2026-10-07: [ArduPilot RTK correction workflow](https://ardupilot.org/copter/docs/common-rtk-correction.html), [NOAA OPUS](https://geodesy.noaa.gov/OPUS/) and [NOAA geodetic reference information](https://geodesy.noaa.gov/).
