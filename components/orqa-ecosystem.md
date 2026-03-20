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

## H7 WingCore — Fixed-Wing / VTOL Flight Controller

| Detail | Value |
|--------|-------|
| MCU | STM32H743 |
| IMUs | Twin orthogonal ICM-42688 |
| Barometer | DPS310 |
| OSD | Orqa custom NDAA-compliant OSD (text + graphics) |
| Current Sensor | 160A on-board |
| Voltage Regulator | 12S (50V) 8A for 5V supply |
| Servo Regulator | 12S (50V) 10A for 6/7.2V servo power (solder-jumper selectable) |
| Motor Outputs | 4× motor connectors (JST-GH, with telemetry) |
| Servo Outputs | 10× standard 0.1" header servo connectors |
| Connectors | Airspeed (I2C), Hybrid VTx/C2 Rx, High-power VTx, SIK telemetry, dual analog cameras (switchable), CAN bus, GPS/magnetometer, microSD |
| Additional I/O | 1× full UART (UART7 with RTS/CTS), 3× GPIO, 3× ADC, 1× PWM, LED output |
| USB | USB-C on remote-mountable PCB |
| Firmware | iNav (preinstalled), ArduPilot (available), PX4 (under development) |
| Mounting | 30.5 × 30.5 mm, M2 |
| Weight | 36.6 g |
| Dimensions | 54 × 17 × 39 mm |
| NDAA | Compliant — designed and manufactured in EU |

### Purpose-Built for Wings and VTOLs

The H7 WingCore is not a multirotor FC repurposed for fixed
wing. It's designed from the ground up for wings, VTOLs, and
enterprise/defense UAVs. The 10 servo outputs handle the
multi-actuator demands of complex VTOL transition mechanisms
(tilt-rotors, quad-plane configs). The 4 dedicated motor
connectors each include telemetry lines for ESC feedback.

The integrated 160A current sensor and 50V-rated regulators
support up to 12S battery systems — well beyond the typical
6S limit of multirotor FCs. The servo regulator provides
switchable 6V or 7.2V output via solder jumper, matching
standard and high-voltage servo requirements.

### Direct Integration with Orqa C2 Links

The HYBRID connector provides a direct solder-free JST-GH
connection to Orqa's Dual-Sub Hybrid (1.5W or 5W) combined
C2 receiver and video transmitter. The separate VTx connector
supports the 10W Wing VTx for higher-power video downlink.
If VTx is used, the Hybrid connector cannot be used
simultaneously (shared UART6). SIK telemetry radio connects
via a dedicated JST-GH port on UART2.

The board features a lost-model buzzer with on/off switch —
critical for fixed-wing recovery after landing in vegetation.

---

## IRONghost — EW-Resilient Dual Sub-GHz C2 Link

IRONghost is Orqa's EW-resilient command and control link
system, operating on licensed sub-GHz frequency bands. It
represents a significant step beyond standard ISM-band Ghost
for contested environments.

| Detail | Value |
|--------|-------|
| Architecture | Dual sub-GHz radio (primary + shadow band) |
| Primary Band | 9xx MHz |
| Shadow Band | 4xx MHz (multirotor) / 4xx MHz (5" variant) |
| Max Tx Power | Up to 3W (JR module) |
| Modulation | Proprietary, firmware-upgradeable |
| EW Resilience | Designed to resist common jamming on primary band |
| Video Integration | Combined C2 Rx + 5.8 GHz analog VTx in single module |
| OTA Updates | Firmware updates over-the-air during binding (<60 seconds) |
| Frequency Ceiling | ~6.02 GHz (beyond range of most conventional jammers) |
| Antenna Connectors | RP-SMA (not SMA) — do not swap |

IRONghost uses a "listening mode" approach: the drone
minimizes its RF emissions during flight, transmitting only
essential telemetry back to the ground station. The pilot can
switch between primary and shadow bands when needed. Each
band's power level is independently configurable.

The system is designed for continuous firmware evolution —
radios can be updated to improve EW resilience as the threat
landscape changes. The upper frequency limit (~6 GHz) sits
above the range of most conventional jamming equipment.

**Critical safety note:** Never power on an IRONghost-equipped
drone without all antennas properly attached. Reflecting 3W of
RF power back into the amplifiers without an antenna load will
cause permanent damage.

### Range Scaling

IRONghost follows standard RF link budget math. At 100 mW
(20 dBm), typical range is ~4 km with omni antennas. At 3W
(~35 dBm), the 15 dB increase corresponds to a 5.6× range
multiplier — roughly 22 km. Directional antennas on the
ground station further extend this.

---

## Orqa Tac.Ctrl — Tactical Controller

The Tac.Ctrl is Orqa's defense-oriented radio controller,
purpose-built for IRONghost-equipped platforms. It replaces
the consumer FPV.Ctrl for tactical operations.

| Detail | Value |
|--------|-------|
| C2 Link | IRONghost dual sub-GHz |
| Protocol | MAVLink support |
| TAK Integration | ATAK compatible |
| Multi-Drone | Single controller binds to multiple drones |
| Band Selection | In-field switching between primary and shadow bands |
| VTx Control | Channel, band, power, and on/off via menu |
| Firmware Updates | OTA to drone receivers during bind process |

The Tac.Ctrl provides full IRONghost menu access: radio band
selection, VTx channel/power configuration, and firmware
management. Channel mappings follow the standard FPV layout
(Roll/Pitch/Throttle/Yaw on CH1-4, Arm on CH5, VTx on CH11)
with additional channels for camera control, payload
activation, flight mode, pre-arm, and band/power sliders.

---

## Orqa GCS-1 — Ground Control Station

The GCS-1 is Orqa's integrated ground control station for
extended-range and NLOS (non-line-of-sight) operations with
MRM platforms.

Key components include the IRONghost Ground Unit (QS 9xx/4xx)
paired with IRONghost GU RF modules for maximum range, and
support for aerial repeaters — a separate drone flown to
altitude as a communication relay between GCS-1 and the
operational platform. This enables operations beyond direct
line of sight, around terrain features and urban obstacles.

For video downlink, the GCS-1 pairs with high-gain directional
receiver antennas. TrueRC Sniper 5.8 GHz antennas are
specifically recommended by Orqa for maximum video range.

---

## MRM Platform Family — Multi-Role Multicopters

Orqa manufactures a family of multi-role FPV multicopter
platforms for defense, law enforcement, and enterprise
applications. All MRM platforms use Orqa's in-house electronics
stack, are NDAA-compliant (EU-manufactured), and are designed
for rapid field deployment.

### MRM2-10 — 10" Multi-Role Platform

| Detail | Value |
|--------|-------|
| Type | Quadcopter, 10" propellers |
| Frame | Carbon fiber body and arms |
| Wheelbase | 465 mm diagonal |
| FC | H7 QuadCore (STM32H743) |
| ESC | 30×30 70A, AM32 firmware |
| Motors | 2814-class, 880 kV |
| Camera | Orqa Justice Analog (1200 TVL, low-light optimized) |
| C2 Link | IRONghost dual sub-GHz |
| Video | 5.8 GHz analog |
| GPS | Integrated with compass and barometric sensor |
| Battery | 6S4P Li-ion recommended (~16000 mAh) |
| Connectors | 1× XT90 + 2× XT60 (parallel) |
| Max Payload | 2.5 kg (up to 3 kg depending on conditions) |
| Cruise Speed | ~70 km/h (optimal efficiency) |
| Est. Range | ~20 km (with recommended battery at cruise speed) |
| Firmware | Betaflight v4.1 (default), BF Configurator v10.10.0+ |
| TAK | MAVLink + ATAK via Tac.Ctrl |
| Controller | Orqa Tac.Ctrl (mandatory) |
| NDAA | Compliant — EU manufactured |

The MRM2-10 ships with OSD telemetry showing mAh/km for
real-time range optimization. Lowering cruise speed below the
70 km/h optimum reduces efficiency due to hover penalty;
exceeding it exponentially increases current draw.

### MRM2-10F — 10" Foldable Variant

| Detail | Value |
|--------|-------|
| Type | Foldable quadcopter, 10" propellers |
| Deployment | Hand-deployable in ~10 seconds |
| C2 Link | IRONghost dual sub-GHz |
| Video | 5.8 GHz analog |
| Battery | 6S4P Li-ion recommended (~16000 mAh) |
| Max Payload | 2.5 kg |
| Cruise Speed | ~70 km/h |
| Est. Range | ~20 km |
| Firmware | Betaflight v4.1 |
| Controller | Orqa Tac.Ctrl (mandatory) |
| NDAA | Compliant — EU manufactured |

Same electronics and performance as the MRM2-10, with folding
arms for transport. Arms click-lock into position when
unfolded. The fold/unfold cycle does not require propeller
removal. All propellers use "outwards rotation" configuration.

### MRM1-5 — 5" Robust Multi-Role Platform

| Detail | Value |
|--------|-------|
| Type | Quadcopter, 5" propellers |
| Frame | Robust carbon fiber |
| FC | F405 30×30 |
| ESC | 30×30 60A, AM32 firmware |
| Motors | 2408, 2200 kV |
| Camera | Orqa Justice Analog (1200 TVL, switchable 4:3/16:9) |
| C2 Link | ISM variant: Ghost 2.4 GHz / EW variant: IRONghost dual sub-GHz |
| Video | 5.8 GHz analog |
| GPS | Integrated |
| Battery | P50B 4S1P Li-ion (included), 4S2P recommended for range |
| Max Payload | 1 kg |
| Max Speed | 130 km/h (unloaded), 60 km/h (1 kg payload) |
| Flight Time | >15 min (unloaded), ~10 min (1 kg with 4S2P) |
| Est. Range | Up to 15 km (unloaded), >5 km (1 kg with 4S2P) |
| Weight | 562 g ISM / 590 g EW (without battery) |
| Firmware | Betaflight, ArduPilot, iNav options |
| TAK | MAVLink + ATAK support |
| Controller | EW: Tac.Ctrl (mandatory) / ISM: FPV.Ctrl or any 2.4 GHz RC |
| NDAA | Compliant — EU manufactured |

The MRM1-5 is the entry-level MRM platform. Available in two
variants: ISM (Ghost 2.4 GHz, standard operations) and EW
(IRONghost, contested environments). The ISM variant works
with any Ghost-compatible controller; the EW variant requires
the Tac.Ctrl.

---

## DTK APB — Flight Computer + Companion Computer

The DTK APB is Orqa's single-board answer to the "FC + companion
computer" integration problem. Instead of wiring a Pixhawk to a
Raspberry Pi over UART and hoping for the best, APB puts an
STM32H743 flight controller and an NXP i.MX8M Plus Linux computer
on the same PCB — sharing power, sharing buses, sharing a 65×40 mm
footprint that weighs 50 grams.

The FC side runs PX4, ArduPilot, iNav, or Betaflight. The SOC side
runs Orqa's Yocto Linux BSP with a 2.25 TOPS NPU for real-time AI,
an H.265/H.264 hardware encoder at 1080p60, dual 4-lane MIPI-CSI
camera inputs, and a PCIe expansion slot. The two halves communicate
over internal UART and CAN — no external wiring, no connector
failures, no integration guesswork.

For builds that need onboard computer vision, AI inference, video
processing, or autonomy running alongside a traditional flight
controller, the APB eliminates the carrier board problem entirely.

### Specifications

| Detail | Value |
|--------|-------|
| SOC | NXP i.MX8M Plus (4x Cortex-A53 + Cortex-M7) |
| FC MCU | STM32H743 (Cortex-M7) |
| NPU | 2.25 TOPS |
| GPU | 3D + 2D |
| Video Encoder | H.265 / H.264, 1080p @ 60fps |
| RAM | 4 GB LPDDR4 |
| Storage | 4 GB eMMC + micro-SD up to 512 GB |
| IMU | ICM42605 |
| Barometer | DPS310 |
| Camera Inputs | 2x 4-lane MIPI-CSI 2 (CSI 1: digital, CSI 2: digital or analog via ADV7282) |
| Analog Video Out | LVDS-to-CVBS, 720×480 @ 60 Hz (Weston/Wayland) |
| OSD | ORQA OSD engine — I2C2 @ 0x0a, max7456 emulation |
| Connectivity | USB 3.0, USB 2.0, 2x UART (switchable), 2x CAN, I2C, 8x PWM, PCIe |
| Power | 2S–8S battery (external connector, max 40 V) or USB-C PD up to 60 W |
| Dimensions | 65 × 40 × 22.11 mm |
| Weight | 50 g |
| Temp Range | 0°C – 70°C |
| Mounting | 30.5 mm, M3 |
| Software | Orqa Yocto Linux BSP, Orqa SDK (Developer Program) |
| FC Firmware | PX4 / ArduPilot / iNav / Betaflight |
| NDAA | Compliant — EU manufactured |

### Board Layout

The APB has connectors on all four edges across both sides of the PCB.

**Top side** — CSI 1 and CSI 2 (MIPI camera inputs), SIK/Gimbal
connector (STM UART6), force flash mode button, DBG (IMX debug
UART2), fan connector, SD card slot, and three bottom-edge
connectors: HYBRID (STM) carrying +5V_SW / VID_OUT / V_IN /
UART3, PWR (IMX) carrying VBUS_IN, and MFC (STM) carrying V_IN /
UART3_TX / FC_GPIO1–4.

**Bottom side** — CAM INPUT (STM) with +5V_SW / VID_IN, GPS (STM)
with UART7 / I2C1, GIMBAL (IMX) with UART1 / V_IN, DFU MODE
button, USB (IMX) with VSYS_5V / USB data, ESC (STM) with 8 motor
outputs / UART8_RX / ADC_CURR, and CANBus (IMX) with CAN_L /
CAN_H / +5V_SW.

### Network & SSH

USB-C RNDIS: Board presents as USB Ethernet at `192.168.75.1`, auto
DHCP to host. SSH: `ssh root@192.168.75.1`. USB-C Ethernet adapter:
DHCP client + static `192.168.1.75`. MAC prefix: `4E:52:51:`.

### UART Routing

UART3 (`/dev/ttymxc2`) connects through an internal GPIO switch
that routes it to three possible destinations:

| SW1 | SW2 | Destination |
|-----|-----|-------------|
| 0 | 0 | CSI 1 Connector |
| 0 | 1 | CSI 2 Connector |
| 1 | 0 | FC UART |

SW1 = GPIO4_IO00, SW2 = GPIO4_IO13. Example routing UART3 to FC:

```bash
gpioset -c gpiochip3 -z 13=1
gpioset -c gpiochip3 -z 0=0
```

UART1 (`/dev/ttymxc0`) is exposed on SOC Connector 1 for general
use — gimbal, telemetry radio, or other serial peripherals.

### Camera System

**CSI 1** — 4-lane MIPI-CSI, default: 1280×720 @ 60fps digital.
Device: `/dev/video2`.

**CSI 2** — Switchable between digital MIPI and analog CVBS input
via ADV7282 decoder. Analog mode: 720×576 PAL @ 50fps, progressive
(de-interlaced internally). Device: `/dev/video3`. Switch between
digital and analog by changing the device tree with
`orqa_dt_switcher`:

- `imx8mp-orqa-apb-rev2.dtb` — CSI 2 digital (default)
- `imx8mp-orqa-apb-rev2-adv.dtb` — CSI 2 analog

Reboot required after switching. Settings persist across updates.

**Analog video output** — GPIO-controlled LVDS-to-CVBS switch:

```bash
gpioset -c gpiochip1 -z 20=0   # LVDS to CVBS output (SOC display)
gpioset -c gpiochip1 -z 20=1   # Analog camera passthrough
```

Output runs Wayland/Weston at 720×480 @ 60 Hz. Test with:
`gst-launch-1.0 videotestsrc ! autovideosink`

### OSD Engine

ORQA's hardware OSD emulates the MAX7456 interface over I2C2
(`/dev/i2c-1`, address `0x0a`). This allows drawing text and
graphics overlays on the analog video output without touching
the live video stream — zero additional latency. The OSD chip
sits between the analog camera input and the VTx output, so
overlays appear on the transmitted feed in real time.

### CAN Bus

CAN 1 is exposed on SOC Connector 2 (bottom side CANBus connector)
for external peripherals — GPS, rangefinder, or DroneCAN devices.
CAN 2 is routed internally to the FC.

### Power

The board accepts 2S–8S battery input through the external power
connector (max 40 V, 4-pin JST-GH 1.25). USB-C PD provides up to
60 W (5 V – 20 V, max 3 A) but may not supply enough power for
the FC under load — supplement with external power for full
operation. Always apply external power before connecting USB when
using both simultaneously.

**Thermal note:** The i.MX8M Plus generates significant heat under
sustained AI/video workloads. Ensure airflow when the board is
stationary or not enclosed in the heatsink assembly. Auto shutdown
triggers at 95°C. Monitor with: `cat /sys/class/thermal/thermal_zone0/temp`

### Recovery & Flashing

The board enters recovery mode after three failed boot attempts.
Recovery provides telnet access at `192.168.75.1` (root, no
password) with full filesystem access.

For complete re-flash (soft brick recovery), use NXP's `uuu`
utility from [nxp-imx/mfgtools](https://github.com/nxp-imx/mfgtools):

| Mode | USB Vendor:Product | How to enter |
|------|-------------------|--------------|
| Fastboot | 0x35b6:0x0210 | `orqa-reboot fastboot` on running board |
| Flash | 0x1fc9:0x0146 | Hold button while powering on |

Persistent partitions: `nvram` (64 MB, config files) and `data`
(remaining flash, general use) survive both OTA updates and
re-flashing.

### Analog Camera Quirk

The ADV7282 CVBS decoder will hang if the video stream isn't
properly stopped before the application exits. Always call
`VIDIOC_STREAMOFF` and `close()` on the camera file descriptor:

```c
enum v4l2_buf_type type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
ioctl(camera_fd, VIDIOC_STREAMOFF, &type);
close(camera_fd);
```

---

## The Complete Orqa Ecosystem

Orqa's product line spans from individual components to
complete integrated platforms. The electronics stack is shared
across all products — the same FC, ESC, and radio technology
in standalone components and in complete MRM platforms.

### Component Stack (for custom builds)

| Layer | Product | Interface |
|-------|---------|-----------|
| RC Transmitter | FPV.Ctrl + Ghost UberLite | 2.4 GHz Ghost |
| Tactical Controller | Tac.Ctrl + IRONghost | Dual sub-GHz |
| RC Receiver | Ghost Átto / Duo / Hybrid | GHST protocol to FC |
| EW Receiver | IRONghost Dual-Sub Hybrid | Sub-GHz to FC |
| Flight Controller (Multi) | F405 3030 / QuadCore H7 | JST-GH to ESC |
| Flight Controller (Wing) | H7 WingCore | JST-GH, 10 servo + 4 motor |
| Flight Computer | DTK APB (FC + i.MX8M Plus companion) | Internal UART/CAN, 2x MIPI-CSI, PCIe |
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

This is the only complete Western-manufactured FPV drone
ecosystem available — from individual EU-sourced components
for custom builds to fully integrated tactical platforms with
EW-resilient communications and ground control stations.

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

4. **For fixed-wing / VTOL:** H7 WingCore is the only
   NDAA-compliant FC purpose-built for wings with enough
   servo outputs for complex VTOL configs. Direct JST-GH
   connection to Orqa Hybrid VTx/C2 modules.

5. **For contested environments:** IRONghost-equipped MRM
   platforms with Tac.Ctrl and GCS-1 provide EW-resilient
   operations with dual-band C2 and MAVLink/ATAK integration.

6. **QuadCore H7 vs F405 3030:** If you have budget and want
   future headroom, go H7. If you're matching to an existing
   3030 ESC stack or need ArduPilot with well-documented
   board targets, the F405 is battle-tested.

---

*Last updated: March 2026*
