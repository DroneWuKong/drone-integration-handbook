# Perception: VIO, SLAM & GPS-Denied State Estimation

GPS denial is the operational baseline in contested airspace — jammed,
spoofed, or simply unavailable. When it happens, the drone still has to know
where it is. This chapter is about how, and where the common answers break.

## Two kinds of position fix

Every GPS-denied method is one of two types, and the distinction is everything:

| Type | Examples | Strength | Failure mode |
|---|---|---|---|
| **Relative** | VIO, LIO, IMU dead-reckoning | smooth, high-rate, locally accurate | **drifts** — error grows without bound |
| **Absolute** | visual georegistration (cam → satellite/DEM), RF anchors | no accumulation; bounds drift | intermittent, coarse, or condition-dependent |

Relative methods answer "how have I moved since the last fix." Absolute methods
answer "where am I, full stop." You need both: relative for smooth high-rate
motion, absolute to stop the relative drift from running away.

## Why VIO drifts

Visual-inertial odometry fuses a camera and an IMU. It is the workhorse of
GPS-denied flight and it is genuinely good — locally. But it integrates velocity
to get position, and any small, slowly-varying bias in that velocity integrates
into a position error that **only grows**. Over a long denial, metres become
tens of metres become hundreds.

The dangerous part is not the drift — it is that a naive filter does not *know*
it is drifting. Its reported uncertainty can stay small (falsely confident)
while the true error climbs. Model the velocity bias as a state and the
uncertainty grows honestly when there is nothing to correct it; skip that and
the operator gets a green light over a wrong position.

## How absolute fixes bound it

- **Visual georegistration** matches the onboard camera (including thermal) to
  satellite/aerial reference maps plus terrain (DEM) for an *absolute* position
  that does not accumulate. It needs texture, a map, and adequate light — so it
  is intermittent, but each fix resets the drift.
- **RF anchors** (signals-of-opportunity): recognizing a known-location emitter
  bounds you to its coverage region. Coarse (accuracy ≈ emitter spacing) but it
  works at night and in featureless terrain where vision fails. See
  [Detection](detection.md).
- **IMU dead-reckoning** is the floor — always available, drifts in seconds,
  buys time when everything else is gone.

Stack them on a degradation ladder: absolute fixes bound VIO; the coarse
fallbacks catch what is left.

## The failure modes that bite

- **Trusting VIO over a long denial.** It is locally smooth and looks healthy
  right up until the accumulated drift puts you somewhere you are not.
- **Overconfident covariance.** A filter that under-reports its own uncertainty
  will reject the very fix that would correct it (its innovation looks like an
  outlier). Recovery after a long drift needs an adaptive gate, not a fixed one.
- **Coarse anchors applied to a confident estimate.** A 50–100 m RF anchor used
  when you already know your position to a few metres pulls you *off*. Only fuse
  a coarse, biased anchor when you are more lost than the anchor is coarse.

## Benchmarks

Evaluate estimators against ground truth before trusting them in the field.
UZH-FPV (aggressive, real) and Mid-Air (synthetic, multi-climate) are the
standard public benchmarks — both non-commercial, so for *research* evaluation
only (see [Datasets](datasets.md)). Project their ground truth into a common
`t,x,y,vx,vy` trace and replay it through your estimator; the result tells you
how far you drift through a denial window and whether your confidence is honest.

---

*Position is not a number, it is a number with an uncertainty. An autonomy
stack that ignores the second half will eventually fly the first half into the
ground.*
