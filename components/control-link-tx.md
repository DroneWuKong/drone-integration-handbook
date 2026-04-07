# Control Link TX Modules

> **Forge cross-reference:** 137 entries in `control_link_tx` category  
> **Related handbook chapters:** RC Receivers, CRSF & ELRS Protocol, Electronic Warfare

## The Transmitter Side of Your RC Link

The `control_link_tx` category covers the transmitter side of the RC control link — the radio modules, handsets, and ground-side hardware that sends stick commands from operator to drone. This is the other half of the ecosystem covered in `receivers.md`.

Most pilots use a full radio handset (RadioMaster Boxer, TX16S, Zorro) with an integrated or removable RF module. Understanding how to pick the right TX module — and how TX hardware affects link performance — is often overlooked.

## Handset vs. Module

Modern RC transmitters are designed around interchangeable RF modules. The handset provides the user interface (gimbals, switches, display, battery) while the module slot accepts different RF hardware.

**JR Module Bay (standard):** Full-size 36-pin bay on back of handset. Accepts ELRS, Crossfire, Tracer, FrSky ACCESS, and legacy modules. RadioMaster TX16S, Jumper T18, FrSky X20S all use this.

**Nano Module Bay:** Smaller format used on compact handsets (RadioMaster Zorro, BetaFPV LiteRadio 3 Pro, RadioMaster Pocket). Accepts ELRS Nano and Crossfire Nano TX modules. Physical size is significantly smaller.

**Internal RF:** Many modern handsets integrate ELRS or CRSF transmitter directly, eliminating the module entirely. RadioMaster Boxer, RadioMaster TX12 MKII, BetaFPV SuperG all have internal ELRS. Simplifies setup, reduces failure points.

## ExpressLRS TX Hardware

### RadioMaster Ranger Micro / Ranger
The reference ELRS TX module at each power tier. Ranger Micro (500mW, 2.4GHz) fits nano bay. Ranger (1W, 2.4GHz) fits JR bay. Both run ELRS firmware directly and are firmware-upgradeable over USB.

**Why RadioMaster dominates:** RadioMaster co-developed ELRS hardware reference designs and ships the most popular ELRS handsets. Their modules are widely used, well-documented, and firmware stays current.

**NDAA:** RadioMaster is Chinese (Shenzhen). Hardware manufactured in China. Non-compliant for federal procurement.

### ELRS Backpack
The ELRS Backpack concept allows a WiFi module to receive VTX control commands via ELRS telemetry, enabling VTX channel/power changes from the transmitter without a separate channel. Minor but useful for competition setup.

### BetaFPV ELRS Micro TX
Compact ELRS TX module. 100mW / 250mW / 1W variants. USB-C charging, hall-effect gimbals on some handsets. Non-NDAA (Chinese).

## Crossfire / Tracer TX Hardware

### TBS Tango 2
Team BlackSheep's dedicated long-range RC transmitter. Crossfire protocol, 1W output, folding design, 12-hour battery. The benchmark for long-range wing and fixed-wing BVLOS operations.

**NDAA ✓** — TBS is headquartered in Switzerland. The Tango 2 is the primary NDAA-compliant dedicated handset option for performance RC control.

### TBS Crossfire TX / TX Lite
The JR-bay and nano-bay Crossfire TX modules respectively. Pair with any JR-compatible handset. 1W output (TX), 250mW (TX Lite).

**NDAA ✓** — Swiss manufacture. The highest-performing NDAA-compliant TX module option.

### TBS Tracer TX
2.4GHz variant of Crossfire TX. Faster packet rates, slightly less range than Crossfire 900MHz. Nano bay form factor.

## FrSky TX Modules

FrSky (Chinese — NDAA ✗) produces the ACCESS-protocol TX modules used with FrSky receivers. R9M (900MHz, long range) and XJT (2.4GHz) are common in legacy setups. Not recommended for new builds — ELRS and Crossfire have surpassed FrSky on every performance metric while being cheaper.

## Spektrum (Horizon Hobby)

Spektrum DSM2/DSMX transmitters are the legacy standard for RC aircraft, helicopters, and some fixed-wing drones. Horizon Hobby is US-based (NDAA ✓). Performatively inferior to ELRS for FPV applications but maintains market share in the RC aircraft community.

Key Spektrum TX products relevant to drone integration:
- **NX8/NX10:** 8-10 channel transmitters for conventional RC aircraft
- **iX12/iX20:** High-channel-count radio for complex platforms (hexacopters, VTOL)

## Power Levels and Legal Considerations

TX module output power is regulated by frequency and jurisdiction:

| Band | US Legal Max | Common Module Max |
|---|---|---|
| 2.4GHz | 1W EIRP (30 dBm) | 1W |
| 900MHz | 4W EIRP | 1W (modules) / 2W (dedicated TX) |
| 5.8GHz | 200mW EIRP | Varies |

**Note:** ELRS modules operating at 1W in 915MHz band are technically legal under FCC Part 15 for most uses, but operators should verify their specific application. Contest and hobby use vs. commercial UAS operations may have different requirements.

**For contested/military environments:** Standard output powers are deliberately low — 100mW at 2.4GHz is trivially jammed. For operations where link resilience matters, use 900MHz at maximum legal power, add frequency hopping (ELRS does this), and consider encrypted binding (MILELRS).

## NDAA Summary

The control link TX category is almost entirely Chinese-manufactured at the consumer level. NDAA-compliant options:

| Product | Origin | NDAA |
|---|---|---|
| TBS Crossfire TX / TX Lite | Switzerland | ✓ |
| TBS Tracer TX | Switzerland | ✓ |
| TBS Tango 2 | Switzerland | ✓ |
| Spektrum NX/iX series | USA (Horizon Hobby) | ✓ |
| RadioMaster (all) | China | ✗ |
| BetaFPV (all) | China | ✗ |
| FrSky (all) | China | ✗ |
| Jumper (all) | China | ✗ |
| Happymodel ELRS | China | ✗ |

For federal procurement: TBS Crossfire ecosystem is the primary option combining NDAA compliance with competitive performance. Spektrum covers the legacy/fixed-wing procurement market.
