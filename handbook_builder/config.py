"""Content registry and navigation taxonomy for the handbook site.

Stable chapter numbers are intentionally explicit. They are public anchors used by
existing links, so new chapters should be appended with a new number rather than
renumbering the existing sequence.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True, slots=True)
class ChapterSpec:
    source: str
    number: int
    title: str

    @property
    def anchor(self) -> str:
        return f"ch{self.number}"


@dataclass(frozen=True, slots=True)
class PartSpec:
    key: str
    label: str
    chapter_numbers: tuple[int, ...]
    description: str


@dataclass(frozen=True, slots=True)
class CategorySpec:
    key: str
    label: str


@dataclass(frozen=True, slots=True)
class ComponentGroupSpec:
    label: str
    patterns: tuple[str, ...]


CHAPTERS: Final[tuple[ChapterSpec, ...]] = (
    ChapterSpec("fundamentals/five-link-types.md", 1, "The Five Link Types"),
    ChapterSpec("fundamentals/frequency-bands.md", 2, "Frequency Bands & Regulatory Reality"),
    ChapterSpec("fundamentals/antennas.md", 3, "Antennas for People Who Aren't RF Engineers"),
    ChapterSpec("fundamentals/link-budgets.md", 4, "Link Budgets Without the Math"),
    ChapterSpec("firmware/four-firmwares.md", 5, "The Four Firmwares"),
    ChapterSpec("firmware/msp-protocol.md", 6, "MSP Protocol"),
    ChapterSpec("firmware/mavlink-protocol.md", 7, "MAVLink Protocol"),
    ChapterSpec("firmware/uart-layout.md", 8, "UART Layout and Why It Matters"),
    ChapterSpec("field/preflight.md", 9, "Pre-Flight Checklist That Actually Works"),
    ChapterSpec("field/blackbox.md", 10, "Blackbox Logs"),
    ChapterSpec("field/pid-tuning.md", 11, "PID Tuning for People Who Fly"),
    ChapterSpec("field/troubleshooting.md", 12, "When Things Go Wrong"),
    ChapterSpec("integration/companion.md", 13, "Adding a Companion Computer"),
    ChapterSpec("integration/mesh-radios.md", 14, "Mesh Radios for Multi-Vehicle"),
    ChapterSpec("integration/tak.md", 15, "TAK Integration"),
    ChapterSpec("integration/mesh-rider-usb-setup.md", 16, "Mesh Rider over the i.MX USB Port"),
    ChapterSpec("field/unsolved-problems.md", 17, "Unsolved Problems"),
    ChapterSpec("vendor/dow-uas-marketplace.md", 18, "How to Get Listed on the Army UAS Marketplace"),
    ChapterSpec("vendor/dow-uas-marketplace-buyer-access.md", 19, "Army UAS Marketplace — Buyer Account & Access"),
    ChapterSpec("autonomy/autonomy-levels.md", 20, "Levels of Drone Autonomy"),
    ChapterSpec("autonomy/datasets.md", 21, "Datasets & Benchmarks for Drone Autonomy"),
    ChapterSpec("autonomy/perception.md", 22, "Perception: VIO, SLAM & GPS-Denied State Estimation"),
    ChapterSpec("autonomy/detection.md", 23, "Detection: RF and Visual"),
    ChapterSpec("autonomy/onboard-ai-control.md", 24, "Onboard AI & Control"),
    # IDs 26–37 were added after publication. Keep the gap and existing anchors.
    ChapterSpec("firmware/appendix-b-uart-maps.md", 26, "UART Maps for Common Flight Controllers"),
    ChapterSpec("firmware/crsf-elrs-protocol.md", 27, "CRSF & ELRS Protocol"),
    ChapterSpec("firmware/dshot-esc-protocols.md", 28, "DShot & ESC Protocols"),
    ChapterSpec("field/ghost-config.md", 29, "Ghost RC Link Configuration"),
    ChapterSpec("field/elrs-airport-mode.md", 30, "ELRS Airport Mode"),
    ChapterSpec("field/frequency-planning.md", 31, "Frequency Planning Worksheet"),
    ChapterSpec("field/crash-recovery.md", 32, "Crash Recovery & Field Repair"),
    ChapterSpec("field/night-ops.md", 33, "Thermal & Night FPV Operations"),
    ChapterSpec("field/repeater-relay.md", 34, "Repeater & Relay Deployment"),
    ChapterSpec("field/substitution-guide.md", 35, "Supply Chain Substitution Guide"),
    ChapterSpec("integration/edge-node-k3s.md", 36, "Portable Telemetry Edge Node (K3s)"),
    ChapterSpec("fundamentals/packable-antennas.md", 37, "Packable Antennas — Range You Can Carry"),
)


PARTS: Final[tuple[PartSpec, ...]] = (
    PartSpec(
        "rf",
        "Part 1 — RF Fundamentals",
        (1, 2, 3, 4, 31, 37),
        "Links, spectrum, antennas, range, and field frequency planning.",
    ),
    PartSpec(
        "firmware",
        "Part 2 — Flight Controller Firmware",
        (5, 6, 7, 8, 26, 27, 28, 29, 30),
        "Firmware choices, serial protocols, UART maps, RC links, and ESC control.",
    ),
    PartSpec(
        "field",
        "Part 3 — Field Operations",
        (9, 10, 11, 12, 32, 33, 34, 35),
        "Preflight, diagnostics, tuning, recovery, night operations, and substitutions.",
    ),
    PartSpec(
        "integration",
        "Part 4 — Integration",
        (13, 14, 15, 16, 36),
        "Companion compute, mesh, TAK, edge nodes, and system-level wiring.",
    ),
    PartSpec(
        "open-problems",
        "What's Left to Solve",
        (17,),
        "Known gaps, partial workarounds, and unresolved integration problems.",
    ),
    PartSpec(
        "vendor",
        "Part 5 — Vendor Guides",
        (18, 19),
        "Marketplace listing, buyer access, and procurement workflow references.",
    ),
    PartSpec(
        "autonomy",
        "Part 6 — Autonomy",
        (20, 21, 22, 23, 24),
        "Autonomy levels, datasets, state estimation, detection, and onboard control.",
    ),
)


PLATFORM_CATEGORIES: Final[tuple[CategorySpec, ...]] = (
    CategorySpec("cots", "COTS"),
    CategorySpec("blue-uas", "NDAA / Blue UAS"),
    CategorySpec("open-source", "Open-Source / Custom"),
    CategorySpec("tactical", "Tactical / Defense"),
)


COMPONENT_GROUPS: Final[tuple[ComponentGroupSpec, ...]] = (
    ComponentGroupSpec(
        "Propulsion & Airframe",
        (
            "frames-",
            "motors",
            "escs",
            "propellers",
            "propulsion-system",
            "propulsion-non-electric",
            "power-architecture",
        ),
    ),
    ComponentGroupSpec(
        "Flight Controllers & Firmware",
        ("flight-controller", "integrated-stacks"),
    ),
    ComponentGroupSpec(
        "RF, Comms & Control Links",
        ("comms-datalinks", "c2-datalinks", "mafiairs", "military-firmware"),
    ),
    ComponentGroupSpec(
        "Video & Cameras",
        ("fpv-cameras", "video-transmitters", "thermal-cameras"),
    ),
    ComponentGroupSpec(
        "Navigation & Sensors",
        (
            "gps",
            "gnss-",
            "rtk-ppk",
            "navigation-pnt",
            "lidar",
            "sensor-payload",
            "detect-and-avoid",
        ),
    ),
    ComponentGroupSpec(
        "Companion & Compute",
        ("companion-computer", "ai-accelerator", "ground-control"),
    ),
    ComponentGroupSpec(
        "Batteries & Power",
        ("batteries", "battery-deep"),
    ),
    ComponentGroupSpec(
        "Defense & Tactical",
        (
            "electronic-warfare",
            "counter-uas",
            "esad-safe",
            "tactical-accessories",
            "rf-detection",
            "swarm-software",
        ),
    ),
    ComponentGroupSpec(
        "Platforms & Compliance",
        (
            "platforms-global",
            "ndaa-compliance",
            "remote-id",
            "bvlos",
            "utm-airspace",
            "uas-maintenance",
            "industry-intelligence",
            "cellular-lte-bvlos",
            "fleet-management",
            "payload-integration-patterns",
            "fixed-wing-specific",
            "power-systems-deep-dive",
        ),
    ),
    ComponentGroupSpec(
        "Manufacturer Guides",
        ("orqa-hardware", "openhd-implementation"),
    ),
)


SITE_TITLE: Final = "The Drone Integration Handbook"
SITE_DESCRIPTION: Final = (
    "An open field reference for drone RF, integration, firmware, platform, "
    "component, autonomy, and field operations work."
)
SITE_URL: Final = "https://uas-handbook.com/"
REPOSITORY_URL: Final = "https://github.com/DroneWuKong/drone-integration-handbook"
