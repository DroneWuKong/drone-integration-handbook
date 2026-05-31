# Onboard AI & Control

Perception tells the drone where it is and what is around it. This chapter is
about what it does next — the decision and control layer — and the one rule that
keeps autonomy from being a liability: **act on your confidence, not just your
estimate.**

## The layers above perception

| Layer | Job |
|---|---|
| State estimation | where am I (see [Perception](perception.md)) |
| Detection | what is around me (see [Detection](detection.md)) |
| Planning | what path achieves the goal while avoiding obstacles |
| Control | track that path on this airframe |
| Decision / authority | how much autonomy to permit *right now* |

The first four are well-trodden — sampling planners, MPC and LQR control, behavior
trees. The last one is where contested-environment autonomy lives or dies.

## Confidence-driven authority

Autonomy should not silently degrade when its inputs do. It should *know* its
inputs degraded and *change behavior* accordingly. Tie the authority level to the
navigation confidence:

| Nav confidence | Posture |
|---|---|
| GPS-like (σ < 5 m) | full autonomy permitted |
| Aided (5–25 m) | autonomy allowed; widen margins, reduce speed |
| Coarse / RF-anchored (25–100 m) | conservative behaviors; bias to loiter / return |
| Dead-reckoning (≥ 100 m) | hand back / hold / pre-planned safe action |

This only works if confidence is honest (a filter that lies about its
uncertainty defeats the whole ladder) and **visible to the operator**. A pilot
who cannot tell that navigation is estimated rather than fixed cannot make the
call the autonomy is deferring to them.

## What contested environments add

Most autonomy research assumes a benign RF environment, a single platform, and
clean GPS. Operationally none of that holds:

- **EW-aware behavior.** Jamming and spoofing are the baseline. Planning that
  ignores the RF picture will fly into a denial zone and lose its links;
  planning that uses it can route around jammers and minimize its own
  detectability.
- **Capability-aware autonomy.** The stack should adapt to whatever sensors the
  airframe actually carries — camera, LiDAR, RF detector, or none — rather than
  assume a fixed suite.
- **Graceful degradation, not failure.** The goal is not "never lose GPS." It is
  to lose it and keep flying a known, bounded, operator-visible solution.

## The failure mode

The single most dangerous autonomy bug is **trusted overconfidence**: the system
acts with full authority on a position it should not trust, because nothing in
the loop is watching its confidence. Every layer above perception inherits the
uncertainty from below. Carry it forward, gate authority on it, and show it to
the human. Autonomy is only trustworthy when its doubt is legible.

---

*An autonomous drone that cannot say "I am not sure" is not advanced — it is
unsupervised. The competent version knows when to ask for help.*
