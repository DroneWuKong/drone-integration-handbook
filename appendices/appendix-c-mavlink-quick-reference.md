# Appendix C — MAVLink Message Quick Reference

The 20 MAVLink messages you actually use in field operations.

---

## Connection & Heartbeat

### HEARTBEAT (ID: 0)
Sent every 1s by every MAVLink node. If you stop receiving it, the link is dead.

```
type          — vehicle type (1=fixed-wing, 2=quad, 6=GCS)
autopilot     — firmware (3=ArduPilot, 12=PX4)
base_mode     — bitmask (128=armed, 4=guided, 8=stabilized)
system_status — 4=standby, 5=active, 6=critical
```

---

## State & Status

### SYS_STATUS (ID: 1)
Battery voltage, current, remaining %. Check `voltage_battery` (mV) and `battery_remaining` (%).

### STATUSTEXT (ID: 253)
Human-readable status messages from the FC. **First place to look when something is wrong.**
`severity` 0=Emergency, 3=Error, 4=Warning, 6=Info.

### EXTENDED_SYS_STATE (ID: 245)
VTOL state, landed state. `landed_state` 1=on ground, 2=in air, 3=takeoff, 4=landing.

---

## Position & Navigation

### GLOBAL_POSITION_INT (ID: 33)
Primary position message. `lat`/`lon` in degE7, `alt` in mm AMSL, `relative_alt` in mm AGL.
`vx`/`vy`/`vz` in cm/s. `hdg` in cdeg.

### LOCAL_POSITION_NED (ID: 32)
Local frame position in meters. Origin is arming location. `vx`/`vy`/`vz` in m/s.

### GPS_RAW_INT (ID: 24)
Raw GPS data. `fix_type` 0=no GPS, 3=3D fix, 4=DGPS, 5=RTK float, 6=RTK fixed.
`satellites_visible`. Check `eph` (horizontal dilution) — below 200 is good.

### HOME_POSITION (ID: 242)
GPS coordinates of the home/RTL point. Request with MAV_CMD_GET_HOME_POSITION.

---

## Attitude

### ATTITUDE (ID: 30)
Roll, pitch, yaw in radians. Rates in rad/s. 100Hz on most FCs.

### VFR_HUD (ID: 74)
Human-readable: airspeed (m/s), groundspeed (m/s), heading (deg), throttle (%), altitude (m), climb (m/s).

---

## Commands (MAV_CMD)

Commands sent via COMMAND_LONG (ID: 76) or COMMAND_INT (ID: 75).
FC replies with COMMAND_ACK (ID: 77): `result` 0=accepted, 1=temp rejected, 2=denied, 3=unsupported, 4=failed.

### MAV_CMD_NAV_TAKEOFF (22)
Arm and takeoff to altitude. `param7` = target altitude in meters.

### MAV_CMD_NAV_LAND (21)
Land at current position. FC handles descent and motor cutoff.

### MAV_CMD_NAV_RETURN_TO_LAUNCH (20)
RTL. Returns to home position and lands.

### MAV_CMD_NAV_WAYPOINT (16)
Navigate to waypoint. `param5`=lat, `param6`=lon, `param7`=alt.

### MAV_CMD_DO_SET_MODE (176)
Change flight mode. `param1`=base_mode (1=custom), `param2`=custom_mode.
ArduCopter custom modes: 0=Stabilize, 2=AltHold, 3=Auto, 4=Guided, 5=Loiter, 6=RTL, 9=Land.

### MAV_CMD_COMPONENT_ARM_DISARM (400)
Arm: `param1`=1. Disarm: `param1`=0. Force disarm: `param2`=21196.

### MAV_CMD_DO_GRIPPER (211)
Payload dropper/gripper. `param1`=instance, `param2`=action (0=release, 1=grab).

### MAV_CMD_GET_HOME_POSITION (410)
Request the HOME_POSITION message.

### MAV_CMD_REQUEST_MESSAGE (512)
Request any MAVLink message by ID. `param1`=message ID. Use to get AUTOPILOT_VERSION, etc.

---

## Missions

### MISSION_COUNT (ID: 44)
Total waypoints in mission. Start of mission upload/download handshake.

### MISSION_ITEM_INT (ID: 73)
Single waypoint with integer lat/lon (degE7). Preferred over MISSION_ITEM for precision.

### MISSION_CURRENT (ID: 42)
Current active waypoint index during mission execution.

### MISSION_ACK (ID: 47)
Mission upload/download result. `type` 0=accepted, 1=error, 2=unsupported, 4=no space.

---

## Parameters

### PARAM_VALUE (ID: 22)
Single parameter value. `param_id` (16-char string), `param_value` (float), `param_type`.

### PARAM_SET (ID: 23)
Write a parameter. FC responds with PARAM_VALUE confirming the change.
**Always read back after write to confirm.**

### PARAM_REQUEST_LIST (ID: 21)
Request full parameter dump. FC streams all PARAM_VALUE messages.

---

## Common Patterns

**Check if armed:**
```
HEARTBEAT.base_mode & 128 != 0
```

**Get battery %:**
```
SYS_STATUS.battery_remaining  (0–100, -1 = unknown)
```

**Detect RTK fix:**
```
GPS_RAW_INT.fix_type == 6  (RTK fixed)
GPS_RAW_INT.fix_type == 5  (RTK float — usable but less precise)
```

**Safe disarm check:**
```
EXTENDED_SYS_STATE.landed_state == 1  (on ground)
then COMMAND_LONG MAV_CMD_COMPONENT_ARM_DISARM param1=0
```

---

## Related

- [MAVLink Protocol Overview](../firmware/mavlink-protocol.md)
- [Companion Computer Integration](../integration/companion.md)
- [MSP Quick Reference](appendix-d-msp-quick-reference.md)
