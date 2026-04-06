# Repeater & Relay Deployment

> FPV range is limited by line of sight between the pilot and the drone.
> Terrain, buildings, and vegetation block the signal. A repeater drone
> — flown to altitude as a communication relay — extends operational
> range beyond direct LOS. TAF Industries produces the Kolibri 13 FR1
> purpose-built repeater. This guide covers the generic principles for
> deploying any drone as a relay, whether purpose-built or improvised.

**Cross-references:** [Frequency Planning](frequency-planning.md) ·
[EW Countermeasures](ew-countermeasures.md) ·
[Link Budgets](../fundamentals/link-budgets.md) ·
[Comms & Datalinks](../components/comms-datalinks.md) ·
[Video Transmitters](../components/video-transmitters-vtx.md) ·
[C2 Datalinks](../components/c2-datalinks.md)

---

## Why Repeaters

RF signals travel in straight lines. At ground level, the Earth's
curvature, terrain, trees, and buildings create blind spots where your
control link and video link cannot reach. A repeater at altitude solves
this by creating two shorter line-of-sight paths instead of one blocked
long path:

```
Without repeater:
  Pilot ----X---- [hill] ----X---- Drone
  (no LOS = no link)

With repeater:
  Pilot -------- Repeater (200m AGL) -------- Drone
  (two clear LOS paths)
```

The altitude advantage is enormous. At 200m AGL, the radio horizon
extends roughly 50 km in every direction (assuming flat terrain).
Even modest altitude (100m) clears most urban and forested terrain.

---

## Repeater Architectures

### Type 1: Dedicated Relay Drone

A separate platform whose only job is to hover at altitude and relay
signals. No camera, no payload — just radios, battery, and GPS hold.

**Advantages:** purpose-optimized, maximum endurance (no payload weight),
can use larger battery, simplest operational concept.

**Disadvantages:** consumes an entire drone and operator for relay duty,
single point of failure for all NLOS platforms.

**Example:** TAF Industries Kolibri 13 FR1. Half the cost of a DJI
Matrice-based relay. Ready to use out of the box. One day operator
training.

### Type 2: Mother Drone with Relay Function

A larger drone (7" or 10"+) that carries FPV drones as payload AND
acts as a signal relay while the FPV drones operate. The mother drone
provides both transport and communication relay.

**Advantages:** dual-purpose, extends FPV range to 60-70 km (mother
drone range + FPV range from mother), reduces total platforms needed.

**Disadvantages:** complex operations, mother drone loss = loss of all
carried FPVs, higher cost platform.

### Type 3: Fixed Repeater (Ground-Based)

A mast-mounted or building-mounted relay station. Not a drone — a
fixed radio installation at elevation.

**Advantages:** unlimited endurance (wired power), no flight operations
needed, can be hardened/concealed.

**Disadvantages:** fixed position (can't reposition quickly), vulnerable
to detection and targeting, requires physical access to install.

**Example:** IRONghost QS ground station with mast-mounted antenna
provides 1 km operator standoff via CAT5 cable.

---

## Link Budget for Relay

A relay adds a second hop to every link. Each hop has its own path
loss. The total system performance is limited by the weaker of the
two hops.

### Control Link (Ground → Repeater → Drone)

```
Ground TX → [path loss A] → Repeater RX
Repeater TX → [path loss B] → Drone RX
```

The repeater receives the control signal and retransmits it. Total
latency increases by the repeater's processing time (typically 1-5 ms
per hop for digital systems). For CRSF/ELRS at 250 Hz, 2-5 ms added
latency is imperceptible to the pilot.

### Video Link (Drone → Repeater → Ground)

```
Drone VTX → [path loss B] → Repeater video RX
Repeater video TX → [path loss A] → Ground RX (goggles)
```

**Analog video relay:** the repeater receives the analog video signal
and retransmits it on a different channel. Each relay hop adds noise
to the analog signal. After one relay hop, video quality is noticeably
degraded. After two hops, it's often unusable. One relay hop is the
practical maximum for analog video.

**Digital video relay:** digital signals don't degrade per hop (they
either work or they don't). Digital relay adds latency (decode +
re-encode) but maintains image quality. This is a significant
advantage for relay operations.

### Power Budget

Each hop must have sufficient link margin independently. If either
hop is weak, the relay doesn't help.

**Rule of thumb:** the repeater needs at least the same TX power as
the ground station for the ground-to-repeater hop, and the drone's
VTX/RC link must have enough power for the drone-to-repeater hop at
the intended operating distance.

---

## Deployment Procedures

### Site Selection

1. **Altitude:** 100-300m AGL is the sweet spot. Higher = more coverage
   but more wind exposure and more visible to enemy. Lower = less
   coverage but less conspicuous.
2. **Position:** ideally at the midpoint between the ground station and
   the operational area. If terrain is the problem, position the
   repeater to clear the specific obstruction.
3. **Wind:** the repeater must hold position in wind. GPS hold mode is
   essential. In strong wind, the drone will drain battery fighting
   to hold station. Monitor battery consumption rate and plan endurance
   accordingly.

### Pre-Flight

1. Bind the repeater to the ground station (its own binding, separate
   from operational drones)
2. Assign VTX channel for the repeater if it has video (separate from
   operational drone channels)
3. Verify GPS lock on the repeater (strong lock needed for stable hold)
4. Plan relay endurance: how long can the repeater hold at altitude on
   its battery? Subtract 20% safety margin for wind.
5. Plan recall procedure: what happens when repeater battery hits
   minimum? All NLOS drones must be recalled BEFORE the repeater lands.

### Launch Sequence

1. Launch repeater first
2. Climb to planned altitude and enter GPS hold / position hold / loiter
3. Verify relay links are active (test control + video through relay)
4. Only then launch operational drones for NLOS mission
5. Monitor repeater battery continuously throughout operation

### Recovery Sequence

**Critical: reverse order.** Recovery must happen in this sequence:

1. Recall all NLOS operational drones to within direct LOS of ground
   station (or land them)
2. Verify all operational drones are safe (landed or within direct link)
3. Only then recall the repeater
4. Land the repeater

**If repeater battery is critical:** emergency recall all NLOS drones
immediately. Do not wait for them to complete their mission. A dead
repeater means instant loss of all NLOS links.

---

## Frequency Management

The repeater adds RF links to the frequency plan. Key rules:

### Repeater Control Link

The repeater needs its own control link from the ground station.
This consumes one RC channel/binding on the ground side.

- If using IRONghost: the repeater gets its own IRONghost binding
  on the same or different band as operational drones
- If using ELRS: separate binding phrase for the repeater
- If using a commercial relay (DJI Matrice, etc.): uses its own
  proprietary link

### Video Relay Channels

If the repeater receives video from operational drones and
retransmits to the ground:

- **Receive channel:** must match the operational drone's VTX channel
- **Transmit channel:** must be DIFFERENT from the receive channel
  (otherwise the repeater jams itself). Minimum 60 MHz separation
  between receive and transmit channels on the repeater.
- **Directional antenna on receive side** (pointed at operational area)
  and **omnidirectional on transmit side** (back to ground station) helps
  isolate the two channels.

### Avoid Self-Interference

The repeater is simultaneously receiving and transmitting. If the
transmit signal leaks into the receive path, the repeater will
create a feedback loop (howl/oscillation) or desense its own
receiver. Mitigation:

- **Maximum frequency separation** between RX and TX channels
- **Directional antennas** to isolate TX and RX paths
- **Physical separation** of TX and RX antennas on the repeater airframe
- **Power management:** use minimum necessary TX power on the repeater

---

## Failure Modes

| Failure | Effect | Response |
|---------|--------|----------|
| Repeater battery depleted | All NLOS links lost instantly | Emergency recall before this happens |
| Repeater GPS loss | Drifts from position, link geometry changes | Monitor, manual control if needed |
| Repeater link to GCS lost | Can't control repeater, but relay may continue | Failsafe behavior depends on config |
| Wind exceeds hold capability | Repeater blown off station | Reduce altitude or land |
| Repeater motor failure | Falls from altitude | All NLOS platforms enter failsafe |
| Self-interference on repeater | Relay quality degrades or drops | Increase TX/RX frequency separation |

**The fundamental risk:** repeater failure is a cascading failure.
Every platform relying on the repeater loses its link simultaneously.
This is why relay operations require disciplined battery management
and a standing recall plan.

---

## Endurance Planning

| Repeater Platform | Battery | Hover Endurance | Practical Relay Time |
|------------------|---------|-----------------|---------------------|
| 5" quad (minimal payload) | 6S 1500 mAh | 8-12 min | 6-9 min |
| 7" quad (relay-optimized) | 6S 3000 mAh | 18-25 min | 14-20 min |
| 10" quad (heavy lift) | 6S 6000 mAh | 25-35 min | 20-28 min |
| Kolibri 13 FR1 (purpose-built) | — | — | Designed for relay endurance |
| DJI Matrice 300 (commercial) | Dual battery | 45-55 min | 35-45 min |

**Practical relay time** = hover endurance minus 20% safety margin
minus climb/descent time.

For operations requiring longer relay time than a single battery
provides, plan battery swaps: land repeater, swap battery, relaunch.
All NLOS drones must be within direct LOS during the swap window.

---

## Sources

- TAF Industries, Kolibri 13 FR1 repeater specifications
- Orqa GCS-1 / IRONghost QS ground station documentation
- RF link budget fundamentals
- FPV community relay operation reports
- Multi-drone operational planning best practices
