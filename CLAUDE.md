# Drone Integration Handbook — build & CI notes for Claude

Open reference for drone RF, firmware, field operations, and integration. **CC BY-SA 4.0** (most content; platform-specific entries may carry additional restrictions from the manufacturer). Live at [uas-handbook.com](https://uas-handbook.com).

## Build / deploy
- **Generator:** `build.py` is the stable Python 3.12 entrypoint (pinned by `runtime.txt`). The implementation lives in `handbook_builder/`: `config.py` owns stable chapter IDs and reader-facing Part order; `site.py` discovers and renders Markdown, rewrites internal links, and assembles `site/`.
- **Presentation:** `templates/handbook.html` owns semantic page structure. `assets/handbook.css` and `assets/handbook.js` own the shared Forge/Patterns-aligned UI, responsive navigation, search, scrollspy, and browser behavior.
- **Local build:** `pip install -r requirements.txt && python3 build.py` → output in `site/`.
- **Validation:** `python3 -m compileall -q build.py handbook_builder scripts tests && node --check assets/handbook.js && python3 -m unittest discover -s tests && python3 scripts/check_links.py && python3 build.py && python3 scripts/check_generated_site.py site/index.html`.
- **CI:** `.github/workflows/link-check.yml` runs the complete production build and validation sequence, then uploads `site/` as a seven-day review artifact.
- **Deploy:** Cloudflare Pages, configured via `wrangler.jsonc` (project `uas-handbook`, `pages_build_output_dir: site`). Auto-deploys on push to default branch. GitHub Actions validates the artifact but does not deploy it.
- **Redirects:** `_redirects` carries cross-property 301s to `uas-forge.com` (Forge) and `uas-patterns.com/patterns/` (PIE). Keep canonical there; don't hardcode external product URLs inside chapter markdown.

## Content layout (the URL structure)
The directory tree is the source/content tree. Rename a file → break GitHub links and may change auto-discovered platform/component anchors.

| Dir | Part | Owns |
|---|---|---|
| `fundamentals/` | Part 1: RF Fundamentals | Five link types, frequency bands, antennas, link budgets |
| `firmware/` | Part 2: Flight Controller Firmware | Four firmwares, MSP, MAVLink, UART layout, Appendix B |
| `field/` | Part 3 + Field Guides | Pre-flight, diagnostics, recovery, contested/austere operations, unsolved problems |
| `integration/` | Part 4: Integration | Companion computers, mesh radios, TAK / CoT, edge nodes |
| `autonomy/` | Part 6: Autonomy | Levels, datasets, perception, detection, and onboard control |
| `appendices/` | Appendices | Printable frequency, MAVLink, MSP, CoT, and regulatory references |
| `platforms/` | Platform References | `cots/`, `blue-uas/`, `open-source/`, `tactical/` — full integration profiles per airframe |
| `components/` | Component References | Hardware ecosystems and category deep dives |
| `patterns/`, `grayzone/`, `vendor/`, `pipeline/` | Auxiliary tracks | Patterns/PIE intake, gray-zone tracking, marketplace/listing guides |
| `templates/`, `assets/` | Site support | HTML structure, printable cards, diagrams/images, CSS, and JavaScript |
| `data/` | Raw data | Indexed via app logic; `.graphifyignore` excludes from indexing |

## Workflows
- `.github/workflows/link-check.yml` — PR/push production build, source-link check, unit tests, JavaScript syntax check, generated-site validation, and review artifact upload.
- `.github/workflows/procurement-scanner.yml` — daily/weekly cron for the procurement intel pipeline.
- Two `*.yml.RETIRED` files (`intel-miner`, `pie-pipeline`) — legacy intake from when the handbook owned the PIE pipeline; PIE now lives in `Ai-Project` + `droneclear_forge`. Don't reactivate without coordinating with those repos.

## Style / contribution guide (`CONTRIBUTING.md` is the source of truth)
- Tables for reference data, prose for explanations.
- No emojis. No marketing. "Safe" in quotes — systems mitigate danger, don't eliminate it.
- Show the failure mode, not just the procedure.
- Cite field experience (radio + range + outcome) over theoretical claims.

## Gotchas (hard-won — don't relearn these)
- Stable published IDs are in `CHAPTERS` inside `handbook_builder/config.py`, **not** alphabetical. Adding a chapter, advanced field guide, or appendix requires a new unused number and assignment to one `PARTS` entry. Do not renumber published IDs such as `#ch12`.
- Chapter ID 25 is intentionally reserved after its public source was withdrawn. Do not reuse it or reintroduce the removed file through an indirect link.
- `PARTS` controls both navigation and reader-facing chapter order. The build fails if a chapter is missing, unknown, duplicated across Parts, or unassigned.
- Existing Markdown is not automatically public just because it is in `field/`, `integration/`, or `appendices/`. Register reader-facing material explicitly so internal links become stable in-page anchors.
- Platform and component files are auto-discovered. Their generated `#p...` / `#c...` anchors depend on sorted file order, so renaming a file can change those anchors.
- `scripts/check_links.py` verifies source targets. `scripts/check_generated_site.py` verifies the deployable artifact and catches unpublished relative `.md` links, duplicate/missing IDs, bad search metadata, unresolved template tokens, and missing local assets.
- `_redirects` ordering matters on CF Pages (first-match wins). New redirects go at the **top** unless they're a more specific prefix of an existing rule.
- Don't hardcode `uas-intel.com` anywhere — it was an old vanity domain and has been replaced by `uas-patterns.com` (see `_redirects` for the canonical destination).
- `data/*.csv` and `vendor/`/`assets/vendor/` are excluded from the AI/index pass via `.graphifyignore`. Large data dumps go in `data/`, vendored JS goes in `vendor/`.
- `CLAUDE.md` and `AGENTS.md` are also `.graphifyignore`d — assistant instructions shouldn't get indexed as content.
- Keep product-specific application CSS out of the handbook. Shared visual tokens belong in `assets/handbook.css`; the handbook is a long-form reader, not a Forge dashboard.

## Cross-repo context
- **Ai-Project** (`DroneWuKong/Ai-Project`) — private repo housing Prismo Prime (Tauri 2 GCS), Prismo APB (on-board AI), PIE source data, and the parts-db. Some chapter content (component references, intel feeds) is informed by data living there.
- **droneclear_forge** (`DroneWuKong/droneclear_Forge`) — Forge web app at `uas-forge.com`. The handbook redirects `/forge` → Forge; never duplicate Forge content here.
- **forge-data** (`DroneWuKong/forge-data`) — public sanitized parts/platforms JSON. If a chapter cites part counts, the canonical numbers live there.

## Planning
- `ROADMAP.md` carries the editorial roadmap (chapter additions, platform coverage, content gaps). Treat any stale entry that conflicts with the current registry as historical, then correct it in the same PR.
- `CHANGELOG.md` records shipped chapters / structural changes.
- `docs/SITE_ARCHITECTURE.md` documents the builder split, stable-anchor policy, navigation behavior, visual system, publishing rules, and validation commands.
