# Non-Electric Propulsion — Beyond Batteries

> **Part 6 — Components**
> When batteries aren't enough. Hydrogen fuel cells, hybrid-electric
> engines, IC engines, and micro-turbines for endurance platforms.

---

## When Electric Isn't Enough

Battery-powered multirotors dominate the small UAS market because
they're simple, reliable, and require no fuel handling. But batteries
have hard physical limits: current lithium-ion tops out at 260 Wh/kg
(conventional) to 520 Wh/kg (Amprius silicon anode). Gasoline stores
12,000 Wh/kg. Hydrogen stores 33,000 Wh/kg (though fuel cell system
weight reduces the practical advantage significantly).

For missions requiring hours of endurance, heavy payloads at range,
or VTOL-to-fixed-wing transition, non-electric propulsion fills the
gap that batteries physically cannot.

---

## Hydrogen Fuel Cells

Fuel cells convert hydrogen directly to electricity. No combustion,
no moving parts in the cell itself. The electricity powers standard
brushless motors. Flight times of 2–5.5 hours are achievable vs.
30–50 minutes on batteries for equivalent platforms.

### Doosan Mobility Innovation (South Korea)

The most commercially mature hydrogen drone platform.

| Detail | Value |
|--------|-------|
| HQ | South Korea |
| Key Product | DS30W — world's first mass-produced hydrogen fuel cell drone |
| Flight Time | 2 hours (no payload), extended with lighter loads |
| Range | Up to 80 km |
| Speed | Up to 80 km/h |
| Fuel Cell | DP30M2S powerpack, 2.6 kW |
| Voltage Range | 40–74V output |
| System Weight | 21 kg (with 10.8L tank), 20 kg (with 7L tank) |
| Payload | Up to 5 kg |
| Motors | 8 (octocopter) |
| Fixed-Wing | DJ25 VTOL — 330 min endurance, 450 km range at 25 m/s |
| Awards | CES 2022 Innovation Award |

The DS30W is available as a complete system or the DP30 powerpack
can be integrated into custom airframes. Doosan provides hydrogen
storage, transport cases, and monitoring via their View App.

The DJ25 fixed-wing VTOL is the endurance champion — 5.5 hours of
flight on hydrogen vs. ~2 hours on lithium batteries for equivalent
platforms.

### HES Energy Systems (Singapore)

Hydrogen fuel cell systems optimized for UAS. Modular powerpack
design for integration into third-party airframes.

### Pegasus Aeronautics (Canada)

Hydrogen-powered UAS systems. Focused on long-endurance applications.

---

## Hybrid-Electric

Hybrid systems combine an internal combustion engine with electric
motors. The engine drives a generator that powers the electric
motors and charges batteries. This provides IC engine endurance
with electric motor simplicity and redundancy.

### Currawong Engineering (Australia)

The most complete hybrid UAS powertrain manufacturer.

| Detail | Value |
|--------|-------|
| HQ | Australia |
| Products | Corvid-29 (29cc EFI), Corvid-50 (50cc EFI), Cortex-50 Hybrid |
| Key Feature | Turnkey systems: engine + generator + ECU + hybrid power management |
| ECU Heritage | Based on Autronic SM4 platform (10,000+ units in field) |
| Protocols | DroneCAN, PiccoloCAN, UART |
| Partners | Veronte/Embention (autopilot integration), Honeywell (700+ EFI systems on T-Hawk) |

**Corvid-29:** 29cc single-cylinder 2-stroke EFI. High power-to-weight.
Minimal maintenance. Passed two 150-hour FAR Part 33 endurance tests
without major overhaul. Turnkey system includes generator, power supply,
remote starter, isolation mount, low-noise exhaust.

**Cortex-50 Hybrid:** 50cc 2-stroke EFI with hybrid power architecture.
Bi-directional power flow — engine charges batteries while flying,
batteries supplement during peak demand. Cortex Hybrid Power System
(CHPS) provides up to 750W electrical, supports 6S–14S batteries
(24–56V), integrated engine restart. Single high-voltage battery
operation for VTOL quad-planes.

**Heavy fuel option:** UMAN-VP4F fuel for safer field operations
(non-volatile, stable). Power output comparable to petrol.

### Hirth Engines (Germany)

Two-stroke UAS engines. German engineering, established manufacturer.
Models range from small tactical to medium endurance platforms.

### ePropelled (UK/USA)

Partnership with Hirth Engines announced for next-gen hybrid systems.
Combining advanced IC engines with intelligent electric propulsion
and power management. Prototype demonstrations expected early 2026.

---

## Internal Combustion (Direct Drive)

IC engines driving propellers directly. Simpler than hybrid (no
generator/motor conversion losses) but limited to fixed-wing or
single-rotor configurations.

### Rotron / Aero Design Works (Australia)

Wankel rotary engines for UAS. Compact, high power-to-weight,
smooth operation (no reciprocating vibration). Used in medium
endurance fixed-wing and VTOL platforms.

### UAV Turbines (USA)

| Detail | Value |
|--------|-------|
| HQ | USA |
| Technology | Micro-turbine engines |
| R&D Investment | $50M+ over 15+ years |
| Key Product | Monarch 5 micro-turbine |
| Generator Sets | 25 kW APEX — 75% lighter, 50% smaller than diesel equivalents |
| Fuel | Multi-fuel including JP-5, JP-8, Jet-A, diesel, biofuels |
| Demonstrated | 480 lb TigerShark drone platform |

Micro-turbines offer superior reliability, fuel flexibility, lower
noise, and lower total cost of ownership vs. diesel/piston engines.
The challenge has always been miniaturization — components like
ignitors, pumps, and compressors require complete redesign at
micro scale, not just scaling down.

UAVT's APEX generator sets are also positioned for man-portable
ground power — 3-4× more generators per helicopter/truck load
than conventional diesel units.

---

## Choosing Propulsion

| Method | Endurance | Complexity | Best For |
|--------|-----------|------------|----------|
| Battery (LiPo/Li-Ion) | 20–50 min | Low | Small multirotor, FPV, tactical |
| Battery (Amprius SiCore) | 40–90 min | Low | Extended multirotor, high-value ISR |
| Hydrogen Fuel Cell | 2–5.5 hr | Medium | Long endurance, BVLOS, delivery |
| Hybrid-Electric | 2–8 hr | High | VTOL fixed-wing, heavy payload |
| IC Direct Drive | 4–24+ hr | Medium | Fixed-wing ISR, MALE class |
| Micro-Turbine | 4–12+ hr | High | Group 3-4 platforms, heavy payloads |

1. **Battery if you can.** Electric is simpler, more reliable, and
   cheaper to operate. Only go non-electric when battery endurance
   is genuinely insufficient for the mission.

2. **Hydrogen for clean endurance.** No exhaust emissions, no
   vibration from combustion. But hydrogen handling requires
   training and infrastructure (storage, transport, refueling).

3. **Hybrid for VTOL transition.** Quad-plane designs (vertical
   takeoff, horizontal cruise) benefit most from hybrid — electric
   for hover, engine for cruise efficiency.

4. **IC/turbine for maximum endurance.** When you need a platform
   in the air for 8+ hours, combustion is the only practical option
   with current technology.

5. **Fuel logistics matter.** JP-8/Jet-A compatibility (UAV Turbines,
   Currawong heavy fuel) simplifies military logistics. Hydrogen
   requires dedicated supply chain.

---

*Last updated: March 2026*
