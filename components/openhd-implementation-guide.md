# OpenHD Implementation Reference

OpenHD uses an air/ground video and telemetry architecture. Select a matched software image, camera/codec pipeline and exact adapter revision. A chipset family name alone does not establish driver or image compatibility.

## Adapter support — checked 2026-10-07

The project's [WiFi adapter page](https://openhdfpv.org/hardware/wifi-adapters/) lists **RTL8812AU, RTL8814AU, RTL8811AU, RTL8812BU and RTL8812EU** as supported since **2.6.3**. Its dongle list includes **BLM8812EU**. The project also maintains an [RTL88x2EU driver repository](https://github.com/OpenHD/rtl88x2eu). The earlier suggestion that EU support was absent is withdrawn.

| Record | Establish before integration |
|---|---|
| Adapter | Manufacturer/model/revision, actual chipset, USB IDs and antennas |
| Image | Exact OpenHD release/image/hash, air/ground role and SBC target |
| Driver | Kernel, driver revision and injection/receive support in that image |
| Camera | Interface, driver, encoder, codec/profile and tested mode |
| Ground | Supported hardware decoding and display path |
| Power | Adapter and SBC rail demand, transients, cooling and connectors |

The adapter page warns about certification status for BLM8812EU. Technical support is separate from authorization or equipment approval; verify the exact module and intended jurisdiction against current authority. No import/use permission is implied here.

## Software-first checks

Start with the [official setup documentation](https://openhdfpv.org/introduction/first-time-setup/) and image for the exact host. Preserve a known-good image before changes. Confirm both nodes' software versions, device discovery and configuration readback. A generic MediaTek issue report is evidence about that reported setup, not proof that every adapter in that family fails or succeeds.

Replay local media through the intended encoder/decoder pipeline, then test a controlled transport fixture. Track video frame freshness separately from MAVLink telemetry. On the ground, the receiving pipeline **decodes** video; air-side encoding and ground-side decoding must not be conflated.

## Latency and failures

Report the complete measurement boundary: camera exposure/capture, codec/profile, resolution/frame rate, buffering/FEC, RF mode, decoder and display. Packet timing or a decoder benchmark is not glass-to-glass latency. Generic claims that a particular SBC halves latency or guarantees a numerical range are withdrawn.

Inspect device enumeration, driver logs, video frame/caps errors, link/FEC counters, frame age and power/thermal state before changing parameters. Keep the exact original settings and test result. See [video pipeline troubleshooting](../integration/video-pipeline-troubleshooting.md), [software failure tests](../integration/software-failure-testing.md) and [field evidence](../field/evidence-record.md).
