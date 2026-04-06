# EW Countermeasures Field Card

> You're flying and something goes wrong with the link. This card tells you
> what's happening, why, and what to do about it — in the order you need to
> do it. Not theory. Not a procurement guide. A decision tree for when
> you're being jammed and you have seconds to act.

**Format:** Print this. Laminate it. Keep it in your kit.
**Cross-references:** [Electronic Warfare](../components/electronic-warfare.md) ·
[Military Firmware Forks](../components/military-firmware-forks.md) ·
[CRSF & ELRS Protocol](../firmware/crsf-elrs-protocol.md) ·
[Video Transmitters](../components/video-transmitters-vtx.md) ·
[Frequency Bands](../fundamentals/frequency-bands.md) ·
[Troubleshooting](troubleshooting.md)

---

## Symptom → Cause → Action

### 1. VIDEO FREEZES OR BREAKS UP — CONTROL STILL WORKS

**What's happening:** Your video link is being jammed but your control link
is still intact. This is the most common jamming scenario since summer 2024.
Video is the easiest link to disrupt because analog video is unencrypted and
operates on well-known 5.8 GHz channels.

**Immediate actions:**

1. **Do NOT panic-stick.** You still have control. The drone is flying fine,
   you just can't see. Hold current heading and altitude.
2. **Check OSD** — if OSD elements are still rendering but the camera image
   is gone, the VTX is still transmitting but the camera feed is being
   overwhelmed. If the entire image including OSD is gone, the VTX link
   is disrupted.
3. **Switch VTX channel** — if your firmware supports armed VTX switching
   (MILBETA does, stock Betaflight does not), change to a channel outside
   the jammer's band. Move from Raceband to Band A or Band E. If running
   non-standard frequencies (1.2 GHz, 7.2 GHz), you're likely already
   outside jammer coverage.
4. **Increase VTX power** — if you pre-configured power ramp, push to max.
   More power doesn't beat a jammer but it improves signal-to-noise at
   the receiver (your goggles), buying marginal range.
5. **RTH or manual return** — if video doesn't recover in 3–5 seconds, use
   control link to bring the drone back. If GPS-equipped, trigger RTH. If
   not, use compass heading and timer to dead-reckon back.

**Pre-mission setup:**

- Pre-program 2–3 VTX channels across different bands in your VTX table
- Enable armed VTX switching if firmware supports it
- Set VTX power to auto-ramp (low on ground, max in air)
- Know your return heading before launch

---

### 2. LINK QUALITY (LQ) DROPPING — VIDEO STILL WORKS

**What's happening:** Your control link is being targeted. The jammer is
operating on your RC frequency band (900 MHz or 2.4 GHz for ELRS/CRSF,
433 MHz for some MafiaLRS configs). LQ below 70 means packets are being
lost. Below 50 is danger. At 0 you hit failsafe.

**Immediate actions:**

1. **Check LQ trend** — is it dropping steadily (getting closer to jammer)
   or spiking (intermittent interference)? Steady drop = turn around now.
   Spikes = you may be able to push through.
2. **Reduce range** — turn toward home. Every meter closer to your TX
   improves your link budget relative to the jammer.
3. **Check RSSI** — if RSSI is strong but LQ is low, you're being jammed
   (strong signal received but packets corrupted). If both RSSI and LQ are
   low, you're at range limit, not being jammed.
4. **Switch packet rate** — if running ELRS at 250/500 Hz, drop to 50/100 Hz.
   Lower rates have better range because the receiver has more time to
   accumulate signal energy. This is the single most effective countermeasure
   for control link jamming.
5. **Switch bands** — if running MILELRS with multiband, switch from the
   jammed band (e.g., 2.4 GHz) to the alternate (e.g., 900 MHz). If
   running MafiaLRS on 433 MHz, you're already on a band most jammers
   don't cover.

**Pre-mission setup:**

- Set failsafe to GPS RTH (not drop or land-in-place)
- Configure failsafe stage 1 timeout to at least 5 seconds (MILBETA: set
  to 0.5 in configurator for 5 real seconds due to 10x multiplier)
- Pre-configure rate switching on a TX switch (high rate for close, low
  rate for far)
- If MILELRS: verify multiband binding is active

---

### 3. GPS DRIFTING OR TOILET-BOWLING

**What's happening:** GPS/GLONASS signals are being jammed or spoofed.
Jamming causes position uncertainty (toilet-bowl effect, position hold
wandering). Spoofing feeds false coordinates — the drone thinks it's
somewhere else and may fly toward the spoofed position.

**Immediate actions:**

1. **Switch to ACRO or ANGLE mode** — remove GPS from the control loop
   immediately. The drone will fly on gyro/accelerometer only. You maintain
   manual control.
2. **Do NOT trust RTH** — if GPS is compromised, RTH will fly to the wrong
   position. Spoofed GPS can send your drone into enemy territory.
3. **Check sat count on OSD** — sudden drop from 12+ sats to 3–4 indicates
   jamming. Sat count staying high but position jumping indicates spoofing.
4. **Use visual landmarks and compass heading** — fly back by line of sight
   or dead reckoning. If compass is also affected (it can be by strong
   magnetic interference from some jammers), use known terrain features.
5. **Land as soon as practical** — GPS jamming is usually area-denial. The
   jammer wants to keep drones out of a zone. Don't fight it. Get your
   drone back and reassess.

**Pre-mission setup:**

- Always have a non-GPS flight mode mapped to a switch (ACRO or ANGLE)
- Know your return heading by compass before every launch
- Set OSD to display heading, sat count, and distance-to-home
- If available, configure dual GNSS (GPS + GLONASS + Galileo + BeiDou)
  for redundancy — harder to jam all constellations simultaneously
- Consider INS/visual odometry if platform supports it (VOXL 2, etc.)

---

### 4. TOTAL BLACKOUT — NO VIDEO, NO CONTROL

**What's happening:** Broadband jamming is hitting everything — control,
video, GPS. Alternatively, your drone flew into a high-power EW bubble
(vehicle-mounted jammer, fixed installation). This is the worst case.

**What happens next depends entirely on your failsafe configuration:**

- **GPS RTH failsafe:** drone climbs to failsafe altitude and attempts
  to return. May work if the jammer's coverage has a ceiling. May not
  work if GPS is also jammed.
- **Land-in-place failsafe:** drone descends and lands wherever it is.
  You lose the drone but it doesn't fly into hostile territory.
- **MILBETA extended failsafe:** drone continues at full throttle for the
  configured time (up to 200 seconds actual), giving it time to exit the
  EW bubble before triggering stage 2.
- **No failsafe configured:** drone falls out of the sky. Total loss.

**You cannot do anything in real-time during a total blackout.** This is
won or lost before launch based on failsafe configuration.

**Pre-mission setup:**

- **This is the most important section in this card.** Configure failsafe
  before every mission.
- GPS RTH with a sensible altitude (high enough to clear terrain, low
  enough to stay under EW ceiling)
- Stage 1 timeout: 5–10 seconds minimum (gives the drone time to exit
  an EW bubble in transit)
- Stage 2 action: GPS RTH if GPS is trusted, land-in-place if operating
  in a spoofing environment
- MILBETA users: extended failsafe with full throttle toward home heading
  before triggering stage 2

---

### 5. OSD SHOWS EW DIRECTION / LQ BY FREQUENCY

**This requires MILELRS + MILBETA.**

MILBETA function 3 displays the direction and strength of detected EW
sources on the OSD. Function 6 displays LQ statistics broken down by
frequency band (12 bands).

**How to read it:**

- **EW direction indicator** — shows bearing to the strongest jamming
  source relative to your heading. Fly perpendicular to or away from
  this bearing.
- **Per-band LQ** — identifies which specific frequency bands are being
  jammed. If 900 MHz shows LQ 20 but 2.4 GHz shows LQ 95, switch to
  2.4 GHz. If both are degraded, reduce range.
- **Trend over time** — LQ improving as you fly = moving away from jammer.
  LQ worsening = moving toward it. Use this to map the EW bubble's
  boundary.

**Tactical use:**

This data is what enables EW hunter-killer operations. If you can see the
jammer's direction on OSD, you can fly toward it. The FPV_VYZOV ecosystem
uses exactly this capability to target and destroy enemy EW assets. Whether
you're hunting the jammer or avoiding it depends on your mission.

---

## Pre-Mission Checklist: EW Preparedness

Before every flight in a contested or potentially contested environment:

- [ ] Failsafe configured and tested (GPS RTH or controlled descent)
- [ ] Failsafe stage 1 timeout set (5+ seconds)
- [ ] Non-GPS flight mode mapped to switch (ACRO or ANGLE)
- [ ] Return heading noted (compass bearing to home)
- [ ] VTX channel list pre-programmed (2–3 channels across different bands)
- [ ] VTX power set to auto-ramp or manually set to mission-appropriate level
- [ ] ELRS packet rate switch configured (high rate / low rate toggle)
- [ ] OSD displaying: LQ, RSSI, sat count, heading, distance-to-home, battery
- [ ] If MILELRS: multiband active, TX key verified
- [ ] If MILBETA: EW overlay enabled (functions 3 and 6)
- [ ] Battery charged to mission profile (enough for RTH from furthest point)

---

## Jammer Types You'll Encounter

| Type | Targets | Range | Indicator |
|------|---------|-------|-----------|
| Handheld gun jammer | RC + video, directional | 500 m – 2 km | Sudden LQ drop when pointed at you |
| Vehicle-mounted | RC + video + GPS, broadband | 2 – 10 km | Area-denial, all links degrade in a zone |
| Fixed installation | Everything, high power | 10 – 50+ km | Persistent dead zone, known locations |
| GPS spoofer | Navigation only | 5 – 30 km | Position jumps, sat count stays high |
| Video interceptor | Passive (listens, doesn't jam) | 1 – 4 km | No indication — they see your feed silently |

**Key insight:** a video interceptor (Chuyka 3.0 and similar) does NOT jam
your video. It passively receives your analog video feed. You will have no
indication you're being watched. The only countermeasure is encrypted digital
video or fiber optic.

---

## The Five Layers of Video Survivability

From the VTX chapter, summarized here for field reference:

1. **Frequency diversification** — don't use standard 5.8 GHz Raceband
2. **Power management** — minimum necessary to reduce detectability
3. **Digital encryption** — DJI, Walksnail encrypt the feed
4. **FHSS / spread spectrum** — Barvinok-5 style, very hard to jam
5. **Fiber optic** — immune to all RF jamming, limited by cable weight/range

Each layer adds cost, weight, or complexity. Match to threat level.

---

## Sources

- Armada International, "Jamming UAV Video Signals" (Feb 2026)
- Cyber Shafarat, MILELRS/MILBETA capability documentation
- Advances in Military Technology Vol. 20 No. 2, counter-FPV tactics
- Endoacustica, FPV Drone Tactics & Countermeasures
- VGI-9, "Drones vs Electronic Warfare" (Jun 2025)
- Ukrainian EW Demo Day "EW vs FPV" (Oct 2024, 45 teams tested)
- Field experience documentation, Wild Hornets, TAF Industries
