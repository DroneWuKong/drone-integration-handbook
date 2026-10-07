# Appendix A — Frequency Planning Quick Reference

This card supports planning and calculations. It is not a frequency authorization, equipment certification or guaranteed-range table. Use the current [regulatory resources](appendix-f-regulatory-resources.md) and [frequency planning worksheet](../field/frequency-planning.md).

## Record before selecting a channel

| Item | Required record |
|---|---|
| Jurisdiction and authority | Applicable rules, license/authorization, current equipment approval and permitted operating mode |
| Equipment | Exact radio/adapter revision, firmware, antennas and configured power |
| Occupied spectrum | Center frequency, bandwidth, harmonics and all co-located transmitters |
| Separation test | Receiver filtering, near/far geometry, antenna isolation and simultaneous-link test result |
| Performance | Packet mode/rate, sensitivity for that mode, link margin and measured conditions |

A center-frequency list is not an occupied-bandwidth plan. There is no universal 40 MHz spacing that guarantees zero interference and no universal limit of three simultaneous FPV links. Channel labels can include frequencies outside the permitted band. Obtain the exact device channel table and coordinate the complete installation.

## Free-space loss

For frequency in MHz and distance in km:

`FSPL_dB = 32.45 + 20 log10(f_MHz) + 20 log10(d_km)`

At **915 MHz and 10 km**, this convention gives **111.68 dB**, not 91.5 dB. The 32.4 rounded convention used by the handbook calculator differs by 0.05 dB. State the constant and units when comparing results.

[claim:rf-card-fspl-915-10]

A usable link budget also includes receive antenna gain, cable/installation losses, receiver sensitivity for the selected mode and a stated fade margin. Terrain, Fresnel clearance, interference, antenna orientation and equipment restrictions affect the result. Free-space loss is a calculation, not field evidence or permission to operate at the calculated distance.

See [Link Budgets](../fundamentals/link-budgets.md) for the calculator and managed mathematical references. The former generic ELRS range promises and obstacle divisors are withdrawn.

## Procurement status

Country of headquarters is not a compliance conclusion. Record the exact item, configuration, buyer, applicable prohibition/contract clause and dated evidence using the [federal procurement screening guide](../components/ndaa-compliance.md). This card assigns no nationality-based compliance badges.
