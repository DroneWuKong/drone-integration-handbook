# Remote ID for Custom Builds

Most Remote ID guides are written for DJI pilots. If you're flying a custom Betaflight quad, an ArduPilot fixed-wing, or anything else that wasn't bought in a box, the compliance picture looks very different. This guide covers the actual rules, how they apply to open-source and custom-built platforms, and how to achieve compliance without buying a new aircraft.

---

## What Remote ID Is

Remote ID is an FAA-mandated broadcast from every drone in flight, transmitting identification and location data via Bluetooth 4 or 5 / Wi-Fi (IEEE 802.11). The broadcast can be received by any smartphone or dedicated receiver within ~300m. The data includes:

- Drone serial number or session ID
- Drone GPS position, altitude, and velocity
- Control station (takeoff point or pilot) GPS position
- Timestamp
- Emergency status flag

The rule has been in effect since September 16, 2023. Non-compliance is a regulatory violation regardless of whether you're flying recreationally or commercially.

---

## The Weight Cutoff That Matters

Remote ID applies to all drones in the 0.55 lb (250g) to 55 lb (25kg) category operating in US airspace.

**Under 250g:** No Remote ID required. This is why the DJI Mini 3 exists at 249g. Most competitive FPV builds on 3" frames or smaller (without a camera) can hit this threshold, but a 5" freestyle quad with a GoPro and LiPo is almost certainly over 250g.

**Weigh your build.** Not the frame weight. Not the advertised weight. Weigh the complete flying system on a postal scale including the battery you typically fly. If it's 251g you need Remote ID.

---

## Three Compliance Paths

### Path 1: Standard Remote ID (Built-In)

The drone has Remote ID capability integrated into its firmware, broadcast from an onboard module. This is what DJI, Autel, Skydio, and most commercial UAS manufacturers provide. The FC or companion processor handles the broadcast — no external hardware needed.

**For custom builds:** This requires Remote ID support in your flight controller firmware. As of 2025:
- **ArduPilot** (4.3+): Native Remote ID support via MAVLink RemoteID messages. Supported with external broadcast module (see Path 2 setup) or via companion computer.
- **Betaflight** (4.4+): Native Remote ID support. Requires an external serial broadcast module, configured as a SERIAL port peripheral.
- **iNav** (6.0+): Remote ID support added. External module required.

### Path 2: Broadcast Module (Add-On)

A small external module handles the Remote ID broadcast independently. The module receives GPS data (either from the FC via serial or from its own GPS), and handles the Bluetooth/Wi-Fi broadcast. This is the standard compliance path for custom builds.

The module connects to a spare UART on the FC and receives position data via MAVLink or a dedicated Remote ID protocol.

**Widely-used modules:**
- **BlueMark db202** — most popular for Betaflight; compact, UART connection, both BT and WiFi
- **uAvionix Ping (sRID)** — well-regarded, slightly larger, MAVLink native
- **Spectral Devices** modules — open-source firmware option

**Module wiring:**
```
FC UART TX → Module RX
FC UART RX → Module TX (for bidirectional GPS sync)
FC 5V → Module power
FC GND → Module GND
```

Configure the FC UART port as "Remote ID" in Betaflight Configurator (Ports tab), or set `SERIAL_PASSTHROUGH` / `FRSKY_TELEMETRY_SERIAL_PORT` + Remote ID function in ArduPilot.

**GPS requirement:** The module needs a GPS fix to broadcast valid position data. If your build has no GPS, the module cannot transmit compliant position data. You have two options: add a dedicated GPS module, or operate only at a FRIA (see below).

### Path 3: FRIA (FAA-Recognized Identification Area)

A FRIA is an FAA-approved location where drones without Remote ID can fly. FRIAs are designated at fixed locations — almost exclusively model aircraft club fields and a small number of educational institutions.

**Key FRIA constraints:**
- You must remain within the FRIA boundary at all times
- You must maintain VLOS (visual line of sight)
- The drone operator (pilot) must be physically present at the FRIA
- You cannot use a FRIA as a compliance shortcut for commercial operations — they're for recreational flying at designated fields

For most commercial work and any off-site flying, FRIAs are not a practical compliance path.

---

## Custom Build Specifics

### Open-Source FC Without Built-In Serial Number

The FAA Remote ID rule requires a serial number in ANSI/CTA-2063-A format: a manufacturer code + serial string. DJI and commercial manufacturers provide this at the factory. Custom builds do not have one assigned by default.

**The path for custom builds:** Register your drone on the FAA DroneZone website. The FAA assigns a registration number (FAxxxxxx format). This registration number becomes the broadcast identifier for your build — the serial number field in the Remote ID broadcast uses your FAA registration number.

Every broadcast module configures this via either:
- A companion app (BlueMark uses a Bluetooth-paired phone to configure)
- A USB CLI (uAvionix uses a web-based configurator)
- Betaflight Configurator CLI: `set drone_serial = FA12345678`

### Multiple Aircraft on One Registration

The FAA allows one registration for multiple aircraft of the same make/model. For a fleet of identical custom builds, you can register them as a "class" rather than individually, reducing administrative overhead. Each aircraft needs its own broadcast module, but they can share a registration — differentiate by using a session ID that includes the frame number.

### What to Do if Your Drone Has No GPS

Without GPS, the broadcast module can't transmit position — the module sends an empty position field, which is technically non-compliant for Standard Remote ID. Options:

1. Add a minimal GPS module (a BN-180 or similar UART GPS is ~3g, ~$8)
2. Add a module with its own integrated GPS (several broadcast modules now include GPS onboard)
3. Only fly at a FRIA where Remote ID isn't required
4. Only fly drones under 250g AUW

### ELRS and Remote ID: The Frequency Question

ExpressLRS operates at 2.4GHz. The Remote ID broadcast uses Bluetooth 5 (2.402–2.480 GHz) and Wi-Fi (2.4GHz or 5.8GHz). These frequency bands overlap.

In practice, the ELRS radio and the Remote ID broadcast coexist without issues — ELRS uses frequency hopping with very short packet times, while Bluetooth/Wi-Fi handle congestion through their own protocols. Hundreds of thousands of users run ELRS + Remote ID modules without conflict.

**One thing to watch:** If you're running a Remote ID module that uses 5.8GHz Wi-Fi and you have a 5.8GHz FPV VTX, run the VTX and Remote ID module on different 5.8GHz channels. The Remote ID uses a specific channel for discovery broadcasting; it won't interfere with FPV video but they shouldn't share the same channel.

---

## What the Broadcast Contains — and What It Doesn't

The Remote ID broadcast is **not** a government tracking system. It's a local Bluetooth/Wi-Fi broadcast receivable only within radio range (~300m in practice). It does not upload to a database, does not contact the FAA, and is not stored anywhere. The pilot's personal information (name, address) is not in the broadcast — it's linked only via the registration number, and that link is accessible only to law enforcement with appropriate authorization.

The broadcast contains:
- Your drone's registered identifier
- Your drone's GPS position and altitude
- The control station location (your takeoff point if not actively updated)
- Speed and heading
- Timestamp

It does not contain: your name, your address, your flight log, or any persistent data.

---

## Configuring Remote ID in Betaflight

Betaflight 4.4+ has Remote ID support built in. You'll need a serial broadcast module connected to a UART.

**Step 1 — Wire the module:**
Connect the module to a free FC UART (TX/RX/GND/5V).

**Step 2 — Enable in Ports tab:**
Set the UART to "Remote ID" function in Betaflight Configurator → Ports.

**Step 3 — Set the serial number:**
In CLI:
```
set drone_serial = FAXXXXXXXXXXX
save
```
Use your FAA registration number in place of the X characters. Format: no spaces, no dashes, just the alphanumeric string.

**Step 4 — Verify:**
Download a Remote ID receiver app (OpenDroneID Android, or FAA's own viewer). Power up your quad with a GPS fix and verify your drone appears in the app with correct position data.

---

## Configuring Remote ID in ArduPilot

ArduPilot supports Remote ID via the DroneCAN (UAVCAN) protocol or via MAVLink serial passthrough.

**MAVLink serial method:**
1. Connect module to a UART configured as MAVLink2 (SERIAL_PROTOCOL = 2)
2. Set `REMOTE_ID_ENABLE = 1`
3. Set `REMOTE_ID_SERIAL_NUM` to your FAA registration number
4. Reboot and verify with a receiver app

ArduPilot's Remote ID implementation also works with the BlueMark and uAvionix modules in their MAVLink modes.

---

## Enforcement Reality

Remote ID enforcement is light as of 2025 — the FAA's attention has been on commercial operations and repeat offenders near airports and restricted airspace. But the rule is in effect, and local law enforcement increasingly has access to Remote ID receiver apps. The risk calculus is changing.

More practically: Remote ID is a prerequisite for Part 108 BVLOS operations. If you're building toward any kind of expanded operational authority, compliance now is infrastructure for later.

---

## Quick Compliance Checklist for Custom Builds

- [ ] Weigh complete flying system — is it ≥250g?
- [ ] If ≥250g: register on FAA DroneZone, note your registration number
- [ ] Select and install a broadcast module (BlueMark db202 or uAvionix sRID)
- [ ] Wire module to FC UART (TX/RX/GND/5V)
- [ ] Ensure build has GPS (required for valid position broadcast)
- [ ] Configure UART in FC firmware (Betaflight: Ports → Remote ID; ArduPilot: REMOTE_ID_ENABLE)
- [ ] Set registration number in firmware or module configuration
- [ ] Test with a receiver app before first compliant flight
- [ ] Carry FAA registration number documentation when flying
