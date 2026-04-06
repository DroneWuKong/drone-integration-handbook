# Attritable Drone Production Handbook

> Ukraine produces 8+ million FPV drones per year across 160+
> manufacturers. Individual units build and repair drones in field
> workshops. TAF Industries alone produces 80,000 per month. This isn't
> hobbyist building — it's industrial-scale manufacturing of attritable
> weapons systems using commercial components and decentralized production.
> The process knowledge is tribal. This guide documents it.

**Cross-references:** [Supply Chain Substitution](substitution-guide.md) ·
[Crash Recovery](crash-recovery.md) ·
[Frames](../components/frames-airframe-selection.md) ·
[Flight Controllers](../components/flight-controllers.md) ·
[ESCs](../components/escs.md) ·
[NDAA Compliance](../components/ndaa-compliance.md) ·
[CRSF & ELRS Protocol](../firmware/crsf-elrs-protocol.md)

---

## Design Principles

### Attritable = Designed to Be Lost

These drones are not designed to last thousands of flights. They're
designed to be built fast, fly once or a few times, and be replaceable
at scale. Every design decision flows from this principle:

- **Simplify assembly.** Fewer solder joints = faster build time and
  fewer failure points. JST-SH connectors where possible. Solder-free
  builds for training configurations.
- **Standardize components.** One FC, one ESC, one motor across the
  fleet. Interchangeable parts between platforms. See [Substitution
  Guide](substitution-guide.md) for drop-in alternatives when primary
  components go out of stock.
- **Minimize unique parts.** Frame arms should be replaceable individually.
  3D-printed mounts and adapters can be produced locally. Carbon plates
  can be cut from published DXF files (TBS Source One model).
- **Accept lower margins.** A drone that flies well enough for one mission
  doesn't need the same PID tuning as a racing quad. Good enough is
  the standard.

### The Production Unit

A typical production unit (Ukrainian model) consists of:

| Role | Count | Responsibility |
|------|-------|---------------|
| Build technicians | 3-8 | Assembly, soldering, wiring |
| Firmware technician | 1-2 | Flashing, configuration, binding |
| QC inspector | 1 | Pre-flight verification, test hover |
| Parts manager | 1 | Inventory, ordering, receiving |
| Repair tech | 1-2 | Post-crash repair, component salvage |

A team of 5-8 people can produce 10-30 drones per day depending on
complexity and component availability.

---

## Component Sourcing

### Primary Supply Chain

Most FPV components originate from Chinese manufacturers (Shenzhen
ecosystem): HappyModel, BETAFPV, GEPRC, iFlight, Foxeer, Caddx,
SpeedyBee, T-Motor, EMAX. These companies produce the majority of
the world's FPV hardware.

**Procurement channels:**

- **Direct from manufacturer** (Alibaba, manufacturer websites) —
  best pricing at volume, 2-6 week lead time, MOQ (minimum order
  quantity) requirements.
- **Distributors** (GetFPV, RaceDayQuads, Pyro Drone, RMRC) — faster
  delivery, no MOQ, higher per-unit cost. Good for filling gaps.
- **Local/regional suppliers** — emerging in Ukraine, EU, and US.
  Higher cost but shorter logistics chain and reduced supply disruption
  risk.

### Inventory Management

For production at scale, maintain buffer stock:

| Component | Buffer Stock | Reason |
|-----------|-------------|--------|
| Frames | 2 weeks production | Longest lead time from overseas |
| Motors | 2 weeks | High failure rate from crashes |
| ESCs | 1 week | Occasional DOA or crash burn |
| FCs | 1 week | Lowest failure rate |
| Receivers (ELRS) | 2 weeks | Most commonly stocked-out |
| Props | 1 month | Cheapest, highest consumption rate |
| Batteries | 1 week | Cycle life limits, cold weather attrition |
| Connectors (XT60, JST) | 1 month | Cheap, always needed |
| Wire, solder, heatshrink | 1 month | Consumables |

**The single biggest supply chain risk is receivers.** ELRS receivers
from HappyModel and BETAFPV go in and out of stock constantly. Always
maintain alternatives. See [Substitution Guide](substitution-guide.md).

---

## Assembly Line

### Station Layout

Organize the workspace into stations. Each station handles one step.
Drones flow through stations sequentially:

**Station 1: Frame Assembly**
- Assemble frame hardware (arms, plates, standoffs, screws)
- Install camera mount
- Install motor mounts if separate
- Output: bare frame ready for electronics

**Station 2: Motor Install**
- Mount motors to arms (4x M3 screws each)
- Route motor wires through arms
- Verify rotation direction markings (CW/CCW)
- Output: frame with motors

**Station 3: ESC + FC Stack**
- Install ESC on standoffs
- Connect motor wires to ESC (solder or JST)
- Install FC on standoffs above ESC
- Connect ESC signal cable to FC
- Output: frame with powered stack

**Station 4: Wiring**
- Solder/connect receiver to FC UART
- Route and mount receiver antenna
- Connect VTX to FC (video + SmartAudio/Tramp)
- Mount and connect camera
- Connect battery lead (XT60)
- Install GPS if equipped
- Output: fully wired drone

**Station 5: Firmware + Config**
- Flash FC firmware (Betaflight/iNav/ArduPilot target)
- Load standard CLI dump (pre-configured settings)
- Flash receiver firmware (ELRS version match)
- Bind receiver to TX
- Verify motor order and direction in configurator
- Set failsafe
- Output: configured drone

**Station 6: QC + Test**
- Visual inspection (solder joints, antenna routing, wiring)
- Continuity check (no shorts between power and signal)
- Motor spin test (correct direction, no grinding)
- Bench test (arm, throttle up on props, verify response)
- Test hover (30 seconds, verify stability)
- OSD verification (battery, LQ, GPS lock)
- Output: flight-ready drone

---

## Firmware Flashing at Scale

### The Problem

Flashing firmware one drone at a time through Betaflight Configurator
is acceptable for one build. For 20+ drones per day, it's a bottleneck.

### Solutions

**Pre-configured CLI dumps:** create a master CLI dump file containing
all settings for your standard build. After flashing the FC firmware
target, paste the CLI dump. This configures everything — UART
assignments, motor protocol, OSD layout, receiver protocol, failsafe,
rates, PIDs — in one operation.

```
# Save master config
dump all > standard_build_v3.txt

# Load onto new FC (after flashing correct firmware target)
# Paste contents of standard_build_v3.txt into CLI
# Type "save" to apply
```

**Version control your CLI dumps.** Keep them in a shared folder or
git repo. When you change a setting (PID update, new failsafe config),
update the master dump and note the version. Every drone built from
that point gets the new settings.

**ELRS batch flashing:** use the ExpressLRS Configurator or web flasher
to flash receivers in batches. Set the binding phrase in the build
options — every receiver built with the same phrase will bind to any
TX using that phrase. For fleet operations, use one binding phrase per
flight group and model match IDs to prevent cross-binding.

**Betaflight Configurator Presets:** Betaflight's preset system can
apply standard configurations. Create a custom preset file for your
build and load it on each new FC.

---

## Quality Control Checklist

Print this. Use it on every drone before it leaves the build station.

### Visual Inspection
- [ ] All solder joints are clean (shiny, concave, no cold joints)
- [ ] No wire pinch points under frame plates or standoffs
- [ ] Antenna exits frame cleanly (not pinched, not near carbon)
- [ ] Camera lens is clean and undamaged
- [ ] No loose standoffs or screws
- [ ] Battery strap is secure and positioned for CG
- [ ] XT60 connector is firmly attached (no cracked solder)
- [ ] GPS module is mounted on top, away from power wiring

### Electrical Test
- [ ] No shorts between battery positive and negative
- [ ] No shorts between battery and signal wiring
- [ ] Receiver LED indicates proper state (bound or binding)
- [ ] FC boots when battery connected (LED pattern normal)

### Motor Test
- [ ] All 4 motors spin freely by hand (no grinding or catching)
- [ ] Motor direction matches firmware config (verify in configurator)
- [ ] Props are correct rotation (CW/CCW per position)
- [ ] Props are tight on shafts (no wobble)
- [ ] Motor screws are correct length (too long = hits windings)

### Firmware Verification
- [ ] Correct firmware target flashed
- [ ] CLI dump loaded (verify serial RX config, motor protocol)
- [ ] Receiver bound (LQ showing on OSD)
- [ ] Failsafe configured and tested (disarm TX → drone responds correctly)
- [ ] OSD shows: battery voltage, LQ, GPS sats (if equipped)
- [ ] VTX on correct channel (check frequency plan)
- [ ] Motor order verified in configurator (match Betaflight motor diagram)
- [ ] Arm switch works (arms only when switch is in correct position)

### Hover Test
- [ ] Drone hovers stable at 1m for 10 seconds
- [ ] No oscillations, wobbles, or toilet-bowling
- [ ] OSD data matches expected values
- [ ] Motors are warm (not hot) after hover test
- [ ] No abnormal sounds (grinding, clicking, whistling)

---

## Batch Testing

For production runs of 10+ drones, batch testing saves time:

1. **Bench test all drones** at Station 6 before any hover tests
2. **Group hover tests** — fly 3-4 drones sequentially in the same
   area, same battery voltage, same conditions. Consistent behavior
   confirms consistent builds. An outlier indicates a build defect.
3. **Record serial numbers** — label each drone with a serial (masking
   tape + marker is fine). Track which components went into which drone.
   If a motor fails after 5 flights across 3 drones with the same motor
   batch, that's a supplier quality issue.

---

## Repair and Salvage

Crashed drones return to the repair station. The goal is to recover
every reusable component:

### Salvage Priority (most to least valuable)

1. **Flight controller** — highest value, most resilient to crashes.
   Even a cracked PCB may have a working MCU and gyro.
2. **ESC** — durable unless it took a direct short. Test before reuse.
3. **Receiver** — small and often survives intact. Verify binding.
4. **GPS module** — usually mounted on top, exposed to impact but
   often survives.
5. **Camera** — lens cracks are common. Replace lens if possible,
   otherwise salvage the sensor board.
6. **VTX** — check antenna connector integrity. If SMA/MMCX is
   intact, likely still functional.
7. **Motors** — spin test after crash. Bent shaft or grinding bearing =
   replace. Motors with undamaged stators can be rebuilt with new
   bearings and shafts (if your team has the skill).
8. **Battery** — inspect for damage. Cell check voltage. Mild puffing
   from impact may be acceptable for training but not for operational
   use. Punctured or heavily deformed = retire immediately.
9. **Frame** — individual broken arms can be replaced. If the center
   section is cracked, salvage hardware (standoffs, screws) and
   discard the carbon.

### Repair Workflow

1. Incoming crashed drone: tag with date and damage notes
2. Strip damaged components, sort into "reuse" and "scrap" bins
3. Reusable components go back to inventory
4. Rebuild with a fresh frame and any needed replacement parts
5. The rebuilt drone goes through the full QC checklist again

---

## Scaling Production

### From 10/day to 50/day

- **Parallelize stations.** Two Station 4 (wiring) positions since
  wiring is the slowest step.
- **Pre-cut and pre-strip wires.** Prepare wire bundles in advance
  (cut to length, stripped, tinned) so Station 4 just connects.
- **Jig/fixtures for soldering.** 3D-printed jigs hold FCs and ESCs
  at the right angle for consistent solder joints.
- **Dedicated firmware station.** One laptop with Betaflight
  Configurator + ELRS flasher + CLI dump templates running
  continuously.

### From 50/day to 200+/day

This requires factory-level organization:

- **Pick-and-place for connector pre-assembly** — pre-assemble wire
  harnesses with JST connectors crimped
- **Wave soldering or reflow** for high-volume PCB work
- **Automated test rigs** — connect each drone to a test jig that
  verifies motor response, receiver bind, and OSD output
- **Supply chain management software** — track component inventory,
  lead times, supplier quality metrics
- **Multiple parallel assembly lines** — each line staffed by a
  trained team

This is where Ukrainian manufacturers like TAF Industries (80,000/month)
and Wild Hornets operate. The transition from workshop to factory
requires capital, space, and trained personnel — but the process
knowledge is the same scaled up.

---

## Sources

- Ukrainian FPV production model documentation (public)
- TAF Industries, production capacity reporting
- Wild Hornets, build and repair operations
- Betaflight CLI dump documentation
- ExpressLRS batch flashing documentation
- NSDC Ukraine, defense industry capacity reporting (Jan 2026)
- UAS Nexus Syndicate, decentralized manufacturing model
