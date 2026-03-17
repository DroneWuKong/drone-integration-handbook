# Unsolved Problems in Mesh Networking & Drone Swarm Operations

**The Unhandled Exceptions in Mesh Networking & Drone Swarm Operations**

*Version 1.0 — March 2026*

---

Drone shows are not swarms. They are pre-choreographed screensavers playing back trajectory files in controlled airspace with RTK GPS and zero autonomy. If your "swarm" can't handle a 15 mph crosswind, a lost radio link, or a drone it's never met before, it's not a swarm.

This document exists because every unchecked box is an invitation. Solve one of these and you've moved the entire industry forward.

Buddy up.

---

## The Drone Show Illusion

People watch 5,000 drones paint a dragon in the night sky and walk away thinking swarm technology is solved. It is not. Those shows are remarkable engineering achievements, but they are the opposite of what the word "swarm" means in any operational context. Here is what a drone show actually is:

- **Pre-choreographed:** Every trajectory is computed offline, often hours or days before the show. No drone makes a single decision during flight.
- **Central server playback:** A ground computer sends every position waypoint to every drone. Remove the server and nothing flies.
- **RTK GPS:** Sub-centimeter positioning from fixed base stations set up at the venue. Not field-deployable, not available indoors, not available in contested environments.
- **Controlled airspace:** The show area is a restricted zone with no other air traffic, no RF interference, no obstacles, no unknowns.
- **Identical hardware:** Every drone is the same model with the same firmware. Zero heterogeneity.
- **No wind tolerance:** Shows are cancelled in winds above 10–15 mph. Real operations happen in whatever weather the mission requires.
- **No autonomy:** If a drone loses comms, it lands. If the server fails, everything lands. There is no independent decision-making.
- **No sensing:** The drones don't see anything. They don't detect anything. They don't react to anything. They play back a file.

Now consider what a real operational swarm would need to do:

- Fly heterogeneous platforms (different sizes, different sensors, different endurance) in uncontrolled airspace.
- Coordinate in real time with sub-second latency over unreliable mesh radio links.
- Make autonomous decisions when communication is lost, degraded, or jammed.
- Share sensor data (video, detections, position) across the mesh without saturating bandwidth.
- Handle wind, weather, obstacles, and other aircraft that weren't in the plan.
- Operate with or without GPS.
- Add and remove drones mid-mission without stopping the operation.
- Keep flying safely when individual drones fail.

The gap between these two lists is the subject of this document. Every item below is a specific, defined problem that stands between the drone show illusion and real swarm capability. Some are being actively worked on. Some have partial solutions. Some have no credible path to solution with current technology.

If someone tells you their drone swarm "just works," ask them: how many drones, at what range, sharing what bandwidth, at what latency, in what weather, for how long, with how many operators, and what happens when you jam the radio? The answers will be disappointing. That's not a criticism. That's where the work is.

## How to Read This Document

This is a checklist, not a textbook. Each problem is stated as concisely as possible with three columns:

- **The Problem:** What doesn't work and why it matters.
- **The Reality:** What actually happens today, with real numbers where available.
- **What Would Solve It:** What a solution would look like. This is the invitation.

**Status key:**

- ☒ **UNSOLVED** — No production-ready solution exists. Active research problem. Pick this one if you want to change the industry.
- ▣ **PARTIAL** — Works in controlled conditions, degrades or fails in the real world. Improvement is valuable but the core problem is understood.
- ☑ **SOLVED** — Production solutions exist and are deployed. Included for context — these were once unsolved too.

The goal is to turn red boxes amber, and amber boxes green. Every color change is a real contribution.

---

## RF & Communications

Radio is the nervous system of a swarm. Everything else — coordination, navigation, sensing — depends on drones being able to talk to each other. And radio physics does not care about your product roadmap.

| # | Problem | The Reality | What Would Solve It |
|---|---------|-------------|---------------------|
| ☒ | **Spectrum Congestion at Scale** | 20+ drones on the same WiFi channel destroy each other's throughput. Hidden node problem compounds in 3D airspace. CSMA/CA was designed for offices, not swarms. | Dynamic spectrum access with cognitive radio. Licensed spectrum for UAS. Directional antennas that create spatial channels. All expensive, all heavy, all power-hungry. |
| ☒ | **Latency vs. Hop Count** | Each mesh hop adds 10–50ms. A 5-hop path = 50–250ms minimum. Swarm coordination needs <100ms. These numbers don't work together. | Deterministic TDMA scheduling on custom waveforms. Eliminates contention but requires precise clock sync (see Navigation section). Military radios do this but cost $20K+ per node. |
| ☒ | **Bandwidth vs. Range** | Shannon's law is not negotiable. High bandwidth = wide channel = high frequency = short range. 5.8 GHz gives bandwidth but 500m range. 900 MHz gives range but 1 Mbps. You cannot have both. | Don't stream raw video. Process onboard (NPU), send detections + thumbnails (100× compression). Design the swarm protocol for the link, not the other way around. |
| ☒ | **Inter-Swarm Interference** | Two swarms in the same area on the same frequencies interfere with each other. No coordination mechanism exists between independent swarm operators. | Airspace-anchored spectrum allocation. Cooperative spectrum sharing protocols. Standardized swarm-to-swarm deconfliction. None of this exists yet. |
| ▣ | **Mesh Self-Healing Speed** | Mesh protocols can reroute around a failed node, but convergence takes 1–10 seconds. A drone at 20 m/s travels 20–200m during reconvergence. That's an eternity for collision avoidance. | Proactive routing with pre-computed backup paths. batman-adv and OLSR do this partially. Still too slow for safety-critical coordination. |
| ▣ | **EW/Jamming Resilience** | Frequency hopping helps but a broadband jammer saturates all hop frequencies simultaneously. DSSS provides processing gain but at the cost of bandwidth. Commercial mesh radios are not designed for contested RF. | Affordable, compact, jam-resistant waveforms for sub-250g platforms. The military has solutions but they weigh 2 kg and cost $50K. The gap is bringing that capability to small drones. |
| ▣ | **Video Backhaul** | Real-world WiFi mesh throughput is 20–40 Mbps aggregate. That's 4–8 simultaneous 720p streams. A 20-drone swarm with cameras cannot stream everything. | Edge processing eliminates the need to stream raw video. Compress observations to metadata + keyframes. The compute exists (NPUs) but the software pipeline is immature. |

## Swarm Coordination & Decision-Making

Coordination is where the swarm either becomes more than the sum of its parts, or collapses into an expensive traffic jam. Almost every coordination algorithm that works in simulation has never been tested with real radios, real wind, and real failure modes.

| # | Problem | The Reality | What Would Solve It |
|---|---------|-------------|---------------------|
| ☒ | **Scaling Past ~50 Agents** | Algorithms that coordinate 10 drones break at 100. Communication and computation scale O(n²) or worse. No production system has demonstrated reliable coordination beyond ~50 heterogeneous agents. | Hierarchical coordination: cluster leaders + local consensus + inter-cluster gossip. Reduces scaling to O(n log n). Proven in simulation, unproven in the field with real comms. |
| ☒ | **Consensus Under Packet Loss** | Consensus algorithms assume reliable delivery. Real mesh loses 5–20% of packets under load. Byzantine fault tolerance adds latency. Raft and Paxos weren't designed for 100ms round-trips with 15% loss. | Byzantine fault-tolerant consensus adapted for high loss. Computationally expensive. May need to accept eventual consistency instead of strong consensus for non-safety-critical decisions. |
| ☒ | **Real-Time Task Allocation** | Optimal task assignment for N drones is NP-hard. Heuristics exist but degrade with incomplete information (which is the normal case in a swarm). | Distributed auction/market algorithms with bounded computation. Show promise in simulation. Performance with real latency and packet loss is unknown. |
| ☒ | **Graceful Degradation at Scale** | When 1 of 10 drones fails, the swarm adapts. When 10 of 100 fail simultaneously, cascading failures are likely. No system has demonstrated graceful degradation at scale with realistic failure rates. | Pre-computed degradation scenarios (the Assumptions List concept). Resilient planning that expects failure, not just tolerates it. Tested only in simulation. |
| ▣ | **Formation in Real Wind** | Precise formation requires sub-second position updates and responsive control. Gusty conditions create oscillations. Wind estimation is local — each drone sees different wind. | Cooperative wind estimation (share wind observations across swarm). GPS + VIO + IMU fusion for position. PID gains that adapt to conditions. Works in light wind, untested in real gusts. |
| ▣ | **Human-Swarm Interface** | One operator, one drone: well understood. One operator, 20 drones: information overload. Current GCS interfaces show individual drone telemetry. No interface has solved swarm-level situational awareness. | Intent-based commands ("survey this area" not "fly to waypoint 7"). Autonomy sliders that let operators choose how much control to delegate. Exception-based management: the UI is quiet unless something needs human attention. |

## Navigation & Positioning

GPS made drone navigation feel solved. It is not. Take away GPS and most drones become expensive lawn darts. Even with GPS, the accuracy and update rate are insufficient for tight swarm coordination.

| # | Problem | The Reality | What Would Solve It |
|---|---------|-------------|---------------------|
| ▣ | **VIO Drift** | Visual odometry drifts 0.5–2% of distance traveled. After 1 km, error is 5–20m. Accumulates over time with no correction. Not acceptable for precision coordination. | Loop closure (revisit known areas), terrain-relative matching (reference maps), GPS integration when available. Each adds compute, power, and complexity. No single solution works in all conditions. |
| ☒ | **Absolute Position Without GPS** | No vision-based system provides absolute Earth-referenced position. VIO/SLAM gives relative position only. eLoran, terrestrial beacons, and signals-of-opportunity navigation are research-stage. | Alternative absolute positioning: eLoran, terrestrial beacons, signals of opportunity (cellular, WiFi, broadcast TV). All immature or unavailable for airborne platforms. |
| ☒ | **Vision Nav in Bad Conditions** | VIO and SLAM fail in: low light, fog, rain, smoke, snow, featureless terrain (water, desert, snow fields). These are exactly the conditions where GPS-denied navigation is most needed. | Multi-modal sensing: thermal + radar + LiDAR + acoustic. Each adds weight, power, and cost. Sensor fusion algorithms for degraded-visual-environment navigation are active research. |
| ▣ | **Inter-Drone Relative Position** | Swarm-mates need to know each other's positions. Options: GPS (1–3m error, requires satellites), UWB ranging (centimeter accuracy, requires line of sight), vision (works but computationally expensive). | Cooperative localization: drones share observations to collectively improve position estimates. Mathematically elegant. Practically untested at scale with real latency. |
| ▣ | **Clock Sync Without GPS** | Swarm protocols need synchronized clocks. GPS provides nanosecond sync. Without GPS, network-based sync achieves microsecond accuracy at best, which degrades with hop count and packet loss. | Network time protocols over mesh. Cooperative clock sync. Chip-scale atomic clocks (CSACs) are $1,500+ and provide holdover but not initial sync. |

## Power, Weight & Endurance

Every capability we add to a drone — compute, radios, sensors, cameras — draws power from the same battery that keeps it in the air. Physics does not offer free compute cycles.

| # | Problem | The Reality | What Would Solve It |
|---|---------|-------------|---------------------|
| ☒ | **Compute vs. Flight Time** | Running VIO + SLAM + detection + mesh networking draws 5–15W on a companion computer. On a 250g drone with a 2S battery, that's 20–50% of total power budget. Every watt of compute is a minute of flight time. | More efficient silicon (NPUs > GPUs by 10× per watt). Algorithm optimization. Larger drones with more battery. Each solution has tradeoffs — efficiency means less capability, size means less deployability. |
| ☒ | **Mesh Relay Power Cost** | A drone relaying other drones' traffic keeps its radio transmitting continuously. A WiFi radio at full power draws 2–5W. This is comparable to the propulsion cost of the compute itself. | Duty-cycle-aware routing that balances relay load. Sleep scheduling. Both reduce throughput. The fundamental tension: the mesh needs relay nodes, but relay duty kills endurance. |
| ▣ | **Heterogeneous Endurance** | Different drones have different battery levels. The swarm's effective mission time equals its lowest-endurance member unless you plan for early RTLs. Most swarm planners don't. | Dynamic role assignment based on energy state. Low-battery drones take passive roles. Landing and relaunching mid-mission. Battery-aware task allocation. Demonstrated in simulation only. |
| ☒ | **Weight Budget for Swarm Hardware** | A mesh radio module + antennas + companion computer + cameras + ranging sensors = 50–200g. On a 250g drone, that's the entire payload budget. On a 5 kg drone, it's manageable. Sub-250g swarm-capable drones don't exist yet. | Integration (APB-style single boards). Lighter radios. More capable SoCs. The trend is favorable but current COTS options still exceed budget for small platforms. |

## Software, Standards & Regulation

Even if we solved every physics problem above, the software and regulatory infrastructure to deploy real swarms does not exist.

| # | Problem | The Reality | What Would Solve It |
|---|---------|-------------|---------------------|
| ☒ | **No Swarm Protocol Standard** | MAVLink standardized single-drone C2. Nothing equivalent exists for multi-agent coordination. Every swarm project invents its own protocol. Interoperability is zero. | An open swarm coordination protocol. STANAG 4586 covers single-UAS but not multi-agent. ROS 2 DDS provides middleware but not a swarm protocol. Someone needs to write the MAVLink equivalent for swarms. |
| ☒ | **Multi-Vendor Abstraction** | Different FCs, different firmware, different sensors, different radios. Building a swarm from mixed hardware is an integration nightmare. No abstraction layer exists. | Lightweight swarm middleware that runs on ESP32 through Jetson. Must abstract FC differences, sensor differences, and radio differences behind a common API. The integration tax is currently paid per-project. |
| ▣ | **Sim-to-Reality Gap** | Swarm algorithms tested in simulation often fail in the real world. Simulations underestimate latency, overestimate link reliability, ignore wind, and don't model RF propagation accurately. | Hardware-in-the-loop simulation with real radios and injected faults. Digital twins that model RF, wind, and failure modes. Expensive to build, essential to trust. |
| ☒ | **Regulatory Framework** | No country has a clear regulatory path for one operator controlling multiple autonomous drones simultaneously. BVLOS waivers exist for single drones. Swarm operations are regulatory terra incognita. | Regulatory frameworks that recognize swarm-level autonomy and define acceptable failure modes. This requires technical standards (see above) that regulators can reference. Chicken-and-egg problem. |
| ☒ | **Cybersecurity at Swarm Scale** | Mesh networks are inherently harder to secure than point-to-point links. Every node is an attack surface. Spoofing, injection, and denial of service at swarm scale are largely unstudied. | Lightweight authenticated encryption that doesn't break latency budgets. Hardware root of trust on each node. Swarm-level intrusion detection. All active research areas with no deployed solutions for small UAS. |

---

## The Scoreboard

As of March 2026:

| Category | ☒ Unsolved | ▣ Partial | ☑ Solved | Total |
|----------|-----------|----------|---------|-------|
| RF & Communications | 4 | 3 | 0 | 7 |
| Coordination & Decision-Making | 4 | 2 | 0 | 6 |
| Navigation & Positioning | 2 | 3 | 0 | 5 |
| Power, Weight & Endurance | 3 | 1 | 0 | 4 |
| Software, Standards & Regulation | 4 | 1 | 0 | 5 |
| **TOTAL** | **17** | **10** | **0** | **27** |

**17 unsolved. 10 partial. 0 solved.**

Zero boxes in the green column. That is the honest state of swarm technology in 2026. This is not a condemnation — it is the most exciting engineering frontier in robotics. Every one of these 27 problems is a PhD thesis, a startup, a contract, or a contribution to an open-source project that the entire industry would benefit from.

## What AI Wingman Does About It

We don't pretend these problems are solved. We design around them:

- **The Wingman Grid works without GPS.** It doesn't fix GNSS-denied absolute positioning — it sidesteps it by making GPS optional, not required.
- **The Assumptions List acknowledges that communication will fail.** Instead of pretending the mesh is reliable, we pre-agree on what each drone does when the mesh is gone.
- **Edge processing reduces the bandwidth problem.** The APB's NPU processes video onboard and sends detections, not streams. This turns a 5 Mbps problem into a 50 Kbps problem.
- **The autonomy slider explicitly communicates how much the system can do alone.** L0 is honest: the drone flies, the human decides. L4 is aspirational: the drone operates independently per the Assumptions List. We don't claim L4 is production-ready.
- **Product separation** (Wingman advises, Forge recommends hardware, Command integrates C2) means each product can be honest about its own limitations without pretending the whole system is more capable than it is.
- **Open documentation** (including this document) invites the community to help solve these problems rather than pretending we already have.

We put "safety" in quotes because it reduces danger without eliminating it. We should put "swarm" in quotes too. The honest version: a group of drones that try to coordinate, sometimes succeed, and have a plan for when they can't.

## The Invitation

This document is intended for inclusion in The Drone Integration Handbook — the free, open industry reference. It is not proprietary. It is not competitive intelligence. It is a shared accounting of what is hard, written by people who have tried to make this stuff work and know where it breaks.

If you solve one of these problems — even partially — tell someone. Publish it. Open-source it. Present it at a conference. File a patent if you need to, but make sure the knowledge reaches the people building drones in garages and labs and forward operating bases. The industry moves forward when hard problems get easier, and they get easier when people share what they've learned.

Every red box that turns amber is progress. Every amber box that turns green is a breakthrough. The scoreboard will be updated as the state of the art advances.

The drone show is beautiful. The unsolved problems list is useful. We'd rather be useful.

---

*AI Wingman — Unsolved Problems in Mesh & Swarm v1.0*
*17 unsolved. 10 partial. 0 solved. Let's get to work.*

**Buddy up.**
