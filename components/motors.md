# Motors — Who Actually Makes Them

> **Part 6 — Components**
> The parts that go into the drone, where they come from,
> and what the compliance landscape actually looks like.

---

## The Supply Chain Reality

The global drone motor market has a simple structure: China makes
most of them. Estimates vary, but roughly 73% of the world's FPV
drone motors are Chinese-manufactured. This includes many brands
that market themselves as American, European, or otherwise — the
motors are designed elsewhere but manufactured in China.

This matters because NDAA Section 889 and the American Security
Drone Act (ASDA, effective December 2025) prohibit federal agencies
from purchasing drone components from "covered foreign entities."
Starting with DDG Phase II and NDAA FY2026 battery provisions,
the restrictions are tightening further — motors and batteries from
covered countries will be explicitly prohibited in DoD programs.

For operators who don't face procurement restrictions, Chinese motors
remain the most cost-effective option at roughly $70–100/unit for
quality FPV motors. The price gap matters: comparable NDAA-compliant
motors run $150–500+ depending on class.

This chapter covers the real global motor landscape — who makes
what, where, and what the compliance picture actually looks like.

---

## Ukraine — The Combat-Proven Ecosystem

Ukraine consumed roughly 9.6 million drone motors in 2025. The
country operates the most combat-proven UAS ecosystem on earth,
and its motor manufacturers have been refined by continuous battlefield
feedback at a pace no test range can replicate.

### Motor-G

Ukraine's largest drone motor manufacturer. Founded after the
full-scale Russian invasion by Oleksii Grebin and three co-founders
(two from drone production, two from industrial HVAC). Self-funded
with millions of dollars, no external investment.

| Detail | Value |
|--------|-------|
| HQ | Ukraine (location undisclosed for security) |
| Production | 200,000 motors/month (as of March 2026) |
| Market Share | ~17% of Ukraine's motor market |
| Customers | 100+ drone manufacturers including Vyriy, General Cherry |
| QA | 6-stage inspection, 2/1000 defect rate |
| Localization | 85% Ukrainian-sourced, targeting 90%+ (stators 100% localized from May 2026) |
| CEO | Oleksii Grebin |
| Growth | 181 units (Dec 2024) → 200,000/month (12 months) |
| R&D | In-house — custom motors to spec available |

**Product Line:**
- 9 standard FPV motor models covering 5"–15" frame sizes
- **Vandal** — interceptor motor for 3–5 kg drones, designed for
  speeds exceeding 350 km/h. Priced above Chinese equivalents.
  Minister of Defence Fedorov reported Motor-G equipment enabling
  an anti-aircraft drone to reach 400 km/h.
- Expanding into UGV and heavy bomber motors
- Persian Gulf interest in interceptor drone applications

**Remaining imports:** Small magnets, bearings, some voltage testing
equipment. The company notes that EU motor production is effectively
nonexistent — European brands are typically Chinese-manufactured.

**Lean manufacturing model:** Motor-G ships in small batches matched
to customer production rates, avoiding the Chinese model of paying
for and waiting on tens of thousands of units at once.

### Aeromotors

Ukraine's second-largest motor manufacturer. ~10,000 motors/month.
All components manufactured in-house. €467K ($550K) investment from
Swedish Front Ventures (end 2025). Custom motors to spec. Motor-G's
primary domestic competitor.

### Other Ukrainian Motor Manufacturers

- **Bullet** — Claims 450 km/h interceptor motors
- **Realgold** — Previously used by Vyriy before Motor-G partnership
- **~8 total competitors** in the Ukrainian market (per Motor-G CEO)

### The Ukrainian Advantage

Ukrainian motors cost roughly $150/unit — twice the Chinese price
but half the US price. The real advantage isn't cost, it's iteration
speed. Troops test motors in combat daily and feed results back
immediately. A Ukrainian motor with 200,000+ combat sorties of
validation data is more credible than a US motor with zero field
hours, regardless of what the spec sheet says.

---

## United States — NDAA-Compliant Motors

### UMAC / Unusual Machines / EU Motors USA

Blue UAS Framework listed. Scaling local manufacturing in Orlando, FL.
50,000+ motors/month capacity.

| Detail | Value |
|--------|-------|
| HQ | Orlando, FL, USA |
| Blue UAS | Framework component |
| NDAA | Compliant |
| Facility | 17,000 sq ft manufacturing |
| Key Products | UMAC 2207 (5"), UMAC 2807 (7" — used in Red Cat FANG F7), UMAC 3220 (larger format) |
| UMAC 2807 Specs | 28×7mm stator, N552SH magnets, 12mm bearings, 3-8S |
| Customers | Red Cat ($800K initial FANG components order), PBAS selectees |
| Acquisition | Rotor Lab (Australia) acquired Sep 2025 for $7M |

### KDE Direct

US-designed heavy-lift and industrial motors. 10+ years in market.

| Detail | Value |
|--------|-------|
| HQ | Bend, OR, USA |
| Designed | USA |
| Manufacturing | USA + abroad (verify specific models) |
| IP Rating | IP56 / IP66 (model dependent) |
| Certifications | ISO 9001, CE, WEEE |
| Range | 1806 mini through 13218XF heavy-lift |
| Applications | Hollywood aerial cinema, LiDAR, SAR, military, agriculture |
| NDAA | Designed in USA — verify manufacturing origin per model |

KDE also manufactures ESCs tuned and optimized for their motor
line. Their "Build Your System" tool helps match motors to
airframes and payloads.

### Vertiq

Integrated motor+ESC modules with embedded position sensor.
Blue UAS Framework listed. NDAA compliant.

| Detail | Value |
|--------|-------|
| HQ | USA |
| Blue UAS | Framework component (81-08 G2 module) |
| NDAA | Compliant |
| Key Feature | Integrated motor + ESC + position sensor in one module |
| Compatibility | ArduPilot, PX4 native support |
| Product Line | 23-06, 23-14, 40-06, 40-14, 60-08, 81-08, 81-17 modules |
| Applications | Commercial, defense, high-value aerial vehicles |

Vertiq's position sensor enables precise propeller positioning
in-flight and on landing — relevant for applications requiring
consistent blade orientation (folding props, coaxial).

### Dronesmith USA

Purpose-built for government/defense. NDAA §889 compliant with
verified US supply chain. Prohibited vendors excluded. Traceable
components with vendor attestations. Pre-production designs
covering mid-lift, 5–7" tactical FPV/ISR, and heavy-lift classes.

### Lumenier

Premium FPV/cinema brand based in Sarasota, FL. ZIP series motors.
In parts-db for some products. **Verify manufacturing origin per
model** — some Lumenier products are manufactured in China despite
US brand identity.

### Other US Motor Manufacturers

- **NeuMotors** — High-end, extreme efficiency, aerospace research
- **LaunchPoint EPS** — Dual-Halbach axial flux motors, hybrid-electric propulsion, eVTOL
- **Allied Motion / Allient** — Precision brushless for defense, aviation, medical. Gimbal + propulsion
- **USA Drone Motors** — Built-to-print or standard specs, NDAA BLDC
- **Moog** — Aerospace/defense-grade actuation and propulsion

---

## European Union

### Scorpion Power Systems

| Detail | Value |
|--------|-------|
| HQ | Prague, Czech Republic |
| Manufacturing | EU |
| Range | Competition and commercial UAS motors |
| NDAA | Non-Chinese manufacturing — likely compliant but verify |

### Plettenberg Motoren

German manufacturer. High-end industrial and defense brushless
motors. Premium pricing.

### Hacker Motor

German manufacturer. Competition and industrial brushless motors.
Well-established in the European RC/UAS market.

### The EU Gap

As Motor-G's CEO noted: European motor "brands" exist, but actual
EU manufacturing is rare. Most European-branded motors are
Chinese-manufactured. This is a significant supply chain vulnerability
for European defense programs, and several EU nations are in
early discussions about localizing motor production.

---

## Australia

### Hargrave Technologies

Not a motor manufacturer but critical to mention here — Hargrave
makes NDAA-compliant ESCs (the other half of the propulsion system).

| Detail | Value |
|--------|-------|
| HQ | Australia |
| NDAA | Compliant — Western-sourced components |
| Key Products | nanoDRIVE 4LPi (4-in-1 ESC), microDRIVE LP (IP67) |
| Protocols | DroneCAN, ARINC825, DShot, PWM |
| Deployed | 10,000+ aircraft in 50+ countries |
| Recognition | Sovereign Capability Defence Grant recipient |

---

## China (Context)

Chinese motors dominate the global market (~73% of Ukraine's
market alone). Key manufacturers include T-Motor, MAD Components,
and dozens of smaller OEMs. Pricing runs $70–100/unit for quality
FPV motors — roughly half the Ukrainian price and a third of
the US price.

**T-Motor** is the most recognized Chinese motor brand in
professional/commercial UAS. Already in the parts-db but needs
compliance flags added to all entries: **NOT NDAA compliant.**

Chinese motors are NOT recommended for any NDAA, Blue UAS, or
government-adjacent builds. However, they remain the reality for
most commercial operators worldwide and the Handbook should
document them accurately — operators need to know what exists,
not just what procurement officers can buy.

---

## The Price Reality

| Origin | Typical FPV Motor Cost | NDAA Status |
|--------|----------------------|-------------|
| China | $70–100 | NOT compliant |
| Ukraine | ~$150 | Not applicable (non-NDAA nation, but non-Chinese) |
| EU (actual mfg) | $150–300 | Likely compliant (verify per product) |
| USA | $200–500+ | Compliant (verify per product) |
| USA (integrated module, e.g. Vertiq) | $300–800 | Blue UAS Framework |

Any NDAA/supply chain discussion must acknowledge this price gap.
The DDG Phase II Chinese components ban will force Phase I winners
currently using Chinese motors to absorb a 2–5x cost increase
on propulsion alone.

---

## Choosing Motors: What Matters

1. **Match the motor to the prop and voltage.** Every motor has an
   optimal prop size and cell count. Running outside that range
   wastes energy or risks burnout.

2. **Stator volume determines power.** Width × height (e.g., 2807 =
   28mm wide, 7mm tall). Larger stator = more torque = heavier props
   and payloads.

3. **KV determines RPM per volt.** Higher KV = higher RPM = smaller
   props. Lower KV = more torque = larger props. Match to your
   application.

4. **Compliance is a procurement constraint, not a quality indicator.**
   A Chinese T-Motor may outperform an NDAA motor on a spec sheet.
   The NDAA motor exists because procurement rules require it.

5. **Combat-proven > spec sheet.** If a motor has been validated
   across thousands of real-world sorties (Motor-G, Neros), that
   data is worth more than any test bench report.

---

*Last updated: March 2026*
