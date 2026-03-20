# Ghost RC Link — Operator Configuration Reference

> **Part 7 — Field Operations**
> Complete binding, configuration, and integration guide for
> the ImmersionRC/Orqa Ghost RC control system. Covers all
> transmitter modules, receivers, and flight controller
> integration.

---

## Quick Reference

| Task | Method |
|------|--------|
| Bind Ghost to drone | FPV.Ctrl app → Ghost Menu → Start Bind |
| Set protocol on FC | GHST (recommended over SBus) |
| Update Tx module firmware | Ghost Updater app (Windows/Mac) via USB |
| Update Rx firmware | Automatic on bind to updated Tx |
| VOXL 2 RC input | Set `RC_INPUT = GHST` in `/etc/modalai/voxl-px4.conf` |
| QGroundControl | Set `RC_INPUT_PROTO` parameter to `GHST` |
| OpenTX minimum version | 2.3.10 (2.3.13+ recommended for full support) |

---

## Binding Procedures

### Method 1 — FPV.Ctrl App (Recommended)

This is the primary binding method for the Orqa FPV.Ctrl
radio with Ghost UberLite module.

1. Power on the Orqa transmitter.
2. Open the Orqa FPV.Ctrl app on your phone/tablet.
3. Connect to the transmitter via Bluetooth (app walks
   through pairing on first use).
4. Navigate to **Ghost Menu** within the app.
5. If the receiver is new, it auto-enters bind mode on
   power-up. For a previously bound receiver, power it up
   and press the button next to the antenna connector within
   30 seconds — the LED turns blue (searching).
6. In the Ghost Menu, select your desired protocol (GHST
   recommended). Set Rx ID (only matters if flying multiple
   drones simultaneously).
7. Tap **Start Bind**. Wait for "Success" message.
8. Restart both drone and transmitter after successful bind.

### Method 2 — Quick Bind (No App)

For field situations where the app isn't needed and default
settings are acceptable:

1. Power on the Orqa transmitter.
2. Press the button on the back of the antenna module — LED
   turns blue (bind mode).
3. Power up the receiver and put it in bind mode (press
   button near antenna connector within 30 seconds of
   power-on — LED turns blue).
4. Both devices cycle through color sequences, then settle
   on solid green.
5. Bind complete. No settings changes possible via this
   method.

### Method 3 — JR/xLite Module with OpenTX

For the Ghost JR or xLite module on third-party transmitters
(Taranis, Jumper, etc.):

1. In your transmitter's model settings, set **External RF**
   module to **GHST** protocol.
2. On the Ghost module OLED, navigate to the bind menu.
3. Put the receiver in bind mode (same button procedure as
   above).
4. Select **Bind** on the module's OLED interface.
5. Confirm successful bind (both go solid green).

**Critical OpenTX setting:** The ADC Filter function (global
by default) **must be set to OFF** for Ghost. If left on, you
will get jittery or unresponsive channel outputs.

For EdgeTX users: set the radio into **ONEBIT** mode for
proper GHST communication.

---

## Firmware Updates

### Transmitter Module (JR / xLite)

1. Download the Ghost Updater/Installer from ImmersionRC's
   website (under Firmware/Downloads → Utility Software).
2. **Windows:** Install the ImmersionRC USB drivers + Zadig
   if needed. **Mac:** No drivers required.
3. Connect the module to your computer via USB.
4. Open Ghost Updater — it should auto-detect the module on
   the correct COM port.
5. Click **Update Ghost**. The program auto-selects the
   latest firmware if connected to internet.
6. Wait 1–2 minutes for completion + success message.
7. After updating the Tx module, rebind to all receivers —
   they will automatically receive firmware updates during
   the bind process.

### Orqa FPV.Ctrl Transmitter

The FPV.Ctrl transmitter and UberLite module have **separate
firmware**. The transmitter firmware updates through the
FPV.Ctrl mobile app. The UberLite module firmware requires
the Ghost Updater desktop application (same as JR/xLite
modules above).

### Receiver Firmware

Receivers (Átto, Átto Duo, Zepto) auto-update when binding
to a transmitter that has been updated to the latest firmware.
No separate receiver update process needed.

---

## Flight Controller Integration

### Protocol Selection

GHST is the recommended protocol for all Ghost setups. It
provides lower latency, more channel resolution, and native
telemetry compared to SBus fallback.

| Protocol | Channels | Resolution | Latency | Notes |
|----------|----------|------------|---------|-------|
| GHST | 16 | High | Lowest | Recommended. Native Ghost protocol. |
| SBus | 16 | Standard | Higher | Legacy fallback. Available on OpenTX 2.3.9 and below. |
| Fast SBus | 16 | Standard | Lower | 200 kbaud variant |
| SRXL-2 | 16 | High | Low | 400 kbaud. Alternative to GHST for some FCs. |
| PWM | 1 per wire | Analog | Variable | Only for legacy hardware |

### ModalAI VOXL 2

1. Connect Ghost Átto to the correct UART port (see VOXL 2
   pinout documentation).
2. SSH into the VOXL 2.
3. Edit `/etc/modalai/voxl-px4.conf`.
4. Set `RC_INPUT` to `GHST`.
5. Restart PX4.

**Pin connections (Átto to VOXL 2):**

| Átto Pin | VOXL 2 Pin | Signal |
|----------|------------|--------|
| + (5V) | 5VDC | Power |
| G (GND) | GND | Ground |
| S (Serial Out) | UART Rx | RC data |
| T (Tramp Telemetry) | UART Tx | Optional — VTX control |

ModalAI notes that having Tramp Telemetry connected to Tx
does not cause issues, and enables swapping between Ghost
and ELRS receivers without re-wiring (using the Harwin
rectangular connector on MCBL-89-01).

### ModalAI VOXL Flight / Flight Core

Use cable MSA-D0001-1-02, connected to J1003 and J1004:

| Connector | Pin | Signal |
|-----------|-----|--------|
| J1003 Pin 1 | 5VDC | Power to Átto (+) |
| J1003 Pin 3 | GND | Ground to Átto (G) |
| J1004 Pin 2 | USART6_TX | Serial from Átto (S) |

Set `RC_INPUT_PROTO` to `GHST` in QGroundControl.

### Betaflight

In Betaflight Configurator 10.9+:

1. Go to **Ports** tab. Enable Serial Rx on the UART
   connected to the Ghost receiver.
2. Go to **Configuration** tab. Under Receiver, set
   **Serial Receiver Provider** to `GHST`.
3. Save and reboot.

### ArduPilot / PX4

For ArduPilot on the Orqa F405 3030 FC:

1. Set `SERIAL*_PROTOCOL = 23` (RC Input) on the UART
   connected to the Ghost receiver.
2. Set `RC_PROTOCOLS` to include GHST.
3. For PX4: set `RC_INPUT_PROTO` to GHST.

---

## RF Mode Selection Guide

| Scenario | Recommended Mode | Why |
|----------|------------------|-----|
| FPV racing | Pure Race (250 Hz) | Minimum latency, no telemetry overhead |
| Race with battery monitoring | Race (166 Hz) | Low latency + bidirectional telemetry |
| Freestyle / general flying | Normal (~50 Hz) | Good range + full telemetry |
| Long-range missions | Long Range (~15 Hz) | Maximum range, LoRa modulation |
| Sub-250g builds with Hybrid | 500 Hz | Hardware-synchronized, Hybrid boards only |

**Field tip:** ModalAI found that Normal mode can introduce
perceptible lag compared to Race mode. For tactical or
time-critical operations, use Race mode as the default and
only drop to Normal/Long Range when range demands it.

---

## Receiver LED States

| LED Color | State | Meaning |
|-----------|-------|---------|
| Blue | Steady | Bind mode — searching for transmitter |
| Green | Steady | Bound and connected |
| Red + Yellow | Alternating flash | Hardware fault — check solder pads between 5V and GND (ferrite filter removal) |
| Off | — | No power |

---

## Antenna Considerations

Ghost operates on 2.4 GHz. Antenna size is compact — the
supplied dipoles are 2.1 dBi. Key considerations:

**Transmitter side:** The JR module runs Tx-side antenna
diversity by default (two antennas). Single-antenna mode is
one menu option away. For maximum range, a directional antenna
on the transmitter can double expected range — 2.4 GHz
directional antennas are physically small enough to be
practical.

**Receiver side:** The Átto has a single U.FL antenna. The
Átto Duo has two U.FL antennas providing true diversity (two
independent receiver channels, not just two antennas on one
channel). For race builds where diversity matters, the Duo
is recommended.

**Coexistence:** Ghost's LoRa/FHSS modulation handles 2.4 GHz
congestion well, but the standard deconfliction rules apply —
if your mesh radio AND Ghost AND companion computer WiFi are
all on 2.4 GHz, expect desensitization. See the Handbook's
frequency bands chapter for the full 2.4 GHz deconfliction
discussion.

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| No bind | Rx not in bind mode | Press button within 30s of Rx power-on |
| Bind succeeds but no RC in FC | Wrong protocol selected | Set GHST in FC config (not SBus) |
| Jittery channels on OpenTX | ADC Filter enabled | Disable ADC Filter globally |
| Red/Yellow alternating flash on Rx | Ferrite filter pads damaged | Inspect/repair solder pads between 5V and GND pins |
| Rx doesn't update on bind | Tx module not updated | Update Tx module via Ghost Updater first, then rebind |
| Lag in Normal mode | Normal uses ~50 Hz | Switch to Race mode for time-critical ops |

---

## External Resources

- ImmersionRC Ghost Manual (comprehensive):
  https://www.immersionrc.com/?download=6746
- ModalAI Ghost integration docs:
  https://docs.modalai.com/orqa-ghost/
- ArduPilot OrqaF405 board docs:
  https://ardupilot.org/copter/docs/common-OrqaF405.html
- Orqa support portal:
  https://orqafpv.freshdesk.com/support/home
- Ghost Updater download:
  https://www.immersionrc.com/fpv-products/ghost/#specifications
  (under Firmware/Downloads → Utility Software)

---

*Last updated: March 2026*
