# Chapter 4: Link Budgets with Evidence

> **Updated:** October 1, 2026. A free-space reference model with explicit inputs; not a guaranteed operating range.

Use the [RF calculator](/reference.html#calculate) to enter a configuration and export the result, working, sources, and publication release.

## Describe your configuration

Record hardware and firmware revisions, frequency, packet/data mode, antennas, cables, connectors, and geometry. The receiver threshold must apply to that configuration. Unknown sensitivity remains unknown.

## Convert transmit power

dBm = 10 log10(P_mW). These are mathematical conversions, not permitted-power limits or recommended settings.

[table:rf-power]

## Calculate free-space loss

ITU-R P.525-5 Annex section 2.3 gives the practical rounded form:

```text
FSPL_dB = 32.4 + 20 log10(frequency_MHz) + 20 log10(distance_km)
```

The table below is derived from that formula. Path loss is positive and subtracted from the budget. These values do not include obstructions, polarization mismatch, multipath, measured cable losses or interference.

[table:rf-fspl]

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
