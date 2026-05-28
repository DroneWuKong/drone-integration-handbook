# Drone Integration Handbook — build & CI notes for Claude

Open reference for drone RF, firmware, field operations, and integration. **CC BY-SA 4.0** (most content; platform-specific entries may carry additional restrictions from the manufacturer). Live at [uas-handbook.com](https://uas-handbook.com).

## Build / deploy
- **Generator:** `build.py` (Python 3.12 — pinned by `runtime.txt`). Reads markdown chapter files in chapter order (the `CHAPTERS` list at the top of `build.py` is the source of truth) and assembles `site/`.
- **Local build:** `pip install -r requirements.txt && python3 build.py` → output in `site/`.
- **Deploy:** Cloudflare Pages, configured via `wrangler.jsonc` (project `uas-handbook`, `pages_build_output_dir: site`). Auto-deploys on push to default branch. There is no GitHub Actions build/deploy workflow — CF Pages owns it.
- **Redirects:** `_redirects` carries cross-property 301s to `uas-forge.com` (Forge) and `uas-patterns.com/patterns/` (PIE). Keep canonical there; don't hardcode external product URLs inside chapter markdown.

## Content layout (the URL structure)
The directory tree IS the URL tree. Rename a file → break a link.

| Dir | Part | Owns |
|---|---|---|
| `fundamentals/` | Part 1: RF Fundamentals | Five link types, frequency bands, antennas, link budgets |
| `firmware/` | Part 2: Flight Controller Firmware | Four firmwares, MSP, MAVLink, UART layout |
| `field/` | Part 3: Field Operations | Pre-flight, blackbox logs, PID tuning, troubleshooting, unsolved problems |
| `integration/` | Part 4: Integration | Companion computers, mesh radios, TAK / CoT |
| `platforms/` | Part 5: Platform References | `cots/`, `blue-uas/`, `open-source/`, `tactical/` — full integration profiles per airframe |
| `components/` | Component references | Orqa ecosystem, Ghost RC link config, etc. |
| `patterns/`, `grayzone/`, `vendor/`, `pipeline/` | Auxiliary tracks | Patterns/PIE intake, gray-zone tracking, marketplace/listing guides |
| `appendices/`, `templates/`, `assets/` | Reference | Quick-reference cards, printable field cards, diagrams/images |
| `data/` | Raw data | Indexed via app logic; `.graphifyignore` excludes from indexing |

## Workflows
- `.github/workflows/procurement-scanner.yml` — daily/weekly cron for the procurement intel pipeline (only active workflow).
- Two `*.yml.RETIRED` files (`intel-miner`, `pie-pipeline`) — legacy intake from when the handbook owned the PIE pipeline; PIE now lives in `Ai-Project` + `droneclear_forge`. Don't reactivate without coordinating with those repos.

## Style / contribution guide (`CONTRIBUTING.md` is the source of truth)
- Tables for reference data, prose for explanations.
- No emojis. No marketing. "Safe" in quotes — systems mitigate danger, don't eliminate it.
- Show the failure mode, not just the procedure.
- Cite field experience (radio + range + outcome) over theoretical claims.

## Gotchas (hard-won — don't relearn these)
- The chapter order is in `CHAPTERS` inside `build.py`, **not** alphabetical. Adding a chapter requires editing that list — the file alone won't show up in the rendered TOC.
- `_redirects` ordering matters on CF Pages (first-match wins). New redirects go at the **top** unless they're a more specific prefix of an existing rule.
- Don't hardcode `uas-intel.com` anywhere — it was an old vanity domain and has been replaced by `uas-patterns.com` (see `_redirects` for the canonical destination).
- `data/*.csv` and `vendor/`/`assets/vendor/` are excluded from the AI/index pass via `.graphifyignore`. Large data dumps go in `data/`, vendored JS goes in `vendor/`.
- `CLAUDE.md` and `AGENTS.md` are also `.graphifyignore`d — assistant instructions shouldn't get indexed as content.

## Cross-repo context
- **Ai-Project** (`DroneWuKong/Ai-Project`) — private repo housing Prismo Prime (Tauri 2 GCS), Prismo APB (on-board AI), PIE source data, and the parts-db. Some chapter content (component references, intel feeds) is informed by data living there.
- **droneclear_forge** (`DroneWuKong/droneclear_Forge`) — Forge web app at `uas-forge.com`. The handbook redirects `/forge` → forge; never duplicate forge content here.
- **forge-data** (`DroneWuKong/forge-data`) — public sanitized parts/platforms JSON. If a chapter cites part counts, the canonical numbers live there.

## Planning
- `ROADMAP.md` carries the editorial roadmap (chapter additions, platform coverage, content gaps). Update it by hand when scoping new chapters.
- `CHANGELOG.md` records shipped chapters / structural changes.
