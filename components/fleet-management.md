# Fleet Management

> Managing 5–50 platforms is operationally different from managing 1.
> The problems are configuration drift, battery tracking, maintenance
> scheduling, and proving airworthiness at scale.

---

## The Core Problems

**Configuration drift** — after 6 months, no two aircraft in your fleet
have the same firmware version, PID tune, or peripheral set. One crashes.
You don't know if it was a unique config issue or a fleet-wide problem.

**Battery degradation** — LiPo capacity degrades ~20% after 100–150 cycles,
LiIon after 300–500. Without tracking cycle counts, you'll fly degraded
cells without knowing it.

**Maintenance gaps** — props crack, motors wear, frames fatigue. Without
a formal inspection cadence, damage goes unnoticed until failure.

**Regulatory exposure** — Part 108 (expected mid-2026) will require
maintenance records for BVLOS operations. ASTM F3600-22 defines the
standard. Agencies without records will face authorization delays.

---

## Airframe Identification

Assign every physical airframe a unique ID before it enters service.
Options:

| Method | Pros | Cons |
|--------|------|------|
| QR code label on frame | Easy scan, cheap | Can peel off |
| Engraved serial on arm | Permanent | Requires tooling |
| FC hardware ID (MCU serial) | Software-readable | Need USB connection |
| Tooth airframe ID (SHA-256) | Tamper-evident chain | Requires Wingman |

**Recommended:** QR label + Tooth provisioning. The QR gives physical
traceability, Tooth gives digital audit trail.

---

## Configuration Management

### Baseline Configuration

For each platform type in your fleet, define a **baseline config file**:
- Firmware version (exact hash)
- All PIDs (not just the tuned ones — all 10 axes)
- Filter settings
- Rate profile
- Peripheral assignments (UARTs, protocols)
- Failsafe settings

Store baseline configs in git. Tag each version. When you tune one aircraft,
update the baseline and push to the fleet on the next maintenance cycle.

### Detecting Drift

Connect to each aircraft quarterly (or after any crash/repair) and diff
current params against baseline. Wingman Hangar's `diff` command does this:

```bash
hangar diff --baseline fleet/apex-5inch-v3.params --port /dev/ttyACM0
```

Any unexplained diff is a maintenance event.

### Firmware Version Control

Never run mixed firmware versions in a fleet for more than one maintenance
cycle. Mixed versions create inconsistent behavior that's difficult to
diagnose. Maintain a fleet firmware matrix:

| Aircraft | Firmware | Version | Last Updated | Next Update |
|----------|----------|---------|--------------|-------------|
| APEX-01  | Betaflight | 4.5.1 | 2026-03-15 | 2026-06-15 |
| APEX-02  | Betaflight | 4.5.1 | 2026-03-15 | 2026-06-15 |

---

## Battery Management

### Tracking Cycle Counts

Every charge/discharge cycle = 1 cycle count. Track in a spreadsheet or
battery management app. Retire cells when:
- LiPo: 100–150 cycles or capacity < 80% of rated
- LiIon: 300–500 cycles or capacity < 80% of rated
- LiPo if puffed: immediately, regardless of cycle count

### Battery Labeling

Label every battery pack with:
- Pack ID (e.g., B-047)
- Purchase date
- Chemistry and cell count
- Current cycle count (update after each flight)

### Storage Voltage

Never store at full charge or fully depleted.
- LiPo: 3.8V/cell storage voltage
- LiIon: 3.6–3.7V/cell

Most chargers have a storage mode. Use it.

### Fleet Battery Rotation

Rotate batteries across airframes so no single battery is used exclusively
with one airframe. This equalizes wear and catches degraded packs before
they cause an in-flight failure.

---

## Maintenance Scheduling

### Inspection Intervals

| Item | Interval | Check |
|------|----------|-------|
| Props | Every flight | Cracks, chips, balance |
| Motor screws | Every 5 flights | Torque check, vibration |
| Frame arms | Every 10 flights | Cracks, delamination |
| Motor bearings | Every 50 flights | Smooth rotation, no noise |
| FC/ESC solder joints | Every 25 flights | Cold joints, lifted pads |
| Battery connectors | Every 25 flights | Oxidation, fit |
| Antenna cables | Every 25 flights | Breaks near connectors |
| Full teardown | Every 100 flights | Replace motors, props, bearings |

### Maintenance Logging

For each aircraft, log:
- Date and flight count
- What was inspected
- What was replaced (part number, supplier)
- Who performed the work
- Next scheduled maintenance

This is the record that Part 108 will require. Start now.

---

## Firmware Flashing at Scale

### Batch Flashing Workflow

For fleets >5 aircraft, manual Betaflight Configurator flashing is too slow.
Use the Betaflight CLI or a scripted approach:

```bash
# Flash firmware via DFU (requires physical button press or FC shortcut)
dfu-util -d 0483:df11 -a 0 -s 0x08000000:force:leave -D betaflight_4.5.1_STM32H743.hex

# Apply params from baseline file
betaflight-configurator --port /dev/ttyACM0 --apply-params fleet/apex-5inch-v3.params
```

### Param Distribution

Maintain param files in git. When a tuning change is validated on one
aircraft, diff against baseline, review, merge, and distribute:

```bash
git diff baseline.params updated.params
# Review changes
git commit -m "fleet: increase roll P from 48 to 52, validated APEX-01"
# Push to all aircraft on next maintenance day
```

---

## Software Tools

| Tool | Platform | Best For |
|------|----------|----------|
| Betaflight Configurator | Desktop | Manual single-aircraft config |
| Wingman Hangar | Desktop | Fleet param management, Tooth audit |
| Kittyhawk | Web/Mobile | Commercial fleet ops, maintenance logs |
| FlightLogger | Web | Pilot logbooks, maintenance, battery tracking |
| DroneDeploy | Web | Commercial mission planning + fleet |
| UAV Toolbox (MATLAB) | Desktop | Simulation and analysis |

---

## ASTM F3600-22 Alignment

ASTM F3600-22 defines maintenance technician qualification for UAS.
For BVLOS authorization under Part 108, expect to demonstrate:

1. **Maintenance records** — per-aircraft log of all work performed
2. **Configuration records** — version-controlled param history
3. **Battery records** — cycle counts, capacity tests
4. **Technician qualification** — training records for personnel

The Tooth audit trail (tamper-evident SHA-256 event chain) is designed
specifically to satisfy the configuration record requirement.

---

## Related

- [Crash Recovery & Field Repair](../field/crash-recovery.md)
- [BVLOS Pathways](bvlos-pathways.md)
- [Tooth SQLite Documentation](../../../Ai-Project/docs/specs/tooth-architecture.md)
- [Wingman Hangar](../../../Ai-Project/hangar/)
