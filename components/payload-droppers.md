# Payload Droppers & Release Mechanisms

> **Forge cross-reference:** 4 entries in `payload_droppers` category  
> **Related handbook chapters:** Sensor Payload Integration, Frames & Airframe Selection

## Controlled Payload Release

Payload droppers are electromechanical mechanisms that release a carried payload on command from the flight controller or GCS. The applications span commercial delivery (DJI Delivery Hub, Zipline-style systems), agricultural (seed/granule release), search and rescue (supply drops), and military (munition release).

The 4 entries in the Forge database represent the publicly available commercial ecosystem. Military payload release systems are intentionally outside the scope of this handbook.

## Commercial Applications

### Delivery Drones
DJI and other enterprise platforms integrate payload release directly into the platform firmware. The DJI Delivery Hub and WindWing series treat package delivery as a mission type with ground-level winch lowering — not a simple drop. This avoids the impact damage of free-fall delivery and handles the "last meter" precision problem where GPS accuracy (~1m) is insufficient to guarantee safe drop zone clearance.

### Agricultural Distribution
Pellet and granule spreaders attach to multi-rotor platforms (M300, Agras series) for seed distribution, cover crop planting, and pest control material application. These are high-volume release mechanisms with configurable flow rates, not single-item release.

### SAR Supply Drops
Search and rescue operations use payload droppers to deliver survival supplies (water, food, first aid) to stranded individuals when landing is impossible. Simple spring-loaded or servo-actuated mechanisms release a packaged payload. The dropped payload is typically attached to a short drogue chute for deceleration.

## Mechanism Types

**Servo-actuated claw/gripper:** The simplest design. A servo opens a claw or latch when commanded. Low weight, reliable, configurable throw angle. Cannot handle payloads larger than the claw grip radius.

**Electromagnet release:** A powered electromagnet holds a ferromagnetic payload. De-energizing the magnet releases the payload. Clean release, no moving parts. Requires payload to have a magnetic attachment point.

**Winch/cable lowering:** A motorized spool lowers the payload on a thin line then releases. Enables precision placement without free-fall. Higher weight and complexity. DJI Delivery Hub uses this approach.

**Pyrotechnic (defense):** Not covered in this handbook.

## Integration

Payload droppers connect to a spare FC servo output channel and are commanded via a switch on the transmitter assigned to that channel. In Betaflight, use `SERVO` output rules. In ArduPilot, use `SERVOn_FUNCTION` parameter to assign `Gripper` function to the relevant output.

**ArduPilot Gripper:**
```
GRIP_ENABLE = 1
GRIP_TYPE = 1       # servo type
GRIP_CHANNEL = 9    # RC channel to control
SERVO9_FUNCTION = 28  # Gripper function
```

Mission commands `MAV_CMD_DO_GRIPPER` allow GCS-commanded release at a waypoint during an autonomous mission — enabling pre-programmed delivery at a GPS coordinate.

## NDAA

All 4 payload dropper entries in the database are US or allied-nation manufactured. No NDAA concerns in this category for commercial release mechanisms.
