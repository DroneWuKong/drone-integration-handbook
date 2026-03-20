# Orqa MRM2-10

> **Category:** Tactical / Multi-Role FPV
> **NDAA Status:** NDAA §848 + §889 + Berry Act compliant
> **Manufacturer:** Orqa d.o.o. — Osijek, Croatia (EU)
> **Availability:** Commercial / defense procurement — orqafpv.com

---

## Overview

Orqa's flagship 10-inch tactical FPV platform and their most widely fielded system globally. Often referred to simply as "MRM" or "MRM10" by operators. Built around full vertical integration — every component from the flight controller to the motors to the radio is Orqa-designed and EU-manufactured, with no Chinese parts in the BOM.

Orqa acquired ImmersionRC in 2023, consolidating the Ghost radio ecosystem in-house. The MRM2-10 is the centerpiece of the resulting vertically integrated ecosystem: Orqa frame, Orqa FC, Orqa ESC, Orqa motors, IRONghost radio (Orqa), Justice camera (Orqa), Tac.Ctrl ground controller (Orqa), GCS-1 ground station (Orqa).

---

## Specs

| Spec | Value |
|------|-------|
| Prop Size | 10 inch |
| Wheelbase | 465 mm |
| Motors | 2814-class, 880 kV (Orqa-designed) |
| Flight Controller | H7 QuadCore — STM32H743, ICM42688P |
| ESC | 30×30, 70A, AM32 firmware |
| Camera | Orqa Justice Analog (1200 TVL, switchable 4:3/16:9, low-light) |
| C2 Link | IRONghost (licensed bands) |
| Video | 5.8 GHz analog |
| GPS | Integrated (compass + barometric altimeter) |
| Payload Capacity | 2.5 kg standard / 3.5 kg max |
| Range | ~20 km |
| Cruise Speed | ~70 km/h |
| Battery | 6S4P Li-ion (~16,000 mAh), XT90 + 2× XT60 parallel |
| Firmware | Betaflight, ArduPilot, iNav, PX4 |
| Frame Material | Carbon fiber body and arms |

---

## Ground System

| Component | Details |
|-----------|---------|
| Controller | Orqa Tac.Ctrl |
| Ground Station | IRONghost QS (mast-mountable, CAT5 connection) + IRONghost GS video receiver |
| GCS Software | Orqa GCS-1 |
| C2 Protocol | MAVLink |
| ATAK Integration | Yes — via Tac.Ctrl |
| Operator Stand-off | Up to 1 km (IRONghost QS mast configuration) |

---

## Supply Chain & Compliance

Orqa manufactures all core components in-house at their Osijek, Croatia facility: flight controllers, ESCs, motors, PCBs, cameras, and radios. Zero Chinese-sourced parts. Full vertical integration provides supply chain security and eliminates third-party dependency risks.

**Note (2025):** A DoD procurement halt was reported after a radio module subcomponent was found to be Chinese-sourced. Orqa CEO confirmed manufacturing of that module was moved in-house. NDAA compliance status should be independently verified for current contracts.

---

## Production & Scale

| Metric | Value |
|--------|-------|
| Annual capacity | 280,000 drones (Osijek facility, as of late 2025) |
| Roadmap | Up to 1M/year via decentralized partner manufacturing |
| Partner network | Licensing agreements with multiple NATO-country partners |
| Croatia army contract | ~€10M order |
| Firestorm partnership | 3D-printable Orqa design under Firestorm Squall brand (Feb 2026) |

---

## Funding & Industry

| Event | Detail |
|-------|--------|
| $5.8M Series A | Lightspeed Venture Partners, 2024 |
| EU SAFE | ~€100M procurement mechanism |
| Baykar partnership | Integration with Bayraktar TB2 |
| DOK-ING partnership | Manned-unmanned teaming (MUM-T) |

---

## Gotchas

1. **IRONghost requires licensed spectrum** — not ISM. Coordinate with your RF authority before deployment.
2. **Tac.Ctrl is required for IRONghost** — the standard FPV.Ctrl does not drive IRONghost.
3. **DoD NDAA cloud (2025)** — a subcomponent issue caused a procurement pause. Verify current compliance status with Orqa before contracting.
4. **No DJI ecosystem** — fully closed Orqa stack. Ghost/IRONghost receiver protocol (GHST) only.
5. **Proprietary GCS** — Orqa GCS-1 is MAVLink-compatible but the physical ground station hardware is Orqa-only.
6. **MRM2-10F (foldable) also available** — if rapid deployment / backpack carriage matters, evaluate the -F variant.

---

*Last updated: March 2026 | Source: orqafpv.com, WNK Store, Tectonic Defense*
