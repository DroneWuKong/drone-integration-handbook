# Chapter 14: Mesh Radios for Multi-Vehicle Operations

> The expensive tactical mesh radio in your kit bag is running
> the same open-source software as a $15 router. Knowing this
> changes how you think about mesh networking.

---

## What Mesh Radios Actually Are

A mesh radio is a WiFi radio in a ruggedized enclosure with custom
firmware that routes traffic between nodes without infrastructure.
No access point, no router, no internet connection. Nodes find each
other, establish links, and route packets through intermediate
nodes to reach destinations.

That's it. Everything else is implementation detail.

### The Software Stack (What They Won't Tell You in the Datasheet)

| Vendor | Operating System | Mesh Protocol | Radio Hardware |
|--------|-----------------|---------------|----------------|
| Doodle Labs | OpenWRT (Linux) | batman-adv (layer 2 mesh) | Qualcomm/Atheros WiFi |
| Silvus | Custom Linux | Custom MAC + TDMA | Custom MIMO radio |
| Persistent Systems | Custom Linux | Wave Relay (proprietary) | Custom wideband |
| Rajant | Custom Linux | InstaMesh (proprietary) | Dual-radio Atheros |

Doodle Labs is the most transparent about this — their radios run
OpenWRT, and if you SSH into one (which you can), you'll see
batman-adv kernel modules, standard Linux networking, and iptables
rules. The "mesh intelligence" that costs $3,000 per radio is
largely batman-adv with custom antenna design and RF front-end
optimization.

This isn't a criticism. Antenna design, RF front-end engineering,
thermal management, and ruggedization are real engineering. The
software is well-integrated and tuned. But understanding that
the foundation is open-source Linux networking demystifies mesh
radios and helps you troubleshoot them.

---

## The Major Players

### Doodle Labs

**What they sell:** Compact mesh radios from 200 MHz to 6 GHz.
The Mini series (Mini900, Mini2400, etc.) are small enough to
mount on a drone. The MR series are larger with better RF performance.
The Helix series covers L/S/C bands for defense.

**What's good:**
- Open platform (OpenWRT) — you can SSH in and configure anything
- Small form factor (Mini series fits on a 5-inch quad)
- Wide frequency range across the product line
- batman-adv mesh is well-understood and debuggable
- Active development, responsive technical support

**What's not:**
- batman-adv mesh has convergence delays when topology changes
  (a drone moving fast can outrun the routing table)
- Power consumption is significant (2-5W depending on model)
- At the low end (Mini series), RF performance is limited by
  the tiny antenna and low TX power

**Typical use:** Commercial drone fleets, tactical ISR,
research platforms, any application where you want mesh
but also want to understand and customize the network.

### Silvus Technologies

**What they sell:** StreamCaster mesh radios. Higher-end than
Doodle Labs, with custom MIMO radio hardware and their own
MAC-layer protocol. The SC4200/4400 series are the workhorses.

**What's good:**
- Custom MIMO gives better spectral efficiency than commodity WiFi
- TDMA-based MAC layer provides deterministic latency
- High throughput (up to 100 Mbps per radio)
- Strong defense/government customer base
- Good video streaming support (multicast-aware mesh)

**What's not:**
- Closed platform — you can't SSH in and debug the way you can
  with Doodle Labs
- Expensive ($5,000-15,000 per node)
- Configuration is through their web GUI, which is functional
  but not scriptable
- Larger and heavier than Doodle Labs Mini series

**Typical use:** Defense ISR, government operations, commercial
applications where budget supports the higher cost.

### Persistent Systems

**What they sell:** MPU5 (manpack), Wave Relay ecosystem. The most
mature tactical mesh network product. Used extensively by US SOF
and allied forces.

**What's good:**
- Wave Relay protocol is the most resilient mesh available —
  handles high mobility, rapid topology changes, and contested
  spectrum better than batman-adv
- Proven in combat
- Ecosystem includes vehicle mounts, body-worn units, drone-specific
  form factors
- Integrated MANET management tools

**What's not:**
- Most expensive option ($10,000-50,000 per node)
- Heaviest option (MPU5 is not going on a 5-inch quad)
- Closed ecosystem — Wave Relay doesn't interoperate with
  batman-adv or other mesh protocols
- Long procurement cycles for military variants

**Typical use:** Military operations, high-end defense ISR,
applications where proven combat performance justifies the cost.

### Rajant

**What they sell:** BreadCrumb mesh radios. Dual-radio architecture
(each node has two radios on different bands for simultaneous
transmit and receive on different frequencies).

**What's good:**
- Dual-radio avoids the half-duplex penalty of single-radio mesh
- InstaMesh protocol handles mobility well
- Good industrial track record (mining, oil & gas)

**What's not:**
- Larger form factor than Doodle Labs
- Less drone-specific than Silvus or Persistent

**Typical use:** Industrial applications, infrastructure monitoring,
some defense applications.

---

## Mesh Networking Fundamentals

### How batman-adv Works (And Why It Matters)

batman-adv (Better Approach To Mobile Ad-hoc Networking - advanced)
is a Linux kernel module that implements layer-2 mesh routing.
It's what Doodle Labs and many other mesh products use underneath.

Key concepts:
- Each node broadcasts **OGMs** (Originator Messages) periodically.
  These propagate through the mesh, allowing every node to learn
  the best path to every other node.
- OGM interval (default 1 second) controls how fast the mesh
  adapts to topology changes. Lower = faster adaptation but more
  overhead.
- **TQ (Transmit Quality)** is batman-adv's link quality metric.
  It's calculated from OGM reception rates. Higher = better link.
- Routing is hop-by-hop. Each node only needs to know the next
  hop toward the destination, not the full path.

**Why this matters for drones:** Drones move fast. A mesh network
optimized for static nodes (cell towers, sensor posts) may not
adapt fast enough for a drone moving at 20+ m/s. If the OGM interval
is 1 second and the drone has moved 20 meters since the last OGM,
the routing table may be stale. Solutions:
- Lower OGM interval (250-500 ms for fast-moving nodes)
- Accept that mesh routing will lag position by 0.5-1 second
- Use direct unicast for time-critical messages when nodes are
  within direct radio range (bypass mesh routing)

### Throughput vs. Hops

Every hop in a mesh network costs throughput. A single-hop link
at 50 Mbps becomes roughly:
- 2 hops: ~25 Mbps
- 3 hops: ~17 Mbps
- 4 hops: ~12 Mbps

This is because traditional mesh radios are half-duplex — they
can't transmit and receive at the same time on the same channel.
Each hop requires the intermediate node to receive, then retransmit.
Rajant's dual-radio approach mitigates this by receiving on one
radio while transmitting on the other.

**For drone operations:** Keep the mesh shallow. 2-3 hops maximum
for real-time data (telemetry, commands). Store-and-forward is
acceptable for non-real-time data (sensor logs, blackbox files).

### Channel Planning

Mesh radios on the same channel form a shared collision domain.
More nodes = more contention = less per-node throughput.

Rules of thumb:
- Up to 5 nodes on one channel works well
- 5-15 nodes: consider splitting into two channels with a
  gateway node bridging them
- 15+ nodes: you need a proper network plan with multiple
  channels and deliberate topology

For drone swarms, the practical limit is usually 8-12 platforms
on a single mesh channel before throughput degrades noticeably.
This aligns with typical tactical swarm sizes.

---

## Practical Setup: Doodle Labs on a Drone

This section covers the most common drone mesh setup — a Doodle Labs
Mini radio on a multi-rotor.

### Physical Installation

- Mount with the antenna(s) pointing down or outward, not blocked
  by carbon fiber. CF is a moderate RF attenuator.
- Keep the radio away from the ESCs and battery leads. Conducted
  EMI from motor current can desense the radio's receiver.
- Power from a dedicated BEC, not the FC's 5V rail. Mesh radios
  draw 500-2000 mA and the FC's regulator may not handle it.
- Secure the Ethernet or USB cable. A disconnect in flight kills
  your mesh link and possibly your telemetry.

### Network Configuration

- Assign static IP addresses. DHCP works but adds boot time and
  can fail in contested RF environments.
- Use a consistent addressing scheme:
  `10.0.0.{MAVLink_system_ID}` — GCS is 10.0.0.255,
  drone 1 is 10.0.0.1, drone 2 is 10.0.0.2, etc.
- Set the mesh SSID and encryption key to match across all nodes.
  PSK (pre-shared key) with AES-256 is standard.
- Set the OGM interval based on platform speed:
  - Static ground nodes: 1000 ms (default)
  - Slow-moving drones (<10 m/s): 500 ms
  - Fast-moving drones (>10 m/s): 250 ms

### MAVLink Over Mesh

The companion computer (or FC with Ethernet) sends MAVLink over
UDP to the mesh radio. The mesh radio delivers it to the GCS.

```
FC (UART) → Companion (mavproxy) → UDP → Mesh Radio → [mesh] → GCS
```

MAVProxy configuration on the companion:
```
mavproxy.py --master=/dev/ttyS1,921600 --out=udp:10.0.0.255:14550
```

On the GCS, QGroundControl or Mission Planner listens on UDP 14550
for incoming MAVLink from any mesh node.

**Critical: Set the MAVLink system ID on each drone to a unique value.**
If two drones both use system ID 1, the GCS can't distinguish them.
PX4: `MAV_SYS_ID` parameter. ArduPilot: `SYSID_THISMAV` parameter.

---

## When Mesh Isn't The Answer

Mesh networking adds weight, power consumption, complexity, and
a new failure mode to every platform. Before adding a mesh radio, ask:

- **Do I need real-time data between platforms?** If each drone
  operates independently and you analyze data after landing,
  you don't need mesh. You need SD cards and patience.

- **Can I solve it with sequential operations?** If you can brief
  platforms one at a time via direct link (Tooth, phone, laptop),
  you don't need mesh. Mesh is for simultaneous coordination.

- **Is my mesh just carrying telemetry to a GCS?** If you only need
  one drone's telemetry at a time, a point-to-point telemetry
  radio (RFD900x) is simpler, cheaper, lighter, and more reliable
  than mesh.

- **Is my operation within visual line of sight?** If all platforms
  are within 500m of the operator, ESP-NOW (free, built into ESP32,
  no additional hardware) may be sufficient for coordination.

Mesh is the right answer when you need multiple platforms sharing
data simultaneously, beyond point-to-point range, with dynamic
topology. For everything else, simpler is better.

---

## Next

- **Chapter 13: Adding a Companion Computer** — the compute platform
  that bridges the FC and the mesh radio.
- **Chapter 15: TAK Integration** — getting drone data onto the
  tactical common operating picture.

---

*A $5,000 mesh radio is a $15 router with a great antenna and a
ruggedized case. Respect the engineering. But don't be intimidated by it.*
