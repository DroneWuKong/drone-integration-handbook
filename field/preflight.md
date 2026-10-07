# Chapter 9: Preflight, Bench Checks and Flight Readiness

Use the aircraft and firmware manufacturer's checklist alongside this integration checklist. Record the exact airframe, battery chemistry, firmware and configuration. A short check cannot establish readiness after a repair or software change.

## Props-off bench checks

Remove **every propeller** before motor-output, receiver-loss or arming tests. Keep the aircraft secured, disconnect propulsion power before touching it, and follow the board/ESC manufacturer's test procedure. Never tilt an armed aircraft by hand or use a throttle blip as a ground control-direction test.

- Confirm board orientation and sensor directions in the configuration tool while disarmed.
- Verify receiver channels, mode assignments, arming switch and command ownership.
- Verify motor numbering and rotation using the firmware's documented props-off test facility.
- Save/read back the configuration and check battery monitoring against a reference instrument.
- Exercise documented link-loss and recovery behavior with props removed. Record receiver output on loss, firmware failsafe stage, selected action, timeout and reconnection behavior.

A bench test can establish output/state transitions. It cannot prove airborne landing, return, GPS rescue or obstacle clearance. Validate those separately through the aircraft's approved test procedure and suitable operating conditions. See [software failure testing](../integration/software-failure-testing.md) and [firmware recovery](../firmware/backup-upgrade-recovery.md).

## Before each flight

| Check | Evidence to look for |
|---|---|
| Structure and propulsion | Correct propeller variant/rotation, intact mounts and fasteners checked to manufacturer requirements; inspect while unpowered |
| Battery and power | Correct chemistry/cell count, condition, secure mounting, connector integrity, expected state of charge and monitor readings |
| Wiring and antennas | Strain relief, protected balance lead, intact connectors, correct radio antennas and sensor visibility |
| Configuration | Expected firmware/target, saved parameters, correct modes and documented failsafe action |
| Navigation | Required sensor/estimator health, fix quality, fresh home/origin and required mode prerequisites |
| RC/telemetry/video | Correct vehicle identity, current telemetry and a genuinely live image; advancing OSD alone does not prove live video |
| Operating area | People, clearance, weather, airspace/spectrum permissions and aircraft-specific operating limits |
| Logs and recovery | Storage available, emergency controls understood and recorded configuration available |

Satellite count alone is not a navigation quality test. Use the installed firmware's fix, estimator and arming requirements. Battery internal resistance depends on pack construction, temperature, state of charge and measurement method; trend like-for-like measurements and use manufacturer retirement criteria. The former universal resistance thresholds and satellite minimum are withdrawn.

## Failsafe is a configuration-specific choice

Betaflight documents different Stage 2 procedures, including Drop, Landing and GPS Rescue. ArduPilot and PX4 have different mode, sensor and link prerequisites. A failsafe action appropriate for one aircraft or location may be unsuitable for another. Read the exact release's documentation; do not substitute a universal action from this handbook.

[Betaflight failsafe documentation](https://betaflight.com/docs/wiki/guides/current/Failsafe), checked 2026-10-07. This reference explains firmware behavior; it does not validate a particular installation.

## After flight or repair

Disarm and disconnect propulsion power before handling. Inspect damage, unusual heating, connectors and battery condition using manufacturer limits. Preserve logs before they are overwritten, note configuration changes, and return to bench validation after repairs, receiver changes, firmware upgrades or altered failsafe settings. Charge and store batteries using the exact chemistry manufacturer's guidance.

Use the [evidence record](evidence-record.md) to retain what was actually checked and what remains open.
