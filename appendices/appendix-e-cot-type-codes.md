# Appendix E — CoT Type Code Reference

Common Cursor on Target (CoT) type codes for drone operations.
CoT is the messaging standard used by ATAK, TAK Server, and military C2 systems.

---

## Type Code Format

```
atom-affiliation-battle-dimension.function.modifier
```

Example: `a-f-A-M-F-Q` = Atoms, Friendly, Air, Military, Fixed Wing, Unmanned

---

## Affiliation

| Code | Meaning |
|------|---------|
| `f` | Friendly |
| `h` | Hostile |
| `n` | Neutral |
| `u` | Unknown |
| `p` | Pending (being tracked) |
| `a` | Assumed friend |
| `s` | Suspect |

---

## Battle Dimension (3rd character)

| Code | Meaning |
|------|---------|
| `A` | Air |
| `G` | Ground |
| `S` | Sea surface |
| `U` | Subsurface |
| `P` | Space |
| `X` | Other |

---

## Common UAS Type Codes

### UAS Platform Types

| Code | Description |
|------|-------------|
| `a-f-A-M-F-Q` | Friendly, Air, Military, Fixed Wing, Unmanned |
| `a-f-A-M-H-Q` | Friendly, Air, Military, Rotary Wing, Unmanned |
| `a-f-A-M-F-Q-r` | Friendly, UAS Fixed Wing, Reconnaissance |
| `a-f-A-M-H-Q-r` | Friendly, UAS Rotary Wing, Reconnaissance |
| `a-h-A-M-F-Q` | Hostile, Air, Military, Fixed Wing, Unmanned |
| `a-h-A-M-H-Q` | Hostile, Air, Military, Rotary Wing, Unmanned |
| `a-u-A-M-F-Q` | Unknown, Air, Military, Fixed Wing, Unmanned |
| `a-u-A-M-H-Q` | Unknown, Air, Military, Rotary Wing, Unmanned |

### Ground Control / Personnel

| Code | Description |
|------|-------------|
| `a-f-G-U-C-F` | Friendly, Ground, Unit, Combat Support, Aviation |
| `a-f-G-E-V-A` | Friendly, Ground, Equipment, Vehicle, Aircraft |
| `a-f-G-U-C-F-A-D` | UAS Detachment (customary extension) |

### Points of Interest

| Code | Description |
|------|-------------|
| `b-m-p-s` | Waypoint |
| `b-m-p-w` | Warning point |
| `b-m-p-i` | Information waypoint |
| `b-m-p-c-cp` | Control point |
| `b-m-r` | Route |
| `b-m-r-w` | Route waypoint |
| `b-m-p-j` | Jump point / launch point |
| `b-r-f-h-c` | FARP (Forward Arming and Refueling Point) |

---

## UAS Sensor / Track Events

| Code | Description |
|------|-------------|
| `a-f-A-M-H-Q` | Friendly UAS rotary (generic track) |
| `t-x-c` | Contact report |
| `t-x-d` | Detection event |
| `t-x-t` | Track report |
| `t-r-c-a` | Aircraft contact |

---

## Common DFR Use Cases

### Responding Drone (friendly)

```xml
<event type="a-f-A-C-H-Q" ...>
  <!-- a = atoms, f = friendly, A = air, C = civil, H = rotary, Q = unmanned -->
  <detail>
    <contact callsign="DFR-01"/>
    <status readiness="true"/>
    <uas type="DFR" model="Skydio X10D"/>
  </detail>
</event>
```

### Detected Hostile UAS

```xml
<event type="a-h-A-M-H-Q" ...>
  <detail>
    <contact callsign="UNK-01"/>
    <remarks>Detected 5.8GHz analog video, ~200m altitude, S approach</remarks>
  </detail>
</event>
```

### Launch Point Marker

```xml
<event type="b-m-p-j" ...>
  <detail>
    <contact callsign="LP-NORTH"/>
    <remarks>DFR launch point, clear approach from W</remarks>
  </detail>
</event>
```

---

## ATAK Integration Notes

**PLI (Position Location Information):** UAS PLI tracks appear in ATAK
with the UAS icon when using `a-f-A-*-Q` type codes. Most autopilot
MAVLink bridges (WinTAK-UAS, DRONELINK) emit these automatically.

**GeoFence:** Use `a-u-r` (unknown, area) type for geofence boundaries.

**Emergency:** Use `b-r-e` emergency type for lost link / emergency RTL
alerts sent from GCS to TAK network.

**Team Awareness:** Pilots should appear as `a-f-G-U-C-F` (friendly
ground unit) with their location, not as UAS tracks.

---

## Further Reference

- MIL-STD-2525C: *Department of Defense Interface Standard: Common Warfighting Symbology*
- TAK Product Center: tak.gov
- [TAK Integration Guide](../integration/tak.md)
