# FPV Cameras

> The FPV camera is the pilot's eyes. It determines what you see, how fast
> you see it, and whether you can fly in low light. Camera choice is tightly
> coupled to your video system — analog cameras don't work with digital VTX
> systems and vice versa. Getting this wrong means a black screen.

**Forge DB:** 193 FPV cameras
**Cross-references:** [Video Transmitters](video-transmitters-vtx.md) ·
[Antennas](../fundamentals/antennas.md) ·
[Frames](frames-airframe-selection.md) ·
[Sensor Payloads](sensor-payload-integration.md) ·
[Thermal Cameras](thermal-cameras.md)

---

## Analog vs Digital

### Analog FPV

The original and still most common FPV system. The camera outputs a composite
video signal (NTSC or PAL) directly to an analog VTX, which broadcasts it on
5.8 GHz (or 1.2/1.3 GHz for long range). The receiver in your goggles
demodulates and displays it.

**Strengths:** lowest possible latency (sub-1ms camera-to-screen is
achievable), cheapest, lightest, enormous selection of cameras from many
manufacturers, field-repairable, no firmware dependencies.

**Weaknesses:** resolution capped at ~700 TVL effective, no encryption
(anyone with a receiver on the same frequency sees your feed — critical
vulnerability in contested environments), susceptible to interference and
multipath, image quality degrades with distance rather than cutting out
cleanly.

**Resolution is measured in TV lines (TVL)**, not pixels. Higher TVL =
sharper image. Most modern analog cameras are 1200 TVL or higher, but the
actual displayed resolution is limited by the analog transmission standard.

### Digital FPV Systems

Digital systems encode the video into a data stream, transmit it digitally,
and decode it in the goggles. The four major systems:

**DJI O3 / O4 Pro** — highest image quality, 1080p or higher, 50ms typical
latency. O4 Pro is the newest generation. Locked ecosystem — only works with
DJI goggles. Most expensive. Dominant in the prosumer market.

**Walksnail Avatar** — Caddx/Walksnail system, 1080p capable, comparable
latency to DJI. Works with Walksnail and some compatible goggles. More open
than DJI but still a proprietary ecosystem.

**HDZero** — unique approach: digital transmission with analog-like latency
(sub-4ms). 720p max resolution currently. Open protocol — works with multiple
goggle brands. Preferred by racers who need minimum latency. The camera
modules tend to be smaller and lighter.

**OpenHD / WifiBroadcast** — open-source digital video over WiFi hardware.
Runs on Raspberry Pi or IP camera boards (OpenIPC). Fully customizable
frequencies, encryption possible, but higher latency (80–150ms) and more
complex setup. See [OpenHD Implementation Guide](openhd-implementation-guide.md).

---

## Key Camera Specifications

### Sensor Size

Larger sensors capture more light. Common FPV camera sensor sizes:

- **1/4"** — smallest, used in micro/whoop cameras. Adequate in daylight,
  poor in low light.
- **1/3"** — standard for most FPV cameras. Good balance of size, weight,
  and light sensitivity.
- **1/2"** — larger sensor, better low-light performance. Found in premium
  cameras like the Foxeer Cat series (marketed as "Starlight").
- **1/1.8" and larger** — typically found in HD recording cameras (action
  cams), not FPV feed cameras.

### Sensor Type

**CMOS** — standard for FPV. Fast readout, low power. All modern FPV cameras
are CMOS.

**Global shutter vs rolling shutter** — most FPV cameras use rolling shutter,
which can produce jello artifacts from vibration. Global shutter cameras
(rare in FPV) read the entire frame at once, eliminating jello but at higher
cost and power.

### Minimum Illumination (Lux)

How well the camera sees in the dark. Lower = better night vision.

- **0.01 lux** — excellent low light (Foxeer Cat 4, Caddx Ratel 2)
- **0.1 lux** — good low light
- **1.0 lux** — daytime only

Night-capable cameras are critical for military FPV operations. Ukraine
pioneered night FPV strikes using low-lux cameras paired with IR illumination.
"Night Hornets" (Wild Hornets) is one of the most active night FPV units.

### Field of View (FOV)

Measured in degrees. Wider FOV = more situational awareness but more
distortion at edges.

- **120°+** — ultra-wide, good for proximity freestyle and racing
- **150°–170°** — typical FPV range, balances awareness and usability
- **180°+** — fisheye, maximum awareness but significant barrel distortion

Most FPV cameras offer a fixed lens with FOV determined by the lens focal
length. Some cameras offer replaceable lenses.

### Aspect Ratio

**4:3** — traditional FPV aspect ratio. More vertical field of view. Preferred
for freestyle where you need to see above and below.

**16:9** — widescreen. More horizontal coverage. Standard for digital systems
and HD recording. Some pilots prefer this for racing.

**Switchable** — many cameras support both via OSD menu.

---

## Camera Sizing

FPV cameras come in standardized mounting sizes:

| Size | Dimensions | Typical Use |
|------|-----------|-------------|
| Nano | 14×14 mm | Tiny whoops, micro builds |
| Micro | 19×19 mm | 3" builds, compact 5" builds |
| Mini | 21×21 mm | Some 5" builds |
| Full / Standard | 28×28 mm | 5"+ builds, maximum image quality |

The mounting hole pattern must match your frame's camera mount. Most frames
specify which camera sizes they accept. Adapter plates exist for mismatched
sizes.

---

## Analog Camera Selection

The analog camera market is mature with well-understood options:

**Budget (sub-$15):** Foxeer Razer, Caddx Ant — adequate for daylight flying,
limited low-light performance. Good for training builds.

**Mid-range ($15–30):** RunCam Phoenix 2, Caddx Ratel 2 — excellent all-around
performers. Good low light, reliable. The workhorse tier.

**Premium ($30+):** Foxeer Cat 4 (1200 TVL, 0.0001 lux claimed), Caddx Polar
series — best low-light performance. The "starlight" category. Essential for
dawn/dusk/night operations.

### OSD Compatibility

Most analog cameras can overlay OSD data (battery voltage, RSSI, flight mode)
via connection to the FC's OSD output. The FC generates the OSD overlay and
mixes it into the video signal before it reaches the VTX. This is handled by
the FC firmware (Betaflight OSD, iNav OSD, etc.), not the camera.

---

## Digital Camera Selection

Digital cameras are paired to their respective ecosystems:

**DJI O4 Pro Camera Unit** — integrated camera + VTX. You don't choose the
camera separately — it's part of the air unit. Highest quality, but you're
locked into the DJI ecosystem.

**Walksnail Avatar cameras** — separate camera modules that connect to a
Walksnail VTX board. More modularity than DJI. Multiple camera options
(standard, micro, board camera).

**HDZero cameras** — Nano-series cameras designed for minimum latency.
Micro and nano sizes available. The lightest digital camera option, important
for racing and weight-sensitive builds.

---

## Camera Durability

FPV cameras take impacts. Key durability considerations:

- **Lens protection** — some cameras have replaceable lenses. A cracked lens
  is a common crash result. Replaceable = back in the air faster.
- **Housing material** — metal housings survive impacts better than plastic.
  Most quality cameras use aluminum or CNC housings.
- **Connector type** — JST-SH connectors are fragile. Cameras with solder
  pads or more robust connectors survive crashes better.
- **Conformal coating** — protects the PCB from moisture and debris. Important
  for field operations.

---

## Military / Contested Environment Considerations

In the context of the Russo-Ukrainian War, FPV camera selection has become
a tactical decision:

**Analog video interception** — any analog camera feed can be intercepted by
enemy receivers. Russian forces use purpose-built video signal detectors
(Chuyka 3.0) that scan 900–6000 MHz and display intercepted video feeds in
real time. This is why encrypted digital video (Barvinok-5, proprietary
systems) is being developed.

**Video jamming** — since summer 2024, video jamming has become the most
effective counter-drone tactic. Jammers target standard 5.8 GHz video bands.
Countermeasures include operating on non-standard frequencies (1.2 GHz,
7.2 GHz), using higher-power VTX, and digital systems with error correction.

**Night operations** — low-lux cameras are standard for military FPV. Paired
with IR illuminators, they enable effective night strikes. Camera selection
for military use prioritizes minimum illumination over resolution.

**See:** [Military Firmware Forks](military-firmware-forks.md) for MILBETA's
VTX frequency unlock (3000–6999 MHz) and video frequency diversification
strategies.

---

## Sources

- Forge parts database (193 FPV cameras)
- Oscar Liang, FPV camera guides and reviews
- Manufacturer specifications (Foxeer, Caddx, RunCam, HDZero, Walksnail, DJI)
- Armada International, "Jamming UAV Video Signals" (Feb 2026)
- Militarnyi, "Chuyka 3.0 video signal detector" (2025)
