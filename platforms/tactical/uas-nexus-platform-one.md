# UAS Nexus Platform One

> **Category:** Tactical / MOSA FPV Ecosystem Platform
> **NDAA Status:** NDAA §848 compliant — NOT Blue UAS listed (uses Blue UAS-listed components)
> **Manufacturer:** UAS Nexus (United States)
> **Availability:** Syndicate membership required — syndicate.uasnexus.com

---

## Overview

Platform One is less a fixed product and more an ecosystem — a MOSA-first (Modular Open Systems Architecture) airframe designed to accept whatever Western avionics stack the mission requires. Inspired by Ukraine's decentralized FPV production model: no single golden BOM, no single firmware, no vendor lock-in. The frame is the common denominator; everything else is operator-configured.

Supports 7-inch and 10-inch prop configurations on the same airframe. Solder-free build option available for trainer/non-technical user configuration. Decentralized manufacturing model targets 10,000+ aircraft/month capacity. Full NDAA §848 compliance. The platform is **not** itself Blue UAS listed, but is designed to accept Blue UAS Framework-listed components (ARK FPV, ModalAI VOXL 2, Auterion Skynode-S, Doodle Labs, etc.).

Access is gated behind UAS Nexus Syndicate membership, which requires request-based approval.

---

## Specs

| Spec | Value |
|------|-------|
| Airframe | 17 in wide × 14 in long |
| Prop Support | 7-inch and 10-inch |
| Max Speed | ~80 mph (129 km/h) |
| Endurance | 20+ min at cruise |
| Power | 6S LiPO or LiON, XT60 bulkhead connector |
| Materials | Carbon fiber, flexible FDM print (Shore 95A), stainless hardware |
| Cooling | Active cooling or heatsink (compute-dependent) |
| Production Capacity | 10,000+ aircraft/month (decentralized manufacturing) |
| NDAA | §848 compliant |
| Blue UAS | NOT listed — platform accepts Blue UAS Framework components |

---

## Supported Avionics

### Flight Controllers
| Component | Notes |
|-----------|-------|
| TBS Lucid H7 | Primary recommended FC |
| BrainFPV RADIX 2 HD | Digital video + autopilot combo |
| Orqa F405 3030 | NDAA-compliant EU-manufactured option |

### Autopilot / Compute
| Component | Notes |
|-----------|-------|
| Raspberry Pi CM5 | General compute |
| ModalAI VOXL 2 | Full autonomy stack, VIO, PX4 |
| ModalAI VOXL 2 Mini | Lighter autonomy option |
| Auterion Skynode-S | Enterprise PX4, LTE, mission management |
| ARK FPV | Open-source, NDAA-compliant PX4 compute |

### C2 / Radio Links
| Component | Notes |
|-----------|-------|
| ORQA IRONghost | EW-resilient sub-GHz (licensed) |
| TBS Crossfire / ELRS | ISM 900 MHz long range |
| Doodle Labs NANO/MINI Mesh Rider | Mesh networking, IP datalink |
| BlueSDR | Software-defined radio |
| L3Harris SDR | Defense-grade SDR |
| Silvus StreamCaster | MANET mesh |

### Autopilot Software
- Betaflight, INAV, PX4, ArduPilot

---

## Configurations

### FPV Trainer / EW
Learn to fly or defeat jammers. Featured: IRONghost or TBS/ELRS radio, TBS Lucid H7 or Orqa F405, NDAA camera, 3–5 kg payload capacity, solder-free option.

### Mesh Node
Comms relay for GPS-denied environments. Featured: VOXL 2 Mini, Doodle Labs / BlueSDR / L3Harris / Silvus radio, low-light EO camera.

### Autonomy Testing
Perception and navigation research with modular sensors. Featured: VOXL 2 / VOXL 2 Mini, Doodle Nano, low-light EO + perception cameras, downward LiDAR, autonomy software.

---

## Sensors & Cameras
- NDAA-compliant EO camera
- Low-light EO camera
- Perception / stereo camera
- Downward LiDAR

---

## Gotchas

1. **Syndicate access is gated** — membership requires approval. Factor lead time into procurement planning.
2. **No fixed BOM** — Platform One is an ecosystem, not a single SKU. Component selection varies by configuration and availability. You assemble your own stack.
3. **Decentralized manufacturing** — high-volume capacity but supply chain coordination is on the operator/integrator.
4. **Multi-firmware support** — no single "golden path." Operator must select and configure the autopilot stack. VOXL 2 / PX4, ArduPilot, Betaflight, and iNav all have different integration complexities.
5. **Deeper product catalog behind the membership wall** — publicly available specs are limited. Full component catalog accessible only post-approval.
6. **NOT Blue UAS listed** — the platform itself is not on the DoD approved list. It is NDAA §848 compliant and designed to accept Blue UAS Framework-listed components, but those are different designations. Do not represent it as Blue UAS listed in procurement documents.

---

*Last updated: March 2026 | Source: syndicate.uasnexus.com, UAS Nexus Syndicate catalog*
