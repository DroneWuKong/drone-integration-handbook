# UTM and Airspace Awareness Stack

Before you fly anywhere near controlled airspace, you need to know what airspace you're in, whether authorization is required, what restrictions are active, and how to file your intent. This guide covers the full airspace awareness stack — from the apps on your phone to the UTM infrastructure being built for BVLOS.

---

## The Authorization Hierarchy

Not all airspace requires the same process. The FAA classifies airspace into classes, and each has different authorization requirements for drones.

| Airspace Class | What It Is | Drone Authorization |
|---|---|---|
| Class G (uncontrolled) | Below 700ft AGL in most rural areas | No authorization needed (under 400ft AGL) |
| Class E (controlled) | Most of the NAS above 1,200ft; some areas from surface | No authorization at surface E; LAANC or DroneZone above |
| Class D | Airspace around smaller towered airports (typically 5nm, SFC–2,500ft) | LAANC authorization required |
| Class C | Airspace around medium airports (typically 5–10nm, SFC–4,000ft) | LAANC authorization required |
| Class B | Airspace around major airports (multi-layer, 0–10,000ft) | LAANC authorization required; more restrictive |
| Class A | IFR airspace, 18,000–60,000ft MSL | No drone operations |
| Prohibited/Restricted | Military, national security, etc. | Special authorization or prohibited entirely |
| TFRs | Temporary Flight Restrictions | Check before every flight |

**The key tool for class D/C/B authorization is LAANC.** The Low Altitude Authorization and Notification Capability is an automated system that grants near-instant authorization (typically within 30–90 seconds) in pre-approved UAS Facilities Map (UASFM) grids.

---

## LAANC: The Standard Authorization Tool

### What LAANC Does

LAANC grants automated Part 107 authorization to fly in controlled airspace at or below the altitude shown on the UAS Facilities Map. The UASFM shows a grid overlaid on controlled airspace, with each grid cell showing a maximum altitude (0ft, 100ft, 200ft, 400ft) where automated authorization is available.

Authorization is near-instant (typically under 2 minutes), tied to your FAA registration number, and valid for the time window and location you specified.

### LAANC Access

LAANC is available through FAA-approved USS providers via their apps:
- **AiRHub** — popular in commercial sector; web + mobile
- **Aloft (formerly Kittyhawk)** — popular with enterprise operators
- **Skydio Cloud** — integrated with Skydio aircraft
- **DroneDeploy** — primarily for mapping workflows
- **Wing Pilot** — Wing Aviation's app, includes free airspace awareness
- **Garmin Pilot** — for pilots who use Garmin EFB already
- **ForeFlight** — integrated with EFB workflows

All of these connect to the FAA's LAANC backend. Authorization from any of these is equally valid.

### What LAANC Doesn't Cover

- **Above UASFM altitude:** If the UASFM shows 100ft and you need 200ft, you must use DroneZone manual authorization (5-day minimum wait).
- **Class B airspace with 0ft UASFM altitude:** This means automated authorization is not available at all altitudes in that cell — you need a manual DroneZone authorization.
- **TFRs:** LAANC does not override active TFRs. Even with LAANC authorization, a TFR in effect makes flight unlawful.
- **BVLOS:** LAANC is for VLOS Part 107 operations only. BVLOS requires a waiver or Part 108 Permit.

---

## Pre-Flight Workflow: What to Check

**Every flight, without exception:**

1. **TFRs** — tfr.faa.gov or any LAANC app. TFRs can appear with little notice (VIP movement, emergency response, large events). A presidential TFR covers ~10nm radius and is a federal crime to violate.

2. **NOTAMs** — notams.faa.gov. Relevant to your airspace and route. UAV-specific NOTAMs (NOTAM type D) are most relevant; also check general airspace NOTAMs for your area.

3. **Airspace class** — is authorization required? Which tool do you use?

4. **UASFM altitude** — if in controlled airspace, what's the authorized altitude ceiling for automated approval?

5. **Weather** — Part 107 requires 3 statute miles visibility minimum and 500ft below clouds. Check wind at altitude, not just surface.

**For BVLOS operations, additionally:**
6. File a UAS NOTAM via DroneZone
7. Coordinate with the ADSP (once Part 108 infrastructure is in place)
8. Confirm C2 link coverage for the planned corridor

---

## Ground Control Station Software

### Mission Planner

Windows-native, most feature-complete for ArduPilot. Key airspace-relevant features:
- **ArcGIS / Google satellite layers** — visualize terrain and obstacles
- **Geofence editor** — define operational area boundaries; ArduPilot enforces these in firmware
- **NOTAM overlay via 3rd party plugins** — Herelink or FAA data feeds
- **Corridor planning** for BVLOS linear missions

Configuration:
```
# Enable geofence enforcement
FENCE_ENABLE = 1
FENCE_TYPE = 7        # All fence types (polygon + altitude + circle)
FENCE_ACTION = 1      # RTL on breach
FENCE_ALT_MIN = 0     # Minimum altitude (0 = surface)
FENCE_ALT_MAX = 120   # Maximum altitude (meters AGL)
```

### QGroundControl (QGC)

Cross-platform (Windows/Mac/Linux/iOS/Android). More approachable than Mission Planner, works with both ArduPilot and PX4. Key airspace features:
- **Airmap integration (legacy)** — basic airspace overlay
- **Geofence editor** — similar to Mission Planner
- **Survey and corridor mission tools** — optimized flight paths for mapping

QGC is better for operators who work across platforms or need a mobile GCS.

### UgCS

Designed for professional survey and inspection workflows. Key differentiators:
- **Terrain following** — automatically adjusts altitude to maintain AGL height over varying terrain (uses SRTM or custom DEM data)
- **Corridor planning** — linear corridor missions for pipeline, power line, road inspection
- **Virtual terrain 3D view** — preview the planned flight path against terrain
- **DJI, ArduPilot, PX4 support** — single GCS for mixed fleets

UgCS is the professional standard for corridor and terrain-following missions. It's not free ($500+/year for commercial license) but the terrain following alone justifies it for complex terrain operations.

---

## UTM: What It Is and How It's Evolving

UTM (UAS Traffic Management) is the digital infrastructure that will eventually manage drone traffic the way air traffic control manages manned aviation — but without human controllers, using automated coordination.

The core UTM services:

| Service | What It Does |
|---|---|
| **Airspace awareness** | Know where flight is and isn't permitted, in real time |
| **Flight planning** | File intent, request authorization, check for conflicts |
| **Conformance monitoring** | Detect when a drone deviates from its planned flight |
| **Deconfliction** | Separate planned flights from each other in time/space |
| **Dynamic airspace configuration** | Respond to TFRs, emergencies, airspace changes |

**Current state (2026):**
The FAA's LAANC covers airspace authorization. Remote ID provides identification. But the deconfliction and conformance monitoring services — the ones that enable multiple BVLOS operators in the same airspace — are still being built. The Part 108 ADSP (Automated Data Service Provider) framework is the regulatory foundation; the technical standards and certified providers are in development.

**Near-term expectation:**
Part 108 Permits will require filing flight intent with an FAA-approved ADSP before BVLOS operations. This filing will:
- Register your planned flight path and time window
- Check for conflicts with other filed flights
- Return a "de-conflicted corridor" or flag conflicts for resolution
- Enable conformance monitoring during the flight

**European U-Space:**
The EU has a more structured UTM framework (U-space, under EASA Regulations EU 2021/664–666). U-space is operational in several EU member states and requires drone operators to use certified USSPs (U-space Service Providers) for most operations. U-space is more mature than the US UTM framework and offers a preview of what the US system may look like.

---

## Digital Notice to Airmen (NOTAM) and DroneZone

For any operation that requires manual FAA authorization (above UASFM altitude, BVLOS, Class B full coverage), use the FAA DroneZone portal (droneconnect.faa.gov).

**Authorization types available via DroneZone:**
- **Part 107 Airspace Authorization** — manual review, 90-day processing time, for operations not covered by LAANC
- **Part 107 Waivers** — for BVLOS, night (pre-2021), operation over people; 6–18 month review
- **UAS NOTAM filing** — file a voluntary NOTAM for any UAS operation; required for BVLOS operations and useful for public safety coordination

**UAS NOTAM best practice:**
File a UAS NOTAM for any operation over 400ft AGL, any BVLOS operation, and any operation near an airport even if LAANC-authorized. A filed NOTAM ensures ATC is aware of your operation and protects you in an airspace conflict investigation.

---

## Integrating Airspace Data into the Flight Stack

For automated and autonomous operations, airspace data should flow into the aircraft's geofence, not just the pilot's phone.

**ArduPilot dynamic fences:**
ArduPilot's geofence system can be updated in flight via MAVLink. A companion computer with airspace API access can:
1. Pre-flight: query airspace API (OpenAIP, AirHub, FAA UDDS) for restrictions in the operation area
2. Convert restrictions to ArduPilot fence polygons
3. Upload fences to FC before departure
4. Monitor for TFR activations and update fences dynamically in flight

**Open data sources:**
- **FAA UDDS (UAS Data Delivery Service):** Free API for authorized airspace, FRIAs, UAS Facility Maps
- **OpenAIP:** Global airspace data, free for non-commercial, API available
- **Airmap/Kittyhawk:** Commercial APIs with global coverage
- **SkyVector:** Web-based, good for visual planning (not for programmatic access)

**ArduPilot fence upload via MAVLink:**
```python
# Upload an exclusion fence polygon via MAVSDK
await drone.param.set_param_int('FENCE_ENABLE', 1)
# Upload polygon vertices via MAVLink MISSION_ITEM_INT
# type = MAV_CMD_NAV_FENCE_POLYGON_VERTEX_EXCLUSION
```

This integration pattern — dynamic airspace to dynamic fence — is the technical foundation for automated Part 108-compliant BVLOS operations. The regulatory infrastructure (ADSPs, certified APIs) is still maturing, but the aircraft-side implementation can be built now.
