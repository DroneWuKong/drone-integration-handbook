# Thermal & Night FPV Operations

> Night-capable FPV changed the war. Ukrainian units like Wild Hornets'
> "Night Hornets" team pioneered night strikes using low-lux cameras and
> IR illumination. Both sides now operate 24-hour FPV cycles. This guide
> covers the operator-level knowledge for flying FPV in darkness — camera
> selection, IR integration, OSD configuration, cold-weather battery
> management, and the operational patterns that work at night.

**Cross-references:** [FPV Cameras](../components/fpv-cameras.md) ·
[Thermal Cameras](../components/thermal-cameras.md) ·
[Video Transmitters](../components/video-transmitters-vtx.md) ·
[Batteries](../components/batteries.md) ·
[EW Countermeasures](ew-countermeasures.md)

---

## Night Vision Tiers

Not all "night capable" is equal. There are three distinct tiers of
night FPV capability, each with different hardware and operational
tradeoffs.

### Tier 1: Low-Lux Analog Camera (Passive)

The simplest approach. Use a camera with very low minimum illumination
and rely on ambient light — moonlight, starlight, urban glow, fires.

| Camera | Min Lux | Sensor | Notes |
|--------|---------|--------|-------|
| Foxeer Cat 4 | 0.0001 lux | 1/2" CMOS | Best-in-class low light |
| Caddx Ratel 2 | 0.01 lux | 1/1.8" CMOS | Good low light |
| Orqa Justice | 0.01 lux | 1200TVL | Standard MRM camera |
| RunCam Night Eagle 3 | 0.0001 lux | 1/2" | Mono (B&W), max sensitivity |

**Key insight:** "Starlight" cameras (0.0001 lux) can see under moonlight
and urban ambient conditions. They cannot see in total darkness (cave,
deep forest canopy, moonless overcast). For total darkness you need
active illumination (Tier 2) or thermal (Tier 3).

**Color vs mono:** some cameras switch to black-and-white mode in low
light to maximize sensitivity. Mono cameras like the RunCam Night Eagle
are always B&W but extract maximum photons. Color is useless at night —
accept the mono image.

### Tier 2: Low-Lux Camera + IR Illuminator (Active)

Add an infrared LED illuminator to the drone. The camera sees IR
reflected off objects. Works in total darkness but the IR emission
is detectable by enemy night vision equipment.

**IR illuminator specs:**

| Parameter | Typical Value |
|-----------|--------------|
| Wavelength | 850 nm (faint red glow, visible to NVG) or 940 nm (invisible) |
| Power | 1-5W LED |
| Weight | 3-15 g |
| Beam angle | 30-60° (match to camera FOV) |
| Power source | Flight battery via BEC (3.3V or 5V) |

**850 nm vs 940 nm:** 850 nm produces a faint red glow visible to the
naked eye at close range and bright to any NVG. 940 nm is invisible to
the eye and dim to Gen 2 NVG, but cameras are less sensitive to it —
shorter effective range. Choose based on threat: 940 nm if operating
near enemy with NVG, 850 nm if detection risk is low.

**Mounting:** mount the IR LED below or beside the camera, angled to
illuminate the camera's field of view. Avoid mounting above — downwash
from props can vibrate the illuminator and cause flickering on video.

**Wiring:** most IR LEDs run on 3.3V or 5V DC. Wire to a spare BEC
output or directly to a regulated pad on the FC. Use a switch channel
(AUX) to toggle IR on/off in flight — the pilot should be able to kill
the IR if detection risk increases.

### Tier 3: Thermal Camera (Passive, All-Conditions)

Thermal (LWIR) cameras detect heat radiation, not light. They work in
complete darkness, through smoke, and in conditions where optical cameras
are blind. But they produce low-resolution imagery with no texture detail
— you see heat signatures, not visual features.

**For thermal camera hardware, see:** [Thermal Cameras](../components/thermal-cameras.md)

**FPV integration:** most thermal cameras output analog composite video
(PAL/NTSC) that connects directly to the VTX like any other FPV camera.
Some output digital (USB/MIPI) and require a companion computer to
convert to analog for the VTX.

**Thermal + optical dual feed:** some operators run two cameras — a
thermal for detection and a low-lux optical for the final approach.
Switch between feeds via an AUX channel controlling a video switcher.
This requires two camera inputs and a video switch module, adding weight
and complexity.

---

## OSD Configuration for Night

The OSD must be readable at night without overwhelming the pilot's
dark-adapted vision.

### Brightness and Contrast

- **Reduce OSD brightness** if your OSD chip supports it. Standard
  daytime OSD brightness is blinding on a night low-lux feed.
- **Use minimal OSD elements** — only what you need: battery voltage,
  LQ/RSSI, altitude/distance, heading, flight mode. Remove decorative
  elements, timers, and non-critical data.
- **Position OSD elements at edges** — keep the center of the image
  clear for target identification.

### Critical Night OSD Elements

| Element | Why |
|---------|-----|
| Battery voltage (per cell) | Cold batteries sag faster — monitor closely |
| LQ / RSSI | Link health awareness is critical when you can't see the drone |
| Distance to home | You can't estimate distance visually at night |
| Heading | No visual landmarks — compass heading is primary nav |
| Altitude | No visual altitude reference at night |
| Flight mode | Know immediately if GPS drops you to ANGLE |

### Goggle Settings

- **Reduce goggle brightness** to minimum comfortable level. Your
  pupils need to stay dilated for the low-lux feed.
- **If using OLED goggles (Orqa FPV.One):** OLED blacks are true black,
  which helps low-lux contrast. LCD goggles have backlight bleed that
  washes out dark scenes.
- **DVR recording:** always record. Night footage is harder to review
  in real-time — DVR lets you analyze after landing.

---

## Cold Weather Battery Management

Night operations often mean cold operations. Battery performance
degrades significantly below 10°C and becomes dangerous below 0°C.

### LiPo Cold Behavior

| Temperature | Effect |
|-------------|--------|
| 20°C+ | Normal performance |
| 10-20°C | 5-15% capacity reduction |
| 0-10°C | 15-30% capacity reduction, increased voltage sag |
| Below 0°C | 30-50% capacity loss, risk of cell damage under load |

### Field Practices

- **Pre-warm batteries** before flight. Keep them in an insulated bag
  with hand warmers. Target 20-25°C at launch.
- **Reduce flight time estimates by 20-30%** in cold conditions.
  A battery that gives 8 minutes at 20°C may give 5-6 minutes at 5°C.
- **Monitor voltage sag under load** — cold batteries sag harder.
  If voltage per cell drops below 3.3V under throttle, land immediately.
  Cold sag can recover when the battery warms up, but pushing a cold
  battery risks permanent cell damage.
- **Land with more reserve** than daytime. 3.5V/cell landing voltage
  instead of the typical 3.3V/cell.
- **Don't charge cold batteries.** Charging below 5°C causes lithium
  plating and permanent capacity loss. Warm the battery above 10°C
  before charging.

---

## Night Operational Patterns

### Launch and Recovery

- **Mark the launch site** with an IR chemlight or low-power IR LED
  visible to your goggles but not to naked eye. You need to find home
  in the dark.
- **Launch vertically, climb to safe altitude before translating.**
  Obstacles invisible at night are at ground level.
- **Recovery approach:** use GPS distance and heading on OSD to navigate
  back to launch. Descend slowly — you cannot judge ground proximity
  visually on a low-lux feed. Consider a dedicated landing camera
  (downward-facing) if the platform supports it.

### Navigation

- **Fly by instruments, not visuals.** At night, the camera feed gives
  situational awareness but not reliable distance/altitude perception.
  Trust your OSD heading, altitude, and distance readouts.
- **Use GPS waypoints** if firmware supports them (iNav, ArduPilot).
  Pre-plan the route with waypoints at known positions. The OSD will
  guide you between points.
- **Terrain awareness:** if operating in terrain with elevation changes,
  know the terrain profile before launch. AGL (above ground level) can
  differ significantly from altitude over the launch site.

### Target Engagement (Strike)

- **IR illuminator on for final approach only.** Fly dark to the target
  area using ambient light, then activate IR for the last 200-500m
  when you need precision.
- **Thermal for detection, optical for terminal.** If running dual
  cameras, use thermal to locate the target (heat signature stands out
  at range), then switch to low-lux optical for the final approach
  where you need texture/shape detail for positive identification.
- **Video frequency at night:** enemy ELINT may be lower priority at
  night, but your VTX emission is still detectable. Consider reduced
  VTX power or non-standard frequencies for night operations where
  stealth matters.

---

## Hardware Checklist: Night Build

| Component | Requirement | Notes |
|-----------|------------|-------|
| Camera | 0.01 lux or better | Foxeer Cat 4 or RunCam Night Eagle class |
| VTX | Standard analog or digital | No special requirement |
| IR illuminator | 850 or 940 nm, 1-5W | Optional (Tier 2) |
| IR switch | AUX channel toggle | On/off control from TX |
| Battery | Pre-warmed, insulated | Cold management critical |
| OSD | Minimal config, reduced brightness | Heading, altitude, distance, battery, LQ |
| Goggles | Brightness adjustable | OLED preferred for contrast |
| DVR | Always recording | Post-flight analysis essential |
| Launch marker | IR chemlight or LED | Invisible to naked eye |
| GPS | Required | Primary navigation at night |

---

## Sources

- Wild Hornets, Night Hornets team operational reporting
- TAF Industries, Kolibri 10 thermal variant specs
- Oscar Liang, low-light FPV camera reviews
- LiPo cold weather performance studies
- Ukrainian FPV operator training materials (public)
