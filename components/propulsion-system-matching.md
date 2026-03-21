# Propulsion System Matching

Motor, ESC, prop, and battery are a single system. Change one and you've changed all of them. Most build failures — insufficient hover time, thermal shutdown, desync, weak punch-out — trace back to a mismatch somewhere in this chain. This guide walks the selection process from frame weight to battery spec, in the order you should actually make the decisions.

---

## The Selection Order

**Frame weight → thrust-to-weight ratio → motor → prop → ESC → battery**

Never start with the motor. Start with what you need the system to *do*.

---

## Step 1: Establish Your All-Up Weight

All-up weight (AUW) is the total flying weight: frame + motors + ESC + FC + battery + payload + wiring. Before you know your AUW you don't know anything else.

For a first build, estimate: weigh the frame, add ~30g per motor, ~20g for the ESC stack, ~30g for FC + GPS + wiring, then the battery (usually the biggest variable). Your payload weight is fixed — design around it, not against it.

**Rule of thumb for initial estimates:**
- 5" FPV freestyle: 350–450g AUW
- 5" long-range: 500–650g AUW
- 7" long-range: 700–900g AUW
- 10" survey quad: 1.2–2.0kg AUW
- Heavy-lift hex (spray/survey): 4–10kg AUW

---

## Step 2: Set Your Thrust-to-Weight Ratio

Thrust-to-weight ratio (TWR) is total maximum thrust divided by AUW. It determines what the aircraft can *do*.

| Application | Minimum TWR | Recommended TWR |
|---|---|---|
| Stable photography / mapping | 2:1 | 3:1 |
| General utility / survey | 3:1 | 4:1 |
| Freestyle / sport | 4:1 | 6–8:1 |
| Racing | 8:1 | 10–14:1 |
| Payload delivery (heavy-lift) | 2.5:1 | 3.5:1 |

A 2:1 TWR means the motors produce exactly twice the aircraft's weight at full throttle. This sounds like plenty, but it means you're flying at ~50% throttle just to hover — leaving almost no margin for wind, attitude corrections, or payload variation. For anything other than calm, stable survey work, 3:1 is a better floor.

**Calculate required total thrust:**
```
Required thrust = AUW × TWR target
Per-motor thrust = Required thrust ÷ motor count
```

A 700g 5" quad targeting 5:1 TWR needs 3,500g total thrust — 875g per motor on a quad.

---

## Step 3: Select the Motor

### KV Rating

KV is RPM per volt with no load. Higher KV = higher RPM at a given voltage, smaller prop needed. Lower KV = lower RPM, larger prop, more torque, more efficient at extracting thrust from large slow propellers.

**KV × prop size × voltage must balance.** The constraint is that tip speed (prop diameter × RPM) should stay below roughly 200m/s for efficiency, and prop loading (thrust per square centimeter of disc area) should stay in the efficient range.

| Frame / Prop | Battery | Typical KV Range |
|---|---|---|
| 3" micro / cinewhoop | 3–4S | 2000–3000 KV |
| 5" FPV freestyle | 4–6S | 1700–2400 KV (4S), 1400–1700 KV (6S) |
| 5" long-range | 6S | 1300–1700 KV |
| 7" long-range | 4–6S | 1300–1600 KV |
| 10" survey | 4–6S | 700–1200 KV |
| Heavy-lift 15"+ | 6–12S | 100–400 KV |

**Higher voltage = lower KV for the same prop.** Running a 1750 KV motor on 4S (16.8V) gives ~29,400 RPM. The same prop on 6S (25.2V) would give ~44,100 RPM — too fast for most 5" props and brutally inefficient. Drop to ~1200 KV for 6S with a 5" prop to hit the same RPM range.

### Stator Size

Motor stator is described as `WWHHmm`: width × height in millimeters. A 2306 motor has a 23mm wide, 6mm tall stator.

- Larger stator = more copper = more torque = better for larger props
- Taller stator = more winding depth = higher torque at similar width
- Wider stator = faster motor, better for higher RPM applications

| Prop Size | Typical Stator |
|---|---|
| 2–3" | 1103–1306 |
| 3–4" | 1404–1606 |
| 5" | 2203–2306 |
| 6–7" | 2407–2806 |
| 8–10" | 3110–3515 |
| 12"+ | 4012–4114+ |

### Thrust Curves

Always verify thrust against manufacturer data at your target voltage. Rated thrust is usually at full throttle on the test bench — your hover throttle should be 40–60% of max thrust, not 70%+. If you're hovering at 70% throttle you have no margin left.

---

## Step 4: Select the Propeller

### Diameter

Larger diameter = more air moved per revolution = more efficient thrust per watt (at low speed). But larger props are heavier, have more gyroscopic effect, and react more slowly to throttle changes.

Match prop diameter to your motor stator (see table above) and verify clearance in your frame. Standard clearance is at least 10% of prop diameter between the tip and the nearest obstruction.

### Pitch

Pitch is the theoretical distance the prop advances per revolution in inches. Higher pitch = more thrust per RPM at higher airspeeds but less efficient at hover. Lower pitch = more efficient hover but less top speed.

| Application | Pitch Target |
|---|---|
| Hover efficiency / mapping | Low pitch (3–4") |
| General purpose | Medium pitch (4.3–4.5") |
| Speed / aggressive freestyle | High pitch (5–6"+) |

### Blade Count

Two-blade propellers are more efficient at lower RPMs. Three-blade props move more air per revolution (higher thrust at same RPM) but are less efficient. Four-blade props are even less efficient but provide smoother thrust, useful for cinematography where prop wash artifacts matter more than flight time.

### Changing Props Requires Retuning

Every prop change is a PID tuning event. A new prop of the same nominal spec from a different manufacturer — different weight, rigidity, blade profile — will change the aircraft's response. If you swap props, run a Blackbox session and check for oscillations before putting on a camera.

---

## Step 5: Select the ESC

### Amperage Rating

ESC continuous current rating must exceed the motor's maximum current draw with margin.

```
ESC amperage ≥ motor max current × 1.25 (25% margin minimum)
```

Motor max current is on the datasheet, measured at the test voltage with the test prop. Your combination may differ — verify with a watt meter on the first flights.

**4-in-1 vs individual ESCs:**
- 4-in-1: cleaner build, lighter, centralized mass. Standard for 3"–7" builds. Thermal density is higher — heat from all four ESCs in one package.
- Individual: better thermal management, field-replaceable. Better for 8"+ where each motor draws more current.

### Protocol

| Protocol | Type | Notes |
|---|---|---|
| PWM | Analog | Legacy. Avoid on new builds. |
| OneShot125/42 | Analog hybrid | Obsolete. |
| Multishot | Analog hybrid | Obsolete. |
| DShot150/300/600 | Digital | Standard for 2024. Use DShot300 or DShot600. |
| DShot1200 | Digital | For F7/H7 FCs at high loop rates. |
| Bidirectional DShot | Digital + telemetry | Enables RPM filtering. Required for dynamic notch. **Use this.** |
| ProShot | Digital | Rare, not widely supported. |

Use **Bidirectional DShot** on any modern build. It enables RPM-based notch filtering in Betaflight/ArduPilot, which is the single biggest filter improvement available.

### BEC vs OPTO

- **BEC (Battery Eliminator Circuit)**: ESC includes a 5V regulator to power the FC/receiver. Convenient for simple builds but introduces a potential noise coupling path between the power stage and flight controller.
- **OPTO**: No integrated BEC — FC must be powered separately. Eliminates one noise path. Required on high-amperage builds where a BEC would be thermally stressed.

On modern FC stacks with a dedicated 5V regulator on the FC board, OPTO ESCs are often the cleaner choice even on small builds.

### Capacitor

Solder a low-ESR electrolytic capacitor (typically 35V 1000µF or 50V 470µF) as close to the ESC power input as possible. Without it, voltage spikes from motor commutation will reach the flight controller, causing video noise and occasional FC brownouts. This is the number one overlooked step in custom builds.

---

## Step 6: Select the Battery

### Cell Count (Voltage)

Battery voltage directly determines motor RPM (KV × V = RPM). Select cell count to put your motor in the right RPM range for your prop at your target hover throttle.

| Cell Count | Nominal V | Fully Charged |
|---|---|---|
| 1S | 3.7V | 4.2V |
| 2S | 7.4V | 8.4V |
| 3S | 11.1V | 12.6V |
| 4S | 14.8V | 16.8V |
| 6S | 22.2V | 25.2V |
| 8S | 29.6V | 33.6V |
| 12S | 44.4V | 50.4V |

Higher voltage on the same motor gives more power but also more heat. Verify your motor, ESC, and FC are rated for the voltage you're using — this is particularly important on the FC (many are 3–6S only).

### Capacity (mAh)

More capacity = heavier battery = lower effective payload capacity and potentially lower TWR. There's a crossover point where adding battery capacity reduces flight time because the extra weight costs more than the extra energy provides.

**Rough flight time estimate:**
```
Flight time (min) ≈ (capacity_mAh × 0.8) / (average_current_A × 1000) × 60
```

Average current is typically 30–50% of maximum current on a well-matched build at moderate flying.

### C Rating

C rating × capacity_Ah = maximum continuous discharge current.

```
Peak current required = motor_max_current × motor_count
Required C rating = peak_current / capacity_Ah
```

A 4S 1500mAh (1.5Ah) pack powering four 35A-max motors needs to supply up to 140A peak — requiring a C rating of at least 93C. In practice, most LiPo packs are de-rated; buy at least 1.5× the required C rating.

**Chemistry comparison:**

| Chemistry | Energy Density | Discharge Rate | Weight | Cycle Life | Use Case |
|---|---|---|---|---|---|
| LiPo | 150–200 Wh/kg | Very high (C-rated) | Light | 200–400 cycles | Racing, freestyle, high-performance |
| Li-Ion | 200–265 Wh/kg | Moderate (2–5C typical) | Similar | 500–1000 cycles | Long-range, mapping, endurance |
| LiHV | 155–210 Wh/kg | High | Light | 200–350 cycles | FPV, cinematography (4.35V/cell) |
| LiFePO4 | 90–120 Wh/kg | Moderate | Heavy | 2000+ cycles | Heavy-lift, ground vehicles |

Li-Ion is often the right call for long-range or mapping builds where flight time matters more than peak power. A 21700 cell pack will typically give 30–50% more flight time than a same-weight LiPo because of its higher energy density, at the cost of lower peak discharge.

---

## Common Failure Modes and Their Root Causes

| Symptom | Likely Cause | Fix |
|---|---|---|
| Motors hot after short flight | Under-rated KV for voltage; prop too aggressive | Lower KV or cell count; reduce pitch |
| Short flight time | Hover throttle >60%; battery over-C-rated for weight | Higher capacity; lighter battery; lower TWR target |
| ESC thermal shutdown | ESC amperage too close to motor max | 25% margin minimum; add cooling |
| Desync (motor stutter/stop) | ESC timing mismatch; low-quality motor; electrical noise | Recalibrate ESC; try different timing value; add capacitor |
| FC brownout under full throttle | No capacitor; BEC undersized | Add 1000µF cap to power leads; use separate BEC |
| Video gets noisy at high throttle | Motor switching noise on power rail | Add capacitor; route video and power lines separately |
| Oscillations after prop change | PID tune no longer matches new prop inertia | Retune — run Blackbox, adjust D term first |
| Can't lift payload | TWR too low; CG too far from center | Recheck AUW with payload; move battery for CG |

---

## Quick Reference: 5" 6S Freestyle Build

A worked example to illustrate the process:

- **Frame:** 5" 215mm X-frame, ~100g
- **Target AUW:** 450g with 1000mAh battery
- **TWR target:** 6:1 → need 2,700g total thrust → 675g per motor
- **Motor selection:** 2306 1400KV on 6S → peaks at ~900g thrust per manufacturer data ✓
- **Prop selection:** 5.1×4.1 3-blade HQ prop → designed for this motor/voltage combo
- **ESC:** 4-in-1 45A BLHeli_32 with bidirectional DShot → motor peaks at ~35A, 45A gives 28% margin ✓
- **Battery:** 6S 1000mAh 100C LiPo → 100A peak discharge, motor peak ~140A (marginally tight — consider 1300mAh)
- **Capacitor:** 35V 1000µF across ESC power pads ✓

The battery is slightly marginal here — the 1000mAh 100C pack provides 100A discharge vs 140A peak demand. A 1300mAh pack at 80C gives 104A (still marginal) or a 1500mAh at 100C gives 150A (comfortable margin but heavier). This is the typical LiPo weight-vs-margin tradeoff for freestyle builds.
