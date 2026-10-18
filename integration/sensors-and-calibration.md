# Sensors and Calibration: Placement, Alignment, Boresight and Lever Arms

A camera can produce a sharp image while its position estimate is wrong. A GNSS receiver can report a precise antenna position while the camera is somewhere else. Each sensor measures from a particular place, in particular directions, at a particular time. Integration means making those relationships explicit.

Start with the physical installation, define its geometry, then calibrate and check it. The [Sensor Installation and Calibration Record](../appendices/appendix-g-sensor-calibration-record.md) provides a worksheet for that process.

## The terms in plain language

| Term | What it describes | Example |
|---|---|---|
| Placement | Where a sensor is mounted and what surrounds it | A compass beside a high-current cable |
| Alignment | How a sensor's axes relate to the aircraft or another sensor | An FC mounted sideways |
| Boresight | The angular relationship between a sensor's viewing or measurement direction and a reference | A camera looking slightly right of the IMU's forward direction |
| Lever arm | The position vector between two specified reference points | IMU origin to GNSS antenna reference point |
| Intrinsic calibration | Properties within a sensor's measurement model | Camera focal lengths, principal point and distortion; IMU scale and bias |
| Extrinsic calibration | Rotation and translation between sensors or frames | Camera-to-IMU orientation and spacing |
| Temporal calibration | The relationship between measurement times | Camera exposure time relative to IMU sampling time |
| Validation | Checking requirements and performance for the intended use | Fresh target views are one check; application accuracy needs suitable reference measurements |

This chapter uses **calibration** in the engineering sense of estimating measurement-model and alignment parameters. Metrological calibration also relates measurements to standards with associated uncertainty; it is distinct from adjusting settings. A fresh-data consistency check is useful evidence, but does not by itself establish suitability for an intended use. [JCGM calibration](https://jcgm.bipm.org/vim/en/2.39.html) and [validation](https://jcgm.bipm.org/vim/en/2.45.html) definitions explain that distinction.

In imaging, boresight often refers to the orientation between the camera and an inertial reference. Specify the full rotation when image roll matters: matching the two optical axes alone does not determine rotation around the viewing axis. [NovAtel's imaging boresight documentation](https://docs.novatel.com/Waypoint/Content/Inertial_Explorer/Solve_Boresighting_Angles.htm) describes an IMU-to-imaging-system angular calibration; its survey procedure is specific to that system.

Alignment can also mean initializing an inertial navigation system's attitude. State whether you mean a mounting rotation, a measured sensor relationship, or estimator initialization.

## Choose placement before solving calibration

An offset model describes a stable installation. Mount flex, moving cables, interference and changing airflow can make that model invalid during use.

| Sensor | Placement questions | Installation and processing issues to check |
|---|---|---|
| Flight controller / IMU | Is the mounting strategy appropriate for this controller? How far is its measurement origin from the aircraft's center of gravity? | Loose mounting, excessive vibration, clipping or changing relative motion |
| GNSS antenna | Does the installed antenna have the sky view and ground plane its manufacturer requires? Where is its specified reference point? | Blocked signals, multipath and interference; an antenna offset alone does not remove them |
| Magnetometer / compass | What motors, magnets, steel parts and power wiring surround it? Can that magnetic environment change with electrical load? | Static magnetic calibration and any supported load-dependent compensation have different scopes |
| Camera | Is the view clear across the expected motion? Are focus, zoom, resolution, crop and mounting repeatable? | Blur, an obscured view, or a lens configuration that changes after fitting |
| Camera + IMU or camera rig | Are the sensors rigid relative to one another, with useful target coverage? | A camera moving on a soft mount relative to the IMU, or flex between cameras |
| Rangefinder / LiDAR | Is the measurement direction known? Can the beam hit the frame, landing gear or an unsuitable surface? | Occlusion, invalid returns, and the attitude/terrain model used to convert slant range to height |
| Optical flow | Is there a clear view of textured ground, suitable lighting and a valid distance source where required? | Poor texture, motion blur, or an incorrect ground-distance assumption |
| Barometer / airspeed | Do the pressure ports and tubing follow the manufacturer's installation guidance? Are heat, airflow and leaks considered? | Blocked ports, pressure disturbances and plumbing faults; any pressure-error model has configuration limits |

[claim:sensor-fc-mounting]

Follow the controller's mounting instructions rather than adding arbitrary foam. A camera and IMU used as one rigid assembly need a stable relationship even if the complete assembly is isolated from the airframe. Record both relationships if the assembly can move relative to the aircraft.

For a combined GNSS/compass module, antenna position and compass orientation are separate entries. A good sky view does not establish a good magnetic environment. ArduPilot's [advanced compass guide](https://ardupilot.org/copter/docs/common-compass-setup-advanced.html) discusses orientation and motor-related interference. Use the exact system's approved checks; this chapter does not prescribe a powered propeller test.

[claim:sensor-compensation-limits]

For airspeed, match the actual pressure ports, tubing and pitot installation. ArduPilot's [airspeed installation guide](https://ardupilot.org/plane/docs/airspeed.html#installing-the-pitot-tubes) describes one system's plumbing and airflow considerations; its dimensions and port assignments are not universal mounting rules.

For optical flow, check what the reported axes mean. PX4's MAVLink input uses integrated angular measurements about the sensor axes; forward vehicle translation appears in the other flow axis. Raw integrated flow is not already a displacement vector. Its documented setup also uses valid downward range data. [PX4 optical-flow setup and conventions](https://docs.px4.io/main/en/sensor/optical_flow) must be matched by the recorder/adapter rather than inferred from field names.

There is no universal separation distance or calibration interval for every installation. Use the sensor documentation, the required measurement performance and observations of the assembled system.

## Draw the frames before entering offsets

A **coordinate frame** has an origin and three directed axes. The aircraft body frame moves with the aircraft. A navigation frame is referenced to the environment. An optical frame follows the camera's viewing geometry. Write down which one a value uses.

| Frame convention | +X | +Y | +Z |
|---|---|---|---|
| Aircraft body, forward-right-down (FRD) | Forward | Right | Down |
| ROS body, forward-left-up (FLU) | Forward | Left | Up |
| ROS camera optical | Image right | Image down | Through the lens into the scene |
| Local navigation, NED | North | East | Down |
| Local navigation, ENU | East | North | Up |

[claim:sensor-ros-frames]

[claim:sensor-ardupilot-offset-convention]

FRD and NED share a downward Z axis, but their horizontal directions differ as the aircraft turns. A forward-facing camera's optical Z can point along aircraft X; equal numbers in these frames do not mean equal physical directions.

Board mounting orientation, level-horizon correction and magnetic calibration are different settings. Set the actual mount orientation, then perform the firmware's applicable calibration procedure. A level-horizon correction is not a replacement for configuring a board mounted sideways. See [PX4 flight-controller/sensor orientation](https://docs.px4.io/main/en/config/flight_controller_orientation).

Record units as well. Millimeters entered as meters produce an offset a thousand times too large. Degrees and radians differ. Quaternion component order, Euler rotation order and transform direction must match the receiving software; a field named `rotation` does not define them.

### For software integration: make the transform direction explicit

Here, `B` is the chosen body frame and `C` is the camera optical frame. For column-vector point coordinates, define:

```text
p_B = R_BC * p_C + t_BC

R_BC: rotates vector coordinates from C into B
t_BC: position of C's origin relative to B's origin, expressed in B
```

This is a convention for this explanation. Check the destination's definition before exporting. The reverse transform has `R_CB = transpose(R_BC)` and `t_CB = -transpose(R_BC) * t_BC`. Reversing a transform generally requires both a rotation and a sign change of its translation.

The frame-composition and inverse rules follow [Modern Robotics' homogeneous-transform convention](https://modernrobotics.northwestern.edu/nu-gm-book-resource/3-3-1-homogeneous-transformation-matrices/). The translation column of a camera-from-IMU transform is the IMU origin expressed in camera axes; it is not directly the camera's mounting offset expressed in IMU axes.

Apply each transform once. Check whether the driver already rotated sensor data into body axes and whether the estimator already compensates its offset. Two correct compensations applied to the same measurement can create an incorrect result.

## Lever arms: where the measurement happens

The lever arm is a vector with a start point, an end point, a frame and units. A tape-measure distance alone leaves out direction.

Suppose the chosen origin is the IMU, with FRD body axes. A GNSS antenna reference point is 120 mm forward, 40 mm right and 80 mm above that origin. Its IMU-to-antenna lever arm, in meters, is:

```text
r_B = [+0.120, +0.040, -0.080] m
```

The negative Z means above the origin. This is a hypothetical geometry example, not a parameter preset. Confirm the firmware's actual origin: ArduPilot documents conditions where sensor offsets are relative to the IMU and where they become relative to the center of gravity. An IMU origin, the center of an FC enclosure and the center of gravity are different reference points.

Measure to the manufacturer's defined reference points. Camera projection centers, IMU reference marks and antenna reference points may not be at a housing's geometric center. Mark an inaccessible origin as estimated and record the measurement method and uncertainty.

[claim:sensor-gnss-reference-points]

A camera's **principal point** `(cx, cy)` is an image-plane coordinate, usually expressed in pixels. Its **projection/optical center** is the 3D origin used in the camera model and lever arm. They are different quantities. Preserve the pixel intrinsics, image dimensions and distortion model alongside the physical transform. [OpenCV's model definition](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) and [ROS CameraInfo](https://docs.ros.org/en/jazzy/p/sensor_msgs/msg/CameraInfo.html) make those roles explicit.

![Two side-view diagrams distinguish the IMU-to-camera position vector from the camera viewing angle. The example camera is 0.20 m forward and 0.05 m below the IMU.](/assets/sensor-geometry.svg)

[Open the geometry diagram at full size](/assets/sensor-geometry.svg).

Why does the offset matter during rotation? A sensor away from the rotation center moves even when that center stays still. For two points fixed to a rigid assembly, their inertial velocities differ by `omega × r`, where `r` points from the reference to the sensor, angular velocity is in radians per second, and both vectors use the same frame. This is not the derivative of a constant body-frame offset. At 90 degrees per second, a sensor 0.20 m perpendicular to the rotation axis has about 0.31 m/s tangential speed. The [angular-velocity cross-product relation](https://modernrobotics.northwestern.edu/nu-gm-book-resource/3-2-2-angular-velocities/) supports this calculated pure-rotation example; it is not measured aircraft performance.

If that motion is interpreted as translation of the aircraft's reference point, the estimate can be wrong during turns. Offset support and the extent of compensation depend on the estimator. Measuring an offset does not ensure that a particular firmware consumes it.

Position/velocity compensation also does not imply complete accelerometer lever-arm compensation. ArduPilot's [offset documentation](https://ardupilot.org/copter/docs/common-sensor-offset-compensation.html#parameter-details) explicitly describes its IMU-offset correction as partial.

For a single beam over flat, level ground, simple geometry gives the sensor's vertical separation as `range * cos(tilt from vertical)`. Converting that to height at the aircraft reference point also requires the sensor lever arm and attitude. Sloping terrain and unexpected returns need a different assessment; a tilted range is not automatically height above ground at the aircraft origin.

## Boresight: which way the sensor looks

Boresight describes angular geometry. A camera can be at the correct measured position while looking a little sideways or downward relative to the expected direction.

At a plane perpendicular to the nominal viewing direction and 100 m away, a 1 degree pointing error moves the intersection by approximately `100 * tan(1 degree) = 1.75 m`. This is a simple calculated line-of-sight example, not a survey accuracy claim. Actual ground error also depends on geometry, terrain, position and attitude errors, timing and the sensor model.

Separate the nominal mount orientation from the residual misalignment. A downward-facing camera needs a large, intentional body-to-optical rotation before small alignment errors are considered. Do not enter a small boresight correction where software expects the complete sensor-to-body rotation.

For a moving gimbal, the body-to-camera transform varies with joint angles. Record the body-to-gimbal-base transform, joint conventions, gimbal-to-camera transform and measurement times. A static boresight fit describes only its stated fixed configuration.

Two cameras can have parallel viewing directions and still be separated by a baseline. That separation causes depth-dependent parallax: an overlay aligned at one distance can disagree at another. Check RGB/thermal or stereo alignment across the intended distance range; a single image shift does not describe the full geometry. The [ROS CameraInfo stereo model](https://docs.ros.org/en/jazzy/p/sensor_msgs/msg/CameraInfo.html) relates baseline to the projection matrix; aligned optical axes do not imply coincident projection centers.

## Timing is another calibration dimension

[claim:sensor-camera-imu-acquisition]

An image timestamp may refer to exposure start, exposure midpoint, a driver callback or arrival at a computer. Those events occur at different times. Record the event definition and clock for each stream. ROS [CameraInfo](https://docs.ros.org/en/jazzy/p/sensor_msgs/msg/CameraInfo.html) specifies image acquisition time, so receipt time should not silently stand in for it. Hardware triggers, PPS and clock synchronization have specific roles; none substitutes for checking the timestamp's event definition.

At 15 m/s, a 20 ms timing error corresponds to 0.30 m of travel. At 60 degrees per second, that interval corresponds to 1.2 degrees of rotation. These are separate constant-rate examples calculated as rate times duration. They illustrate why apparent position or boresight errors can come from timing.

A fitted constant time shift cannot establish that clocks stay synchronized, remove random jitter or describe every rolling-shutter row's exposure time. A rolling-shutter sensor exposes rows at different times; short exposure reduces blur but does not eliminate that row-to-row timing. [Basler's shutter documentation](https://docs.baslerweb.com/electronic-shutter-types) distinguishes exposure and readout timing. Inspect dropped samples, clock drift, restarts and buffering. See [Time and Coordinate Provenance](time-and-coordinate-provenance.md) for the accompanying record.

## What to calibrate, and in what order

Choose the model and capture procedure supported by the actual tool. Some solvers jointly estimate parameters; the sequence below is a way to organize prerequisites and evidence.

1. **Freeze and identify the installation.** Record sensor serials, mounts, lens settings, image dimensions, firmware, configuration and the intended use. Make bench motion checks with propulsion disabled and propellers removed.
2. **Check raw measurements and conventions.** Confirm axis direction, units, sample rates and timestamp meaning. Check the sensor's documented intrinsic prerequisites before estimating relationships between sensors.
3. **Calibrate the individual measurement model.** For a camera, estimate the appropriate intrinsics and distortion model at the recorded image geometry. A lens fit does not determine its position on the aircraft. [OpenCV's camera calibration tutorial](https://docs.opencv.org/4.13.0/dc/dbb/tutorial_py_calibration.html) distinguishes intrinsics from pose rotation and translation.
4. **Measure and estimate spatial relationships.** Record accessible lever arms, nominal orientation and uncertainties. Use a supported procedure to fit remaining extrinsics. Compare the result with the physical drawing. A plausible residual alone cannot resolve a reversed frame or an incorrect target scale.
5. **Establish timing.** Use the acquisition system's documented synchronization and event records, and estimate a residual offset only where supported. Keep the timing model with the spatial calibration.
6. **Check the fixed candidate using fresh data.** Exclude those observations from fitting, and compare against an independent reference appropriate to the intended use. If the check prompts a refit, capture another check set. Renaming or retimestamping training data does not make it fresh.
7. **Export, read back and validate the consumer.** Confirm units, frame directions, full coefficients and timing conventions survive conversion. Save the previous configuration. Check that the intended driver or estimator actually loaded the result before proceeding through the aircraft's commissioning procedure.

For camera acquisition, photograph the target **with the camera being calibrated**. Measure printed squares or displayed target scale physically; printer settings and screen pixels are not length standards. Keep the target flat, retain its border, and vary distance, position and tilt rather than repeatedly capturing the same centered view. Follow the chosen tool's required image counts and target type.

[Kalibr's target guidance](https://github.com/ethz-asl/kalibr/wiki/calibration-targets) calls for measured dimensions, flatness and a border. Square count and **inner-corner count** are different. Target scale also matters: in an ideal target-based pinhole pose solve, entering 20 mm for an actual 25 mm square scales the recovered translations to `20/25 = 0.8` of their true values while leaving the same image projections possible. This is a geometric example, not an accuracy prediction for a joint camera/IMU solver. OpenCV's [target-unit explanation](https://docs.opencv.org/4.13.0/dc/dbb/tutorial_py_calibration.html) explains why pose translations inherit the target's length units.

Camera/IMU recording needs informative motion around multiple axes as well as translation, with usable images and timestamps. A recording held still or moved only in one direction may leave parameters weakly observable. More frames of the same uninformative motion do not solve that problem. Kalibr's [acquisition guidance](https://github.com/ethz-asl/kalibr/wiki/camera-imu-calibration) explains these requirements for its solver. Depending on the selected IMU model, intrinsic corrections must be supplied or estimated jointly; a bias estimate alone is not a complete intrinsic calibration.

[claim:sensor-motion-observability]

Set acceptance criteria before fitting: for example, allowable image residuals across the field of view, independent position/angle discrepancies, timing behavior and repeatability over the intended operating conditions. Residuals, solver covariance and repeated-fit spread describe different things; none alone is a complete uncertainty bound or flight qualification.

## Where Sensor Calibration Lab fits

**Sensor Calibration Lab** is the local, hardware-neutral handbook companion. This capability summary is pinned to v0.3.0, commit `8db0394`, and was checked against its implementation on 18 October 2026. It describes these candidate-fitting and fresh-data checks:

| Workflow | Required input | Candidate result |
|---|---|---|
| Camera lens | Original photos, browser snapshots or target-corner recordings | Intrinsics and distortion, with a fresh-view check |
| Camera + IMU | Metric poses in one fixed target world, corrected gyro/specific-force samples, mapped capture clocks and a linked lens result | Relative rotation, spacing, biases and residual time shift, with a fresh-motion check |
| Optical flow | Gyro-compensated flow normalized to the declared XY convention; independently measured planar motion and normal distance | Full XY mapping and drift, with a fresh-window check |
| Camera rig | Synchronized target corners and linked lens results for 2–8 cameras | Relative transforms, baseline and optical boresight, with a fresh cross-camera check |

Use the workflow's input contract. A set of still photos does not supply camera/IMU timing; a browser snapshot time does not establish exposure time. The Lab does not directly record every flight controller or automatically turn arbitrary telemetry into calibration input. Standalone IMU intrinsic, compass, barometer, GNSS and rangefinder calibration are outside these workflows.

For the Lab's optical-flow fit, the input contract assumes a flat target normal to the optical axis and constant distance within each motion window. Raw MAVLink rotation-axis fields need an explicit conversion before import. The camera/IMU importer requires accelerometer **specific force**, including gravity response, rather than gravity-subtracted linear acceleration. Those are implemented input restrictions, not interchangeable sensor formats.

Keep the neutral result, original input, sensor/configuration record and fresh-check evidence together. Available destination exports include ROS camera calibration/static-transform templates and a version-specific monocular OpenVINS fragment where representable. Optical-flow output retains its full matrix; it is not an automatic firmware parameter mapping. Destination software behavior still needs checking.

Rig adjustment angles use the documented camera optical axes. They are not aircraft roll/pitch/yaw or gimbal actuator commands. Convert through the actual mount/joint model, then remeasure after adjustment.

The Lab applies no device settings. Accepted results retain physical verification, bench validation, hardware timing validation and flight qualification as unverified. A numerical check cannot establish those physical outcomes. Synthetic examples demonstrate software behavior and remain labeled synthetic.

The Orqa-focused **Prismo Calibration** app is a separate edition with its own setup and recording paths. Keep its instructions separate from the Lab's. Authorized local packages carry their installation instructions; the apps currently have private distribution, and the handbook's content license does not grant an app license.

## When the result looks wrong

These are diagnostic leads. Reproduce a symptom and inspect the underlying records before deciding its cause.

| Symptom | Possible causes | Next check |
|---|---|---|
| Estimated motion follows the wrong axis | Wrong frame, reversed transform or a rotation applied twice | Disarmed direction checks against the recorded frame drawing |
| Position disagreement grows during turns | Lever-arm error, timing error, flex or attitude error | Compare straight and rotating motion with timestamped reference data |
| Camera overlay fits at one distance only | Baseline/parallax, wrong intrinsics or an unsuitable overlay model | Check several known depths using the full camera relationship |
| Camera/IMU residuals grow with motion speed | Timestamp offset/jitter, blur, rolling shutter or mount movement | Exposure timing, sample intervals and image sharpness |
| Compass changes with electrical configuration | Magnetic interference or a changed installation | Manufacturer-approved interference checks and wiring review |
| Range disagrees as the aircraft tilts | Slant range treated as height, wrong orientation or an unexpected surface | Beam direction, target geometry and distance convention |
| Calibration passes its fit but fails new data | Weak coverage, overfitting, changed settings or an incomplete model | Fresh observations across the intended conditions |

## When to check it again

Revisit affected geometry after a sensor, bracket, antenna or gimbal is moved, a mount is repaired, or an impact may have changed alignment. Revisit camera intrinsics after changing lens, focus, zoom or image geometry. A known pure image rescale permits corresponding scaling of pixel intrinsics while retaining the distortion coefficients in the same model; an undocumented sensor mode, crop or changed optics needs separate assessment. [OpenCV's rescaling guidance](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) states the applicable model rule. Recheck timing after changing capture hardware, drivers, clocks or buffering. Compare results over relevant temperature and vibration conditions rather than assuming a room-temperature bench fit covers them.

[claim:sensor-lever-arm-remount]

Keep the old record and create a new configuration revision. A date alone does not identify which assembly a calibration belongs to. Use the [installation worksheet](../appendices/appendix-g-sensor-calibration-record.md), [preflight checks](../field/preflight.md) and [integration evidence record](../field/evidence-record.md) to retain the connection between installation, calibration, application and observed performance.

## Sources and scope

Primary documentation and the cited observability paper were read on **18 October 2026**. The linked conventions, vendor procedures and research conclusions apply within their stated models; they do not establish the performance of a particular aircraft. The diagrams and numerical examples are original instructional illustrations. App statements were checked against the pinned v0.3.0 source, including input validation, exports and result flags; public app distribution and physical qualification are not claimed.
