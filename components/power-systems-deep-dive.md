# Power Systems Deep Dive

> Every UAS failure chain eventually traces back to power. Voltage sag
> kills motors. Brownouts reset FCs mid-flight. Bad BECs corrupt GPS.
> Getting power right is the foundation everything else sits on.

---

## Battery Chemistry

### LiPo (Lithium Polymer)

The default for FPV and short-duration multirotor. High discharge rate,
light weight, but degrades fast and is fire-hazardous when damaged.

| Spec | Typical Range | Notes |
|------|--------------|-------|
| Energy density | 150–200 Wh/kg | |
| C-rate (continuous) | 25–100C | Higher C = heavier |
| Cycle life | 100–300 cycles | 80% capacity threshold |
| Storage voltage | 3.8V/cell | Never store full or empty |
| Charge rate | 1–5C | 1C safest for longevity |
| Failure mode | Fire/explosion if punctured | Serious hazard |

**When to retire:** puffing, capacity <80% of rated, inner resistance
rises >50% from new. Measure capacity with charger discharge test.

### LiIon (Lithium Ion)

Better for endurance builds. Lower C-rate means heavier for the same
discharge current, but 3–5× the cycle life and lower fire risk.

| Spec | Typical Range | Notes |
|------|--------------|-------|
| Energy density | 200–265 Wh/kg | Molicel P42A, Samsung 50S |
| C-rate (continuous) | 5–15C | Much lower than LiPo |
| Cycle life | 300–500 cycles | Better long-term economics |
| Storage voltage | 3.6V/cell | Less sensitive than LiPo |
| Charge rate | 0.5–1C | Slow charging extends life |

Best cells: Molicel P42A (NDAA ✓, Canadian brand), Samsung 50S
(South Korean), Panasonic NCR21700A (Japanese).

### LiFePO4 (Lithium Iron Phosphate)

For ground equipment, GCS, and battery banks. Very safe, 2000+ cycle
life, but lowest energy density (~120 Wh/kg). Rarely used in airframes.

---

## BEC Selection

A BEC (Battery Eliminator Circuit) provides regulated 5V (or 12V) from
the main battery. Choosing the wrong one causes brownouts.

### Linear vs Switching

| Type | Efficiency | Heat | Noise | Use |
|------|-----------|------|-------|-----|
| Linear (LDO) | 30–60% | High | Low | FC only, <1A |
| Switching (SMPS) | 85–95% | Low | Higher | Payload power |

**Never power a high-current payload from a linear BEC.** The wasted
power becomes heat and can cause thermal shutdown mid-flight.

### Sizing

Rule: BEC current rating ≥ 2× peak load.

Typical FC + peripherals: 1.5–3A
Add GPS + compass: +0.5A
Add telemetry radio: +1A
Add companion computer: +3–8A (use dedicated BEC)

**Total typical avionics draw:** 5–12A. Use a 15A switching BEC minimum.

### Separate BECs for FC vs Payload

The FC must have a stable, noise-free power supply. Payload power spikes
(disk writes, motor startup) should not sag FC voltage. Use two BECs:

```
Battery → BEC-1 (5V, 5A) → FC, GPS, RX, telemetry
Battery → BEC-2 (5V, 15A or 12V, 10A) → companion, cameras, LiDAR
```

---

## Power Distribution Boards

### PDB Selection

| Feature | Why it matters |
|---------|---------------|
| Continuous current rating | Must exceed all ESC peaks simultaneously |
| Capacitor bank | Filters voltage spikes from motor switching |
| Integrated BEC | Convenient but size-limited |
| Current sensor | For mAh tracking and battery monitoring |
| Voltage sensing | For low-battery warnings |

### Capacitor Bank

Motor switching creates voltage spikes that can destroy ESCs and reset
FCs. A capacitor bank at the PDB absorbs these spikes.

Rule of thumb: 1000µF per 10A of peak current draw.
For a 4S 60A system: 6000µF minimum. Use low-ESR caps (electrolytic
or polymer capacitors rated to 25V+ for 4S).

### Wiring Gauge

| Current | Gauge (AWG) | Max length |
|---------|------------|------------|
| <10A | 22 AWG | Short runs only |
| 10–20A | 20–18 AWG | |
| 20–40A | 16–14 AWG | |
| 40–80A | 12–10 AWG | |
| 80–120A | 8 AWG | |

Use silicone wire (flexible, heat-resistant). Keep power runs as short
as possible — every centimeter is resistance and voltage drop.

---

## Voltage Sag Under Load

The voltage you see at rest is not the voltage you see under full throttle.

Typical sag on a fresh LiPo:
- 4S at rest: 16.8V
- 4S at 50% throttle: 15.5V
- 4S at 100% throttle: 14.0–14.5V

**Configure low-battery failsafe for the voltage under load**, not at rest.
A 3.5V/cell failsafe at rest becomes a 3.3V/cell under load — below
the safe minimum for LiPo.

ArduCopter:
```
BATT_LOW_VOLT = 14.0    (4S, triggers LOW_BATTERY warning)
BATT_CRT_VOLT = 13.2    (4S, triggers critical failsafe → land)
FS_BATT_ENABLE = 2      (land on battery failsafe)
```

---

## Field Charging

### Charger Selection

For field operations, prioritize:
- **Multi-chemistry support** (LiPo, LiIon, NiMH)
- **AC/DC input** (can charge from car 12V or generator)
- **Parallel charging capability** (charge multiple packs simultaneously)
- **Balance charging** (essential for longevity)

Recommended: ISDT Q8 Max, HOTA D6 Pro, Junsi iCharger 4010 DUO.

### Parallel Charging

Charge multiple batteries simultaneously at the same voltage in parallel.
**Only parallel charge batteries of the same cell count and similar state
of charge.** Never mix 4S and 6S. Never mix fresh and deeply discharged.

Risk: if one battery has a damaged cell, it can pull down the others
and cause a fire. Inspect before parallel charging.

### Temperature Limits

- **Charge:** only charge at 0°C–45°C. Below 0°C causes lithium plating.
- **Discharge:** LiPo performs best at 20°C–40°C. Cold batteries (below 10°C)
  sag more and deliver less capacity.

Pre-warm cold batteries before flight: insulated bag, hand warmers, or
brief low-throttle hover before full-power maneuvers.

---

## EMI and Power Cleanliness

### Common Noise Sources

- ESCs: high-frequency switching (20–40kHz)
- SMPS BECs: switching ripple (50–300kHz)
- Video transmitters: RF coupling into power lines
- LTE modems: 700MHz–2.1GHz into DC rails

### Mitigation

**Ferrite beads** on power leads to FC and GPS — absorb HF noise.

**Capacitors at the FC power input** — 100µF electrolytic + 0.1µF ceramic
in parallel. Low-ESR combination suppresses both low and high frequency.

**Physical separation** — route power cables away from signal cables.
GPS cable especially sensitive — keep away from motor wires and VTX.

**Ground plane** — in custom builds, a solid ground plane under the FC
dramatically reduces noise pickup.

---

## Battery Storage & Transport

### Storage

- Never leave fully charged >24 hours
- Never leave discharged (below 3.5V/cell)
- Store in fireproof LiPo bags
- Room temperature (15–25°C) is ideal
- Do not store in vehicles in summer (>60°C destroys cells)

### Transport (FAA/TSA)

- Carry-on only — checked baggage regulations prohibit spare LiPo
- Each battery ≤100Wh (up to 2 batteries 100–160Wh with airline approval)
- Terminals must be covered/insulated
- Quantity limits vary by airline

---

## Related

- [Batteries](batteries.md)
- [Power Architecture & EMI](power-architecture-emi.md)
- [ESCs](escs.md)
- [Motors](motors.md)
