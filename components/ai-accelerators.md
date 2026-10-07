# AI Accelerators for Drone Systems

Neural inference is one possible workload. Classical estimation, geometry, planning and control do not universally require a neural network. Select compute against the actual model, camera/video path and concurrent CPU workload.

## Manufacturer-reported example

Hailo reports **up to 26 TOPS** for **Hailo-8** and **typical chip power of 2.5 W**. Those are manufacturer-reported chip specifications, not measured whole-board power or camera-to-result performance. A 26 TOPS part does not belong in a 1–15 TOPS category; the former category placement is corrected.

[claim:hailo8-spec-scope]

[Hailo-8 manufacturer specifications](https://hailo.ai/products/ai-accelerators/hailo-8-ai-accelerator/), checked 2026-10-07. Distinguish Hailo-8 from Hailo-8L and Hailo-10H, and chip from module/carrier. The old unsourced price/power/availability rankings are withdrawn pending exact-model checks.

## Compare complete workloads

| Dimension | Evidence |
|---|---|
| Arithmetic | Precision/sparsity conditions and the operations counted by the vendor |
| Model | Operator support, compiler/runtime version, input shape and measured accuracy |
| Pipeline | Capture/ISP, decode/encode, memory copies and preprocessing/postprocessing |
| Timing | End-to-end distribution, deadline misses and stale-result rejection |
| Power/thermal | Whole-board/carrier/cooling measurements and throttling behavior |
| Lifecycle | Exact product/release status, drivers, updates and recovery |

More TOPS does not establish a lower latency or a supported model. A neural accelerator may not include the required video codec engine. Benchmarks must name the exact workload and hardware/software configuration.

## Procurement

Headquarters, allied-country status or fabrication location does not establish a procurement conclusion. Screen the exact component, assembled system, buyer and contract under the [federal procurement guide](ndaa-compliance.md). This page assigns no universal NDAA badges.

See [workload selection](../integration/compute-workload-selection.md), [companion integration](../integration/companion.md) and [emerging technology](../integration/emerging-technology-watch.md).
