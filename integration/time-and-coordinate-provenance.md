# Time, Coordinates and Survey Provenance

A position without its reference frame and timestamp cannot be reliably joined to another sensor record.

| Value | Preserve with it |
|---|---|
| UTC/GNSS time | Time scale, leap-second handling, synchronization method and uncertainty |
| Monotonic/boot time | Clock origin, units, reboot/session identity and rollover handling |
| Global altitude | Ellipsoidal or orthometric/MSL height, datum and geoid model |
| Relative altitude | Home/origin definition and reset/change events; not automatically terrain AGL |
| Local position | ENU/NED convention, estimator origin, units and reset events |
| Body vector | Axis convention, orientation, sensor-to-body transform and lever arm |

MAVLink `GLOBAL_POSITION_INT.relative_alt` is altitude above home. `LOCAL_POSITION_NED` uses the local NED reference. `TIMESYNC` estimates timing offsets between communicating systems; firmware/message-version support and clock behavior still need checking. [MAVLink common definitions](https://mavlink.io/en/messages/common.html) and [TIMESYNC service](https://mavlink.io/en/services/timesync.html), checked 2026-10-07.

PPS, PTP, NTP and a camera event signal serve different timing contracts. Receipt time is not exposure time. Test clock steps, reboot, missing synchronization and future/stale samples in replay. A live heartbeat cannot refresh an old position or video frame.

For a survey, retain reference-frame realization and epoch, base coordinate provenance, antenna height/type, raw observation overlap, correction age, camera event records, lever arm, boresight and independent checkpoint residuals. [NOAA geodetic resources](https://geodesy.noaa.gov/) and [OPUS](https://geodesy.noaa.gov/OPUS/), checked 2026-10-07.

See [RTK/PPK integration](../components/rtk-ppk-gps-integration.md), [video diagnostics](video-pipeline-troubleshooting.md) and [evidence records](../field/evidence-record.md).
