# Orqa MRM1-5

> **Category:** Tactical / 5-Inch Multi-Role Trainer
> **NDAA Status:** NDAA §848 + §889 + Berry Act compliant
> **Manufacturer:** Orqa d.o.o. — Osijek, Croatia (EU)
> **Availability:** Commercial / defense procurement — orqafpv.com

---

## Overview

The MRM1-5 is Orqa's 5-inch multi-role platform — the training workhorse of the MRM fleet and the cost-effective entry point to the full Orqa tactical ecosystem. Airframe is reinforced with four carbon fiber braces for crash survivability during intensive training cycles. Available in two radio variants: ISM (Ghost 2.4 GHz) for standard operations and EW (IRONghost sub-GHz) for contested environments.

Operators who train on the MRM1-5 with Tac.Ctrl build direct muscle memory that transfers to the MRM2-10 — same controller, same GCS, same MAVLink/ATAK workflow. This cross-platform proficiency is intentional: the MRM1-5 is designed to feed the larger MRM2-10 pipeline, not replace it.

Beyond training, it functions as a small payload delivery system (1 kg over 7 km) and a kinetic tool (window/material breach).

---

## Specs

| Spec | Value |
|------|-------|
| Prop Size | 5 inch |
| Motors | 2408, 2200 kV (Orqa-designed) |
| Flight Controller | F405 30×30 (Orqa 3030) |
| ESC | 4-in-1, 60A, AM32 firmware |
| Camera | Orqa Justice Analog (1200 TVL, switchable 4:3/16:9) |
| C2 Link — ISM variant | Ghost 2.4 GHz (ImmersionRC/Orqa, LoRa/FLRC) |
| C2 Link — EW variant | IRONghost dual sub-GHz (licensed bands) |
| Video | 5.8 GHz analog |
| GPS | Integrated |
| Payload Capacity | 1.0 kg |
| Range (unloaded) | ~15 km |
| Range (with payload) | ~7 km |
| Max Speed | 130 km/h |
| Speed (with payload) | ~60 km/h |
| Flight Time (unloaded) | ~15 min |
| Flight Time (loaded) | ~10 min |
| Weight — ISM variant | 562 g (without battery) |
| Weight — EW variant | 590 g (without battery) |
| Battery (included) | P50B 4S1P Li-ion, 321 g |
| Battery (recommended) | P50B 4S2P Li-ion |
| Firmware | Betaflight / ArduPilot / iNav |

---

## Ground System

| Component | ISM Variant | EW Variant |
|-----------|------------|-----------|
| Controller | FPV.Ctrl or any 2.4 GHz RC | Tac.Ctrl (mandatory) |
| GCS Software | — | Orqa GCS-1 |
| C2 Protocol | MAVLink | MAVLink |
| ATAK Integration | Yes | Yes |

---

## Roles

| Role | Notes |
|------|-------|
| **Pilot training** | Primary role — high crash-rate training on cheap 5-inch airframe |
| **MRM2-10 pipeline** | Tac.Ctrl + GCS-1 proficiency transfers directly |
| **Payload delivery** | 1 kg / 7 km with payload; 1 kg / 5 km per combat-configured spec |
| **Kinetic** | Window and material breach; direct action at close quarters |
| **EW environment training** | EW variant with IRONghost for contested airspace operator prep |

---

## ISM vs EW Variant Selection

Choose ISM when:
- Training in permissive/uncontested environments
- Budget is a constraint (ISM variant is lower cost)
- Operating with mixed RC/FPV infrastructure

Choose EW when:
- Training will transition directly to contested ops
- IRONghost sub-GHz link consistency in RF-dense environments is required
- Tac.Ctrl + GCS-1 workflow proficiency is the training objective

---

## Gotchas

1. **EW variant requires Tac.Ctrl** — the standard FPV.Ctrl does not drive IRONghost. Factor controller cost into per-seat training budget.
2. **ISM variant Ghost 2.4 GHz** — note Ghost is ImmersionRC/Orqa (GHST protocol), not ELRS. Confirm receiver compatibility if integrating into non-Orqa ground equipment.
3. **4S battery, not 6S** — unlike the MRM2-10 (6S). Separate battery logistics if running mixed MRM fleet.
4. **Not Blue UAS listed** — NDAA compliant but not on the DoD approved list.
5. **High attrition expected in training** — reinforced carbon braces help but budget for airframe replacement at scale.

---

*Last updated: March 2026 | Source: orqafpv.com, Helicomicro, Flying Eye*
