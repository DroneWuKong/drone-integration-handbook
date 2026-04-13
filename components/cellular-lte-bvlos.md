# Cellular / LTE for BVLOS Operations

> Cellular modems let you fly beyond visual line of sight without a
> dedicated RF link — using existing carrier infrastructure. The tradeoff
> is latency, reliability, and regulatory complexity.

---

## When to Use Cellular vs Dedicated RF

| Scenario | Cellular | Dedicated RF |
|----------|----------|--------------|
| Urban/suburban BVLOS | ✓ Good coverage | ✗ Path loss |
| Rural/remote | ✗ Coverage gaps | ✓ Reliable |
| Latency-sensitive (FPV) | ✗ 40–120ms | ✓ <10ms |
| Long range (>10km) | ✓ If covered | Depends on hardware |
| Redundancy (backup link) | ✓ Excellent | — |
| Infrastructure-independent | ✗ Carrier dependent | ✓ |
| BVLOS regulatory path | ✓ FAA prefers | Requires BVLOS waiver |

**Bottom line:** Cellular is best for planned routes in covered areas with
moderate latency tolerance. Use dedicated RF (Silvus, Doodle Labs) for
tactical or latency-sensitive ops. Use both for redundancy.

---

## Hardware Options

### Modems

| Modem | LTE Cat | Notes | NDAA |
|-------|---------|-------|------|
| Sixfab Raspberry Pi Hat | Cat 4/M1 | RPi integration, broad carrier support | ✓ |
| Holybro LTE Telemetry | Cat 4 | Plug-and-play with Pixhawk, MAVLink native | ✓ |
| Digi XBee LTE | Cat M1/NB1 | Industrial grade, wide temp range | ✓ |
| Skydio LTE Module | Integrated | Skydio X10 only, AES-256 encrypted | ✓ |
| Sierra Wireless RV50 | Cat 6 | Enterprise, multi-carrier failover | ✓ |
| TILT Autonomy Starlink PoE | Starlink | Blue UAS Framework cleared, LEO satellite | ✓ |

### Integration Approaches

**MAVLink over LTE (most common):**
```
FC → UART → LTE modem → cellular network → GCS
```
Use MAVLink-router or MAVSDK to forward MAVLink streams over TCP/UDP.

**Companion computer as bridge:**
```
FC → UART/USB → RPi → LTE modem → cloud → GCS
```
More flexible, supports encryption, logging, and AI inference onboard.

---

## Latency Reality

Cellular latency is non-deterministic. Typical values:

| Condition | RTT |
|-----------|-----|
| LTE urban, good signal | 40–80ms |
| LTE rural, marginal signal | 80–200ms |
| LTE congested network | 100–500ms+ |
| 5G sub-6GHz | 20–50ms |
| Starlink LEO | 20–60ms |

**40–120ms is acceptable for telemetry and waypoint navigation.**
It is **not acceptable for manual FPV control** — use dedicated RF for
any hands-on piloting.

**Jitter matters more than average latency.** A 100ms average with
50ms jitter is worse than a 60ms average with 5ms jitter for telemetry
stability. Look for networks with consistent performance.

---

## Carrier Selection

**Redundancy:** Multi-carrier SIMs (Eseye, Telnyx, Twilio Super SIM)
auto-failover between carriers. Essential for any operational deployment.

**Coverage mapping:** Use carrier coverage maps + field testing. Indoor
coverage maps are useless for airborne UAS — you're above buildings,
so signal is usually better than ground level.

**Band selection:** Bands 12, 13, 14 (700MHz) penetrate obstacles and
have wider rural coverage. Bands 4, 2, 66 (1700–2100MHz) have more
urban capacity but shorter range.

**FirstNet (AT&T):** Priority network access for public safety agencies.
DFR operators using FirstNet get pre-emption over commercial traffic
during emergencies. Significant advantage for reliability.

---

## Regulatory Considerations

### FAA BVLOS Authorization

Cellular links are accepted as a C2 (command and control) link for
BVLOS operations. FAA requires:

1. **Demonstrated reliability** — link performance data showing >99.9%
   uptime in the proposed operating area
2. **Lost link procedures** — documented RTL/land behavior on link loss
3. **Remote ID compliance** — standard or broadcast RID still required
4. **LAANC or waiver** — cellular doesn't eliminate airspace authorization

### Part 135 / BVLOS Waiver

For the FAA's Beyond Authorization process (post-2025 streamlined process):
- Submit link budget analysis for cellular
- Include coverage maps for operating area
- Document carrier redundancy
- Show lost link timeline: [link loss] → [CC override] → [RTL] → [land]

---

## Implementation Notes

### Lost Link Behavior

Configure this **before your first BVLOS flight:**

```
ArduCopter:
FS_LONG_ACTION = 2 (RTL on long failsafe)
FS_LONG_TIMEOUT = 20  (seconds before long failsafe)
FS_SHORT_ACTION = 0 (continue on short failsafe)
FS_SHORT_TIMEOUT = 3

PX4:
COM_DL_LOSS_T = 10  (data link loss timeout, seconds)
NAV_DLL_ACT = 2 (RTL on data link loss)
```

### Encryption

Raw MAVLink over the internet is unencrypted. For any operational use:
- Wrap in WireGuard or OpenVPN tunnel
- Or use MAVLink 2 signing (per-packet HMAC)
- Holybro LTE module handles this transparently

### Bandwidth Requirements

MAVLink telemetry at 4Hz: ~1–3 kbps
MAVLink telemetry at 10Hz: ~3–8 kbps
Video stream (720p): 1–4 Mbps
Video stream (1080p): 4–10 Mbps

Cellular handles all of these comfortably. Budget for video if you need
live feed. Telemetry-only C2 is trivial bandwidth.

---

## Relevant Platforms

- **Skydio X10** — integrated LTE module, AES-256, FirstNet-capable
- **American Robotics Scout** — LTE-native, Part 135 certified
- **Teal 2** — LTE option via payload bay
- **Holybro Pixhawk series** — LTE telemetry module available

---

## Related

- [BVLOS Pathways](bvlos-pathways.md)
- [C2 Datalinks](c2-datalinks.md)
- [Mesh Radios](mesh-radios.md)
