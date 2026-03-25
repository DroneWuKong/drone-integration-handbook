# MafiaLRS â Combat-Adapted ELRS Fork

> MafiaLRS is a Ukrainian fork of ExpressLRS adapted for contested RF
> environments. It operates outside standard ELRS frequency bands to
> evade electronic warfare coverage. Actively maintained and battle-tested in Ukraine.

---

## What MafiaLRS Is

MafiaLRS is a fork of ELRS maintained by the Ukrainian developer community (BUSHA/targets@mafia-targets).

**Status:** Actively maintained as of March 2026
**Targets:** 376 RX targets, 122 TX targets

---

## Key Differences from Stock ELRS

| Parameter | Stock ELRS | MafiaLRS |
|-----------|------------|----------|
| 900MHz band | 868/915MHz | 433-735MHz modified |
| 490-560MHz | Not supported | Supported |
| Frequency hopping | Standard ELRS pattern | Modified for EW evasion |
| Compatibility | Standard ELRS | Requires MafiaLRS on both ends |

The core modification is frequency hopping outside the bands that standard EW jamming systems cover.

---

## Operational Context

Developed in response to active RF jamming of standard drone control frequencies in Ukraine. Standard ELRS, Crossfire, and DJI links are vulnerable to broadband jamming. MafiaLRS operates in the gaps.

---

## Accessing MafiaLRS

Firmware generated via: **Forge -> RF Tools -> MafiaLRS Generator**

- 376 RX targets selectable
- 122 TX targets
- Manufacturer filtering

---

## Legal Notes

MafiaLRS operates on frequencies not licensed for unlicensed use in many jurisdictions. For US operators: not appropriate for routine commercial or recreational use. Defense and public safety contexts only.

---

## Related

- [ELRS Airport Mode](elrs-airport-mode.md)
- [RF Detection Hardware](rf-detection-hardware.md)
- [Forge MafiaLRS Generator](https://forgeprole.netlify.app/tools/)
