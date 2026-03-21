# Power Architecture & EMI

Most "random" failures on custom builds — video noise at high throttle, FC reboots on fast descents, RSSI drop near the motor arms, GPS losing lock on takeoff — are power problems. The root causes are almost always the same: the power rail isn't clean, grounds aren't shared correctly, or high-frequency switching noise is coupling into sensitive electronics. This guide explains the full power path and the practical fixes for each failure mode.

---

## The Power Path

```
Battery → Main leads → ESC power input → Motor phases
                    ↓
              Capacitor (parallel)
                    ↓
              BEC / Power module → FC + peripherals
                    ↓
              FC regulated 5V → Receiver, GPS, cameras
```

Every component in this chain is a noise source or noise victim. Understanding the direction current flows — and what happens at each transition — determines where problems originate.

---

## The Battery and Main Leads

### Lead Length and Inductance

Battery leads are inductors. Long leads store energy in their magnetic field; when current changes rapidly (like when a motor commutates), the inductor resists the change and generates a voltage spike. A 150mm pair of 12AWG leads on a 4S build can produce voltage spikes of 3–5V above the rail voltage during aggressive motor braking.

**Keep main leads as short as physically possible.** The target is under 100mm from connector to ESC power pads. On builds where the battery tray is remote from the ESC stack, use a low-impedance power distribution board rather than long leads.

### Connector Choice

| Connector | Continuous | Burst | Best For |
|---|---|---|---|
| JST-PH | 2A | 3A | 1S micro builds |
| JST-XH | 5A | 8A | Balance connectors only |
| XT30 | 30A | 60A | 3" builds, sub-4S |
| XT60 | 60A | 100A | Standard 5"–7" builds |
| XT90 | 90A | 150A | Heavy-lift, 10"+ |
| AS150 | 150A | 300A | Very high current |

Use the right connector for the current. An XT60 on a 12S heavy-lift build that pulls 200A peak will run hot and eventually fail. An XT90 on a 5" freestyle build adds 10g of unnecessary weight.

---

## The Capacitor: The Most Ignored Component

The bulk capacitor across the ESC power input is the single most effective noise reduction measure on a custom build. Most builders omit it. Almost every builder who adds one later says "I wish I'd done that from the start."

### What It Does

BLDC motors are switched loads. At the moment of commutation, the current draw changes sharply — the inductance of the motor winding releases stored energy back into the power rail as a brief voltage spike. Without a capacitor, this spike travels up the power leads to the battery and to every other component on the rail. With a capacitor, the spike is absorbed locally and dissipated.

The capacitor also acts as a local energy reservoir, keeping voltage stable during rapid throttle changes. When all four motors suddenly increase thrust simultaneously (a quick pitch-up), the current demand spikes before the battery leads can respond. The capacitor fills that gap.

### Selecting the Capacitor

Low-ESR (Equivalent Series Resistance) electrolytic capacitors are the correct type. Ceramic capacitors have too low capacitance; standard electrolytics have too high ESR to absorb fast spikes.

**Minimum specifications:**
- Voltage rating: at minimum 1.5× your fully-charged battery voltage
- 4S (16.8V): use 35V or higher
- 6S (25.2V): use 35V or 50V
- 12S (50.4V): use 63V or higher

**Capacitance:** 470µF–1000µF for 4S–6S builds. Higher capacitance is better up to a point; above ~2200µF there's diminishing return and significant weight addition.

**Placement:** As close to the ESC power pads as physically possible. The leads between the capacitor and the ESC are part of the inductive loop — every millimeter counts. On a 4-in-1 stack, solder directly to the battery pads on the ESC board if layout permits.

**Popular parts:**
- Panasonic FR series 35V 1000µF — low ESR, compact
- Nichicon HE series 35V 470µF — very low ESR, common in FPV
- Nichicon UHE series 50V 680µF — good for 6S builds

---

## BEC vs OPTO: Powering the FC

### The BEC Problem

An ESC with a Battery Eliminator Circuit (BEC) steps down battery voltage to 5V to power the FC and receiver. Convenient, but the BEC shares a power and ground plane with the motor drive stage. Switching noise from the motor commutation can couple directly through the shared ground into the FC's microcontroller and ADC inputs.

On low-power 1S–3S builds with modest motor noise, this is rarely a problem. On 6S+ builds with large motors, it can cause:
- Gyroscope noise visible in Blackbox as high-frequency spikes
- Compass interference (magnetometer picks up switching fields)
- RSSI jitter on receivers sharing the 5V bus
- Video noise coupling through shared 5V to the VTX

**The fix:** Use a separate, isolated 5V power source for the FC. Options:
1. A dedicated linear regulator or low-noise DC-DC converter on the FC board's own input (most modern FC boards have this — check the schematic)
2. A separate BEC (dedicated 5V regulator) powered directly from the battery, isolated from the ESC
3. OPTO ESC (no BEC at all) + separate FC power input

Most FC boards sold in 2024+ have their own 5V regulator on a separate input. Use it.

### FC Power Input Best Practice

```
Battery (4S–6S) → ESC (motor drive only, no BEC used)
Battery (4S–6S) → Separate 5V BEC → FC 5V input
FC 5V output → Receiver, GPS, cameras
```

On stacked FC/ESC builds, check whether the FC's 5V pin is powered from the ESC BEC or from its own regulator. Many "stacks" run everything off the ESC BEC to simplify wiring — this is convenient but electrically noisy.

---

## Ground: The Most Misunderstood Conductor

### What Ground Actually Is

"Ground" is not a zero-voltage reference point — it's a return current path. Current flows in loops. Every milliamp that flows from the battery through a motor flows back to the battery through the ground conductor. On a poorly designed build, all return current shares the same ground wire, and different currents interfere with each other.

The key principle: **keep high-current return paths physically separate from low-current signal return paths.**

### The Ground Loop Problem

A ground loop occurs when a circuit has multiple ground return paths, creating a loop of wire with varying potentials at different points. The symptom is usually video interference — a rolling bar in the FPV feed that gets worse with motor speed.

**Classic ground loop:** VTX and camera share the same ground wire as the ESC. Motor switching current flows through this shared ground, inducing a voltage across the impedance of the wire, which appears as noise in the video signal.

**Fix:** Separate the video ground from the power ground. Use a capacitor or ferrite bead in series with the video ground return. Many FPV cameras include this; many do not.

### Common Ground Rule

The FC must share a common ground with every component it communicates with. UART RX/TX, PWM outputs, analog inputs — all require a shared ground between the FC and the peripheral. Floating grounds cause erratic behavior: random telemetry values, ESC calibration failures, GPS lock issues.

**On every UART connection:**
```
FC TX → Peripheral RX
FC RX → Peripheral TX
FC GND → Peripheral GND  ← this wire is as important as the data wires
```

The ground wire on a UART connection can be the same wire as the 5V supply ground if the peripheral is powered from the FC's 5V rail. If the peripheral is independently powered (e.g., a VTX running off battery directly), a separate ground wire from the FC to the peripheral is required.

---

## EMI: High-Frequency Noise Sources and Victims

### Sources of EMI on a UAS

| Source | Frequency Range | Victims |
|---|---|---|
| ESC motor commutation | 10kHz–500kHz | FC gyro, magnetometer, video |
| Motor magnets (mechanical) | RPM-dependent | FC gyro (via vibration) |
| 2.4GHz receiver | 2.4GHz | GPS L1 (1.575GHz — adjacent) |
| 5.8GHz VTX | 5.8GHz | Remote ID (5.8GHz WiFi), FPV |
| Remote ID (WiFi/BT) | 2.4GHz, 5.8GHz | RC links |
| GPS (L1) | 1.575GHz | Nearby 1.8GHz links |

### Separation and Shielding

The practical rule: **distance is the cheapest shielding.** Double the separation and you cut radiated interference by 6–12dB depending on geometry.

**GPS placement:** As far from the VTX as the frame allows. The VTX is the strongest intentional emitter on the build; GPS is one of the most sensitive receivers. Minimum 10cm separation. Never stack GPS directly above a VTX.

**Magnetometer:** Move it as far as possible from motor wires and power leads. Motor current creates a magnetic field proportional to current flow. A magnetometer (compass) directly above a high-current ESC will read garbage at full throttle. 5–10cm separation from any high-current conductor is the minimum.

**RC receiver:** Antennas should be oriented so they're not parallel to motor wires. Perpendicular routing reduces coupling. Avoid routing receiver antenna wires along power leads.

### Ferrite Beads

A ferrite bead is a passive component that attenuates high-frequency noise on a wire by increasing its impedance at radio frequencies while leaving DC and low-frequency signals unaffected.

Where to use them:
- In series on the 5V power line to the VTX (attenuates switching noise from BEC)
- In series on the video signal line between camera and VTX
- On the GPS power line if GPS noise is suspected
- In series on UART power lines for noisy peripherals

Ferrite beads are passive noise mitigation — they address symptoms, not root causes. Fix the root cause first (capacitor, ground separation, physical layout), then add ferrite beads for any remaining residual noise.

---

## Specific Failure Modes

### "Video noise at high throttle"

**Cause:** Motor switching noise coupling into the video chain via shared power or shared ground.

**Fix sequence:**
1. Add/upgrade capacitor on ESC power pads
2. Power VTX from a separate filtered 5V source (not direct battery or ESC BEC)
3. Add ferrite bead in series on VTX power wire
4. Add ferrite bead on video signal wire
5. Check for ground loops — is the camera ground connected to FC ground connected to ESC ground? If so, try breaking one path

### "FC reboots on fast descent / motor braking"

**Cause:** Regenerative braking. When motors decelerate rapidly (fast descent, motor_stop in Betaflight), they briefly act as generators, pushing current back into the power rail. Without a large capacitor to absorb this, voltage spikes above the FC's operating limit.

**Fix:**
1. Add a larger capacitor (1000–2200µF) close to the ESC power input
2. Enable bidirectional DShot and disable motor_stop (use digital idle instead)
3. Verify the FC's input voltage range — some FCs have poor voltage spike tolerance

### "GPS drops lock on throttle up"

**Cause:** RF interference from ESC switching reaching the GPS receiver's front end.

**Fix sequence:**
1. Physically move GPS further from ESC stack
2. Move GPS antenna clear of motor wires (route away from arms)
3. Ensure GPS module has its own filtered 5V supply
4. Add ferrite bead on GPS power wire
5. If using a combined GPS/compass module, check compass for interference (see magnetometer section above)

### "RSSI drops when VTX is active"

**Cause:** 5.8GHz VTX output reaching the 2.4GHz RC receiver's RF front end (harmonic mixing), or physical proximity causing desensitization.

**Fix:**
1. Move VTX antenna away from receiver antennas — minimum 5cm, perpendicular if possible
2. If using a 5.8GHz VTX near an ExpressLRS 2.4GHz receiver, verify no receiver de-sense (the LNA in the receiver can be driven into compression by a nearby strong transmitter at a nearby frequency)
3. Consider using a different VTX frequency band if the problem persists

### "Gyro noise / oscillations with no obvious cause"

**Cause:** Electrical noise from ESC coupling into the gyroscope via the power rail or PCB traces.

**Fix:**
1. Add capacitor to ESC power input
2. Use soft-mounting for the FC stack (rubber standoffs) — vibration and electrical noise often appear together
3. Enable RPM filtering (requires bidirectional DShot) — this directly removes motor-frequency noise from the gyro signal
4. Check ESC firmware version — older BLHeli_32 / AM32 versions have known noise issues; update

---

## Power Budget: Know Your Numbers

Before a build is complete, calculate the total power draw to verify the battery and BEC can handle every component simultaneously.

| Component | Typical Draw |
|---|---|
| Flight controller | 200–500mA at 5V |
| GPS module | 50–150mA at 5V |
| RC receiver (ELRS) | 100–200mA at 5V |
| FPV camera | 100–200mA at 5V |
| VTX (5.8GHz, 500mW) | 1–2A at 5V |
| LED strip (per meter) | 300–1000mA at 5V |
| Companion computer (Pi Zero) | 200–500mA at 5V |

A 5" freestyle quad with FC + GPS + ELRS + camera + VTX draws roughly 2.5–4A at 5V continuously. A 1A BEC will thermal-shutdown. Use a 3A minimum BEC; 5A for builds with companion computers or many LEDs.

**Tracking total wattage:** Multiply 5V draw by 5, then divide by battery efficiency (~85%) to get the battery watts consumed by electronics alone. On a 4S (14.8V) build drawing 3A at 5V, that's 15W from electronics, ~18W from the battery — a non-trivial portion of total power on a lighter build.
