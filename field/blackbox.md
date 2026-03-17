# Chapter 10: Blackbox Logs — What They Tell You

> The blackbox doesn't lie. Your memory does. Pull the log.

---

## What Gets Logged

A blackbox log records everything the flight controller knows at
high sample rate (typically 1–4 kHz on Betaflight, 100–400 Hz on
ArduPilot/PX4). This includes:

| Data | What It Tells You |
|------|-------------------|
| Gyroscope (roll, pitch, yaw rate) | How the drone is actually rotating — the ground truth |
| Accelerometer | Attitude estimation, vibration level |
| Motor outputs (1–8) | What the FC commanded each motor to do |
| RC commands | What the pilot actually asked for |
| PID terms (P, I, D per axis) | How the PID controller responded to error |
| Setpoint | What the FC was trying to achieve |
| Battery voltage | Voltage under load, sag profile |
| Battery current (if sensor) | Power consumption, mAh tracking |
| GPS position/speed (if equipped) | Flight path, speed, altitude |
| Filter state | Pre/post filter gyro (Betaflight debug modes) |

---

## How to Pull Logs

### Betaflight (Flash-Based)

Betaflight stores blackbox data on the FC's on-board flash chip
(typically 2–16 MB) or an SD card.

**Via Configurator:**
1. Connect USB
2. Blackbox tab → Download Flash → Save .bbl file

**Via MSP (what Wingman does):**
1. MSP_DATAFLASH_SUMMARY → get used bytes
2. MSP_DATAFLASH_READ in 4 KB chunks → stream raw data
3. Save as .bbl file

**Important:** Flash fills up. If it's full, new flights overwrite
old ones. After a session where you need the data, pull logs before
the next flight. Or switch to SD card logging if your FC supports it.

### ArduPilot (SD Card)

ArduPilot writes .bin DataFlash logs to the SD card.

**Via Mission Planner:** DataFlash Logs → Download
**Via MAVLink:** LOG_REQUEST_LIST → LOG_REQUEST_DATA → stream
**Via SD card:** Pull the card, copy .bin files directly

### PX4 (SD Card)

PX4 writes .ulg (ULog) files to the SD card.

**Via QGroundControl:** Analyze → Log Download
**Via SD card:** Pull the card, copy .ulg files

---

## Reading the Traces

### The Gyro Trace Is Everything

The gyroscope trace is the single most important data in a
blackbox log. It shows the actual angular rate of the drone on
each axis, sampled at 1–4 kHz. Everything else is derived from
or compared against the gyro.

**A clean gyro trace** looks like smooth curves that follow the
stick inputs. When you push the stick right, the roll gyro shows
a clean step to the commanded rate, holds, then returns to zero
when you release.

**A noisy gyro trace** looks like the clean curve with fuzz,
spikes, or oscillation layered on top. The noise is real — the
drone is actually vibrating. The question is where the vibration
comes from and whether it matters.

### The Five Patterns That Indicate Real Problems

**Pattern 1: High-frequency noise on all axes, increasing with throttle.**

What it looks like: Fuzz on the gyro trace that gets worse as
you increase throttle. Consistent across roll, pitch, and yaw.

What it means: Mechanical vibration from the motors/props is
reaching the FC. The motors are the only thing on the drone
whose vibration scales with throttle.

What to check: Prop balance, motor bearings, FC soft mount,
frame arm tightness. If the noise is broadband (not at a specific
frequency), it's probably multiple sources. Fix the biggest one
first — usually props.

---

**Pattern 2: Oscillation at a specific frequency, visible as regular waves.**

What it looks like: A sine wave overlaid on the gyro trace.
Consistent frequency regardless of stick input. May be present
on one axis more than others.

What it means: Resonance. Something on the frame has a natural
frequency that's being excited by the motors. The FC's filters
are either not catching it or are making it worse.

What to check: Look at the frequency (use the Betaflight Blackbox
Explorer's spectrum analyzer). Common resonances:
- 80–150 Hz: Frame flex (arms, standoffs)
- 150–300 Hz: Prop/motor mechanical resonance
- 300–600 Hz: Gyro noise floor (filter issue, not mechanical)

If the dynamic notch filter is enabled, check if it's tracking
this frequency. If not, adjust the notch range.

---

**Pattern 3: D-term noise spikes, especially on yaw.**

What it looks like: The D-term trace (visible in debug mode) is
noisy or spiky, even when the gyro trace looks relatively clean.
Yaw axis is typically worst.

What it means: The D-term is the derivative of gyro error. It
amplifies high-frequency noise by design — that's how it reacts
quickly to changes. If the gyro has even small amounts of
high-frequency content, D amplifies it into large motor corrections.

What to check: Lower D-term gain (try -20%). If that helps
significantly, the issue is D sensitivity to noise, not mechanical.
Also check: D-term lowpass filter cutoff (lowering it reduces
D noise at the cost of slower D response), dynamic notch filter
(should be catching the frequencies that D is reacting to).

---

**Pattern 4: Motor output asymmetry — one motor consistently higher.**

What it looks like: In the motor output traces, one motor is
always running at higher output than the others. The difference
is consistent across throttle levels.

What it means: The FC is compensating for something that makes
the drone want to rotate toward the weak motor's side. Possible
causes:
- Motor or ESC weaker on one side (dying motor, marginal ESC)
- Center of gravity offset (battery mounted off-center)
- Bent motor mount changing thrust angle
- Damaged prop generating less thrust

What to check: Swap the suspect motor to a different arm. If the
asymmetry follows the motor, it's the motor. If it stays on the
same arm, it's the mount or frame. If it moves to the diagonal,
it's CG.

Rule of thumb: Up to 5% asymmetry is normal. 5–10% is worth
investigating. Above 10% is a problem that will get worse.

---

**Pattern 5: Voltage sag correlating with performance loss.**

What it looks like: Battery voltage drops sharply during aggressive
maneuvers. At the same time, motor outputs hit 100% (full throttle
commanded but can't produce it), and the gyro shows the drone
not achieving the commanded rate.

What it means: The battery can't deliver enough current. The
voltage sags, the ESCs can't spin the motors fast enough, and
the drone loses authority. This is a power system problem, not
a tuning problem.

What to check: Battery internal resistance (measure with a charger
that shows IR per cell). IR above 15 mΩ/cell means the pack is aging.
Voltage sag below 3.3V/cell under load is concerning. Below 3.0V/cell
is damaging the battery.

**Don't tune around bad batteries.** If the battery is sagging,
no amount of PID tuning will fix the performance loss. Replace
the battery.

---

## Blackbox Analysis Workflow

**Step 1: Pull the log.** Immediately after the flight you want
to analyze. Don't fly again first.

**Step 2: Open in the right tool.**
- Betaflight: [Betaflight Blackbox Explorer](https://github.com/betaflight/blackbox-log-viewer)
- ArduPilot: Mission Planner → DataFlash Log tab, or [UAV Log Viewer](https://plot.ardupilot.org)
- PX4: [Flight Review](https://review.px4.io) or PlotJuggler

**Step 3: Look at the gyro first.** Always. Before looking at PIDs,
motor outputs, or anything else. The gyro tells you what actually
happened. Everything else tells you what the FC tried to do about it.

**Step 4: Compare setpoint to gyro.** The setpoint is what the FC
was trying to achieve. The gyro is what actually happened. The gap
between them is the error. A well-tuned drone tracks setpoint closely.
A poorly tuned one lags, overshoots, or oscillates around it.

**Step 5: Check motor outputs.** Are they even? Are any hitting
100%? Are there sudden spikes? Motor output tells you how hard
the FC is working to maintain control.

**Step 6: Check battery voltage.** Does it hold steady or sag
under load? Voltage sag during aggressive maneuvers is normal.
Voltage sag during hover is a problem.

**Step 7: If you found a problem, change ONE thing.** Fly again.
Pull another log. Compare. This is how tuning works — iterative,
data-driven, one variable at a time.

---

## What Logs Don't Tell You

- **Why the pilot made a decision.** Logs show what the drone did,
  not what the operator intended. If a flyaway log shows the drone
  going north, you don't know if the pilot pushed north or if the
  drone went north on its own without checking the stick inputs.

- **External conditions.** Wind, temperature, air density, obstacles
  — none of these are in the log. A drone that oscillates on a
  windy day and flies clean on a calm day isn't broken. It's
  dealing with turbulence. Logs won't show you the wind.

- **What happened after the crash.** If the drone hits something
  and the FC loses power, the log ends. The last few hundred
  milliseconds of data may be corrupt or missing. The moments
  before the crash are usually there.

---

## Next

- **Chapter 11: PID Tuning for People Who Fly** — using blackbox data
  to improve your tune.
- **Chapter 12: When Things Go Wrong** — the diagnostic tree that
  starts with symptoms and uses logs to find causes.

---

*The log is the flight's memory. It remembers what you don't.
Pull it. Read it. Trust it over your recollection.*
