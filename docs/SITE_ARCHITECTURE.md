# Handbook Site Architecture

The handbook remains a zero-database static site built from Markdown. The refactor separates the public content registry, build logic, HTML structure, CSS, and browser behavior so navigation and visual changes no longer require editing one large Python string.

## Build

```bash
pip install -r requirements.txt
python3 build.py
```

The compatibility entrypoint still writes the deployable site to `site/`, which is the directory configured in `wrangler.jsonc` for Cloudflare Pages.

## Source layout

| Path | Responsibility |
|---|---|
| `build.py` | Stable command-line entrypoint |
| `handbook_builder/config.py` | Stable chapter IDs, Part ordering, platform categories, and component groups |
| `handbook_builder/site.py` | Discovery, Markdown rendering, internal-link rewriting, navigation rendering, and output assembly |
| `templates/handbook.html` | Semantic page structure and build tokens |
| `assets/handbook.css` | Shared Forge/Patterns-aligned visual system and responsive/print layout |
| `assets/handbook.js` | Drawer, search, scrollspy, reading progress, copy-link, keyboard, and analytics behavior |
| `scripts/check_links.py` | Source Markdown target validation |
| `scripts/check_generated_site.py` | Generated-ID, in-page target, metadata, source-link, and asset validation |
| `tests/` | Stable-anchor, ordering, link-rewrite, generated-site, and output smoke tests |

## Published content registry

Core chapters, advanced field guides, and appendices use explicit `ChapterSpec` entries. This prevents completed Markdown from existing in the repository without appearing in the generated reading rail and search index.

The reader-facing groups are defined by `PARTS`:

- RF fundamentals;
- flight-controller firmware;
- field operations;
- contested and austere field guides;
- integration;
- open problems;
- vendor guides;
- autonomy;
- appendices and quick references.

Chapter ID 25 is intentionally reserved after its public source was withdrawn. Do not reuse it.

## Stable anchors

Published chapter anchors such as `#ch12` are compatibility identifiers. Do not renumber existing entries. New core chapters receive a new number in `CHAPTERS`; the `PARTS` registry controls where they appear in the reader-facing navigation and page order.

Platform and component references remain auto-discovered:

- platforms start at `#p101` and are grouped by their category directory;
- components start at `#c600` and are grouped by filename patterns in `COMPONENT_GROUPS`.

Renaming auto-discovered files can still change their generated order and anchor. Use explicit core chapter IDs for references that need long-lived external links.

## Adding a published chapter, guide, or appendix

1. Add the Markdown file under the correct content directory.
2. Add a `ChapterSpec` to `CHAPTERS` with a new, unused number.
3. Add that number to exactly one `PartSpec.chapter_numbers` tuple.
4. Add the reference to the repository README when it belongs in the public content map.
5. Run the complete validation sequence.

The build fails if a registered entry is missing or if a Part references an unknown, duplicate, or unassigned chapter number.

## Navigation behavior

The desktop reading rail and mobile drawer are generated from the same taxonomy. The browser script adds:

- active-reference highlighting and automatic group expansion;
- exact-heading search with `Ctrl/Command+K`;
- chapter/platform/component search filters;
- reading progress and current-location text;
- previous/next reference navigation;
- copyable stable links.

The generated HTML keeps all content available without JavaScript. JavaScript enhances navigation and search but does not own the source content.

## Visual system

The handbook uses the same warm near-black surfaces, cream text, compact mono labels, cards, chips, and restrained motion vocabulary used by Forge and Patterns. Product identity remains explicit:

- Handbook: cyan;
- Forge: red;
- Patterns: green.

Keep shared structural tokens in `:root` and avoid copying page-specific Forge overrides into the handbook. The handbook is a long-form reader, not an application dashboard.

## Validation

```bash
python3 -m compileall -q build.py handbook_builder scripts tests
node --check assets/handbook.js
python3 -m unittest discover -s tests
python3 scripts/check_links.py
python3 build.py
python3 scripts/check_generated_site.py site/index.html
```

`check_links.py` validates the source tree. `check_generated_site.py` validates the deployable artifact and fails on duplicate IDs, missing fragment targets, unpublished relative `.md` links, invalid search metadata, unresolved template tokens, or missing local UI assets.

The `handbook-check` GitHub workflow runs the full sequence with Python 3.12 and Node 22, then uploads `site/` as a seven-day review artifact. Cloudflare Pages remains the deployment authority.

The builder test suite uses a small Markdown renderer stub for orchestration tests, so it can verify the builder independently of Python-Markdown internals. The production CI build installs and uses `markdown>=3.4` from `requirements.txt`.
