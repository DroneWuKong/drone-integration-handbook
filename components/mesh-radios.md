# Mesh Radios

> **Forge cross-reference:** 29 entries in `mesh_radios` category  
> **Related handbook chapters:** C2 Datalinks, Companion Computers, Electronic Warfare

## Beyond Point-to-Point

Standard FPV and RC links are point-to-point: one transmitter, one receiver, fixed roles. Mesh radio networks are fundamentally different — every node is both a router and an endpoint. A mesh network of 6 drones plus 3 ground nodes creates 9 potential relay paths for every packet. If one path fails, traffic reroutes automatically. No single point of failure.

This architecture unlocks three capabilities that point-to-point links cannot provide: multi-vehicle coordination without a central ground station, range extension through relay nodes, and resilience to node loss (a drone going down doesn't break the network for everyone else).

The tradeoff: complexity, weight, cost. A serious mesh radio node costs $2,000–$15,000 vs $200 for a quality point-to-point link. This is defense and enterprise territory.

## Technology Approaches

### Kinetic Mesh (Rajant BreadCrumb)
Rajant Corporation (Malvern PA, USA — NDAA ✓) invented the "Kinetic Mesh" concept — a fully mobile, peer-to-peer radio network where nodes move at speed without handoff latency. Every BreadCrumb node simultaneously operates multiple radios on different frequencies, creating redundant simultaneous paths.

**Key differentiator:** InstaMesh protocol makes topology decisions in microseconds. Traditional WiFi mesh has handoff latency of hundreds of milliseconds — unacceptable for moving vehicles. Rajant's InstaMesh is effectively zero-latency for the application layer.

**Drone applications:** Multi-drone swarm coordination, mining/industrial autonomous vehicle fleets, military multi-platform operations. Extensively deployed in DoD programs.

**Specs (LX5):** 5 radio interfaces, 900MHz + 2.4GHz + 4.9GHz + 5.8GHz options. 1W max per radio. ~120g. Ethernet + serial interfaces. IP67. NDAA compliant.

### Silvus StreamCaster
Silvus Technologies (Los Angeles CA, USA — NDAA ✓) produces the MANET (Mobile Ad-hoc Network) radios used extensively in DoD programs. StreamCaster uses MIMO (Multiple Input Multiple Output) OFDM to maximize throughput and range in multipath environments.

**Technical differentiator:** 4×4 MIMO provides spatial multiplexing — effectively 4 parallel data streams on the same frequency. This dramatically increases throughput in the 5–30km range band compared to single-antenna designs.

**Key products:**
- StreamCaster 4200 — Compact, 210g, 20MHz–6GHz configurable, 10km range. The standard drone-mounted node.
- StreamCaster 4400S — Higher power (5W), 25km range, ground vehicle and fixed installation.

**Encryption:** AES-256. FIPS 140-2 validated. Type 1 encryption option (NSA Suite B) for classified programs.

**ATAK integration:** Silvus radios are the standard radio layer under ATAK (Android Team Awareness Kit) deployments. Native CoT/SA broadcast.

### Doodle Labs Mesh Rider
Doodle Labs (USA/Singapore — verify per contract) produces compact mesh radios specifically designed for drone integration. Their Smart Radio architecture combines a LoRa command channel with a high-throughput mesh data channel, separating control from payload.

**Drone-specific design:** The Mesh Rider 2450 and 900m variants weigh 60–80g and fit into Group 1-2 UAS. Native MAVLink routing — the radio appears as a virtual serial link to the flight controller, passing MAVLink packets transparently.

**Why it matters:** Most mesh radios require a companion computer for protocol translation. Mesh Rider handles MAVLink natively, which simplifies integration dramatically for small drones.

### Elsight HALO
Elsight (Petah Tikva, Israel — allied nation ✓) produces the HALO multi-link connectivity platform. HALO differs from pure mesh radios — it's a multi-WAN bonding device that aggregates cellular (4G/5G), satellite, and RF links simultaneously.

**Use case:** BVLOS operations where no single link is reliable. HALO bonds 4G + satellite + RF into a single virtual connection, automatically routing traffic over the best-available path. Latency and bandwidth are load-balanced across all active links.

**Weight:** 115g (HALO Pro). Integrates via Ethernet with companion computer.

### Horizon31 MobileMesh
Horizon31 (USA — NDAA ✓) produces compact mesh radios for small UAS. The RM-1900 operates at 900MHz for superior range and obstacle penetration. Designed for Group 1-2 drones as a relay node for extending LTE/cellular connectivity.

### Software-Defined Mesh (Meshmerize, Silvus SmartEdge)
A growing category of mesh software that runs on commodity hardware (Raspberry Pi, Intel NUC, Nvidia Jetson) with off-the-shelf SDR radios. Meshmerize (Germany — EU/NATO ✓) provides a software stack that turns Linux hardware into a MANET node.

**Advantage:** Flexibility, upgradability, cost. **Disadvantage:** Integration complexity, no hardened RF front end, regulatory compliance varies.

## NDAA Landscape

| Product | Manufacturer | Origin | NDAA |
|---|---|---|---|
| BreadCrumb (all variants) | Rajant | USA | ✓ |
| StreamCaster 4200/4400 | Silvus | USA | ✓ |
| Mesh Rider | Doodle Labs | USA | ✓ |
| HALO | Elsight | Israel | ✓ Allied |
| MobileMesh | Horizon31 | USA | ✓ |
| Meshmerize | Meshmerize | Germany | ✓ EU/NATO |
| CreoAir | Creomagic | Israel | ✓ Allied |

Mesh radios are one of the cleanest NDAA categories — the serious players are all US, Israeli, or European. No Chinese-manufactured mesh radio has established a foothold in this market segment.

## Integration Patterns

### Topology Design
For a 6-drone swarm with 2 ground operators:
- Each drone carries one mesh node (e.g., Silvus 4200 or Doodle Labs Mesh Rider)
- Each GCS carries one mesh node
- All nodes auto-discover and form mesh
- Each GCS can reach all drones regardless of which drones are in line-of-sight

**Relay altitude:** Mesh performance improves significantly with altitude. A drone hovering at 50m AGL extends ground-level mesh range by 3–5× compared to all-ground nodes.

### MAVLink Over Mesh
Doodle Labs native MAVLink mode:
1. Connect Mesh Rider UART to FC UART
2. Set serial protocol to MAVLink
3. Ground node Ethernet connects to GCS
4. MAVLink appears as standard serial connection on both ends

For non-native mesh radios (Rajant, Silvus):
- Requires companion computer
- Companion runs MAVLink router (e.g., `mavlink-router`) to bridge FC serial to IP
- Ground GCS connects to mesh IP address

### Bandwidth Planning
MAVLink telemetry: ~10 kbps per drone  
Video (H.264 compressed): 1–8 Mbps per drone  
6 drones + video: ~50 Mbps required  

Silvus 4200 in 4×4 MIMO: up to 100 Mbps aggregate across the network. Adequate for 6 drones with compressed video.

For uncompressed video or high-resolution payload data, plan for dedicated high-bandwidth RF links separate from the mesh control network.
