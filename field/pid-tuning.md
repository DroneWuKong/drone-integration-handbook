# Chapter 11: PID Tuning for People Who Fly, Not Simulate

> PID tuning is not magic. P reacts to error. I removes steady
> error. D resists change. That's it. The rest is learning what
> each one feels like through the sticks.

---

## What P, I, and D Actually Do

### P (Proportional) — The Reaction

P pushes back proportional to how far off the drone is from where
it should be. Big error = big correction. Small error = small correction.

**Too high:** The drone overshoots its target and corrects back,
creating fast oscillation. Feels like the quad is vibrating or
buzzing, especially visible on a punch-out or sharp turn.

**Too low:** The drone feels mushy, soft, unresponsive. It drifts
through commands instead of snapping to them. Slow to respond to
stick input.

**What to listen for:** P oscillation is fast — 10-50 Hz range.
It sounds like a buzz or rattle. If you hear a high-pitched
buzzing that increases when you do aggressive maneuvers, P is
too high.

---

### I (Integral) — The Memory

I accumulates error over time. If the drone is consistently a
little off in one direction (wind pushing it, CG offset, motor
imbalance), I builds up a correction to counter it.

**Too high:** The drone feels "stuck" or slow to change direction.
Overshoot on sustained moves. After a long turn, it keeps turning
briefly after you release the stick. In extreme cases, I windup
causes the drone to suddenly lurch as the accumulated correction
releases.

**Too low:** The drone drifts. In a hover, it doesn't hold position
well. In forward flight, wind pushes it off course and it doesn't
correct. The quad won't hold a steady rate in a turn.

**What to feel for:** I issues are slow. If the drone seems to
"remember" what it was doing and resists changing, I is too high.
If it can't hold a line in wind, I is too low.

**For most operators:** Leave I at the default. It's the least
sensitive of the three terms and the default is usually close
enough. Only touch I if you have specific drift or windup problems.

---

### D (Derivative) — The Brake

D resists change. It's proportional to how fast the error is
changing, not how big it is. D slows down both the drone's
response AND oscillation.

**Too high:** Motors run hot. D amplifies noise (see Chapter 10,
Pattern 3). The drone feels "dampened" — controlled but lacking
snap. In extreme cases, motors make a grinding sound from rapid
micro-corrections driven by noise.

**Too low:** The drone overshoots on quick maneuvers. Feels
bouncy at the end of rolls and flips. P oscillation becomes
harder to control because D isn't there to brake it.

**What to listen for:** D noise is a constant, low-level motor
buzz that's present even in smooth flight. It gets worse with
throttle because motor vibration (which D amplifies) increases
with RPM.

**The D dilemma:** You need enough D to control overshoot but
not so much that it amplifies noise. This is the core tension
in PID tuning and why filters exist — filters clean the gyro
signal so D can do its job without reacting to noise.

---

## The Field Tuning Workflow

This workflow assumes you're starting from a reasonable default
(Betaflight defaults are a good starting point for most 5-inch
builds). If you're building from scratch on unusual hardware,
start with community presets for your motor/frame size.

### Step 0: Mechanical First

Before touching PIDs, confirm:
- Props are balanced and undamaged
- Motors spin freely with no grit or catch
- FC is soft-mounted properly
- Frame has no loose screws or cracked arms
- Battery is secured and not shifting in flight

If any of these are wrong, no amount of PID tuning will fix it.
See Chapter 12 (Troubleshooting), Step 2.

### Step 1: Fly the Default

Fly a representative flight — hover, forward flight, some rolls
and flips, a punch-out, some turns. Pay attention to:
- Does it feel mushy or sharp? (P)
- Does it hold a line in wind? (I)
- Does it bounce at the end of maneuvers? (D)
- Is there any buzzing or vibration? (P too high or D noise)

Pull a blackbox log.

### Step 2: Adjust P

P is where most of the feel comes from. Adjust P first.

- If mushy/soft: raise P by 10%. Fly. Repeat until it feels
  responsive but not buzzy.
- If buzzy/oscillating: lower P by 10%. Fly. Repeat until
  the buzz goes away but it still feels locked in.

**Adjust roll and pitch P together** unless you have a reason
not to (asymmetric frame, different prop spacing). Yaw P is
usually set independently and is less sensitive.

### Step 3: Adjust D

Once P feels right, check D:

- If bouncy at the end of flips/rolls: raise D by 10%.
- If motors are hot or buzzing at idle: lower D by 10%.
- If blackbox shows D-term noise: lower D, then check filters.

D and P interact — raising P often requires raising D to maintain
damping. If you raised P in Step 2, you may need more D.

### Step 4: Leave I Alone (Usually)

I is rarely the problem for freestyle and racing. If the default
works, keep it.

- If the quad drifts in hover or can't hold a turn rate in wind:
  raise I by 10-20%.
- If the quad feels sluggish to change direction or has overshoot
  on sustained turns: lower I.

### Step 5: Check Filters

If you can't get P and D where you want them because noise
starts before you reach the desired gain, the issue is filters,
not PIDs.

- Enable dynamic notch filter if not already enabled.
- Check gyro lowpass filter cutoff. Betaflight default (250 Hz
  for gyro lowpass 1) is fine for clean builds. Noisy builds may
  need 150-200 Hz.
- Check D-term lowpass. This is the most impactful filter for
  D noise. Lowering it from 150 Hz to 100 Hz significantly
  reduces D noise but also slows D response.

**The filter-PID relationship:** Filters remove noise so PIDs
can run higher without reacting to it. A well-filtered build
can run higher P and D, which means sharper and more responsive
flight. A poorly filtered build (or a build with mechanical
vibration issues) must run lower PIDs to compensate.

### Step 6: Fly, Log, Compare, Repeat

After each change:
1. Fly a representative flight (same maneuvers as before)
2. Pull blackbox
3. Compare gyro traces to the previous flight
4. Did it get better or worse? If better, keep the change.
   If worse, revert.

**One change at a time.** If you change P, D, and filters
simultaneously, you won't know what helped and what hurt.

---

## Rates vs. PIDs

Rates and PIDs are different things. People confuse them constantly.

**Rates** control how fast the drone rotates per degree of stick
deflection. Higher rates = faster rotation at full stick. Rates
affect how the drone FEELS to fly but they don't affect stability.

**PIDs** control how well the drone FOLLOWS the rate command.
Higher P = more aggressively follows the command. Higher D =
more damped following.

If the drone feels slow: it might be rates (increase max rate),
not PIDs.

If the drone feels floaty: it might be PIDs (increase P), not rates.

If the drone rotates at the right speed but wobbles while doing it:
that's PIDs.

---

## Tuning for Different Flight Styles

### Freestyle

- Higher P for crisp, snappy response
- Moderate D for controlled stops after flips
- Lower I is acceptable (you're not holding position)
- Slightly higher rates (800-1200 deg/s max)

### Racing

- Moderate P — not as high as freestyle because you need
  predictability, not snap
- Higher D to damp oscillation in high-speed turns
- Higher I to hold lines through corners and in prop wash
- Lower rates than freestyle (600-900 deg/s) for precision

### Cinematic / Smooth

- Lower P for gentle, smooth movements
- Lower D to avoid any micro-corrections visible in footage
- Standard I
- Low rates (400-600 deg/s) for butter-smooth pans

### Long-Range / GPS Cruise

- Default PIDs are usually fine
- I matters more here (wind rejection, position hold)
- D can be lower (less aggressive flying = less noise)
- Rates are less important (you're not doing flips at 5 km)

---

## When to Stop Tuning

The tune is "good enough" when:
- No audible buzz or vibration in normal flight
- The drone responds to stick inputs without delay or overshoot
- Blackbox gyro traces are clean (no sustained oscillation)
- Motors are warm after flight, not hot (hot = D noise or P oscillation
  making the ESCs work too hard)
- You stop noticing the quad and start noticing the flying

Most pilots overtune. The difference between a "good" tune and
a "perfect" tune is 2-3% performance improvement that you'll never
notice in real flying. Get it to "no oscillation, responsive,
motors not hot" and go fly.

---

## Next

- **Chapter 10: Blackbox Logs** — reading the data that drives
  these tuning decisions.
- **Chapter 12: When Things Go Wrong** — when the problem isn't
  PIDs at all.

---

*The best tune is the one that lets you forget about the quad
and focus on the flying. If you're thinking about PIDs in the air,
you're not done tuning. If you're not thinking about PIDs in the
air, you probably are.*
