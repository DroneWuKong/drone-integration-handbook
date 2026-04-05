# Propellers

> Propellers are the largest single category in the Forge database at 484
> entries. They're also the most frequently replaced component — crashes,
> vibration wear, and performance tuning all drive prop swaps. Choosing the
> right propeller is a direct tradeoff between thrust, efficiency, noise,
> and flight feel.

**Forge DB:** 484 propellers (HQProp 211, Gemfan 179, APC 19, Azure Power 16)
**Cross-references:** [Propulsion Matching](propulsion-system-matching.md) ·
[Motors](motors.md) · [ESCs](escs.md) ·
[Frames](frames-airframe-selection.md) ·
[PID Tuning](../field/pid-tuning.md)

---

## Reading a Prop Spec

Propeller size is expressed as **diameter × pitch** in inches, sometimes
followed by blade count. For example:

**5145×3** = 5.1" diameter, 4.5" pitch, 3 blades (tri-blade)

- **Diameter** — distance from tip to tip. Must fit your frame.
- **Pitch** — theoretical distance the prop advances in one revolution (in
  inches). Higher pitch = more speed but more current draw. Lower pitch =
  more hover efficiency and less aggressive feel.
- **Blade count** — 2 (bi-blade), 3 (tri-blade), or 4+ (quad-blade).

---

## Blade Count

| Blades | Count in Forge | Characteristics |
|--------|---------------|-----------------|
| Bi-blade | 40 | Most efficient, smoothest, least thrust per diameter. Long range, cruising. |
| Tri-blade | 267 | The standard. Best balance of thrust, efficiency, and control feel. Freestyle/racing default. |
| Quad-blade | 109 | Maximum grip and thrust per diameter. Most current draw. Cinematic smoothness, heavy quads. |

**Tri-blade dominates** because it's the sweet spot — enough thrust for
aggressive maneuvering, enough efficiency for reasonable flight times, and
enough damping for smooth video.

**Bi-blade** is the long-range choice. Less thrust means less drag in forward
flight, and lower current draw extends flight time. Used on 7" and 10" long-
range builds where efficiency matters more than agility.

**Quad-blade** provides maximum grip in the air — more responsive to throttle
inputs, better in propwash. Draws significantly more current. Used on heavy
builds (HD camera, payload) and cinematic quads where smooth authority matters.

---

## Size Classes

| Prop Size | Frame Class | Motor Size (typical) | Battery | Use Case |
|-----------|------------|---------------------|---------|----------|
| 3" / 3.5" | 3" micro | 1404–1507 | 2–4S 450–850 mAh | Cinewhoops, indoor, micro FPV |
| 4" | 4" | 1507–2004 | 4S 850–1300 mAh | Compact freestyle, proximity |
| 5" / 5.1" | 5" | 2205–2306 | 4–6S 1100–1500 mAh | Freestyle, racing, general FPV |
| 6" | 6" | 2207–2507 | 4–6S 1300–1800 mAh | Long range, cruising |
| 7" | 7" | 2806–3115 | 6S 1500–2200 mAh | Long range, payload, tactical |
| 9"–10" | 10" | 3115–4014 | 6S 3000–6000+ mAh | Heavy lift, bomber, payload delivery |

The 5-inch class accounts for over half the propellers in the database (247
of 484), reflecting its dominance in FPV.

---

## Pitch Selection

Pitch is the most impactful spec after diameter. Think of it as the prop's
"gear ratio."

### Low Pitch (3.0–3.5")

- More hover efficiency (less throttle needed to maintain altitude)
- Smoother throttle response
- Lower top speed
- Lower current draw
- Best for: long range, cinematics, cruising, heavy builds

### Medium Pitch (4.0–4.5")

- Balance of efficiency and speed
- Standard freestyle feel
- Moderate current draw
- Best for: general FPV, freestyle, training

### High Pitch (4.8–5.5"+)

- Maximum speed and acceleration
- Aggressive throttle response
- High current draw (stresses ESCs and battery)
- Less efficient at hover
- Best for: racing, fast freestyle, experienced pilots

**Rule of thumb:** if you're building for flight time, go lower pitch. If
you're building for speed, go higher pitch. Most pilots land on 5x4.3 or
5.1x4.5 tri-blade as their default.

---

## Prop Materials

### Polycarbonate (PC)

The standard FPV prop material. Durable, flexible enough to survive minor
impacts without shattering, holds its shape reasonably well. Most HQProp and
Gemfan props are PC.

### Glass Fiber Nylon

Stiffer than polycarbonate. Better efficiency (less flex under load = less
energy lost to blade deformation). More brittle — shatters on hard impacts
rather than bending. Some racing and premium props use this.

### Carbon Fiber Reinforced

Stiffest option. Best efficiency at high RPM. Very brittle — shatters
violently on impact. Used in some racing and premium long-range props.
Expensive and not practical for training or high-crash-rate use.

### Unbreakable / Durable Variants

Some manufacturers (Gemfan "Durable" series, HQProp "Durable" series) offer
softer, more flexible variants specifically designed to survive crashes. They
sacrifice some efficiency for longevity. Good for training and beginners.

---

## Prop Balance

Out-of-balance props cause vibration, which degrades:
- Gyro readings → poor PID performance
- HD video quality → jello artifacts
- Motor bearing life → premature failure
- FC sensor accuracy → altitude hold drift

**How to check:** magnetic prop balancer. Place the prop on the balancer —
if one blade dips, it's heavier. Sand or scrape the heavy blade tip until
it balances level.

**When to balance:** always on a new build, and whenever you notice increased
vibration after prop replacement. Racing pilots often skip this; long-range
and HD cinematographers never skip it.

---

## Prop Direction and Motor Mapping

FPV quads use two CW (clockwise) and two CCW (counter-clockwise) props:

```
        CW(2)    CCW(1)
           \      /
            [FC]
           /      \
        CCW(3)   CW(4)
```

Betaflight's default motor order (looking down, nose forward):
- Motor 1 (rear right) — CCW
- Motor 2 (front right) — CW  
- Motor 3 (rear left) — CW
- Motor 4 (front left) — CCW

**Props in** (blades rotating toward the center on top) is the Betaflight
default. This configuration provides slightly better yaw authority and
propwash handling.

**Props out** (blades rotating away from center on top) is an alternative
some pilots prefer for different wash characteristics. Requires reversing
motor direction in firmware.

---

## Prop Damage Assessment

After every crash, inspect props before flying again:

- **Chips or missing blade tips** — replace immediately. Unbalanced, vibration
  will damage everything downstream.
- **Bent blades** — PC props can sometimes be bent back. Fiber-reinforced props
  cannot — replace.
- **Stress whitening** — white marks at the root or along the blade indicate
  stress fracture. The prop may hold for a flight or snap mid-air. Replace.
- **Leading edge nicks** — small nicks from grass/debris are usually fine.
  Large gouges or deformation = replace.

Props are cheap. Motors, FCs, and cameras are not. When in doubt, replace
the prop.

---

## Military / Tactical Considerations

### Noise Signature

Propellers are the primary source of drone noise. Lower RPM = quieter.
This favors larger props at lower pitch (7" or 10" bi-blade) for reconnaissance
and approach. Some military programs are exploring specially shaped blade tips
to reduce noise signature.

### Attritable Supply

For military FPV operations at scale (Ukraine produces 8+ million drones/year),
prop supply chain matters. HQProp and Gemfan (both Chinese) dominate the
market. PROP UA (Ukrainian) produces locally. Supply chain diversification
is an active concern — see [NDAA Compliance](ndaa-compliance.md).

### Prop Selection for Strike Drones

Strike FPV drones (one-way attack) optimize differently than reusable builds:
- Maximum speed to target → high pitch, aggressive props
- Single flight only → durability irrelevant, cheapest option wins
- Current draw less important → battery sized for one mission
- Noise less important on attack run → priority is closing speed

Reconnaissance FPV drones optimize for:
- Maximum loiter time → low pitch, efficient props
- Minimum noise → large diameter, low RPM
- Reusability → durable props

---

## Notable Manufacturers

| Manufacturer | Count | Known For |
|-------------|-------|-----------|
| HQProp | 211 | Largest selection, excellent quality, wide range from racing to long-range |
| Gemfan | 179 | Strong second, "Durable" series for crash resistance, Hurricane series |
| APC | 19 | Fixed-wing and large prop specialist, precision-molded |
| Azure Power | 16 | Premium racing props, glass fiber nylon |
| DALProp | 14 | Budget-friendly, cyclone design |
| PROP UA | 5 | Ukrainian manufacturer, local production for military supply chain |

---

## Quick Selection Guide

| Build Type | Recommended Prop | Why |
|-----------|-----------------|-----|
| 5" Freestyle | 5.1x4.5x3 (HQProp Ethix S5 / Gemfan 51466) | Balanced thrust/efficiency |
| 5" Racing | 5.1x3.1x3 or 5x4.8x3 | Low drag / max speed |
| 5" Cinematic | 5.1x3.5x4 | Smooth authority, good in propwash |
| 7" Long Range | 7x3.5x2 | Maximum efficiency, lowest current |
| 7" Payload | 7x4x3 | Thrust for weight, reasonable efficiency |
| 10" Heavy Lift | 10x4.5x2 | Big diameter, low pitch, heavy lift |
| 3" Cinewhoop | 3x1.5x4 (ducted) | Smooth, quiet, indoor safe |

---

## Sources

- Forge parts database (484 propellers)
- Oscar Liang, propeller selection guides
- Manufacturer specifications (HQProp, Gemfan, APC, Azure Power)
- Propulsion system matching theory (see cross-reference)
