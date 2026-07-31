# Drone Integration Handbook Roadmap

This file tracks **current handbook work only**. Completed historical work remains available in Git history and in [`CHANGELOG.md`](CHANGELOG.md).

Last reconciled: **July 31, 2026**

## Current published baseline

The production builder currently publishes:

- **47 numbered chapters and guides**
- **39 platform profiles**
- **61 component references**
- **147 total searchable references**

The content registry and reader-facing order live in [`handbook_builder/config.py`](handbook_builder/config.py). The deployable artifact is produced by `python3 build.py` and validated by the `handbook-check` GitHub workflow before Cloudflare Pages deployment.

Chapter ID **25 is reserved** after its public source was withdrawn. Do not reuse or recreate that public anchor without an explicit content-release decision.

## Shipped July 31, 2026

- [x] Refactored the monolithic site generator into configuration, build logic, HTML template, CSS, JavaScript, and tests.
- [x] Aligned the handbook interface with Forge and Patterns while retaining cyan handbook identity.
- [x] Added grouped desktop navigation, a mobile drawer, current-location tracking, reading progress, previous/next controls, stable-link copying, and exact-heading search.
- [x] Published five contested/austere field guides that previously existed only as repository files.
- [x] Published Appendices A, C, D, E, and F; Appendix B remains grouped with firmware.
- [x] Published the AI Wingman on Orqa DTK APB integration guide.
- [x] Added the Brecourt Solutions iDFR profile and reconciled the tactical platform index.
- [x] Added a production artifact validator for duplicate IDs, missing fragments, leaked Markdown links, bad search metadata, unresolved template tokens, and missing local assets.
- [x] Upgraded GitHub Actions to compile, test, link-check, build, validate, and upload the exact review artifact.

See [`docs/releases/2026-07-31-site-refactor-and-hardening.md`](docs/releases/2026-07-31-site-refactor-and-hardening.md) for the release record.

## Next priorities

### 1. Stable platform and component URLs

Platform and component profiles are currently auto-numbered (`#p...` and `#c...`) from sorted filenames. Renaming or inserting files can move those anchors.

- [ ] Introduce slug-based canonical anchors such as `#platform-shield-ai-nova-2` and `#component-mesh-radios`.
- [ ] Preserve existing numeric anchors as compatibility aliases.
- [ ] Add tests proving old numeric links and new canonical links resolve to the same reference.

### 2. Offline and field use

The handbook is a single large static document, which is useful for complete local search but increasingly expensive to load.

- [ ] Add a service worker and offline cache manifest.
- [ ] Provide an explicit “save for field use” state rather than relying on incidental browser caching.
- [ ] Cache the HTML, CSS, JavaScript, fonts, and local images with a versioned release key.
- [ ] Define update behavior so an operator can see whether a cached handbook is stale before disconnecting.

### 3. Page weight and delivery architecture

- [ ] Establish performance budgets for generated HTML, CSS, JavaScript, and local media.
- [ ] Measure cold-load and repeat-load behavior on low-bandwidth mobile connections.
- [ ] Decide whether to retain one-page delivery, split references into static detail pages, or produce both from the same registry.
- [ ] If split pages are added, keep the complete local search index and stable legacy anchors.

### 4. Visual field aids

- [ ] Add antenna radiation-pattern diagrams to the antenna fundamentals chapter.
- [ ] Add common FC-to-companion wiring diagrams.
- [ ] Add mesh topology and relay diagrams.
- [ ] Add CoT message-flow diagrams.
- [ ] Add annotated blackbox traces and failure examples.
- [ ] Produce printable field-card layouts for the advanced guides and appendices.

### 5. Content provenance and maintenance

- [ ] Add visible “last verified” and evidence-strength metadata to platform and compliance profiles.
- [ ] Flag claims that are vendor-reported, independently verified, inferred, or field-observed.
- [ ] Add a scheduled stale-source report for regulations, Blue UAS status, manufacturer ownership, prices, and availability.
- [ ] Add a review queue for documents whose source links or verification dates exceed their maintenance window.

### 6. Platform coverage

Profiles worth prioritizing when sufficient public integration detail is available:

- [ ] DJI Matrice 400 and FlyCart 100
- [ ] Watts Innovations Prism and Harris Aerial H6
- [ ] JOUAV CW-25E and comparable VTOL fixed-wing platforms
- [ ] AeroVironment Puma family
- [ ] L3Harris FVR-90
- [ ] Additional less-known NDAA-compliant and allied fixed-wing platforms

### 7. Cross-property work

- [ ] Confirm the current status of the Forge autonomy dataset browser before rescheduling it here.
- [ ] Keep handbook references linked to Forge and Patterns without duplicating application-specific content.
- [ ] Define a shared release/version marker across Handbook, Forge, and Patterns so cross-property links can be regression-tested together.

## Contribution rules for roadmap work

A roadmap item is complete only when:

1. The source content or implementation is merged.
2. The production handbook build includes it.
3. Source and generated-site validation pass.
4. Public navigation and search expose it where appropriate.
5. Documentation and release notes describe the shipped state.

Open an issue or pull request to propose additions. New numbered chapters must receive an unused stable ID in `handbook_builder/config.py`; never renumber an existing published chapter.
