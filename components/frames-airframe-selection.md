# Frames & Airframe Selection

> The frame is the skeleton of every build. It determines what props you can
> run, how your stack mounts, where your antenna exits, how you handle crashes,
> and how much your quad weighs before you bolt a single component onto it.
> Frame choice affects vibration, durability, repairability, and ultimately
> flight feel more than most pilots realize.

**Forge DB:** 349 frames across 15+ manufacturers
**Cross-references:** [Propulsion Matching](propulsion-system-matching.md) ·
[ESCs](escs.md) · [Flight Controllers](flight-controllers.md) ·
[PID Tuning](../field/pid-tuning.md) · [Preflight](../field/preflight.md)

---

## Frame Sizing

Frame size is defined by the maximum propeller diameter it accepts, which
in turn determines motor size, battery capacity, and mission profile.

| Size | Prop | Typical Use | AUW Range | Stack |
|------|------|-------------|-----------|-------|
| 3" / 3.5" | 3–3.5" | Indoor, cinewhoop, tight spaces | 150–250 g | 20×20 mm |
| 5" | 5–5.1" | Freestyle, racing, general FPV | 500–750 g | 30.5×30.5 mm |
| 6" | 6" | Long range, cruising | 600–900 g | 30.5×30.5 mm |
| 7" | 7" | Long range, payload, strike | 800–1400 g | 30.5×30.5 mm |
| 10" | 10" | Heavy lift, payload delivery, bomber | 1500–4000 g | 30.5×30.5 mm |

The 5-inch class dominates the hobby and consumer market. The 7-inch and
10-inch classes dominate military/tactical use because they carry meaningful
payloads and fly longer on larger batteries.

---

## Frame Geometry

### True X vs Squashed X vs Deadcat

**True X** — all arms at 45° angles from center. Equal prop wash distribution,
symmetrical yaw authority. Standard for freestyle and racing. Most 5-inch
frames use this layout.

**Squashed X** — front arms closer together, rear arms wider (or vice versa).
Keeps props out of camera FOV. Popular for cinematic builds where you want
clean HD footage without prop-in-frame. Slight asymmetry in yaw response but
negligible with modern PID tuning.

**Deadcat** — rear arms angled sharply outward, front arms close together.
Maximum camera clearance, props completely out of frame. Common on cinewhoops
and some long-range builds. Trades some flight efficiency for clean video.

### Stretched X

Arms angled so front-to-back distance is longer than side-to-side. Improves
forward flight efficiency and pitch authority. Popular for long-range and
racing. The tradeoff is reduced roll authority and slightly more complex PID
tuning.

### H-Frame / Box Frame

Arms parallel, creating a rectangular or square footprint. Structurally strong,
easy to mount payloads and electronics. Common in utility/payload drones and
some cinewhoops (ducted). Less aerodynamically efficient than X layouts but
simpler to build and repair.

---

## Materials

### Carbon Fiber

The standard for performance frames. Unmatched stiffness-to-weight ratio.
Typical thickness: 2–5 mm for arms, 1.5–2 mm for top/bottom plates.

Key considerations: carbon fiber is electrically conductive — it can short
exposed pads and interfere with RF. Always insulate between carbon and
electronics. Carbon also blocks GPS and some antenna signals, so antenna
placement matters.

Quality varies enormously. Cheap carbon can delaminate on impact. Premium
manufacturers (Armattan, ImpulseRC, Lumenier) use higher-quality layups that
hold together better in crashes.

### 3D Printed (TPU / PETG / Nylon)

Common for cinewhoop ducts, GoPro mounts, antenna holders, and
custom parts. TPU is flexible and absorbs impacts well. Full 3D-printed
frames exist for lightweight or disposable builds. Military FPV production
(FPV_VYZOV and others) uses 3D-printed components extensively for rapid
iteration.

### Aluminum / CNC

Used in some commercial/industrial frames. Heavier than carbon but
machinable and repairable. Common in larger payload platforms. Can be bent
back into shape after impacts that would shatter carbon.

---

## Stack Mounting

Most FPV frames use standardized mounting hole patterns:

| Pattern | Hole Spacing | Used By |
|---------|-------------|---------|
| 20×20 mm | M2 or M3 | Micro builds, 3" and smaller |
| 25.5×25.5 mm | M2 or M3 | Some whoop/micro FCs |
| 30.5×30.5 mm | M3 | Standard 5"+ builds |

The 30.5 mm pattern is dominant for anything 5-inch and above. Stack mounting
uses standoffs (typically nylon or aluminum) between layers: bottom plate →
ESC → FC → VTX → top plate.

**Soft mounting** — rubber grommets or O-rings on FC mounting screws to isolate
the gyro from frame vibration. Critical for clean PID performance. Some frames
include soft-mount provisions; others require aftermarket grommets.

---

## Arm Design

### Unibody vs Replaceable Arms

**Unibody** — arms are integral to the bottom plate, cut from a single piece
of carbon. Lightest, stiffest, but if one arm breaks you replace the entire
bottom plate.

**Replaceable arms** — individual arms bolt to a center section. Heavier (more
hardware) but you only replace the broken arm. Significant advantage for
training and attritable military use where crash frequency is high.

**Dead cat with replaceable arms** — common pattern for 7" and 10" builds
where crashes are expensive. UAS Nexus Platform One uses this approach.

### Arm Thickness

Thicker arms resist bending but add weight. Typical ranges:

- 4 mm — standard freestyle 5"
- 5 mm — heavy freestyle, 7" builds
- 6 mm — 10" and heavy lift

Carbon fiber grain direction matters — arms with fibers aligned along the
length are stiffer in bending but can split along the grain on impact. Cross-
weave layups distribute stress better.

---

## Durability & Repairability

The number one factor in frame selection for high-volume operations (training,
military, commercial) is how fast you can get back in the air after a crash.

**Armattan** — lifetime warranty on carbon. If you break an arm, they replace
it. Unusual in the industry and worth noting for training programs.

**ImpulseRC** — replaceable arms on most frames (Apex series). Well-documented
hardware kits.

**TBS Source One** — open-source frame design. Anyone can cut the carbon from
the published DXF files. Ensures long-term parts availability even if the
manufacturer disappears.

For military/attritable use, the trend is toward simple, easily manufactured
frames with replaceable arms and minimal unique hardware. Ukrainian FPV
production prioritizes frames that can be assembled quickly with standard
hardware.

---

## Camera Mount & Protection

Most FPV frames include a camera mount at a fixed or adjustable angle
(typically 0–60°). Key considerations:

- **TPU camera mount** — absorbs vibration, protects camera in crashes, but
  can introduce jello in video if too flexible
- **Fixed carbon mount** — stiffer, better for HD video, but transmits crash
  forces directly to the camera
- **Adjustable tilt** — essential for builds that switch between cruising
  (low angle) and racing/freestyle (high angle)
- **Camera protection** — top-mounted GoPro or action cam needs a cage or TPU
  mount. Naked action cams (board-only, no case) save weight but are fragile.

---

## Antenna Routing

Frame choice affects antenna placement, which affects link quality:

- **Rear antenna exit** — most common for control link (ELRS/Crossfire
  receiver antenna). Route the antenna out the back, away from carbon and
  motors. T-antenna or immortal-T mount on a standoff.
- **Top-mount VTX antenna** — keeps the VTX antenna vertical and above the
  frame. SMA or MMCX pigtail through the top plate.
- **GPS placement** — must be on top, away from carbon (which blocks satellite
  signals) and away from power wiring (which creates magnetic interference for
  the compass).

Carbon fiber frames attenuate RF signals. Never sandwich an antenna between
carbon plates. The antenna must have a clear path to the sky/receiver.

---

## Frame Selection Decision Tree

1. **What size props do you need?** → determines frame class
2. **Freestyle or long range or payload?** → determines geometry (True X vs
   Stretched X vs Deadcat)
3. **How often will you crash?** → replaceable arms vs unibody
4. **What stack size?** → 20×20 or 30.5×30.5
5. **HD camera mount needed?** → check GoPro/action cam compatibility
6. **Weight target?** → compare frame-only weights (lighter frame = more
   battery capacity within AUW budget)

---

## Notable Manufacturers in Forge

| Manufacturer | Count | Known For |
|-------------|-------|-----------|
| Lumenier | 75 | QAV series, premium carbon, wide range |
| iFlight | 20 | Nazgul/Chimera, integrated designs |
| Diatone | 16 | Budget-friendly, Roma series |
| GEPRC | 15 | Mark/Cinelog series, clean builds |
| Armattan | 10 | Lifetime warranty, Badger/Rooster |
| ImpulseRC | 10 | Apex series, replaceable arms |
| TBS | varies | Source One (open source) |
| PIRAT | 8 | Ukrainian FPV combat frames |

---

## Sources

- Forge parts database (349 frames)
- Oscar Liang, frame selection guides
- Manufacturer specifications and DXF files
- Ukrainian FPV production documentation
