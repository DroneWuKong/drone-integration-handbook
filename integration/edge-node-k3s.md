# Chapter 36: Portable Telemetry Edge Node (K3s)

> A companion computer thinks about one drone. An edge node thinks
> about all of them — it sits on the ground, aggregates everything
> the mesh carries, and is the last thing standing when the uplink
> to the cloud dies.

---

## When You Need One

A companion computer (Chapter 13) rides the airframe and reasons
about that one vehicle. An edge node is a **ground** box: a small
Kubernetes (K3s) node in a Pelican case that ingests telemetry from
every vehicle on the mesh, stores it locally, shows it on a screen
at the test site, and forwards a refined copy to the cloud when a
link is available.

You want one when:

- **Multiple vehicles, one picture** — you're flying a swarm or a
  sequence of test flights and want every vehicle's telemetry
  aggregated, queryable, and overlaid in one place on site.
- **The uplink is intermittent** — cellular drops behind terrain,
  Starlink re-orients, the directional backhaul gets bumped. You
  need data to survive the outage and sync when the link returns.
- **You want analytics in the field, not after** — PID trends,
  battery-sag curves, link-margin-vs-range plots while you can still
  change something, instead of on the drive home.
- **You're bridging the field to a back-end** — the node is the
  clean boundary between "raw MAVLink on a tactical mesh" and
  "structured time-series in a cloud TSDB."

If you're flying one drone and watching it on a GCS, you don't need
this. A GCS shows you *now*; an edge node remembers, aggregates, and
forwards. Don't add a cluster to watch a single battery gauge.

---

## Why K3s Specifically

K3s is a CNCF-certified Kubernetes distribution in a single ~70 MB
binary. The properties that matter in the field are not the ones
that matter in a datacenter:

| Property | Why it matters in austere conditions |
|----------|--------------------------------------|
| Single binary, 5–15 W | Runs on a Pi 5, Jetson Orin Nano, or fanless x86 off a power bank or vehicle 12 V |
| SQLite datastore default | A single node is a real deployment, not a degraded cluster — no 3-node etcd quorum to stand up |
| Agent survives a dead control plane | Workloads keep running when the node can't reach anything upstream — the normal case in the field |
| Air-gap friendly | Pre-load images with `k3s ctr images import`; the node boots with zero internet |
| Declarative redeploy | After a battery swap and reboot, everything comes back exactly as specified |

The failure mode K3s avoids: a stack of `systemd` services and
hand-run Docker containers that nobody can bring back identically
after the box reboots mid-test. The cost: you have to think in
manifests. For a box you redeploy across sites and reboot often,
that trade favors K3s.

> A working reference deployment of everything below — manifests,
> the MAVLink→MQTT decoder, the store-and-forward config — lives in
> the `Ai-Project` repo under `infra/edge-node/`. This chapter is
> the field-facing "why"; that directory is the "how."

---

## The Data Path

```
Flight controller / companion
        │  MAVLink UDP :14550  (over the mesh)
        ▼
   mavlink-router ──TCP :5760──> GCS on the mesh (Prismo / QGC)
        │
        ▼
   MAVLink → MQTT decoder  (pymavlink)
        ▼
   MQTT broker (Mosquitto)
        ▼
   Telegraf (MQTT → line protocol)
        ▼
   vmagent ─┬─> VictoriaMetrics (local, full resolution)
            └─> cloud aggregator (store-and-forward over the uplink)
        ▼
   Grafana (local screen)  ←  reads VictoriaMetrics
```

The shape worth internalizing: a **message bus in the middle**
(MQTT), a **local store** (VictoriaMetrics), and a **forwarder with
an on-disk queue** (vmagent) as the cloud boundary. Decoupling the
decoder from storage via the bus means a database restart never
drops the ingest socket. Putting a disk-backed queue at the cloud
boundary means a dead uplink never loses data.

### Match the Payload to the Pipe

The mesh transport under the telemetry decides what is even possible.
Chapter 14 (Mesh Radios) covers the radios; here's the rule for
telemetry specifically:

| Transport | Layer | What it's good for |
|-----------|-------|--------------------|
| B.A.T.M.A.N. adv | L2 (`bat0`) | Multi-hop mesh that looks like one flat Ethernet to K3s — pods see normal IPs. Raw MAVLink + video between ground nodes. |
| DroneBridge | L2 (Wi-Fi) | Air-to-ground transparent MAVLink pipe. Good for the FC→node hop. |
| LoRaWAN | L3-ish, tiny | Hundreds of bytes, seconds of latency. Distilled status only — never raw streams. |

The hard rule: **raw MAVLink rides B.A.T.M.A.N. / DroneBridge;
LoRaWAN gets only the heartbeat-level summary** (position, battery
percent, GPS fix, alerts), decoded at the gateway and published as a
handful of fields. Tunneling a telemetry stream over LoRa does not
fail loudly — it silently saturates the duty cycle and the link goes
useless for everyone on that channel. Decode at the gateway; forward
the summary.

---

## B.A.T.M.A.N. adv Tuning for Telemetry

B.A.T.M.A.N. Advanced (`batman-adv`) is the workhorse for ground
meshes here because it operates at layer 2: once `bat0` is up, K3s,
MAVLink, RTSP, and MQTT all just see a flat Ethernet segment and a
normal IP subnet, regardless of how many hops away the peer is. No
routing daemon to configure per-service.

Minimal bring-up on each node (the radio is in IBSS/ad-hoc or 802.11s
mode first; `batman-adv` rides on top):

```bash
# wlan0 already in ad-hoc mode, same SSID/channel/cell on every node
modprobe batman-adv
batctl if add wlan0
ip link set up dev wlan0
ip link set up dev bat0
ip addr add 10.10.0.<n>/24 dev bat0   # unique <n> per node
```

The settings that actually move latency and stability for telemetry:

| Setting | Default | For telemetry | Why |
|---------|---------|---------------|-----|
| `batctl orig_interval` (OGM interval) | 1000 ms | 1000 ms, or **2000–5000 ms** for static ground nodes | OGMs are mesh overhead. Faster = quicker reconvergence when a node moves, but more airtime stolen from data. Static ground nodes don't need 1 Hz topology gossip. |
| `batctl bridge_loop_avoidance` | off | **on** if any node also has a wired/AP bridge | Prevents L2 loops when a node double-homes the mesh to Ethernet/Wi-Fi-AP. A loop here floods the channel and telemetry latency goes to seconds. |
| `batctl hop_penalty` | 30 | raise toward 60 to **prefer fewer hops** | Each B.A.T.M.A.N. hop adds airtime + retransmit latency. Penalizing hops keeps a marginal direct path over a 3-hop relay when both exist. |
| Multicast | on | keep **on** | MAVLink-over-UDP broadcast and mDNS depend on it; turning it off to "save airtime" breaks discovery. |
| Wi-Fi rate | auto | **fix a low rate** (e.g. 6 Mbps) on long links | Rate auto-negotiation thrashes at the edge of range; a fixed conservative rate is more stable for a telemetry-only link than a flapping high rate. |

**Field experience that maps to these knobs:** on a 3-node 2.4 GHz
ad-hoc mesh with omni antennas, two nodes ~400 m line-of-sight and a
third behind a tree line at ~150 m, leaving the OGM interval at the
1 s default and rate at auto produced 200–800 ms telemetry jitter and
periodic 2–3 s stalls whenever the obscured node's rate renegotiated.
Pinning the link to 6 Mbps and raising the hop penalty so the obscured
node relayed through the nearer peer instead of fighting for a direct
path dropped jitter to a steady ~60–90 ms. The mesh got *slower* on
paper and *better* in practice — the lesson is that for telemetry,
predictable beats fast.

**Failure mode to expect:** a bridge-loop-avoidance miss. The moment
one node bridges `bat0` to a wired LAN (to give the edge node
internet, say) without `bridge_loop_avoidance on`, you can form an
L2 loop. It presents as the whole mesh going to multi-second latency
and high retransmits with no obvious culprit — every node looks busy
because the loop is flooding broadcast. Turn BLA on before you
double-home any node, not after you're debugging it in the field.

### Choosing the routing algorithm: BATMAN_IV vs BATMAN_V

`batman-adv` ships two routing algorithms, and which one you pick
changes the meaning of half the table above.

| | BATMAN_IV (default) | BATMAN_V |
|---|---|---|
| Topology gossip | OGM flooding | ELP (per-neighbour probes) + OGMv2 |
| Path metric | hop count + packet loss (TQ, 0–255) | estimated **throughput** |
| Your levers | `orig_interval`, `hop_penalty` | mostly automatic |
| Heterogeneous rates | hand-tuned | self-optimising |

- **BATMAN_IV** ranks paths by a transmit-quality (TQ) score that
  degrades per hop — so the `hop_penalty` / `orig_interval` knobs in
  the table are IV's levers. Simple, deterministic, easy to debug.
- **BATMAN_V** ranks paths by **measured throughput**, so it
  naturally avoids a marginal link or a slow relay without you
  hand-tuning `hop_penalty`. On a mixed-rate mesh (some nodes close,
  one obscured) V usually gives steadier telemetry with less fiddling.
- Set it **before** `bat0` exists — the algorithm can't change while
  interfaces are attached:

  ```bash
  batctl routing_algo BATMAN_V   # then bring up bat0 as before
  ```

- **Every node must run the same algorithm.** IV and V do **not**
  interoperate. The failure mode is silent: a node left on default IV
  joining a V mesh shows an **empty originator table** (`batctl o`)
  even though the radio link is perfectly fine. If `batctl n` lists
  neighbours but `batctl o` is empty, suspect an algorithm mismatch
  before you suspect RF.

Rule of thumb: reach for **V** on a heterogeneous or moving mesh and
drop the `hop_penalty` tuning; keep **IV** when you want simple,
predictable, hand-reasoned behaviour on uniform hardware.

### 2.4 GHz vs 5 GHz for the telemetry mesh

| | 2.4 GHz | 5 GHz |
|---|---|---|
| Range / penetration | **better** (longer, through foliage/walls) | shorter, line-of-sight-ish |
| Clean spectrum | crowded (Wi-Fi, BT, analog video) | mostly clean, many non-overlapping channels |
| Channel width | narrow, few clear channels | wide channels available |
| Gotcha | co-channel interference | **DFS radar-avoidance blackouts** |

- For **C2 / telemetry**, robustness beats bandwidth — 2.4 GHz's
  range and penetration usually win, *if* you can find a clean
  channel away from the site's Wi-Fi and the analog FPV video.
- **Never put C2 telemetry on a DFS channel.** If the radio detects
  (or thinks it detects) radar, it must vacate the channel for
  seconds to minutes — a hard, non-negotiable link blackout while the
  aircraft is flying. DFS is acceptable for bulk video you can lose;
  it is not acceptable for the control link.
- If video shares the mesh, **split the bands**: high-rate video on
  its own 5 GHz wide channel, low-rate telemetry on a robust 2.4 GHz
  channel. Mixing a saturating video stream and C2 on one radio is
  the most common cause of "telemetry gets choppy whenever I'm
  streaming."

### MTU and fragmentation

`batman-adv` prepends its own header to every frame. If `bat0` keeps
the standard 1500-byte MTU on top of a 1500-byte radio, every full
packet **fragments** — a throughput and latency tax.

- The clean fix: raise the *underlying* interface MTU to ~1560
  (1500 + batman-adv overhead) so `bat0` can present a full 1500
  without fragmenting. Many Wi-Fi drivers support this; some don't.
- If you can't, leave fragmentation on (`batctl fragmentation enable`,
  the default). For **telemetry** this is mostly moot — MAVLink
  packets are tiny and rarely fragment. It bites **video** (large
  RTSP packets), so this knob matters most on a mesh that also carries
  the stream.

### Gateway mode — electing the uplink node

When more than one node can reach the cloud (e.g. two vehicles within
LTE coverage), let `batman-adv` elect the uplink instead of static
routes:

```bash
# on the node holding the backhaul:
batctl gw_mode server 10000/2000     # advertised up/down kbit/s
# on every other node:
batctl gw_mode client
```

Clients then auto-select the best-announced gateway and default-route
through it, with automatic failover if that node drops off. This pairs
directly with store-and-forward: the vmagent node simply follows the
elected gateway to reach the cloud. **Failure mode:** multiple
`server` nodes plus a loose client selection class can cause clients
to flap between gateways mid-flight — pin a single server, or set a
stable selection class, when determinism matters more than failover.

### DAT and multicast

- **Distributed ARP Table** (`batctl distributed_arp_table`, on by
  default): caches ARP mesh-wide so an ARP lookup doesn't broadcast-
  flood every hop. Keep it on for any multi-node mesh.
- **Multicast** (`batctl multicast_mode`, on by default): converts
  multicast to targeted unicast when there are few listeners — good,
  keep it. But note a **MAVLink UDP broadcast** (to `…255`) is still
  treated as broadcast and floods every hop. For high-rate streams,
  send **directed UDP to the node's `bat0` IP** (as the edge node's
  `:14550` ingest does) and reserve broadcast for low-rate discovery.

### Test before you fly (`batctl`)

A 60-second pre-flight from the edge node catches a bad link while you
can still fix it (re-aim an antenna, drop the rate, reposition a
relay) instead of discovering it as a telemetry stall at altitude:

| Command | What it tells you |
|---------|-------------------|
| `batctl ping <mac>` | L2 round-trip to a neighbour, bypassing IP — raw link latency |
| `batctl tp <mac>` | **measured** throughput to that node — trust this before routing video over a hop |
| `batctl o` | originator table: who's reachable, via which next-hop, with TQ (IV) / throughput (V) |
| `batctl n` | direct neighbours + last-seen age |
| `batctl tg` | translation table — confirms the FC/companion's MAC is visible mesh-wide |

The go/no-go: every airframe-side node should answer `batctl ping`,
post healthy `batctl tp`, and show in `batctl o` with **TQ ≥ ~200**
(BATMAN_IV) or solid throughput (BATMAN_V). A link sitting at
**TQ < ~150** will produce intermittent telemetry stalls under load —
treat it as a fail and fix the RF before launch, not after.

---

## Store-and-Forward: Surviving the Uplink

The single hardest requirement is also the most mundane: **don't
lose data when the uplink dies, and don't let the dying uplink take
local visibility down with it.** The link to the cloud is *expected*
to be intermittent. The design treats an offline uplink as the
normal case, not an error.

The mechanism is a forwarder (vmagent) with a separate **on-disk
queue per destination**:

```
                    ┌─> local VictoriaMetrics   (always up, queue ~empty)
   telemetry ──> forwarder
                    └─> cloud aggregator        (flaky uplink, spools to disk)
```

The two destinations do not share fate. The local write drains in
milliseconds and feeds the on-site Grafana, so the operator's live
view never depends on the uplink. The cloud write spools to disk
when the link is down and drains oldest-first, in order, with
backpressure, when the link returns — no loss, no reordering, no
manual intervention, and it survives a node reboot because the queue
is on persistent storage.

Why not let the dashboard or the collector buffer in memory instead?
Because in-memory buffers are bounded and drop the *oldest* data
first during a long outage — exactly the data you spooled because you
couldn't afford to lose it. A multi-hour outage plus a battery-swap
reboot is the design case; that needs a disk-backed queue measured in
gigabytes, not a RAM buffer measured in megabytes.

### Sizing the Queue

How long you can stay offline before the queue cap starts dropping
the oldest samples:

```
offline_window ≈ disk_cap / (bytes_per_sample × samples_per_second)
```

For one drone at ~1 Hz the math is generous — a couple of GB holds
*weeks* of total cloud blackout, because compressed time-series runs
under ~1 byte per sample. The cap only bites at fleet scale: tens of
drones at multi-Hz fills the same couple of GB in a day or two. Run
the arithmetic for your fleet and ingest rate, size the disk to the
worst-case outage you actually expect, and **set a hard per-destination
cap** so a long outage drops bounded old data instead of filling the
card and crashing the node.

### Reduce What Crosses the Link

The cheapest byte is the one you don't send. Two levers, both applied
*only* to the cloud copy so local fidelity is untouched:

1. **Downsample before the cloud** — roll up to 10 s or 1 min
   averages/min/max for the uplink while the local store keeps full
   resolution. Biggest win on a metered link.
2. **Drop high-rate series from the cloud copy** — keep attitude and
   rate channels local; forward only position, battery, and GPS fix.

The detailed queue math, the per-destination relabel/aggregation
config, and the full failure-mode table live alongside the manifests
in `Ai-Project` at `infra/edge-node/STORE-AND-FORWARD.md`.

---

## Relationship to the GCS and to CoT

An edge node is **not** a replacement for a ground control station.
The GCS (Prismo Prime, QGroundControl) is the operator's command and
control surface — it arms vehicles, runs missions, and shows the live
map. The edge node is a headless aggregator: it persists, analyzes,
and forwards. They run side by side. In the reference stack the
MAVLink router keeps a TCP server open on `:5760` specifically so a
GCS on the mesh can attach to the same raw stream the node is
ingesting — the node taps the firehose, it doesn't gate it.

The natural fan-out to end users is **CoT** (Cursor-on-Target — see
Chapter 15). The same B.A.T.M.A.N. mesh that carries MAVLink to the
edge node can carry CoT to ATAK end-user devices. A small bridge on
the node that turns each vehicle's decoded position into a CoT event
puts every tracked drone on every ATAK screen on the mesh, while the
full-resolution telemetry goes to the local TSDB and the refined copy
goes to the cloud. One ingest, three consumers: the database, the
cloud, and the tactical picture.

---

## What to Start With

1. **Prove the path on one node, one drone.** Install K3s on a Pi 5,
   apply the reference stack, point a companion's MAVLink output at
   the node's IP, and watch the battery gauge move in a local Grafana.
   No mesh, no cloud — just the ingest path.
2. **Add the mesh.** Bring up `batman-adv` between the node and the
   air side, move the MAVLink feed onto `bat0`, and tune per the
   table above until jitter is steady.
3. **Add the cloud.** Point the forwarder's second destination at
   your cloud TSDB and pull the uplink cable mid-flight to confirm
   the queue spools and drains. That test — not a clean-network demo
   — is the one that tells you the node is field-ready.

The hardware scales from a $80 Pi to a Jetson to a rugged x86 without
changing any of this. The data path stays the same. Learn it once on
a Pi on the bench, and it's the same node in the case at the range.

---

## Next

- **Chapter 13: Adding a Companion Computer** — the air-side box that
  feeds this ground-side one.
- **Chapter 14: Mesh Radios for Multi-Vehicle** — the radios under
  `bat0`.
- **Chapter 15: TAK Integration** — the CoT fan-out to end users.

---

*The companion thinks about the drone. The edge node remembers the
flight, shows it to you on site, and gets it home when the link comes
back. Build the queue before you need it.*
