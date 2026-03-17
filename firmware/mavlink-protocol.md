# Chapter 7: MAVLink Protocol — The ArduPilot/PX4 Language

> MAVLink is a publish-subscribe protocol. You tell the FC what
> streams you want, and it sends them continuously. You send
> commands when you need something done. Both directions flow
> at the same time.

---

## What MAVLink Is

MAVLink (Micro Air Vehicle Link) is the communication protocol
used by ArduPilot, PX4, and their ecosystems. It's been the
standard for autonomous drone communication since ~2009.

Unlike MSP (request-response), MAVLink is a streaming protocol.
The FC continuously publishes telemetry at configured rates, and
the GCS/companion sends commands as needed. Both directions are
independent — you can receive telemetry while sending a command.

**MAVLink v2** is the current version. v1 is deprecated but still
supported for backward compatibility. Always use v2 for new
development.

---

## Packet Format (MAVLink v2)

```
Byte:  0     1     2     3     4       5       6       7-9       10..N    N+1..N+2
       0xFD  len   seq   sys   comp    msg_id  msg_id  msg_id    payload  crc16
       magic             id    id      [24-bit LE]               [data]   [checksum]
```

| Field | Size | Description |
|-------|------|-------------|
| Magic | 1 | 0xFD (v2) or 0xFE (v1) |
| Payload length | 1 | 0-255 bytes |
| Incompatible flags | 1 | Feature flags (signing, etc.) |
| Compatible flags | 1 | Backward-compatible flags |
| Sequence | 1 | Incrementing counter per link |
| System ID | 1 | Which vehicle (1-254) |
| Component ID | 1 | Which subsystem (1=autopilot, 191=companion) |
| Message ID | 3 | 24-bit, little-endian |
| Payload | variable | Message-specific data |
| Checksum | 2 | CRC-16/MCRF4XX with seed byte |

---

## System and Component IDs

Every device on a MAVLink network has a system ID and component ID.

**System ID:** Identifies the vehicle. Drone 1 = system 1, Drone 2
= system 2. GCS is typically system 255. In a swarm, each drone
must have a unique system ID.

**Component ID:** Identifies a subsystem within the vehicle.
- 1 = Autopilot (the FC)
- 100 = Camera
- 154 = Gimbal
- 191 = Companion computer (Wingman uses this)
- 250 = GCS

**Why this matters:** When you connect to a mesh with 10 drones,
you'll receive MAVLink messages from all of them. The system ID
tells you which drone sent each message. If two drones have the
same system ID, you can't tell them apart. This is one of the most
common mistakes in multi-vehicle setups.

**Setting the system ID:**
- ArduPilot: `SYSID_THISMAV` parameter
- PX4: `MAV_SYS_ID` parameter

---

## The Messages That Matter

### HEARTBEAT (msg_id = 0) — The Keepalive

Every MAVLink device sends HEARTBEAT at 1 Hz. It's how devices
discover each other and know the connection is alive.

```
Fields:
  type          = vehicle type (2=quadrotor, 1=fixed wing, etc.)
  autopilot     = firmware (3=ArduPilot, 12=PX4)
  base_mode     = armed/disarmed flag (bit 7)
  custom_mode   = current flight mode (firmware-specific number)
  system_status = boot/calibrating/active/critical/emergency
```

**Auto-detect pattern:** Send a HEARTBEAT with system ID 255
(GCS). Wait for a response. Read the `autopilot` field:
3 = ArduPilot, 12 = PX4. This is the equivalent of MSP_FC_VARIANT
for the MAVLink world.

**No heartbeat = dead link.** If you stop receiving heartbeats
from a drone for > 5 seconds, the link is lost. ATAK and QGC
both use this to mark connections as stale.

---

### Parameter Protocol

MAVLink parameters are named floating-point values. ArduPilot has
~1,200. PX4 has ~900.

| Message | Direction | Description |
|---------|-----------|-------------|
| PARAM_REQUEST_LIST | GCS → FC | "Send me all parameters" |
| PARAM_VALUE | FC → GCS | One parameter: name, value, type, index, count |
| PARAM_SET | GCS → FC | "Set this parameter to this value" |

**Full parameter pull:**
1. Send PARAM_REQUEST_LIST
2. FC streams PARAM_VALUE messages (one per parameter)
3. Track received indices — if any are missing after the stream
   ends, request them individually with PARAM_REQUEST_READ

A full pull of ~1,200 ArduPilot parameters at 115200 baud takes
5-15 seconds depending on link quality.

**Writing a parameter:**
1. Send PARAM_SET with param_id (name) and param_value
2. FC responds with PARAM_VALUE confirming the new value
3. If the confirmed value differs from what you sent, the FC
   rejected or clamped the value

**Parameters persist across reboots** (stored in EEPROM/flash).
No separate save command needed, unlike MSP's MSP_EEPROM_WRITE.

---

### Telemetry Streams

Request telemetry streams by sending REQUEST_DATA_STREAM or
SET_MESSAGE_INTERVAL.

Key telemetry messages:

| Message | ID | Rate | Content |
|---------|-----|------|---------|
| GLOBAL_POSITION_INT | 33 | 2-10 Hz | Lat, lon, alt, heading, velocities |
| ATTITUDE | 30 | 10-50 Hz | Roll, pitch, yaw (radians) |
| VFR_HUD | 74 | 2-10 Hz | Airspeed, groundspeed, heading, throttle, alt, climb |
| SYS_STATUS | 1 | 1-2 Hz | Sensor health, battery voltage, current, remaining % |
| BATTERY_STATUS | 147 | 1 Hz | Per-cell voltage, current, mAh consumed, temperature |
| GPS_RAW_INT | 24 | 2-5 Hz | GPS fix type, satellites, HDOP, raw position |
| RC_CHANNELS | 65 | 5-10 Hz | All RC channel values (for monitoring stick input) |

**Setting stream rates (ArduPilot):**
```
SR0_POSITION=2      # GLOBAL_POSITION_INT at 2 Hz
SR0_EXTRA1=4         # ATTITUDE at 4 Hz
SR0_EXTRA2=2         # VFR_HUD at 2 Hz
SR0_RAW_SENS=1       # RAW sensor data at 1 Hz
SR0_RC_CHAN=5         # RC channels at 5 Hz
```

`SR0_*` parameters control stream rates for serial port 0 (usually
TELEM1). Replace `0` with the port number for other connections.

**Setting stream rates (PX4):**
PX4 uses SET_MESSAGE_INTERVAL command to set per-message rates.

---

### Commands

MAVLink commands are sent via COMMAND_LONG or COMMAND_INT and
acknowledged via COMMAND_ACK.

| Command | ID | Description |
|---------|-----|-------------|
| MAV_CMD_COMPONENT_ARM_DISARM | 400 | Arm or disarm |
| MAV_CMD_DO_SET_MODE | 176 | Change flight mode |
| MAV_CMD_NAV_TAKEOFF | 22 | Takeoff to specified altitude |
| MAV_CMD_NAV_LAND | 21 | Land at current position |
| MAV_CMD_NAV_RETURN_TO_LAUNCH | 20 | Return to home |
| MAV_CMD_DO_REBOOT | 246 | Reboot FC |

**Arm command:**
```
COMMAND_LONG:
  target_system = 1    (drone's system ID)
  command = 400         (ARM_DISARM)
  param1 = 1.0          (1=arm, 0=disarm)
  param2 = 0.0          (0=normal, 21196=force arm — dangerous)
```

**Wait for COMMAND_ACK.** Result 0 = accepted. Result 4 = denied
(pre-arm checks failed). Result 5 = in progress.

---

### Mission Protocol

Upload waypoint missions to the FC:

1. Send MISSION_COUNT (number of waypoints)
2. FC requests each with MISSION_REQUEST_INT
3. Send each MISSION_ITEM_INT
4. FC confirms with MISSION_ACK

Download existing mission:
1. Send MISSION_REQUEST_LIST
2. FC sends MISSION_COUNT
3. Request each with MISSION_REQUEST_INT
4. FC sends each MISSION_ITEM_INT

---

### Offboard Control (PX4)

PX4's offboard mode lets the companion computer directly command
position, velocity, or attitude setpoints:

```
SET_POSITION_TARGET_LOCAL_NED:
  x, y, z = position in local NED frame (meters)
  vx, vy, vz = velocity (m/s)
  type_mask = which fields are valid
```

**Requirements for offboard mode:**
1. Companion must stream setpoints at > 2 Hz (PX4 requires
   continuous updates or it exits offboard mode)
2. RC switch must be set to offboard mode
3. Vehicle must be armed

This is the control path for Wingman L3 (Delegate) autonomous
operations on PX4.

---

## ArduPilot vs. PX4: MAVLink Differences

Both speak MAVLink v2, but they differ in important ways:

| Feature | ArduPilot | PX4 |
|---------|-----------|-----|
| Flight mode numbers | ArduPilot-specific (0=Stabilize, 3=Auto, 6=RTL) | PX4-specific (different numbers for same concepts) |
| Parameter names | `ATC_RAT_RLL_P` style | `MC_ROLLRATE_P` style |
| Stream rate config | `SR0_*` parameters | SET_MESSAGE_INTERVAL command |
| Offboard control | Guided mode + SET_POSITION_TARGET | Offboard mode + SET_POSITION_TARGET |
| Sensor data | High-bandwidth DDS bridge | uXRCE-DDS to ROS2 |
| Mission dialect | Standard + ArduPilot extensions | Standard (fewer extensions) |

**Implication for tools:** Any tool that works across both ArduPilot
and PX4 (QGroundControl, MAVSDK, Wingman) must handle these
differences. The MAVLink wire format is identical — the interpretation
of mode numbers, parameter names, and command behaviors differs.

---

## Practical Tips

**Always send heartbeats.** Your GCS or companion must send
HEARTBEAT at 1 Hz to the FC. If the FC doesn't receive GCS
heartbeats, it may trigger GCS failsafe (ArduPilot: `FS_GCS_ENABLE`).

**Monitor packet loss.** MAVLink packets have a sequence number.
If you see gaps in the sequence, you're losing packets. At > 5%
loss, the link is degraded. At > 20%, it's unreliable for commands.

**Don't flood the link.** Sending commands faster than the FC can
process them causes buffer overflow and dropped messages. One
command at a time, wait for COMMAND_ACK before sending the next.

**Use MAVSDK or pymavlink, not raw parsing.** MAVLink has 300+
message types with varying payload formats. Writing a parser from
scratch is an error-prone waste of time. MAVSDK (for control) and
pymavlink (for analysis) handle the parsing.

**Test with SITL.** Both ArduPilot and PX4 have Software-In-The-Loop
simulators that emulate a real FC over a simulated MAVLink link.
Test your companion software against SITL before connecting to
real hardware.

---

## Next

- **Chapter 6: MSP Protocol** — the simpler alternative for
  Betaflight and iNav.
- **Chapter 8: UART Layout** — where MAVLink connections go
  in the FC's serial port map.

---

*MAVLink is a conversation. The FC talks continuously. You listen
and speak when you have something to say. The protocol handles
the rest.*
