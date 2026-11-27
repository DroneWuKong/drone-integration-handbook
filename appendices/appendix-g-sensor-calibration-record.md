# Appendix G — Sensor Installation and Calibration Record

Copy or print this record for each installation revision. Use **unknown**, **estimated**, **not checked** or **not applicable** explicitly. Start with [Sensors and Calibration](../integration/sensors-and-calibration.md) for definitions and examples.

## Installation identity

| Field | Record |
|---|---|
| Installation ID / revision / date | ______________________________ |
| Aircraft and intended use | ______________________________ |
| Sensor roles, models, serials and hardware revisions | ______________________________ |
| Firmware, driver, estimator and calibration-tool versions | ______________________________ |
| Mount/bracket revision and installation photos | ______________________________ |
| Lens, focus, zoom, crop, image dimensions and pixel model | ______________________________ |
| Operating conditions and required performance | ______________________________ |
| Previous configuration and recovery location | ______________________________ |

## Geometry: one entry for each sensor relationship

Draw the aircraft nose, the origin and the positive axes. Label the actual measurement reference points on the installation photos. Use the same named relationship throughout measurement, fitting and export.

| Field | Record |
|---|---|
| Reference frame / origin / physical reference point | ______________________________ |
| Sensor frame / origin / physical reference point | ______________________________ |
| GNSS ARP / antenna-radome model / applied phase-center model | ______________________________ |
| Reference +X / +Y / +Z physical directions | ______________________________ |
| Sensor +X / +Y / +Z physical directions | ______________________________ |
| Lever-arm direction: from ___ to ___, expressed in ___ | ______________________________ |
| Signed X / Y / Z and units | ______________________________ |
| Method, instrument, uncertainty and inaccessible origins | ______________________________ |
| Nominal mount orientation and residual boresight | ______________________________ |
| Full rotation convention and units | Matrix direction, quaternion order or Euler order: __________ |
| Transform equation used by the consumer | ______________________________ |
| Rigid assembly or moving gimbal / joint-state convention | ______________________________ |
| Where rotation and offset compensation are each applied | Driver / estimator / processing stage: __________ |

**Sign check:** describe a known point above, forward and to the right of the chosen origin, and predict its coordinates before reading software output. Explain any conversion between FRD, FLU, optical, ENU or NED frames.

## Acquisition and timing

| Field | Record |
|---|---|
| Target type, measured dimensions, flatness and scale check | ______________________________ |
| Target square count / inner-corner count / ordered origin | ______________________________ |
| Raw input filenames / hashes / storage location | ______________________________ |
| Training set and genuinely fresh check set identities | ______________________________ |
| Image and IMU sample rates, units and missing samples | ______________________________ |
| Timestamp event definition for each stream | Exposure start/midpoint / sampling / receipt / unknown: __________ |
| Shutter type and row readout timing, where applicable | ______________________________ |
| Clock domains, synchronization and reboot/drift behavior | ______________________________ |
| Estimated time-shift equation, sign and units | ______________________________ |
| Temperature, lighting, motion coverage and fixed settings | ______________________________ |
| Physical / synthetic / unknown input provenance | ______________________________ |

## Candidate and validation

| Field | Record |
|---|---|
| Acceptance criteria chosen before fitting | ______________________________ |
| Calibration candidate ID and full result location | ______________________________ |
| Fresh-data checks and observations excluded from fitting | ______________________________ |
| Independent reference, method and its uncertainty | ______________________________ |
| Residuals, repeatability, spatial coverage and outliers | ______________________________ |
| Physical plausibility against measured geometry | ______________________________ |
| Passed / failed / inconclusive, and remaining limits | ______________________________ |

A successful fit or fresh-data check does not establish physical accuracy by itself. Keep software checks, independent measurements, destination checks and aircraft qualification as separate recorded outcomes.

## Application and change control

- [ ] Confirm the destination supports this model and retains every required coefficient.
- [ ] Check transform direction, axes, units, quaternion/Euler order and timing sign.
- [ ] Save the prior configuration and record the exact export and destination version.
- [ ] Read back the loaded settings or effective processing configuration.
- [ ] Confirm that each rotation and offset correction is applied at its intended stage.
- [ ] Complete documented bench checks and the aircraft's separate commissioning process.
- [ ] Record the operator/reviewer, evidence locations and any unresolved requirements.

Application status: __________. Bench result: __________. Physical/timing validation: __________. Aircraft qualification status: __________. Responsible person/date: __________.

Revisit affected entries after movement, repair, impact, changed optics/image geometry, firmware/driver changes or altered timing. Preserve this record and create a new revision. Attach it to the broader [Integration and Field Evidence Record](../field/evidence-record.md).
