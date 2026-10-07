# Software-Only Integration and Failure Testing

Use simulation and replay to test parser, freshness, routing and state-transition contracts before connecting hardware. Pin the firmware/source revision and keep simulated observations visibly labeled.

## Reproducible test record

Retain the input fixture/hash, simulator version, application revision, configuration, clock model, expected result and observed output. [ArduPilot SITL setup](https://ardupilot.org/dev/docs/SITL-setup-landingpage.html) and [PX4 simulation](https://docs.px4.io/main/en/simulation/) describe simulator entry points; choose a released version rather than silently follow development `main`.

| Injected condition | Contract to inspect |
|---|---|
| Stale telemetry | Age advances; last known values do not become fresh merely because the UI redraws |
| Link loss/reconnect/flapping | Vehicle identity, ownership and reconnect state remain explicit |
| Duplicate/reordered packets | Counters and state updates reflect the protocol's sequence semantics |
| Clock jump/reboot | Boot-relative, UTC and monotonic times are not mixed |
| Sensor disagreement/frame mismatch | Invalid or inconsistent inputs remain observable |
| Partial parameter download | Missing indices stay missing; no complete-backup claim |
| Video freeze with live OSD | Video freshness and telemetry freshness are tracked separately |

## Included software exercise

Run `python3 scripts/check_integration_replay.py`. It uses local fixtures and two read-only observers, injects stale/reordered/reboot samples, and emits machine-readable observations. It opens no network socket, arms no aircraft and writes no device configuration. Passing proves only the included replay contract.

A public example of this boundary exists in the publisher's [TAK Bridge software demo](https://github.com/DroneWuKong/MultiProtocol-UAS-TAK-Bridge): its simulated positions remain local. Verify the current source/release before extending that behavior to another application.

Separate **simulation**, **props-off bench** and **field observation** in every evidence record. See [telemetry ownership](secure-multiclient-telemetry.md) and [evidence records](../field/evidence-record.md).
