# Drone-to-Drone Intercept Playbook

> FPV interceptors are now a real weapons category. Wild Hornets' Werewolf
> and Sting drones have reduced enemy Lancet drone strikes by 75% within
> two months of introduction. Ukraine's FPV air defense capability
> launched an entirely new mission type: drone-on-drone combat. In October
> 2022, the first drone-vs-drone engagement was recorded. By 2025, it's
> a routine operational capability. This guide covers the operator-level
> knowledge for building and flying intercept missions. Zero public
> documentation existed for this before this guide.

**Cross-references:** [Propellers](../components/propellers.md) ·
[Motors](../components/motors.md) ·
[FPV Cameras](../components/fpv-cameras.md) ·
[Video Transmitters](../components/video-transmitters-vtx.md) ·
[Frames](../components/frames-airframe-selection.md) ·
[PID Tuning](pid-tuning.md) ·
[Frequency Planning](frequency-planning.md)

---

## Intercept vs Strike

Intercepting a drone in flight is fundamentally different from striking
a ground target. The key differences:

| Factor | Ground Strike | Air Intercept |
|--------|--------------|---------------|
| Target motion | Stationary or slow | 60-150+ km/h |
| Approach vector | Any angle, pilot's choice | Must match target altitude + heading |
| Time on target | Pilot controls timing | Closing speed leaves seconds |
| Camera tracking | Target stays in frame | Target moves across frame rapidly |
| Throttle management | Climb, cruise, dive | Sustained max or near-max throttle |
| Prop selection | Efficiency or speed | Speed above all else |
| Failure cost | Miss → go around | Miss → target continues to its objective |

---

## Interceptor Build Requirements

An interceptor drone must be faster than its target. The primary targets
are reconnaissance drones (Mavic-class, 50-70 km/h), Lancet loitering
munitions (80-110 km/h), and Shahed-type one-way attack drones
(150-180 km/h cruise).

### Speed Targets

| Target Class | Target Speed | Required Interceptor Speed | Notes |
|-------------|-------------|---------------------------|-------|
| Recon (Mavic) | 50-70 km/h | 100+ km/h | Easiest intercept |
| FPV strike | 80-120 km/h | 140+ km/h | Peer engagement |
| Lancet | 80-110 km/h | 130+ km/h | Fixed-wing, predictable path |
| Shahed | 150-180 km/h | 200+ km/h | Very fast, requires high-speed build |

### Frame

- **5" aggressive freestyle frame** for Mavic/FPV intercept. True X
  geometry for maximum agility.
- **5" stretched X or 7"** for Lancet/Shahed intercept where straight-line
  speed matters more than agility.
- **Low drag profile** — minimize frontal area. Camera angle 35-45°
  (higher than freestyle's typical 25-30°) because you're flying
  aggressively nose-down at full throttle.

### Motors

High-KV motors for maximum RPM on the chosen props. Speed comes from
RPM, not torque.

- **5" intercept:** 2207 or 2306, 2400-2700 KV on 6S. This produces
  speeds well above 150 km/h.
- **7" intercept:** 2806, 1500-1700 KV on 6S for 130+ km/h with
  better endurance than 5".

### Propellers

Speed is the priority. Intercept props are different from freestyle props.

- **High pitch, bi-blade or tri-blade.** 5x4.8x3 or 5.1x5x2 (bi-blade
  for absolute top speed). Higher pitch = more speed at the cost of
  efficiency and hover authority.
- **Aggressive pitch = less hover time.** An interceptor drone is not
  designed to loiter. It launches, climbs, intercepts, and returns (or
  is expended). Optimize for sprint, not endurance.
- **Don't use durable/soft props.** Stiff props (standard PC or glass
  fiber) transfer more power at high RPM. Flexible "durable" props
  lose efficiency at the RPMs you need.

### Battery

- **6S 1100-1300 mAh** for 5" intercept. Light, high discharge rate.
- **6S 1500-1800 mAh** for 7" intercept. More endurance for longer
  intercept windows.
- **High C-rating (100C+).** Sustained full-throttle intercept runs
  draw 80-120A from the battery. Low C-rate packs will sag, cutting
  motor RPM when you need it most.

---

## Camera and Video Setup

### The Tracking Problem

Tracking a fast-moving airborne target on an FPV feed is the hardest
piloting skill in drone operations. The target appears as a small dot
that moves rapidly across your field of view. Key camera settings:

### Camera Angle

- **35-45° uptilt.** Higher than freestyle. You're flying nose-down
  at full throttle, so a steeper angle keeps the horizon and target
  in the center of frame rather than at the top.

### FOV

- **Wide (150-170°).** Maximum field of view to spot and track the
  target. Narrow FOV makes it impossible to acquire a small, fast
  target.

### WDR / Contrast

- **WDR off or minimal.** WDR (Wide Dynamic Range) processing adds
  latency. For intercept, you need minimum camera-to-screen latency.
  Accept blown-out skies and crushed shadows.

### Analog vs Digital

- **Analog preferred for intercept.** Sub-1ms latency. At closing
  speeds of 200+ km/h combined, every millisecond of latency translates
  to meters of position error. Digital systems (30-50ms latency) make
  precise terminal intercept harder.
- **HDZero** is the best digital option for intercept (sub-4ms latency).
  DJI and Walksnail latency (30-50ms) is workable for slow targets
  (Mavic) but challenging for high-speed targets.

### VTX Power

- **Maximum available.** The intercept flight profile takes you away
  from your position rapidly. You need VTX range to match the
  intercept distance.

---

## Intercept Procedures

### Detection

The target must first be detected. Methods:

- **Visual observation** from the ground (daytime, close range)
- **Acoustic detection** (engine noise for Shaheds, prop noise for
  multirotors)
- **RF detection** (RF scanner picking up the target's control or
  video emissions — see [RF Detection Hardware](../components/rf-detection-hardware.md))
- **Radar** (military-grade, provides bearing and altitude)
- **Cued by another drone** (recon drone spots target, radios
  position to intercept team)

### Scramble

Once detected, the interceptor must launch and climb to the target's
altitude as fast as possible. Pre-position interceptors at alert status:

- **Battery connected, props on, armed switch off.** Flip arm and
  launch in under 5 seconds.
- **Pre-set a climb waypoint** if using GPS modes — climb to expected
  target altitude (100-300m for Lancets, 500-1500m for Shaheds) on
  the shortest path.
- **Manual climb in ACRO** is faster than GPS-assisted climb. Full
  throttle, nose up 60-70°, pure manual. This is where racing pilot
  skills translate directly.

### Approach Geometry

**Stern chase (from behind):** easiest intercept geometry. You're
flying in the same direction as the target, closing from behind.
Relative speed is your speed minus the target's speed. If you're
doing 160 km/h and the target is doing 100 km/h, closing speed is
60 km/h. Slow approach, easy tracking. But you need to be faster
than the target, and it takes longer to close.

**Head-on (from the front):** hardest intercept. Closing speed is
your speed plus the target's speed. If both are doing 100 km/h,
closing speed is 200 km/h. The target goes from a dot to filling
your frame in under 2 seconds. Extremely difficult to execute but
requires no speed advantage — you just need to be in the right
place.

**Beam (from the side):** intercept from 90° off the target's path.
You fly a collision course — aim ahead of the target so your paths
intersect. Requires accurate speed estimation and lead calculation.
Think skeet shooting.

**Recommended for beginners: stern chase.** Climb to the target's
altitude behind it, match heading, and close from behind. The
target grows slowly in frame, giving you time to align.

### Terminal Phase

The last 50-100 meters. The target fills a significant portion of
your camera view. At this point:

- **Aim for the propellers/rotors** — hitting the body may not kill
  a fixed-wing. Hitting a prop or wing surface causes immediate
  loss of control.
- **Use the entire drone as the weapon** — you're not shooting, you're
  ramming. Center mass is fine if you can get there.
- **Accept that this is likely a one-way flight** for the interceptor.
  The intercept drone is attritable. The asset it's protecting
  (howitzer, vehicle, position) is not.
- **Full throttle through impact.** Don't decelerate on approach.
  Your kinetic energy is what damages the target.

---

## PID Tuning for Intercept

Standard freestyle PID tunes prioritize smooth video and propwash
handling. Intercept tunes prioritize response speed and tracking
accuracy at high throttle.

- **Higher P gains** than freestyle. You need aggressive correction
  when you input a tracking adjustment at 150 km/h.
- **Lower D filtering** — accept more noise for faster response.
  Video quality is irrelevant; control authority is everything.
- **Rates:** high rates (800-1000 deg/s roll/pitch) for maximum
  agility during the approach phase. You need to make large, fast
  corrections to keep the target in frame.
- **Throttle management:** consider setting throttle limit to 100%
  (no throttle cap). Some freestyle tunes cap at 80-90% for
  smoother response — intercept needs everything the battery can
  deliver.

---

## Multi-Drone Intercept

For defending an area, multiple interceptors provide redundancy:

- **Alert rotation:** 2-3 interceptors on ready status, cycling
  batteries. Fresh batteries = maximum sprint speed.
- **Vectored intercept:** ground observer or recon drone provides
  bearing and altitude. Interceptor launches on vector rather than
  searching.
- **High-low pair:** one interceptor at altitude (early detection,
  head-on opportunity) and one at ground level (scramble on cue,
  stern chase).

### Frequency Planning

Each interceptor needs its own VTX channel. With 2-3 interceptors
plus a recon drone, you need 3-4 simultaneous video feeds. Use the
frequency planning worksheet — assign Raceband channels with
30 MHz minimum spacing.

---

## Target-Specific Notes

### vs Lancet

Lancet is a fixed-wing loitering munition. Predictable flight path
once committed to a target. Approaches in a shallow dive. Speed
80-110 km/h. Best intercepted during the loitering phase before it
commits — once in terminal dive, closing speed makes intercept
very difficult.

### vs Shahed/Geran

Large, fast (150-180+ km/h), flies at 300-1500m altitude. Very
predictable straight-line path (GPS-guided). Best intercepted from
a pre-positioned altitude with a head-on or beam approach. Wild
Hornets' "Sting" interceptors are purpose-built for this — very
high speed 5" builds with aggressive prop pitch.

### vs Recon Quad (Mavic-class)

Slow (50-70 km/h), hovers frequently, orbits target areas. Easiest
intercept target. Can be chased down from behind. The challenge is
detecting it — small visual and acoustic signature. RF detection
(picking up the DJI control link) is the most reliable detection
method.

### vs Enemy FPV

Peer engagement. Both drones are fast, agile, and piloted in real-
time. This is the hardest intercept — the target can evade. The
interceptor needs a speed and/or position advantage. Surprise
approach (from above or behind) before the enemy pilot reacts.
Training matters more than hardware in this scenario.

---

## Sources

- Wild Hornets, intercept drone operational reporting
- Forbes, "First drone-vs-drone dogfight" (Oct 2022)
- Ukrainian FPV air defense capability documentation
- TAF Industries, Kolibri interceptor variants
- NSDC Ukraine, FPV drone defense industry results (Jan 2026)
