# OpenHD Implementation Guide

OpenHD is an open-source digital HD video link built on wifibroadcast — commodity WiFi adapters repurposed as a broadcast video transmitter. Video is one-way broadcast (no association, no ACK — degrades gracefully like analog). Telemetry, settings, and RC control are bidirectional. The link supports encryption with verification. This guide takes you from an empty bench to a working long-range video link with MAVLink telemetry passthrough.

**Difficulty:** Moderate — requires Linux comfort, soldering, and MAVLink configuration  
**Time to first link:** 2–4 hours  
**BOM cost:** $30–80 depending on hardware tier  
**Repository:** [github.com/OpenHD/OpenHD](https://github.com/OpenHD/OpenHD) (GPL-3.0, 2.3k stars)  
**Docs:** [openhdfpv.org](https://openhdfpv.org)

---

## What You're Building

Two nodes — Air and Ground — each running the OpenHD software stack on a Linux SBC or x86 computer. Both nodes have a WiFi adapter running in monitor/injection mode. The air node captures video from a CSI camera, encodes it, wraps it in wifibroadcast frames, and injects it into the air. The ground node captures all frames promiscuously, decodes the video, and displays it in the QOpenHD app — which also shows MAVLink telemetry forwarded from your flight controller.

```
[FC] ──UART── [Air SBC] ──wifibroadcast──▶ [Ground SBC/PC] ──UDP── [QOpenHD / Mission Planner]
                │                                                     │
             [CSI Cam]                                           [Live Video]
```

No network router. No association. No ACK. Video is one-way broadcast with FEC. Telemetry and settings are bidirectional. OpenHD also supports dual cameras with picture-in-picture, low-latency RC control via USB joystick, and link encryption.

---

## Hardware BOM

### Tier 1 — Minimum (RPi Zero 2 + laptop)

| Item | Notes | ~Cost |
|------|-------|-------|
| Raspberry Pi Zero 2 W | Air unit. **Not** Zero 1 — not supported | $15 |
| 2× ASUS USB-AC56 or ALFA AWUS036ACH | One for air, one for ground (RTL8812AU, 500mW). For best performance: BLM8812EU (800mW+, no FCC/CE cert). | $20–30 each |
| Arducam or RPi HQ Camera | CSI, supported by OpenHD drivers | $25–50 |
| 22-pin type B CSI cable | Pi Zero uses this, not standard 15-pin | $3 |
| 5V/3A BEC for WiFi adapter | Dedicated power — mandatory | $5 |
| 5V/3A BEC for RPi | Separate rail from the WiFi adapter | $5 |
| Laptop (x86) | Ground station — modern CPU, SecureBoot off | — |
| USB stick (fast) | Ground station image boot (if not native) | $10 |

**Total air unit: ~$80**  
**Total ground (excluding laptop): ~$30**

### Tier 2 — Recommended (CM4 + Rock5)

| Item | Notes | ~Cost |
|------|-------|-------|
| Raspberry Pi CM4 (4GB, eMMC) | Better thermal, dual camera, lower latency | $60 |
| Ochin CM4 carrier board | Designed for OpenHD, compact form factor | $35 |
| Radxa Rock 5B | Ground station — H.265 hardware decode, lowest latency | $80 |
| 2× ALFA AWUS036ACH | One for air, one for ground | $30 each |
| Arducam Skymaster or IMX477 | Best IQ for OpenHD | $40–80 |

### Tier 3 — Lowest Latency

OpenHD custom hardware (purpose-built SBC + camera combination). Check the project Discord for current availability. Cuts latency roughly in half vs. RPi builds.

---

## Step 1: Flash Air Image

1. Download the latest OpenHD Evo image from [openhdfpv.org/downloads](https://openhdfpv.org/downloads). Select the image matching your SBC (Pi Zero 2, CM4, Rock5, or x86).
2. Flash to SD card (Pi Zero 2) or eMMC (CM4 via Ochin) using the **OpenHD ImageWriter** (recommended — available at openhdfpv.org/downloads) or Balena Etcher.
   - CM4/Ochin: enter flash mode by holding the button while connecting USB-C power. Flash is slow — do not disconnect.
3. First boot takes several minutes. The SBC reboots multiple times during initial config. This is normal.

---

## Step 2: Flash Ground Image

For x86 (laptop):
1. Flash the x86 OpenHD image to a fast USB stick.
2. Disable SecureBoot in BIOS/UEFI.
3. Set boot priority to USB.
4. Boot from the stick — QOpenHD will start automatically. If not, launch OpenHD and QOpenHD from the desktop shortcuts.

For Rock5 ground station:
1. Flash the Rock5 image to SD or eMMC per the Radxa standard process.
2. OpenHD starts automatically on boot.

---

## Step 3: Wire the Air Unit

**Power — critical:**  
The WiFi adapter draws more current than most SBCs can supply via USB. You need a dedicated BEC wired directly to the WiFi adapter, bypassing the SBC's USB port. Most builds solder the WiFi adapter directly to the SBC's USB power and data pads — remove the USB connector entirely to eliminate vibration disconnects. Two separate BECs: one for the SBC, one for the WiFi adapter.

**Camera:**  
Connect the CSI camera to the SBC using the correct cable (22-pin type B for Pi Zero 2, standard 15-pin for CM4/Ochin). Mount the camera with a solid connection — no flex cable vibration.

**Flight Controller:**  
Connect the FC's MAVLink UART to the SBC's UART. The SBC serial port and FC baud rate must match. Default is 115200; configure the same value in OpenHD's AIR → FC_UART_BAUD and in your FC's telemetry port settings.

```
FC UART TX ──► SBC RX
FC UART RX ◄── SBC TX
FC GND ──────── SBC GND   ← common ground required
```

---

## Step 4: WiFi Adapter — Air Side

The adapter should appear automatically if using a supported chipset. If you have connection but no video, check:
1. Camera is recognized — in QOpenHD go to AIR CAM 1 → CAMERA_TYPE and select the correct overlay.
2. The SBC reboots after camera type change — this is normal.

Solder the adapter to the SBC USB pads rather than using a plug. Mark the cable with a zip tie so you can identify which antenna connector is which later.

---

## Step 5: Configure the Link

Open QOpenHD on the ground station. The OpenHD logo opens the main menu; the red circle opens the sidebar.

**Frequency:**  
Go to OPENHD → LINK/QUICK. Set frequency to 5.8GHz (recommended — cleaner than 2.4GHz and compatible with 2.4GHz RC transmitters). You can use ANALYZE to see which channels are cleanest in your environment.

Do not change frequency while armed — it will interrupt the link.

**STBC/LDPC:**  
Enable both on air and ground if your adapters support it (RTL8812AU and 8814AU do; RTL8811AU does not — single antenna). These use both antennas for receive diversity and significantly improve range. Both must be enabled or disabled on both ends — mismatched settings break the link.

**TX Power:**  
Set per local regulations. Higher power = longer range. Configure in SOFTWARE SETUP → TX POWER.

**RX Diversity (ground):**  
You can connect multiple WiFi adapters to the ground station for receive diversity — OpenHD picks the best signal per packet. Keep adapters same chipset and same manufacturer. Do not mix RTL8812AU with RTL8812BU or different brands. Not recommended for new users — start with a single adapter.

---

## Step 6: Verify Link

In QOpenHD → STATUS tab, you should see both AIR and GROUND showing as LIVE. If only one shows, check:
- WiFi adapter is powered and seated
- Both nodes are on the same frequency
- STBC/LDPC match between air and ground

**Video troubleshooting:**  
- Black image with "rebooting camera" → wrong CAMERA_TYPE setting. Fix in AIR CAM 1 menu, then wait for reboot.
- Video but no telemetry → UART baud rate mismatch or wiring error. Check FC_UART_BAUD in AIR settings and match it in your FC configurator.

---

## Step 7: MAVLink Forwarding

OpenHD automatically forwards the MAVLink stream from the FC over UDP on the ground station's local network. Default port is 14550. To connect Mission Planner or QGroundControl:

1. Connect your laptop to the same network as the ground station (or use the ground station directly).
2. In Mission Planner: Connection → UDP → port 14550.
3. In QGroundControl: Application Settings → Comm Links → UDP → 14550.

Both QOpenHD and your GCS can receive the MAVLink stream simultaneously — OpenHD broadcasts it to all connected clients.

For Buddy/Wingman: Buddy can connect as a second MAVLink UDP client on port 14550 alongside QOpenHD. No configuration change needed on the OpenHD side.

---

## Step 8: Key Settings Reference

| Setting | Location | Notes |
|---------|----------|-------|
| Frequency | LINK/QUICK | 5.8GHz recommended. Cannot change while armed. |
| Channel width | Sidebar → LINK | 20/40MHz. Wider = more throughput, less range. |
| STBC/LDPC | LINK/QUICK | Enable both if adapter supports. Must match air/ground. |
| TX power | SOFTWARE SETUP → TX POWER | Obey local regs |
| Camera type | AIR CAM 1 → CAMERA_TYPE | Must match physical camera. Reboot required. |
| Video resolution | Sidebar → VIDEO | Also sets air recording resolution |
| Camera exposure | Sidebar → CAMERA | Adjustable in flight, no reboot needed |
| Air recording | Sidebar → AIR RECORDING | OFF / ON / AUTO (arms trigger). Air-side storage only |
| FC baud rate | AIR → FC_UART_BAUD | Must match FC telemetry port config |

---

## Frequency Selection Guide

| Band | Pros | Cons | Use when |
|------|------|------|----------|
| 5.8GHz | Clean spectrum, coexists with 2.4GHz RC | Less obstacle penetration | Most builds — open terrain, line of sight |
| 2.4GHz | Better penetration, slightly more range through obstacles | Heavy interference in populated areas, conflicts with 2.4GHz RC | Remote/rural ops where 5.8GHz is congested |
| 6GHz | Coming soon in OpenHD Evo — even cleaner spectrum | Newer hardware required | Future builds |

---

## Integration Patterns

**OpenHD + GHST/ELRS (dual-link):**  
Run OpenHD for video and MAVLink telemetry (long range, high latency acceptable). Run GHST or ELRS as the primary RC control link (low latency, high reliability, shorter range). The FC connects to both simultaneously — telemetry over OpenHD UART, RC input from the RC receiver. This is the recommended pattern for FPV/survey builds where video quality matters but you don't want to bet RC control on wifibroadcast.

**OpenHD + Meshtastic (backup comms):**  
OpenHD as primary video + telemetry. Meshtastic LoRa node as backup telemetry mesh for emergency commands when the OpenHD link degrades. See the [Meshtastic section](/components/comms-datalinks#meshtastic--lora-mesh-as-a-telemetry-backbone) for the dual-link architecture pattern.

**OpenHD + Wingman/Buddy:**  
Buddy connects to the OpenHD ground station's MAVLink UDP stream (port 14550) as a second client alongside QOpenHD. No changes to the OpenHD side. Buddy's Kalman telemetry estimator smooths the MAVLink stream normally regardless of source. The video stream can be displayed in Buddy via RTSP if the ground station exposes one.

---

## Gotchas

**Soldering is not optional on the air side.** Any plug-in USB connection to the WiFi adapter will eventually vibrate loose mid-flight. Solder it.

**Dedicated BECs are not optional.** Powering the WiFi adapter from the SBC's USB rail will cause brownouts under TX load. Two separate BECs — one per component.

**STBC/LDPC must match on both ends.** If one end has it enabled and the other doesn't, you get no link, not a degraded link. Easy to forget when flashing a replacement ground unit.

**Camera type must match physical hardware.** OpenHD cannot auto-detect the camera model. Wrong CAMERA_TYPE gives a black screen. Set it in QOpenHD, wait for the reboot, then test.

**Don't change frequency while armed.** The link drops during frequency change. Plan your frequency before takeoff.

**The first CM4/Ochin flash is slow.** This is a known limitation of the CM4 eMMC interface. Do not disconnect during flash — it will brick the device.

---

## Resources

- [openhdfpv.org](https://openhdfpv.org) — official docs (Evo and 2.0 legacy)
- [github.com/OpenHD/OpenHD](https://github.com/OpenHD/OpenHD) — source code, GPL-3.0
- [QOpenHD Android app](https://github.com/OpenHD/QOpenHD/releases) — ground station app
- Telegram: [t.me/OpenHD_User](https://t.me/OpenHD_User) — active community, fastest support
- Discord: [discord.gg/NRRn5ugrxH](https://discord.gg/NRRn5ugrxH)

---

*Last updated: March 2026*
