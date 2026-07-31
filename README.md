# The Drone Integration Handbook

> **Free. Open. No login required.**
>
> A practical bench and field reference for drone RF, firmware, integration,
> diagnostics, platforms, components, and autonomy.

**Live handbook:** [uas-handbook.com](https://uas-handbook.com/)

The handbook is built by operators for operators. It is not a product manual
or a sales pitch. The goal is to document what connects to what, what fails in
the field, how to diagnose it, and where the public evidence runs out.

## Start here

| Need | Recommended starting point |
|---|---|
| Learn the system from the beginning | [The Five Link Types](fundamentals/five-link-types.md) |
| Diagnose a failure | [When Things Go Wrong](field/troubleshooting.md) |
| Configure an FC or serial link | [The Four Firmwares](firmware/four-firmwares.md) and [UART Layout](firmware/uart-layout.md) |
| Add companion compute, mesh, or TAK | [Integration](integration/companion.md) |
| Compare airframes | [Platform References](platforms/README.md) |
| Review hardware ecosystems | [Orqa Ecosystem](components/orqa-hardware-guide.md) |
| Understand autonomy requirements | [Levels of Drone Autonomy](autonomy/autonomy-levels.md) |

The generated site adds a grouped reading rail, mobile navigation, exact-heading
search, active-section tracking, previous/next controls, and stable chapter
anchors. Use `Ctrl/Command+K` on the live site to search the entire reference.

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

### Part 3 — Field Operations

1. [Pre-Flight Checklist That Actually Works](field/preflight.md)
2. [Blackbox Logs](field/blackbox.md)
3. [PID Tuning for People Who Fly](field/pid-tuning.md)
4. [When Things Go Wrong](field/troubleshooting.md)
5. [Crash Recovery and Field Repair](field/crash-recovery.md)
6. [Thermal and Night FPV Operations](field/night-ops.md)
7. [Repeater and Relay Deployment](field/repeater-relay.md)
8. [Supply Chain Substitution Guide](field/substitution-guide.md)

### Part 4 — Integration

1. [Adding a Companion Computer](integration/companion.md)
2. [Mesh Radios for Multi-Vehicle](integration/mesh-radios.md)
3. [TAK Integration](integration/tak.md)
4. [Mesh Rider over the i.MX USB Port](integration/mesh-rider-usb-setup.md)
5. [Portable Telemetry Edge Node](integration/edge-node-k3s.md)

### Additional tracks

- [Unsolved Problems](field/unsolved-problems.md)
- [Vendor Guides](vendor/dow-uas-marketplace.md)
- [Autonomy](autonomy/autonomy-levels.md)
- [Platform References](platforms/README.md)
- Component references under [`components/`](components/)

## Build the site

Python 3.12 is the supported runtime.

```bash
pip install -r requirements.txt
python3 build.py
```

The deployable static site is written to `site/`, matching the Cloudflare Pages
configuration in [`wrangler.jsonc`](wrangler.jsonc).

### Validate a change

```bash
python3 -m compileall -q build.py handbook_builder tests
node --check assets/handbook.js
python3 -m unittest discover -s tests
python3 scripts/check_links.py
python3 build.py
```

## Site architecture

The build is intentionally split by responsibility:

| Path | Responsibility |
|---|---|
| `build.py` | Stable command-line entrypoint |
| `handbook_builder/config.py` | Stable chapter IDs and navigation taxonomy |
| `handbook_builder/site.py` | Discovery, Markdown rendering, link rewriting, and output assembly |
| `templates/handbook.html` | Semantic page structure |
| `assets/handbook.css` | Forge/Patterns-aligned visual system and responsive layout |
| `assets/handbook.js` | Search, drawer, scrollspy, progress, keyboard, and copy-link behavior |
| `tests/test_builder.py` | Builder and stable-anchor tests |

See [Site Architecture](docs/SITE_ARCHITECTURE.md) for the extension and
compatibility rules.

## Stable links

Published core chapter anchors such as `#ch12` are compatibility identifiers.
Do not renumber an existing core chapter. New chapters receive a new number in
`handbook_builder/config.py`, while the Part registry controls reader-facing
order.

Platform and component references are auto-discovered. Renaming one of those
Markdown files can change its generated ordering and anchor, so use explicit
core chapter IDs for links that must remain stable outside the repository.

## Contributing

Corrections, field data, platform experience, diagrams, and failure reports are
welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

The core rules are:

- Be accurate. State uncertainty explicitly.
- Be practical. Explain the field consequence, not only the theory.
- Show the failure mode, not only the nominal procedure.
- Do not write marketing copy.
- Systems mitigate danger; they do not eliminate it.

Planning and shipped changes are tracked in [ROADMAP.md](ROADMAP.md) and
[CHANGELOG.md](CHANGELOG.md).

## License

Handbook content is released under CC BY-SA 4.0 unless a file states otherwise.
Platform-specific material may retain additional restrictions from its source
or manufacturer.

---

*Built in the field. With real data. On real hardware.*
