# Chapter 5: The Four Firmwares

> There are four flight controller firmware ecosystems that matter.
> Each one is the right choice for somebody and the wrong choice
> for somebody else. This chapter helps you figure out which.

---

## The Landscape

| Firmware | Protocol | Built For | License |
|----------|----------|-----------|---------|
| Betaflight | MSP v2 | FPV racing, freestyle, acro | GPL-3.0 |
| iNav | MSP v2 | GPS navigation, fixed-wing, VTOL | GPL-3.0 |
| ArduPilot | MAVLink v2 | Autonomous missions, survey, commercial | GPL-3.0 |
| PX4 | MAVLink v2 | Research, defense, companion compute | BSD-3 |

All four are open-source. All four run on STM32 flight controllers.
All four are actively developed. None of them are going away.

---

## Betaflight

**What it does well:** Rate-mode acrobatic flight. Sub-millisecond
gyro loop. The tightest, most responsive flight controller stack
for manual piloting. If you're flying FPV by hand and you want
the sticks to feel like an extension of your body, Betaflight.

**What it doesn't do:** Autonomous anything. No waypoint missions,
no GPS hold (angle mode with GPS rescue is a failsafe, not a
flight mode), no companion computer integration beyond MSP bridge,
no offboard control. Betaflight assumes a human is flying at all times.

**Protocol:** MSP v2. Binary request/response over serial. Simple,
fast, well-documented. Every message has a function code and a
payload. Read PID values, write PID values, download blackbox,
read sensor state. No streaming — you ask, it answers.

**Configuration:** Betaflight Configurator (Chrome app) or CLI.
The CLI is powerful — `diff all` gives you a complete delta from
defaults, `dump all` gives you everything. Most experienced
operators work in CLI.

**Typical platforms:** 5-inch freestyle quads, 3-inch cinewhoops,
racing drones, micro quads, FPV wings (with limitations).

**Community:** Massive. Largest FPV firmware community. Fast
development cycle. Frequent releases. Sometimes too frequent —
breaking changes between minor versions are common.

**When to choose it:** Your primary control input is a human with
a transmitter. You need the best possible manual flight feel.
You don't need autonomous modes, waypoints, or programmatic control.

---

## iNav

**What it does well:** GPS navigation on everything. Multi-rotor,
fixed-wing, VTOL, rovers, boats. If it moves and you want it to
follow waypoints or hold position, iNav probably supports it.
iNav is what Betaflight would be if Betaflight cared about navigation.

**What it doesn't do:** It doesn't have ArduPilot's depth of
autonomous mission planning or PX4's companion computer integration.
It's a step up from Betaflight toward autonomy, but it's not a
full autopilot stack.

**Protocol:** MSP v2 with extensions. Same wire format as Betaflight,
but with additional messages for navigation, waypoints, and
mission planning. iNav also supports MSP2_COMMON_SETTING for
named parameter access — cleaner than Betaflight's CLI-only
approach for many settings.

**Configuration:** iNav Configurator (forked from Betaflight
Configurator, same Chrome app pattern). CLI is similar but not
identical to Betaflight — don't assume commands transfer 1:1.

**Typical platforms:** Long-range FPV with GPS return, survey wings,
fixed-wing platforms, VTOL (tiltrotor, tailsitter), autonomous
boats, GPS-guided multicopters.

**Community:** Smaller than Betaflight, deeply knowledgeable.
Fixed-wing and VTOL support is stronger than any other open-source
option except ArduPilot.

**When to choose it:** You need GPS navigation and you're coming from
the FPV world. You want something more capable than Betaflight but
less complex than ArduPilot. You're building a fixed-wing or VTOL
and don't want to learn the ArduPilot parameter universe.

---

## ArduPilot

**What it does well:** Everything. Multi-rotor, fixed-wing, helicopter,
rover, submarine, boat, antenna tracker, blimp. ArduPilot is the
Swiss Army knife of autopilots. It has more flight modes, more
parameters, more sensor support, and more mission planning capability
than any other open-source firmware.

**What it doesn't do well:** Simple. ArduPilot has ~1,200 parameters.
The learning curve is real. The documentation is extensive but
assumes you know what you're looking for. If you just want to fly
a 5-inch quad freestyle, ArduPilot is overkill.

**Protocol:** MAVLink v2. Binary message protocol with system/component
addressing. Every device on the network has a system ID (1-254) and
component ID (1-254). Messages are published, not requested — you
tell the FC what stream rates you want and it sends them continuously.
Bidirectional: commands go up, telemetry comes down.

**Configuration:** Mission Planner (Windows), QGroundControl (cross-platform),
MAVProxy (command-line). Parameter tree is deep — learning which
parameters matter for your platform takes time. The ArduPilot wiki
is your primary reference.

**Typical platforms:** Commercial survey drones, delivery platforms,
research vehicles, defense platforms, agricultural sprayers,
any platform that needs full autonomous mission capability.

**Community:** Large, technical, welcoming. Strong contributor base.
Excellent wiki. Monthly developer calls. The go-to choice for
academic and government research.

**When to choose it:** You need real autonomous capability. Waypoint
missions, sensor integration, companion computer support, multiple
flight modes, or you're building something that isn't a standard
multicopter. ArduPilot probably already supports your platform.

---

## PX4

**What it does well:** Companion computer integration, research
workflows, defense applications. PX4 was designed from the ground
up for programmatic control. The uORB publish/subscribe internal
bus, the uXRCE-DDS bridge to ROS2, and the clean offboard control
API make it the natural choice when a computer is flying the drone
and a human is supervising.

**What it doesn't do well:** Community hand-holding. PX4's
documentation assumes a higher baseline than ArduPilot's. The
parameter set (~900 parameters) is smaller than ArduPilot's but
the naming convention is less intuitive. Hardware support is
narrower — PX4 cares less about supporting every FC board and
more about supporting the ones that matter for its target users.

**Protocol:** MAVLink v2 (same as ArduPilot, different dialect
extensions). Additionally supports uXRCE-DDS for high-bandwidth
sensor telemetry to companion computers, replacing the older
microRTPS bridge.

**Configuration:** QGroundControl (primary), PX4 CLI via MAVLink
shell. No equivalent to ArduPilot's Mission Planner.

**Typical platforms:** Research drones, defense autonomous systems,
companion-compute-heavy platforms, anything running ROS2,
platforms that need VTOL transition.

**Community:** Smaller than ArduPilot, more academic/defense-focused.
Strong institutional backing (Dronecode Foundation, Auterion).
Development is faster on core features, slower on edge-case
platform support.

**When to choose it:** You're integrating with ROS2 or a companion
computer. You need offboard control APIs. You're building for
defense or research. You want a clean software architecture that's
designed for programmatic control first and manual control second.

---

## Cross-Firmware Reality

### The Split

The FPV world runs Betaflight and iNav. MSP protocol. Configurator
apps. CLI dumps. Rate mode. Manual piloting with optional GPS backup.

The autonomous world runs ArduPilot and PX4. MAVLink protocol.
GCS applications. Parameter trees. Mission planning. The human
supervises, the computer flies.

These two worlds are converging. Betaflight quads are getting GPS
rescue and companion computers. ArduPilot platforms are getting
acro mode and FPV video. But the protocol split (MSP vs. MAVLink)
remains the fundamental divide.

Any tool that wants to work across the whole spectrum — which is
what Wingman does — needs to speak both languages fluently.

### Switching Firmware

Changing firmware on an existing platform is possible but not trivial.
The major challenges:

- **Parameter translation:** Betaflight PID 44 is not the same as
  ArduPilot ATC_RAT_RLL_P 0.135. The numbers are in different
  units, different scales, different ranges. Translation requires
  understanding both systems.
- **UART reassignment:** Each firmware has its own UART allocation
  conventions. Moving from Betaflight to iNav may require remapping
  every serial port.
- **Sensor calibration:** Accelerometer, gyro, and compass calibration
  doesn't transfer. Re-calibrate everything.
- **Failsafe behavior:** Different firmwares handle RC loss, GPS loss,
  and battery failsafe differently. Understand the new behavior
  before you fly.

---

## Quick Reference

| Feature | Betaflight | iNav | ArduPilot | PX4 |
|---------|-----------|------|-----------|-----|
| Manual acro flight | Best | Good | Good | Good |
| GPS hold / RTH | Basic rescue | Good | Best | Good |
| Waypoint missions | No | Yes | Best | Yes |
| Fixed-wing | Limited | Good | Best | Good |
| VTOL | No | Yes | Yes | Yes |
| Companion computer | MSP bridge | MSP bridge | MAVLink + DroneKit | MAVLink + uXRCE-DDS + ROS2 |
| Offboard control | No | Limited | Yes (Guided mode) | Yes (Offboard mode) |
| Parameters | ~100 (CLI) | ~200 (CLI/MSP2) | ~1200 (MAVLink) | ~900 (MAVLink) |
| Configuration tool | BF Configurator | iNav Configurator | Mission Planner / QGC | QGC |
| Blackbox logging | Flash / SD | Flash / SD | SD (DataFlash) | SD (ULog) |
| Community size | Largest | Medium | Large | Medium |
| Release cadence | ~3-4 months | ~6 months | Monthly point releases | ~6 months |

---

## Next

- **Chapter 6: MSP Protocol** — how to talk to Betaflight and iNav
  from anything with a serial port.
- **Chapter 7: MAVLink Protocol** — how to talk to ArduPilot and PX4
  from anything with a network connection.

---

*No religious wars. Use what works for your mission. Switch when the mission changes.*
