# Handheld GCS Hardware Deep-Dive

> **Forge cross-reference:** complements 13 entries in `ground_control_stations` category
> **Related handbook chapters:** Ground Control Stations, C2 Datalinks, Companion Computers, Antennas, Cellular LTE BVLOS, Power Architecture & EMI, OpenHD Implementation Guide, NDAA Compliance
> **Handbook Roadmap:** Aligns with planned Chapter 22 (Ground Control Stations) — “Build Your Own” appendix

## Scope

`ground-control-stations.md` covers the **landscape** of GCS software and hardware. This page covers the **build**: if you wanted to design and ship your own integrated hand controller comparable to **CubePilot Herelink**, **Freefly Pilot Pro**, **DJI RC Pro / RC Plus**, **Skydio Enterprise Controller**, or **Inspired Flight GS-ONE**, what does the BOM and architecture look like at the minimum, mid, and maximum tiers?

The target form factor is a single device the operator holds in both hands containing:

- A sunlight-readable touchscreen (5–10″)
- Dual Hall-effect gimbals + switches/triggers/wheels
- An integrated radio for control + telemetry + HD video
- Optional cellular and/or satcom for BVLOS failover
- Internal compute running a Linux- or Android-based GCS app (QGroundControl, Mission Planner, Auterion Mission Control, or custom)
- Hot-swappable or long-runtime battery
- Operator GNSS for moving-baseline RTK and CoT “my position”

## Reference devices (what we are benchmarking against)

| Device | SoC class | Display | Radio link | Notable |
|---|---|---|---|---|
| **CubePilot Herelink** | Allwinner H6 (quad A53) | 5.46″ 1080p, ~800 nit | 2.4 GHz OFDM, 20 km claim | Integrated air + ground modules, Android + QGC |
| **DJI RC Pro / RC Plus** | Snapdragon-class octa-core | 5.5–7″ 1080p, 1200–1400 nit | OcuSync 3+ / O3 Enterprise | Tight DJI ecosystem only |
| **Freefly Pilot Pro** | Samsung Galaxy Tab Active3 (SD 855) | 8″ 1920×1200 | Doodle Labs Helix N (added) | Auterion Mission Control |
| **Skydio Enterprise Controller** | Snapdragon 8-class | 6.4″ OLED, ~1000 nit | Skydio Connect (proprietary) | NDAA-compliant |
| **Inspired Flight GS-ONE** | Qualcomm QCS6490 | 7″ 2000 nit | Modular (Microhard, Silvus, Doodle) | NDAA, Blue UAS focus |
| **Auterion AMC Tablet (RM Boxer)** | i.MX 8M Plus / Snapdragon | 8″ 1000 nit | External Microhard / Silvus | Industrial / defense |
| **MotioNew M10** | Rockchip RK3588 class | 10.1″ 1000 nit | Microhard pDDL2450 | All-in-one form factor |
| **Teledyne FLIR SkyController / RM Boxer ELRS variants** | varies | 5–7″ | ExpressLRS / proprietary | Tactical |

## Architecture block diagram (logical)

```
           +----------------------------------------------------+
           |                    Enclosure                       |
           |                                                    |
  RF in -->|--[Patch/Omni MIMO Antennas]--+                     |
           |                              |                     |
           |               +--------------v-------------+       |
           |               | Radio Modem (HD video +    |       |
           |               |  telemetry + RC control)   |       |
           |               +--------------+-------------+       |
           |                              | Ethernet / USB3.0   |
           |                              v                     |
           |   +------+   I2C/UART  +------------+   MIPI-DSI   |
           |   | IMU  |<----------->|            |<---+         |
           |   +------+             |            |    |         |
           |   +------+   UART      |   Main     |  +-+------+  |
           |   | GNSS |<----------->|   SoC /    |  |Display |  |
           |   +------+             |   AP       |  |+ Touch |  |
           |   +------+   USB/SPI   |            |  +--------+  |
           |   |Cellular| <-------->|            |              |
           |   +------+             |            |              |
           |   +------+   SDIO      |            |              |
           |   |WiFi/BT|<---------->|            |              |
           |   +------+             |            |--->[HDMI out, USB-C DP, microSD, SIM]
           |                        +------+-----+              |
           |                               | I2C/SPI/USB         |
           |                               v                     |
           |               +---------------+----------------+    |
           |               | MCU (STM32/RP2040)             |    |
           |               |  - Hall gimbal ADC sampling    |    |
           |               |  - Switch/wheel debounce       |    |
           |               |  - Haptic / LED / fan control  |    |
           |               |  - Battery gauge / PMIC mgmt   |    |
           |               +--------------------------------+    |
           |                                                    |
           |   [Hot-swap Li-ion pack(s)] --> PMIC --> rails      |
           +----------------------------------------------------+
```

The **MCU is doing the realtime work** (sampling sticks at ≥500 Hz, debouncing, building MAVLink RC_CHANNELS_OVERRIDE / SBUS / CRSF frames), the **AP/SoC is doing the UI + video + map + mission planning**, and the **radio modem is its own subsystem**. Keeping these three responsibilities separate is the single most important architectural decision.

## Compute SoC — the brain

The SoC has to simultaneously: decode an H.264/H.265 1080p (ideally 4K) video stream, render a moving map with tiles and overlays, run the GCS app, talk to the radio modem, and not melt the enclosure.

### What matters

- **Hardware video decode** — software decoding of 1080p60 H.265 burns 3–6 W of CPU. Pick a SoC with a dedicated VPU.
- **Sustained, not peak, performance** — sealed enclosures throttle hard. RK3588 advertises 8 cores at 2.4 GHz but sustains ≈ 1.6–1.8 GHz on all cores in a passive controller-style case.
- **Display pipeline** — MIPI-DSI (1–4 lanes) is the right interface for an integrated panel. eDP works for larger displays. Avoid HDMI-internal designs — more components, more EMI, higher power.
- **GPIO / serial wealth** — you will burn UARTs, I2C, SPI, USB endpoints fast. Budget early.
- **NPU** — ≥6 TOPS lets you do onboard CV (operator-side target tracking, video stabilization, OSD object detection) without a separate accelerator.
- **NDAA** — Rockchip, Allwinner, and HiSilicon are Chinese-origin. If you target US DoD / Blue UAS, you must use NXP, TI, Qualcomm (US), or NVIDIA.

### SoC options ranked

| Class | SoC | Cores | NPU | Video | Sustained TDP in handheld | NDAA | Module/SBC examples | ~Unit price |
|---|---|---|---|---|---|---|---|---|
| Entry | **Raspberry Pi CM4** (BCM2711) | 4× A72 @ 1.5 GHz | none | 1080p60 H.264 dec | 3–4 W | no | CM4 8GB module + carrier | $55–80 |
| Entry | **Radxa CM3** (RK3566) | 4× A55 @ 1.8 GHz | 0.8 TOPS | 4K H.265 dec | 3–4 W | no | Radxa CM3 + carrier | $40–70 |
| Entry | **Allwinner H6 / H618** | 4× A53 | none | 4K H.265 dec | 2–3 W | no | OrangePi Zero3, Herelink class | $20–40 |
| Mid | **Rockchip RK3588 / RK3588S** | 4× A76 + 4× A55 @ 2.4 GHz | 6 TOPS | 8K H.265 dec, 4K H.264 enc | 5–7 W | no | Radxa Rock 5C, Orange Pi 5+, Khadas Edge 2, Banana Pi BPI-W3 | $80–200 |
| Mid | **NXP i.MX 8M Plus** | 4× A53 @ 1.8 GHz + M7 | 2.3 TOPS | 1080p60 H.265 dec | 3–5 W | **yes** (US) | Variscite DART-MX8M+, Toradex Verdin | $90–180 |
| Mid | **TI AM62Ax** | 4× A53 @ 1.4 GHz + R5F + C7x DSP | 2 TOPS | 1080p60 H.265 dec | 2–4 W | **yes** | TI SK-AM62A | $70–150 |
| High | **Qualcomm QCS6490 / QRB5165** | 8× Kryo, Adreno 643/650 | 12–15 TOPS | 4K60 H.265 dec/enc | 5–8 W | **yes** | Lantronix Open-Q 6490, Thundercomm TurboX | $250–500 (incl. integration support) |
| High | **NVIDIA Jetson Orin Nano 8GB** | 6× A78AE | Ampere GPU, 40 TOPS (sparse) | 4K60 H.265 dec | 7–10 W | **yes** | Seeed reComputer J3010, Orin Nano dev kit | $250–500 |
| Max | **NVIDIA Jetson Orin NX 16GB** | 8× A78AE | Ampere, 100 TOPS (sparse) | 4K60 H.265 dec / 4K30 enc | 10–15 W (handheld limit) | **yes** | ConnectTech, Auvidea, Forecr carriers | $700–1,100 |
| Max | **Qualcomm QCS8550 (SD 8 Gen 2 class)** | 8-core Kryo, Adreno 740 | ~45 TOPS | 8K60 dec | 7–10 W | **yes** | Thundercomm Rubik Pi 3 | $400–700 |

### What I'd actually pick

- **Min:** Radxa CM3 (RK3566) — cheaper than the Pi CM4, has an NPU, hardware decode, and broad community Yocto/Buildroot support. Use Pi CM4 only if you need Pi software ecosystem.
- **Mid:** RK3588S on a Radxa Rock 5C or Orange Pi 5+. If you need NDAA, NXP i.MX 8M Plus on a Variscite SoM.
- **Max:** Jetson Orin NX 16GB if you want onboard CV / target tracking / video stabilization. Qualcomm QCS6490 if you want Android-first development and a 5G modem natively integrated.

## Display — 50% of perceived product quality

Sunlight readability matters more than resolution. A 1080p display at 400 nits is unusable outdoors; an 800×480 display at 1500 nits is fine. Operators rate “good” controllers on screen, sticks, and battery — in that order.

### Specs that actually matter

- **Luminance:** ≥ 1000 nits for prosumer, ≥ 1500 nits for commercial, ≥ 2000 nits for tactical/sun-glare. DJI RC Pro is 1000; RC Plus is 1200; GS-ONE is 2000.
- **Optical bonding (OCA):** eliminates the parallax / reflection gap between cover glass and panel. Adds $50–150 to BOM, doubles outdoor readability. Non-negotiable above the entry tier.
- **Anti-reflective + anti-glare coatings:** AR reduces specular reflection ~70 %; AG diffuses haze. Both, ideally.
- **Transflective vs transmissive:** transflective panels (Pixel Qi-style, now Topaz / Ortustech) use ambient light and stay readable in direct sun with the backlight off. Expensive, narrower color gamut, but unrivaled in bright conditions.
- **Touch:** projected capacitive (PCAP), ≥ 5-point. Must work with thin gloves — specify a controller IC tuned for high-Z input (FocalTech FT5x or Goodix GT9xx series).
- **Cover glass:** chemically strengthened (Gorilla Glass 3+ or Asahi Dragontrail) bonded to the panel.
- **Viewing angle:** IPS at minimum (178°), avoid TN.

### Panel options by tier

| Tier | Size / Res | Brightness | Bonding | Vendor / part examples | Touch | ~Cost |
|---|---|---|---|---|---|---|
| Min | 5″ 800×480 IPS | 500 nit | none | Waveshare 5DP-CAPLCD, generic | resistive or PCAP | $40–70 |
| Min | 5″ 1280×720 | 700 nit | optional | Hannstar HSD050IDW1 | PCAP | $60–110 |
| Mid | 7″ 1280×800 | 1000 nit | yes | BOE / Innolux N070ICE-GB1 (bonded variant) | PCAP, glove-capable | $130–220 |
| Mid | 7″ 1920×1200 | 1000 nit | yes | Innolux N070JCD-G02, Sharp LQ070Y3DG3B | PCAP | $180–300 |
| High | 7″ 1920×1200 | 1500 nit | yes, AR + AG | Tianma TM070JVHG33 “sunlight readable” | PCAP, glove | $250–400 |
| Max | 7″ 1920×1200 transflective | 2000+ nit equivalent | yes, AR/AG, chemically strengthened cover | Ortustech COM70H8M65ULC, Litemax SLO0708-Y | PCAP, glove + rain | $500–900 |
| Max | 10.1″ 1920×1200 | 1500–2000 nit | yes | Sharp LQ101R1SX03, Tianma TM101JDHP60 | PCAP | $400–700 |

## Radio link — 50% of product capability

The radio is the largest single variable in cost, range, and certification effort. You can build everything else around any of these; you cannot easily swap radios after enclosure design freeze.

### Open / hobby tier (≤5 km LOS, control + 1080p video)

- **ExpressLRS (ELRS) 2.4 GHz or 900 MHz** — open-source LoRa-based RC control link, ≤1 ms RTT, 25–500 Hz packet rates, ~25–40 km LOS in clear RF. **Control + telemetry only**, no video. Tx modules: HappyModel ES24TX Pro, BetaFPV Micro 2.4 GHz, RadioMaster Ranger.
- **OpenHD / WFB-NG (Wireless Broadcasting for Drones)** — software-defined digital video link over 5.8 GHz WiFi cards (RTL8812AU/AU2, MediaTek MT7921) in monitor mode. 1080p30 at 25–60 ms latency, 5–20 km LOS depending on antennas. Open source, runs on Pi / RK3588. Pair with ELRS for control.
- **Walksnail Avatar HD / DJI O3 Air Unit** — closed-source FPV digital video links you could host inside a custom controller, but you are locked to their goggles/decoders unless you tap the analog out. Not recommended for a custom GCS.

### Prosumer / commercial tier (10–30 km LOS, encrypted)

- **CubePilot Herelink Air + Ground modules** — dropping in the Herelink Ground unit as an internal sub-module is the fastest path to a working HD video + telemetry + control link. ~$500 BOM for both ends, 20 km LOS, 1080p60 ~110 ms latency. **Not NDAA-compliant.**
- **Doodle Labs Helix-N (RM-2450 / RM-915 / RM-2455)** — OFDM mesh radios, AES-256, 1–2 W TX, 5–30 km LOS, IP-based (Ethernet). $1.2–2 k per node. NDAA-compliant variants available. The default for prosumer/commercial builds.
- **Microhard pMDDL2450 / pDDL900** — robust point-to-point, 2 W, encrypted, broad regulatory certification. $1.5–2.5 k per node.
- **uAvionix microLink** — newer entrant, 2 W, NDAA, focuses on Type-Certified BVLOS.

### Tactical / max tier (50–100 km, MIMO mesh, mil-grade)

- **Silvus StreamCaster SC4240 / SL4200 “Lite”** — MN-MIMO 2×2 or 4×4, AES-256, mesh, 50–100 km with high-gain antennas. $3–6 k per node. Industry standard for tactical UAS.
- **Persistent Systems Wave Relay MPU5 / Embedded Module** — MANET mesh, AES-256, integrates with ATAK, ~$5–10 k.
- **Domo Tactical SOLO7 / NETNode** — COFDM, NLOS-capable, broadcast-grade.
- **TrellisWare TW-950 TSM Shadow** — barrage relay mesh.

### Cellular / 5G as primary or failover

- **Quectel EC25** (LTE Cat-4, global) — $40–80, USB or PCIe. Min/mid tier.
- **Quectel RM502Q-AE / RM520N** (5G Sub-6, NSA+SA) — $200–400, M.2. Mid/max tier. Pair with eSIM (eUICC) so you can swap carriers in firmware.
- **Telit FN980 / FN990** — NDAA-friendlier 5G alternative.

### Satcom (max tier only)

- **Iridium Certus 100 / 700** (Cobham EXPLORER 323, Thales VesseLINK-style modems shrunken). 22–704 kbps. Useful as a telemetry-only failover. $1.5–3 k module + ~$150/mo airtime.
- **Starlink Mini** as a ground-side backhaul if you can carry it separately (not inside the controller).

## Antennas

See `components/antennas.md` for the full primer. For the controller specifically:

- **MIMO 2×2 minimum** in the prosumer tier and above — spatial diversity halves fade margin requirements.
- **Detachable RP-SMA / SMA pigtails** so operators can swap to high-gain directional (patch, Yagi, helical) for long-range work.
- **Integrated patch on the back of the controller** angled at the typical operator stance (≈30° up) gives ~6–9 dBi forward gain without extra setup.
- **GNSS antenna** (active, 3.3 V LNA, 28 dB gain) on the top edge with clear sky view.
- **Cellular antenna** physically separated from the main link antennas to avoid desensitization; a top-edge or side-edge flex antenna works.
- **WiFi/BT** can share an internal antenna with diversity; keep at least 50 mm from cellular.

## Input controls

The difference between a $200 and a $2,000 controller is felt in the sticks before anything else.

### Gimbals

- **Min:** RadioMaster AG01 Hall-effect gimbals (~$30 ea). Better than the FrSky M7 / Taranis stock by a lot.
- **Mid:** FrSky M9 Hall, RadioMaster AG01-V2, or T-Lite Hall gimbals (~$60–80 ea). Smoother, replaceable springs, adjustable tension.
- **Max:** RadioMaster AG01-Pro magnetic / FrSky M10, or fully custom CNC aluminum Hall gimbals with adjustable centering, dampers, and removable spring kits (cinematic operators self-center; aerial gunners self-center; survey operators ratchet on throttle). Add gimbal triggers (analog pots or Halls).

### Switches, wheels, buttons

Budget at minimum: **6 toggle switches** (2-pos and 3-pos mix), **2 momentary buttons**, **2 analog scroll wheels** (one per index finger), **2 analog triggers** behind the gimbals, **4 programmable face buttons**, a **5-way “key” navigator** for menu use, and a **dedicated emergency / RTH** button under a flip cover.

Prefer Alps Alpine or C&K switches over generic; they survive 100k+ cycles and feel consistent across temperature.

### Realtime MCU

A dedicated MCU (STM32G4, STM32H7, RP2040, or NXP LPC55) reads all inputs, applies expo/curves, and emits SBUS / CRSF / MAVLink RC_CHANNELS_OVERRIDE to the radio modem at ≥500 Hz. Doing this on the AP/SoC introduces jitter from the OS scheduler. Use the MCU — it also handles the watchdog, battery gauge, and fan PWM.

## GNSS on the controller

Why put GNSS on the controller and not just the aircraft?

- **Moving-baseline RTK** — if the aircraft uses RTK and the controller carries a base, you can get cm-level relative positioning with no external base station. Requires u-blox ZED-F9P on **both** ends.
- **Operator “my position”** for TAK CoT, geofences, and “know where I am” during BVLOS handoffs.
- **Follow-me** modes that require operator position.

| Tier | Module | Bands | Accuracy | Notes |
|---|---|---|---|---|
| Min | u-blox NEO-M9N | L1 GPS/GLO/GAL/BDS | 1.5 m CEP | Cheap and good enough |
| Mid | u-blox ZED-F9P | L1/L2 multi-constellation, RTK rover | 1 cm | $180–220 |
| Max | u-blox ZED-F9P + Tallysman TW7972 helical | L1/L2 | 1 cm + heading via dual-antenna | $300–500 |

See `components/rtk-ppk-the-real-story.md` for the integration realities.

## IMU + magnetometer

A 6-axis IMU + 3-axis magnetometer on the controller enables:

- AHRS overlay (“which way am I facing relative to the drone”) for orientation cues.
- **Tilt-to-pan / tilt-to-zoom** gimbal control as a secondary input.
- Step counting / motion logging for op-tempo metrics.

Recommended: **Bosch BMI270** (low-power 6-axis) + **Bosch BMM150** or **PNI RM3100** (mag). The RM3100 is dramatically more stable in iron-rich environments but $20 vs $2.

## Power architecture

Reference budget (mid-tier handheld at full load):

| Subsystem | Typical | Peak |
|---|---|---|
| SoC (RK3588S) | 4 W | 8 W |
| Display (7″ 1000 nit, backlight 80 %) | 4 W | 6 W |
| Radio modem (Helix-N TX 1 W avg) | 5 W | 9 W |
| Cellular modem | 1.5 W | 4 W |
| GNSS + IMU + MCU | 0.5 W | 0.8 W |
| USB charging downstream | 0–2 W | 7.5 W |
| Fan + housekeeping | 0.5 W | 1.5 W |
| **Total continuous** | **~15.5 W** | **~36 W peak** |

### Battery / PMIC

- **Min:** 2× 18650 (Samsung 35E or LG MJ1, 3500 mAh @ 3.6 V) in 2S = ~25 Wh. ~1.5 h runtime. USB-C PD 30 W charging.
- **Mid:** 4S1P or 2S2P Li-ion 21700 (Molicel P42A or Samsung 50S) = ~60 Wh. 4–5 h runtime. USB-C PD 65 W in/out, with hot-swap via dual cells gated by P-FETs.
- **Max:** **dual hot-swap** removable packs (think Powerbank-style cartridges) each ~50 Wh, runtime 8–12 h with one always live. USB-C PD 100 W in/out (passes through to charge other devices or accept external solar/genset). Optional XT30/XT60 secondary for vehicle DC-in.

### PMIC choices

- **TI BQ25700A / BQ25713** — SMBus-controlled buck-boost battery charger, supports USB-PD 3.0 / PPS up to 20 V 5 A, hot-swap-friendly.
- **TI BQ40Z50-R3** — SBS-compliant gas gauge with cell balancing, perfect for 2S–4S Li-ion.
- **TPS65988 / TPS25750** — USB-C PD controller with DisplayPort alt-mode.
- Build for **−5 V to 26 V DC input** so operators can feed it from vehicle, solar, or a generic Li-ion power station.

## Thermals

A sealed handheld with a 1000-nit display + a 1 W TX radio + an RK3588 will easily hit 70 °C internally on a sunny day. Plan for this.

- **Pyrolytic graphite sheet (PGS)** or copper heat-spreader from SoC to enclosure backplate. PGS in-plane k ≈ 1500 W/m·K.
- **Vapor chamber** for max tier (Jetson Orin NX dissipates 10–15 W).
- **One small blower** (Sunon MagLev 30 mm or 40 mm) drawing through a labyrinth vent maintains IP54 while cooling. Add a hydrophobic Gore vent membrane.
- **Thermal throttle the SoC at 75 °C internal**, fan ramps from 50 °C, log all of this to the GCS app.
- **Sun-load model:** a black enclosure in direct sun absorbs ~600 W/m². A 200 cm² front surface = 12 W of solar gain on top of internal dissipation. Light gray / matte exteriors and IR-reflective coatings help.

## Enclosure / mechanical / ergonomics

- **Min:** 3D-printed PETG or ABS; M3 brass heat-set inserts. Good for prototypes, marginal for field use.
- **Mid:** machined polycarbonate or glass-filled nylon; IP54 with gasketed seams; soft TPU overmold on the grip areas; tripod thread on the bottom; sun-hood mount points on the top edge.
- **Max:** CNC aluminum chassis with elastomer bumpers; IP65; MIL-STD-810G shock/vibration/temperature; integrated neck-strap anchors; quick-release tripod plate (Arca-Swiss or Mantis-style); detachable sun-hood; replaceable shoulder strap mounts.

Ergonomically: **15–20° of stick tilt** toward the operator (mimic Herelink / TBS Tango 2), thumb sticks for cinematic operators, pinch-grip / index-finger sticks for racing. Provide both Mode 1 and Mode 2 gimbal mappings in firmware.

Weight target by tier: **<700 g min**, **<1.4 kg mid**, **<2.2 kg max** including battery. Beyond 2 kg, neck strap or chest harness is mandatory.

## Connectivity (the “back panel”)

The ports operators actually use, in priority order:

1. **USB-C** (PD in + DisplayPort alt-mode out + data) — powers the controller, drives an external monitor, sideloads logs.
2. **HDMI out** (mid/max) — mirror display for spotter, recording, or briefing screen.
3. **microSD** — offline map tiles, telemetry logs, mission files. Spec UHS-I A2 minimum.
4. **Nano-SIM tray + eSIM** — for cellular failover.
5. **3.5 mm TRRS audio** — voice comms, intercom, alert tones; tactical operators wire this to their headset.
6. **Ethernet (RJ45 or M12)** (max) — wired backhaul to a base station / starlink terminal.
7. **USB-A** (mid/max) — for keyboards, joysticks, OTG sticks.
8. **GPIO bay** (max) — user-accessible 8–16 pin connector for accessory radios, hand mics, slew-to-cue laser rangefinders, etc.

All external connectors should be **sealed** and located on a single edge under a hinged door, not scattered around the housing — IP rating dies at every seam.

## OS / software stack

| Layer | Min | Mid | Max |
|---|---|---|---|
| OS | Raspberry Pi OS or Armbian | Yocto-built Linux (Wayland + Weston) **or** AOSP Android 13 | Ubuntu 22.04 / 24.04 LTS or AOSP, with PREEMPT_RT for the input MCU bridge |
| Window system | X11 / Wayland | Wayland | Wayland w/ HDR-capable compositor |
| Map renderer | QGC built-in | QGC + Mapbox GL offline tiles | Custom Cesium / MapLibre with terrain + 3D obstacles |
| GCS app | QGroundControl | QGC, Mission Planner, or Auterion AMC | Auterion AMC, ATAK plugin, or custom Flutter / Qt |
| Video pipeline | gst-launch → v4l2decoder → waylandsink | GStreamer with hardware decoder (`v4l2h265dec` on RK3588, `nvv4l2decoder` on Jetson) | Same + on-SoC tracker, picture-in-picture, OSD |
| Radio driver | ELRS USB serial + GStreamer RTP | Vendor SDK (Doodle DGL, Microhard “Pipe”) | Vendor SDK + redundant link mux |
| Update path | manual SD card swap | OTA via Mender or RAUC, A/B rootfs | Signed A/B OTA + remote attestation |

See `components/openhd-implementation-guide.md` for OpenHD-specific build patterns.

## Compliance & regulatory

- **FCC Part 15** (US, license-exempt) — fine for ELRS, WFB-NG on 5.8 GHz at <1 W EIRP, Herelink-class modems. Required testing: FCC ID for the radio module (vendor-provided if integrated), and an unintentional-radiator declaration for the host.
- **FCC Part 90 / Part 96** — needed for high-power Microhard / Silvus / Persistent gear above Part 15 power limits. Operator license required.
- **CE / RED (EU)** — EN 300 328 (2.4 GHz), EN 301 893 (5 GHz), EN 301 489 (EMC), EN 62368-1 (safety).
- **ETSI** — if you ship anywhere outside the US.
- **NDAA Section 889** — no Chinese-origin SoCs (Rockchip, Allwinner, HiSilicon, MediaTek WiFi), no DJI radio, no Hikvision/Dahua optics. See `components/ndaa-compliance.md`.
- **Remote ID** — controller doesn’t need to broadcast Remote ID itself, but should display the aircraft’s RID status. See `components/remote-id-custom-builds.md`.
- **Battery shipping (UN 38.3)** — design batteries ≤ 100 Wh per pack to avoid IATA Section II restrictions; if larger, you ship hazmat-only.
- **Export control** — anything with Silvus / Persistent radios or AES-256 above 56-bit triggers EAR / ITAR review. Plan for this if you sell internationally.

## Full BOM — Minimum tier (~$450–650)

*Target: 1–5 km LOS, hobbyist/research, line-of-sight only, single drone.*

| Subsystem | Part | Notes | Cost |
|---|---|---|---|
| SoC SBC | Radxa Rock 3C / Pi CM4 4GB + carrier | 32GB eMMC | $80 |
| Display | 5″ 800×480 IPS w/ PCAP touch | 500 nit | $50 |
| Radio (control) | ExpressLRS 2.4 GHz Tx module (HappyModel ES24TX Pro) | | $35 |
| Radio (video) | RTL8812AU USB WiFi (Alfa AWUS036ACH) running WFB-NG | | $40 |
| Antennas | 2× 5.8 GHz dipole + 2.4 GHz omni | | $25 |
| Gimbals | 2× RadioMaster AG01 Hall | | $60 |
| Switches/buttons | 6× toggle + 4× button + 2× wheel | Alps generic | $25 |
| Input MCU | STM32G431 Nucleo or RP2040 board | | $10 |
| GNSS | u-blox NEO-M9N module | | $30 |
| IMU | BMI270 breakout | | $8 |
| Battery | 2× 18650 (Samsung 35E) + 2S BMS | ~25 Wh | $25 |
| PMIC / charger | TP4056 + boost or IP2368 | USB-C PD | $15 |
| Cooling | passive heatsink + 25 mm fan | | $8 |
| Enclosure | 3D-printed PETG | self-printed | $20 (material) |
| Misc (cables, connectors, FFC, screws) | | | $40 |
| **BOM total** | | | **~$470** |

## Full BOM — Mid tier (~$1,800–2,800)

*Target: 10–30 km LOS, commercial inspection/mapping/cinematography, prosumer.*

| Subsystem | Part | Notes | Cost |
|---|---|---|---|
| SoC SBC | Radxa Rock 5C (RK3588S, 8 GB) | 64 GB eMMC | $130 |
| Display | 7″ 1920×1200 IPS, 1000 nit, optically bonded | Innolux N070JCD-G02 + bonded touch | $250 |
| Radio (integrated) | CubePilot Herelink Air + Ground module | 1080p60 HD, 20 km | $500 |
| LTE modem | Quectel EC25-AF (mPCIe) + SIM tray | | $70 |
| Antennas | 2×2 MIMO dual-band patch + LTE flex + GNSS active | | $80 |
| Gimbals | 2× FrSky M9 Hall | | $140 |
| Switches/wheels/triggers | 6× toggle, 4× button, 2× wheel, 2× trigger pot, C&K-class | | $80 |
| Input MCU | STM32H743 board | | $25 |
| GNSS | u-blox ZED-F9P + Tallysman TW3970 antenna | RTK rover capable | $250 |
| IMU + mag | BMI270 + RM3100 | | $35 |
| Battery | 4S1P Li-ion 21700 (Molicel P42A) ~60 Wh + smart BMS (BQ40Z50) | | $80 |
| PMIC / charger | TI BQ25713 + TPS65988 USB-PD | 65 W in/out | $30 |
| Cooling | heatpipe + 30 mm blower + Gore vent | | $25 |
| Enclosure | machined PC + TPU overmold, IP54 | small-batch CNC | $200 |
| HDMI/USB/SIM ports + sealed door | | | $50 |
| Speakers + mic for voice comms | | | $20 |
| Haptic motor (LRA) | for alarm/RTL alerts | | $8 |
| Misc (cables, FFC, FPC, fasteners) | | | $80 |
| **BOM total** | | | **~$2,053** |

Substitutions if NDAA is required: swap RK3588S → NXP i.MX 8M Plus (+$50), Herelink → Doodle Labs RM-2455 Helix-N pair (+$2,000), still <$5k BOM.

## Full BOM — Maximum tier (~$8,000–16,000)

*Target: defense / commercial BVLOS / swarm / 50+ km, with onboard CV.*

| Subsystem | Part | Notes | Cost |
|---|---|---|---|
| SoC SBC | NVIDIA Jetson Orin NX 16 GB on Auvidea / ConnectTech carrier | NVMe SSD 512 GB | $1,000 |
| Co-processor (optional) | Hailo-8 M.2 | for redundant CV path | $250 |
| Display | 7″ 1920×1200 transflective, 2000 nit equiv, OCA-bonded, AR+AG | Ortustech COM70H8M65ULC | $700 |
| Radio (integrated) | Silvus StreamCaster SL4200-Lite OEM | 2×2 MIMO, AES-256, 50 km+ | $4,500 |
| Cellular (5G) | Quectel RM502Q-AE M.2 + eSIM/eUICC | global Sub-6 | $300 |
| Satcom (optional) | Iridium Certus 100 OEM (Cobham) | telemetry failover | $1,800 |
| Antennas | 2×2 MIMO patch + omni, dual-band, separable; LTE/5G dual flex; GNSS dual L1/L2; Iridium patch | | $250 |
| Gimbals | 2× RadioMaster AG01-Pro magnetic or custom CNC Hall | + 2 analog triggers | $400 |
| Switches/wheels/buttons | mil-spec C&K, anodized aluminum knobs | flip-cover EMG / RTH | $200 |
| Input MCU | STM32H743 + redundant LPC55 watchdog | | $50 |
| GNSS | u-blox ZED-F9P + dual antenna for heading | RTK base/rover | $400 |
| IMU + mag | BMI270 + RM3100 + tilt-comp baro (LPS22HH) | | $50 |
| Battery | 2× hot-swap 4S 21700 cartridges (~50 Wh ea), smart fuel gauge, MIL-PRF-32383-like contacts | | $250 |
| PMIC / charger | TI BQ25700A + redundant USB-PD 100 W | DC-in 9–26 V | $80 |
| Cooling | vapor chamber + dual 30 mm blower + Gore vent | | $100 |
| Enclosure | CNC aluminum chassis + TPU overmold + Arca tripod plate + sun hood | IP65, MIL-STD-810G | $1,200 |
| Sealed I/O bay | USB-C, HDMI, RJ45 M12, SIM, GPIO | | $150 |
| Speakers + boom mic + 3.5 mm TRRS | | | $50 |
| Haptic motors (LRA) x2 + LED indicator ring | | | $25 |
| EMI / RF shielding cans, gaskets | | | $80 |
| Misc | | | $200 |
| **BOM total (without satcom)** | | | **~$10,135** |
| **BOM total (with satcom)** | | | **~$11,935** |

Add development NRE: certification (~$25k FCC + CE), tooling (~$30–80k for cast/machined parts), and software (~$200–500k for a credible GCS UI + OTA + fleet backend) — these are not BOM but are typically larger than BOM at this tier.

## What people underestimate (expanded)

1. **Display dominates outdoor UX.** Below ~1000 nits is unusable; bonded + AR coatings matter more than resolution.
2. **The radio is 50 % of the product.** A great SoC won’t save a bad RF chain. The Herelink Air/Ground integration shortcut saves 6–12 months of work but locks you out of NDAA markets.
3. **Regulatory and EMI testing eat 3–6 months.** Plan for shielding cans on the radio modem, ferrite beads on every cable that exits the enclosure, and at least two pre-compliance lab trips before formal cert.
4. **Thermals throttle the SoC.** RK3588 and Jetson Orin throttle hard in a sealed enclosure under sun. Budget ≥5 W of active dissipation and instrument it.
5. **Hall-effect gimbals are non-negotiable above the entry tier.** Pot gimbals drift, feel awful after a month, and operators will rate the entire product on stick feel.
6. **Battery hot-swap is the difference between “prosumer” and “commercial.”** Operators who can’t change packs mid-mission lose 20–30 minutes per swap; this kills BVLOS day-rate economics.
7. **OTA + signed updates from day one.** Retrofitting secure boot, A/B partitions, and rollback into shipping firmware is twice the work of building it in.
8. **Software is the long pole.** 6–12 months of GCS app polish (map tiles, mission planner, video pipeline, log review, OTA, fleet) typically out-runs the hardware bring-up.
9. **Ergonomics decide repeat purchases.** Weight distribution, stick angle, button reach, and screen tilt drive operator preference. Prototype with foam and tape before CNC.
10. **Ecosystem lock-in is a feature.** Herelink wins because pairing “just works” with a Cube Orange. Whatever you ship needs to be a one-button bind to your supported flight controllers, or operators won’t care that your hardware is better.

## Recommended starting point

If you are building this today, the **fastest credible path** is:

- **Mid tier**, **RK3588S** main board, **7″ 1000-nit optically-bonded** display, **Herelink Air + Ground** as the radio sub-assembly (you sell the kit with a “non-DJI / non-NDAA” disclaimer), **FrSky M9** gimbals, **dual 21700** battery, **Quectel EC25** for cellular failover, **u-blox ZED-F9P** so you can offer RTK at no marginal cost, **AOSP Android 13** + **QGroundControl** as the launcher.

From that working baseline, fork into:

- **NDAA SKU:** swap to **i.MX 8M Plus** + **Doodle Labs RM-2455** — unlocks Blue UAS adjacent customers.
- **Tactical SKU:** swap to **Jetson Orin NX** + **Silvus SL4200** — unlocks 50 km MIMO mesh + onboard CV / target tracking.

The controller is a platform; design the carrier board and enclosure so the radio modem, SoC SoM, and battery are **module-swappable** at the cable level. That is the lesson Inspired Flight learned with GS-ONE: every defense customer wants a different radio, and if you can drop in Microhard / Silvus / Doodle without re-doing the housing, you win 80 % more deals.

## See also

- `components/ground-control-stations.md` — the landscape of GCS software and existing hardware
- `components/c2-datalinks.md` — control link options
- `components/comms-datalinks.md` — full datalink primer
- `components/openhd-implementation-guide.md` — building OpenHD/WFB-NG end-to-end
- `components/antennas.md` — antenna selection and placement
- `components/cellular-lte-bvlos.md` — cellular for BVLOS / failover
- `components/power-architecture-emi.md` — power rails, EMI, and shielding
- `components/rtk-ppk-the-real-story.md` — RTK on the controller side
- `components/ndaa-compliance.md` — component restrictions for US gov customers
- `components/remote-id-custom-builds.md` — RID display obligations
