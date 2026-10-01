# Chapter 4: Link Budgets with Evidence

> **Updated:** October 1, 2026. A free-space reference model with explicit inputs; not a guaranteed operating range.

Use the [RF calculator](/reference.html#calculate) to enter a configuration and export the result, working, sources, and publication release.

## Describe your configuration

Record hardware and firmware revisions, frequency, packet/data mode, antennas, cables, connectors, and geometry. The receiver threshold must apply to that configuration. Unknown sensitivity remains unknown.

## Convert transmit power

dBm = 10 log10(P_mW). These are mathematical conversions, not permitted-power limits or recommended settings.

| Power | dBm | Evidence |
|---|---|---|
| 1 mW | 0.00 | [claim:rf-power-1] |
| 10 mW | 10.00 | [claim:rf-power-10] |
| 25 mW | 13.98 | [claim:rf-power-25] |
| 100 mW | 20.00 | [claim:rf-power-100] |
| 250 mW | 23.98 | [claim:rf-power-250] |
| 500 mW | 26.99 | [claim:rf-power-500] |
| 1000 mW | 30.00 | [claim:rf-power-1000] |

## Calculate free-space loss

ITU-R P.525-5 Annex section 2.3 gives the practical rounded form:

```text
FSPL_dB = 32.4 + 20 log10(frequency_MHz) + 20 log10(distance_km)
```

The table below is derived from that formula. Path loss is positive and subtracted from the budget. These values do not include obstructions, polarization mismatch, multipath, measured cable losses or interference.

| Distance | Frequency | Calculated loss | Evidence |
|---|---|---|---|
| 0.1 km | 900 MHz | 71.48 dB | [claim:rf-fspl-0p1-900] |
| 0.1 km | 2400 MHz | 80.00 dB | [claim:rf-fspl-0p1-2400] |
| 0.1 km | 5800 MHz | 87.67 dB | [claim:rf-fspl-0p1-5800] |
| 0.5 km | 900 MHz | 85.46 dB | [claim:rf-fspl-0p5-900] |
| 0.5 km | 2400 MHz | 93.98 dB | [claim:rf-fspl-0p5-2400] |
| 0.5 km | 5800 MHz | 101.65 dB | [claim:rf-fspl-0p5-5800] |
| 1 km | 900 MHz | 91.48 dB | [claim:rf-fspl-1-900] |
| 1 km | 2400 MHz | 100.00 dB | [claim:rf-fspl-1-2400] |
| 1 km | 5800 MHz | 107.67 dB | [claim:rf-fspl-1-5800] |
| 5 km | 900 MHz | 105.46 dB | [claim:rf-fspl-5-900] |
| 5 km | 2400 MHz | 113.98 dB | [claim:rf-fspl-5-2400] |
| 5 km | 5800 MHz | 121.65 dB | [claim:rf-fspl-5-5800] |
| 10 km | 900 MHz | 111.48 dB | [claim:rf-fspl-10-900] |
| 10 km | 2400 MHz | 120.00 dB | [claim:rf-fspl-10-2400] |
| 10 km | 5800 MHz | 127.67 dB | [claim:rf-fspl-10-5800] |

[claim:rf-distance-double]

## Received power and margin

```text
Received_dBm = TX_dBm + TX_gain_dBi + RX_gain_dBi - FSPL_dB - other_losses_dB
Margin_dB = Received_dBm - receiver_threshold_dBm
```

A positive margin says only that modeled received power exceeds your supplied threshold. It does not establish reliable connectivity, acceptable latency, permitted operation or aircraft authority. Unknown losses or an inappropriate threshold can dominate the answer.

[claim:rf-budget-example]

## Replace range shortcuts with evidence

The former fixed environment multipliers were not supported by a documented test method or configuration and have been withdrawn. Generic device sensitivities, obstacle-loss allowances, noise floors and legal-power labels were also removed pending configuration-specific sources.

Use Report / add field evidence to contribute a measurement. Include equipment and revisions, firmware/mode, antennas and placement, distance and geometry, date, conditions, measurement method and units, and uncertainty. A result applies to its recorded setup rather than every device in its band.

Keep measured losses separate from estimates. A noise-floor increase is not a universal subtraction from sensitivity; assess the receiver, bandwidth and measurement method.

## Correction record

Proposed October 1 rewrite: unsupported range multipliers and categorical range conclusions withdrawn; configurable thresholds; explicit loss signs; sourced formula-derived tables. Publication remains subject to review.
