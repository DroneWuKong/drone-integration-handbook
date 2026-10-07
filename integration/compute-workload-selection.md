# Selecting Compute by Workload

Select a compute platform against a complete measured workload. TOPS is an arithmetic throughput specification at stated precision/sparsity conditions, not camera-to-result latency, power at the battery or assurance that a model compiles.

## Workload record

| Workload dimension | Record |
|---|---|
| Model | Exact artifact/hash, operators, input shape, precision, compiler/runtime and accuracy test |
| Camera/video | Capture interface, ISP, encode/decode, copies, resolution/frame rate and timestamp path |
| Resource use | CPU, accelerator, RAM/bandwidth, storage and concurrent workloads |
| Power/thermal | Whole board/carrier/cooling, rail measurements, ambient/load and throttling |
| Timing | End-to-end latency distribution, deadline misses and stale-result behavior |
| Packaging | Module versus development board, connectors, recovery and software updates |

Use classical geometry/estimation/control where the workload calls for them; autonomous functions do not universally require neural inference. A CPU, GPU, NPU and video codec engine solve different parts of the pipeline.

## Emerging candidates to evaluate

ST's **STM32N6x7 AI line** includes its Neural-ART accelerator; the N6x5 general-purpose line must not be assumed to share that feature. NXP's **i.MX 95** family includes an eIQ Neutron NPU. These are manufacturer-described features, not tested flight integrations or performance equivalence to a Linux companion.

[ST STM32N6 family](https://www.st.com/en/microcontrollers-microprocessors/stm32n6-series.html) and [NXP i.MX 95](https://www.nxp.com/products/i.MX95), checked 2026-10-07. Verify exact orderable part, BSP/compiler release, supported operators, memory/camera path and board availability. Watch their release/document dates rather than treat an announcement as hardware acceptance.

For Hailo-8, the manufacturer reports up to 26 TOPS and typical chip power of 2.5 W; whole-system power remains a separate measurement. [Hailo source](https://hailo.ai/products/ai-accelerators/hailo-8-ai-accelerator/), checked 2026-10-07.

See [companion integration](companion.md), [AI accelerators](../components/ai-accelerators.md) and the [emerging technology watch](emerging-technology-watch.md).
