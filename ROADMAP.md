# Drone Integration Handbook Roadmap

This file tracks **current handbook work only**. Completed historical work remains available in Git history and in [`CHANGELOG.md`](CHANGELOG.md).

Last reconciled: **July 31, 2026**

## Current published baseline

The production builder currently publishes:

- **52 numbered chapters, guides, and publisher/legal pages**
- **39 platform profiles**
- **61 component references**
- **152 total searchable references**

Eight previously published operational, compliance, or relationship-sensitive references currently resolve to visible review-hold notices instead of their former text. The content registry and reader-facing order live in [`handbook_builder/config.py`](handbook_builder/config.py). The deployable artifact is produced by `python3 build.py` and validated by the `handbook-check` GitHub workflow before Cloudflare Pages deployment.

Chapter ID **25 is reserved** after its public source was withdrawn. Do not reuse or recreate that public anchor without an explicit content-release decision.

## Legal and editorial remediation — active priority

- [x] Disable handbook behavioral analytics and exact search-query transmission.
- [x] Publish visible publisher identity, material-relationship, privacy, terms, corrections, and IP/takedown pages.
- [x] Separate editorial-content and software licensing.
- [x] Add contributor ownership, confidentiality, provenance, relationship, and export-control representations.
- [x] Place EW countermeasures, drone interception, ELINT, military firmware, Remote ID, NDAA compliance, Orqa hardware, and Wingman/APB pages on visible review hold while preserving stable paths.
- [x] Add CI tests that fail if behavioral analytics or withdrawn operational markers return.
- [ ] Obtain qualified export-controls review for held defense-adjacent material.
- [ ] Rebuild Remote ID guidance from current FAA sources and accepted Declarations of Compliance.
- [ ] Rebuild government-procurement compliance guidance as a dated, source-specific decision aid.
- [ ] Rebuild Orqa coverage with claim-level sources, independent review, and close material-relationship disclosure.
- [ ] Create a claim-level evidence ledger and right-of-reply record for named-company profiles.
- [ ] Audit remaining articles for copied media, standards excerpts, unverified specifications, stale legal claims, and third-party licenses.
- [ ] Decide whether a registered DMCA agent or other formal notice process is appropriate with counsel.

## Shipped July 31, 2026

- [x] Refactored the monolithic site generator into configuration, build logic, HTML template, CSS, JavaScript, and tests.
- [x] Aligned the handbook interface with Forge and Patterns while retaining cyan handbook identity.
- [x] Added grouped desktop navigation, a mobile drawer, current-location tracking, reading progress, previous/next controls, stable-link copying, and exact-heading search.
- [x] Published field guides and appendices that previously existed only as repository files.
- [x] Published the AI Wingman on Orqa DTK APB integration guide, then placed it on review hold during legal hardening.
- [x] Added the Brecourt Solutions iDFR profile and reconciled the tactical platform index.
- [x] Added a production artifact validator for duplicate IDs, missing fragments, leaked Markdown links, bad search metadata, unresolved template tokens, missing local assets, required legal pages, and analytics regression.
- [x] Upgraded GitHub Actions to compile, test, link-check, build, validate, and upload the exact review artifact.

See [`docs/releases/2026-07-31-site-refactor-and-hardening.md`](docs/releases/2026-07-31-site-refactor-and-hardening.md) for the original site release record.

## Product and architecture priorities

### 1. Stable platform and component URLs

Platform and component profiles are currently auto-numbered (`#p...` and `#c...`) from sorted filenames. Renaming or inserting files can move those anchors.

- [ ] Introduce slug-based canonical anchors such as `#platform-shield-ai-nova-2` and `#component-mesh-radios`.
- [ ] Preserve existing numeric anchors as compatibility aliases.
- [ ] Add tests proving old numeric links and new canonical links resolve to the same reference.

### 2. Offline and field use

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
- [ ] Produce printable field-card layouts for reviewed field guides and appendices.

### 5. Content provenance and maintenance

- [ ] Add visible “last verified” and evidence-strength metadata to platform and compliance profiles.
- [ ] Flag claims that are vendor-reported, independently verified, inferred, or field-observed.
- [ ] Add a scheduled stale-source report for regulations, Blue List status, manufacturer ownership, prices, and availability.
- [ ] Add a review queue for documents whose source links or verification dates exceed their maintenance window.

### 6. Platform coverage

Profiles worth prioritizing when sufficient public integration detail is available:

- [ ] DJI Matrice 400 and FlyCart 100
- [ ] Watts Innovations Prism and Harris Aerial H6
- [ ] JOUAV CW-25E and comparable VTOL fixed-wing platforms
- [ ] AeroVironment Puma family
- [ ] L3Harris FVR-90
- [ ] Additional less-known compliant and allied fixed-wing platforms, with dated official evidence rather than categorical labels

### 7. Cross-property work

- [ ] Confirm the current status of the Forge autonomy dataset browser before rescheduling it here.
- [ ] Keep handbook references linked to Forge and Patterns without duplicating application-specific content.
- [ ] Define a shared release/version marker across Handbook, Forge, and Patterns so cross-property links can be regression-tested together.

## Completion rules

A roadmap item is complete only when:

1. The source content or implementation is merged.
2. The production handbook build includes it.
3. Source and generated-site validation pass.
4. Public navigation and search expose it where appropriate.
5. Material relationships, rights, and evidence status are documented.
6. Release notes describe the shipped state.

Open an issue or pull request to propose additions. New numbered chapters must receive an unused stable ID in `handbook_builder/config.py`; never renumber an existing published chapter.
