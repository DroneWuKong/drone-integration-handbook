# AI Wingman on the Orqa DTK APB

> How the AI Wingman analysis stack runs on top of what the Orqa DTK APB
> (IS-0001) already provides. Cross-reference:
> [Orqa Hardware Guide](../components/orqa-hardware-guide.md).

---

## What the APB already gives you

The DTK APB is an integrated stack, not a separate FC + companion:

| Subsystem            | Hardware         | Runs              |
|----------------------|------------------|-------------------|
| Flight controller    | STM32H7          | PX4               |
| Companion computer   | NXP i.MX8M Plus  | Linux             |
| AI inference         | 2.3 TOPS NPU     | (application)     |
| FC↔companion link    | On-board bridge  | MAVLink, Ethernet |
| External I/O         | JST-GH (Pixhawk) | —                 |

Because the MAVLink bridge between the H7 and the i.MX8M is built into the
board, there is no extra wiring to add. Anything running on the Linux side
can subscribe to the PX4 stream directly.

## Where Wingman lives

```
            ┌───────────────────────┐
            │  STM32H7 — PX4          │
            │   • IMU, mixer, control │
            │   • MAVLink streams     │
            └──────────┬──────────────┘
                       │ on-board bridge (UDP 14540)
            ┌──────────▼──────────────┐
            │  i.MX8M Plus — Linux    │
            │   wingman-apb (service) │   ← signal processing (CPU)
            │     • MavlinkUdpSource  │
            │     • FlightSampleBuffer│
            │     • wingman-analysis  │
            │     • HTTP :8088         │
            │                         │
            │   AI Brain / vision     │   ← inference (NPU)
            └────────────────────────┘
```

Two planes of work on the companion:

1. **CPU plane (`wingman-apb`)** — deterministic DSP. FFT/PSD, step response,
   phase latency, PID error by throttle. This is `wingman-analysis` from the
   AI Project, hosted as a Kotlin JVM service.
2. **NPU plane** — quantized models that *consume* the features the CPU
   plane computes (the interpretive "AI Brain," plus `wingman-vision`
   detection / terrain classification). NPUs are poor at FFTs and good at
   CNN / transformer inference — keep the split.

## Data path

PX4 publishes the relevant streams out of the box:

| MAVLink message           | Feeds                                   |
|---------------------------|-----------------------------------------|
| `HIGHRES_IMU`             | `FlightSample.gyroFiltered/Unfiltered`  |
| `ATTITUDE_SETPOINT`       | `FlightSample.setpoint`                 |
| `ACTUATOR_CONTROL_TARGET` | `FlightSample.motors`, `throttlePercent`|
| `HEARTBEAT` + `AUTOPILOT_VERSION` | `FlightMetadata.firmware / version` |

The companion service subscribes on `udp://127.0.0.1:14540` (PX4 default on
the APB bridge), decodes the frames, and appends `FlightSample`s to a rolling
buffer. Analyses run over that window — not over full-flight `.ulg` logs.

## Preset selection by phase of flight

| Phase        | Preset     | Why                                              |
|--------------|------------|--------------------------------------------------|
| Armed, pre-takeoff | `QUICK`    | Only PID error by throttle. Cheap, runs every 10 s. |
| In flight    | `QUICK`    | Same. Do **not** run heavier presets in flight.  |
| Post-landing | `STANDARD` | Spectra, step response, phase latency.           |
| On ground, triggered | `DEEP`     | Time spectrograms, Bode, filter sim. Operator pull. |
| Uplink handoff | `FLEET`    | Batch summary to Command.                        |

The APB companion isn't a laptop. `DEEP` on an i.MX8M is only safe with the
vehicle disarmed and on the ground.

## Wiring notes

- **No extra wiring.** The FC↔companion link is on-board. External integrators
  don't need to route a second MAVLink cable the way they would on a
  Pixhawk + Jetson stack.
- **Power.** The APB delivers both FC and companion rails; don't feed the
  companion from a separate BEC.
- **Link timing.** PX4 streams at 250 Hz by default for `HIGHRES_IMU`.
  Bump `MAV_0_RATE` on the bridge if you want 1 kHz into `wingman-apb` —
  spectral analyses below 500 Hz are fine at 250 Hz, but step response
  quality improves with higher sample rate.
- **NDAA.** APB is Croatian (EU) origin. Same procurement notes as the rest
  of the Orqa line — see the hardware guide.

## Exposed surface

The service opens a local HTTP surface so Hangar / Buddy / Command can pull
results:

```
GET  http://<apb>:8088/health
GET  http://<apb>:8088/analysis/latest
POST http://<apb>:8088/analysis/run?preset=STANDARD
```

Results are a compact JSON projection of `FlightAnalysis` — headline metrics
only (step-response overshoot / settling, mean PID error, noisiest motor,
dominant noise frequency). Full spectra / spectrogram matrices stay on the
vehicle; pull the full `FlightAnalysis` over the uplink only when an operator
asks for it.

## Reference implementation

Scaffold module: [`ai-project/apb/`](https://github.com/DroneWuKong/Ai-Project/tree/claude/wingman-apb-integration-SgtHN/apb).

Key files:

- `apb/build.gradle.kts` — Kotlin JVM + `application`, depends on
  `:wingman-analysis` via `includeBuild`.
- `apb/src/main/kotlin/ai/wingman/apb/Main.kt` — process entry; wires
  source → buffer → runner → HTTP.
- `apb/src/main/kotlin/ai/wingman/apb/mavlink/MavlinkUdpSource.kt` — UDP
  MAVLink reader; MAVLink v2 decode body is `TODO` for the next commit.
- `apb/src/main/kotlin/ai/wingman/apb/service/AnalysisRunner.kt` — calls
  `FlightAnalyzer.analyze(samples, metadata, preset)`.
- `apb/deploy/wingman-apb.service` — systemd unit.

## Related

- [Orqa Hardware Guide](../components/orqa-hardware-guide.md)
- [Companion Computers](../components/companion-computers.md)
- [The Four Firmwares](../firmware/four-firmwares.md)
