# RTK vs PPK: The Real Story

There is no correct answer to "should I use RTK or PPK?" Anyone who tells you otherwise is selling something or hasn't worked in enough terrain types. Both methods achieve centimeter-level accuracy. Both have workflows that can fail silently. Both require things the vendor won't tell you until you've already ruined a mission. This guide covers the physics, the failure modes, and the cases where one is genuinely better than the other.

---

## The Physics: What Both Methods Are Actually Doing

Standard GNSS positions your receiver by measuring the travel time of pseudorandom noise codes from satellites to your antenna. The timing accuracy of modern chips puts this at roughly 1–5 meters of horizontal position. That's the code-based solution.

Both RTK and PPK use **carrier phase measurements** instead. The carrier wave of a GPS L1 signal has a wavelength of 19cm. By tracking the phase of this wave rather than the timing of the code, a receiver can resolve position to roughly 1–3% of a wavelength — in the millimeter range. The problem is integer ambiguity: you're measuring the fractional phase, but you don't know how many complete cycles are between you and the satellite. That unknown integer is the "ambiguity."

Resolving this integer ambiguity is the entire technical challenge of both RTK and PPK. Everything else — the radio link, the base station, the post-processing software — exists to solve for these integers accurately and reliably.

**Double differencing** eliminates common-mode errors (atmospheric delays, clock errors) by computing the difference of phase measurements between two receivers (rover and base) and two satellites simultaneously. This is why you need a base station: you need two receivers measuring the same satellites at the same time to cancel the noise that prevents ambiguity resolution.

---

## RTK: Real-Time Ambiguity Resolution

In RTK, the base station sends its raw observations to the rover **during the flight** via a radio link or cellular/NTRIP connection. The rover's processor resolves the integer ambiguities in real time and outputs a corrected position solution every epoch (typically every 100–200ms).

### The FIX vs FLOAT Distinction

This is the most important thing to understand about RTK:

**RTK FIXED:** Integer ambiguities are resolved. Position accuracy is 1–3cm horizontal. This is what the spec sheet is advertising.

**RTK FLOAT:** Ambiguities are not resolved — the processor has a floating-point estimate of the integers but hasn't locked them down. Accuracy is 20cm to 1m. Your drone is flying, your camera is firing, and the positions being written to the photo EXIF are **not centimeter-accurate** even though the RTK system is "working."

**Float happens more than vendors admit.** During sharp turns, the antenna tilts away from optimal sky view. Flying close to trees, buildings, or terrain causes signal blockage and multipath. A momentary data-link dropout (radio range, NTRIP latency spike) stops correction delivery. In each case, the system drops from FIX to FLOAT silently — the drone keeps flying, the camera keeps firing, and the photos keep getting tagged with positions that may be 30cm off.

### RTK Initialization Period

When the rover starts up, or after a FIX is lost and regained, there is an initialization period during which the ambiguities are being resolved. For a stationary receiver with good sky view, this takes 30–120 seconds. For a moving drone with an antenna that's rocking through attitude changes: longer. Some multi-band receivers (dual-frequency L1/L2 or L1/L5) initialize much faster than single-band because the second frequency provides additional constraints on the ambiguity solution.

**What this means in practice:** Don't start your survey grid the moment the controller shows "RTK Fixed." Hover for 2–3 minutes first to confirm the solution is stable, then depart. The initialization that happened on the pad in perfect conditions may not survive the first 90-degree turn at the mission start.

---

## PPK: Post-Processing What RTK Does in Real Time

In PPK, the rover logs its raw GNSS observations throughout the flight. The base station logs simultaneously. After the flight, you run a processing algorithm that does what the RTK rover's processor tried to do in real time — but now with access to the complete dataset, forward and backward, and optionally precise satellite ephemerides.

### The Forward-Backward Processing Advantage

This is why PPK can be more accurate than RTK in marginal conditions, and why it's not just "offline RTK."

An RTK receiver processes data causal — it can only use observations from the past and present. When a signal blockage causes a FIX to drop, the receiver has to re-initialize forward in time.

A PPK processor runs the Kalman filter twice: **forward** (in time order) and **backward** (reverse time order). Then it combines them. A signal dropout mid-flight that loses FIX in the forward pass may be initialized from observations that come *after* the blockage in the backward pass — because from the end of the flight looking backward, the solver already knows where the aircraft ended up and can propagate that constraint backward through the blockage.

The combined forward-backward solution has higher ambiguity resolution rates and better accuracy in the segments around signal blockages than any real-time system can achieve. This is a fundamental mathematical advantage, not a software trick.

### Precise Ephemerides

Broadcast satellite ephemerides (the satellite position and clock data your receiver uses in real time) are accurate to 1–2 meters. The International GNSS Service (IGS) publishes precise ephemerides after the fact, accurate to a few centimeters. PPK can use these; RTK cannot.

For baselines under 20km, the improvement from precise ephemerides is small. For long baselines (50km+) or when using CORS stations, the improvement is significant — this is one reason why CORS-based PPK with a 40km baseline can still achieve centimeter accuracy when CORS-based RTK at the same distance would struggle.

---

## Where Each Method Fails

### RTK Failure Modes

**1. Link dropout → silent float**
The radio link drops for 5 seconds during a turn. The RTK rover loses corrections, drops to FLOAT, assigns 40cm position estimates to 20 photos, then re-acquires FIX and continues. Your processing software sees no flag — the photos look fine, the coordinates look fine, but a strip across your survey has terrible position accuracy. You won't know until you compare against check points.

**2. NTRIP latency → float or degraded FIX**
NTRIP delivers corrections over cellular. In remote areas with marginal signal, packets arrive late. The rover's ambiguity filter gets stale corrections and may degrade to FLOAT or produce a biased FIX solution. RTK via NTRIP is sensitive to the quality of cellular coverage in a way that a direct radio link is not.

**3. Long baseline degradation**
Single-band RTK over a 30km CORS baseline: the tropospheric and ionospheric delays are different at the base and rover, and double-differencing doesn't fully cancel them. Accuracy degrades to 5–15cm. Multi-band (dual-frequency) receivers handle this much better — the ionospheric delay is frequency-dependent, and two-frequency data allows direct ionospheric modeling.

**4. Multipath at the drone antenna**
The drone's GPS antenna is surrounded by carbon fiber arms, ESCs, and other RF-reflective surfaces. Signals reflecting off these surfaces create multipath that corrupts carrier phase measurements. This shows up as a "noisy" FIX — technically FIX status but with 3–5cm scatter rather than 1–2cm. Active antenna designs and careful antenna placement reduce this.

**5. False FIX**
The ambiguity resolution algorithm can converge on the wrong integer values. The position looks like a FIX (the ratio test passes, the algorithm reports fixed integers), but the integers are wrong and the position has a systematic offset — often 10–20cm — from the truth. The ratio test threshold controls the probability of a false fix. Default settings in many receivers may be too permissive for high-stakes survey work.

### PPK Failure Modes

**1. Short flight / inadequate initialization time**
The PPK ambiguity solver needs enough data to converge. For a single-frequency receiver, less than 5–10 minutes of continuous flight data can result in a FLOAT-only solution. The rover is in the air, moving, which makes ambiguity resolution harder than a static survey — the processor needs enough redundant observations from different satellite geometries to lock down the integers. Flights under 5 minutes with a short observation window are high-risk for PPK.

**2. Base station logging rate mismatch**
The drone logs at 5Hz or 10Hz. A base station logging at 1Hz (every second) means the PPK solver interpolates base observations between the 200ms drone samples. This introduces interpolation error, particularly during clock drifts and ionospheric activity. The base must log at the same rate as the rover — 5Hz minimum, 10Hz preferred.

**DJI Matrice 4E issue:** Multiple operators have reported that PPK with the M4E produces consistently worse results than RTK, with 8–10cm vertical offset even when PPK is processed correctly. Diagnosis points to the M4E logging raw observations at a different internal rate than the M3E, causing the base-rover time alignment to degrade. The fix: use DJI's own DJI Terra software for M4E PPK rather than third-party tools, or set the base station logging rate to match exactly the rover's output rate.

**3. Baseline too long**
PPK has more baseline tolerance than RTK because it can use precise ephemerides and ionospheric models. But there are still limits. With single-band receivers:
- < 10km: reliable FIX expected
- 10–30km: FIX likely, depends on ionospheric activity
- 30–50km: FLOAT likely, accuracy 10–30cm
- > 50km: FLOAT almost certain, not suitable for cm-accuracy work

With multi-band (dual-frequency) receivers the thresholds roughly double.

**4. Base station on an unknown point**
If the base is "free-stationed" (placed anywhere and coordinates derived from averaging GPS readings), the absolute position of the base has 30cm–3m uncertainty. Your relative accuracy (internal consistency) will still be centimeter-level, but the absolute position of your dataset is uncertain. For volume calculations and change detection this doesn't matter. For cadastral surveys or tying to existing infrastructure, the base must be on a known point or post-processed against a CORS to determine its precise absolute position.

**5. Camera shutter timing errors**
PPK assigns positions to photos based on a timestamp. If the timestamp comes from the EXIF metadata written by the camera controller rather than a hardware signal wired to the GNSS receiver, there's typically 10–50ms of timing uncertainty from operating system latency and camera processing delay.

At 10m/s groundspeed, 50ms = 50cm position error. This is the single most common reason PPK produces worse results than expected even when the GNSS solution looks clean.

**The fix:** Use a hardware shutter sync — the GNSS receiver's event input (or "hot shoe" signal) is triggered by the physical shutter, not the camera's software. Emlid Reach's hot shoe connection provides <1µs timing accuracy. DJI RTK drones write `.MRK` files with hardware-synced shutter timestamps, which is why they work much better with PPK than third-party integrations using EXIF-only timing.

---

## The Controversy: "Which Is Better?"

The internet argument about RTK vs PPK is mostly people talking about different scenarios without acknowledging it.

**RTK advocates argue:** Faster workflow, no post-processing, immediate quality check, no risk of forgetting to collect base data, works with standard photogrammetry pipelines without special handling.

**PPK advocates argue:** More robust, no data loss from link dropout, forward-backward processing is fundamentally more accurate, works at long range, doesn't depend on radio/cellular infrastructure.

**Both are right** about their chosen scenario. Here's the honest breakdown:

| Scenario | RTK Advantage | PPK Advantage |
|---|---|---|
| Urban/suburban, NTRIP available | ✓ Faster workflow, no base equipment | — |
| Remote area, no cellular | — | ✓ No link dependency |
| Large site, multiple batteries | Risky — link may drop between batteries | ✓ Continuous log across battery swaps |
| Site near buildings/trees | Risky — signal blockage causes float | ✓ Forward-backward recovers from blockage |
| Time-critical delivery | ✓ No post-processing delay | — |
| Legal/cadastral survey | Both need GCPs/checkpoints regardless | ✓ Auditable raw data log |
| LiDAR mission | ✓ Guides real-time flight path | ✓ Better trajectory for scan strip alignment |
| Long baseline (>20km) | Difficult with single-band | ✓ Handles better with precise ephemerides |
| Quality assurance | Visible in GCS during flight | Visible only after post-processing |

---

## The Case for Doing Both

Modern RTK drones (DJI M3E/M4E, Autel EVO Max, Skydio X10 RTK) log raw observations simultaneously with applying RTK corrections. This means you have PPK data even when flying in RTK mode.

**The dual workflow:**
1. Fly in RTK mode — get instant geotag corrections
2. Keep the raw log running
3. If RTK holds FIX throughout: use the RTK-tagged photos, done
4. If RTK dropped to FLOAT in a segment: post-process that segment with PPK
5. Result: RTK speed with PPK reliability

This is not a compromise — it's strictly better than either alone. DroneDeploy's Smart Uploader implements exactly this: it applies RTK corrections by default and automatically falls back to PPK for segments where RTK quality was poor.

---

## Ground Control Points: Still Not Optional

Neither RTK nor PPK eliminates the need for ground validation. They reduce the *number* of GCPs needed, but they don't replace the QA function that GCPs provide.

**Why checkpoints matter even with RTK/PPK:**

1. **Absolute accuracy verification:** RTK/PPK gives you a precise trajectory, but the absolute accuracy of that trajectory depends on the absolute accuracy of the base station's coordinates. Even if the base is on a "known point," that point may have 2–5cm uncertainty depending on how it was established. A checkpoint on a separately surveyed point catches this.

2. **False fix detection:** A false RTK fix (wrong integer ambiguity, position biased by 10–20cm) can pass all internal quality metrics. It's impossible to detect without an external reference. One well-placed checkpoint would catch it.

3. **Photogrammetric consistency:** The RTK/PPK position is the GNSS antenna position. The actual camera position involves the antenna-to-camera offset vector (lever arm) that must be measured and applied. A systematic error in the lever arm — which is easy to make — produces a consistent offset in the final model. Checkpoints catch this.

**Minimum checkpoint strategy for RTK/PPK surveys:**
- 3–5 checkpoints distributed across the site (corners + center for a rectangular area)
- Measured with independent survey equipment at higher accuracy than the expected drone survey accuracy
- Checkpoints should not also be used as GCPs in the photogrammetric bundle adjustment — they must be kept independent for verification

The standard practice in survey-grade work: use 1–3 GCPs to anchor the bundle adjustment, and 3–5 independent checkpoints to verify. RTK/PPK with this approach typically achieves 1–3cm RMSE on checkpoints in good conditions.

---

## Software Options for PPK Processing

| Software | Cost | Learning Curve | Best For |
|---|---|---|---|
| **Emlid Studio** | Free | Low | Emlid hardware; DJI with .MRK files; beginner-friendly |
| **RTKLIB** (rtkpost) | Free, open-source | High | Custom setups, research, any hardware |
| **KlauPPK** | Paid (~$200/yr) | Medium | DJI enterprise; handles DJI-specific formats natively |
| **Pix4Dfields PPK** | Paid (subscription) | Low | Integrated with Pix4D photogrammetry |
| **Leica Infinity** | Paid (expensive) | Medium | Professional survey; full adjustment capability |
| **Novatel Inertial Explorer** | Paid (expensive) | High | Survey grade; INS/GNSS tightly coupled processing |
| **DJI Terra** | Paid (subscription) | Low | DJI hardware; best for M4E and newer DJI RTK drones |

**For most operators starting with PPK:** Emlid Studio is the right choice. It handles RINEX data from any manufacturer, processes DJI's `.MRK` files, and produces geotagged photos ready for import into any photogrammetry package.

**For DJI Matrice 4E specifically:** Use KlauPPK or DJI Terra. Third-party tools have documented issues with M4E raw data formats.

---

## Practical Decision Framework

```
Do you have reliable cellular or radio C2 coverage over the entire site?
│
├─ YES → RTK is faster. Use it.
│         Still log raw data as PPK fallback.
│         Verify FIX status throughout — check the flight log, not just the summary.
│
└─ NO → PPK is required.
          │
          ├─ Is baseline < 20km from nearest CORS?
          │   ├─ YES → Use CORS base data (no hardware needed). Multi-band preferred.
          │   └─ NO → Set up local base station. Must log at rover rate. Log >1 hour.
          │
          ├─ Is the flight > 10 minutes of continuous data?
          │   └─ NO → PPK may not achieve FIX. Consider shorter segments or
          │            single-band upgrade to multi-band for faster initialization.
          │
          └─ Does the camera have hardware shutter sync?
              ├─ YES → MRK/event log will give <1ms timing accuracy. Expect cm results.
              └─ NO → EXIF-only timing. Expect 10–50cm error at normal survey speeds.
                       Fly slower (<5m/s) to reduce shutter-lag position error.
```

---

## The One Thing Everyone Gets Wrong

The accuracy number on the spec sheet — "1cm + 1ppm horizontal" — is the GNSS trajectory accuracy. It is **not** the final map accuracy.

Final map accuracy depends on:
1. GNSS trajectory accuracy (RTK/PPK performance)
2. Camera calibration (lens distortion, principal point)
3. IMU/camera boresight offset
4. Ground sampling distance (flight altitude)
5. Image overlap (how well photogrammetry can reconstruct geometry)
6. Processing software settings
7. Whether you have independent checkpoints to verify

A drone with a 1cm RTK solution but a poorly calibrated camera, flying at 120m AGL, will produce a survey with 5–10cm absolute accuracy. A drone with a 3cm PPK solution but a well-calibrated camera, flying at 60m AGL with 80% overlap, will beat it on every project. Hardware matters, but workflow matters more.
