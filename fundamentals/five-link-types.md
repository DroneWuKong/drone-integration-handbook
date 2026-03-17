# Chapter 1: The Five Link Types

> Every drone in the air right now is using between one and five
> simultaneous radio links. Most operators can name two. This chapter
> covers all five.

---

## The Problem Nobody Talks About

A racing quad has two links — RC control and video. Simple. But the
moment you add GPS return-to-home, you've added a third (telemetry).
Add a companion computer with a mesh radio and you're at four. Add
a payload camera with its own downlink and you're at five.

Each link has its own frequency, its own protocol, its own antenna,
its own failure mode, and its own opinion about which direction
the drone should go. When they disagree, things get interesting.

Understanding the five link types is the foundation of everything
else in this handbook. If you don't know what's talking on your
drone, you can't diagnose why it stopped talking.

---

## The Five Links

### Link 1: Manual Control (RC)

**What it does:** Carries stick commands from the pilot to the
flight controller. The link that keeps a human in the loop.

**Protocols:** ELRS (ExpressLRS), CRSF (TBS Crossfire), GHST (IRC Ghost),
SBUS (FrSky), IBUS (FlySky), PPM (legacy).

**Frequencies:**
- 2.4 GHz — most common (ELRS 2.4, CRSF, Ghost, FrSky ACCST)
- 900/868 MHz — long range (ELRS 900, Crossfire, FrSky R9)
- Sub-GHz proprietary — tactical (IRONghost dual-band)

**What you need to know:**
- This is the only link where latency matters in milliseconds.
  ELRS at 500 Hz has ~2 ms latency. SBUS is ~6 ms. At 250 Hz
  freestyle, you won't feel the difference. In a racing final, you might.
- Loss of this link triggers failsafe. Every FC firmware handles
  failsafe differently. Know yours before you need it.
- ELRS and Crossfire use serial protocols (CRSF wire format) that
  carry bidirectional telemetry inside the RC link. This blurs the
  line between Link 1 and Link 2 — your RC receiver is also a
  telemetry radio. This is efficient but means RC loss also kills
  your telemetry.

**Common problems:**
- RC and video on the same frequency band (both 2.4 GHz) causing
  desense. Solution: different bands, or physical antenna separation.
- Wrong UART baud rate in FC configurator — CRSF wants 420000, not 115200.
- ELRS binding phrase mismatch after firmware update.

---

### Link 2: Telemetry / Command & Control (C2)

**What it does:** Bidirectional data link between the drone and a
ground station. Carries flight data down (position, battery, attitude)
and commands up (waypoints, parameter changes, mode switches).

**Protocols:** MAVLink v2 (ArduPilot, PX4), MSP (Betaflight, iNav),
LTM (Lightweight Telemetry), FrSky S.Port/F.Port.

**Transport options:**
- Embedded in RC link — CRSF/ELRS carry MAVLink or custom telemetry
  inside the control channel. No separate radio needed.
- Dedicated telemetry radio — SiK (3DR), RFD900x, MicroHard P900.
  Separate frequency, separate antenna, separate failure mode.
- WiFi — ESP32 bridge, companion computer WiFi, mesh radio backhaul.
- Cellular — LTE modems for beyond-visual-line-of-sight (BVLOS).

**What you need to know:**
- MAVLink is the lingua franca for autonomous platforms. If you're
  running ArduPilot or PX4, everything speaks MAVLink. If you're
  running Betaflight, everything speaks MSP. If you're running a
  mixed fleet, you need both.
- Telemetry bandwidth matters more than telemetry latency. You
  don't need millisecond position updates on the ground — 1-10 Hz
  is fine. But you do need all the data fields to arrive intact.
- Dedicated telemetry radios (RFD900x, SiK) are point-to-point.
  They don't scale to multiple drones without a mesh layer on top.

**Common problems:**
- MAVLink stream rate misconfigured — too high floods the link,
  too low makes the GCS look frozen. Start with `SR0_POSITION=2`,
  `SR0_EXTRA1=4`, adjust from there.
- SiK radio firmware mismatch between air and ground units.
- UART conflict — telemetry and GPS both assigned to the same UART.

---

### Link 3: Video Downlink

**What it does:** Sends camera feed from the drone to the pilot's
goggles or ground station monitor. The link that lets you see.

**Technologies:**
- **Analog 5.8 GHz** — lowest latency (~1 ms glass-to-glass),
  degrades gracefully (static, then snow, then nothing). Still
  dominant in FPV racing and tactical ops where latency kills.
- **DJI digital** — DJI O3, O4, Vista, Air Unit. Low latency (~20-28 ms),
  good image quality, locked ecosystem. No third-party interop.
- **HDZero** — digital, ultra-low latency (~15 ms), open ecosystem,
  lower resolution than DJI. Popular with racers going digital.
- **OpenHD / WFB-ng / OpenIPC** — open-source digital video over
  commodity WiFi hardware (RTL8812AU/EU). Higher latency (~80-120 ms),
  fully open, hackable, configurable. The platform for custom builds.
- **Walksnail (Avatar)** — Caddx/Walksnail digital system. Competes
  with DJI on image quality, runs on Artosyn AR8030 chip.

**What you need to know:**
- Video is almost always 5.8 GHz. This means it's on the same band
  as 5 GHz WiFi, some mesh radios, and the 5.8 GHz ISM band that
  everyone assumes is uncontested. In practice, 5.8 GHz is crowded.
- Analog video uses 40 channels across 5.8 GHz. At a race event
  with 8 pilots, frequency management is a real operational problem.
  At a tactical deployment with multiple teams, it's a coordination
  requirement.
- Digital video links (DJI, HDZero) are frequency-hopping or
  wideband. They're harder to interfere with but also harder to
  coordinate. You can't just "pick a channel" the way you can
  with analog.
- The RTL8812AU chip that OpenHD/WFB-ng depends on has been
  discontinued by Realtek. The RTL8812EU replacement does NOT
  support monitor mode in the same way. This is slowly killing
  the open-source digital FPV ecosystem. OpenIPC is moving to
  other solutions.

**Common problems:**
- 5.8 GHz video transmitter (VTX) too close to 2.4 GHz RC antenna
  causes receiver desense. Minimum 10 cm separation, more is better.
- VTX power set too high for proximity flying — at 800 mW you're
  heating the VTX and potentially interfering with your own RC.
  25-200 mW is enough for most LOS operations.
- Wrong VTX table in Betaflight — mismatched power levels,
  missing channels, or wrong band assignments.

---

### Link 4: Payload Data

**What it does:** Carries data from a mission payload — mapping camera,
multispectral sensor, LiDAR, SAR, SIGINT receiver, delivery mechanism
confirmation. Distinct from the FPV video feed (Link 3).

**Technologies:**
- Ethernet (wired, on companion computer)
- USB (camera to companion)
- WiFi (payload-specific AP)
- Dedicated RF downlink (separate frequency, separate antenna)
- Store-and-forward (record on board, download after landing)

**What you need to know:**
- Most consumer and racing drones don't have Link 4. It shows up
  on commercial mapping drones, agricultural platforms, and defense
  ISR platforms.
- Payload data is usually high bandwidth and tolerant of latency.
  A mapping camera generates gigabytes per flight — you're not
  streaming that in real time. You're storing it and downloading
  after landing.
- When payload data IS streamed (tactical video from a gimbal camera,
  SAR data, EW sensor output), it competes for bandwidth with
  telemetry and video. This is where mesh radios with QoS become
  important — prioritize C2 over payload, always.
- The companion computer is the integration point. Payload connects
  to companion via USB/Ethernet/GPIO. Companion decides what goes
  down the RF link and what gets stored.

**Common problems:**
- Payload drawing too much power from the FC's 5V/12V rail.
  Payload should have its own BEC or regulated supply.
- USB bandwidth contention between payload camera and companion
  computer's other USB devices.
- Payload data timestamps not synchronized with flight controller
  timestamps. Use GPS time or NTP on the companion for correlation.

---

### Link 5: Mesh / Swarm Coordination

**What it does:** Drone-to-drone communication for fleet operations.
Position sharing, intent coordination, task allocation, sensor data
relay. The link that turns individuals into a team.

**Technologies:**
- **ESP-NOW** — Espressif peer-to-peer, 2.4 GHz, ~250 byte packets,
  no infrastructure needed. Good for ground operations (Tooth mesh,
  pre-flight sync). Not suitable for in-flight swarm at range.
- **WiFi mesh (batman-adv / 802.11s)** — Linux-based mesh networking.
  Doodle Labs, Silvus, and Persistent Systems all use this under
  the hood (yes, your $5,000 Silvus StreamCaster is running
  OpenWRT with batman-adv). Range 1-50 km depending on radio
  and power.
- **MANET (Mobile Ad-hoc Network)** — military-grade mesh with
  frequency hopping, anti-jam, encryption. Persistent Systems MPU5,
  Silvus at higher tiers, Harris/L3Harris. $10,000-50,000 per node.
- **MAVLink over mesh** — any of the above carrying MAVLink messages
  between platforms. Each drone gets a unique system ID (1-254).
  Standard MAVLink messages (GLOBAL_POSITION_INT, HEARTBEAT)
  become the swarm awareness layer.

**What you need to know:**
- Most drones don't have Link 5. It's the last link to be added
  and the first to be cut when budget or weight is tight.
- Mesh radios that claim "50 km range" are telling you the radio
  range, not the mesh range. Mesh adds overhead. Real throughput
  across 3 hops is typically 30-50% of single-hop throughput.
- The dirty secret of tactical mesh: Doodle Labs is OpenWRT on
  Atheros/Qualcomm WiFi silicon running batman-adv. Silvus is
  similar with their own MAC layer. Persistent Systems MPU5 is
  the most custom but still builds on standard radio architectures.
  They're not magic. They're well-engineered WiFi radios in
  ruggedized enclosures with good antenna design and custom firmware.
- Mesh network planning is its own discipline. Node placement,
  antenna orientation, channel assignment, traffic prioritization —
  these matter more than the radio's datasheet specs.

**Common problems:**
- Mesh radio on 2.4 GHz interfering with 2.4 GHz RC link.
  Solution: different bands (mesh on 900 MHz or 5 GHz).
- batman-adv OGM (Originator Message) interval too high, causing
  stale routing. Default 1 second is fine for slow-moving platforms.
  Fast-moving drones may need 250 ms.
- IP address conflicts in the mesh. Use a consistent addressing
  scheme: `10.0.0.{system_id}` with system_id matching MAVLink ID.

---

## How They Interact

The five links are not independent. They share spectrum, share power,
share the FC's limited UARTs, and share the operator's limited attention.

### Frequency Deconfliction

| Link | Common Frequency | Conflict With |
|------|-----------------|---------------|
| RC (Link 1) | 2.4 GHz | WiFi mesh, BLE, companion WiFi |
| RC (Link 1) | 900 MHz | Telemetry radio, mesh radio |
| Telemetry (Link 2) | 900 MHz | Long-range RC, mesh radio |
| Video (Link 3) | 5.8 GHz | 5 GHz WiFi, mesh radio, payload WiFi |
| Payload (Link 4) | varies | depends on payload type |
| Mesh (Link 5) | 2.4/5/900 MHz | everything else |

The rule: **no two links on the same band within the same airframe
unless they're designed to coexist.** ELRS 2.4 GHz and an ESP32
WiFi AP on the same drone will fight. ELRS 900 MHz and an RFD900x
telemetry radio will fight. Plan your frequency layout before
you build.

### UART Allocation

A typical F405 flight controller has 3-6 UARTs. They get consumed fast:

| UART | Typical Assignment |
|------|-------------------|
| UART1 | RC receiver (CRSF/ELRS/SBUS) |
| UART2 | GPS |
| UART3 | Telemetry radio or MSP bridge |
| UART4 | ESC telemetry (if DShot + telemetry) |
| UART5 | Companion computer (MAVLink or MSP) |
| UART6 | (you're out of UARTs) |

Running out of UARTs is one of the most common integration problems
on F4-class FCs. Solutions: use soft serial (limited baud rate),
upgrade to an H7 FC (more UARTs), or use a companion computer to
multiplex multiple data streams over a single UART.

### Power Budget

Every link has a radio that draws power. Every radio has an amplifier
that draws more power. On a 5-inch FPV quad with a 1300 mAh 6S battery,
your total electronics budget (FC + ESCs + radio + VTX + GPS + receiver)
is typically 2-5W continuous. Adding a mesh radio at 1-2W is significant.
Adding a companion computer at 3-10W changes your flight time.

**Know your power budget before you add links.**

---

## The Operator's Decision

Not every drone needs all five links. Most don't. The right number
of links depends on the mission:

| Mission | Links Needed |
|---------|-------------|
| FPV racing | 2 (RC + video) |
| Freestyle / cinematic | 2-3 (RC + video + optional telemetry) |
| Mapping / survey | 3-4 (RC + telemetry + video + payload) |
| Tactical ISR | 4-5 (all five) |
| Swarm operations | 5 (all five, mesh is mandatory) |
| Autonomous delivery | 3 (telemetry + video + optional mesh) |

More links = more complexity = more things to break = more things
to diagnose. Add links because the mission requires them, not because
the hardware supports them.

---

## Next

- **Chapter 2: Frequency Bands and Regulatory Reality** — the rules
  that govern where your links can operate, and the gaps between
  the rules and reality.
- **Chapter 8: UART Layout and Why It Matters** — the practical
  constraint that limits how many links you can actually use.

---

*Every link you add is a complication. Know what it costs before you add it.*
