# UTM and Airspace Awareness Stack

Before you fly anywhere near controlled airspace, you need to know what airspace you're in, whether authorization is required, what restrictions are active, and how to file your intent. This guide covers the full airspace awareness stack — from the apps on your phone to the UTM infrastructure being built for BVLOS.

---

## The Authorization Hierarchy

Not all airspace requires the same process. The FAA classifies airspace into classes, and each has different authorization requirements for drones.

| Airspace Class | What It Is | Drone Authorization |
|---|---|---|
| Class G (uncontrolled) | Below 700ft AGL in most rural areas | No authorization needed (under 400ft AGL) |
| Class E (controlled) | Most of the NAS above 1,200ft; some areas begin at the surface | Authorization is required within the lateral boundaries of Class E airspace designated for an airport; use an available FAA authorization channel |
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

LAANC is available through FAA-approved UAS Service Suppliers. Use the FAA's current provider list rather than relying on a static vendor list in this handbook. Near-real-time requests can be made on the flight date; Part 107 further-coordination requests above the mapped altitude and below 400 feet must be submitted at least 72 hours before the requested start time and may be submitted up to 90 days in advance. [claim:reg-laanc-scope]

### What LAANC Doesn't Cover

- **Above UASFM altitude:** Part 107 pilots may use LAANC further coordination for requests above the mapped value and at or below 400 feet where the service is available; other requests use the FAA's applicable manual authorization channel.
- **Class B airspace with 0ft UASFM altitude:** This means automated authorization is not available at all altitudes in that cell — you need a manual DroneZone authorization.
- **TFRs:** LAANC does not override active TFRs. Even with LAANC authorization, a TFR in effect makes flight unlawful.
- **BVLOS:** LAANC airspace authorization does not itself authorize BVLOS. Use a currently available waiver, certificate, exemption, or other FAA approval applicable to the operation; the proposed Part 108 framework is not current operating authority.

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
7. Follow any third-party-service conditions in the actual operating approval; ADSP requirements remain part of the proposed Part 108 framework
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
The FAA's LAANC covers certain airspace authorizations, and Remote ID provides identification information. Broader deconfliction and conformance-monitoring services are still developing. The proposed Part 108 ADSP (Automated Data Service Provider) framework describes one possible regulatory structure; it is not current operating authority.

**Near-term expectation:**
The Part 108 proposal describes filing flight intent through an approved ADSP for covered operations. A future final rule and approved service would determine the actual workflow. Proposed functions include:
- Register your planned flight path and time window
- Check for conflicts with other filed flights
- Return a "de-conflicted corridor" or flag conflicts for resolution
- Enable conformance monitoring during the flight

**European U-Space:**
The EU has a more structured UTM framework (U-space, under EASA Regulations EU 2021/664–666). U-space is operational in several EU member states and requires drone operators to use certified USSPs (U-space Service Providers) for most operations. U-space is more mature than the US UTM framework and offers a preview of what the US system may look like.

---

## Digital Notice to Airmen (NOTAM) and DroneZone

Use the FAA's current application channel for the authority requested. Part 107 operational waivers now begin in the Aviation Safety Hub; Part 107 airspace authorizations remain in FAADroneZone until the FAA announces otherwise. [claim:reg-part107-application-channel]

An authorization, waiver, and NOTAM serve different purposes. Follow the conditions in the actual authorization, waiver, COA, or exemption and check current NOTAMs and TFRs. Do not assume filing a notice grants operating authority or changes a regulatory limit.

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

This integration pattern—dynamic airspace to dynamic fence—is a useful engineering concept for a future BVLOS approval. It is not evidence of Part 108 compliance, and any aircraft-side implementation must remain a test feature until accepted data services and an operating authorization define its role.
