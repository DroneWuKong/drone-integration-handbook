# Orqa — The EU FPV Powerhouse

> **Part 6 — Components**
> Orqa builds the only complete Western-manufactured FPV
> electronics stack: goggles, radio controller, RC link,
> flight controller, ESC, and video transmitter. All designed
> and assembled in Croatia. NDAA compliant.

---

## The Company

Orqa was founded in Osijek, Croatia in 2018 by Srdjan
Kovačević (CEO), Ivan Jelušić (CSO), and Vlatko Matijević
(CTO). The company debuted its FPV.One goggles at CES 2019,
ran a Kickstarter that hit its goal in two minutes, and has
been expanding vertically ever since.

| Detail | Value |
|--------|-------|
| HQ | Osijek, Croatia |
| Founded | 2018 |
| Employees | 150+ |
| NDAA | Compliant — EU manufactured |
| ImmersionRC | Acquired 2022 (100% ownership) |
| Funding | $5.8M from Lightspeed Venture Partners (2024) |
| Defense | Baykar partnership (TB2 integration), Croatian military contracts, EU SAFE mechanism procurement |
| Manufacturing | All engineering in-house — RF, optics, electronics, firmware, mechanical. Only micro-displays sourced externally. |

In 2022, Orqa acquired ImmersionRC — the Swiss company that
pioneered FPV electronics with products like RapidFIRE and
the Ghost RC system. ImmersionRC's CEO Tony Cake joined as
CTIO. The combined entity is the only company in the Western
hemisphere that manufactures all drone building blocks
in-house.

The company has since pivoted from pure consumer FPV into
defense. Their FPV MRM-2 Interceptor is in service with the
Croatian military. A €100M procurement through the EU SAFE
mechanism will supply Orqa drones to Ukraine. A partnership
with Estonian company Lendurai targets a joint assembly plant
and autonomous next-gen FPV drones, in a deal reportedly
worth ~€400M.

---

## ImmersionRC Ghost — 2.4 GHz RC Link System

Ghost is a complete RC control ecosystem operating on 2.4 GHz.
Designed by ImmersionRC (now Orqa) as a competitor to TBS
Crossfire and ExpressLRS, Ghost uses LoRa-based chirp spread
spectrum with adaptive FHSS for both long-range reach and
ultra-low-latency racing performance.

### Why Ghost Matters

Ghost sits in a unique position: it's a European-manufactured,
NDAA-compliant RC link with both race performance and long-range
capability. For builds that need compliance AND FPV performance,
Ghost is one of very few options that isn't Chinese-manufactured.

### Ghost Transmitter Modules

| Module | Form Factor | Antenna | Max Power | Compatibility |
|--------|-------------|---------|-----------|---------------|
| Ghost JR Module | JR bay | Dual dipole (2.1 dBi), Tx diversity | 350 mW | Any JR-compatible Tx (Taranis, Jumper, etc.) |
| Ghost xLite Module | Lite bay | Single dipole | 350 mW | Lite-bay Tx (Taranis X9 Lite, TBS Tango 2 w/ mod) |
| Ghost UberLite Module | Orqa-specific | Integrated foldable | 350 mW | Orqa FPV.Ctrl radio controller |

All modules feature an integrated OLED display and joystick
for menu navigation, spectrum analyzer, and real-time latency
display. No Lua scripts required.

### Ghost Receivers

| Receiver | Weight | Size (mm) | Antennas | Notes |
|----------|--------|-----------|----------|-------|
| Ghost Átto | ~0.6 g | 14.8 × 11.5 | 1× U.FL | Smallest Ghost Rx. Single channel. |
| Ghost Átto Duo | ~1.0 g | — | 2× U.FL | Dual independent receiver channels. True diversity. |
| Ghost Zepto | ~0.5 g | — | 1× MHF4 | Smallest form factor. Standard MHF4 connector. |
| Ghost Hybrid DUO V2 | ~2.2 g | 20×20 / 25.5×25.5 | 2× qTee | Combined 5.8 GHz VTX (25–600 mW) + 2.4 GHz Rx. Two full Rx channels. |
| Ghost Hybrid UNO V2 | ~2.2 g | 20×20 / 25.5×25.5 | 1× qTee | Combined VTX + Rx. Single channel. Single-sided for low-profile mounting. |
| Ghost Proton 30×30 | — | 30×30 | — | PCB carrier for Tramp Nano + Ghost. Simplifies wiring/mounting/cooling. |
| Ghost Proton 25×25 | — | 25×25 | — | Same concept, 25×25 stack. |

### Ghost Technical Specs

| Parameter | Value |
|-----------|-------|
| Frequency | 2.4 GHz ISM band |
| Modulation | Chirp Spread Spectrum + Adaptive FHSS (LoRa/FLRC) |
| Binding | Bidirectional with confirmation and protocol negotiation |
| Protocol | GHST (native), SBus, Fast SBus (200k), SRXL-2 (400k), PWM |
| Telemetry | Bidirectional (available in Race, Normal, Long Range modes) |

### RF Modes

| Mode | Update Rate | Modulation | Telemetry | Use Case |
|------|-------------|------------|-----------|----------|
| Pure Race / Race250 | 222–250 Hz | MSK / FLRC | Disabled | Minimum latency racing |
| Race | 160–166 Hz | LoRa | Enabled | Racing with telemetry |
| Normal | ~50 Hz | LoRa | Enabled | General flying, freestyle |
| Long Range | ~15 Hz | LoRa | Enabled | Maximum range |
| 500 Hz (Hybrid) | 500 Hz | FLRC | — | Ghost Hybrid hardware, synchronized frames |

End-to-end latency (OpenTx to flight controller) runs below
4 ms in race modes. ModalAI recommends Race Mode for optimal
balance of performance and range in non-long-range scenarios.

### Integration Notes

Ghost works with ModalAI VOXL 2 (set `RC_INPUT` to `GHST` in
`voxl-px4.conf`), QGroundControl (set `RC_INPUT_PROTO` to
`GHST`), and any FC running Betaflight 4.3+, iNav, ArduPilot,
or PX4 with GHST protocol support. OpenTX 2.3.10+ required
for native GHST support (2.3.13+ recommended).

The Orqa FPV.Connect module on the FPV.One goggles integrates
with Ghost — a mounted Ghost Átto on the FPV.Connect board
auto-syncs VTX channel switching from the Ghost Tx UI.

---

## Orqa F405 3030 FC — NDAA Flight Controller

| Detail | Value |
|--------|-------|
| MCU | STM32F405 |
| IMU | Multiple options (board revision dependent) |
| Mounting | 30.5 × 30.5 mm, M3 |
| Voltage | 2S–6S LiPo |
| Firmware | Betaflight, iNav, ArduPilot, PX4 |
| OSD | MAX7456 analog + DisplayPort HD OSD (simultaneous) |
| PWM Outputs | 8 (outputs 1–4 support bi-directional DShot) |
| Features | microSD slot, switchable dual camera inputs, locking JST-GH connectors |
| Compass | None built-in (external I2C supported) |
| NDAA | Compliant — designed and manufactured in EU |

### What Sets It Apart

The F405 3030 requires **no soldering**. All connections use
lockable JST-GH connectors — a significant reliability
improvement over hobby-standard pin headers and solder pads.
This matters for field maintenance: a connector-based FC can
be swapped in minutes without a soldering iron.

The FC ships with soft silicone gummies for vibration
isolation. When stacked atop the Orqa 3030 ESC, the
recommended approach is to hard-mount the ESC and soft-mount
the FC on top using the gummies.

### ArduPilot Configuration

For ArduPilot users, the board target is `OrcaF405Pro`. Key
parameters for analog OSD: `OSD_TYPE = 1` (MAX7456). For
simultaneous DisplayPort HD OSD: set `OSD_TYPE = 5` and
`SERIAL6_PROTOCOL = 42` (USART6 to HD air unit).

For BetaflightX motor wiring migration, outputs M1–M4 are
pre-configured with default motor mapping parameters. Voltage
sensor is built-in via VBAT pin. No internal current sensor —
use an external sensor on the Curr pin. If paired with the
Orqa 3030 ESC, default voltage/current calibration values are
pre-programmed and correct.

Initial firmware load via DFU: plug USB while holding the
bootloader button, flash `with_bl.hex`.

---

## Orqa QuadCore H7 — Next-Gen NDAA Flight Controller

| Detail | Value |
|--------|-------|
| MCU | STM32H743 (H7 family) |
| IMU | ICM-42688-P |
| Mounting | 30.5 × 30.5 mm, M3 |
| Voltage | 3S–6S LiPo |
| Firmware | Betaflight, iNav, ArduPilot, PX4 |
| NDAA | Compliant — designed and manufactured in EU |

The QuadCore H7 is Orqa's higher-spec FC with the H7
processor family — more flash, faster processing, more UARTs
than the F405. The ICM-42688-P IMU is the same sensor used in
ARK Electronics' NDAA FCs and is considered better than the
hobby-standard BMI270. For new builds requiring NDAA
compliance and maximum processing headroom, the QuadCore H7
is the recommended choice over the F405.

---

## Orqa 3030 4-in-1 ESC — NDAA

| Detail | Value |
|--------|-------|
| Type | Brushless 4-in-1 |
| Continuous Current | 70A per motor |
| Burst Current | 80A (10 seconds) |
| Battery | 3S–6S |
| Firmware | AM32 pre-installed |
| Protocols | DShot 300/600/1200, including bi-directional |
| Mounting | 30.5 × 30.5 mm |
| Weight | ~28 g |
| Connectors | Includes direct-connect cable for Orqa F405 3030 FC |
| NDAA | Compliant — designed and manufactured in EU |

The 3030 ESC is purpose-built to stack with the F405 FC.
Hard-mount the ESC, soft-mount the FC on top. The included
JST-GH cable eliminates custom wiring between the two boards.

AM32 firmware (open-source ESC firmware, successor to
BLHeli_32 for open development) means the ESC supports
bi-directional DShot for RPM filtering in Betaflight — a
significant tuning advantage.

---

## Orqa FPV.One Pilot Goggles

| Detail | Value |
|--------|-------|
| Displays | 2× 0.5" Sony OLED |
| Resolution | 1280 × 960 pixels |
| Aspect Ratio | 4:3 native, 16:9 (720p) supported |
| FOV | 37° (4:3) / 33° (16:9) — switchable |
| IPD Range | 56–74 mm |
| Focus | -4D to +4D diopter adjustment |
| DVR | Built-in, 1280×960, 50/60 fps, H.264 MP4 |
| Video Input | Analog (via receiver module bay) + Micro HDMI (digital) |
| Power | 6–25 VDC (2S–6S Li-ion), 2.8 W typical |
| Head Tracker | Built-in, 3.5 mm jack output |
| Weight | 259 g (without battery) |
| Dimensions | 177 × 107 × 72 mm |
| Made In | Croatia, EU (hand-assembled, QC'd by engineers) |

### Design Philosophy

The FPV.One Pilot is built for operators who need precision
optics over wide-screen cinematic viewing. The 37° FOV is
narrower than Fat Shark HDO2 (46°) — more like sitting a few
rows back in a cinema versus the front row. The tradeoff is
sharper edge-to-edge image quality with zero aberrations. Some
pilots prefer this for racing; the entire image is visible
without eye movement.

### Architecture

Two module bays enable expandability. The primary bay accepts
standard analog VRx modules (RapidFIRE, Fusion, etc.). The
"Portal" connector on top is the interface for Orqa's upcoming
HD digital system and can be used for wired video output,
external cameras, or special antennas.

Redesigned optical engines eliminated the two top fans from
the original FPV.One. Each optical engine now has its own
dedicated fan with automatic defogging — no more foggy lenses
or dry eyes from constant airflow.

Overvoltage and reverse polarity protection mean you won't
fry the displays by plugging in the wrong battery. Accepts up
to 6S.

### FPV.Connect Integration

The FPV.Connect module enables Bluetooth connectivity to the
Orqa mobile app for firmware updates, DVR download, and
settings management. Full GoPro integration (Hero 8/9/10)
allows direct camera control from the goggles: battery status,
SD card status, recording start/stop, resolution/FPS switching.

When paired with a Ghost Átto on the FPV.Connect board, the
goggles auto-sync VTX channel changes from the Ghost Tx —
no manual channel switching required.

---

## Orqa FPV.Ctrl Radio Controller

The FPV.Ctrl is a dual-purpose device: a simulator game
controller that doubles as a real RC transmitter when paired
with the Ghost UberLite module. Settings, firmware, channel
assignment, and stick calibration are managed via the
FPV.Ctrl mobile app (iOS, Android, Huawei).

This is the recommended entry path for new FPV operators:
learn in a simulator with the same controller you'll fly with,
then add the Ghost module and go fly. The UberLite module
provides full 2.4 GHz Ghost capability with 500 Hz
synchronized frames, integrated foldable antenna, and 350 mW
output.

---

## The Complete Orqa Stack

For NDAA-compliant FPV builds, Orqa offers a fully integrated
electronics stack where every component is designed to work
together:

| Layer | Product | Interface |
|-------|---------|-----------|
| RC Transmitter | FPV.Ctrl + Ghost UberLite | 2.4 GHz Ghost |
| RC Receiver | Ghost Átto / Duo / Hybrid | GHST protocol to FC |
| Flight Controller | F405 3030 / QuadCore H7 | JST-GH to ESC |
| ESC | 3030 4-in-1 70A | Direct cable to FC |
| Video Tx | Ghost Hybrid (combined VTX+Rx) or Tramp | 5.8 GHz analog |
| Goggles | FPV.One Pilot | Analog + HDMI |

This is the only complete Western-manufactured FPV electronics
stack available. Every component is EU-sourced and
NDAA-compliant. The JST-GH connector standard across the
stack eliminates solder joints and enables rapid field swap.

---

## Choosing Orqa Components

1. **For NDAA builds needing a complete stack:** The Orqa
   ecosystem is the cleanest option. FC, ESC, Rx, goggles,
   and radio all from one manufacturer, all EU-made, all
   designed to connect together.

2. **For mixed builds:** Ghost receivers and Orqa FCs integrate
   cleanly with ModalAI VOXL 2, ArduPilot, PX4, and
   Betaflight. You don't need the full Orqa stack to use
   individual components.

3. **For racing:** Ghost in Pure Race / Race250 mode delivers
   sub-4ms latency with 222–250 Hz updates. The FPV.One Pilot
   goggles' focused FOV favors precision over immersion.

4. **QuadCore H7 vs F405 3030:** If you have budget and want
   future headroom, go H7. If you're matching to an existing
   3030 ESC stack or need ArduPilot with well-documented
   board targets, the F405 is battle-tested.

---

*Last updated: March 2026*
