# AI-Assisted PID Tuning â Wingman Integration

> PID tuning used to mean hours of test flights and incremental adjustments.
> AI-assisted tuning compresses that cycle by reading your blackbox data
> and generating specific recommendations before you fly.

---

## The Workflow

1. **Upload your blackbox log** â one upload feeds all analysis tools
2. **Spectral Analysis** â FFT identifies noise peaks and motor Harmonics
3. **AI Tune Advisor** â synthesizes log data + current PIDs into specific recommendations
4. **Apply and iterate** â implement, fly, re-upload

---

## Uploading Blackbox Data

A single upload zone in the sidebar feeds all analysis panels.

**Accepted formats:**
- `.bbl` - Raw Betaflight blackbox binary
- `.bfl` - Betaflight log alternate extension
- `.csv` - CSV export from Betaflight Blackbox Explorer
- `.txt` - Plain text gyro values

**Recommended workflow:** Fly with blackbox enabled â pull SD card â open in Betaflight Blackbox Explorer â export as CSV â upload

---

## Spectral Analysis - Reading the FFT

**Motor harmonics:** A 1950KV motor on 4S at 50% throttle:
- 1x harmonic: ~180Hz
- 2x: ~360Hz
- 3x: ~540Hz

Enable RPM filtering (BLHeli_32 or AM32 with bidirectional DSHOT) to notch precisely.

**Propwash:** 20-100Hz range. Address with D-term and FF tuning.

**Frame resonance:** 100-250Hz. Dynamic notch filters target this range.

---

## AI Tune Advisor

When you send a message, the AI receives your blackbox summary, current PIDs, quad class, RPM filter status, and FC type.

Example: User reports hot motors + propwash. AI sees 180Hz dominant peak with RPM filtering enabled and recommends: D:30 -> 22, I:80 -> 90.

---

## Data Pipeline

Anonymized session data (filename hash, sample count, FFT peaks, PIDs, quad class) is stored locally in `wingman_bbx_pipeline`. This data builds platform-specific PID baselines over time.

---

## Starting Points by Quad Class

| Class | P | I | D | FF |
|-------|---|---|---|----|
| 5" Freestyle | 45 | 80 | 30 | 120 |
| 5" Racing | 52 | 88 | 35 | 130 |
| 3" Cinewhoop | 38 | 72 | 22 | 90 |
| 7" Long Range | 35 | 70 | 20 | 100 |
| Tiny Whoop | 65 | 95 | 45 | 60 |
| 8-10" Cinelifter | 28 | 65 | 18 | 80 |

---

## Related

- [Blackbox Logs](blackbox.md)
- [The Four Firmwares](../firmware/four-firmwares.md)
- [Orqa Hardware Guide](../components/orqa-hardware-guide.md)
- [Forge PID Tuning Tool](https://forgeprole.netlify.app/pid-tuning/)
