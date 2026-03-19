# Electronic Speed Controllers — The Firmware Matters

> **Part 6 — Components**
> ESCs translate flight controller commands into motor speed.
> The firmware running on them determines capability, and the
> hardware origin determines compliance.

---

## The Landscape

The ESC market split in two when BLHeli_32 was discontinued in
June 2024 (closed-source, can no longer be updated). The hobby
market migrated to AM32 (open-source, GPL) for 32-bit ESCs
and Bluejay/BLHeli_S for 8-bit legacy hardware.

For NDAA compliance, the picture is simpler: almost every hobby
ESC on the market is Chinese-manufactured. The parts-db has 148
ESCs — all from the GetFPV consumer catalog, all Chinese hardware.
Three manufacturers are building NDAA-compliant alternatives.

---

## NDAA-Compliant ESCs

### ARK Electronics — ARK 4IN1 ESC CONS

| Detail | Value |
|--------|-------|
| HQ | USA |
| Blue UAS | Framework component |
| NDAA | Compliant, made in USA |
| Type | 4-in-1 ESC |
| Firmware | AM32 (open-source) |
| Voltage | 3-8S |
| Current | 50A continuous |
| Protocol | DroneCAN |
| Key Feature | Connectorized (no-solder) — designed for mass production |
| Manufacturing | USA |

ARK's connectorized design is significant — it eliminates
soldering from the assembly process, enabling production-line
manufacturing at scale. This directly supports the DDG goal
of producing hundreds of thousands of drones.

### Hargrave Technologies

| Detail | Value |
|--------|-------|
| HQ | Australia |
| NDAA | Compliant — Western-sourced components |
| Deployed | 10,000+ aircraft in 50+ countries |
| Recognition | Sovereign Capability Defence Grant recipient |

**Product Line:**

| Product | Key Feature |
|---------|-------------|
| nanoDRIVE 4LPi | 4-in-1, DroneCAN/ARINC825/DShot/PWM, 60+ configurable params, dual-input priority, machine-mountable |
| microDRIVE LP | IP67 rated, FOCAL algorithm, 72-hour circular data logging |
| microFLUX 4LP/2MP | Smart power supply (power avionics, not ESC per se) |

Hargrave is the most mature NDAA-compliant ESC manufacturer
by deployment count. Their DroneCAN support and industrial
protocols (ARINC825) position them for defense and commercial
platforms, not hobby builds.

### Unusual Machines / Rotor Riot — Brave 55A ESC

| Detail | Value |
|--------|-------|
| HQ | USA (Orlando, FL) |
| Blue UAS | Framework component |
| NDAA | Compliant |
| Type | 4-in-1 ESC |
| Voltage | 3-8S |
| Current | 55A |
| Firmware | 32-bit |
| Manufacturing | USA |
| Customers | Performance Drone Works ($3.75M order), PBAS Tranche 1.1 selectees |

The Brave 55A pairs with the Brave F7 flight controller
(F722/BMI270/BMP390) — a full NDAA-compliant flight stack
from a single manufacturer.

---

## ESC Firmware Landscape

| Firmware | License | Status | Notes |
|----------|---------|--------|-------|
| BLHeli_S | Closed | Legacy | 8-bit, widely deployed, not updatable |
| Bluejay | GPL | Active | Open-source BLHeli_S alternative, active development |
| BLHeli_32 | Closed | **Discontinued** (June 2024) | Cannot be updated. Thousands of ESCs in field now unsupported |
| AM32 | GPL | Active | **De facto 32-bit open-source standard.** Used by ARK Electronics |

**AM32** is the future for NDAA builds. Open-source firmware on
NDAA-compliant hardware (ARK) gives full supply chain transparency
with no proprietary firmware dependencies.

**ESC-Configurator** (esc-configurator.com) is the modern web-based
tool for flashing BLHeli_S, Bluejay, and AM32 via WebSerial API.
No app install needed.

---

## The Compliance Gap

| Manufacturer | Origin | NDAA | Blue UAS | Price (4-in-1) |
|-------------|--------|------|----------|----------------|
| Chinese (T-Motor, Hobbywing, etc.) | China | NOT compliant | No | $30–80 |
| ARK Electronics | USA | Compliant | Framework | ~$200+ |
| Hargrave Technologies | Australia | Compliant | No (defense validated) | $300+ |
| Unusual Machines Brave | USA | Compliant | Framework | ~$150+ |

The price gap is 3–5× for NDAA-compliant ESCs. As with motors,
any DDG Phase II competitor using Chinese ESCs will need to absorb
this cost increase.

---

## Choosing ESCs

1. **Match current rating to your motors.** ESC continuous amperage
   must exceed motor draw under load. Headroom matters — a 50A ESC
   running at 48A will thermal-throttle or fail.

2. **Protocol matters.** DShot is standard for Betaflight/iNav.
   DroneCAN is standard for PX4/ArduPilot. PWM is legacy.

3. **4-in-1 vs. individual.** 4-in-1 ESCs reduce wiring but create
   a single point of failure. Individual ESCs are heavier but
   individually replaceable. Defense platforms often prefer
   individual for field repairability.

4. **Firmware is the capability.** AM32 gives you RPM filtering,
   bidirectional DShot, and active development. BLHeli_32 is frozen.
   BLHeli_S works but is 8-bit limited.

5. **For NDAA builds:** ARK 4IN1 ESC CONS + AM32 is the cleanest
   path — open-source firmware on Blue UAS hardware.

---

*Last updated: March 2026*
