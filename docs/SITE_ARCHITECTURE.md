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
| `tests/test_builder.py` | Stable-anchor, ordering, link-rewrite, and output smoke tests |

## Stable anchors

Published chapter anchors such as `#ch12` are compatibility identifiers. Do not renumber existing entries. New core chapters receive a new number in `CHAPTERS`; the `PARTS` registry controls where they appear in the reader-facing navigation and page order.

Platform and component references remain auto-discovered:

- platforms start at `#p101` and are grouped by their category directory;
- components start at `#c600` and are grouped by filename patterns in `COMPONENT_GROUPS`.

Renaming auto-discovered files can still change their generated order and anchor. Use explicit core chapter IDs for references that need long-lived external links.

## Adding a core chapter

1. Add the Markdown file under the correct content directory.
2. Add a `ChapterSpec` to `CHAPTERS` with a new, unused number.
3. Add that number to the relevant `PartSpec.chapter_numbers` tuple.
4. Run the build and tests.

The build fails if a registered core chapter is missing or if a Part references an unknown or duplicate chapter number.

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
python3 -m compileall -q build.py handbook_builder tests
node --check assets/handbook.js
python3 -m unittest discover -s tests
python3 build.py
```

The test suite uses a small Markdown renderer stub for orchestration tests, so it can verify the builder independently of Python-Markdown internals. The real build still requires `markdown>=3.4` from `requirements.txt`.
