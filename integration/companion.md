# Chapter 13: Adding a Companion Computer

> A flight controller flies the drone. A companion computer
> thinks about why it's flying. They're different jobs on
> different hardware connected by a serial cable.

---

## When You Need One

You don't need a companion computer to fly a drone. You need one when:

- **Autonomous missions beyond waypoints** — obstacle avoidance,
  dynamic replanning, following a target, search patterns
- **Computer vision** — object detection, tracking, landing on a
  target, visual navigation without GPS
- **Sensor fusion** — combining LiDAR, depth cameras, and IMU data
  for environment mapping
- **High-bandwidth data processing** — real-time video analytics,
  SIGINT, spectrum analysis
- **Network hub** — bridging the FC to mesh radios, cellular modems,
  and other IP-based devices
- **AI/ML inference** — running neural networks for real-time decisions

If all you need is fly-to-waypoint with GPS, the FC handles that
natively on ArduPilot and PX4. Don't add complexity you don't need.

---

## The Hardware Options

| Platform | CPU | RAM | GPU / Accelerator | Weight | Power | Price | Best For |
|----------|-----|-----|-------------------|--------|-------|-------|----------|
| Raspberry Pi 5 | Cortex-A76 4-core | 4-8 GB | None (VideoCore for display) | 50g | 5-10W | $60-80 | General companion, MAVProxy, basic CV |
| Pi Zero 2W | Cortex-A53 4-core | 512 MB | None | 10g | 1-3W | $15 | Lightweight telemetry, data logging, RF detect |
| Jetson Orin Nano | Cortex-A78AE 6-core | 8 GB | 1024 CUDA + 32 Tensor | 60g (module) | 7-15W | $250-500 | ML inference, real-time CV, object detection |
| Jetson Orin NX | Cortex-A78AE 8-core | 8-16 GB | 1024 CUDA + 32 Tensor | 60g (module) | 10-25W | $400-900 | Heavy ML, multiple camera streams |
| ModalAI VOXL 2 | QRB5165 | 8 GB | Hexagon DSP + GPU | 16g | 4-8W | $400 | Integrated flight platform, PX4 native |
| Radxa Zero 3W | RK3566 4-core | 2 GB | Mali-G52 | 10g | 2-4W | $25 | Budget Linux companion, WiFi scanning |

### What Matters Most

**Weight:** On a 5-inch quad, every gram counts. A Pi 5 at 50g
(plus carrier board, cables, heatsink) adds 80-100g total. That's
a significant percentage of all-up weight. A Pi Zero 2W at 10g
is much more practical for small platforms.

**Power:** A companion drawing 10W from a 1300 mAh 6S battery
is consuming roughly 30% of your total energy budget. Flight time
drops proportionally. Budget the power before choosing the hardware.

**I/O:** The companion needs to connect to the FC (UART or USB),
to the network (WiFi, Ethernet for mesh radio, USB for cellular),
and to sensors (USB cameras, CSI cameras, SPI/I2C sensors).
Count your I/O requirements before selecting hardware.

---

## Connecting to the Flight Controller

### The Physical Connection

The companion talks to the FC over serial (UART) or USB. Serial
is preferred for reliability — USB adds a hub, OTG logic, and
enumeration that can fail.

```
Companion TX  →  FC UART RX
Companion RX  →  FC UART TX
Companion GND →  FC GND
```

**Baud rate:** 921600 for high-bandwidth MAVLink. 115200 for MSP.
Match both ends.

**Level shifting:** Pi GPIO is 3.3V. Most FCs are 3.3V. Compatible
without level shifting. If your FC has 5V serial outputs (rare),
use a level shifter or resistor divider.

### The Protocol

**ArduPilot / PX4:** MAVLink v2. The companion runs mavproxy,
MAVSDK, DroneKit, or a custom MAVLink parser. The FC streams
telemetry to the companion and accepts commands from it.

```python
# ArduPilot: connect via MAVSDK (Python)
from mavsdk import System
drone = System()
await drone.connect(system_address="serial:///dev/ttyAMA0:921600")
```

```python
# PX4: connect via MAVSDK (same API, different autopilot behavior)
drone = System()
await drone.connect(system_address="serial:///dev/ttyAMA0:921600")
```

**Betaflight / iNav:** MSP over serial. The companion sends MSP
requests and receives MSP responses. No streaming — poll-based.

```python
# MSP: manual serial (simplified)
import serial
ser = serial.Serial('/dev/ttyAMA0', 115200)
# Send MSP_IDENT request
ser.write(bytes([0x24, 0x4D, 0x3C, 0x00, 0x64, 0x64]))
response = ser.read(32)
```

### PX4 Dual-Channel

PX4 supports two simultaneous communication channels:

1. **MAVLink** (UART) — commands, parameters, mission, C2
2. **uXRCE-DDS** (UART or UDP) — high-bandwidth sensor telemetry,
   ROS2 topics

The dual-channel architecture lets you separate control traffic
(low bandwidth, high priority) from data traffic (high bandwidth,
lower priority). The companion runs a Micro-XRCE-DDS agent that
bridges PX4's internal uORB topics to ROS2 topics on the companion.

This replaces the older microRTPS bridge. If you see references
to microRTPS in older documentation, use uXRCE-DDS instead.

---

## Software Stack

### MAVProxy (Simplest)

MAVProxy is a command-line MAVLink proxy. It connects to the FC,
parses MAVLink, and forwards it to multiple destinations (GCS,
scripts, log files).

```bash
# Basic: FC on serial, forward to GCS on mesh radio
mavproxy.py \
  --master=/dev/ttyAMA0,921600 \
  --out=udp:10.0.0.255:14550
```

MAVProxy can run scripts (modules) that react to MAVLink messages.
It's the fastest path from "I have a companion computer" to
"I have telemetry flowing to a mesh radio."

### MAVSDK (Programmatic Control)

MAVSDK is a library (Python, C++, Swift, Rust) for programmatic
drone control over MAVLink. It abstracts MAVLink messages into
clean API calls.

```python
# Take off, fly to a point, land
await drone.action.arm()
await drone.action.takeoff()
await drone.action.goto_location(lat, lon, alt, yaw)
await drone.action.land()
```

MAVSDK is the recommended path for PX4. For ArduPilot, both
MAVSDK and DroneKit work (DroneKit is older, more ArduPilot-specific).

### ROS2 (Full Robotics Stack)

ROS2 (Robot Operating System 2) is the standard middleware for
robotics. It provides publish/subscribe messaging, service calls,
parameter management, and a massive ecosystem of packages for
navigation, perception, planning, and control.

PX4 integrates with ROS2 via uXRCE-DDS. ArduPilot has a ROS2
interface via mavros2.

**When to use ROS2:** When you need sensor fusion (multiple cameras,
LiDAR, IMU), SLAM (Simultaneous Localization and Mapping), path
planning with obstacle avoidance, or integration with existing
robotics software. ROS2 is heavyweight — it's the right choice
for research and complex autonomy, overkill for "relay telemetry
to a mesh radio."

---

## Power and Cooling

### Power Distribution

The companion needs clean, stable power. Noise from ESCs and motors
on the main power bus will crash a Pi faster than any software bug.

**Recommended:** Dedicated BEC (Battery Eliminator Circuit) from
the main battery to the companion. 5V, rated for the companion's
peak current draw (2A minimum for Pi 5, 500mA for Pi Zero 2W).

**Do not:**
- Power the companion from the FC's 5V rail (not enough current
  for most companions, and FC brownout risk)
- Share a BEC with servos or LEDs (current spikes from servos
  cause voltage drops that crash the companion)
- Use a USB cable to power the companion from the FC (USB host
  mode, OTG, and power delivery vary wildly between platforms)

### Cooling

Most companions need cooling at sustained load. A Pi 5 at full
CPU load will thermal throttle within minutes without airflow.

On a drone, the props create significant airflow. Mount the
companion where prop wash hits the heatsink. In a sealed
enclosure, this doesn't help — add a small thermal pad to
conduct heat to the frame (carbon fiber is a reasonable heat
spreader).

The VOXL 2 is designed for drones and handles thermal management
internally. The Jetson Orin modules require active cooling (fan)
for sustained ML inference.

---

## The UART Budget Impact

Adding a companion computer consumes at least one FC UART. If
you're using the companion-as-hub architecture (see Chapter 8),
it may be the only non-RC UART you need — GPS, mesh radio, and
telemetry radio connect to the companion instead of the FC.

```
Before (consuming 4 FC UARTs):
  FC ← RC receiver (UART1)
  FC ← GPS (UART2)
  FC ← Telemetry radio (UART3)
  FC ← Mesh radio (UART4)

After (consuming 2 FC UARTs):
  FC ← RC receiver (UART1)
  FC ← Companion MAVLink (UART2)
  Companion ← GPS (USB)
  Companion ← Telemetry radio (Ethernet)
  Companion ← Mesh radio (Ethernet)
  Companion ← Camera (USB/CSI)
```

This is one of the strongest practical reasons to add a companion
even if you don't need AI or computer vision: it solves the UART
shortage on F4-class FCs.

---

## What to Start With

If you've never used a companion computer on a drone:

1. **Start with a Pi Zero 2W** ($15, 10g, 2W). Wire it to the
   FC UART, install MAVProxy, forward telemetry to your laptop
   over WiFi. This proves the concept without the weight or
   power penalty.

2. **Graduate to a Pi 5** when you need more compute — running
   CV models, processing sensor data, or hosting a Wingman agent.

3. **Move to Jetson or VOXL 2** when you need real-time ML
   inference with multiple camera streams. This is where
   object detection, visual SLAM, and neural network planning
   live.

The hardware changes. The MAVLink connection pattern stays the same.
Learn it once on a Pi Zero and it works the same on a Jetson.

---

## Next

- **Chapter 8: UART Layout** — how the companion fits into the
  FC's limited serial ports.
- **Chapter 14: Mesh Radios** — the network hardware that the
  companion bridges to the FC.

---

*The flight controller flies. The companion thinks.
Don't make the flight controller think.
Don't make the companion fly.*
