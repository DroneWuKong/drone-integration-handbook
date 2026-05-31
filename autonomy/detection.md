# Detection: RF and Visual

Detecting a drone — yours, a swarm-mate, or a threat — happens in two
independent modalities. They fail in different conditions, which is exactly why
you want both.

## RF detection (passive)

Every drone radiates: a control link, a video downlink, telemetry, sometimes a
GPS-denied mesh. A passive RF detector listens for those emissions. Passive
means it transmits nothing — no probe requests, no giveaway — which matters on
patrol.

What you match on:

| Layer | Signal | Notes |
|---|---|---|
| Control link | 2.4 GHz / 900 MHz / 5.8 GHz FHSS, ELRS, Crossfire | narrowband, hopping |
| Video | analog 5.8 GHz, DJI OcuSync, WiFi | wideband |
| Consumer drones | 2.4 GHz WiFi-class (Parrot, DJI Phantom) | wideband, from the DroneRF dataset |
| MANET / mesh | Doodle Labs, Silvus, Persistent Wave Relay | tactical |

The DroneRF dataset (CC BY 4.0) provides labeled 2.4 GHz signatures for three
consumer drones — the starting point for a consumer-drone detector. Tactical and
military C2 signatures are a separate, narrowband problem.

**Failure modes.** RF detection needs a signature it recognizes — a genuinely
new emitter is invisible until learned. Wideband WiFi-class signatures and
narrowband FHSS C2 are different detection problems; a detector tuned for one
will miss the other. And the RF environment is crowded: telling a drone control
link from a WiFi access point is the hard part, not seeing energy.

## Visual detection

A camera plus a detector model finds drones as small objects against sky or
clutter. The datasets are permissively licensed and ready (Seraphim CC BY 4.0,
pathikg MIT — see [Datasets](datasets.md)).

**Failure modes.** The signature failure of visual detection is the **bird**.
Small, fast, erratic, and everywhere — birds are the dominant false positive for
any sky-facing drone detector, which is why the bird-vs-drone discrimination
problem has its own datasets. Visual also needs line of sight and light; it is
blind at night, in fog, and behind terrain — precisely where RF still hears.

## Why both

| Condition | RF | Visual |
|---|---|---|
| Night / fog | hears | blind |
| RF-silent drone (wired/autonomous) | deaf | sees |
| New/unknown emitter | misses | may still see |
| Bird vs drone | not fooled (no RF) | fooled |

The modalities cover each other's blind spots. A serious detection posture fuses
them rather than betting on one.

## Detection feeds navigation

The same passive RF detector that finds threats can also *position* the
aircraft: a recognized, known-location emitter is a coarse navigation anchor
when GPS is denied (see [Perception](perception.md)). One payload, two jobs —
threat sensing and a denial-resilient position fix.

---

*"We didn't detect it" almost always means "we weren't listening on that
modality." Birds will teach you humility; RF silence will teach you the rest.*
