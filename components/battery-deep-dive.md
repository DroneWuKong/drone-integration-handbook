# Battery Deep Dive

The propulsion system matching guide covers battery selection for a given build. This guide goes deeper: what actually happens inside a LiPo as it ages, how to read internal resistance and what it tells you, why the C rating on the label is mostly marketing, and how to make rational decisions about parallel packs and storage.

---

## Chemistry Comparison

### LiPo (Lithium Polymer)

The standard for performance UAS. High discharge rate, low weight, available in every cell count and capacity imaginable. The cathode material is typically NMC (Nickel-Manganese-Cobalt) or NCA (Nickel-Cobalt-Aluminum).

- **Nominal voltage:** 3.7V/cell
- **Full charge:** 4.20V/cell (standard), 4.35V/cell (LiHV)
- **Discharge cutoff:** 3.5V/cell (conservative), 3.3V/cell (aggressive)
- **Storage voltage:** 3.80–3.85V/cell
- **Energy density:** 150–200 Wh/kg
- **Cycle life:** 150–400 cycles to 80% capacity
- **Peak discharge:** 25–150C rated (see C rating section)

### Li-Ion (Lithium Ion)

Cylindrical cells (18650, 21700) with higher energy density but lower peak discharge. The right choice for long-endurance platforms that don't need burst power.

- **Nominal voltage:** 3.6V/cell
- **Full charge:** 4.20V/cell
- **Discharge cutoff:** 2.5–3.0V/cell
- **Storage voltage:** 3.6–3.7V/cell
- **Energy density:** 200–265 Wh/kg (35–60% more than LiPo)
- **Cycle life:** 500–1000 cycles
- **Peak discharge:** 2–10C typical (high-drain cells: 20–30C)

**Where Li-Ion wins:** Long-range fixed-wing, mapping platforms, delivery drones, anything where flight time matters more than max power. A 21700 Samsung 40T cell pack at 4,000mAh provides ~35% more flight time per gram than a same-weight LiPo — but if you need punch-out power for a 6S freestyle quad, Li-Ion won't keep up with the current demand.

### LiHV (High Voltage LiPo)

Same physical construction as LiPo, charged to 4.35V instead of 4.20V. About 5–8% more energy per cell. Requires an LiHV-capable charger and an LiHV-rated ESC/FC (most modern ESCs handle 4.35V fine).

The tradeoff: the cells spend more time at high voltage, which accelerates degradation. Expect 20–30% shorter cycle life compared to the same cell charged to 4.20V. Worth it if you fly frequently and replace batteries regularly; not worth it if batteries sit between sessions.

### LiFePO4 (Lithium Iron Phosphate)

Extremely safe, long cycle life, thermally stable. The chemistry of choice for ground vehicles, industrial systems, and high-cycle applications. Not competitive for UAS due to low energy density (90–120 Wh/kg) and low cell voltage (3.2V nominal).

---

## The C Rating: What It Actually Means

The C rating on a LiPo label is a multiplier applied to the capacity:

```
Max discharge current (A) = C_rating × capacity_Ah
```

A 4S 1500mAh 100C pack has a rated max discharge of 150A.

**The problem:** C ratings are self-reported by manufacturers with no standard test methodology. A pack labeled 100C from a budget brand may actually provide 40–60A before voltage sag degrades significantly. A quality pack labeled 45C may outperform a cheap 100C pack at identical current.

**What actually matters is internal resistance,** not the C rating. Internal resistance is the real physical limit on discharge capability and it's measurable with a charger that has an IR measurement function.

---

## Internal Resistance: The Real Health Metric

Internal resistance (IR) is the resistance inside the battery cell and wiring. When current flows, some voltage is lost across this resistance (V = IR), reducing the voltage available to your motors.

**What IR tells you:**
- Fresh LiPo (good quality): 2–6mΩ per cell
- Aged LiPo (80% capacity): 8–15mΩ per cell
- Damaged/puffed cell: 20–50mΩ+

**How voltage sag works:**
At 50A draw through a pack with 5mΩ IR per cell (4S = 20mΩ total):
```
Voltage sag = Current × IR = 50A × 0.020Ω = 1.0V
```
A 4S pack that reads 15.0V at rest shows 14.0V under 50A load. As the pack ages and IR increases to 40mΩ, sag at 50A becomes 2.0V — now your "15V" pack shows 13V under load, and your ESCs may hit their undervoltage cutoff.

**Measuring IR:** Use a charger with built-in IR measurement (iCharger, ISDT, Junsi series). Measure at rest, at consistent temperature (IR varies with temperature — cold cells have higher IR). Log IR on each charge cycle; rising IR is an early indicator of aging.

**When to retire a pack:** IR more than 3× the initial value, or capacity below 80% of rated, or any cell with a cell delta >0.1V after a full charge.

---

## Voltage Sag Under Load

Voltage sag is not a flaw — it's physics. But excessive sag causes real problems:

- **FC brownout:** If the voltage at the FC input drops below minimum, the FC resets mid-flight.
- **ESC undervoltage cutoff:** ESCs have minimum operating voltages; crossing them causes motor shutdown.
- **Reduced thrust:** At lower voltage, motor RPM drops, reducing thrust.
- **Inaccurate voltage monitoring:** If you rely on resting voltage to estimate state-of-charge, the loaded voltage gives you a pessimistic picture — the battery recovers voltage when current demand drops.

**Practical mitigation:**
- Set `BATT_ARM_VOLT` based on loaded voltage, not resting voltage. Test your platform's hover voltage under load and use that as the floor.
- Add a 1000µF capacitor close to the ESC power input. This doesn't fix sag — it filters the fast transients.
- Don't push packs to their rated maximum discharge for sustained periods. Flying at 70% of rated max discharge leaves margin for peaks.

---

## Capacity Fade: How Batteries Age

LiPo capacity degrades with each charge-discharge cycle due to:
1. **SEI (Solid Electrolyte Interphase) layer growth:** Forms on the anode during charging; irreversible; increases IR over time
2. **Lithium plating:** At high charge rates or low temperatures, lithium metal deposits on the anode instead of intercalating; causes capacity loss and internal shorts
3. **Cathode degradation:** Physical and chemical changes at the cathode reduce active material

**Accelerating factors:**
- High charge rate (>1C is fine; >3C degrades faster)
- High storage voltage (storing at 4.2V vs 3.85V doubles degradation rate)
- High operating temperature (>40°C significantly accelerates aging)
- Deep discharge (below 3.3V/cell)
- Physical damage (swelling, impact, moisture)

**Slowing degradation:**
- Store at 3.80–3.85V/cell (most chargers have a "storage charge" function)
- Charge at 1C or lower when not in a hurry
- Avoid flying in temperatures below 5°C without pre-warming
- Don't discharge below 3.5V/cell per battery monitor during flight (3.3V absolute minimum)
- Don't charge immediately after a hot flight — let cells cool to under 40°C first

---

## Storage Voltage: The Most Important Practice

Flying at full charge is fine. Storing at full charge is not. A LiPo stored at 4.2V/cell for a week loses measurable capacity; stored for a month, it may puff.

The sweet spot is 3.80–3.85V/cell — enough charge to prevent deep-discharge cell damage during storage, low enough to minimize electrolyte oxidation.

**Practical workflow:**
1. After flying: if you won't fly again within 48 hours, discharge or storage-charge to 3.85V/cell
2. Before flying: charge to 4.2V within 24 hours of use
3. Long-term storage (>1 month): store at 3.7–3.8V/cell, in a fireproof bag, in a cool location

Most quality chargers (iCharger, ISDT Q8, ToolkitRC M8) have a one-button storage charge function.

---

## Parallel Packs

Running two or more batteries in parallel doubles capacity (and weight) without changing voltage.

**What goes right:** More capacity, lower effective C-rate for the same load, longer flights.

**What can go wrong:**

**Connecting packs at different states of charge:** When you connect a full pack (4.2V/cell) to a depleted pack (3.5V/cell), a large current flows between the packs as they equalize. This instantaneous equalization current can trip your ESCs, damage cell chemistry, or in extreme cases cause fires.

**Rule:** Never parallel-connect packs that differ by more than 0.1V per cell. Use a parallel charging board that lets you charge multiple packs simultaneously to the same voltage, then connect them in parallel.

**Cell mismatches between packs:** Even two nominally identical packs from the same manufacturer will have slightly different internal resistances. When paralleled, the lower-IR pack will supply more current under load. Over time this can cause one pack to age faster than the other.

**Practical parallel approach for BVLOS endurance:**
1. Buy a matched pair from the same batch (same production lot, same measured IR)
2. Cycle both packs together from new — don't alternate which pack you use
3. Retire both when either shows signs of aging

---

## BMS for Larger Systems

For Group 2+ platforms and multi-cell configurations above 6S, a dedicated Battery Management System (BMS) is advisable.

A BMS provides:
- Cell-level voltage monitoring (catch a single bad cell before it causes a runaway)
- Overcurrent protection (hardware cutoff if current exceeds a threshold)
- Temperature monitoring (thermistor per cell group)
- State-of-charge estimation (Coulomb counting + voltage model)
- Cell balancing (active or passive)

For ArduPilot integration, the BMS typically reports via I2C or UART. ArduPilot's `BATT_MONITOR` supports multiple BMS protocols:
```
BATT_MONITOR = 16  # SMBus-Maxim (common for 18650 packs)
BATT_MONITOR = 17  # ESCON
BATT_MONITOR = 18  # Bebop 2
BATT_MONITOR = 20  # Maxell (for industrial packs)
```

For custom or industrial LiPo packs with an integrated BMS UART output, use the `BATT_MONITOR = 4` (UART protocol) or write a custom driver.

---

## Fire Safety

LiPo thermal runaway is fast, hot (>800°C), and produces toxic gases. The standard precautions:

- **Charge and store in a LiPo-safe bag** — ceramic or reinforced bags rated for LiPo fires
- **Never leave charging unattended**
- **Don't charge below 0°C** — lithium plating risk
- **Don't charge above 45°C ambient**
- **Inspect every pack before and after flight** — any swelling, impact damage, or unusual warmth: ground it
- **Discharge a damaged or retired pack completely** (to 0V per cell, using a LiPo discharger or a resistive load) before disposal or recycling. A fully discharged LiPo is safe to dispose of in most municipal waste streams; a charged LiPo is not.

**If a pack catches fire:** Don't use water (water reacts with lithium). Move it outdoors if safe to do so; allow it to burn out. A metal bucket with sand is the standard field containment method.
