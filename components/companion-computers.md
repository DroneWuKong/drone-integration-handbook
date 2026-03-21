# Companion Computers — When the FC Isn't Enough

> **Part 6 — Components**
> When you need AI, computer vision, SLAM, or ROS on a drone,
> you add a companion computer. This is the compute layer
> between the flight controller and intelligence.

---

## When You Need One

A flight controller runs the stabilization loop — PID control,
motor mixing, sensor fusion for attitude. It doesn't run neural
networks, process camera feeds, execute ROS nodes, or make
autonomous decisions beyond basic waypoint navigation.

When your mission requires object detection, visual-inertial
odometry, SLAM, AI-driven analysis, swarm coordination, or
onboard data processing, you need a companion computer.

The companion computer talks to the FC over MAVLink (UART or
Ethernet) and handles everything the FC can't.

---

## ModalAI — The Blue UAS Standard

ModalAI holds 16 Blue UAS Framework listings — more than any
other single manufacturer. Their VOXL 2 platform is the reference
companion computer for PX4-based autonomous drones.

### VOXL 2

| Detail | Value |
|--------|-------|
| HQ | San Diego, CA, USA |
| Blue UAS | 16 Framework components |
| NDAA | FY20 §848 compliant, assembled in USA |
| Processor | Qualcomm QRB5165 (8-core, 2.84 GHz) |
| AI | 15+ TOPS (GPU + DSP combined) |
| Camera Inputs | 7× MIPI CSI-2 (supports FLIR Lepton/Boson) |
| Weight | 16g (module only) |
| Software | PX4 (native), VOXL SDK, ROS, OpenCV, TensorFlow Lite |
| GPS-Denied | VIO, VOA, SLAM built-in |
| Connectivity | 5G option |
| Price | ~$1,199 |

VOXL 2 runs PX4 natively — it IS the flight controller AND the
companion computer in one module. This eliminates the FC-to-
companion serial bottleneck entirely.

### VOXL 2 Mini

Same QRB5165 processor in a smaller form factor: 11g, 42mm×42mm
(30.5mm standard mounting holes). 4× MIPI camera inputs. Designed
for sub-250g drone builds.

### Starling 2 / Starling 2 Max

Pre-integrated VOXL 2 development drones:
- **Starling 2:** 280g, 40 min indoor SLAM flight
- **Starling 2 Max:** 500g, 55 min outdoor, 500g payload capacity

### ModalAI Sentinel

Defense-oriented configuration with enhanced security features.

---

## NVIDIA Jetson Ecosystem

NVIDIA Jetson is the dominant GPU compute platform for onboard AI.
The Jetson module provides the raw compute; a carrier board provides
the I/O, power regulation, and physical interface to the drone.

### Jetson Modules

| Module | AI Performance | Power | Memory | Price | Status |
|--------|---------------|-------|--------|-------|--------|
| Orin Nano 8GB | 67 TOPS | 7–25W | 8 GB | ~$249 (dev kit) | Entry-level UAS AI |
| Orin NX 16GB | 157 TOPS (JetPack 6.2 Super MAXN) | 10–40W | 16 GB | ~$699 | Primary UAS companion compute |
| AGX Thor | 2,070 FP4 TFLOPS | Higher | 128 GB | Defense tier | Heavy UAS / ground station |

The Orin NX 16GB at 157 TOPS is the sweet spot for most drone
AI applications — enough to run real-time object detection,
tracking, and VIO simultaneously.

### NDAA-Compliant Jetson Carriers (Critical Layer)

The Jetson module is NVIDIA-manufactured (Taiwan/USA). The carrier
board determines NDAA compliance. Chinese-made carriers are NOT
compliant.

#### ARK Electronics Carriers

| Product | Key Feature |
|---------|-------------|
| **ARK Just a Jetson** | NDAA, made in USA. 75V direct battery input (!), built-in IMU, open-source. WiFi 6E/BT 5.3 M.2 option with Remote ID. NDAA bundles with USA-made Jetson + Swissbit SSD. |
| **ARK Jetson PAB Carrier** | Orin NX/Nano + any PAB flight controller (inc. ARKV6X). 90W redundant power across 3 inputs. JetPack 6.2 w/ Super MAXN = 157 TOPS. Can run LLMs on-device. |
| **ARK VOXL2 RTK PAB Carrier** | ModalAI VOXL2 + built-in RTK GNSS. Best of both worlds. Blue UAS Framework listed. |

ARK's 75V direct battery input on the Just a Jetson is a
significant design choice — it means you can power the companion
computer directly from a 6S–18S flight battery without a separate
BEC or voltage regulator. One less failure point.

#### Other Carriers

| Product | HQ | Key Feature |
|---------|-----|-------------|
| Neousys FLYC-300 | Taiwan | Orin NX, 100 TOPS, 2× GigE, CAN, 4S-14S via XT30, -25°C to 70°C |
| Forecr DSBOARD-ORNXS | Turkey | Compact Orin NX/Nano, 2× GigE, CAN, 9-28V, -25°C to 85°C |

---

## Auterion Skynode

Skynode deserves mention here as a converged FC + companion
computer running AuterionOS (Linux). See the Flight Controllers
chapter for full specs. 50,000+ deployed. Runs PX4 with
containerized applications, ROS 2, and Auterion SDK.

---

## CubePilot Herelink

Not a traditional companion computer but an integrated GCS +
video + control system. The Herelink ground unit + air unit
provides HD video streaming, RC control, and a touchscreen
interface in one package. Widely used in ArduPilot commercial
builds. Australian-made (verify specific component origins).

---

## Raspberry Pi (Context)

Raspberry Pi 5 and CM4 are widely used as companion computers
in open-source UAS builds. Low cost (~$80), large community,
extensive software support. NOT NDAA compliant (UK design,
various manufacturing origins). The ARK Pi6X integrates a
CM4 with an ARKV6X flight controller on a single NDAA-compliant
board — the cleanest path to using Pi compute in a compliant build.

---

## Orqa DTK APB

The DTK APB takes the converged approach to an extreme: an
STM32H743 flight controller and an NXP i.MX8M Plus Linux SBC
on a single 65×40 mm board at 50 grams. The FC side runs PX4,
ArduPilot, iNav, or Betaflight. The SOC side runs Orqa's Yocto
Linux with a 2.25 TOPS NPU, dual 4-lane MIPI-CSI camera inputs
(one supporting analog CVBS via ADV7282), an H.265 hardware
encoder at 1080p60, hardware OSD (MAX7456 emulation), CAN bus,
and a PCIe expansion slot. FC-to-SOC communication runs over
internal UART and CAN — no external wiring.

| Detail | Value |
|--------|-------|
| HQ | Osijek, Croatia |
| SOC | NXP i.MX8M Plus (4x Cortex-A53, Cortex-M7) |
| FC MCU | STM32H743 |
| NPU | 2.25 TOPS |
| RAM / Storage | 4 GB LPDDR4 / 4 GB eMMC + micro-SD |
| Camera Inputs | 2x 4-lane MIPI-CSI 2 |
| Video Encoder | H.265 / H.264, 1080p @ 60fps |
| Sensors | ICM42605 IMU, DPS310 barometer |
| Power | 2S–8S battery or USB-C PD (60 W max) |
| Weight | 50 g |
| NDAA | Compliant — EU manufactured |

The APB's sweet spot is FPV builds that need onboard AI, computer
vision, or video processing without the wiring overhead of a
separate companion board. The 2.25 TOPS NPU handles lightweight
inference (object classification, pixel tracking) while the
hardware encoder can stream processed video back through the
analog OSD path to existing FPV goggles. Where VOXL 2 targets
the autonomous PX4 market and Jetson targets heavy ML workloads,
the APB targets the FPV-first operator who needs compute without
leaving the analog video ecosystem.

---

## The Architecture Decision

| Approach | Example | Pros | Cons |
|----------|---------|------|------|
| Separate FC + companion | ARKV6X + Jetson Orin NX | Maximum flexibility, hot-swap compute | Wiring complexity, serial bottleneck |
| Converged FC + compute | ModalAI VOXL 2, Auterion Skynode, Orqa DTK APB | Single board, no bottleneck, lighter | Less flexible, vendor lock-in |
| FC + carrier board | ARKV6X + ARK Jetson PAB Carrier | Best of both — PAB standard allows swapping either | Most complex physically |

For the AI Wingman architecture, VOXL 2 is the primary PX4
integration target (converged approach). The Orqa DTK APB
(STM32H7 FC + i.MX8M Plus companion) is the converged
development hardware — same single-board philosophy as VOXL 2
but with FPV-native features (analog video I/O, hardware OSD,
multi-firmware FC support).

---

## Choosing a Companion Computer

1. **Start with your AI workload.** Object detection at 30fps needs
   ~10+ TOPS. VIO + detection + tracking simultaneously needs 40+.
   LLM inference on-device needs 100+.

2. **Power budget matters more than specs.** A Jetson Orin NX at
   25W on a 5" FPV quad is a 15-20% hit to flight time. Plan
   accordingly.

3. **NDAA compliance is in the carrier, not the module.** The Jetson
   module itself is fine. The carrier board you mount it on
   determines compliance. Use ARK carriers for NDAA builds.

4. **Camera interface determines capability.** MIPI CSI-2 is the
   standard. Count how many camera inputs you need (stereo VIO =
   2, plus thermal = 3, plus downward flow = 4) and match to the
   platform's MIPI port count.

5. **For NDAA builds:** ModalAI VOXL 2 (Blue UAS, converged) or
   ARK Just a Jetson / Jetson PAB Carrier (NDAA, modular).

6. **For FPV builds that need compute:** Orqa DTK APB. It's the
   only converged FC + companion that keeps you in the analog
   video ecosystem — hardware OSD, CVBS camera input, and an
   encoder that can process video on-board without replacing
   your existing FPV stack. 2.25 TOPS NPU won't run heavy
   detection models, but it handles classification, tracking,
   and sensor fusion at the edge.

7. **For long-range telemetry and fleet management without onboard AI:**
   DroneEngage on RPI Zero W. 42g complete, cellular, swarm-capable,
   air-gap deployable. If the requirement is BVLOS telemetry and
   multi-drone coordination rather than onboard inference, this is
   the right answer.

---

## DroneEngage — Cellular Companion Software

DroneEngage is not a hardware platform — it's companion computer *software* that turns a Raspberry Pi into a cloud-connected ground link. Developed under the ArduPilot umbrella, it runs alongside any ArduPilot or PX4 flight controller and provides cellular telemetry, video streaming, and swarm management over 4G/LTE/5G.

It answers the question of what software to run on a generic Raspberry Pi when the primary requirement is long-range telemetry and fleet management rather than onboard AI.

### Architecture

A Raspberry Pi connects to the FC over UART or USB, connects to the internet via a USB LTE modem, and runs the DroneEngage agent. From that point the drone is reachable from any browser. The web client handles MAVLink telemetry, gamepad RC, video feeds, geofencing, and swarm coordination. DroneEngage also forwards MAVLink transparently over UDP to Mission Planner or QGroundControl — no change to existing GCS workflows.

### Weight

| Config | Total weight | Capability |
|--------|-------------|------------|
| RPI Zero W + LTE modem | **42g** | Full telemetry, cloud GCS, geofencing, swarm |
| RPI Zero 2 W + modem + camera | **52g** | Above + live video stream |
| RPI 4 + modem | ~90g | Multi-camera, heavier compute |

42 grams for unlimited-range telemetry, independent geofencing, RC blocking, and swarm coordination is competitive with dedicated telemetry radios — and those don't include cloud GCS or swarm management.

### Key Features

**Air-gap server**: fully self-hosted backend. All drone↔GCS traffic routes through a local Raspberry Pi 4 at the GCS site rather than ArduPilot's cloud. Identical protocol and security model. Viable for contested environments, classified programs, and field sites without reliable internet.

**RC Blocking / TX Freeze**: local field pilot hardware override; TX Freeze holds current throttle for long-range cruise without active stick input.

**Swarm operations**: hierarchical formation management, synchronized missions, single-interface multi-drone control. Developer guide documents the swarm logic — maps directly to CBBA task allocation with a broadcast command layer on top.

**GPS injection**: companion can inject GNSS corrections into the FC — relevant for Hangar's preflight RTK workflow.

### Andruav (Android Predecessor)

Andruav is the original version: an Android phone as companion computer, connected to the FC over USB serial. Phone provides GPS, FPV camera, 4G telemetry, and SMS fallback control. Still maintained; new development is on DroneEngage. Useful for rapid prototyping where Pi + LTE modem overhead isn't justified.

---

*Last updated: March 2026*
