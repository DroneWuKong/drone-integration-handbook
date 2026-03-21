# EW-Resilient Communications — Keeping the Link Alive

> **Part 6 — Components**
> The radio link between operator and drone is the single point of
> failure that electronic warfare exploits. This chapter covers
> who builds the links that survive jamming.

---

## The EW Reality

GPS-denied, spectrum-contested environments are the new baseline.
Ukraine proved this at scale — Russian EW systems routinely jam
GPS, spoof navigation, and disrupt C2 links. The average lifespan
of a commercial drone on the Ukrainian front is days, not months,
largely because consumer-grade links fail under EW pressure.

Any drone system intended for contested environments needs
communications that degrade gracefully rather than failing
catastrophically. This means frequency hopping, spread spectrum,
mesh networking, and ultimately — for complete EW immunity —
fiber-optic links.

The Handbook's RF Fundamentals (Part 1) covers the physics.
This chapter covers the products and manufacturers.

---

## Sine Engineering — Combat-Proven from Day One

The most important communications company most people have never
heard of. Founded in Lviv, Ukraine in 2022 as a counter-UAS team.
After realizing that resilient connectivity is both the most critical
enabler and the most vulnerable aspect of UAS operations, they
pivoted to building their own solutions.

| Detail | Value |
|--------|-------|
| HQ | Lviv, Ukraine (European office planned) |
| Founded | 2022 |
| Employees | 150 |
| Customers | 150+ UAV development teams, 70+ drone manufacturers worldwide |
| Notable Client | Vyriy Drone (100% Ukrainian-sourced FPV) |
| NATO | Innovation Range winner (Dec 2025, communications category) |
| Production | Scaling 5× in 2026 |
| Funding | Bootstrapped through 2025, first investment round in progress |

### Pasika Platform

Pasika ("Apiary") is Sine Engineering's integrated platform for
multi-drone operations in contested environments. Four core pillars:

1. **Resilient C2 Datalinks** — Secure command and control with
   Smart FHSS (frequency hopping spread spectrum), jamming detect
   and avoid. Hardware-agnostic.
2. **Digital Video Datalinks** — HD video transmission optimized
   for EW-contested environments.
3. **GPS-Independent Navigation** — Satellite-free positioning
   using time-of-flight signals from nearby Sine.Links (inspired
   by legacy aviation navigation). Not centimeter-accurate, but
   maintains operational continuity when GPS is denied.
4. **Swarm Capability** — One operator controls multiple drones
   via single interface. Assign mission zones, launch sequentially,
   switch between drone feeds, deconflict paths automatically.

**Combat record:** Missions exceeding 200+ km in active EW
conditions. Deployed across multiple Ukrainian drone types
including strike FPVs, fiber-optic drones, and interceptors
(Wild Hornets' Sting).

### Why Sine Engineering Matters

Pasika allows $300–500 FPV drones to complete missions that would
typically require more expensive platforms — because they maintain
comms longer, avoid jamming more often, and deliver telemetry for
continuous improvement. The system evolves weekly from direct
battlefield feedback. As Sine puts it: "We don't bet on stability.
We design for instability."

Their approach — "operator-scaled deployment" that extends human
capability rather than replacing it — maps directly to the AI
Wingman "Jarvis not Ultron" philosophy.

**FPGA-based modules** are in development for next-generation
hardware. European branch opening for NATO-aligned manufacturing
partnerships, including targeting US defense manufacturers
supplying the Pentagon.

---

## Western Mesh Radio Manufacturers

### Doodle Labs

| Detail | Value |
|--------|-------|
| HQ | USA / Singapore |
| Blue UAS | Framework component (Mesh Rider Radios) |
| Technology | OpenWRT + batman-adv mesh networking |
| Products | Mesh Rider series in Helix configuration |
| Key Feature | Wi-Fi-based mesh with ruggedized form factor |
| NDAA | Compliant (Blue UAS Framework listed) |

Doodle Labs Mesh Rider radios are the most commonly integrated
mesh networking solution in commercial and defense small UAS.
Under the hood, they run OpenWRT Linux with batman-adv mesh
protocol — which means they're configurable Linux devices, not
black boxes. This is both a strength (flexible, hackable) and
a vulnerability (software complexity increases attack surface).

See the Handbook's mesh radios chapter (Chapter 14) for
configuration details and real-world range expectations.

### Silvus Technologies

| Detail | Value |
|--------|-------|
| HQ | Los Angeles, CA, USA |
| Technology | StreamCaster MIMO radios |
| Key Feature | MN-MIMO (Mobile Networked MIMO) — highest throughput mesh |
| Products | SC-4200, SC-4400 series |
| Weight | 100–300g depending on model |
| Power | 5–15W |
| NDAA | US manufacturer — compliant |

Silvus provides the highest-throughput mesh radios in the market.
Their MN-MIMO technology uses multiple-input multiple-output
antenna configurations with mesh networking for combined
throughput and resilience. Premium pricing — positioned for
high-value platforms where bandwidth justifies the SWaP cost.

### Persistent Systems

| Detail | Value |
|--------|-------|
| HQ | New York, NY, USA |
| Technology | MPU5 MANET radio |
| Key Feature | Android-based radio with integrated compute |
| Products | MPU5 series |
| NDAA | US manufacturer — compliant |

Persistent Systems MPU5 is unique in running Android OS natively
on the radio, enabling onboard application hosting. Wave Relay
MANET protocol. Used extensively by US SOF and DoD.

### TrellisWare Technologies

| Detail | Value |
|--------|-------|
| HQ | San Diego, CA, USA |
| Technology | TSM (TrellisWare Scalable MANET) waveform |
| Key Feature | Barrage Relay — patented non-routing mesh, 800+ nodes tested |
| Waveforms | TSM (wideband MANET), Katana (anti-jam ECCM), NB LOS |
| Encryption | AES-256 built-in |
| Bands | UHF + L-band + S-band (225–2600 MHz) in single radio |
| NDAA | US manufacturer — compliant |
| New (2025) | Anti-jam C2 waveform for uncrewed systems, Barrage Beamforming |

**Product Line:**

| Radio | Form Factor | Key Feature |
|-------|-------------|-------------|
| TW Shadow 950 | Handheld SDR | Flagship. Multi-band, HD video multicast, 32 talk-groups |
| TW Shadow 750 | Compact handheld | Mission-critical voice/data/PLI, simplified operation |
| TW Shadow 135 HPR | High Power (20W) | Vehicular/airborne/relay. Extended range |
| TW Ghost 875 | Small relay | Built-in battery, deploy as network node |
| TW Ghost 870 | OEM module | Embeddable into drones, robotics, platforms |
| TW Spirit 860 | Next-gen soldier | Public safety, first responder compatible |

TrellisWare's Barrage Relay technology eliminates traditional
routing — all nodes collaboratively relay all traffic using
cooperative combining. This means the network self-heals
instantly when nodes join, leave, or are destroyed. Tested
with 800+ nodes. Network formation in under 5 seconds.

**Anti-jam C2 for UAS (2025):** New waveform specifically for
drone command and control with anti-jam uplink alongside high-
throughput video/sensor downlink. Lowest latency in the industry.
This directly addresses the DDG Phase II EW requirement.

### Mobilicom

| Detail | Value |
|--------|-------|
| HQ | Israel / USA |
| Blue UAS | Framework component (SkyHopper) |
| Products | SkyHopper PRO, PRO Lite, PRO Micro |
| Key Feature | Encrypted, cybersecure drone datalinks |
| Partnership | ARK Electronics — affordable AI drone solutions |
| NDAA | Blue UAS Framework listed |

---

## Turkish Manufacturers

### Aselsan

Turkey's largest defense electronics company. Produces military-
grade communications, EW systems, and radar. Supplies datalinks
for Baykar TB2/TB3 and TAI ANKA platforms. Export-controlled.

### TUALCOM

Stackable data acquisition and telemetry suites for UAS.
Integrated with Turkish military platforms.

### Meteksan

AKSON C-Band datalink (announced Nov 2025). Turkish defense
communications.

---

## Fiber-Optic — The EW-Immune Option

Fiber-optic FPV eliminates RF entirely. Video and control signals
travel through a thin optical fiber trailed behind the drone.
Zero RF emissions means zero detectability and complete immunity
to electronic warfare jamming.

**Key players:**
- **Kela Technologies** (Israel, In-Q-Tel backed) — fiber-optic
  technology partner for Neros Archer Fiber. World's first
  NDAA-compliant fiber-optic FPV.
- **SkyFall** (Ukraine) — Fiber-optic FPV drones. Partnered with
  Skycutter for DDG Phase I (Shrike 10 Fiber won with 99.3 points).
- **3DTech** (Ukraine) — 3D-prints their own fiber spool casings.
- **Hasta** (Ukraine) — Optically-guided FPV, 20–50 km range.

**Tradeoff:** Range is limited by spool length (physical fiber
must trail behind the drone). The fiber can snag on obstacles.
But for missions where EW immunity is paramount and range is
known, fiber-optic is unbeatable.

DDG Phase I validated this: the fiber-optic Shrike dominated
the competition. DDG Phase II's full EW environment will likely
further advantage fiber-optic platforms.

---

## NDAA RC & C2 Links

Most consumer RC links (ELRS, CRSF, FrSky) are Chinese-manufactured.
For NDAA-compliant builds, the options narrow significantly.

### Orqa Ghost — 2.4 GHz RC Link

EU-manufactured, NDAA-compliant 2.4 GHz RC link using LoRa-based
chirp spread spectrum with adaptive FHSS. One of very few
non-Chinese RC link options with both race and long-range performance.

| Parameter | Value |
|-----------|-------|
| Frequency | 2.4 GHz ISM band |
| Modulation | Chirp Spread Spectrum + Adaptive FHSS (LoRa/FLRC) |
| Protocol | GHST (native), SBus, SRXL-2, PWM |
| Modes | Pure Race (222–250 Hz, <4 ms), Normal (~50 Hz), Long Range (~15 Hz) |
| Receivers | Átto (~0.6 g), Átto Duo (true diversity), Hybrid DUO/UNO V2 (combined VTx + Rx) |
| Tx Modules | JR bay, Lite bay, UberLite — all 350 mW |

Works with PX4 (`RC_INPUT` = `GHST`), QGroundControl,
Betaflight 4.3+, iNav, and ArduPilot. OpenTX 2.3.13+ recommended.

### Orqa IRONghost — Licensed-Band C2

Defense-grade C2 link operating on licensed bands. Dual-radio
architecture. Manufactured in EU, NDAA compliant.

| Parameter | Value |
|-----------|-------|
| Spectrum | Licensed bands (contact Orqa for spectrum details) |
| Max Tx Power | 3W |
| Modulation | Proprietary, firmware-upgradeable |
| Video | Combined C2 Rx + 5.8 GHz analog VTx in single module |
| OTA Updates | Firmware during binding (<60 seconds) |

Paired with Orqa Tac.Ctrl (MAVLink, ATAK-compatible) and GCS-1
ground station for extended range and NLOS operations via aerial
repeater. Requires licensed spectrum — coordinate with your RF
authority before deployment.

**Critical:** Never power on without all antennas attached — 3W
reflected back into amplifiers causes permanent damage.

---

## Choosing Communications

1. **Consumer FPV links (ELRS, CRSF, DJI) are NOT EW-resilient.**
   They work in benign environments. They fail under deliberate
   jamming. Don't pretend otherwise.

2. **Mesh radios add resilience but add SWaP.** A Doodle Labs or
   Silvus radio is 100–300g and 5–15W. That's your biggest payload
   hit after the camera. Budget it.

3. **Frequency diversity matters.** A single-band radio can be
   jammed with a single jammer. Multi-band radios (TrellisWare
   UHF+L+S in one device) are harder to deny.

4. **Non-routing mesh > traditional routing.** TrellisWare's
   Barrage Relay and batman-adv (Doodle Labs) both eliminate
   single-point-of-failure routing tables. The network heals
   when nodes die.

5. **For DDG Phase II / contested environments:** TrellisWare
   anti-jam C2 or Sine Engineering Pasika are the purpose-built
   solutions. Fiber-optic for maximum EW immunity at the cost
   of range flexibility.

6. **Combat-proven > spec sheet.** Sine Engineering's Pasika has
   been tested against Russian EW daily for years. That validation
   data doesn't appear on any data sheet.

---

## Meshtastic — LoRa Mesh as a Telemetry Backbone

Meshtastic is an open-source project that turns cheap LoRa radios (typically ESP32-based, sub-$30) into a self-healing encrypted mesh network. It was designed for off-grid human communication, but the architecture maps directly onto drone telemetry requirements for GPS-denied or RF-contested operations.

### Why It Matters for Drones

Commercial drone links (GHST, ELRS, Crossfire) are point-to-point. When the GCS moves out of line-of-sight or the primary link is jammed, you lose everything. Meshtastic offers a different failure mode: packets route through whatever mesh nodes are still alive. A swarm of drones, each carrying a Meshtastic node, effectively forms its own relay network — each aircraft extending range for every other aircraft and the GCS.

Bandwidth is the constraint. Meshtastic at LoRa long-range settings moves roughly 1–5 kbps. That's enough for MAVLink heartbeat, GPS position, battery voltage, and flight mode — the minimum viable telemetry set — but not enough for video, high-rate sensor data, or fast command loops. Think of it as the backup nervous system, not the primary one.

### AkitaEngineering Pattern (DroneBridge32 + Meshtastic)

The AkitaEngineering Meshtastic-Integration-for-DroneBridge32-Swarm project (GitHub, GPL-3.0) demonstrates the integration architecture: Arduino C++ on DroneBridge32 parses MAVLink from the FC, encrypts the telemetry payload with AES, and transmits over Meshtastic. Python ground station plugins receive, decrypt, display, and send control commands back. The project also implements geofencing at the mesh layer (drone enforces a fence independent of FC), dynamic channel switching based on link quality, and emergency landing commands that propagate through the mesh even under degraded conditions.

The code is a reference implementation, not production firmware — no versioned releases, minimal testing. But the architectural patterns are sound and directly applicable:

- **MAVLink-over-Meshtastic bridge**: parse MAVLink on the embedded side, serialize the essential fields, transmit over LoRa, reassemble on the GCS side and re-inject into Mission Planner or QGroundControl via UDP.
- **Mesh-layer geofencing**: the drone enforces its fence using its own GPS + the received boundary definition, independent of FC-level fence. This survives link degradation.
- **Swarm broadcast commands**: Meshtastic's broadcast addressing lets a single GCS message reach all nodes in the mesh simultaneously — useful for emergency stop, RTL, or mode change across a swarm.
- **Dynamic channel switching**: if interference is detected on the primary channel, both sides coordinate a channel hop through a pre-agreed fallback sequence.

### Hardware

Any Meshtastic-compatible LoRa hardware works. The most drone-relevant options:

| Device | Weight | Form factor | Notes |
|--------|--------|-------------|-------|
| LilyGo T-Beam | ~35g | Dev board | GPS onboard — useful for mesh relay nodes |
| Heltec LoRa 32 | ~8g | Compact | No GPS, pure mesh relay |
| RAK WisBlock | ~5–15g | Modular | Cleanest integration option for embedded builds |
| TTGO LoRa32 | ~10g | Compact | Common, well-supported |

All run at 915 MHz (US) or 868 MHz (EU). LoRa is ISM band — no license required, but power limits apply. At maximum legal EIRP, reliable range in open terrain is 5–15 km depending on antenna and terrain.

### Integration Pattern for Wingman/Command

For a Wingman swarm deployment, the recommended architecture is a **dual-link stack**: GHST (or ELRS) as the primary high-bandwidth link for normal operations, Meshtastic as the secondary low-bandwidth link for telemetry heartbeat and emergency commands. The Meshtastic node on each drone runs independently of the primary link — it has its own power rail, its own CPU, and its own antenna. A primary link failure leaves the mesh intact.

The MAVLink-over-Meshtastic bridge runs as a process on the companion computer (APB or VOXL 2), feeding MAVLink telemetry from the FC to the Meshtastic serial interface, and forwarding received commands from the mesh back to the FC.

---

## DroneEngage — Cellular Telemetry at Scale

DroneEngage is the ArduPilot project's cloud companion software, running on Raspberry Pi and providing unlimited-range telemetry, video streaming, and fleet management over 4G/LTE/5G. It is the Linux successor to Andruav (the Android companion app) and is actively developed under the ArduPilot umbrella.

### What It Does

A Raspberry Pi connected to an ArduPilot or PX4 flight controller via UART/USB becomes a DroneEngage unit. The Pi connects to the internet via a USB LTE modem or HAT, and from that point the drone is reachable from anywhere with a browser. The web client provides a full ground control station: MAVLink telemetry, gamepad control, video streaming, geofencing, and swarm management.

Key capabilities:

- **Unlimited telemetry range** — the link goes through the internet, so range is only limited by cellular coverage. Relevant for BVLOS operations.
- **MAVLink forwarding** — DroneEngage forwards MAVLink transparently to Mission Planner, QGroundControl, or any UDP endpoint. No change to existing GCS workflows.
- **Video streaming** — supports Raspberry Pi cameras and USB cameras. Stream from one or multiple cameras simultaneously.
- **Swarm operations** — control multiple drones from a single interface with synchronized missions and hierarchical formation management.
- **RC Blocking / TX Freeze** — a local field pilot can override remote control; TX Freeze holds throttle position for safe long-range cruise without active stick input.
- **Independent geofencing** — enforced at the companion computer level, independent of the FC's fence logic. Survives FC configuration changes.
- **Air-gap server** — self-hostable backend for operations where cloud dependency is unacceptable (contested environments, classified sites, comms-restricted areas).

### Hardware

DroneEngage runs on Raspberry Pi Zero W, Zero 2 W, Pi 3, 4, or 5. Weight matters:

| Platform | Weight (with LTE modem) | Use case |
|---|---|---|
| RPI Zero W | ~42g complete | Telemetry-only, minimal payload budget |
| RPI Zero 2 W + camera | ~52g | Telemetry + single camera stream |
| RPI 3/4 | ~85–95g | Multi-camera, heavier compute tasks |

The 42g complete-system figure for the Zero W is notable — it's competitive with dedicated telemetry radios when you factor in that you're also getting cloud connectivity, geofencing, and swarm management in the same package.

### Andruav (Legacy Android Path)

Andruav is the predecessor: an Android phone running as a companion computer, connected to the FC over USB serial. The phone provides GPS, camera (FPV), cellular telemetry, and SMS-based control as a fallback. It's simpler to deploy for rapid prototyping — tape a phone to the airframe, connect USB, install the app — but less capable than DroneEngage for serious operations. Active development has shifted to DroneEngage; Andruav is maintained for existing deployments.

### Air-Gap Deployment

For operations where cloud routing is off the table, DroneEngage supports a self-hosted server that can run on a Raspberry Pi 4 at the GCS site. All drone-to-GCS traffic routes through this local server rather than ArduPilot's cloud infrastructure. The protocol and security model are identical — the only change is the server endpoint. This makes DroneEngage viable for classified programs, contested environments, and locations with unreliable internet.

### Integration with Command

DroneEngage's swarm logic and its air-gap server are directly relevant to Command's architecture. The hierarchical swarm formation model (lead drone + subordinates, commands propagate through the tree) maps to CBBA task allocation with a broadcast command layer on top. The air-gap server pattern is exactly what Command needs for field-deployable C&C without cloud dependency. The DroneEngage communication protocol is documented (see ArduPilot cloud docs) and could serve as a reference or direct integration point for Command's GCS-to-swarm link.

---

*Last updated: March 2026*

---

## OpenHD — Open-Source Digital Video Link

OpenHD is the open-source answer to DJI O3, Walksnail Avatar, and HDZero. Instead of proprietary hardware running a proprietary protocol, it puts commodity RTL8812AU WiFi adapters into a one-way broadcast mode (wifibroadcast) that behaves like an analog video transmitter — no association handshake, no ACK, just raw packets into the air. The result is a long-range digital HD video link built from hardware you can source on AliExpress for under $50 total.

The suite transmits HD video, two-way UAV telemetry, two-way OpenHD telemetry (settings, range adjustments, channel changes, wifi modulation), and RC control signals — all multiplexed over a single RF channel, using MAVLink for the telemetry layer. The world record stands at 55km on a fixed-wing platform.

### Why It Matters

Commercial HD video links (DJI O3, HDZero, Walksnail) cost $150–400 for the air unit alone, lock you into specific cameras, and ship from China. OpenHD costs $15–30 for the air unit, works with any CSI camera your SBC supports, and is open source down to the driver level. For teams that need HD video over ranges where commercial links won't reach, or who can't use Chinese-manufactured hardware, OpenHD is the practical path.

It's also the only digital FPV link where you can inspect and modify every layer of the stack — from the WiFi driver to the video codec to the OSD renderer.

### How Wifibroadcast Works

Standard WiFi requires both ends to associate before exchanging data. That association process adds latency and creates a hard cliff at range — when signal degrades below the association threshold, the link drops entirely. Wifibroadcast bypasses association entirely. The air unit injects raw 802.11 frames directly into the driver; the ground unit captures all frames promiscuously regardless of source. This is the same transmission model as analog video: signal degrades gracefully with distance rather than falling off a cliff. FEC (forward error correction) across multiple packets replaces the ACK mechanism, so isolated packet loss doesn't corrupt the stream.

### Hardware Stack

**Air unit (minimum):**
Raspberry Pi Zero 2 (not the original Zero 1 — not supported), a dedicated BEC for the WiFi adapter, and a supported camera with the 22-pin type B CSI cable. The WiFi adapter must be soldered to the SBC's USB pads — vibration will disconnect any plug-in connection.

**Air unit (better):**
Raspberry Pi CM4 with Ochin CM4 carrier board, plus a supported WiFi card. The CM4 enables dual camera, better thermal performance, and lower latency.

**Ground station:**
A laptop with SecureBoot disabled, plus a supported WiFi adapter. X86 performance matters — faster hardware means lower decode latency. For lowest latency ground decode, a Radxa Rock 5 is the current recommendation — it hardware-encodes H.265 in real time.

**WiFi adapters:**

Supported chipsets: RTL8812AU, RTL8814AU, RTL8811AU, RTL8812BU, RTL8812EU. Top picks: ALFA AWUS036ACH (500mW, 8812AU, 2× RP-SMA), ASUS USB-AC56 (500mW, 8812AU, widely available), "Taobao card" (generic 8812AU, 500mW, 2× u.fl). Most users prefer 5.8GHz — cleaner spectrum than 2.4GHz and no interference with 2.4GHz RC transmitters. 5.8GHz does not offer better penetration but has cleaner channels in most operating environments.

The BLM8812EU is the newest and most capable chipset — higher sensitivity and better power output — but has no FCC/CE certification so import and use are at the operator's discretion.

### Latency

Lowest latency requires OpenHD custom hardware (purpose-built SBC + camera combination), which can cut latency roughly in half compared to standard configurations. Second-lowest is achievable with the Radxa Rock5 on both air and ground. RPi Zero 2 builds have higher latency — usable for FPV but not competitive with commercial HD systems on this metric.

Practical glass-to-glass latency numbers for RPi-based builds: 80–150ms depending on resolution, codec, and SBC. Custom hardware targets sub-40ms.

### MAVLink Integration

OpenHD passes MAVLink telemetry transparently over the wifibroadcast link. The air unit connects to the FC via UART (same as any telemetry radio — standard MAVLink port configuration). On the ground, QOpenHD receives and displays the telemetry, and also forwards the MAVLink stream over UDP so Mission Planner or QGroundControl can connect simultaneously. This makes OpenHD a functional telemetry radio replacement, not just a video link.

### Integration with Wingman / Buddy

QOpenHD's Android app receives the ground station video and telemetry stream over WiFi or USB. For Wingman deployments, this means:

- Buddy can consume the MAVLink UDP stream from the OpenHD ground station without any modification to the existing telemetry pipeline — it connects as a second MAVLink client on the same forwarded stream.
- The video stream can be pulled via RTSP or UDP from the ground station and displayed in Buddy's live view alongside the GCS data.
- OpenHD's RC passthrough can operate alongside dedicated GHST/ELRS links — video and telemetry over OpenHD, high-rate control commands over the primary link.

### Range Realities

55km is the record under ideal conditions — fixed-wing platform, good antennas, line of sight, quiet spectrum. Realistic operational range for a typical build: 5–20km depending on obstructions, antenna gain, and spectrum cleanliness. 2.4GHz gives better obstruction penetration at shorter range; 5.8GHz gives cleaner channels at longer range. Both require line of sight for the extreme numbers.

*See also: [OpenHD Implementation Guide](/components/openhd-implementation-guide) — step-by-step from hardware to first flight*
