# Plan — Autonomy Section (cross-property)

**Status:** planned (not started). Scoped 2026-05-31.
**Properties:** Handbook (uas-handbook.com) reference chapters **+** Forge (uas-forge.com) interactive browser.
**Estimated effort:** ~1 focused day.

The Autonomy section is the user-facing home for everything the drone-data-mining
effort surfaced that isn't a part or a platform: the autonomy stack (perception,
on-board AI, control) and the datasets/benchmarks that feed it. The data backbone
already exists — `forge-data/intel/sources/external_datasets.json` (11 sources,
each tagged mineable / trainable / reference-only with license + ecosystem fit).

---

## Division of labor

| Property | Role | Why |
|----------|------|-----|
| **Handbook** | "Part 6 — Autonomy" prose + tables (4 chapters) | Reference content, durable, CC BY-SA, build via `CHAPTERS` |
| **Forge** | Interactive Autonomy page — filterable dataset/benchmark browser | App surface; fetches `forge-data` JSON at runtime; links back to handbook |

Cross-link both ways: Forge cards link to the handbook chapter for context;
handbook chapters link to the Forge browser for the live dataset list.

---

## The four sections

### 1. Datasets & Benchmarks
- **Source of truth:** `forge-data/intel/sources/external_datasets.json` → publish a
  display-ready `forge-data/autonomy/datasets.json` (curated columns: name, task,
  modality, license, license_class [permissive/NC/unconfirmed], size, ecosystem_use, url).
- **Forge:** card/table browser, filter by task (VIO/SLAM, CV detection, RF, SAR),
  modality (RGB/depth/event/IMU/RF), and **license class** (badge non-commercial
  datasets clearly — UZH-FPV, Mid-Air; flag unconfirmed Kaggle ones).
- **Handbook:** a chapter table summarizing the same, with the license/usage caveats
  spelled out (what you may/may not do with NC data).

### 2. Perception: VIO / SLAM / Depth
- **Handbook chapter:** state estimation, visual-inertial odometry, SLAM, depth &
  semantic understanding — what they are, where they fail, and the benchmarks that
  test them (UZH-FPV for aggressive 6DoF, Mid-Air for synthetic multi-climate).
- Tie to the stack: how perception output feeds `rl-pilot` / `apb`.

### 3. Detection: RF + Visual
- **Handbook chapter + Forge cross-link:** two detection modalities.
  - RF: DroneRF signatures → `NeedleNThread` / `ESP32-Based-RF-Detector` (already mined).
  - Visual: drone-detection corpora (Seraphim CC BY 4.0, pathikg MIT) + the
    bird-vs-drone C-UAS discrimination problem.
- Ties datasets → hardware → the counter-UAS components already in the handbook
  (`components/counter-uas.md`, `fpv-detectors.md`, `rf-detection-hardware.md`).

### 4. Onboard AI & Control
- **Handbook chapter:** the decision/control layer — `apb` on-board AI,
  `rl-pilot` reinforcement learning, detect-and-avoid, swarm autonomy.
- How perception + detection feed control; where autonomy is/ isn't trusted.

---

## Phased day-plan

**Phase 0 — Data prep (forge-data)**
- Generate `autonomy/datasets.json` (display-ready) from `external_datasets.json`.
- Add `license_class` + `usage_note` columns; confirm the 2 unverified Kaggle licenses.
- Add to `manifest.json` so Forge can discover it.

**Phase 1 — Handbook "Part 6 — Autonomy"**
- Author 4 chapter `.md` files: `autonomy/datasets.md`, `autonomy/perception.md`,
  `autonomy/detection.md`, `autonomy/onboard-ai-control.md`.
- Register in `build.py` `CHAPTERS` (chapters 19–22) and add a `PARTS` entry
  "Part 6 — Autonomy", [19,20,21,22]. (Reminder: `CHAPTERS` is the source of truth —
  a file alone won't show in the TOC.)
- `python3 build.py`, verify the four chapters render and cross-links resolve.

**Phase 2 — Forge interactive Autonomy page**
- New page in `forge-source/` (HTML + JS), registered in `build_static.py` + nav + `_routes.json`.
- Fetch `forge-data/autonomy/datasets.json` at runtime (same pattern as parts/platforms).
- Filters: task / modality / license-class. Cards link to the matching handbook chapter.

**Phase 3 — Cross-link & nav**
- Handbook chapters link to the Forge browser; Forge links to chapters.
- Nav entries on both; `_redirects` if a vanity path is wanted (e.g. `/autonomy`).

**Phase 4 — Polish**
- Analytics snippet (Forge already injects one), SEO/meta, and a visible
  **non-commercial license banner** on NC datasets so users don't misuse them.

---

## Guardrails / open items
- **Licensing is the main risk.** UZH-FPV and Mid-Air are CC BY-NC-SA (non-commercial):
  list and link them, do **not** host or repackage the data, and badge them clearly.
  Confirm the unverified Kaggle licenses before listing. Lacmus is SAR (person
  detection) — either a clearly-labeled "adjacent" callout or omit.
- **Don't duplicate** the registry — `external_datasets.json` stays the single source;
  `autonomy/datasets.json` is a generated view.
- **No new data hosting** — the page is a catalog/reference that links out, not a mirror.

---

*When picked up: start at Phase 0, then Handbook (Phase 1) and Forge (Phase 2) can
proceed in parallel since they share only the JSON contract.*
