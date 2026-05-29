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

## Choosing a Mesh Routing Protocol

The "Mesh Networking Fundamentals" section above describes how batman-adv
works. The harder question is whether batman-adv is the *right* protocol for
a fast-moving drone swarm. The honest answer, backed by the one published
real-flight comparison, is: usually not.

### batman-adv is a community-mesh protocol, not a mobility protocol

batman-adv was built by the German Freifunk community to replace OLSR in
large, mostly-static rooftop mesh networks. The "Mobile" in the name means
"infrastructure-less," not "high-velocity." Its known weaknesses bite exactly
where a swarm lives:

- **Slow reaction.** The default OGM interval is 1000 ms; in a FANET the
  topology can change completely inside that window. BATMAN V's throughput
  metric uses a heavily-smoothed average (EWMA, α≈0.125), so a link dropping
  from 50→5 Mbps can take **~10 seconds** to register, and the protocol will
  keep routing over an already-dead link until a 30–60 s timeout
  ([EWSN 2024 measurement](https://ewsn.org/file-repository/ewsn2024/ewsn2024posters-final14.pdf)).
- **Broadcast flooding.** batman-adv floods broadcast/multicast across the
  whole mesh. Fine for small control traffic; past ~50 nodes it needs
  multicast filtering, and it "fails for multicast streaming."
- **The field result.** In a real outdoor multi-UAV test (two quadcopters
  plus a relay, 802.11 ad-hoc), batman-adv delivered the **lowest throughput
  and highest packet loss of the three protocols tested** — worse than both
  OLSR and Babel — explicitly because "its routing-update period was
  originally not intended for FANETs"
  ([MDPI Appl. Sci. 11:4363](https://www.mdpi.com/2076-3417/11/10/4363)).

It can be made to work — lower the OGM/ELP interval to ~500 ms, run it over a
stable link mode, and accept that positive published UAV results lean on
either *connectivity-aware flight* (the swarm maneuvers to hold links) or
*custom GPS-predictive metrics that are not in the mainline kernel*. For a
swarm with genuinely fast, arbitrary topology change, that is a lot of
tuning to land in third place.

### The open-source alternatives

A useful distinction: **layer-2** protocols (batman-adv, 802.11s/HWMP) route
on MAC addresses and present a transparent bridge; **layer-3** protocols
(Babel, OLSR, BMX) route on IP. Layer-3 protocols run over *any* link —
IBSS ad-hoc, 802.11s mesh-point, or wired — which decouples your routing
choice from the chipset's mesh-mode quirks. HWMP is the exception: it only
runs over 802.11s.

| Protocol | L2/L3 | Link mode | Mobility | Scale (10s–100s) | Maturity | Verdict |
|---|---|---|---|---|---|---|
| **Babel** | L3 | any | **Strong** — built for wireless mobility, loop-free reconverge | Good | High — [RFC 8966](https://www.rfc-editor.org/rfc/rfc8966.html), in FRR/BIRD | **Primary choice** |
| OLSRv2 (OONF) | L3 | any | Moderate — MPR favors *dense*, not sparse | Good in dense | [RFC 7181](https://datatracker.ietf.org/doc/rfc7181/) | Standardized fallback |
| batman-adv IV/V | L2 | any | Weak for fast FANET | Good (community) | High — mainline kernel | Only with heavy tuning |
| 802.11s + HWMP | L2 | 802.11s only | Weak — "does not consider mobility" | Limited | In mac80211 | Avoid for mobile |
| BMX7 | L3 | any | Little evidence | "100s" claimed | Inactive since 2019 | Skip |
| AODV / DSR / AODVv2 | L3 | any | Fast reaction, high discovery latency | Churn-sensitive | No production Linux build | Research only |

**Recommendation:** prototype on **Babel** — it is the one protocol that beat
both OLSR and batman-adv in the real UAV test, it is IETF-standardized
(RFC 8966), it is mobility-designed, and it runs over any link mode so you
are not married to IBSS or 802.11s. Keep **OLSRv2** as the standardized
fallback. Note that long-range/sparse topologies specifically *disfavor*
OLSR's MPR flooding optimization, which is tuned for dense networks — another
point for Babel. If pure topology routing still struggles at speed, add
geographic / mobility-predictive forwarding (P-OLSR-style, GPS-fed).

---

## The MAC Layer: Why CSMA/CA Limits You

Above the routing protocol and below it lies the part you usually cannot
change on commodity WiFi: the medium-access layer. Standard 802.11 uses
CSMA/CA — listen, contend, back off — and it degrades structurally in
multi-hop, mobile meshes:

- **Per-hop collapse.** In a multi-hop chain, per-hop throughput falls roughly
  as 1/n; the hidden-node problem and exponential backoff make it worse as the
  chain lengthens. This is a property of contention-based access, not a
  tuning bug.
- **The rate anomaly.** Because DCF gives every station equal *transmission
  opportunity* rather than equal *airtime*, a single slow or fading link drags
  the whole cell's aggregate throughput down toward the slow rate
  ([Heusse et al., INFOCOM 2003](https://www.researchgate.net/publication/4021079_Performance_Anomaly_of_80211b)).
  In a mobile mesh, somebody is always the slow link.

What you *can* fix on COTS WiFi, without an SDR, is real but bounded:

- **Airtime fairness.** The mac80211 airtime-fairness scheduler largely
  neutralizes the rate anomaly — in testing it raised aggregate throughput of
  three mixed-rate stations from ~20 Mbps to >100 Mbps and cut latency from
  ~300 ms (high variance) to ~10 ms. It has been in mainline Linux since
  **4.11** and was moved into mac80211 in 2019
  ([USENIX ATC '17](https://www.usenix.org/system/files/conference/atc17/atc17-hoiland-jorgensen.pdf)).
  This is the single biggest free win, and it favors the ath9k driver.
- **Long-range tuning.** `iw`/OpenWRT `distance` (coverage class) widens the
  ACK timeout for long propagation delays; fixing the MCS and disabling rate
  adaptation stabilizes marginal links. These help sparse long links and fast
  movers — but they do not change the contention behavior.

What you **cannot** do on COTS WiFi: replace CSMA/CA with a scheduled MAC. The
access method lives in chip firmware. Mainline 802.11s gives you only EDCA
(still CSMA); the standard's contention-free reservation scheme, MCCA, is
[not implemented](https://github.com/o11s/open80211s/wiki/Status) in the
mainline Linux mesh stack. Driver-level TDMA overlays exist on specific
Atheros chips (the WiLDNet/RCP lineage, hMAC, Det-WiFi/RT-WiFi) and have shown
2–5× gains, but they are research-grade, chipset-locked, and brittle under
mobility. A real time-slotted MAC across a fast swarm means an SDR or a
purpose-built radio — which is precisely why the tactical radios below run
proprietary non-802.11 MACs.

---

## Open-Source Waveforms and the SDR Question

If the MAC ceiling on commodity WiFi frustrates you, the next instinct is to
build your own physical-layer waveform on a software-defined radio. Be honest
with yourself about the effort before you spend the money. The realistic
open-source paths are mostly *not* custom PHY work.

| Stack | Data rate | Latency | Hardware | Maturity | Use it for |
|---|---|---|---|---|---|
| **Meshtastic / LoRa** | <10 kbps | seconds | SX126x + MCU (cheap, no SDR) | Deployable | Robust long-range backup C2 / telemetry |
| **wfb-ng / DroneBridge** | Mbps | low | Commodity WiFi (monitor mode) | Deployable | Video + telemetry — rides 802.11, not a new PHY |
| **openwifi** | 802.11a/g/n | real 10 µs SIFS (FPGA MAC) | Zynq SoC SDR | Usable, niche | The *only* credible open custom PHY+MAC |
| GNU Radio custom MAC | tens of Mbps PHY | ~30 ms RTT | USRP + host PC | Research | Demonstrators — can't meet real-time MAC timing |
| OAI LTE/5G NR sidelink | LTE/NR | 10s ms | multi-USRP | Lab-grade / incomplete | Not a fieldable swarm link yet |
| FreeDV / Codec2 modems | 58–980 bps (20 kbps 4FSK) | seconds | SDR / sound card | Mature lib | Beacon-class robust data, down to −4 dB SNR |

The pattern: for genuinely long-range, low-rate, resilient command traffic,
**Meshtastic/LoRa** ships today on cheap hardware. For higher-rate telemetry
and video, **wfb-ng** rides the existing 802.11 PHY rather than inventing one.
If you truly need a custom SDR PHY with deterministic MAC timing, **openwifi**
is the only credible open option, because it puts the time-critical MAC in the
FPGA (the 10 µs SIFS that pure GNU Radio cannot hit) — but you inherit Zynq
SDR hardware cost and still have to build the mesh layer on top. Building a
MANET waveform in pure GNU Radio is a research-grade money pit: the
host-software architecture cannot meet real-time MAC timing (~30 ms
round-trip, unsynchronized clocks, packets marked "late"). Open 5G NR sidelink
is the deepest pit of all — only two of the four sidelink physical channels
exist in open implementations, and it is scoped for automotive V2X, not swarm
MANET.

---

## What the Professionals Actually Run

The tactical radios in the "Major Players" table are valuable precisely
because their waveform and MAC are closed — that is the part you are paying
for. They split into two design philosophies, and both are instructive:

- **Routed mesh:** Silvus (MN-MIMO waveform, proven to 550+ nodes) and
  Persistent Wave Relay use proprietary mesh-routing over custom MIMO radios.
- **Routing-free flooding:** TrellisWare's **TSM (Tactical Scalable MANET)**
  uses "Barrage Relay" — it *eliminates routing entirely* and floods through
  cooperative relays, proven with 800+ radios and 26 mi/hop. Counter-intuitive
  but powerful: under fast topology change, well-managed flooding can beat a
  routing protocol that can't reconverge in time. (If you are experimenting
  with barrage-style flood relays on your own nodes, this is the precedent.)

The strategic lesson for an open-source builder: **ATAK and even DARPA's
OFFSET swarm program sit *on top* of these radios as radio-agnostic IP** —
they do not define their own link. You cannot legally or practically clone
MN-MIMO or TSM. So the honest options are (1) run open routing (Babel/OLSR)
over commodity WiFi and accept its limits, or (2) buy a COTS MANET radio whose
waveform you treat as a black box. **Doodle Labs Mesh Rider is the bridge
between those worlds** — it is OpenWRT-based, so you SSH in and run your own
open IP stack (Babel, MAVLink, ROS 2/DDS) on top of a tactical-grade waveform
you didn't have to build. It is also a documented-compliance NDAA path, unlike
a commodity card whose chip lineage tells you nothing about where the board
was made.

---

## Decision Matrix: Routing / MAC / Waveform

For a command-and-telemetry swarm mesh (not video) optimizing for **swarm
scale + high mobility + long range** on open-source COTS-or-SDR hardware:

| Layer | Choose | Why |
|---|---|---|
| **Routing** | **Babel** (OLSRv2 fallback) | Won the real UAV test; mobility-designed; link-agnostic; standardized |
| **Link mode** | 802.11s mesh-point *or* IBSS | Babel runs over either; 802.11s sidesteps fragile IBSS support on newer chips |
| **MAC** | CSMA/CA + airtime fairness on + long-range ACK tuning + fixed MCS | The only real COTS wins — do not chase TDMA on WiFi |
| **Radio (COTS)** | ath9k-class (AR9271 USB / AR9280 mini-PCIe) | Best COTS ad-hoc/802.11s reliability and injection; clean chip lineage |
| **Backup C2** | Meshtastic / LoRa as a second link | Robust long-range telemetry when the WiFi mesh degrades |
| **If you outgrow COTS** | Doodle Labs Mesh Rider; run your open stack on its OpenWRT | Tactical range without building a waveform |
| **Only if you must build PHY** | openwifi on a Zynq SDR | The sole credible open custom MAC; budget real effort |

**When batman-adv is still fine:** small or slow swarms, connectivity-aware
flight that keeps the topology quasi-static, or where you have already tuned
the OGM/ELP intervals and validated it in the air. **When to move off it:**
anything with genuinely fast, arbitrary topology change at scale — go Babel.

### Radio chip by link role

A drone with both an HD video downlink and a mesh carries two different
radio problems, and no single chip is best at both. The video link
(wifibroadcast/OpenHD — see the OpenHD Implementation Guide) wants a
monitor-mode injection card; the mesh wants reliable IBSS/802.11s and,
for a contested low-latency mode, raw injection. This table spans both.

Ratings: **Best** / **Good** / **Limited** (works but constrained or needs
validation) / **No** (don't).

| Chip | HD video P2P (wifibroadcast) | Mesh — routed (IBSS/802.11s) | Mesh — barrage (raw inject) | Band | Bus | Production | Chip origin |
|---|---|---|---|---|---|---|---|
| **RTL8812AU** | **Best** — the standard | No — Realtek IBSS/802.11s is poor | Limited — injects, but not the usual barrage chip | 2.4/5, WiFi-5 | USB | Current | Realtek (Taiwan) |
| **AR9271** (ath9k_htc) | Limited — the *original* wifibroadcast card; 2.4 GHz, low bitrate | Good — solid IBSS | Good — common barrage injector | 2.4, WiFi-4 | USB | EOL | Atheros/Qualcomm |
| **AR9280** (ath9k) | Limited — WiFi-4 bitrate | **Best** — IBSS + 802.11s | Good | 2.4/5, WiFi-4 | mini-PCIe | EOL | Atheros/Qualcomm |
| **MT7612U** (mt76x2) | Limited — experimental in wfb (Realtek-first) | Good — usable IBSS + 802.11s | Good — injects; validate per kernel | 2.4/5, WiFi-5 | USB / M.2 | Available | MediaTek (Taiwan) |
| **MT7915/16** (mt76) | No — monitor-mode firmware crash ≥80 MHz, injection unproven | No — IBSS broken; 802.11s 2.4 GHz only | Limited — unvalidated | 2.4/5, WiFi-6 | PCIe / M.2 | Current | MediaTek (Taiwan) |

**Read-out:** RTL8812AU owns the video link; ath9k (AR9271/AR9280) and
MT7612U own the mesh. The only plausible *single-chip, both-jobs* part is
**MT7612U** — it can run wifibroadcast video (experimentally) and mesh
(IBSS/802.11s/barrage) on one current, embeddable radio, at the cost of
inferior video versus a dedicated RTL8812AU. Note the reliability/longevity
trap: the best mesh-IBSS chips (ath9k) are **end-of-life and dongle-centric**,
which is a poor base for an integrated product — another reason to route the
mesh with Babel over 802.11s (so you are not locked to a legacy IBSS chip) and
choose a current, embeddable module.

### Sources and further reading

- [MDPI Appl. Sci. 11:4363 — FANET routing comparison (real conditions)](https://www.mdpi.com/2076-3417/11/10/4363)
- [BATMAN V mobility measurement (EWSN 2024)](https://ewsn.org/file-repository/ewsn2024/ewsn2024posters-final14.pdf) · [UAV/V2X BATMAN V study (arXiv 1901.02298)](https://arxiv.org/pdf/1901.02298)
- [RFC 8966 — Babel](https://www.rfc-editor.org/rfc/rfc8966.html) · [RFC 7181 — OLSRv2](https://datatracker.ietf.org/doc/rfc7181/)
- [Airtime fairness on ath9k (USENIX ATC '17)](https://www.usenix.org/system/files/conference/atc17/atc17-hoiland-jorgensen.pdf) · [open80211s MCCA status](https://github.com/o11s/open80211s/wiki/Status)
- [openwifi (open-source 802.11 SDR)](https://github.com/open-sdr/openwifi) · [Meshtastic mesh algorithm](https://meshtastic.org/docs/overview/mesh-algo/) · [wfb-ng](https://github.com/svpcom/wfb-ng)
- [TrellisWare TSM / Barrage Relay](https://www.trellisware.com/waveforms/tsm-waveform/) · [Silvus MN-MIMO](https://silvustechnologies.com/products/streamcaster-mini-5200/) · [Doodle Labs technology](https://doodlelabs.com/technology/)

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
