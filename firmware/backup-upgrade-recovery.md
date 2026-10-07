# Firmware Backup, Upgrade and Recovery

An upgrade changes a versioned configuration contract. Preserve enough evidence to restore the previous tested state rather than assume a parameter dump transfers across versions.

## Change record

| Record | Preserve |
|---|---|
| Identity | Board target/revision, bootloader, aircraft ID and attached peripherals |
| Software | Installed firmware version/hash, configurator/GCS version, build options and release date |
| Configuration | Full readback, differences from defaults, calibration/mixer/mode/serial assignments |
| Recovery | Exact known-good image, documented bootloader/recovery path and recovery prerequisites |
| Validation | Before/after readback, changed/removed parameters and unresolved tests |

For Betaflight, `dump all` and `diff all` provide different views; retain the version/target with the output. Do not paste an old dump into a different target or release without migration checks. [Betaflight CLI reference](https://betaflight.com/docs/wiki/guides/current/Command-Line-Interface), checked 2026-10-07.

## Software rehearsal

Use an isolated configuration and simulator/replay where available. Compare parameter names, types, units and accepted values; a missing or clamped value is a migration result to investigate. Interrupt an upload in a software adapter and verify that partial state is not reported as a complete backup. Reconnect and read back rather than infer persistence from a successful send.

Hardware flashing and bootloader recovery follow the exact board/firmware documentation with propulsion disabled. A simulator cannot establish USB bootloader behavior or motor-output correctness. After a real change, run [props-off bench checks](../field/preflight.md) and the applicable aircraft acceptance procedure before operation.

Track upstream release dates and relevant migration notes in the [update watchlist](../field/update-status.md). [ArduPilot firmware reference](https://ardupilot.org/copter/docs/common-loading-firmware-onto-pixhawk.html), checked 2026-10-07.
