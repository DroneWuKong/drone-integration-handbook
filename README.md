# The Drone Integration Handbook

> **Free. Open. No login required.**
>
> A practical bench and field reference for drone RF, firmware, integration,
> diagnostics, platforms, components, autonomy, and field operations.

**Live handbook:** [uas-handbook.com](https://uas-handbook.com/)

The handbook is published by **Jeremiah Wong through Midwest Nice UAS LLC**. It is an informational and editorial reference, not a product manual, legal opinion, procurement certification, aviation authorization, or substitute for manufacturer documentation and qualified professional review.

## Material relationship disclosure

Jeremiah Wong also provides technical advisory and systems-integration services to **Orqa Inc.** through **Midwest Nice Advisory LLC**. Readers should consider that relationship when evaluating Orqa-related coverage. See [Publisher, Affiliations, and Editorial Independence](legal/publisher-and-affiliations.md).

## Start here

| Need | Recommended starting point |
|---|---|
| Learn the system from the beginning | [The Five Link Types](fundamentals/five-link-types.md) |
| Diagnose a failure | [When Things Go Wrong](field/troubleshooting.md) |
| Configure an FC or serial link | [The Four Firmwares](firmware/four-firmwares.md) and [UART Layout](firmware/uart-layout.md) |
| Add companion compute, mesh, or TAK | [Adding a Companion Computer](integration/companion.md) |
| Compare airframes | [Platform References](platforms/README.md) |
| Understand autonomy requirements | [Levels of Drone Autonomy](autonomy/autonomy-levels.md) |
| Open a printable field reference | [Frequency Quick Reference Card](appendices/appendix-a-frequency-quick-reference.md) |
| Report an error or request a reply | [Editorial and Corrections Policy](legal/editorial-and-corrections-policy.md) |

The live site adds grouped navigation, local exact-heading search, active-section tracking, previous/next controls, stable anchors, and visible publisher/legal policies. Search is performed in the browser and is not sent to the publisher.

## Important use limitation

The handbook does not authorize unlawful spectrum use, interference, jamming, spoofing, Remote ID defeat, weapons use, offensive operations, surveillance, export-controlled transfers, or unsafe aircraft or payload modification. See the [Terms of Use and Safety Disclaimer](legal/terms-and-disclaimer.md).

## Content map

### Part 1 — RF Fundamentals

1. [The Five Link Types](fundamentals/five-link-types.md)
2. [Frequency Bands and Regulatory Reality](fundamentals/frequency-bands.md)
3. [Antennas for People Who Aren't RF Engineers](fundamentals/antennas.md)
4. [Link Budgets Without the Math](fundamentals/link-budgets.md)
5. [Frequency Planning Worksheet](field/frequency-planning.md)
6. [Packable Antennas](fundamentals/packable-antennas.md)

### Part 2 — Flight Controller Firmware

1. [The Four Firmwares](firmware/four-firmwares.md)
2. [MSP Protocol](firmware/msp-protocol.md)
3. [MAVLink Protocol](firmware/mavlink-protocol.md)
4. [UART Layout and Why It Matters](firmware/uart-layout.md)
5. [UART Maps for Common Flight Controllers](firmware/appendix-b-uart-maps.md)
6. [CRSF and ELRS Protocol](firmware/crsf-elrs-protocol.md)
7. [DShot and ESC Protocols](firmware/dshot-esc-protocols.md)
8. [Ghost RC Link Configuration](field/ghost-config.md)
9. [ELRS Airport Mode](field/elrs-airport-mode.md)

### Part 3 — Field Operations

1. [Pre-Flight Checklist That Actually Works](field/preflight.md)
2. [Blackbox Logs](field/blackbox.md)
3. [PID Tuning for People Who Fly](field/pid-tuning.md)
4. [When Things Go Wrong](field/troubleshooting.md)
5. [Crash Recovery and Field Repair](field/crash-recovery.md)
6. [Thermal and Night FPV Operations](field/night-ops.md)
7. [Repeater and Relay Deployment](field/repeater-relay.md)
8. [Supply Chain Substitution Guide](field/substitution-guide.md)

### Contested and Austere Operations

Some material is currently represented by visible review notices rather than operational instructions:

- [EW Countermeasures — publication hold](field/ew-countermeasures.md)
- [Fiber-Optic FPV Integration](field/fiber-optic-fpv.md)
- [Drone-to-Drone Intercept — publication hold](field/intercept-ops.md)
- [Attritable Drone Production Handbook](field/attritable-production.md)
- [ELINT for Drone Operators — publication hold](field/elint-operators.md)

### Part 4 — Integration

1. [Adding a Companion Computer](integration/companion.md)
2. [Mesh Radios for Multi-Vehicle](integration/mesh-radios.md)
3. [TAK Integration](integration/tak.md)
4. [Mesh Rider over the i.MX USB Port](integration/mesh-rider-usb-setup.md)
5. [Portable Telemetry Edge Node](integration/edge-node-k3s.md)
6. [AI Wingman on the Orqa DTK APB — review hold](integration/wingman-apb.md)

### Additional tracks

- [Unsolved Problems](field/unsolved-problems.md)
- [Vendor Guides](vendor/dow-uas-marketplace.md)
- [Autonomy](autonomy/autonomy-levels.md)
- [Platform References](platforms/README.md)
- Component references under [`components/`](components/)

### Appendices — Quick Reference

- [Appendix A — Frequency Quick Reference Card](appendices/appendix-a-frequency-quick-reference.md)
- [Appendix B — UART Maps for Common Flight Controllers](firmware/appendix-b-uart-maps.md)
- [Appendix C — MAVLink Message Quick Reference](appendices/appendix-c-mavlink-quick-reference.md)
- [Appendix D — MSP Function Code Quick Reference](appendices/appendix-d-msp-quick-reference.md)
- [Appendix E — CoT Type Code Reference](appendices/appendix-e-cot-type-codes.md)
- [Appendix F — Regulatory and Open Resources](appendices/appendix-f-regulatory-resources.md)

### Publisher and legal policies

- [Publisher, Affiliations, and Editorial Independence](legal/publisher-and-affiliations.md)
- [Editorial, Corrections, and Right-of-Reply Policy](legal/editorial-and-corrections-policy.md)
- [Privacy Notice](legal/privacy.md)
- [Terms of Use and Safety Disclaimer](legal/terms-and-disclaimer.md)
- [Intellectual Property and Takedown Policy](legal/ip-and-takedown.md)

## Build the site

Python 3.12 is the supported runtime.

```bash
pip install -r requirements.txt
python3 build.py
```

The deployable static site is written to `site/`, matching [`wrangler.jsonc`](wrangler.jsonc).

### Validate a change

```bash
python3 -m compileall -q build.py handbook_builder scripts tests
node --check assets/handbook.js
python3 -m unittest discover -s tests
python3 scripts/check_links.py
python3 build.py
python3 scripts/check_generated_site.py site/index.html
```

The GitHub `handbook-check` workflow builds and validates the production artifact, including required legal pages and the absence of handbook behavioral analytics.

## Site architecture

| Path | Responsibility |
|---|---|
| `build.py` | Stable command-line entrypoint |
| `handbook_builder/config.py` | Stable chapter IDs and navigation taxonomy |
| `handbook_builder/site.py` | Discovery, Markdown rendering, link rewriting, and output assembly |
| `templates/handbook.html` | Semantic page structure and visible disclosures |
| `assets/handbook.css` | Core visual system and responsive layout |
| `assets/legal.css` | Publisher, privacy, disclaimer, and publication-hold presentation |
| `assets/handbook.js` | Local search, drawer, scrollspy, progress, keyboard, and copy-link behavior |
| `scripts/check_generated_site.py` | Generated-ID, anchor, metadata, legal-control, privacy, and asset validation |
| `tests/` | Builder, stable-anchor, legal-control, and generated-site tests |

See [Site Architecture](docs/SITE_ARCHITECTURE.md).

## Stable links and publication holds

Published chapter anchors such as `#ch12` are compatibility identifiers. Do not renumber them. A page under review may be replaced with a hold notice while retaining its path and anchor, so old links do not silently expose withdrawn material or break without explanation.

Chapter ID 25 remains reserved after its public source was withdrawn. Platform and component references remain auto-discovered and currently use order-dependent numeric anchors.

## Contributing and corrections

See [CONTRIBUTING.md](CONTRIBUTING.md). Contributions require rights, source, confidentiality, relationship, and publication-risk representations. Sensitive legal, security, privacy, or rights concerns should be sent privately to [jeremiah@midwestniceuas.com](mailto:jeremiah@midwestniceuas.com).

## Licensing

- Original editorial content: CC BY-SA 4.0, subject to file-specific notices.
- Original code and build tooling: MIT.
- Third-party material: its original rights and licenses.

See [LICENSING.md](LICENSING.md), [LICENSE](LICENSE), [LICENSE-CODE](LICENSE-CODE), and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

---

*Built in the field. With real data. On real hardware.*
