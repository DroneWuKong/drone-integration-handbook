# July 31, 2026 — Site Refactor and Hardening

This release records the two changes that converted the handbook from a monolithic generated page into a maintainable, validated field-reference site.

## Release commits

| Pull request | Merge commit | Scope |
|---|---|---|
| [#36 — Refactor handbook navigation and align UI with Forge/Patterns](https://github.com/DroneWuKong/drone-integration-handbook/pull/36) | `fd15f0b687c0ebb49f7029523c0de9087a6a4eaa` | Builder split, visual system, grouped navigation, responsive drawer, search, scrollspy, stable links, and tests |
| [#37 — Publish field guides and harden handbook CI](https://github.com/DroneWuKong/drone-integration-handbook/pull/37) | `17aef4158065a5fe686d41d3c57a4f012c3b99c6` | Published omitted guides, appendices, Wingman/APB, Brecourt iDFR, generated-site validation, and full production CI |

## Site architecture

The previous `build.py` combined content ordering, Markdown rendering, HTML, styling, JavaScript, analytics, and navigation in one large file. The release separates those responsibilities:

- `build.py` — stable command-line entrypoint
- `handbook_builder/config.py` — stable chapter IDs and navigation taxonomy
- `handbook_builder/site.py` — discovery, Markdown rendering, link rewriting, and output assembly
- `templates/handbook.html` — semantic document structure
- `assets/handbook.css` — Forge/Patterns-aligned visual system
- `assets/handbook.js` — search, drawer, scrollspy, reading progress, keyboard behavior, and copy-link controls
- `scripts/check_generated_site.py` — deployable artifact validation
- `tests/` — stable-anchor, ordering, fragment, builder, and generated-site tests

The deployment command and Cloudflare Pages output remain unchanged:

```bash
python3 build.py
```

## Reader-facing changes

- Persistent grouped reading rail on desktop
- Mobile navigation drawer generated from the same taxonomy
- Current-reference highlighting and automatic group expansion
- Reading progress and current-location display
- `Ctrl/Command+K` exact-heading search
- Chapter, platform, and component search filters
- Previous/next navigation
- Copyable stable reference links
- Responsive and print-specific layouts
- Handbook/Forge/Patterns product links with distinct cyan/red/green identity

## Published content

The hardening release made the following existing documents first-class searchable references:

### Contested and austere field guides

- EW Countermeasures Field Card
- Fiber-Optic FPV Integration
- Drone-to-Drone Intercept Playbook
- Attritable Drone Production Handbook
- ELINT for Drone Operators

### Appendices

- Appendix A — Frequency Quick Reference Card
- Appendix C — MAVLink Message Quick Reference
- Appendix D — MSP Function Code Quick Reference
- Appendix E — CoT Type Code Reference
- Appendix F — Regulatory and Open Resources

Appendix B remains grouped with flight-controller firmware.

### Additional references

- AI Wingman on the Orqa DTK APB
- Brecourt Solutions iDFR platform profile

The resulting production build contains:

- 47 numbered chapters and guides
- 39 platform profiles
- 61 component references
- 147 total references

Chapter ID 25 remains reserved after the former public source was withdrawn.

## Validation contract

The `handbook-check` GitHub workflow now installs the real build dependency and runs:

```bash
python3 -m compileall -q build.py handbook_builder scripts tests
python3 -m unittest discover -s tests -v
node --check assets/handbook.js
python3 scripts/check_links.py
python3 build.py
python3 scripts/check_generated_site.py site/index.html
```

The generated-site validator rejects:

- duplicate element IDs;
- links to missing fragments;
- source `.md` links leaking into the deployed single-page site;
- unresolved template tokens;
- missing local assets;
- invalid, duplicate, or unmatched search metadata;
- removal of required published anchors.

The exact generated `site/` directory is uploaded as a seven-day GitHub Actions artifact for review. Cloudflare Pages remains the deployment authority.

## Compatibility

- Existing core chapter anchors remain unchanged.
- The build command and `site/` output directory remain unchanged.
- Platform numbering still begins at `#p101`.
- Component numbering still begins at `#c600`.
- Source Markdown remains readable independently of JavaScript.
- Existing redirects, analytics ingestion, and tools copying remain in place.

The next compatibility task is introducing slug-based canonical platform and component anchors while preserving existing numeric aliases.
