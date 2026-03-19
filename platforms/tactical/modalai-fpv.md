# ModalAI Seeker / Stinger

> **Category:** Tactical / Defense — Autonomous FPV
> **NDAA Status:** Blue UAS Framework (16 components listed — most of any manufacturer)
> **Manufacturer:** ModalAI (San Diego, CA, USA — spun out of Qualcomm 2018)

---

## Overview

ModalAI produces the most Blue UAS Framework components of any single manufacturer (16 listings). Their VOXL 2 compute platform is the reference companion computer for PX4-based autonomous drones. The Seeker and Stinger are ModalAI's own FPV/autonomous drone platforms built on this ecosystem.

ModalAI placed in the top 5 of DDG Phase I (~77–80 points).

---

## Platforms

### Seeker — Vision-Guided FPV
- GPS-denied capable via VOXL 2 visual-inertial odometry
- Onboard AI for target detection and tracking
- Autonomous terminal guidance option

### Stinger — Strike FPV
- Strike-optimized variant
- Low-cost, expendable architecture
- Designed for contested RF environments

---

## VOXL 2 Compute Platform

| Spec | Value |
|------|-------|
| Processor | Qualcomm QRB5165 (8-core, 2.84 GHz) |
| AI Performance | 15 TOPS (GPU + DSP) |
| Camera Inputs | 7× MIPI CSI-2 |
| Weight | ~16 g (module only) |
| Software | PX4, ROS 2, VOXL SDK |
| Blue UAS | Framework component |

VOXL 2 runs PX4 natively, making it the most direct integration target for any PX4-based AI Wingman deployment.

---

## Notes

ModalAI is the most interesting integration partner for the AI Wingman PX4 architecture. They run PX4 natively on VOXL 2, which maps directly to the existing PX4 Integration Architecture doc. Their visual-inertial odometry stack is production-ready for GPS-denied operations.

---

*Last updated: March 2026*
