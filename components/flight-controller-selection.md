# Flight Controller Selection Framework

The Forge database has 300+ flight controllers. This guide isn't a spec comparison — it's the decision framework for narrowing that list to the three you should actually evaluate for your application.

---

## Start with Firmware, Not Hardware

The single most important question is: **which firmware do you need?**

Your FC choice is constrained by firmware first and hardware second. A great H7 processor running the wrong firmware for your use case is worse than a modest F4 running the right one.

| Firmware | Best For | Avoid When |
|---|---|---|
| **Betaflight** | FPV freestyle, racing, manual-flight-first platforms | You need autonomous navigation, mission planning, or BVLOS |
| **ArduPilot** (ArduCopter, ArduPlane, ArduRover) | Autonomous missions, survey, BVLOS, complex integrations | You just want to fly FPV and don't need the complexity |
| **iNav** | Fixed-wing with GPS, long-range with return-to-home, middle ground | High-performance freestyle, defense/military applications |
| **PX4** | Research, ROS2 integration, enterprise development | Most commercial operators — ArduPilot has better community support |
| **Cleanflight** | Legacy only; superseded by Betaflight | All new builds |
| **KISS** | Proprietary racing ecosystem | Any build requiring open-source flexibility |

Once you've picked firmware, the universe of compatible FCs narrows significantly. Most H7-based boards target Betaflight or ArduPilot; some support both.

---

## MCU: F4 vs F7 vs H7

### F4 (STM32F4xx)

**Clock speed:** 168MHz  
**RAM:** 192KB  
**Best for:** Most Betaflight builds, simple ArduPilot builds without heavy logging

F4 was the standard for 5 years. Still works perfectly for Betaflight freestyle and racing. The constraint: 8KB of SRAM for the logger means compressed logs that can miss fast events, and the 8kHz gyro loop is pushing the limit on an F4 — you'll see CPU usage warnings in Betaflight at 8kHz on most F4 boards.

Betaflight 4.4+ deprecated F4 support for some features (RPM filtering with 8 motors, 8kHz gyro loop stability). If you're building new, there's no good reason to choose F4 over H7 unless cost is the absolute constraint.

### F7 (STM32F7xx)

**Clock speed:** 216MHz  
**RAM:** 512KB  
**Best for:** High-performance Betaflight builds; some ArduPilot builds

F7 hit the sweet spot for a couple of years. Faster than F4, more RAM, no longer the default choice now that H7 prices have dropped. Still a solid choice if you find a good F7 board at a good price.

### H7 (STM32H7xx)

**Clock speed:** 480MHz  
**RAM:** 1MB+  
**Best for:** Everything that benefits from processing power — 8kHz+ gyro loops, heavy logging, ArduPilot with all features enabled, onboard AI inference

H7 is the current standard for mid-to-high-end builds. The extra headroom means:
- 8kHz gyro loop with stable CPU usage in Betaflight
- Full logging without compression
- Room for additional processing (RPM telemetry, MAVLink, camera protocol)
- ArduPilot AHRS computation at higher rates

**Price premium over F4:** $15–30 on a typical stack. Usually worth it.

---

## IMU: Single vs Dual

Dual IMU means two separate inertial measurement units on the FC board. Benefits:

1. **Redundancy:** If one IMU fails mid-flight, the FC continues operating on the second. Critical for BVLOS and commercial operations.
2. **Cross-checking:** The FC can compare both IMUs and alert if they diverge — early warning of sensor degradation.
3. **Vibration isolation:** Two IMUs can use different physical mounting — one soft-mounted for clean attitude estimate, one hard-mounted for fast transient detection.

ArduPilot uses dual IMU natively via `INS_USE` and `INS_USE2` parameters. Betaflight acknowledges the second IMU but uses only one at a time.

**When dual IMU matters:**
- Any BVLOS operation (single IMU failure = loss of aircraft)
- Precision survey (IMU health affects data quality)
- Commercial cargo (liability exposure for hardware failure)
- >$2,000 platform value

**When it doesn't matter:**
- FPV freestyle (crashes happen regardless; redundancy doesn't change the risk profile)
- Racing (weight > redundancy)
- Low-risk recreational builds

---

## NDAA Compliance: What It Actually Means in Procurement

The National Defense Authorization Act restrictions on Chinese-manufactured technology affect drone procurement primarily for government, defense, and critical infrastructure customers.

**What the restriction covers:**
- NDAA Section 848/899 prohibits DoD procurement of UAS manufactured in China, or using components from listed Chinese manufacturers (DJI, Dahua, Hikvision, Huawei, Hytera, and several others depending on the year's NDAA)
- FAA Reauthorization Act extends similar restrictions to FAA and DHS use
- Blue UAS Framework (DIU) identifies NDAA-compliant alternatives

**What it means for FC selection:**
An FC is "NDAA compliant" if:
- It's manufactured outside China (US, EU, Canada, Israel, Taiwan commonly)
- Its MCU is not from a listed Chinese supplier (STMicroelectronics is French/Italian — compliant; some Chinese SoCs are not)
- Its supporting components (IMU, barometer, compass) don't originate from listed entities

Most flight controllers from US-based companies (Pixhawk/Holybro when made in Taiwan/EU, Cube Pilot in Australia, mRo in the US, Emlid in Russia/Latvia — check current status) are NDAA compliant.

**Practical check:** Look at the Forge database entry for `ndaa_compliant: true`. For defense procurement, verify against the current Blue UAS Framework list maintained by the Defense Innovation Unit — the list updates annually and some previously-compliant manufacturers have been added or removed.

**For commercial operations without government clients:** NDAA compliance is a marketing differentiator, not a legal requirement. For government or defense contracts: it's a go/no-go criterion.

---

## Peripheral Compatibility Matrix

The FC must physically support every peripheral you plan to use. Before finalizing a FC choice:

| Peripheral | Required FC Feature | Check |
|---|---|---|
| GPS (standard) | 1 UART | Almost universal |
| GPS (RTK) | 1 UART at 230400 baud + injection support | Verify baud rate support |
| Second GPS | 2nd UART | Many boards support; verify |
| Telemetry (MAVLink) | 1 UART | Almost universal |
| RC receiver (SBUS/ELRS) | SBUS/UART input | Standard |
| RC receiver (CRSF/ELRS) | UART (full-duplex) | Most modern boards |
| ESC (DShot + bidirectional) | Timer outputs on motor pins | Standard on F7/H7; verify on F4 |
| Optical flow sensor | I2C or UART | Verify pin availability |
| Rangefinder (UART) | 1 UART | Check total UART count |
| Companion computer | 1 high-speed UART (921600) | Check if baud rate is supported |
| ADS-B receiver | 1 UART | Check total UART count |
| Remote ID module | 1 UART | Check total UART count |
| CAN bus (DroneCAN) | CAN1 (and CAN2 for redundancy) | Check board spec |
| Current sensor | ADC input | Most boards, verify |

**Count your UARTs.** A fully-loaded survey platform (GPS + RTK corrections + MAVLink telemetry + companion computer + ADS-B + Remote ID) needs 5–6 UARTs. Many boards have 6–8; some have only 4. Running out of UARTs forces you into UART multiplexers or sacrificing a peripheral.

---

## Evaluation Checklist

Use this checklist when evaluating a specific FC for a specific application:

**Firmware support**
- [ ] Target firmware confirmed supported (check manufacturer firmware page, not just "compatible")
- [ ] Firmware version matches minimum required version for your features

**Processing**
- [ ] MCU generation (F4/F7/H7) sufficient for planned loop rates and features
- [ ] RAM adequate for logging configuration

**IMU**
- [ ] Single or dual IMU per risk profile requirement
- [ ] IMU type known (ICM-42688P, ICM-42605, MPU-6000, BMI270 — affects filtering requirements)

**Connectivity**
- [ ] UART count ≥ peripheral count
- [ ] CAN bus (if needed)
- [ ] I2C pins available
- [ ] SPI available for fast peripherals

**Power**
- [ ] Input voltage range covers your battery (4S = 16.8V, 6S = 25.2V)
- [ ] Onboard BEC rated for your peripherals
- [ ] Current sensor integrated or available

**Physical**
- [ ] Mounting pattern matches frame (30.5×30.5, 20×20, 25.5×25.5 are common)
- [ ] Stack height fits frame
- [ ] Weight acceptable

**Compliance (if required)**
- [ ] NDAA compliance verified against current Blue UAS list
- [ ] Country of manufacture documented

---

## Common Mistakes

**Choosing the FC before choosing the firmware.** Then discovering the FC has limited firmware support for your required features (e.g., no DroneCAN support, limited UART count for ArduPilot peripherals).

**Buying an all-in-one stack for a complex build.** AIO stacks (FC+ESC on one board) are great for 2"–5" FPV builds. For a survey platform with GPS, ADS-B, companion computer, and gimbal: use separate FC and ESC — it's much easier to troubleshoot when the units are separate.

**Ignoring the BEC spec.** An FC with a 1A BEC powering a Raspberry Pi Zero (350mA) + GPS (150mA) + receiver (200mA) = 700mA — close to the limit before adding a camera. The BEC gets warm, thermal throttles, and causes intermittent brownouts that look like software bugs.

**Assuming dual IMU = better attitude estimation.** Two identical IMUs at the same location produce two noisy measurements from the same vibration environment. The improvement comes from the redundancy and potential for cross-checking, not from statistical averaging of noise. For better attitude estimation, the answer is better vibration isolation and RPM filtering, not more IMUs.
