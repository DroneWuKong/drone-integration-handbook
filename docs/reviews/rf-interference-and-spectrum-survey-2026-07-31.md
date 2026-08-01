# Review Record — RF Interference Safety and Lawful Spectrum Survey

**Articles:**

- `field/ew-countermeasures.md` — RF Interference Recognition and Flight Safety
- `field/elint-operators.md` — Lawful Spectrum Survey for UAS Operations

**Draft prepared:** July 31, 2026  
**Publication status:** Draft replacements prepared; spectrum-law, privacy, flight-safety, export-control, and publisher review remain required.  
**Automated gate:** Reviewed-replacement validation introduced in PR #51.

## Review objective

Replace two operational electronic-warfare/intelligence articles with narrow civil guidance:

1. recognize link and navigation anomalies without attributing intent;
2. recover or terminate a UAS operation safely;
3. troubleshoot ordinary equipment, power, configuration, coexistence, and site causes;
4. perform passive site surveys and self-interference testing involving the operator's own systems;
5. preserve evidence and report unresolved suspected harmful interference through authorized channels.

The drafts do not teach transmitter location, third-party content collection, jammer hunting, evasion, interference, spoofing, protocol exploitation, targeting, or offensive electronic-warfare activity.

## Primary-source record

| Source | Relevant proposition | Accessed |
|---|---|---:|
| GPS.gov — Information About GPS Jamming | Federal prohibition on ordinary jammer operation/marketing/sale; troubleshoot equipment and service causes first; FCC reporting | 2026-07-31 |
| GPS.gov — Spectrum and Interference Issues | Examples of interference sources and federal GPS-interference reporting context | 2026-07-31 |
| FCC Consumer Complaint Center | General interference complaint intake | 2026-07-31 |
| FCC Emergency Complaints | Routing for consumer/non-public-safety and public-safety interference | 2026-07-31 |
| FAA Hotline | Aviation-safety and regulatory reporting | 2026-07-31 |
| NTIA — Regulating the Use of Spectrum | Spectrum coordination and harmful-interference principles | 2026-07-31 |
| NTIA/ITS — Best Practices for Radio Propagation Measurements | Calibration, documentation, repeatability, verification, and measurement uncertainty | 2026-07-31 |

## Material corrections from the withdrawn versions

### Former EW field card

- Removed instructions to change bands or channels during a suspected attack.
- Removed recommendations to increase power, use non-standard frequencies, extend combat failsafes, or continue a mission through interference.
- Removed jammer-direction displays, EW-bubble mapping, pursuit, emitter targeting, and hunter-killer discussion.
- Removed unsupported statements that a symptom proves jamming or spoofing.
- Replaced them with safe recovery, evidence preservation, ordinary-cause troubleshooting, manufacturer escalation, and regulator reporting.

### Former ELINT article

- Removed signal-identification tables intended to classify third-party systems.
- Removed direction finding, bearing intersection, source localization, operator tracking, enemy-frequency databases, and targeting support.
- Removed advice on decoding, intercepting, exploiting, or allocating effects against third-party communications.
- Replaced it with passive ambient surveys, self-interference testing on the operator's own equipment, lawful channel coordination, privacy limits, measurement records, and cautious evidence language.

## Deliberately excluded scope

- No jammer, spoofer, protocol-takeover, or interference operation is described.
- No unauthorized frequency, bandwidth, channel, power, amplifier, or antenna use is recommended.
- No third-party message content, credential, identifier, or private communication collection is authorized.
- No transmitter, person, organization, military system, public-safety system, or alleged threat is identified or located.
- No method is provided for evading counter-UAS, spectrum enforcement, Remote ID, geofencing, or security controls.
- No public text is presented as authority for military, intelligence, law-enforcement, or licensed experimental activity.
- No symptom is presented as proof of intentional interference without an authorized determination.

## Qualified-review checklist

### Spectrum/FCC review

- [ ] Jammer prohibition language is accurate and appropriately scoped.
- [ ] The articles do not imply that receiving equipment authorizes transmission.
- [ ] Active tests are limited to authorized equipment, frequencies, power, bandwidth, and site conditions.
- [ ] FCC/GPS reporting paths are accurately described.
- [ ] Public-safety interference routing is not overstated.
- [ ] No unauthorized mitigation technique remains.

### Flight-safety review

- [ ] Immediate-action guidance prioritizes separation, approved contingencies, recovery, and landing.
- [ ] No in-flight diagnostic step creates additional workload or risk.
- [ ] Navigation anomalies are treated as untrusted estimates without unsupported spoofing diagnosis.
- [ ] Lost-link, degraded-mode, and alternate-recovery guidance requires prior testing and approval.
- [ ] The articles do not encourage continued operation to gather evidence.

### Privacy/communications review

- [ ] Survey guidance collects only what is necessary for the stated engineering purpose.
- [ ] No third-party content decoding, tracking, identity correlation, or surveillance remains.
- [ ] Identifier, raw-data, access, and retention considerations are sufficient.
- [ ] Report templates avoid unnecessary personal information.

### Export-control/public-scope review

- [ ] No military-intelligence, military end-use, targeting, countermeasure-evasion, or electronic-attack support remains.
- [ ] No customer-restricted, government-controlled, or nonpublic operational source was used.
- [ ] The public scope is limited to civil safety, equipment diagnostics, and spectrum coordination.

### Technical measurement review

- [ ] Instrument-setting and calibration fields are technically meaningful.
- [ ] Comparisons warn against changing antennas, RBW, location, gain, or reference settings without accounting for the difference.
- [ ] Self-interference testing is limited to the operator's own equipment.
- [ ] Observations, correlations, reproduced faults, and authorized source confirmation are correctly distinguished.

## Reviewer disposition

Complete after all applicable reviews:

```text
Reviewer identity:
Reviewer qualifications:
Review domain: spectrum / flight safety / privacy / export / technical
Review date:
Exact commit reviewed:
Approved public scope:
Required changes:
Unresolved limitations:
Private record ID, if applicable:
Disposition: APPROVE / REQUEST CHANGES / DO NOT PUBLISH
```

## Publisher release decision

Complete only after qualified review and passing CI:

```text
Publisher: Jeremiah Wong / Midwest Nice UAS LLC
Decision date:
Exact commit approved:
Decision: APPROVED FOR PUBLICATION / RETAIN HOLD
Reverification date:
```
