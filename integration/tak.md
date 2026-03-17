# Chapter 15: TAK Integration

> TAK is where your drone shows up on the map next to everyone
> else's position. Getting there doesn't require a defense contractor.
> It requires one UDP packet.

---

## What TAK Is

TAK (Team Awareness Kit) is a situational awareness platform used
by the US military, law enforcement, fire services, and increasingly
by civilian teams. It shows positions, tracks, sensor data, and
messages on a shared map.

The ecosystem:
- **ATAK** — Android TAK (phone/tablet)
- **WinTAK** — Windows version (laptop)
- **iTAK** — iOS version
- **TAK Server** — centralized server for team data sharing
- **WebTAK** — browser-based viewer

TAK speaks one protocol: **Cursor-on-Target (CoT)**. Everything
that appears on the map is a CoT event — an XML message with a
type, position, and metadata. If your drone can send a CoT event,
it appears on TAK.

---

## Cursor-on-Target (CoT) Basics

A CoT event is an XML message. Here's the minimum viable drone
position report:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<event version="2.0"
       uid="drone-01"
       type="a-f-A-M-H-Q"
       how="m-g"
       time="2026-03-16T18:30:00Z"
       start="2026-03-16T18:30:00Z"
       stale="2026-03-16T18:30:30Z">
  <point lat="44.9778" lon="-93.2650" hae="300"
         ce="10" le="15"/>
</event>
```

That's it. Send this over UDP to port 4242 on a TAK Server or
directly to ATAK devices on the local network, and your drone
appears on the map.

### The Fields That Matter

**uid:** Unique identifier for your drone. Once set, every update
with the same uid moves the same icon on the map. Use something
stable — `wingman-{tooth-id}` or `drone-{serial}`.

**type:** The CoT type code determines the icon and classification.
It follows the 2525C symbology standard:

| Type Code | Meaning | Icon |
|-----------|---------|------|
| a-f-A-M-H-Q | Friendly, Air, Military, Rotary Wing | Blue helicopter |
| a-f-A-M-F-Q | Friendly, Air, Military, Fixed Wing | Blue airplane |
| a-f-G | Friendly, Ground | Blue ground vehicle |
| a-n-A-M-H-Q | Neutral, Air, Rotary Wing | Green helicopter |
| a-h-A-M-H-Q | Hostile, Air, Rotary Wing | Red helicopter |
| a-h-G-E-V-A | Hostile, Ground, Equipment, Vehicle | Red vehicle (used for RF detections) |

The first character after `a-` is the affiliation:
`f` = friendly, `n` = neutral, `h` = hostile, `u` = unknown.

**how:** How the position was determined.
`m-g` = machine GPS, `h-e` = human entry, `h-g-i-g-o` = GPS from another source.

**time/start/stale:** When the event was generated, when it starts
being valid, and when it becomes stale (should be removed from the
map if not refreshed). Set stale to 30-60 seconds for a moving drone
so the icon disappears if the drone stops reporting.

**point:** Latitude, longitude, height above ellipsoid (meters),
circular error (meters), linear error (meters).

---

## Adding Detail

### Telemetry in CoT

CoT supports a `<detail>` element for additional data. TAK clients
display this in the info popup when you tap the icon:

```xml
<event ...>
  <point lat="44.9778" lon="-93.2650" hae="300" ce="10" le="15"/>
  <detail>
    <remarks>Battery: 14.8V (76%) | Alt: 300m AGL | Speed: 12 m/s</remarks>
    <track course="045" speed="12"/>
    <contact callsign="WINGMAN-01"/>
    <__group name="Blue" role="Team Member"/>
  </detail>
</event>
```

**track:** Course (degrees true) and speed (m/s). Allows TAK to
show heading arrows and predict future position.

**contact:** The callsign displayed on the map next to the icon.

**__group:** Team assignment and role. Determines icon color in
some TAK configurations.

**remarks:** Free-text field. Put your telemetry summary here.
ATAK shows it in the detail popup.

### Sensor Point of Interest

When your drone detects something (RF emission, visual target,
anomaly), send a separate CoT event for the detection:

```xml
<event uid="detect-001"
       type="a-h-G-E-V-A"
       how="m-g" ...>
  <point lat="44.9790" lon="-93.2640" hae="0" ce="50" le="50"/>
  <detail>
    <remarks>RF Detection: DoodleLabs MR900 | RSSI: -72 dBm | Bearing: 045</remarks>
    <contact callsign="RF-DETECT-001"/>
  </detail>
</event>
```

This places a hostile marker on the map at the estimated position
of the detection. The NeedleNThread tactical RF detector uses
exactly this pattern to push detections to TAK.

---

## Transport: Getting CoT to TAK

### Direct UDP (Simplest)

Send CoT XML as a UDP packet to ATAK devices on the local network.
Default port: 4242.

```python
import socket

cot_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<event version="2.0" uid="drone-01" type="a-f-A-M-H-Q"
       how="m-g" time="{time}" start="{time}" stale="{stale}">
  <point lat="{lat}" lon="{lon}" hae="{alt}" ce="10" le="15"/>
  <detail>
    <contact callsign="WINGMAN-01"/>
    <track course="{heading}" speed="{speed}"/>
  </detail>
</event>'''

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(cot_xml.encode(), ('239.2.3.1', 6969))  # multicast
# or
sock.sendto(cot_xml.encode(), ('192.168.1.100', 4242))  # unicast to ATAK device
```

**Multicast** (239.2.3.1:6969) reaches all ATAK devices on the
local network without knowing their IPs. Requires a network that
supports multicast (WiFi works, some mesh radios don't forward
multicast by default).

**Unicast** to a specific IP is more reliable but requires knowing
the ATAK device's address.

### Via TAK Server

A TAK Server centralizes all CoT traffic. Devices connect to the
server (TCP, TLS, or WebSocket) and the server distributes events
to all connected clients.

The drone (or its companion computer) connects to the TAK Server
and sends CoT events. All ATAK/WinTAK clients connected to the
same server see the drone.

**FreeTAKServer** is an open-source TAK Server that runs on a
Pi, laptop, or cloud VM. It handles basic CoT routing without
the complexity of the official TAK Server.

```bash
pip install FreeTAKServer
python -m FreeTAKServer.controllers.services.FTS
```

### Via Mesh Radio

If the drone has a mesh radio (Chapter 14), CoT can travel over
the mesh. The companion computer sends CoT to the mesh radio's
IP, and the mesh radio delivers it to the GCS or TAK Server on
the other end.

```
Drone: FC → Companion → CoT UDP → Mesh Radio → [mesh] → GCS/TAK Server
```

This is the standard architecture for tactical drone operations.
The mesh radio carries both MAVLink (for flight control) and CoT
(for situational awareness) on the same link, typically on
different UDP ports.

---

## Integration Points

### From the Flight Controller

The FC has the position, altitude, heading, speed, and battery
data. This needs to get from the FC to the TAK sender:

**ArduPilot/PX4:** MAVLink messages on the companion → parse
GLOBAL_POSITION_INT, VFR_HUD, BATTERY_STATUS → format as CoT → send.

**Betaflight/iNav:** MSP on the companion → parse MSP_RAW_GPS,
MSP_ATTITUDE, MSP_ANALOG → format as CoT → send. Or use the
ELRS/CRSF telemetry downlink on the transmitter side → forward
to ATAK on the GCS phone.

### From Sensors

Payload sensors (cameras, RF detectors, environmental) generate
their own CoT events through the companion computer. Each detection
gets its own uid and type code.

### From the Wingman Ecosystem

The Wingman architecture naturally generates TAK-compatible data:
- **Tooth mesh:** Fleet position sharing maps directly to CoT events
- **Seed detections:** Acoustic, RF, and PIR detections become
  CoT hostile/unknown markers
- **Wingman Command:** The Command layer IS the TAK integration
  point for the full ecosystem — it translates Wingman mesh data
  into the CoT format that existing TAK infrastructure consumes

---

## Practical Tips

**1. Keep CoT events small.** TAK clients handle thousands of events.
Your drone doesn't need to send a novel — position, callsign, basic
telemetry in remarks. The detail popup in ATAK has limited space.

**2. Update rate: 1 Hz is enough.** TAK is situational awareness,
not flight control. Sending position once per second is plenty.
Faster than that wastes bandwidth and doesn't improve the map display.

**3. Use meaningful callsigns.** "WINGMAN-01" is useful on a shared
map. "drone-abc123def" is not. Callsigns should be short, unique,
and recognizable.

**4. Set stale time appropriately.** 30 seconds for a moving drone.
If the drone stops sending CoT (crash, link loss, battery dead),
the icon disappears from the map after the stale time. This is
correct behavior — a stale position is worse than no position.

**5. Test with ATAK first.** Install ATAK on an Android phone,
connect to the same network as your CoT sender, and verify the
icon appears. Don't integrate with a TAK Server until direct
UDP works.

**6. CoT type codes matter.** Using the wrong type code means your
drone shows up as a ground vehicle, or a hostile, or a waypoint.
Get the type code right for your affiliation and platform type.

---

## Next

- **Chapter 14: Mesh Radios** — the transport that carries CoT
  from the drone to the TAK ecosystem.
- **Chapter 13: Adding a Companion Computer** — the platform that
  generates CoT from flight controller data.

---

*TAK is a shared map. Your drone belongs on it. One UDP packet
puts it there. Everything else is refinement.*
