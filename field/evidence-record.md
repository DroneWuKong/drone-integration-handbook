# Integration and Field Evidence Record

Print or copy this worksheet into the existing **Report / add field evidence** flow. Keep unknown values explicit. A configuration drawing, simulation or manufacturer statement is a different evidence category from a measured installation.

## Wiring and configuration record

| Field | Record |
|---|---|
| Date and purpose | Observation time/timezone and exact question |
| Hardware | Aircraft/board/peripheral model and revision; module versus assembled board |
| Software | Firmware/image/GCS versions, release dates, source hashes and build options |
| Connection | UART logical/physical mapping, TX/RX/GND and measured logic levels; CAN protocol/pinout/termination separately |
| Power | Rail voltage, measured steady/transient demand, converter and thermal conditions |
| Radio/video | Antennas, legal operating mode, packet/channel/codec settings and measurement boundary |
| Expected/observed | Procedure, result, units, sample distribution and uncertainty |
| Evidence | Original logs/captures, configuration readback and artifact hashes |
| Limits | Simulation/bench/field category, untested cases and relevant relationship |

Do not use a UART drawing as a CAN wiring map or infer logic voltage from supply voltage. Resolve pinouts against exact board documentation. The [UART chapter](../firmware/uart-layout.md) and [CAN reference](../firmware/can-dronecan-cyphal.md) provide separate record structures.

## Log comparison

Keep an untouched original. Correlate flight-controller, companion, radio and video records using documented clock/frame transforms. Note resets, missing samples, sample rates, filter/config changes and overwrite behavior. A log screenshot without configuration and time provenance may not support the claimed cause.

Use [Blackbox Logs](blackbox.md), [time/coordinates](../integration/time-and-coordinate-provenance.md) and [software failure testing](../integration/software-failure-testing.md). Reports remain private until separately published under the handbook's evidence and rights rules.
