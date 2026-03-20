# Orqa — The EU FPV Powerhouse

> **Part 6 — Components**
> Orqa builds the only complete Western-manufactured FPV
> electronics stack: goggles, radio controller, RC link,
> flight controller, ESC, and video transmitter. All designed
> and assembled in Croatia. NDAA compliant.

---

## The Company

Orqa was founded in Osijek, Croatia in 2018. In 2022 they
acquired ImmersionRC — the Swiss company behind RapidFIRE
and the Ghost RC system. ImmersionRC's CEO Tony Cake joined
as CTIO. The combined entity is the only company in the
Western hemisphere that manufactures all drone building
blocks in-house: RF, optics, electronics, firmware, and
mechanical.

| Detail | Value |
|--------|-------|
| HQ | Osijek, Croatia |
| Founded | 2018 |
| Employees | 150+ |
| NDAA | Compliant — EU manufactured |
| ImmersionRC | Acquired 2022 (100% ownership) |
| Defense | Baykar partnership, Croatian military, EU SAFE mechanism |
| Manufacturing | All in-house — only micro-displays sourced externally |

---

## ImmersionRC Ghost — 2.4 GHz RC Link

Ghost is an NDAA-compliant 2.4 GHz RC link using LoRa-based
chirp spread spectrum with adaptive FHSS. For builds that
need compliance AND FPV performance, Ghost is one of very
few non-Chinese-manufactured options.

| Parameter | Value |
|-----------|-------|
| Frequency | 2.4 GHz ISM band |
| Modulation | Chirp Spread Spectrum + Adaptive FHSS (LoRa/FLRC) |
| Protocol | GHST (native), SBus, Fast SBus (200k), SRXL-2 (400k), PWM |
| Telemetry | Bidirectional (Race, Normal, Long Range modes) |
| Tx Modules | JR bay, Lite bay, UberLite (Orqa FPV.Ctrl) — all 350 mW |
| Receivers | Átto (~0.6 g), Átto Duo (true diversity), Zepto, Hybrid DUO/UNO V2 (combined VTx + Rx) |

### RF Modes

| Mode | Update Rate | Telemetry | Use Case |
|------|-------------|-----------|----------|
| Pure Race / Race250 | 222–250 Hz | Disabled | Minimum latency racing |
| Race | 160–166 Hz | Enabled | Racing with telemetry |
| Normal | ~50 Hz | Enabled | General flying, freestyle |
| Long Range | ~15 Hz | Enabled | Maximum range |
| 500 Hz (Hybrid) | 500 Hz | — | Ghost Hybrid hardware |

End-to-end latency runs below 4 ms in race modes. Ghost
works with PX4 (`RC_INPUT` = `GHST`), QGroundControl, and
any FC running Betaflight 4.3+, iNav, or ArduPilot with
GHST protocol support. OpenTX 2.3.13+ recommended.

---

## Orqa F405 3030 FC

| Detail | Value |
|--------|-------|
| MCU | STM32F405 |
| Mounting | 30.5 × 30.5 mm, M3 |
| Voltage | 2S–6S LiPo |
| Firmware | Betaflight, iNav, ArduPilot, PX4 |
| OSD | MAX7456 analog + DisplayPort HD OSD (simultaneous) |
| PWM Outputs | 8 (outputs 1–4 support bi-directional DShot) |
| Connectors | All JST-GH lockable — no soldering required |
| NDAA | Compliant — EU manufactured |

The F405 3030 uses lockable JST-GH connectors throughout —
a significant reliability improvement over solder pads for
field maintenance. Stacks directly onto the Orqa 3030 ESC
with included cables. ArduPilot board target: `OrcaF405Pro`.
Initial firmware load via DFU (hold bootloader button,
flash `with_bl.hex`).

---

## Orqa QuadCore H7 FC

| Detail | Value |
|--------|-------|
| MCU | STM32H743 |
| IMU | ICM-42688-P |
| Mounting | 30.5 × 30.5 mm, M3 |
| Voltage | 3S–6S LiPo |
| Firmware | Betaflight, iNav, ArduPilot, PX4 |
| NDAA | Compliant — EU manufactured |

Higher-spec FC with H7 processor — more flash, faster
processing, more UARTs than the F405. The ICM-42688-P is the
same sensor used in ARK Electronics' NDAA FCs. For new NDAA
builds requiring maximum processing headroom, the QuadCore
H7 is the recommended choice over the F405.

---

## Orqa 3030 4-in-1 ESC

| Detail | Value |
|--------|-------|
| Continuous Current | 70A per motor |
| Battery | 3S–6S |
| Firmware | AM32 (open-source, bi-directional DShot) |
| Protocols | DShot 300/600/1200 |
| Mounting | 30.5 × 30.5 mm |
| Weight | ~28 g |
| NDAA | Compliant — EU manufactured |

Purpose-built to stack with the F405 FC. Hard-mount ESC,
soft-mount FC on top with included silicone gummies. AM32
firmware supports RPM filtering in Betaflight via
bi-directional DShot.

---

## Orqa FPV.One Pilot Goggles

| Detail | Value |
|--------|-------|
| Displays | 2× 0.5" Sony OLED, 1280 × 960 |
| FOV | 37° (4:3) / 33° (16:9) |
| IPD Range | 56–74 mm |
| Focus | -4D to +4D diopter adjustment |
| DVR | Built-in, 1280×960, 50/60 fps, H.264 |
| Video Input | Analog (receiver module bay) + Micro HDMI |
| Power | 6–25 VDC (2S–6S), 2.8 W typical |
| Weight | 259 g (without battery) |

Narrower FOV than Fat Shark HDO2 (46°) trades immersion for
sharper edge-to-edge image quality. Primary bay accepts
standard analog VRx modules (RapidFIRE, Fusion, etc.).
FPV.Connect module adds Bluetooth for firmware updates, DVR
download, GoPro control, and Ghost VTx channel auto-sync.

---

## Orqa FPV.Ctrl Radio Controller

The FPV.Ctrl is a dual-purpose device: simulator game
controller that doubles as a real RC transmitter when paired
with the Ghost UberLite module. Settings and calibration
managed via mobile app (iOS, Android). Recommended entry path
for new FPV operators — learn in sim with the same controller
you'll fly with.

---

## H7 WingCore — Fixed-Wing / VTOL FC

| Detail | Value |
|--------|-------|
| MCU | STM32H743, twin orthogonal ICM-42688 |
| Barometer | DPS310 |
| Current Sensor | 160A on-board |
| Motor Outputs | 4× JST-GH (with ESC telemetry) |
| Servo Outputs | 10× standard 0.1" header |
| Voltage | Up to 12S (50V) |
| Firmware | iNav (preinstalled), ArduPilot, PX4 (in development) |
| Weight | 36.6 g |
| NDAA | Compliant — EU manufactured |

Purpose-built for wings and VTOLs — not a multirotor FC
repurposed. 10 servo outputs handle complex VTOL transition
mechanisms. 50V-rated regulators support 12S battery systems.
Direct JST-GH connection to Orqa Hybrid VTx/C2 modules.
Includes lost-model buzzer with on/off switch for fixed-wing
recovery.

---

## IRONghost — EW-Resilient Dual Sub-GHz C2

| Detail | Value |
|--------|-------|
| Architecture | Dual sub-GHz radio (primary + shadow band) |
| Bands | 9xx MHz (primary) + 4xx MHz (shadow) |
| Max Tx Power | Up to 3W |
| Modulation | Proprietary, firmware-upgradeable |
| Video Integration | Combined C2 Rx + 5.8 GHz analog VTx |
| OTA Updates | Firmware during binding (<60 seconds) |

IRONghost minimizes RF emissions during flight, transmitting
only essential telemetry. The pilot switches between primary
and shadow bands as needed. At 3W (~35 dBm), typical range
is ~22 km with omni antennas. Continuous firmware evolution
improves EW resilience as the threat landscape changes.

**Critical:** Never power on without all antennas attached.
3W reflected back into the amplifiers causes permanent damage.

---

## Orqa Tac.Ctrl — Tactical Controller

| Detail | Value |
|--------|-------|
| C2 Link | IRONghost dual sub-GHz |
| Protocol | MAVLink support |
| TAK Integration | ATAK compatible |
| Multi-Drone | Single controller binds to multiple drones |
| Band Selection | In-field switching between primary and shadow bands |

Defense-oriented radio controller for IRONghost-equipped
platforms. Full IRONghost menu access: band selection, VTx
channel/power configuration, and firmware management. OTA
firmware updates to drone receivers during bind process.

---

## GCS-1 — Ground Control Station

Integrated ground control station for extended-range and
NLOS operations with MRM platforms. IRONghost Ground Unit
paired with high-gain antennas (TrueRC Sniper recommended).
Supports aerial repeaters — a separate drone flown to
altitude as a communication relay for beyond-LOS operations.

---

## DTK APB — Flight Computer + Companion Computer

The DTK APB puts an STM32H743 flight controller and an NXP
i.MX8M Plus Linux computer on the same PCB — 65×40 mm,
50 grams. The FC side runs PX4, ArduPilot, iNav, or
Betaflight. The SOC side runs Orqa Yocto Linux with a
2.25 TOPS NPU, dual MIPI-CSI camera inputs, an H.265
hardware encoder, hardware OSD, and a PCIe expansion slot.

| Detail | Value |
|--------|-------|
| SOC | NXP i.MX8M Plus (4x Cortex-A53 + Cortex-M7) |
| FC MCU | STM32H743 |
| NPU | 2.25 TOPS |
| Video Encoder | H.265 / H.264, 1080p @ 60fps |
| RAM / Storage | 4 GB LPDDR4 / 4 GB eMMC + micro-SD |
| Camera Inputs | 2x 4-lane MIPI-CSI 2 (digital + analog via ADV7282) |
| Connectivity | USB 3.0, 2x UART (switchable), 2x CAN, I2C, 8x PWM, PCIe |
| Power | 2S–8S (max 40V) or USB-C PD (60W) |
| Dimensions | 65 × 40 × 22.11 mm, 50 g |
| Mounting | 30.5 mm, M3 |
| NDAA | Compliant — EU manufactured |

For the full APB technical reference — board layout, UART
routing tables, camera system details, OSD engine, recovery
procedures, and developer notes — see the
[Companion Computers](companion-computers.md) chapter and
the [ORQA developer portal](https://developer.orqafpv.com/index.php/apb-user-manual/).

---

## The Complete Ecosystem

### Component Stack (for custom builds)

| Layer | Product | Interface |
|-------|---------|-----------|
| RC Transmitter | FPV.Ctrl + Ghost UberLite | 2.4 GHz Ghost |
| Tactical Controller | Tac.Ctrl + IRONghost | Dual sub-GHz |
| RC Receiver | Ghost Átto / Duo / Hybrid | GHST protocol to FC |
| EW Receiver | IRONghost Dual-Sub Hybrid | Sub-GHz to FC |
| Flight Controller (Multi) | F405 3030 / QuadCore H7 | JST-GH to ESC |
| Flight Controller (Wing) | H7 WingCore | JST-GH, 10 servo + 4 motor |
| Flight Computer | DTK APB (FC + i.MX8M Plus) | Internal UART/CAN, MIPI-CSI, PCIe |
| ESC | 3030 4-in-1 70A | Direct cable to FC |
| Video Tx | Ghost Hybrid / Tramp / Wing VTx (10W) | 5.8 GHz analog |
| Goggles | FPV.One Pilot | Analog + HDMI |
| Ground Station | GCS-1 + IRONghost GU | Extended range, NLOS capable |

### Complete Platforms

| Platform | Size | C2 | Payload | Range | Use Case |
|----------|------|-----|---------|-------|----------|
| MRM1-5 ISM | 5" | Ghost 2.4 GHz | 1 kg | 15 km | Training, standard ops |
| MRM1-5 EW | 5" | IRONghost | 1 kg | 15 km | Contested environments |
| MRM2-10 | 10" | IRONghost | 2.5 kg | 20 km | Multi-role tactical |
| MRM2-10F | 10" | IRONghost | 2.5 kg | 20 km | Foldable tactical |

---

## Choosing Orqa Components

1. **For NDAA builds needing a complete stack:** The Orqa
   ecosystem is the cleanest option. FC, ESC, Rx, goggles,
   and radio all from one manufacturer, all EU-made.

2. **For mixed builds:** Ghost receivers and Orqa FCs integrate
   cleanly with ModalAI VOXL 2, ArduPilot, PX4, and
   Betaflight. You don't need the full stack.

3. **For fixed-wing / VTOL:** H7 WingCore is the only
   NDAA-compliant FC purpose-built for wings with 10 servo
   outputs and 12S support.

4. **For contested environments:** IRONghost with Tac.Ctrl
   and GCS-1 for dual-band EW-resilient C2.

5. **For FPV + compute:** DTK APB — converged FC + companion
   that keeps you in the analog video ecosystem.

6. **QuadCore H7 vs F405 3030:** H7 for future headroom,
   F405 for matching existing 3030 ESC stacks.

---

*Last updated: March 2026*
