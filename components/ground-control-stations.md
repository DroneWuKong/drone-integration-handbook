# Ground Control Stations

> **Forge cross-reference:** 13 entries in `ground_control_stations` category  
> **Related handbook chapters:** TAK Integration, Companion Computers, C2 Datalinks  
> **Handbook Roadmap:** Aligns with planned Chapter 22 (Ground Control Stations)

## What a GCS Does

A Ground Control Station is the operator's interface to the drone: mission planning, real-time telemetry display, manual override, and post-flight data review. At minimum, a GCS receives MAVLink telemetry over a radio link and displays position, altitude, battery, and flight mode. At maximum, it manages fleets of autonomous platforms with video feeds, sensor tasking, and integration into C4ISR networks.

## Software GCS Options

### Open Source

- **QGroundControl (QGC)** — Cross-platform (Windows, macOS, Linux, Android, iOS) open-source GCS maintained by the Dronecode Foundation. Supports any MAVLink-compatible vehicle. The default GCS for PX4 and increasingly for ArduPilot. Clean UI, good mobile support, active development. Limitation: single-vehicle focused; multi-vehicle support is basic.
- **Mission Planner** — Desktop GCS (primarily Windows, experimental Linux/macOS) maintained by Michael Oborne for the ArduPilot project. More features than QGC but a steeper learning curve and dated UI. Advanced features include terrain following planning, auto-survey grid generation, log analysis, and firmware flashing. The power-user choice for ArduPilot.
- **MAVProxy** — Command-line MAVLink proxy and GCS. No GUI — pure text interface with optional map module. Used for scripting, automation, and headless ground stations. Pairs well with DroneKit-Python for programmatic flight control.

### Commercial / Enterprise

- **UgCS (SPH Engineering)** — Enterprise-grade mission planning GCS supporting APM, Pixhawk, DJI, Mikrokopter, and more. Key features: simultaneous control of multiple heterogeneous vehicles, 3D interface, KML/KMZ import, photogrammetry planning, and terrain-aware route generation. The professional survey and mapping tool.
- **Auterion Mission Control** — Cloud-connected GCS from the company behind the Auterion Enterprise PX4 distribution. Designed for fleet management with over-the-air updates, flight logging, and maintenance tracking built in. Tight integration with Auterion Skynode hardware.
- **VOTIX DroneOS** — Software platform for multi-drone fleet management with emphasis on automated operations and regulatory compliance.
- **UAV Nav VECTOR** — GCS platform focused on fixed-wing and VTOL autopilot integration.

### Military / Tactical

- **GA-ASI Advanced Cockpit** — General Atomics' GCS for MQ-9 and similar large UAS. Included for reference — this represents the opposite end of the GCS spectrum from QGroundControl.
- **Veronte** — Embention's autopilot and GCS system used in several European military drone programs. Integrated autopilot + GCS ecosystem.
- **Kutta KGS** — GCS integration middleware that bridges drone C2 to military networks (TAK, ATAK, JBC-P). Not a standalone GCS but a critical integration layer for defense programs.

## Hardware GCS Options

Software needs hardware to run on. For field operations, this means ruggedized devices or purpose-built controllers.

### Purpose-Built Controllers

- **Inspired Flight GS-ONE** — NDAA-compliant handheld GCS with 7-inch 2000-nit sunlight-readable touchscreen. Qualcomm QCS6490 processor running Android. Purpose-built for Blue UAS programs. Integrated radio module, physical control sticks, and pre-loaded GCS software. This is what "professional drone GCS hardware" looks like when designed from scratch rather than adapted from a tablet.
- **CubePilot Herelink** — Integrated controller with touchscreen, joysticks, and built-in 2.4 GHz radio. Runs Android with QGC pre-installed. Popular for commercial applications but not NDAA-compliant (Chinese manufacturing). Listed in `c2_datalinks` as well since it combines C2 radio and GCS in one unit.
- **MotioNew M10** — Portable all-in-one handheld GCS integrating computer, radio, joysticks, and datalink in a single device. 10.1-inch display. Designed for field operations where carrying separate tablet + radio + controller is impractical.

### Rugged Tablets

- **Winmate Rugged Tablet** — MIL-STD-810G rugged tablet running Windows or Android. Not drone-specific but commonly used as GCS hardware in defense programs. Run QGC or Mission Planner on it and pair with an external radio.

### Companion Computer as GCS

- **ARK Electronics "Just a Jetson"** — NDAA-compliant Jetson Orin carrier board that can function as both an onboard companion computer and a ground-side GCS depending on configuration. Running ROS 2 on the ground side enables custom GCS interfaces with direct access to the autonomy stack.

## Selection Criteria

| Factor | Hobby / Research | Commercial BVLOS | Defense / Blue UAS |
|--------|-----------------|------------------|--------------------|
| Software | QGC or Mission Planner | QGC, UgCS, or Auterion MC | Mission-specific, often custom |
| Hardware | Laptop or tablet | Rugged tablet + external radio | GS-ONE or equivalent NDAA hardware |
| NDAA required | No | Sometimes | Always |
| Multi-vehicle | Rarely | Growing need | Mandatory for swarm ops |
| TAK integration | No | Rarely | Frequently |
| Video display | Optional | Required | Required with encryption |

## Integration with TAK/ATAK

For defense applications, the GCS increasingly needs to feed drone telemetry into the Tactical Assault Kit (TAK) ecosystem. This means the GCS must output Cursor on Target (CoT) messages over a network connection. See the TAK Integration chapter for the CoT message format and integration patterns.

QGroundControl does not natively output CoT, but middleware solutions (Kutta KGS, custom scripts using PyTAK) can bridge MAVLink telemetry to CoT. Some Blue UAS manufacturers include TAK integration in their GCS software.

## Field Considerations

- **Sunlight readability** — Standard laptop screens are unreadable in direct sunlight. Budget for a 1000+ nit display or purpose-built hardware like the GS-ONE (2000 nit).
- **Gloved operation** — Touchscreens with glove support or physical controls become essential in cold weather and tactical operations.
- **Power** — A laptop running QGC, a video receiver, and a telemetry radio can draw 60–80W. Plan battery capacity for the ground station, not just the drone.
- **Antenna placement** — Ground station antennas should be elevated (tripod) and aimed at the operating area. A directional patch antenna for telemetry dramatically improves range over the stock omnidirectional antenna on most radios.
