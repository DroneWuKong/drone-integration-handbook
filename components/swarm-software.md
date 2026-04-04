# Swarm Software

> **Forge cross-reference:** 10 entries in `swarm_software` category  
> **Related handbook chapters:** Mesh Radios, Companion Computers, TAK Integration  
> **Related Forge pages:** /swarm-guide/, /swarm-selector/

## What Swarm Software Does

Swarm software coordinates multiple drones as a single system. This ranges from choreographed drone shows (pre-scripted positions and LED colors) to autonomous tactical swarms (real-time decision-making, target assignment, and formation control without operator input for each vehicle).

The common thread is multi-vehicle coordination: the software must manage communications between vehicles, resolve conflicts (collision avoidance, task deduplication), and provide a single-operator interface to the fleet.

## Two Domains

### Drone Show / Formation

Pre-choreographed multi-vehicle flight with precise timing and LED control. Safety is the primary concern — hundreds of drones flying in close proximity with paying spectators below.

- **Skybrush Server (CollMot Robotics)** — Industry-standard open-source drone show server. Python/Trio async architecture managing fleet orchestration, time synchronization, LED control, and geofencing. Supports PX4 and ArduPilot via MAVLink. The server is the backbone; two companion tools complete the ecosystem.
- **Skybrush Live** — React/TypeScript GCS frontend for Skybrush. Real-time map with drone positions, LED preview, formation editor, show timeline, and safety controls.
- **Skybrush Studio for Blender** — Blender add-on for designing and validating drone show choreographies. Animate point objects in 3D, assign LED colors, export to Skybrush format. Includes collision detection and safety validation before export.
- **MDS (MAVSDK Drone Show)** — All-in-one PX4 drone show and smart swarm platform. MAVSDK-based multi-drone coordination with Docker SITL simulation, React GCS dashboard, Skybrush import, LED control, and leader-follower clustering. Free for fewer than 10 drones.

### Research / Tactical Swarm

Autonomous multi-vehicle systems with real-time decision-making. These range from academic research platforms to battlefield-ready systems.

- **Crazyswarm2 (IMRCLab, USC)** — The gold standard for indoor swarm research using Crazyflie nano-quadcopters. Scales to 49+ drones. ROS 2 (Humble) based with trajectory tracking, formation control, real-time visualization, and motion capture integration. If you are publishing swarm research, you are likely using this.
- **CoFlyers (MICROS Lab)** — General platform for collective flying with MATLAB/Simulink simulation and real hardware support (Crazyflie, Tello). Bio-inspired swarming behaviors, formation control, and collective decision-making.
- **DSSE (Drone Swarm Search Environment)** — PettingZoo-based multi-agent reinforcement learning training environment for search-and-rescue drone swarm missions. Published in JOSS and arXiv. Useful for training RL policies before deploying on real hardware.
- **ORCUS** — Fully autonomous swarm kamikaze drone system with YOLOv12 detection, ray-ground intersection geo-localization, EKF multi-drone sensor fusion, Hungarian algorithm attack assignment, and a 7-step handshake attack protocol. Represents the tactical swarm endpoint.

### Adjacent Tools

- **OpenIPC FPV** — Open-source firmware for IP camera SoCs (HiSilicon, Goke, SigmaStar) repurposed as FPV air units using wifibroadcast (WFB-NG). Not swarm software per se, but enables low-cost video links that make swarm platforms economically viable at scale.
- **Insper NVIDIA Jetbot Autopilot** — Jetson Nano ground vehicle with OpenCV lane following and YOLOv3-tiny detection. Included as a multi-vehicle coordination reference rather than an aerial swarm tool.

## Integration Requirements

Swarm software requires three infrastructure layers that single-vehicle operations do not:

1. **Inter-vehicle communications** — Mesh radios (Silvus, Doodle Labs, ELRS mesh experiments) or Wi-Fi for short-range. See the Mesh Radios chapter. Latency and bandwidth per vehicle determine swarm density limits.
2. **Time synchronization** — Drone shows require sub-millisecond time sync (GPS PPS or NTP). Tactical swarms need coordinated clocks for sensor fusion across vehicles.
3. **Centralized or distributed coordination** — Skybrush uses a centralized server model (single point of command). Crazyswarm2 uses centralized motion capture. ORCUS uses distributed decision-making. The architecture choice depends on whether you can guarantee a ground link to every vehicle.

## Scaling Considerations

Swarm scale is constrained by communications bandwidth, not compute. Each vehicle in a MAVLink swarm generates 10–50 kbps of telemetry. At 50 vehicles, that is 500 kbps–2.5 Mbps of inbound telemetry at the ground station, plus outbound commands. Mesh radios handle this well up to ~30 nodes; beyond that, hierarchical architectures (squad leaders relaying for team members) become necessary.
