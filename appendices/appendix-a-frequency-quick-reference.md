# Appendix A — Frequency Quick Reference Card

*Print, laminate, and carry. One page for multi-drone frequency planning.*

---

## Band Summary

| Band | Frequency | Use | Notes |
|------|-----------|-----|-------|
| 433 MHz | 433–434 MHz | RC long-range, telemetry | EU only without license; ISM band |
| 868 MHz | 863–870 MHz | ELRS EU, CRSF EU | EU ISM; better penetration than 2.4 |
| 900 MHz | 902–928 MHz | ELRS US, LoRa RC | US ISM; best range/penetration |
| 1.2 GHz | 1.2–1.3 GHz | Analog video (legacy) | Avoid near GPS (L1=1575MHz) |
| 2.4 GHz | 2.400–2.483 GHz | ELRS 2.4, WiFi RC, RC standard | Crowded; shorter range |
| 4.9 GHz | 4.940–4.990 GHz | Public safety C2 | Licensed (Part 90); PS only |
| 5.8 GHz | 5.725–5.875 GHz | FPV video | ISM; 40 channels |
| 900 MHz | 916–928 MHz | MANET mesh (Doodle Labs) | Licensed version available |

---

## GPS / GNSS Reference

| System | L1 | L2 | L5 |
|--------|----|----|-----|
| GPS (US) | 1575.42 MHz | 1227.60 MHz | 1176.45 MHz |
| GLONASS (RU) | 1598–1606 MHz | 1242–1249 MHz | — |
| Galileo (EU) | 1575.42 MHz | 1207.14 MHz | 1176.45 MHz |
| BeiDou (CN) | 1561.10 MHz | 1207.14 MHz | 1176.45 MHz |

**Interference risk:** 1.2 GHz video transmitters overlap GPS L2.
Keep analog 1.2 GHz video away from L2 GPS modules.

---

## 5.8 GHz FPV Channel Map

```
Band A: A1(5865) A2(5845) A3(5825) A4(5805) A5(5785) A6(5765) A7(5745) A8(5725)
Band B: B1(5733) B2(5752) B3(5771) B4(5790) B5(5809) B6(5828) B7(5847) B8(5866)
Band E: E1(5705) E2(5685) E3(5665) E4(5645) E5(5885) E6(5905) E7(5925) E8(5945)
Band F: F1(5740) F2(5760) F3(5780) F4(5800) F5(5820) F6(5840) F7(5860) F8(5880)
Band R: R1(5658) R2(5695) R3(5732) R4(5769) R5(5806) R6(5843) R7(5880) R8(5917)
```

**Minimum channel separation for zero interference: 40 MHz**
(adjacent channel bleedover starts at <30 MHz separation)

### 4-Drone Deconfliction Template

```
Drone 1: F1 (5740 MHz)
Drone 2: F4 (5800 MHz)  — 60 MHz separation
Drone 3: F7 (5860 MHz)  — 60 MHz separation
Drone 4: A1 (5865 MHz)  — NOT usable with F7 simultaneously
         → Use E5 (5885 MHz) instead — 25 MHz from F7 (marginal)
         → Better: use 2.4 GHz analog for drone 4
```

**Practical limit: 3 simultaneous 5.8 GHz FPV video links** in one location
without careful planning. 4+ requires frequency coordination worksheet.

---

## RC Control Link Comparison

| System | Frequency | Range | Latency | NDAA |
|--------|-----------|-------|---------|------|
| ELRS 2.4 GHz | 2400–2483 MHz | 2–10 km typical | 4–8 ms | ✗ (Chinese) |
| ELRS 900 MHz | 868/915 MHz | 10–40 km | 10–20 ms | ✗ (Chinese) |
| TBS Crossfire | 868/915 MHz | 10–40 km | 5–12 ms | ✓ (Swiss) |
| TBS Tracer | 2.4 GHz | 2–8 km | 4–8 ms | ✓ (Swiss) |
| Orqa IRONghost | Dual-band FHSS | 5–15 km | 8–15 ms | ✓ (Croatian) |
| Herelink Blue | 2.4 GHz | 15 km | 20–30 ms | ✓ (Australian) |
| Silvus SC4200 | 2.4/5 GHz | 15 km | 10 ms | ✓ (US) |

---

## Mesh Radio Frequencies

| System | Frequency | Channel Width |
|--------|-----------|--------------|
| Doodle Labs RM-915 | 902–928 MHz | 5/10/20 MHz |
| Silvus StreamCaster | 2.4 or 4.9 GHz | 5/10/20 MHz |
| Rajant BreadCrumb | 900/2.4/5 GHz | 5/10/20 MHz |
| TrellisWare | 225–450 MHz (military) | Classified |
| MPU5 (Persistent) | 4.9 GHz | 5/10 MHz |

---

## Interference Risk Matrix

| Your system | Interferes with |
|-------------|----------------|
| 2.4 GHz RC | WiFi (ch 1–13), Bluetooth, 2.4 GHz video |
| 5.8 GHz video | 5 GHz WiFi (ch 149–165), other 5.8 GHz video |
| 900 MHz ELRS | ISM devices (door openers, wireless), MANET mesh |
| GPS L1 | 1575 MHz jammer, 1.5 GHz downlinks |
| 4.9 GHz mesh | Other 4.9 GHz users (coordinate with dispatch) |

---

## Quick Link Budget Rule of Thumb

```
Range (km) ≈ 10^((EIRP_dBm - Sensitivity_dBm - 20*log10(f_MHz) - 32.45) / 20)

Typical EIRP:     ELRS 900 = 27 dBm, Crossfire = 30 dBm
Typical sensitivity: ELRS = -130 dBm, Crossfire = -130 dBm
Free space at 915 MHz, 10 km: ~91.5 dB path loss
```

In practice: ELRS 900 at 100mW = 30–50 km in open terrain.
Real-world with obstacles: divide by 3–5.

---

## Related

- [Fundamentals — Frequency Bands](../fundamentals/frequency-bands.md)
- [Frequency Planning Worksheet](../field/frequency-planning.md)
- [Link Budgets](../fundamentals/link-budgets.md)
