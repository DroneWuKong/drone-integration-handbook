# Sensors and calibration — deep research and fact check, 18 October 2026

## Result and scope

The initial draft needed corrections and tighter limits. The revised chapter and worksheet incorporate a self-review of **57 material claim groups**: 30 retained, 5 corrected and 22 expanded. The complete mapping is in [the claim ledger](2026-10-18-sensor-calibration-claims.json). These counts describe this review's grouped claims, not the site's automated passage inventory or an independent review.

The review read **21 primary documentation pages**, two pinned upstream reader implementations, and the version record plus relevant full-text sections of one research paper. It also inspected 13 committed Sensor Calibration Lab files at v0.3.0, revision `8db0394`, and the separate Orqa edition's README at `46a69f7`. Mutable app work was preserved and excluded from the capability assessment. No app runtime, sensor recording, physical test or destination integration was executed.

The chapter remains on the existing local branch based on `ed320f4bb0f234b269d6063a33ef8febca1b0a12`. No publication, deployment or license change is represented by this review.

## Corrections and consequential clarifications

### Compensation is model-dependent

The original placement table's “cannot fix” wording was too broad. ArduPilot documents current-related magnetic compensation; PX4 documents static-pressure position-error compensation when its estimator prerequisites hold. The revised table distinguishes installation issues, static calibration and supported compensation models. Neither mechanism is a generic remedy for arbitrary interference, blocked ports or leaks. [ArduPilot CompassMot](https://ardupilot.org/copter/docs/common-compass-setup-advanced.html#compassmot-compensation-for-interference-from-the-power-wires-escs-and-motors) and [PX4 pressure compensation](https://docs.px4.io/main/en/advanced_config/tuning_the_ecl_ekf#correction-for-static-pressure-position-error) are the primary sources.

Similarly, known beam orientation can be used to convert slant distance under an appropriate terrain model. The new cosine example is explicitly restricted to flat level ground and distinguishes height at the sensor from height at the aircraft reference point. It is a geometric derivation, not an unconditional height correction.

### Calibration and validation need precise meanings

Engineering sensor calibration often means fitting model parameters. The metrological definition includes measurement standards and uncertainty and distinguishes calibration from adjustment. Validation concerns requirements adequate for intended use. The original shorthand equated validation too closely with a fresh-data check; that check is now identified as one part of the evidence. [JCGM calibration](https://jcgm.bipm.org/vim/en/2.39.html) and [validation](https://jcgm.bipm.org/vim/en/2.45.html) support the correction.

### Reference points and transforms

The original signed FRD example and inverse transform were correct. The revised text makes column-vector and origin conventions explicit and distinguishes an inverse transform's translation from a mounting offset in another frame. [Modern Robotics](https://modernrobotics.northwestern.edu/nu-gm-book-resource/3-3-1-homogeneous-transformation-matrices/) supports the frame algebra.

The camera principal point is an image coordinate, whereas the optical/projection center is a three-dimensional model origin. A GNSS physical antenna reference point is also distinct from its frequency/direction-dependent electrical phase-center model. These distinctions are now stated directly and added to the worksheet. [OpenCV](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html), [ROS CameraInfo](https://docs.ros.org/en/jazzy/p/sensor_msgs/msg/CameraInfo.html) and [NOAA NGS](https://geodesy.noaa.gov/ANTCAL/FAQ.xhtml) provide the relevant definitions.

### A small image residual can conceal wrong metric scale

OpenCV defines target-based pose lengths in the units used for object points. Scaling both target coordinates and translation by the same factor preserves ideal pinhole projections. Thus the new 20 mm versus 25 mm example is a deliberate counterexample to treating a good fit as proof of metric accuracy. Its scope excludes a general prediction for jointly constrained camera/IMU solvers. [OpenCV target units](https://docs.opencv.org/4.13.0/dc/dbb/tutorial_py_calibration.html) and [Kalibr target measurement](https://github.com/ethz-asl/kalibr/wiki/calibration-targets) support that explanation.

### Motion and timing assumptions

The observability claim was checked in Yang, Geneva, Zuo and Huang, *Online Self-Calibration for Visual-Inertial Navigation Systems*, arXiv **2201.09170v3**, sections 6 and 7.2. For the analyzed model, pure translation and single-axis rotation leave particular extrinsic translations unobservable. The statement is restricted to that analysis, and does not promise another solver's convergence or accuracy. The [version record](https://arxiv.org/abs/2201.09170v3) identifies revision 3 dated 29 January 2022; [the body text](https://arxiv.org/html/2201.09170v3#S7.SS2) was read rather than relying on an abstract. No journal-review status is inferred from arXiv hosting.

Exposure event, acquisition timestamp and receipt timestamp are also distinguished. Short exposure reduces motion blur but does not remove rolling-shutter row timing. A fitted constant shift is not proof of stable hardware synchronization. [ROS acquisition metadata](https://docs.ros.org/en/jazzy/p/sensor_msgs/msg/CameraInfo.html), [Basler shutter timing](https://docs.baslerweb.com/electronic-shutter-types) and [Kalibr acquisition requirements](https://github.com/ethz-asl/kalibr/wiki/camera-imu-calibration) support these limits.

### The app summary now reflects its actual input contracts

Source inspection confirmed the four task paths, fixed-candidate fresh checks, export restrictions and false physical/application qualification flags. The chapter now additionally states:

- Camera/IMU import expects metric poses in one fixed target world, corrected gyro and accelerometer specific force, linked intrinsics and mapped capture clocks. Gravity-subtracted linear acceleration is a different input.
- Flow import assumes normalized axis conventions, a flat normal target and constant distance within a motion window. Raw MAVLink flow fields are angular rotation-axis measurements, not the app's declared translation convention. [PX4's definition](https://docs.px4.io/main/en/sensor/optical_flow) corroborates this external message distinction.
- Rig adjustment angles use camera optical axes and are not aircraft Euler angles or actuator commands.
- The summary is pinned to v0.3.0 rather than describing unrelated, uncommitted app development as reviewed support.

These are source-code observations, not a fresh app test or proof of hardware behavior. Private app source was not copied into the public ledger; local hashes identify the files inspected.

The export interpretation was additionally checked against the actual [OpenVINS reader at revision 69488123](https://github.com/rpng/open_vins/blob/69488123ed9362dd44b6f28e7f4680abbff1442b/ov_msckf/src/core/VioManagerOptions.h) and the [ROS YAML parser at 5.1.8](https://github.com/ros-perception/image_common/blob/5.1.8/camera_calibration_parsers/src/parse_yml.cpp). The former loads a camera-to-IMU transform and inverts it for its state; the latter names the exported calibration matrices and metadata. These source mappings agree with the pinned app's stated export directions and fields. This does not establish destination runtime acceptance or estimator operation.

## Numerical and source verification

The original numerical examples were correct. A separate geometric calculation, independent of the app solver, checked:

| Example | Calculated value | Interpretation |
|---|---|---|
| Perpendicular plane 100 m away, 1° pointing change | 1.7455064928 m | Ideal ray intersection shift |
| Radius 0.20 m, angular speed 90°/s | 0.3141592654 m/s | Tangential speed perpendicular to the axis |
| Speed 15 m/s, interval 20 ms | 0.30 m | Constant-rate translation |
| Rate 60°/s, interval 20 ms | 1.2° | Constant-rate rotation |
| Actual target square 25 mm, entered square 20 mm | Scale factor 0.8 | Pose-translation scale in the specified ideal model |
| Rigid-transform forward/inverse round trip | Maximum error 0.0 in the checked example | Algebraic consistency only |
| Project original/scaled target and translation | Maximum pixel difference 0.0 in the checked example | Demonstrates the scale ambiguity |

The calculations and original/revised source hashes are retained with the local review artifacts. External captures are normalized Markdown returned by the retrieval tool; their digests are not presented as hashes of raw publisher response bytes. Source reachability is separate from factual support.

The arXiv search index exposed an update timestamp differing from the version record; the version record and versioned body were used for the cited revision. A site-restricted airspeed search returned no results, but direct retrieval of the official [ArduPilot installation page](https://ardupilot.org/plane/docs/airspeed.html) succeeded. Neither discrepancy was treated as a technical contradiction.

## Verification status and remaining limits

All **58 Python tests and 30 JavaScript tests passed**. Python compilation, handbook JavaScript syntax, all 406 internal source links, site build, generated-site validation, evidence/hold checks, table reconciliation and review-queue checks also passed. The generated inventory contains 165 references, 44 supported records and 5,251 unreviewed records, with the two existing holds preserved. Those inventory counts are separate from this review's 57 grouped claims.

The updated generated chapter HTML passed focused rendering checks at 390 px and 1,280 px with the site CSS: no page-level horizontal overflow, a loaded diagram and no page errors. The worksheet remained accessible without JavaScript and was regenerated as a two-page printable PDF. The earlier full-site browser suite remains inconclusive; its timeout/interruption is preserved in [the initial preparation record](handbook-sensors-calibration-20261018.md). Focused rendering checks do not replace that suite.

This is an evidence-backed self-review. It does not establish metrological traceability, an independent human sign-off, physical sensor accuracy, app runtime qualification, flight readiness or production publication. Ordinary checklist prompts and symptom hypotheses remain editorial guidance; no universal distance, calibration interval or acceptance threshold was invented.
