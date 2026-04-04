# AI Accelerators for Drone Systems

> **Forge cross-reference:** 13 entries in `ai_accelerators` category  
> **Related handbook chapters:** Ch. 13 (Companion Computers), Sensor Payload Integration

## Why Edge AI Matters for Drones

Every autonomous drone capability — obstacle avoidance, target tracking, SLAM navigation, classification — requires neural network inference. Running that inference on a ground station adds latency and requires a continuous data link. Running it on the drone (edge inference) eliminates both problems but demands dedicated hardware: the flight controller's MCU cannot spare the cycles.

AI accelerators bridge this gap. They sit alongside or inside the companion computer and handle the matrix math that neural networks require, leaving the CPU free for mission logic, ROS nodes, and communications.

## Key Specifications

**TOPS (Tera Operations Per Second)** is the headline metric, but it is not the whole story. A 26 TOPS accelerator running a well-optimized model can outperform a 40 TOPS chip running unoptimized code. What actually matters for drone integration:

- **TOPS/watt** — Power efficiency determines flight time impact. The Syntiant NDP250 delivers 0.5 TOPS at 10 milliwatts; the Axelera Metis delivers 214 TOPS at ~14.7 TOPS/W. Choose based on mission: always-on acoustic detection needs microwatts, real-time 4K object detection needs tens of TOPS.
- **Form factor** — USB dongles (Coral, Movidius) are fastest to prototype but add cable weight and a failure point. M.2 modules (Hailo-8, Hailo-10H) integrate cleanly into carrier boards. SoC packages (Ambarella CV5/CV7) require custom PCB design but eliminate interconnects entirely.
- **Framework support** — Most accelerators support TensorFlow Lite and ONNX. NVIDIA Jetson requires CUDA/TensorRT. Hailo uses its own compiler (Hailo Dataflow Compiler). Check that your model's operators are supported before committing to hardware.
- **Thermal** — Passive cooling is strongly preferred on drones (no fan noise, no dust ingestion, no vibration-sensitive bearing). Hailo-8 runs passively at 2.5W. Jetson Orin Nano needs a heatsink and may need active cooling above 15W mode.

## The Landscape

### High-Performance (15+ TOPS)

These handle real-time object detection on 4K video, multi-camera SLAM, and path planning neural networks:

- **NVIDIA Jetson Orin Nano** — 40 TOPS, 1024 CUDA cores, full ROS 2 support, CUDA/TensorRT ecosystem. The default choice for Blue UAS programs needing proven autonomy stacks. ARK Electronics makes an NDAA-compliant carrier board ("Just a Jetson"). 7–15W configurable.
- **Hailo-10H** — 40 TOPS at 2.5W with generative AI capability (10+ tokens/sec on 2B parameter models). M.2 form factor, automotive-qualified (AEC-Q100), works on Raspberry Pi 5 or any PCIe host. First edge chip to run LLMs and VLMs on-device.
- **Ambarella CV5/CV7** — 20–30 TOPS with integrated ISP (image signal processor). Designed specifically for camera pipelines — processes 8K video while running detection networks. OEM-only (no dev kit), but dominant in commercial drone cameras.
- **Axelera Metis** — 214 TOPS at 14.7 TOPS/W using digital in-memory compute with RISC-V. Highest raw throughput in the Forge DB. European (Netherlands), allied-nation compliant.
- **Kinara Ara-2** — 50 TOPS at 6W, capable of running models up to 30B parameters in INT4. Runs Llama2-7B at tens of tokens/sec on-device.
- **Qualcomm RB5** — 15 TOPS with 5G connectivity, 7 camera inputs, and ROS 2 support. Unique value: native 5G modem eliminates separate cellular module for BVLOS telemetry.
- **DeepX DX-M1** — 25 TOPS at 5W with proprietary quantization that claims FP32-comparable accuracy in INT8. South Korean (allied nation).

### Mid-Range (1–15 TOPS)

Suitable for single-camera detection, classification, and lightweight tracking:

- **Hailo-8** — 26 TOPS at 2.5W in M.2 form factor. Stackable up to 4× (104 TOPS). Passive cooling, runs YOLOv5/v7/v8/v11 natively. The workhorse for production FPV and ISR builds that need object detection without Jetson power draw.
- **Google Coral USB** — 4 TOPS via Edge TPU over USB 3.0. Lowest barrier to entry ($60, plug-and-play). TensorFlow Lite only. Good for prototyping, limited for production (USB connector reliability, single-framework lock-in).
- **Intel Movidius Myriad X** — 4 TOPS via USB, supports OpenVINO. Effectively discontinued but still available. Being replaced by Hailo in new designs.
- **Kneron KL720** — 1.5 TOPS at 1W with transformer support. Cheapest SoC option (~$30). Good for basic classification on weight-constrained platforms.

### Ultra-Low Power (<1 TOPS)

Always-on sensing that runs on battery power indefinitely:

- **Syntiant NDP250** — 0.5 TOPS at 10 milliwatts. Neural Decision Processor designed for always-on wake word detection, acoustic classification, and anomaly sensing. At 1 gram, it can run for months on a coin cell. Use case: perimeter drone that sleeps until it hears a motor or voice.

## NDAA and Compliance

Most accelerators in the Forge DB are NDAA-compliant or allied-nation sourced. The notable exceptions to watch:

- Hailo is Israeli (allied nation, generally acceptable for DoD)
- Ambarella and NVIDIA are US-headquartered but fabricate on TSMC (Taiwan) — see PIE supply constraint flags for Taiwan scenario analysis
- DeepX is South Korean (allied)
- Axelera is Dutch (NATO ally)

The STM32-based flight controllers that these accelerators pair with face their own supply constraints — see PIE predictions for STM32H7 allocation forecasts.

## Integration Patterns

The typical stack is: **Flight Controller ↔ UART/MAVLink ↔ Companion Computer ↔ PCIe/USB ↔ AI Accelerator**

For companion computer selection and wiring, see the Companion Computers handbook chapter. The critical integration decisions:

1. **Interface choice** — PCIe (M.2) offers lowest latency and highest bandwidth. USB is easiest but adds a failure point. SoC-integrated (Ambarella, Qualcomm) eliminates the interconnect entirely.
2. **Power rail** — Most accelerators draw from the companion computer's power rail. Budget the wattage: a Jetson Orin Nano at 15W mode plus a Raspberry Pi 5 at 8W means 23W just for compute, before cameras and radios.
3. **Model deployment** — Compile and quantize models on a workstation, deploy compiled binaries to the edge device. Each accelerator has its own compilation toolchain.
4. **Thermal management** — Mount heatsinks with thermal pads, ensure airflow from prop wash reaches the compute stack. Vibration-isolate if using active cooling fans.
