# RF Detection Hardware — Field-Deployable Drone Detection

> You don't need a $40,000 RF sensor suite to detect consumer drones.
> A $31 module and open firmware will identify most commercial UAS
> on the market.

---

## The Detection Problem

Commercial drones transmit on predictable frequencies using identifiable
RF signatures: specific modulation schemes, hop patterns, beacon intervals,
and frequency bands. A receiver that can scan these bands and match known
signatures can identify drone activity at useful ranges.

---

## Hardware Tiers

### Tier 1 — $31 — LILYGO T-Embed CC1101

The best single-purchase option for getting started. The T-Embed integrates
an ESP32-S3 with a CC1101 sub-GHz radio and a small display.

**Coverage:** 315MHz, 433MHz, 868MHz, 915MHz
**Detects:** ELRS 900MHz, TBS Crossfire, Microhard pDDL 900, DJI OcuSync sub-GHz variants, FPV analog control links

**Limitations:** No 2.4GHz or 5.8GHz coverage. Misses DJI OcuSync 2.4/5.8, ELRS 2.4GHz, analog FPV video.

**SPI pin definitions for T-Embed CC1101:**
```
SCK:  GPIO18
MISO: GPIO19
MOSI: GPIO23
CS:   GPIO5
GDO0: GPIO4
GDO2: GPIO2
```

Note: These differ from generic CC1101 breakout wiring. Use T-Embed specific definitions or detection will fail silently.

### Tier 2 — ~$10 — XIAO ESP32S3 + Wio-SX1262

Compact, field-portable, LoRa-focused coverage.

**Coverage:** 868MHz, 915MHz (LoRa bands)
**Detects:** ELRS 900MHz LoRa chirp signatures, TBS Crossfire FHSS

Best for ELRS-heavy environments where the primary concern is detecting long-range FPV or autonomous vehicles using 900MHz links.

### Tier 3 — ~$41 — Dual Radio (T-Embed + Wio-SX1262)

Combined coverage across sub-GHz bands. Run CC1101 for FHSS/FSK detection alongside SX1262 for LoRa chirp detection. Recommended field kit for comprehensive sub-GHz coverage.

---

## Known RF Signatures (57 total in current firmware)

### DJI Systems
| System | Frequency | Modulation | Key Identifier |
|--------|-----------|------------|----------------|
| OcuSync 2.4GHz | 2.400-2.483GHz | FHSS burst | 72 channels, ~10ms beacon interval |
| OcuSync 5.8GHz | 5.725-5.850GHz | FHSS burst | Fallback from 2.4GHz |
| O3/O4 Digital | 5.8GHz | OFDM | 10km claim, high bandwidth |
| DJI FPV | 5.8GHz | OFDM | Dedicated FPV variant |

### ELRS
| System | Frequency | Modulation | Key Identifier |
|--------|-----------|------------|----------------|
| ELRS 900MHz | 868/915MHz | LoRa SF6-10, BW500kHz | Low-latency chirp |
| ELRS 2.4GHz | 2.4GHz | LoRa/FLRC | Gemini dual-antenna |
| ELRS Airport | 2.4GHz | Transparent serial | 115200 baud bridge mode |

### Military/Defense Adjacent
| System | Frequency | Modulation | Key Identifier |
|--------|-----------|------------|----------------|
| Microhard pDDL 900 | 902-928MHz | FHSS/DSSS | AES-256, Blue UAS approved |
| Herelink | 2.4GHz | OFDM | CubePilot, combined video+RC |
| MafiaLRS | 433-735MHz | Modified LoRa | Non-standard EW-evasion bands |
| Skydio | 2.4/5.8GHz + LTE | Mixed | Autonomous, dual comms |

### Common FPV
| System | Frequency | Modulation | Key Identifier |
|--------|-----------|------------|----------------|
| TBS Crossfire | 868/915MHz | FHSS | <10ms latency, 150km range claim |
| Analog FPV 5.8GHz | 5.645-5.945GHz | FM analog | Raceband R1-R8, A/B/E/F/R bands |
| Orqa FPV.Connect | 2.4/5.8GHz | Digital | Low-latency goggle ecosystem |

---

## Critical Firmware Bug — strcmp False Matches

A known issue in early versions of ESP32 RF detector firmware caused false positive matches due to incorrect use of strcmp for pattern matching on binary data. The bug: strcmp stops at null bytes, causing truncated comparisons that match multiple different signatures.

**Fix:** Replace strcmp with memcmp and pass explicit length parameters.

```c
// Wrong — stops at null byte
if (strcmp(received_data, signature) == 0) { ... }

// Correct — compares full signature including null bytes
if (memcmp(received_data, signature, SIGNATURE_LEN) == 0) { ... }
```

Always use memcmp for RF signature matching.

---

## Detection Range

| Signal Type | Tier 1 Range | Notes |
|-------------|-------------|-------|
| ELRS 900MHz | 200-800m | Depends on output power and antenna |
| Crossfire | 300-1000m | Higher power than ELRS |
| Microhard pDDL | 100-400m | Encrypted, harder to characterize |
| DJI OcuSync (sub-GHz) | 150-500m | Limited by CC1101 sensitivity |

---

## Related

- [RF Fundamentals](../fundamentals/five-link-types.md)
- [Frequency Bands](../fundamentals/frequency-bands.md)
- [Counter-UAS Integration](../components/counter-uas.md)
- [MafiaLRS](mafiairs-combat-elrs.md)
