# Brecourt Solutions iDFR

> **Category:** Tactical / Defense — Indoor Drone as First Responder (DFR)
> **NDAA Status:** NDAA-compliant, Made in USA (vendor claim — no model/serial published)
> **Manufacturer:** Brecourt Solutions
> **Availability:** Commercial — security firms, schools, law enforcement
> **Status:** Early-stage / pre-deployment as of mid-2026 (demo footage and pilot interest; no public fielded count)

---

## Overview

The **Indoor Drone as First Responder (iDFR™)** is a building-resident security drone designed to put eyes on an interior threat before a human responder arrives. Drones live on charging docks pre-positioned inside a facility, integrate with the customer's Security Operations Center (SOC), and launch on an alert to stream low-latency video back to operators. The pitch is "detect-to-launch in as little as 0.2 seconds" and remote piloting "from anywhere in the U.S." over the same ~0.2 s latency link.

The concept is the indoor analog to outdoor police **Drone as First Responder** programs, and the platform overlaps heavily with [Shield AI Nova 2](shield-ai-nova-2.md) (autonomous GPS-denied indoor ISR) — the differentiator Brecourt markets is *persistent pre-positioning + SOC integration + remote human-in-the-loop piloting*, rather than fully autonomous building clearing.

---

## What's actually documented vs. marketed

The public site is marketing-heavy and a real spec sheet is gated behind a "request the PDF" wall. Treat the table below as **vendor claims**, not measured numbers.

| Parameter | Vendor claim | Operator note |
|-----------|--------------|---------------|
| Detect-to-launch | "as little as 0.2 s" | Marketing best-case; depends on SOC trigger plumbing |
| Video latency | ~0.2 s glass-to-glass, nationwide | Implies a cloud/relay path (AWS-hosted), not a local RF link |
| Flight time | 20+ min | Small indoor airframe; expect less with active maneuvering |
| Navigation | Optical + computer vision, GPS-denied | No published sensor suite (no mention of LiDAR/depth/ToF) |
| Compute | Full-stack **edge** computing, local AI | But the remote-pilot/video path is cloud-relayed — split architecture |
| Range / control | "anywhere in the U.S." | Network-limited, not RF-range-limited; needs facility connectivity |
| Bandwidth | Tested in low-bandwidth settings | No published minimum Mbps |
| Payload | Non-lethal only | "U.S. law prohibits dangerous payloads" — see jamming claim below |
| Charging | Autonomous docking stations, continuous | Pre-positioned indoors |
| Airframe model | **Not published** | No model number, weight, dimensions, or motor/FC stack disclosed |
| Firmware / SDK | **Not published** | No mention of MAVLink, MSP, or any open protocol |

---

## Key Features

- **Pre-positioned, dock-resident** — drones sleep on chargers inside the building, not flown in from outside.
- **SOC integration** — markets as platform-agnostic; "works with your existing cameras, detection systems, and communication networks." Bridges the camera-alert → physical-response gap.
- **ThreatLock™ / ThreatLockAI™ autonomy** — one-tap handoff to an autonomous mode that visually tracks a moving threat indoors while the SOC retains oversight; also the **comms-loss fallback** (if the link drops, the drone holds the track autonomously rather than failsafe-landing).
- **Remote human-in-the-loop piloting** over the network, with seamless manual ↔ autonomous switching.
- **No FAA authorization required** for the indoor use case (drone never enters navigable airspace) — a genuine regulatory advantage over outdoor DFR.
- **Fast onboarding** — vendor claims operators are running in <15 minutes; SOC integration "in hours, not weeks."

---

## Gotchas

1. **Spec opacity.** No published airframe model, mass, dimensions, sensor list, flight-controller stack, or SDK. The "NDAA-compliant / Made in USA" claim cannot be cross-checked against a Blue UAS listing — it is **not** on the DIU Blue UAS Cleared List as of mid-2026. Verify the bill of materials before relying on the NDAA claim for a federal/SLED buyer.
2. **"Edge AI" but cloud-relayed control.** The drone does local CV for navigation, yet the headline "pilot from anywhere in the U.S. at 0.2 s latency" implies an internet/cloud relay (AWS-hosted backend). That is a network-dependency and an attack surface — a facility network outage or WAN degradation directly degrades the response capability the system is sold on. Ask where the video and control plane actually terminate.
3. **The weapon-jamming claim.** The Industries page states an active-shooter mode where "AI scripts detect weapons and deliver a payload to jam them." Treat this as aspirational/marketing: it sits awkwardly against the "non-lethal payload only" line, and an RF/effects payload on a civilian drone raises FCC and ITAR/legal questions the site does not address. Do not assume this capability exists in a shippable form.
4. **Indoor-only.** Not an outdoor platform. No GPS, no BVLOS outdoor profile.
5. **Maturity risk.** As of mid-2026 the public evidence is demo footage and SME testimonials (Chris Grollnek, Greg Shaffer, et al.), not a fielded-fleet track record. Founded by ex-SEAL/Navy-aviator leadership with credible UAS pedigree, but procurement should treat this as early-stage.
6. **Liability model unstated.** A SOC operator remotely flying a drone toward an active threat inside an occupied building (school, etc.) carries use-of-force, privacy, and insurance questions the marketing does not cover. Confirm CONOPS and indemnification before a pilot.

---

## Company / Team

Brecourt Solutions is led by founders with military and security backgrounds:

| Name | Role | Background |
|------|------|------------|
| Jeff Ross | CEO & Co-founder | 13-yr U.S. Navy SEAL (SEAL Team ONE) |
| Ryan Jarvis | CTO | 20-yr Navy, former Naval Aviator; "800+ UAVs built" |
| Nate Jesgarz | Chief Product Officer | — |
| Wade Gibson | COO | Former Navy intelligence officer; attorney |
| Shane Griffin | Chief Revenue Officer | — |
| Larissa Espinosa | Director, Data & Platform Engineering | — |
| Stefan Amundarain | Director, UAS Development & Engineering | — |
| Sabri Sansoy | AI & Robotics Specialist | USAF veteran; MIT MS Aero/Astro |

Backend infrastructure runs on AWS. Target markets: security companies, schools/universities/places of worship, and police departments.

---

## Integration verdict

For this handbook's audience: **interesting concept, unverifiable platform.** The indoor-DFR + SOC-integration niche is real and the no-FAA angle is legitimately useful, but there is nothing to integrate against today — no SDK, no protocol, no published airframe. If you need autonomous indoor ISR with a documented track record, [Shield AI Nova 2](shield-ai-nova-2.md) is the more mature reference point. Revisit Brecourt once a spec sheet and a fielded deployment exist.

---

*Sources: brecourtsolutions.com (iDFR, FAQ, Industries, Team, Testimonials, Blog), accessed June 2026. All performance figures are vendor claims pending independent verification.*

*Last updated: June 2026*
