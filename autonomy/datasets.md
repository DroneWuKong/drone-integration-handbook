# Datasets & Benchmarks for Drone Autonomy

The data you train and test autonomy on decides what it can do — and the
*license* on that data decides what you may ship. This chapter is a working
catalog of the public datasets relevant to drone perception, detection, and
state estimation, with the one thing most lists leave out: whether you can
actually use it.

The machine-readable version is published at
`dronewukong.github.io/forge-data/autonomy/datasets.json` (filterable by task,
license class, and verdict).

## The license trap — read this first

A dataset being public does **not** mean you can put it in a product. Three
buckets matter:

| License class | Examples | What you may do |
|---|---|---|
| Permissive | CC BY 4.0, MIT, Apache-2.0 | Use in products; just attribute |
| Non-commercial | CC BY-**NC**-SA | **Research only.** Not in anything you sell |
| Unconfirmed / closed | "see Kaggle page", ToS-only, no license | Assume nothing; confirm before use |

The failure mode is real: teams train a shippable model on a `CC BY-NC-SA`
benchmark, then can't legally ship it. Check the license before you download,
not after you've built on it.

## VIO / SLAM benchmarks (state estimation)

| Dataset | Content | License | Use |
|---|---|---|---|
| UZH-FPV | Real FPV racing: camera + IMU + event camera + Leica ground truth, to 100 km/h | CC BY-NC-SA 3.0 | research only |
| Mid-Air | Synthetic low-altitude: 420k frames, RGB + depth/semantics + IMU/GPS, 7 climates | CC BY-NC-SA 4.0 | research only |
| EuRoC MAV | Indoor MAV, stereo + IMU + Vicon/Leica ground truth | CC BY (per-sequence) | check sequence |

Both UZH-FPV and Mid-Air are non-commercial: excellent for *evaluating* a
GPS-denied estimator (see [Perception](perception.md)), off-limits for product
data. Ground truth from any of these projects into a common `t,x,y,vx,vy` form
and you can replay it through an estimator without the raw imagery.

## Computer-vision detection (drone / counter-UAS)

| Dataset | Content | License |
|---|---|---|
| Seraphim | 83k YOLO images, single "drone" class, curated from 23 sets | CC BY 4.0 |
| pathikg | 54k COCO images, drone class, from video frames | MIT |
| Maciullo DroneDetectionDataset | 51k+5k images (the upstream of pathikg) | MIT (labels) |
| Birds vs Drone | bird/drone discrimination — the real C-UAS false-positive problem | unconfirmed |

Seraphim and pathikg are permissively licensed and are a ready training base for
a visual drone detector. Note Maciullo is the *original* of the pathikg set —
de-duplicate or you will train and test on the same frames.

## RF signature data

| Dataset | Content | License |
|---|---|---|
| DroneRF | 3 consumer drones (Parrot Bebop, AR 2.0, DJI Phantom 3) across 2.4 GHz ISM | CC BY 4.0 |

See [Detection](detection.md) for how RF signatures are used.

## Adjacent — not drone detection

| Dataset | What it actually is |
|---|---|
| LADD (Lacmus) | Search-and-rescue: detects *people* from drone imagery, not drones |

Listed because it is commonly mis-filed under "drone datasets." Useful only if
you are building person-detection for SAR.

## Discovery, not datasets

Google Dataset Search and Roboflow Universe (`class:drone`) are *indexes*, not
datasets — each hit needs its own license check. DTIC (`discover.dtic.mil`) is a
public-domain source of UAS technical reports, not training data, but it is the
best open well for program and counter-UAS doctrine.

---

*A dataset with no stated license is not "free" — it is unresolved. Treat it as
unusable until someone confirms otherwise.*
