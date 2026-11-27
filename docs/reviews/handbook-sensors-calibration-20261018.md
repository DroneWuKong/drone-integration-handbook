# Sensors and calibration chapter — local candidate, 18 October 2026

Subsequent review: [deep research and claim-level fact check](2026-10-18-sensor-calibration-fact-check.md). The original preparation record below is retained; its inventory and verification counts describe that earlier candidate.

## Scope and base

Prepared on branch `codex/sensors-calibration-chapter` from upstream main commit `ed320f4bb0f234b269d6063a33ef8febca1b0a12`, in a separate Git worktree. The pre-existing checkout, its local deletions and historical copies were preserved. This record describes a local candidate, not a public release or physical validation.

Chapter 65 adds sensor placement, mounting/alignment, coordinate frames, signed lever arms, boresight, camera intrinsics, inter-sensor extrinsics, timing, acquisition, fresh-data validation, destination checks and fault diagnosis. Appendix G, chapter 66, provides an installation/calibration worksheet. Related preflight, perception, optical-flow, payload and time/coordinate pages link to the new material. Original SVG geometry and calculated examples are instructional illustrations.

## Documentation evidence

Primary pages read on 18 October 2026:

- [PX4 controller mounting](https://docs.px4.io/main/en/assembly/mount_and_orient_controller): orientation, center-of-gravity placement and manufacturer mounting strategy.
- [ArduPilot sensor position offsets](https://ardupilot.org/copter/docs/common-sensor-offset-compensation.html): signed meter offsets, reference-origin conditions and partial compensation limitations.
- [ArduPilot advanced compass setup](https://ardupilot.org/copter/docs/common-compass-setup-advanced.html): orientation and interference context. No powered propeller procedure was reproduced.
- [ROS REP 103](https://www.ros.org/reps/rep-0103.html): body/optical/navigation frames, SI units and rotation conventions.
- [Kalibr camera/IMU calibration](https://github.com/ethz-asl/kalibr/wiki/camera-imu-calibration): intrinsic prerequisites, multi-axis motion, blur and timestamp requirements.
- [NovAtel imaging boresight](https://docs.novatel.com/Waypoint/Content/Inertial_Explorer/Solve_Boresighting_Angles.htm): IMU/imaging-system orientation relationship; vendor-specific flight instructions were not generalized.
- [NovAtel OEM7 lever arms](https://docs.novatel.com/OEM7/Content/SPAN_Operation/Lever_Arm_Calibration_Routine.htm): remounting, measurement and observability limitations.
- [OpenCV 4.13.0 camera calibration](https://docs.opencv.org/4.13.0/dc/dbb/tutorial_py_calibration.html): camera intrinsics, distortion and pose rotation/translation.

Five scoped managed claims and five source records were added. Existing claims, source records, identities and table dispositions were compared structurally with the base and preserved. New tables retain the normal machine-classified review state; adding citations does not mark every new inventory passage reviewed. The two existing publication holds remain intact.

## Companion app provenance

The capability summary was checked against Sensor Calibration Lab v0.3.0 documentation at commit `8db0394`, including its README, architecture/export guidance and distribution policy, and the separate Prismo Calibration README/Orqa guide at commit `46a69f7`. These are private app sources. The handbook adds original explanatory prose; no app source, license, recordings, binaries or private evidence was imported.

The Lab's four implemented workflows are camera lens, camera/IMU, optical flow and camera rigs. Device application, generic direct flight-controller acquisition, standalone IMU intrinsic calibration and other sensor workflows are not represented as implemented. Export mapping/software checks remain separate from physical accuracy, hardware synchronization, destination runtime behavior and flight qualification. Private distribution and proprietary licensing are preserved.

## Local verification

- 58 Python tests and 30 JavaScript tests passed. The existing frozen-identity test's reference count was updated from 163 to 165.
- Python compilation, handbook JavaScript syntax, internal source links, site build, generated-site validation, evidence/hold checks and review-queue checks passed.
- The candidate builds 65 chapters, 39 platform profiles and 61 component references, for 165 references. Its inventory has 41 supported records and 5,242 unreviewed records; this is not a completed semantic audit.
- Structural comparisons confirmed that pre-existing identities, managed claims, sources and table dispositions are unchanged. Chapter ID 25 remains reserved.
- The examples were recalculated independently of their printed rounded values: 100 m × tan(1°) = 1.7455 m; 0.20 m × 90°/s = 0.3142 m/s after conversion to radians; 15 m/s × 0.020 s = 0.30 m; 60°/s × 0.020 s = 1.2°.
- Extracted generated chapter HTML with the site's CSS was checked at 390 px and 1,280 px: no page-level horizontal overflow, the diagram loaded, worksheet links resolved in the generated markup and no page errors occurred. The worksheet was also accessed with JavaScript disabled. The original diagram and printable worksheet were visually inspected.
- The full-site browser suite timed out on initial navigation. Its retry was interrupted by the environment restart. It remains inconclusive; the focused rendering checks do not replace that suite.

Local review artifacts are under ignored `.local/browser-check/`: viewport images, diagram previews, `sensor-content-results.json` and `sensor-installation-record.pdf`. The PDF is a review export, not an additional published asset. The generated site remains under ignored `site/`.

Publication and production verification are pending. No hardware, sensor recording, calibration accuracy, independent human review, aircraft readiness or live deployment was established by these software checks.
