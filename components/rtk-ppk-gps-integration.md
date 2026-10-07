# RTK / PPK GNSS Integration

**Source scope:** ArduCopter **4.7.1**, released 2026-09-03; parameter definitions checked 2026-10-07. Other vehicle types/releases and receiver interfaces need their own parameter reference. RTK provides a solution during operation; PPK processes recorded observations afterward. Neither a FIX flag nor a receiver specification proves final map accuracy.

## Versioned parameter reference

The following are lookup values, not a configuration to paste into an unknown aircraft. Read existing values first and match the board's logical serial-port map, receiver output protocol and firmware.

| Parameter | Documented meaning in Copter 4.7.1 |
|---|---|
| `GPS1_TYPE = 1` | AUTO |
| `GPS1_TYPE = 2` | Ordinary u-blox driver |
| `GPS1_TYPE = 17 / 18` | u-blox moving-baseline base / rover; not the ordinary driver |
| `GPS1_TYPE = 15` | NOVA; not a generic Emlid setting |
| `SERIAL3_PROTOCOL = 5` | GPS on logical Serial 3, if that port is the receiver connection |
| `SERIAL3_BAUD = 230` | 230400 baud documented code; `115` denotes 115200 |
| `GPS_INJECT_TO = 0 / 1 / 127` | First GPS / second GPS / all GPS destinations for `GPS_INJECT_DATA` |
| `GPS1_GNSS_MODE = 0` | Leave receiver constellation configuration as configured; not “enable all” |

`GPS1_INJECT_TO` and `GPS1_GNSS` are not the documented parameter names. Emlid configuration depends on exact receiver/output mode, rather than the vendor name alone. Antenna position offsets are measured installation geometry in the defined body frame, not universal values.

[ArduPilot 4.7.1 parameter reference](https://ardupilot.org/copter/docs/parameters-Copter-stable-V4.7.1.html) — sections GPS1_TYPE, GPS_INJECT_TO, GPS1_GNSS_MODE, SERIAL3_PROTOCOL and SERIAL3_BAUD. [GPS for yaw](https://ardupilot.org/copter/docs/common-gps-for-yaw.html) documents the separate moving-baseline use case.

## Corrections and reference coordinates

NTRIP transports correction streams over a network; the caster, mountpoint, message set and correction age matter. [NOAA OPUS](https://geodesy.noaa.gov/OPUS/) is an observation-file post-processing service, not a real-time NTRIP caster. Follow the receiver/GCS integration documentation for correction delivery; do not assume an arbitrary message rate establishes freshness.

[ArduPilot RTK correction reference](https://ardupilot.org/copter/docs/common-rtk-correction.html), checked 2026-10-07.

## Retain the survey provenance

Record base coordinate source, datum/reference frame, epoch, ellipsoidal versus orthometric height, geoid model, antenna type/height, base-rover observation overlap, correction age, solution flags and raw observations. A survey-in average does not establish known absolute coordinates with a universal accuracy.

Record camera event timing, antenna-to-camera lever arm, boresight/calibration, processing software/settings and independent checkpoint residuals. Checkpoints used for validation must remain separate from points used to constrain the adjustment. Choose acceptance criteria and sampling under the applicable project/survey standard; this handbook supplies no universal centimeter guarantee or checkpoint count.

See [time and coordinates](../integration/time-and-coordinate-provenance.md), [RTK versus PPK](rtk-ppk-the-real-story.md) and the [evidence record](../field/evidence-record.md).
