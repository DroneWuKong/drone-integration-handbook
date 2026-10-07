# Chapter 5: Four Flight Controller Firmware Ecosystems

This guide covers Betaflight, INAV, ArduPilot and PX4. Select an exact board target, firmware version and matching configuration application. A protocol name alone does not establish support for a particular message, sensor or vehicle.

## Functional requirements

| Requirement to verify | Project documentation to check | Acceptance record |
|---|---|---|
| Manual rate control, altitude/position hold or rescue | Betaflight release/build options and mode documentation | Exact target, enabled features, required sensors and configured recovery behavior |
| Navigation and mission functions on the intended vehicle | INAV release and target documentation | Vehicle support, configurator compatibility and mission/mode limits |
| Vehicle-specific mission, sensor and peripheral integration | ArduPilot vehicle/version documentation | Exact vehicle firmware, parameter names, units and defaults |
| Companion/offboard integration | PX4 versioned Offboard and interface documentation | Supported message/frame, prerequisites, timeout and loss behavior |

This is a requirements checklist. It does not rank flight feel, community size, safety or compatibility.

## Betaflight

Betaflight 2025.12 introduces Altitude Hold and Position Hold when included in the build. GPS is required for Position Hold and a magnetometer is strongly recommended in the project's documentation. GPS Rescue, position holding and waypoint missions are distinct capabilities. Check the current release rather than extrapolate from older descriptions.

The Betaflight App is a web application with platform-specific packaging; it replaces the former Chrome-app description. Match the app/firmware compatibility table and release channel. The release watchlist separately records newer versions whose capabilities require checking.

MSP provides versioned message/command interfaces; CLI configuration backups such as `diff all` and `dump all` have different scope. Preserve the original firmware/defaults and read back migrated configuration after an upgrade.

Sources checked 2026-10-07: [2025.12 Position Hold](https://betaflight.com/docs/wiki/guides/current/Position-Hold-2025-12), [App guide](https://betaflight.com/docs/wiki/app), and [official releases](https://github.com/betaflight/betaflight/releases). These establish the stated feature/version scope rather than compatibility with every board.

## INAV

INAV publishes firmware, board targets and a matching configurator through its project repositories. Consult the exact release notes for supported vehicles, navigation modes, sensors and MSP interfaces. Do not transfer Betaflight CLI commands or defaults merely because both projects expose MSP and a CLI.

[INAV project documentation](https://github.com/iNavFlight/inav) and [Configurator releases](https://github.com/iNavFlight/inav-configurator/releases). The [release watchlist](../field/update-status.md) separates stable releases from release candidates.

## ArduPilot

ArduPilot documentation and parameters are vehicle- and version-specific. Use the selected vehicle's parameter reference and board documentation. Parameter counts vary with the build and are not a measure of integration capability.

MAVLink supports published telemetry and request/command services. Stream-rate control depends on the firmware and MAVLink interface instance; it does not map universally to a physical UART. Verify message support, addressing, units, frames and command acknowledgements separately.

[ArduPilot vehicle documentation](https://ardupilot.org/ardupilot/index.html), [message-rate requests](https://ardupilot.org/dev/docs/mavlink-requesting-data.html), and [Copter 4.7.1 parameter reference](https://ardupilot.org/copter/docs/parameters-Copter-stable-V4.7.1.html), checked 2026-10-07. See [GNSS integration](../components/rtk-ppk-gps-integration.md) for the scoped parameter audit.

## PX4

PX4 has versioned board, vehicle and interface documentation. Its Offboard mode requires the documented proof-of-life stream and valid estimator/control prerequisites. Message support, reference frames and loss behavior must match the selected release. Main-branch documentation can describe unreleased changes.

[PX4 v1.17 Offboard](https://docs.px4.io/v1.17/en/flight_modes/offboard), checked 2026-10-07. See [multiclient telemetry](../integration/secure-multiclient-telemetry.md) for observer versus command-owner boundaries.

## Upgrade and integration checks

- Record board revision, exact firmware/application versions, enabled features and configuration exports.
- Match sensor/interface support to the exact build, with electrical levels and pinout checked separately.
- Preserve logs and test the configuration/recovery path in software and on a propeller-free bench before field acceptance.
- Use [backup and recovery](backup-upgrade-recovery.md), [software failure replay](../integration/software-failure-testing.md), [UART layout](uart-layout.md), and [MAVLink](mavlink-protocol.md).

A changed release opens a new check; it does not authorize copying parameters or changing an aircraft automatically.
