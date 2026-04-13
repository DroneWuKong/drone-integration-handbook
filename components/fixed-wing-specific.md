# Fixed-Wing Specific Integration

> Fixed-wing UAS are fundamentally different from multirotors in every
> dimension that matters for integration: flight dynamics, firmware,
> failure modes, and airspace requirements.

---

## When Fixed-Wing Makes Sense

| Requirement | Multirotor | Fixed-Wing |
|-------------|-----------|------------|
| Endurance >45 min | ✗ (battery) | ✓ |
| Range >5km | Marginal | ✓ |
| Hover / precise position | ✓ | ✗ (unless VTOL) |
| Wind resistance | Marginal | ✓ (10–15 m/s typical) |
| Payload fraction | ~15–25% | ~20–35% |
| Launch/recovery space | Minimal | Runway or hand-launch |
| BVLOS mapping | Inefficient | Optimal |
| Urban ops | ✓ | ✗ |

---

## Firmware: ArduPlane vs iNav

### ArduPlane
Best for: mission-critical fixed-wing, VTOL, BVLOS, Blue UAS programs.

Key features:
- Mature VTOL support (QuadPlane, tiltrotor, tailsitter)
- TECS (Total Energy Control System) for precise altitude/airspeed hold
- L1 navigation controller — smooth waypoint following
- Loiter, figure-8, survey patterns built-in
- ADSB/FLARM avoidance
- MAVLink, full GCS support (Mission Planner, QGC)

### iNav
Best for: FPV fixed-wing, racers, budget builds, analog video.

Key features:
- Leaner codebase, runs on F4/F7 FCs
- GPS rescue (RTH equivalent for fixed-wing)
- Blackbox logging
- OSD support
- Limited VTOL support (experimental)

**Bottom line:** ArduPlane for anything serious. iNav for FPV wings where
you want Betaflight-like workflow.

---

## Airspeed Sensors

Critical for safe fixed-wing flight. Without airspeed, the FC can't
distinguish low groundspeed (safe landing) from stall (crash).

### Types

| Sensor | Interface | Accuracy | Notes |
|--------|-----------|----------|-------|
| Matek ASPD-7002 | I2C (DroneCAN) | ±0.5 m/s | Good value, NDAA ✓ |
| mRo i2c Airspeed | I2C | ±1 m/s | Common on Pixhawk builds |
| Sensirion SDP3x | I2C | ±0.3 m/s | Highest accuracy, requires calibration |
| Foxtech pitot | Analog | ±2 m/s | Budget option |

### ArduPlane Config

```
ARSPD_TYPE = 1       (analog) or 2 (MS4525) or 3 (SDP3x)
ARSPD_PIN = 15       (ADC pin for analog type)
ARSPD_USE = 1        (use airspeed in flight)
ARSPD_RATIO = 2.0    (calibration ratio — tune via AUTOTUNE)
AIRSPEED_MIN = 12    (stall speed + margin, m/s)
AIRSPEED_CRUISE = 18 (cruise airspeed, m/s)
AIRSPEED_FBW_MAX = 28
TECS_SPDWEIGHT = 1.0 (1.0 = airspeed priority, 0.0 = altitude priority)
```

---

## VTOL Transitions (QuadPlane)

VTOL fixed-wing (tiltrotor, quadplane) gives you vertical takeoff +
fixed-wing cruise efficiency. Complex to tune but operationally powerful.

### Transition Phase

```
Q_TRANSITION_MS = 5000  (milliseconds for transition)
Q_TILT_TYPE = 0 (continuous) or 1 (binary)
Q_ASSIST_SPEED = 15  (m/s — assist motors below this in FW mode)
ARSPD_FBW_MIN = 15   (minimum airspeed before transition attempts)
```

**Most transition crashes** happen when:
1. Transition speed too low — aircraft stalls mid-transition
2. Wind too strong during transition — too much attitude change
3. Pilot induces RC input during transition — let the autopilot do it

**Never manually fly through a transition.** Put it in AUTO or GUIDED,
set a transition waypoint, and let TECS handle it.

### Back-transition

```
Q_GUIDED_MODE = 1  (allow guided mode in VTOL)
Q_RTL_MODE = 1     (use VTOL for RTL landing)
Q_LAND_SPEED = 50  (cm/s descent in VTOL landing)
```

---

## Long-Range Planning

### Wind Compensation

Fixed-wing performance degrades significantly in crosswinds >30% of
cruise airspeed. For 18 m/s cruise, avoid >5–6 m/s crosswind.

ArduPlane compensates automatically via L1 controller, but:
- Upwind legs consume 30–50% more power
- Ground speed varies significantly — plan mission timing accordingly
- Consider wind shadow (terrain blocking wind) for launch/recovery

### Energy Management (TECS)

TECS manages the trade between altitude and airspeed using total energy.
Key params:

```
TECS_CLMB_MAX = 5   (max climb rate, m/s)
TECS_SINK_MIN = 2   (min sink rate for descent, m/s)
TECS_SINK_MAX = 5   (max sink for emergency descent)
TECS_TIME_CONST = 5 (response time — lower = more aggressive)
TECS_THR_DAMP = 0.5 (throttle damping)
```

### Survey Pattern Optimization

For photogrammetry missions:
- Fly into the wind on capture legs (consistent airspeed → consistent GSD)
- Return legs downwind (faster, fewer photos = smaller dataset)
- Plan 20% overlap in downwind direction to account for drift
- Use QGC or Mission Planner survey grid — don't manually enter waypoints

---

## Launch & Recovery

### Hand Launch

Most common for sub-5kg fixed-wing.

```
TKOFF_THR_DELAY = 2  (seconds of full throttle before hand release)
TKOFF_THR_MINACC = 5 (m/s² acceleration to detect launch)
TKOFF_THR_MINSPD = 10 (m/s before climbing)
TECS_PITCH_MAX = 20  (max pitch during climb, degrees)
```

Technique: arm, set mode to FBWA or AUTO, apply full throttle, hold
level, release into wind at normal walking speed. Don't throw — push.

### Belly Landing

```
LAND_FLARE_ALT = 10   (altitude to start flare, m AGL)
LAND_FLARE_SEC = 3    (time to flare)
LAND_PITCH_CD = -300  (pitch during flare, centidegrees, negative = nose up)
LAND_SLOPE_RECALC_STEEP_THRESHOLD_TO_ABORT = 25  (abort steep approach)
```

### Parachute Recovery

For valuable or heavy platforms. ArduPlane has built-in parachute support:

```
CHUTE_ENABLED = 1
CHUTE_TYPE = 10     (relay type)
CHUTE_RELAY_ON = 0  (relay pin)
CHUTE_MIN_ALT = 30  (minimum altitude for deployment, m)
CHUTE_MIN_SPEED = 5 (minimum speed for deployment, m/s)
```

---

## Failure Modes Specific to Fixed-Wing

**Loss of airspeed sensor** — FC falls back to GPS groundspeed.
Configure backup: `ARSPD_TYPE2` for redundant sensor.

**Stall** — at low speed or high AOA. TECS prevents most stalls,
but aggressive manual input overrides this. Set `STALL_PREVENTION = 1`.

**Spiral dive** — autopilot failure mode. If attitude reference is
lost, the aircraft spirals. Configure `FS_LONG_ACTION = 2` (RTL)
with short timeout to catch this.

**Powerplant failure** — fixed-wing can glide to a safe landing.
Configure a glide ratio parameter so the autopilot plans for engine-out:
`TECS_LAND_SPDWGT = 1.9` (prioritize airspeed over altitude on landing).

---

## NDAA-Compliant Fixed-Wing Options

| Platform | Blue UAS | Endurance | Range | Notes |
|----------|----------|-----------|-------|-------|
| WingtraOne GEN II | YES | 59 min | 30km | Mapping specialist |
| AgEagle eBee VISION | YES | 90+ min | 40km | Long-endurance survey |
| AgEagle eBee TAC | YES | 90+ min | 40km | Defense variant |
| Censys Sentaero | YES | 70 min | 20km | BVLOS certified |

---

## Related

- [BVLOS Pathways](bvlos-pathways.md)
- [Cellular / LTE for BVLOS](cellular-lte-bvlos.md)
- [Fleet Management](fleet-management.md)
- [Platforms — Blue UAS](../platforms/README.md)
