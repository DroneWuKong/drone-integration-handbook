# Secure Multi-Client Telemetry

Multiple observers can read telemetry without granting each observer command authority. System/component IDs identify message sources; they are not authentication or permission grants.

## Connection contract

| Concern | Explicit contract |
|---|---|
| Identity | Distinct system/component IDs, discovered target and reconnect/session identity |
| Ownership | One configured command owner; observers cannot acquire authority by receiving data |
| Routing | Defined endpoints, loop prevention and protocol-aware deduplication |
| Rates | One stream-rate policy; record when another client changes it |
| Security | Key provisioning, signing acceptance, protected transport and secret handling |
| Freshness | Per-message age, source clock and unknown/stale state |

MAVLink v2 signing authenticates packets using shared-key and replay/timestamp rules. It does not encrypt telemetry. An installation must also define unsigned-packet acceptance and transport protection. [MAVLink signing](https://mavlink.io/en/guide/message_signing.html) and [routing](https://mavlink.io/en/guide/routing.html), checked 2026-10-07.

## Software observer exercise

`python3 scripts/check_integration_replay.py` fans one local fixture to two observers and compares their recorded states. It exercises stale data, reordering and reboot identity without opening a device or network endpoint. The fixture grants no command authority. A real router/GCS needs separate tests for command routing, signatures, reconnects and stream-rate contention.

For ArduPilot, `SRx_*` is indexed by MAVLink instance, rather than universally by `SERIALx`. Prefer a documented per-message interval interface where supported. [ArduPilot stream requests](https://ardupilot.org/dev/docs/mavlink-requesting-data.html), checked 2026-10-07.

Keep test keys out of production and credentials out of public logs. See [software failure testing](software-failure-testing.md).
