# Chapter 4: Link Budgets Without the Math

> A link budget tells you whether your radio link will work at a
> given distance. You don't need a calculator. You need to understand
> three numbers and three things that kill them.

---

## The Three Numbers

Every radio link has three numbers that determine whether it works:

### 1. Transmit Power (How loud you're shouting)

Measured in milliwatts (mW) or dBm. More power = more range,
up to a point.

| Power | dBm | Typical Use |
|-------|-----|-------------|
| 10 mW | 10 dBm | Bluetooth, low-power telemetry |
| 25 mW | 14 dBm | EU legal VTX limit, ELRS minimum |
| 100 mW | 20 dBm | Standard FPV, ELRS default |
| 250 mW | 24 dBm | Long-range FPV |
| 500 mW | 27 dBm | Extended range |
| 1000 mW (1W) | 30 dBm | FCC limit for most ISM, long-range telemetry |

**The key insight:** Doubling your power only gets you ~40% more
range (because radio signal falls off with the square of distance).
Going from 100 mW to 200 mW doesn't double your range — it adds
about 40%. Going from 100 mW to 1000 mW (10x power) roughly
triples your range. Power is an expensive way to buy range.

### 2. Receiver Sensitivity (How well you can hear a whisper)

Measured in dBm (negative numbers — more negative = more sensitive).
This is how faint a signal the receiver can still decode.

| Sensitivity | Typical Device |
|-------------|---------------|
| -90 dBm | Basic WiFi receiver |
| -105 dBm | Good telemetry radio (SiK) |
| -112 dBm | ELRS 2.4 GHz at 50 Hz |
| -117 dBm | ELRS 900 MHz at 25 Hz |
| -130 dBm | LoRa at lowest data rate |
| -148 dBm | Wio-SX1262 (absolute best available) |

**The key insight:** Receiver sensitivity improves when you lower
the data rate. ELRS at 500 Hz (fast, for racing) has worse
sensitivity than ELRS at 50 Hz (slow, for long range). This is
why long-range modes exist — they trade update rate for range.

### 3. Link Margin (How much room you have before it breaks)

Link margin = (transmit power + antenna gains) - (path loss) - (receiver sensitivity)

If the margin is positive, the link works. If it's negative, it doesn't.
The bigger the positive margin, the more resilient the link is to
fading, interference, and obstacles.

**Comfortable margins:**
- 10 dB: Works in clean conditions, fragile in the real world
- 20 dB: Handles moderate interference and some obstacles
- 30 dB+: Robust link, will survive urban environments and bad days

---

## The Three Things That Kill Links

### 1. Distance (Path Loss)

Radio signals get weaker with distance. In free space (no obstacles),
the signal drops by 6 dB every time you double the distance. That
means at twice the distance, you have one quarter the signal power.

**Free-space path loss at common frequencies:**

| Distance | 900 MHz | 2.4 GHz | 5.8 GHz |
|----------|---------|---------|---------|
| 100 m | -51 dB | -60 dB | -68 dB |
| 500 m | -65 dB | -74 dB | -82 dB |
| 1 km | -71 dB | -80 dB | -88 dB |
| 5 km | -85 dB | -94 dB | -102 dB |
| 10 km | -91 dB | -100 dB | -108 dB |

Read this table like this: at 1 km on 2.4 GHz, the signal is
80 dB weaker than when it left the transmitter. If you started
with 20 dBm (100 mW) transmit power and 0 dBi antennas, the
signal arriving at the receiver is 20 - 80 = -60 dBm. If your
receiver sensitivity is -112 dBm, your margin is 52 dB. Plenty.

At 10 km, the same setup gives you 20 - 100 = -80 dBm arriving
signal. Margin is 32 dB. Still fine in free space.

**But you're not in free space.**

### 2. Obstacles (The Real Range Killer)

Free-space path loss is the theoretical minimum. Everything else
makes it worse:

| Obstacle | Additional Loss |
|----------|----------------|
| Light foliage (few trees) | 3–10 dB |
| Dense forest | 15–30 dB |
| Single brick wall | 10–15 dB |
| Concrete building | 20–40 dB |
| Metal structure | 30–50+ dB |
| Hill / terrain (no line of sight) | 20–60+ dB |
| Rain (heavy, 5.8 GHz) | 1–3 dB per km |
| Humidity (negligible below 10 GHz) | < 1 dB per km |

**The single biggest factor in real-world range is line of sight.**
If you can see the other antenna, the link probably works. If you
can't, it might not. Every obstacle between the two antennas
subtracts from your margin.

This is why 900 MHz outperforms 2.4 GHz in obstructed environments
— lower frequencies diffract around obstacles better. A 900 MHz
signal bends around a tree that a 5.8 GHz signal bounces off of.

### 3. Interference (The Urban Tax)

Every other radio on your frequency subtracts from your link margin
by raising the noise floor. In a clean rural environment, the noise
floor might be -110 dBm. In a city, it could be -90 dBm. That's
20 dB of margin you just lost to other people's WiFi.

| Environment | Noise Floor (2.4 GHz) | Impact |
|-------------|----------------------|--------|
| Rural, no buildings | -105 to -110 dBm | Minimal — close to theoretical range |
| Suburban | -95 to -100 dBm | 10–15 dB lost to ambient noise |
| Urban | -85 to -95 dBm | 15–25 dB lost |
| Stadium / convention | -75 to -85 dBm | 25–35 dB lost — significant range reduction |
| Race event (many pilots) | -80 to -90 dBm | 20–30 dB lost on shared frequencies |

**The fix isn't more power** (that raises the noise floor for everyone).
The fix is:
- Different frequency band (if possible)
- More directional antennas (which reject interference from the sides)
- Lower data rate (which improves receiver sensitivity)
- Better antenna placement (which avoids self-interference)

---

## The No-Math Range Estimate

You don't need to calculate path loss. Use this:

**Step 1:** Find the manufacturer's claimed range for your radio link.

**Step 2:** Apply the environment factor:

| Environment | Multiply By |
|-------------|-------------|
| Open field, clear day, nobody else around | 0.7 |
| Suburban, some trees, moderate interference | 0.4 |
| Urban, buildings, heavy interference | 0.2 |
| Indoor or dense urban canyon | 0.1 |

**Step 3:** That's your expected range.

**Example:** ELRS 900 MHz at 100 mW claims 30 km range.
- Open field: 30 × 0.7 = 21 km. Reasonable.
- Suburban: 30 × 0.4 = 12 km. Realistic.
- Urban: 30 × 0.2 = 6 km. About right.
- These are LOS (line of sight) estimates. Flying behind a hill
  or building cuts range further.

---

## How Antennas Change the Budget

Antenna gain is free range. A 6 dBi antenna on the ground station
adds 6 dB of margin, which effectively doubles your range compared
to a 0 dBi antenna, without increasing power or changing anything
on the drone.

**Both ends count.** If you add 3 dBi on the drone antenna AND
3 dBi on the ground station antenna, you get 6 dB total improvement.
But adding gain on the ground station is usually easier (no weight
constraint, can use larger antennas, can use a tracker).

**The practical limit:** On the drone, you're limited to small,
lightweight, roughly omnidirectional antennas (2–5 dBi). On the
ground, you can use a directional patch (8–14 dBi) or helical
(10–16 dBi) on a tracker. The ground antenna is where you get
the most range improvement per dollar.

---

## Putting It Together: Example Link Budgets

### FPV Racing Quad (Short Range)

```
RC Link (ELRS 2.4 GHz, 250 mW, 500 Hz):
  TX power:            24 dBm
  TX antenna:          2 dBi (dipole on drone)
  RX antenna:          2 dBi (dipole on TX)
  Path loss at 500m:  -74 dB
  Arriving signal:     24 + 2 + 2 - 74 = -46 dBm
  RX sensitivity:     -108 dBm (ELRS 500 Hz)
  Margin:              62 dB  ← massive, no problems
```

Racing at 500m with ELRS has 62 dB of margin. You could fly
behind buildings and through moderate obstacles and still be fine.
RC is not your range bottleneck.

```
Video Link (Analog 5.8 GHz, 400 mW):
  TX power:            26 dBm
  TX antenna:          2 dBi (pagoda)
  RX antenna:          2 dBi (pagoda on goggles)
  Path loss at 500m:  -82 dB
  Arriving signal:     26 + 2 + 2 - 82 = -52 dBm
  RX sensitivity:     -85 dBm (analog threshold for usable image)
  Margin:              33 dB  ← healthy
```

At 500m, analog video has 33 dB of margin. At 2 km it drops to
about 21 dB. At 5 km, about 7 dB — you'll see static. Video is
always the range bottleneck on an FPV quad, not RC.

### Long-Range Survey (5 km)

```
Telemetry (RFD900x, 1W, 900 MHz):
  TX power:            30 dBm
  TX antenna:          3 dBi (dipole on drone)
  RX antenna:          6 dBi (directional on GCS)
  Path loss at 5 km:  -85 dB
  Arriving signal:     30 + 3 + 6 - 85 = -46 dBm
  RX sensitivity:     -121 dBm (SiK at 64 kbps)
  Margin:              75 dB  ← enormous
```

RFD900x at 5 km in open terrain has 75 dB of margin. Even in
heavy suburban with 25 dB noise floor elevation and 15 dB of
foliage, you still have 35 dB of margin. This is why RFD900x
is the standard for long-range telemetry.

---

## Quick Reference: What Uses Your Margin

| Factor | Typical Impact |
|--------|---------------|
| Double the distance | -6 dB |
| Light foliage in path | -5 to -10 dB |
| One building wall | -10 to -15 dB |
| Urban noise floor (2.4 GHz) | -15 to -25 dB |
| Cross-polarized antennas | -20 dB |
| Antenna connector loss (each) | -0.5 to -1 dB |
| Coax cable loss (per meter) | -0.5 to -2 dB (frequency dependent) |
| **Add 6 dBi ground station antenna** | **+6 dB** |
| **Switch from 2.4 to 900 MHz** | **+8 dB at same distance** |
| **Lower ELRS packet rate by half** | **+3 dB sensitivity** |

---

## Next

- **Chapter 3: Antennas** — how antenna gain and placement
  affect these numbers.
- **Chapter 1: The Five Link Types** — which links are range-limited
  and which aren't.

---

*Range is not a single number. It depends on what's between you
and the drone. The link budget tells you how much you can afford
to lose before the link breaks.*
