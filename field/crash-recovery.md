# Crash Recovery & Field Repair

> You crashed. Now what? This guide covers post-crash assessment, field-
> repairable damage vs return-to-bench issues, and getting back in the air
> as fast as possible. For high-volume operations (training, military),
> crash recovery speed is a force multiplier.

**Cross-references:** [Preflight](preflight.md) ·
[Troubleshooting](troubleshooting.md) ·
[Frames](../components/frames-airframe-selection.md) ·
[Motors](../components/motors.md) ·
[ESCs](../components/escs.md) ·
[Propellers](../components/propellers.md) ·
[Blackbox](blackbox.md)

---

## Immediate Post-Crash

1. **Disarm and disconnect battery.** Don't approach a crashed quad with a
   live battery. Props can spin unexpectedly. If the quad is inverted, flip
   it before disconnecting — some ESCs re-arm on flip detection.

2. **Check for smoke or heat.** An ESC burning smells like burnt electronics.
   A shorted LiPo smells acrid and may swell. If the battery is puffing,
   hot, or damaged, move it to a safe area immediately. Do not attempt to
   charge a crashed battery without inspection.

3. **Visual sweep.** Before touching anything, look at the quad from multiple
   angles. Note what's broken, bent, or missing. Take a photo if this is a
   build you're tracking in Tooth.

---

## Damage Assessment Checklist

Work through this in order — each step catches issues that affect downstream
components.

### Props

Most common crash damage. Check all four props for chips, bends, cracks, or
stress whitening at the root. Replace any damaged prop — they're the cheapest
component and an unbalanced prop stresses everything else.

### Arms

Flex each arm gently. A cracked carbon arm may look intact but flex at the
fracture. Listen for creaking. Check the arm-to-body bolts (if replaceable
arm design). Loose bolts = the arm absorbed impact force. Retorque.

### Motors

Spin each motor by hand with the prop removed. They should spin freely and
smoothly with no grit, grinding, or catching. Check for:

- **Bent motor shaft** — the bell wobbles visibly when spun. Replace the
  motor or the shaft (some motors have replaceable shafts).
- **Bearing damage** — grinding feel, rough spots, or excessive play in the
  bell. Replace the motor.
- **Bell dent** — the motor bell hit the ground and is deformed. May still
  spin but will vibrate. Replace.
- **Magnet shift** — rare but possible on hard impacts. Motor feels "coggy"
  when turned by hand (distinct detent positions). Replace.

### Camera

Check the lens for cracks. Check the mount for breaks. TPU mounts absorb
impact — check that the TPU hasn't torn. If using a naked action camera
(GoPro/Insta360 board), check the ribbon cables and board for cracks.

### VTX Antenna

Check the antenna connector (SMA, MMCX, UFL). A bent SMA connector or a
pulled UFL pigtail is a common crash failure. A damaged antenna connector
reduces video range dramatically and may not be obvious until you fly.

### Stack

Open the top plate and visually inspect the FC and ESC. Check for:

- **Loose standoffs** — retorque
- **Cracked PCB** — visible crack lines, especially near mounting holes
- **Dislodged components** — SMD parts knocked off the board
- **Loose connectors** — JST-SH and wire-to-board connectors can pull free

### Battery

Inspect the LiPo:

- **Dented or punctured** — STOP. Remove to safe area. Do not use.
- **Puffed** — the pack has swelled. Mild puffing after crash impact is
  common and often acceptable. Significant puffing = internal damage.
  Retire the pack.
- **Connector damage** — bent XT60 pins, cracked solder joints on the
  balance lead.
- **Cell voltage check** — use a cell checker. If any cell is below 3.0V
  after crash, the battery may have been shorted internally. If cells are
  unbalanced by more than 0.3V, the pack may be damaged.

---

## Field-Repairable vs Bench-Required

| Damage | Field Fix | Bench Required |
|--------|-----------|---------------|
| Broken prop | ✅ Swap prop (carry spares) | — |
| Loose arm bolts | ✅ Retorque with field tool | — |
| Bent motor bell | — | ✅ Motor replacement |
| Snapped antenna | ✅ Swap if carrying spare | ✅ Re-solder pigtail |
| Cracked arm | ✅ Zip tie splint (temporary) | ✅ Arm replacement |
| Loose FC connector | ✅ Re-seat and press | ✅ Re-solder if broken |
| Dented LiPo | — | ✅ Retire pack |
| Cracked camera lens | — | ✅ Replace camera/lens |
| ESC magic smoke | — | ✅ Replace ESC |
| GPS mast snapped | ✅ Tape/zip-tie temporary | ✅ Reprint mount |

---

## Field Kit

Minimum field repair kit for FPV operations:

- Spare props (at least 2 full sets)
- Spare battery straps (they break)
- M3 and M2 hex drivers (frame and stack bolts)
- Small zip ties
- Electrical tape
- Spare antenna (pigtail with connector)
- Cell checker / battery tester
- Small flush cutters
- Tweezers (for re-seating connectors)
- XT60 pigtail (for battery connector swap)

For military/training operations at scale, add: spare motors, spare arms,
solder kit with battery-powered iron, conformal coating pen, and a spare FC.

---

## Post-Crash Flight Test

Before committing to a full mission after crash repair:

1. **Arm at low throttle** — listen for abnormal motor sounds, vibrations,
   or oscillations.
2. **Hover at 1 meter** — check for drift, wobble, or toilet-bowling (GPS
   compass issue from magnetized frame/motor).
3. **Gentle maneuvers** — roll, pitch, yaw at low rates. Check for sluggish
   or uneven response.
4. **Check OSD** — verify battery voltage reads correctly, GPS lock is normal,
   RSSI/LQ is expected.
5. **Land and inspect** — check motor temps by touch (brief touch — they
   should be warm, not burning). One hot motor = possible bearing damage or
   bent shaft adding load.

If anything feels wrong, land and inspect. Flying a damaged quad risks
losing it entirely.

---

## Crash Logging

For builds tracked in Tooth (maintenance/forensic tracking):

- Log the crash with date, flight number, and severity
- Note which components were damaged and what was replaced
- Attach photos of damage
- Track cumulative crash count per component — motors and ESCs have fatigue
  limits

For Blackbox-equipped builds, the crash flight's Blackbox log can reveal
what happened — control input spikes, motor output saturations, gyro
vibration signatures, and failsafe triggers.

**See:** [Blackbox](blackbox.md) for log analysis.

---

## Sources

- Field experience and training program best practices
- Oscar Liang, crash recovery and motor inspection guides
- Forge troubleshooting database (58 entries)
