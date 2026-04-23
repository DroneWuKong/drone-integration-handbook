# Integrated Flight Stacks

> **Forge cross-reference:** 5 entries in `integrated_stacks` category  
> **Related handbook chapters:** Flight Controllers, Companion Computers, AI Accelerators

## The Integration Problem

Traditional drone avionics are modular: a flight controller handles stabilization, a companion computer handles autonomy, an AI accelerator handles inference, and they communicate over UART/MAVLink with separate power, mounting, and cooling. This modularity enables customization but adds weight, wiring complexity, failure points, and integration effort.

Integrated stacks collapse two or more of these functions onto a single board. The trade-off is clear: less flexibility, but dramatically simpler integration, lower weight, and fewer points of failure.

## The Landscape

### ModalAI VOXL 2

The VOXL 2 runs PX4 directly on the Qualcomm QRB5165's DSP — no separate flight controller MCU required. This is the most aggressive integration in the category: flight control, AI inference (15+ TOPS across Hexagon HTA, GPU, DSP, and NPU), and companion computing all on one chip. Blue UAS Framework listed. 8 GB LPDDR5, Wi-Fi 6, 4 MIPI-CSI camera inputs.

The **VOXL 2 Mini** shrinks this to a 42×42mm board (11g) with 30.5mm mounting holes, fitting inside 5-inch FPV frames. Same silicon, same capabilities.

Primary use case: autonomous navigation in GPS-denied environments using visual-inertial odometry. The ModalAI software stack provides VIO, obstacle avoidance, and SLAM out of the box.

Limitation: locked to the Qualcomm/PX4 ecosystem. Cannot run Betaflight or ArduPilot. The QRB5165 is a supply chain concern — see PIE predictions for successor timeline.

### Auterion Skynode S

Combines an FMUv6x flight controller (STM32H7) with a dedicated NPU mission computer in a chip-down design on a 30.5mm board. Blue UAS Framework listed. Unlike VOXL 2, the flight controller runs standard PX4 on a separate MCU from the mission computer, maintaining the traditional separation of concerns at the silicon level while integrating at the board level.

Primary use case: commercial BVLOS platforms that need both certified flight control and onboard AI processing. Auterion's cloud-connected ecosystem provides fleet management, OTA updates, and flight logging.

### Orqa DTK APB

Combines an STM32H743 flight controller with an NXP i.MX8M Plus companion computer (2.25 TOPS NPU). Designed to collapse the FC + companion stack for FPV and tactical platforms. The NPU enables onboard AI inference without a separate accelerator module. 36g, 65 × 37.5 × 16.3 mm, 0–70°C. Firmware: ArduPilot / PX4 / iNav / Betaflight.

Primary use case: tactical FPV platforms where weight and wiring simplicity matter more than maximum AI compute. The 2.25 TOPS NPU handles basic detection and classification but is not sufficient for real-time SLAM or multi-camera processing.

### ARK Electronics ARK FPV Flight Controller

NDAA-compliant FPV FC based on ARKV6X with STM32H743, industrial-grade IIM-42653 IMU, barometer, and magnetometer. 30.5mm mounting, 3–12S input with regulated 12V 2A output. While categorized as an integrated stack, this is closer to a high-quality standalone FC than a true FC+companion integration — the "integration" is the industrial-grade sensors and NDAA compliance, not a companion computer.

Primary use case: NDAA-compliant FPV builds that need better sensors than typical hobby FCs provide.

## When to Use an Integrated Stack vs. Modular

Choose integrated when: weight is critical, the platform is standardized (not experimental), the software ecosystem matches your needs, and you do not need to swap individual components independently.

Choose modular when: you need to iterate on the AI/autonomy stack without replacing the FC, you want to use a specific accelerator (Hailo, Jetson) that is not available in an integrated package, or you need a flight controller firmware (Betaflight, iNav, ArduPilot) that the integrated stack does not support.

## Supply Chain Considerations

Integrated stacks concentrate supply chain risk. If the SoC goes end-of-life or allocation-constrained, the entire avionics package is affected — you cannot swap just the companion computer. The QRB5165 (VOXL 2) and STM32H7 (Skynode, DTK APB, ARK FPV) both appear in PIE supply constraint predictions. Evaluate single-source risk before committing a production program to an integrated stack.
