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

Country of headquarters or assembly does not establish eligibility. Check the exact item, revision, bill of materials, applicable contracting authority and dated supporting documentation using [federal procurement screening](ndaa-compliance.md). This reference does not certify the listed products.

### ELRS Backpack
The ELRS Backpack concept allows a WiFi module to receive VTX control commands via ELRS telemetry, enabling VTX channel/power changes from the transmitter without a separate channel. Minor but useful for competition setup.

### BetaFPV ELRS Micro TX
Compact ELRS TX module. 100mW / 250mW / 1W variants. USB-C charging, hall-effect gimbals on some handsets. Procurement status requires exact-item screening.

## Crossfire / Tracer TX Hardware

### TBS Tango 2
Team BlackSheep's dedicated long-range RC transmitter. Crossfire protocol, 1W output, folding design, 12-hour battery. The benchmark for long-range wing and fixed-wing BVLOS operations.

Procurement status is configuration- and authority-specific; headquarters does not establish it.

### TBS Crossfire TX / TX Lite
The JR-bay and nano-bay Crossfire TX modules respectively. Pair with any JR-compatible handset. 1W output (TX), 250mW (TX Lite).

Procurement status is configuration- and authority-specific; headquarters does not establish it.

### TBS Tracer TX
2.4GHz variant of Crossfire TX. Faster packet rates, slightly less range than Crossfire 900MHz. Nano bay form factor.

## FrSky TX Modules

FrSky (Chinese — procurement status unverified) produces the ACCESS-protocol TX modules used with FrSky receivers. R9M (900MHz, long range) and XJT (2.4GHz) are common in legacy setups. Not recommended for new builds — ELRS and Crossfire have surpassed FrSky on every performance metric while being cheaper.

## Spektrum (Horizon Hobby)

Spektrum DSM2/DSMX transmitters are the legacy standard for RC aircraft, helicopters, and some fixed-wing drones. Horizon Hobby is US-based (procurement status unverified). Performatively inferior to ELRS for FPV applications but maintains market share in the RC aircraft community.

Key Spektrum TX products relevant to drone integration:
- **NX8/NX10:** 8-10 channel transmitters for conventional RC aircraft
- **iX12/iX20:** High-channel-count radio for complex platforms (hexacopters, VTOL)

## Power Levels and Legal Considerations

Record the exact equipment authorization, operating mode, band, antenna and EIRP limit for the applicable jurisdiction. A band-wide power table cannot establish permission for a particular transmitter. See [regulatory resources](../appendices/appendix-f-regulatory-resources.md).

## NDAA Summary

Country of headquarters or assembly does not establish eligibility. Check the exact item, revision, bill of materials, applicable contracting authority and dated supporting documentation using [federal procurement screening](ndaa-compliance.md). This reference does not certify the listed products.
