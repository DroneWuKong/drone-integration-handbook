# Release and Information Update Watchlist

Last checked: **2026-10-21 UTC**. Version matches establish metadata only; they do not verify every claim in a chapter. A changed release opens a section check. Preview releases remain separate from published stable releases. This table observes GitHub releases; projects may also distribute builds through other channels. A tag or code push is not a published release.

| Project | Version covered | Latest stable GitHub release / date | Preview | Status | Check these sections | Next check |
|---|---|---|---|---|---|---|
| [ArduCopter](https://github.com/ArduPilot/ardupilot/releases/tag/Copter-4.7.2) | Copter-4.7.1 | Copter-4.7.2 / 2026-10-14 | none observed | check-section | [rtk-ppk-gps-integration](../components/rtk-ppk-gps-integration.md), [mavlink-protocol](../firmware/mavlink-protocol.md), [lidar-rangefinders](../components/lidar-rangefinders.md) | 2026-10-28 |
| [Betaflight](https://github.com/betaflight/betaflight/releases/tag/2026.6.2) | 2025.12.0 | 2026.6.2 / 2026-09-16 | 2026.6.0-rc3 | check-section | [four-firmwares](../firmware/four-firmwares.md), [preflight](../field/preflight.md) | 2026-10-28 |
| [Betaflight App](https://github.com/betaflight/betaflight-configurator/releases/tag/2026.6.2) | 2025.12.1 | 2026.6.2 / 2026-09-16 | 2026.6.0-RC3 | check-section | [four-firmwares](../firmware/four-firmwares.md), [backup-upgrade-recovery](../firmware/backup-upgrade-recovery.md) | 2026-10-28 |
| [PX4](https://github.com/PX4/PX4-Autopilot/releases/tag/v1.17.0) | v1.17.0 | v1.17.0 / 2026-05-13 | v1.18.0-rc1 | version-matches | [onboard-ai-control](../autonomy/onboard-ai-control.md), [secure-multiclient-telemetry](../integration/secure-multiclient-telemetry.md) | 2026-10-28 |
| [INAV](https://github.com/iNavFlight/inav/releases/tag/9.1.0) | not version-pinned | 9.1.0 / 2026-07-09 | 10.0.0-rc2 | check-section | [four-firmwares](../firmware/four-firmwares.md), [msp-protocol](../firmware/msp-protocol.md) | 2026-10-28 |
| [OpenHD](https://github.com/OpenHD/OpenHD/releases/tag/v2.6.0) | not version-pinned | v2.6.0 / 2024-05-24 | v2.5.0-beta3 | check-section | [openhd-implementation-guide](../components/openhd-implementation-guide.md), [comms-datalinks](../components/comms-datalinks.md) | 2026-10-28 |
| [MAVLink](https://github.com/mavlink/mavlink/releases) | not version-pinned | unknown / unknown | none observed | no-published-release | [mavlink-protocol](../firmware/mavlink-protocol.md), [appendix-c-mavlink-quick-reference](../appendices/appendix-c-mavlink-quick-reference.md) | 2026-10-28 |
| [DroneCAN](https://github.com/DroneCAN/libcanard/releases) | not version-pinned | unknown / unknown | none observed | no-published-release | [can-dronecan-cyphal](../firmware/can-dronecan-cyphal.md) | 2026-10-28 |

## Check list

- Firmware: changed parameters, units, defaults, board targets and configurator compatibility.
- Protocols: XML/DSDL definitions, versioned serialization, enums and service support.
- Video/compute: image/kernel/driver/compiler compatibility, model operators and timing boundary.
- Procurement/regulations: exact authority, effective date, configuration and superseding material.
- Prices/availability: current first-party offer/date; a release is not stock availability.

Source availability and due dates are checked nightly. Software release metadata is refreshed nightly; each entry has a seven-day maximum intended interval. A failed check retains the previous observation as unavailable rather than claiming freshness. New releases trigger independent claim checks; they never silently change an aircraft's configuration.

See [emerging projects](../integration/emerging-technology-watch.md) and [repository notes](../integration/repository-updates.md).

## Related repository discovery

| Repository | Observed revision | Last push | Check attempted | Status |
|---|---|---|---|---|
| [DroneWuKong/droneclear_Forge](https://github.com/DroneWuKong/droneclear_Forge) | ad2dad14d9a4 | 2026-10-21 | 2026-10-21 | observed |
| [DroneWuKong/forge-data](https://github.com/DroneWuKong/forge-data) | 3041642fdca3 | 2026-10-04 | 2026-10-21 | observed |
| [DroneWuKong/MultiProtocol-UAS-TAK-Bridge](https://github.com/DroneWuKong/MultiProtocol-UAS-TAK-Bridge) | 3177a1ffdf91 | 2026-10-04 | 2026-10-21 | observed |
| [DroneWuKong/Orqa_H7_PX4_Ports](https://github.com/DroneWuKong/Orqa_H7_PX4_Ports) | 5dca93e099f4 | 2026-10-14 | 2026-10-21 | observed |
| [DroneWuKong/Field-Kit](https://github.com/DroneWuKong/Field-Kit) | 784d74a0f9b9 | 2026-10-02 | 2026-10-21 | observed |
| [DroneWuKong/Prismo-Calibration](https://github.com/DroneWuKong/Prismo-Calibration) | 82ac97c9e958 | 2026-10-18 | 2026-10-21 | observed |
| [Yookio-Z/Airsim-Agent](https://github.com/Yookio-Z/Airsim-Agent) | a0d97732ebee | 2026-10-21 | 2026-10-21 | observed |
| [rsasaki0109/visloc-rs](https://github.com/rsasaki0109/visloc-rs) | 87f5df38bd44 | 2026-10-21 | 2026-10-21 | observed |
| [M-BSquared/CorvusGCS](https://github.com/M-BSquared/CorvusGCS) | 26847bb9b614 | 2026-10-21 | 2026-10-21 | observed |

## Source checks and review dates

Reachability is a check; the verification date below is the last factual review. Unavailable checks retain prior fingerprints.

| Source | Last verified/accessed | Check attempted | Availability | Next factual review |
|---|---|---|---|---|
| [Reboot Hub: DJI Drone Parts — OEM-Pulled Parts and Compatibility](https://reboot-hub.com/blogs/the-reboot-hub-chronicle/dji-drone-parts-oem-pulled-replacements-compatibility) | 2026-10-03 | 2026-10-21 | reachable | 2027-01-01 |
| [ITU-R P.525-5 (November 2024)](https://www.itu.int/rec/R-REC-P.525-5-202411-I/en) | 2026-10-01 | 2026-10-21 | reachable | 2027-10-01 |
| [NIST SP 811 unit conversions](https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8) | 2026-10-01 | 2026-10-21 | reachable | 2027-10-01 |
| [NIST SP 811 derived units](https://www.nist.gov/pml/special-publication-811/nist-guide-si-chapter-4-two-classes-si-units-and-si-prefixes) | 2026-10-01 | 2026-10-21 | reachable | 2027-10-01 |
| [BIPM CIPM Recommendation 1 (2002)](https://www.bipm.org/en/committees/ci/cipm/91-2002/resolution-1) | 2026-10-01 | 2026-10-21 | reachable | 2027-10-01 |
| [Rohde &amp; Schwarz dB Calculator application note 1GP77](https://scdn.rohde-schwarz.com/ur/pws/dl_downloads/dl_application/application_notes/1gp77/1GP77_8e_dB_Calculator.pdf) | 2026-10-01 | 2026-10-21 | reachable | 2027-10-01 |
| [Federal Register: TSA Part 108 security roundtables notice (September 4, 2026)](https://www.federalregister.gov/documents/2026/09/04/2026-18124/notice-soliciting-representatives-for-technical-roundtables-on-security-of-unmanned-aircraft-systems) | 2026-10-02 | 2026-10-21 | reachable | 2026-12-31 |
| [FAA Part 107 Waivers](https://www.faa.gov/uas/commercial_operators/part_107_waivers) | 2026-10-02 | 2026-10-21 | reachable | 2026-12-31 |
| [FAA Small Unmanned Aircraft Systems Regulations (Part 107)](https://www.faa.gov/newsroom/small-unmanned-aircraft-systems-uas-regulations-part-107) | 2026-10-02 | 2026-10-21 | reachable | 2026-12-31 |
| [FAA Part 91 Public Aircraft/Public Safety CoW/A FAQ v9](https://www.faa.gov/uas/public_safety_gov/public_safety_toolkit/Public_Aircraft-Public_Safety_Operation_CoW-COA_FAQ.pdf) | 2026-10-02 | 2026-10-21 | reachable | 2026-12-31 |
| [FAA UAS Data Exchange (LAANC)](https://www.faa.gov/uas/getting_started/laanc) | 2026-10-02 | 2026-10-21 | reachable | 2026-12-31 |
| [Hailo-8 specifications](https://hailo.ai/products/ai-accelerators/hailo-8-ai-accelerator/) | 2026-10-07 | 2026-10-21 | reachable | 2026-11-06 |
| [Benewake TFmini-S specifications](https://en.benewake.com/TFminiS/index.html) | 2026-10-07 | 2026-10-21 | reachable | 2026-11-06 |
| [MAVLink packet serialization](https://mavlink.io/en/guide/serialization.html) | 2026-10-07 | 2026-10-21 | reachable | 2026-11-06 |
| [MAVLink common dialect](https://mavlink.io/en/messages/common.html) | 2026-10-07 | 2026-10-21 | reachable | 2026-11-06 |
| [MAVLink signing](https://mavlink.io/en/guide/message_signing.html) | 2026-10-07 | 2026-10-21 | reachable | 2026-11-06 |
| [Betaflight 2025.12 position hold](https://betaflight.com/docs/wiki/guides/current/Position-Hold-2025-12) | 2026-10-07 | 2026-10-21 | reachable | 2026-11-06 |
| [OpenHD adapter compatibility](https://openhdfpv.org/hardware/wifi-adapters/) | 2026-10-07 | 2026-10-21 | reachable | 2026-11-06 |
| [PX4 v1.17 Offboard](https://docs.px4.io/v1.17/en/flight_modes/offboard) | 2026-10-07 | 2026-10-21 | reachable | 2026-11-06 |
| [STM32N6 manufacturer series page](https://www.st.com/en/microcontrollers-microprocessors/stm32n6-series.html) | 2026-10-07 | 2026-10-21 | unavailable | 2026-11-06 |
| [NXP i.MX 95 manufacturer page](https://www.nxp.com/products/i.MX95) | 2026-10-07 | 2026-10-21 | unavailable | 2026-11-06 |
| [PX4 Guide: Mounting the Flight Controller](https://docs.px4.io/main/en/assembly/mount_and_orient_controller) | 2026-10-18 | 2026-10-21 | reachable | 2027-04-16 |
| [ArduPilot: Sensor Position Offset Compensation](https://ardupilot.org/copter/docs/common-sensor-offset-compensation.html) | 2026-10-18 | 2026-10-21 | reachable | 2027-04-16 |
| [ROS REP 103: Standard Units of Measure and Coordinate Conventions](https://www.ros.org/reps/rep-0103.html) | 2026-10-18 | 2026-10-21 | reachable | 2027-04-16 |
| [Kalibr: Camera IMU calibration](https://github.com/ethz-asl/kalibr/wiki/camera-imu-calibration) | 2026-10-18 | 2026-10-21 | reachable | 2027-04-16 |
| [NovAtel OEM7: Lever arm calibration routine](https://docs.novatel.com/OEM7/Content/SPAN_Operation/Lever_Arm_Calibration_Routine.htm) | 2026-10-18 | 2026-10-21 | reachable | 2027-04-16 |
| [ArduPilot: Advanced Compass Setup](https://ardupilot.org/copter/docs/common-compass-setup-advanced.html) | 2026-10-18 | 2026-10-21 | reachable | 2027-04-16 |
| [PX4 EKF2: Static pressure position error](https://docs.px4.io/main/en/advanced_config/tuning_the_ecl_ekf) | 2026-10-18 | 2026-10-21 | reachable | 2027-04-16 |
| [NOAA NGS Antenna Calibration FAQ](https://geodesy.noaa.gov/ANTCAL/FAQ.xhtml) | 2026-10-18 | 2026-10-21 | reachable | 2027-04-16 |
| [Yang et al.: Online Self-Calibration for VINS, arXiv:2201.09170v3](https://arxiv.org/html/2201.09170v3) | 2026-10-18 | 2026-10-21 | reachable | 2027-04-16 |
