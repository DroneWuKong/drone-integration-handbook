# Chapter 12: When Things Go Wrong

> This is the chapter you read at the field with a broken drone
> in your hands. Start with the symptom. Follow the tree.

---

## How to Use This Chapter

Find your symptom in the list below. Follow the diagnostic steps
in order. Each step either solves the problem or narrows it down.
Don't skip steps — the obvious cause is often not the actual cause.

---

## Symptom: Won't Arm

The FC refuses to arm. This is the most common field problem and
the one with the most possible causes.

**Step 1: Read the arming flags.**
- Betaflight: CLI → `status` → look for arming disable flags
- iNav: CLI → `status` → same
- ArduPilot: GCS → Messages tab → pre-arm check failures
- PX4: QGC → Vehicle Setup → Summary → pre-arm checks

**Step 2: Common arming flags and fixes.**

| Flag | Meaning | Fix |
|------|---------|-----|
| RXLOSS / No RC | FC not receiving RC signal | Check UART assignment, baud rate, protocol selection. Verify receiver is powered and bound. |
| ACC not cal | Accelerometer not calibrated | Calibrate accel (level the quad, run cal in configurator) |
| ANGLE | Quad not level enough | Place on level surface. If on uneven ground, raise arm angle limit temporarily. |
| THROTTLE | Throttle not at minimum | Move throttle stick fully down. Check endpoint calibration. |
| CLI | CLI is open | Close the CLI connection |
| MSP | MSP connection active preventing arm | Some configurator connections block arming. Disconnect. |
| LOAD | CPU overloaded | Reduce gyro/PID loop frequency or disable unnecessary features |
| RPMFILTER | RPM filter configured but no signal | Check ESC telemetry UART or disable RPM filter |
| GPS FIX | Requires GPS fix before arm (nav modes) | Wait for GPS lock or disable GPS pre-arm requirement |

**Step 3: If no flags show but still won't arm.**
- Check switch assignment. Arm switch might be on a channel that
  isn't configured or is inverted.
- Check throttle endpoints. Some FCs require throttle below 1050 µs.
- Power cycle everything. Receiver, FC, ESCs. In that order.

---

## Symptom: Oscillation / Vibration in Flight

The quad shakes, wobbles, or makes a buzzing sound in flight.
Could be mechanical or electronic.

**Step 1: Determine if it's always present or speed-dependent.**
- Always present (even at hover): likely filter or PID issue
- Only at high throttle: likely mechanical — prop balance, motor bearing, loose standoff
- Only after a crash: prop damage, bent motor shaft, cracked frame arm

**Step 2: Check mechanical first.** Always. Before touching PIDs.
- Spin each motor by hand. Feel for grit, catch, or uneven resistance.
  One bad bearing can cause the whole quad to oscillate.
- Check props for damage. Even a tiny nick changes balance.
  Replace suspect props — they're the cheapest component.
- Check motor mounting screws. Loose motor = oscillation source.
- Press on each arm. Flex = vibration transmission path.
  Carbon fiber arms don't flex. Cheap 3D-printed arms do.
- Check FC mounting. Soft mount grommets should be intact
  and the FC should not contact the frame directly.

**Step 3: Pull a blackbox log.** If mechanical checks pass:
- Look at gyro traces. Clean gyro = clean flight. Noisy gyro =
  something is shaking the FC.
- Compare pre-filter and post-filter gyro. If pre-filter is noisy
  but post-filter is clean, your filters are working hard. Consider
  addressing the source instead of filtering harder.
- Look for a specific frequency peak. A resonance at a consistent
  frequency often indicates a specific mechanical source:
  - Prop-speed frequency: prop balance issue
  - Frame resonance (usually 100-300 Hz): frame flex
  - Motor bearing: broadband noise that increases with throttle

**Step 4: If it's a filter/PID issue:**
- Lower D-term first. D is the most noise-sensitive PID term.
  Drop D by 20% and fly again.
- Check dynamic notch filter. If not enabled, enable it.
  If enabled, check that it's tracking the right frequency range.
- Lower gyro lowpass filter cutoff. Default is usually fine,
  but noisy builds may need 150 Hz instead of 200 Hz.
- As a last resort, lower P-term. But if you need to drop P
  significantly to stop oscillation, the problem is mechanical,
  not tuning.

---

## Symptom: Flyaway / Unexpected Movement

The drone moves in a direction the pilot didn't command.

**Step 1: Did it respond to stick input during the event?**
- Yes, but drifted: likely sensor issue (compass interference, GPS glitch, accelerometer drift)
- No response to sticks at all: likely failsafe triggered, mode switch, or loss of RC link

**Step 2: Check flight mode.** Did the mode change unexpectedly?
- A mode switch bumped during handling can change from acro to
  angle to GPS hold, causing unexpected behavior.
- ArduPilot/PX4: check mode channel (usually CH5) assignment and thresholds.
- Betaflight: check mode tab for overlapping ranges on the aux channels.

**Step 3: Check compass and GPS.** For GPS-assist modes:
- Compass interference from power wires is the #1 cause of
  GPS-mode flyaways. The compass reads the magnetic field from
  the battery leads as a heading change and "corrects" by turning.
- Fix: move the compass (external GPS/compass module) as far from
  power wires as possible. Use a GPS mast.
- Check for GPS glitch in the log. A sudden position jump causes
  the FC to "correct" toward the wrong position.

**Step 4: After landing, pull logs immediately.** Don't fly again
until you understand what happened. Logs will show stick inputs,
actual motor outputs, sensor readings, and mode changes. The cause
is almost always visible in the data.

---

## Symptom: Video Loss / Breakup

FPV video feed drops, goes to static, shows artifacts, or freezes.

**Step 1: Analog or digital?**

**Analog 5.8 GHz:**
- Gradual static/snow = range limit or obstruction. Normal degradation.
- Sudden black screen = VTX failure, antenna disconnect, or power loss to VTX.
- Rolling lines or interference pattern = self-interference from
  another transmitter on the same airframe (RC, mesh radio).
- Check antenna connector. IPEX/U.FL connectors are fragile. A
  crash can unseat them without visible damage. Reseat and check.
- Check VTX power. Is it set to the right level? Too low = no range.
  Too high = overheating (some VTXs thermal throttle or shut down).

**Digital (DJI, HDZero, Walksnail):**
- Frozen frame = link degradation. Digital doesn't gracefully degrade
  like analog — it works perfectly until it doesn't, then freezes.
- Gray screen / "No Signal" = complete link loss.
- Latency spike = the link is fighting to maintain connection.
  Reduce range or increase power.
- Check firmware versions. DJI goggles and air unit firmware must
  match. Mismatched firmware can cause connection failures.

**Step 2: Is it consistent or intermittent?**
- Consistent at a specific distance/direction = range or obstruction.
  Normal. Adjust flight pattern or antenna.
- Intermittent at close range = self-interference, loose antenna,
  or power supply issue. Check that VTX is getting clean power
  (no voltage sag from motor current).
- Only happens at high throttle = voltage sag pulling VTX supply
  below minimum. Add a capacitor on the VTX power input or use
  a dedicated BEC.

---

## Symptom: Motor Desync / Stuttering

One or more motors stutters, stops momentarily, or makes grinding sounds.

**Step 1: Is it one motor or all?**
- One motor: likely ESC or motor issue (bearing, winding, timing)
- All motors: likely FC signal issue (DShot errors, wiring)

**Step 2: Swap the suspect ESC and motor.** If the problem follows:
- The motor: bad bearing or winding
- The ESC: bad ESC
- Neither (stays on the same arm): wiring issue on that arm

**Step 3: Check motor timing.** In BLHeli_S/BLHeli_32/AM32:
- Stock timing is usually fine. If someone has adjusted it, try
  resetting to default.
- High timing + high KV + low battery voltage = desync recipe.

**Step 4: Check DShot settings.**
- Bidirectional DShot (for RPM filter) can cause desyncs on some
  ESC/motor combinations. Try disabling it to test.
- DShot300 is more reliable than DShot600 on longer signal wires.
  If wires from FC to ESC are >10 cm, try DShot300.

---

## Symptom: Failsafe Triggered in Flight

The drone enters failsafe (lands, returns home, or drops) unexpectedly.

**Step 1: Determine which failsafe.**
- RC failsafe (lost RC link): check RC RSSI in the log. Was signal
  actually lost or did the FC misinterpret a signal issue?
- Battery failsafe: check voltage in the log. Did voltage sag
  below threshold under load?
- GPS failsafe (geofence, GPS loss): check GPS data in log.
- GCS failsafe (ArduPilot/PX4): lost MAVLink heartbeat from GCS.

**Step 2: RC failsafe diagnosis.**
- Check RSSI history in the log. A gradual decline to zero = range.
  A sudden drop = obstruction, interference, or antenna issue.
- Check failsafe settings. Betaflight: `failsafe_procedure`.
  ArduPilot: `FS_THR_ENABLE` + `FS_THR_VALUE`. PX4: `COM_RC_LOSS_T`.
- Is failsafe set to the right response? "Drop" is rarely what
  you want. "Land" or "RTH" are usually better. But RTH requires
  GPS — if GPS isn't locked, RTH failsafe may not work.
- Check RC receiver failsafe behavior. Some receivers output "no pulses"
  on signal loss (correct). Others output last-known values (dangerous
  — FC doesn't know signal is lost). Others output a pre-set failsafe
  position. Verify your receiver's behavior.

**Step 3: Battery failsafe diagnosis.**
- Voltage sag under load can briefly dip below the failsafe
  threshold even when the battery has plenty of capacity.
- Fix: lower the failsafe voltage threshold, or use mAh-consumed
  instead of voltage as the trigger (more reliable).
- Check battery internal resistance. An aging battery sags more
  under load. If your pack used to fly 5 minutes and now triggers
  failsafe at 3 minutes, the battery is dying.

---

## Symptom: GPS Glitch / Toilet Bowl / Position Drift

In GPS-assist modes, the drone circles, drifts, or jumps to a wrong position.

**Step 1: Check satellite count.** Below 8-10 satellites, GPS position
accuracy degrades significantly. Don't use GPS modes with < 8 sats.

**Step 2: Check HDOP.** Horizontal Dilution of Precision. Below 1.5 is
good. Above 2.5 is unreliable. Above 4.0, don't trust GPS position at all.

**Step 3: Toilet bowl = compass problem.** The classic circular drift
pattern means the compass heading is wrong, so the FC "corrects"
in the wrong direction, overshoots, corrects again, and orbits.
- Calibrate compass away from metal, cars, buildings.
- Move external compass away from power wires and motors.
- Check compass orientation matches FC configuration.
- If using internal compass on an FC near ESCs: disable it and
  use external compass only.

**Step 4: Position jumps = multipath or interference.**
- Near buildings, GPS signals bounce off walls, creating phantom
  positions. This is normal in urban environments. No fix except
  dual-band GPS (L1+L5) which is more resistant to multipath.
- Near military installations or during exercises, GPS can be
  jammed or spoofed. If GPS suddenly shows you 50 km away,
  that's not a hardware problem.

---

## The Universal Diagnostic Rule

When something breaks:

1. **Don't change multiple things at once.** Change one thing, test,
   observe. If you change PID, filter, and rates all at once,
   you won't know what fixed (or broke) it.

2. **Pull logs before flying again.** The data is in there. Every
   time you fly without understanding why it broke, you're gambling.

3. **Trust the instruments, not your memory.** "I think it was
   oscillating on roll" is less useful than "gyro roll axis shows
   200 Hz peak at 40% throttle." Log it. Read it. Then fix it.

4. **The simplest explanation is usually right.** Loose prop nut
   causes more crashes than firmware bugs. Check the physical
   hardware first.

---

## Next

- **Chapter 10: Blackbox Logs — What They Tell You** — how to read
  the data that diagnoses everything in this chapter.
- **Chapter 11: PID Tuning for People Who Fly** — the tuning
  workflow that addresses oscillation and performance issues.

---

*Something broke. That's normal. The question is whether you
understand why, or whether you're about to break it again.*
