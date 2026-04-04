# Navigation & PNT (Position, Navigation, Timing)

> **Forge cross-reference:** 12 entries in `navigation_pnt` category  
> **Related handbook chapters:** RTK/PPK GPS Integration, GNSS Receiver Quality Ecosystem

## Beyond GPS

Standard GNSS receivers — covered in the GPS Modules and RTK/PPK chapters — work well in open sky. But drones increasingly operate where GNSS degrades or fails entirely: urban canyons, under canopy, indoors, underground, and in contested electromagnetic environments where jamming and spoofing are active threats.

The navigation_pnt category covers hardware that provides position, navigation, and timing when GNSS is degraded, denied, or untrusted. This includes inertial navigation systems (INS), anti-jam antennas, vision-aided navigation, quantum sensors, and multi-sensor fusion platforms.

## Technology Tiers

### Tier 1: Tactical MEMS IMU/INS

MEMS (Micro-Electro-Mechanical Systems) inertial sensors measure acceleration and rotation without external references. They drift over time — the question is how fast.

- **SBG Systems Pulse-40** — Tactical grade MEMS IMU with 0.08°/√h gyro noise and 6µg accelerometers. Individually factory-calibrated. The entry point for "real" inertial navigation (as opposed to the IMUs already on flight controllers, which are consumer-grade and drift in seconds). Pairs with GNSS for GPS/INS fusion; provides dead-reckoning when GNSS drops.
- **Honeywell HGuide o480** — Low-SWaP INS with integrated anti-jamming and anti-spoofing. Available with single or dual antenna configurations. Honeywell pedigree in aviation-grade navigation brings defense program credibility.

### Tier 2: FOG and High-Performance INS

Fiber Optic Gyroscopes (FOG) replace MEMS with optical measurement of rotation via the Sagnac effect. They are larger and more expensive but drift orders of magnitude more slowly.

- **Advanced Navigation Boreas D90** — FOG INS with AI-powered sensor fusion achieving sub-0.1% distance error. This means after 1 km of GPS-denied flight, position error is under 1 meter. Expensive and heavy, but it is the benchmark for autonomous BVLOS in contested environments.
- **Inertial Labs VINS** — Vision-Aided INS combining inertial sensors with camera-based visual odometry plus Air Data Computer. Provides navigation in both GPS-enabled and GPS-denied environments. The visual aiding significantly reduces drift rate compared to pure inertial.

### Tier 3: Anti-Jam / Anti-Spoof GNSS

These do not replace GNSS — they harden it against electronic attack.

- **Inertial Labs M-AJ-QUATRO** — Multi-element Controlled Reception Pattern Antenna (CRPA) for anti-jamming. Null-steers antenna pattern to reject interference while maintaining satellite lock. Works across GPS/GLONASS/Galileo/BeiDou. This is the "armored vest" for your GNSS receiver.
- **infiniDome GPSdome** — Listed in the ew_systems category but functionally a GNSS protection device. Lightweight, lower cost than CRPA arrays, designed for Group 1–2 UAS.

### Tier 4: Vision-Based Navigation

Camera and LiDAR-based positioning that requires no external infrastructure.

- **ModalAI VIO** — Visual-Inertial Odometry system running on VOXL 2 hardware. Uses stereo cameras and IMU fusion for GPS-denied navigation. Integral to the ModalAI Blue UAS autonomy stack. Works indoors, under canopy, and in urban environments where GNSS multipath makes RTK unreliable.

### Tier 5: Quantum and Next-Generation PNT

Emerging technologies that promise order-of-magnitude improvements in drift rate.

- **Infleqtion Tiqker** — Compact atomic clock for timing resilience. When GNSS is denied, timing drifts along with position. Atomic clocks hold time accurately enough to maintain network synchronization and encrypted communications without GNSS timing input.
- **Infleqtion Quantum IMU** — Quantum inertial measurement using cold atom interferometry. Still in development/early deployment, but the physics promises drift rates that make FOG look noisy. The endgame for GPS-denied navigation.
- **Q-CTRL Ironstone Opal** — Quantum-enhanced inertial navigation using trapped-ion technology. Australian company with defense backing.
- **Anello Photonic INS** — Silicon photonic gyroscope using integrated photonics manufacturing. Aims to deliver FOG-class performance at MEMS cost and size by leveraging semiconductor fabrication techniques.

### Tier 6: Underwater/Multi-Domain

- **Teledyne DVL+INS** — Doppler Velocity Log paired with inertial navigation for underwater vehicles. Included because underwater drones (ROVs, AUVs) face the same GPS-denied navigation challenge as aerial platforms in contested environments.

## Selection Framework

The right PNT system depends on the threat environment and mission profile:

| Scenario | Minimum PNT | Recommended |
|----------|-------------|-------------|
| Commercial BVLOS, open sky | RTK GNSS + basic IMU | RTK + SBG Pulse-40 for dead-reckoning backup |
| Urban operations | GNSS + VIO fallback | ModalAI VIO or Inertial Labs VINS |
| Defense, non-contested | GPS/INS fusion | Honeywell HGuide o480 |
| Defense, contested EW | Anti-jam GNSS + FOG INS | M-AJ-QUATRO + Boreas D90 |
| Indoor / subterranean | VIO + LiDAR SLAM | ModalAI VIO + LiDAR (see SLAM guide) |
| Long-endurance GPS-denied | FOG INS + atomic clock | Boreas D90 + Tiqker |

## Integration Notes

PNT systems connect to the flight controller via MAVLink (for autopilots like ArduPilot/PX4) or directly to the companion computer for processing before forwarding navigation solutions. Key integration considerations:

- **Mounting** — INS units must be rigidly mounted to the airframe with known lever arm offsets programmed in. Vibration isolation is counterproductive for inertial sensors — they need to feel the vehicle's motion, not be isolated from it. This is the opposite of how you mount a flight controller IMU.
- **Alignment** — IMU axes must be precisely aligned with the vehicle's body frame. Misalignment directly translates to navigation error.
- **Initialization** — Most INS require a stationary alignment period (30 seconds to several minutes) to establish initial attitude. Plan this into mission timelines.
- **Aiding sources** — Modern INS are designed to fuse multiple aiding sources: GNSS, VIO, barometer, magnetometer, DVL, airspeed. Configure all available aiding sources for best performance.

## Supply Chain Notes

PNT hardware intersects multiple PIE supply constraint flags. MEMS sensors depend on semiconductor fabrication (STM32 and similar MCUs for processing). FOG components have limited suppliers. Quantum PNT is early-market with single-source risk on key components. See PIE predictions for timeline estimates on PNT-adjacent supply constraints.
