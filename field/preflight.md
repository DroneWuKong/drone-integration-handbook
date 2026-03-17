# Chapter 9: Pre-Flight Checklist That Actually Works

> The manufacturer's checklist is marketing. This one catches
> the problems that actually ground you.

---

## The 60-Second Field Check

This is the minimum check before every flight. Takes 60 seconds
once you've done it a few times. Skipping it takes longer when
you have to walk 500 meters to recover a crashed drone.

### Visual (15 seconds)

1. **Props:** All four present, correct rotation, no nicks, nuts tight.
   Spin each by hand — should rotate freely with no catch.

2. **Frame:** No cracks on arms. No loose standoffs. Antenna mounts
   intact. Nothing rattling when you shake it.

3. **Battery:** Strapped tight. Will not shift under acceleration.
   Balance lead tucked, not dangling near props.

4. **Antenna position:** RC antenna elements deployed (not folded
   under the frame). VTX antenna pointed up/back, not blocked by
   battery. GPS antenna has clear sky view.

### Power-On (30 seconds)

5. **Voltage check:** Battery voltage matches expected full charge.
   4S = 16.4–16.8V. 6S = 24.6–25.2V. If significantly low,
   the battery wasn't fully charged or a cell is bad. Don't fly it.

6. **Gyro cal:** Wait for the FC to finish gyro calibration (usually
   1-2 seconds after power on). Don't move the quad during this time.
   On Betaflight the OSD shows "CALIBRATING" then clears.

7. **RC link:** Confirm connected. Move sticks — verify response on
   OSD or in the video feed (stick position overlay if enabled).
   Check that arming switch is in disarmed position.

8. **GPS (if equipped):** Check satellite count. Wait for 3D fix.
   Most firmwares show sat count on OSD. Minimum 8 sats for any
   GPS-dependent mode. More is better. If you need GPS return-to-home,
   confirm the home point is set (some firmwares set home on arm,
   others on first GPS lock).

9. **Video feed:** Confirm you see a live image in your goggles or
   monitor. Correct channel. No interference patterns. If analog,
   check that nobody else is on your channel.

### Arm Check (15 seconds)

10. **Clear the area.** Nobody within 3 meters of the drone. Nothing
    the drone could hit if it does something unexpected on arm.

11. **Arm.** Motors should spin at idle (or not, if "Motor Stop" is
    enabled). Listen for any unusual sounds — grinding, clicking,
    uneven RPM.

12. **Control check (optional but recommended on new builds):**
    With the drone on the ground, briefly blip throttle and check
    that it tries to lift evenly. Tilt the quad by hand — motors
    should speed up on the low side to self-level (in angle/level mode)
    or resist the tilt (in acro/rate mode).

**Go fly.**

---

## The Deep Check (Pre-Session or New Build)

Do this once per session (before the first flight of the day) or
after any change to the build (new props, firmware update, parameter
change, crash repair).

### Electrical

- [ ] Battery internal resistance: check with charger. Per-cell IR
      above 15 mΩ on LiPo or above 30 mΩ on Li-Ion means the pack
      is aging. Above 25 mΩ (LiPo) or 50 mΩ (Li-Ion), retire it.
- [ ] Cell balance: all cells within 0.02V of each other at full charge.
      Imbalance > 0.05V = failing cell. Don't fly it.
- [ ] ESC temperature after a flight: warm is normal. Hot to touch
      = something is wrong (motor issue, prop drag, ESC undersized).
- [ ] Motor temperature: same. Warm = normal. Hot = mechanical issue,
      PID/filter problem, or motor failing.
- [ ] Wiring: no frayed wires, no exposed copper, solder joints intact.
      Pay special attention to battery pigtail and motor phase wires.

### Mechanical

- [ ] Prop adapters / prop nuts: torqued properly. A prop coming off
      in flight is not recoverable.
- [ ] Motor bell screws: C-clip or set screws tight. Bell should not
      wobble on the shaft.
- [ ] Camera mount: secure. Camera angle correct. Tilt hasn't shifted.
- [ ] FC mounting: soft mount grommets intact, FC not contacting frame.
- [ ] Antenna connectors: U.FL/IPEX connectors seated. SMA connectors
      finger-tight (do not overtorque SMA — you'll break the connector
      on the board).

### Software

- [ ] Firmware version: matches what you expect. Verify in configurator
      before flying after any work session where USB was connected.
      Accidental firmware flash happens.
- [ ] Modes: verify arm switch, flight mode switches, and any other
      switches are assigned correctly. A mode switch that accidentally
      triggers GPS rescue at 2 meters altitude is a bad day.
- [ ] Failsafe: configured and tested. The only way to know failsafe
      works is to test it. Turn off the transmitter with the drone
      armed on the ground and verify the FC does what you expect
      (motors stop, or enters land mode, or whatever you configured).
- [ ] Blackbox: enabled, flash has space. If you want logs from this
      session, verify logging is on and the flash isn't full.
- [ ] OSD: shows what you need. Minimum: battery voltage, flight time,
      RSSI (or LQ for ELRS). Recommended: sat count, altitude, warnings.

---

## Post-Flight Check

After each flight, before the next:

1. **Battery voltage:** Check remaining voltage. If below 3.5V/cell
   under resting conditions, you pushed too hard. Adjust your timer.

2. **Temperature sweep:** Touch each motor, each ESC, the FC, the VTX.
   Anything unusually hot compared to normal? Investigate before
   flying again.

3. **Visual scan:** Any new damage? Props nicked? Antenna bent?
   Camera mount shifted?

4. **Log pull (if analyzing this session):** Pull blackbox now.
   Flash will be overwritten by the next flight.

---

## Post-Session

After the last flight of the day:

1. **Storage charge batteries.** LiPo storage voltage is 3.8V/cell
   (22.8V for 6S). Do not leave batteries at full charge or fully
   depleted. Storage charge the same day.

2. **Clean the quad.** Grass, dirt, and moisture accelerate corrosion
   on exposed electronics. Compressed air for motor bells.

3. **Note anything that needs attention.** A prop you noticed was
   slightly nicked. A motor that felt warm. A GPS that took too long
   to lock. Write it down or you'll forget by next session.

---

## The Checks That Catch Real Problems

In order of how often they prevent incidents:

1. **Props** — wrong rotation, damaged, or loose. The most common
   cause of unexpected behavior on arm or immediately after takeoff.

2. **Battery strap** — a battery that shifts forward on a punch-out
   changes the CG and the drone flips. Cinch it tight.

3. **RC link** — flying on a dead receiver because you forgot to
   check the link. Especially after changing receiver firmware or
   binding phrase.

4. **Failsafe** — having the wrong failsafe behavior configured.
   "Drop" is almost never what you want. Test it before you need it.

5. **GPS home point** — flying 2 km out, triggering RTH, and having
   the drone return to a GPS position from three flights ago because
   you didn't wait for a fresh fix.

6. **Antenna** — a U.FL connector that popped off a receiver during
   a battery change. Video or RC works at 5 meters, fails at 50.

---

## The One Check Nobody Does (But Should)

**Turn off your transmitter with the drone armed on the ground.**

This tests your failsafe. Every time you change firmware, change
receivers, or change failsafe settings, do this test. It takes
10 seconds and it's the only way to know what will actually happen
when you lose signal in the air.

If the motors keep spinning at the last throttle position: your
failsafe is misconfigured and your drone will fly away on signal loss.
Fix it before flying.

---

## Next

- **Chapter 12: When Things Go Wrong** — when something slips past
  the checklist.
- **Chapter 10: Blackbox Logs** — analyzing what happened after
  the flight.

---

*The checklist is boring. Walking half a kilometer to pick up a
crashed drone because you didn't check the prop nuts is also boring,
and takes longer.*
