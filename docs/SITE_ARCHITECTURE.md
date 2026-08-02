# Handbook Site Architecture

The handbook is a zero-database static site built from Markdown. Content order, build logic, document structure, styling, browser behavior, legal controls, and validation are separated so one change does not silently alter every responsibility.

## Build

```bash
pip install -r requirements.txt
python3 build.py
```

The compatibility entrypoint writes the deployable site to `site/`, matching the Cloudflare Pages configuration in `wrangler.jsonc`.

## Source layout

| Path | Responsibility |
|---|---|
| `build.py` | Stable command-line entrypoint |
| `handbook_builder/config.py` | Stable chapter IDs, Part order, legal pages, platform categories, and component groups |
| `handbook_builder/site.py` | Discovery, Markdown rendering, link rewriting, navigation rendering, and output assembly |
| `templates/handbook.html` | Semantic page structure, publisher identity, legal notices, and build tokens |
| `assets/handbook.css` | Core Forge/Patterns-aligned visual system and responsive/print layout |
| `assets/legal.css` | Safety notice, publication-hold, privacy, and legal-page presentation |
| `assets/handbook.js` | Local-only search, drawer, scrollspy, progress, keyboard, and copy-link behavior |
| `scripts/check_links.py` | Source Markdown target validation |
| `scripts/check_generated_site.py` | Generated IDs, targets, metadata, assets, required legal pages, and analytics-removal validation |
| `tests/test_legal_controls.py` | Review-hold, public-association, privacy, and reviewed-publication regression controls |
| `legal/` | Publisher, corrections, privacy, terms, and intellectual-property policies |
| `docs/PRIVATE_SOURCE_OF_RECORD.md` | Public/private repository boundary and export-state model |
| `docs/LEGAL_REVIEW_HOLDS.md` | Public hold and draft-replacement register |

## Private source of record

This repository is the canonical source for the **public** Handbook revision. It is not the complete internal evidence or review system.

The private `DroneWuKong/Ai-Project` repository is the source of record for:

- the private handbook mirror/extensions;
- research and evidence;
- proprietary configurations;
- claim ledgers and source snapshots;
- rights and permission records;
- detailed qualified-review dispositions;
- publisher release decisions;
- the immutable article-to-blob archive register.

Public PRs may carry a nonprivileged summary, review checklist, internal record ID, and approved public scope. They should not contain privileged advice, controlled technical data, customer-restricted information, raw restricted-portal manuals, private reviewer notes, or proprietary configurations.

The boundary is documented in [`docs/PRIVATE_SOURCE_OF_RECORD.md`](PRIVATE_SOURCE_OF_RECORD.md).

`DroneWuKong/droneclear_Forge` is a separate public application and implementation-guide hub. It is not the canonical source for the long-form public Handbook.

## Published content registry

Core chapters, field guides, appendices, and publisher/legal policies use explicit `ChapterSpec` entries. This prevents a completed or sensitive Markdown file from becoming public merely because it exists in the repository.

The reader-facing groups are defined by `PARTS`:

- RF fundamentals;
- flight-controller firmware;
- field operations;
- contested and austere field guides;
- integration;
- open problems;
- vendor guides;
- autonomy;
- appendices;
- publisher and legal policies.

Chapter ID 25 remains reserved after its public source was withdrawn. Do not reuse it.

## Publication holds

A review hold replaces the current article text while preserving its repository path and stable anchor. This keeps old links from exposing withdrawn material or failing without explanation.

The public hold register is [`docs/LEGAL_REVIEW_HOLDS.md`](LEGAL_REVIEW_HOLDS.md). A held article returns only after the applicable technical, safety, legal, export-control, editorial-independence, provenance, and evidence conditions are documented.

CI validates publication-state metadata and known regression markers. It does not provide legal, export, regulatory, safety, technical, provenance, independent-review, or publisher approval.

## Stable anchors

Published chapter anchors such as `#ch12` are compatibility identifiers. Do not renumber existing entries. New explicit references receive a new number in `CHAPTERS`; `PARTS` controls reader-facing order.

Platform and component references remain auto-discovered:

- platforms start at `#p101` and are grouped by category directory;
- components start at `#c600` and are grouped by filename patterns in `COMPONENT_GROUPS`.

Renaming auto-discovered files can still change their generated order and numeric anchor. Use explicit chapter IDs for references requiring long-lived external links.

## Adding a published reference

1. Prepare or identify the private source/evidence record when the article has an internal basis.
2. Add the Markdown file in the correct public directory.
3. Assign a new, unused `ChapterSpec` number when it is an explicit reference.
4. Assign that number to exactly one Part.
5. Identify primary sources, evidence status, rights, relevant external relationships, foreseeable misuse, and approved public scope.
6. Complete the applicable qualified review and record Jeremiah Wong's publisher decision for the exact revision.
7. Update the README, release record, private manifest/register, and third-party notices when applicable.
8. Run the complete validation sequence.
9. Verify the custom domain after merge.

Adding a file alone does not publish it. Passing CI alone does not approve it.

## Browser behavior and privacy

The desktop rail and mobile drawer share one generated taxonomy. Browser JavaScript adds active-reference highlighting, automatic group expansion, exact-heading search, filters, reading progress, current location, and copy-link controls.

Search is performed locally against content already loaded in the browser tab. The handbook client does not transmit search queries, session identifiers, scroll depth, time-on-page events, outbound-link text, or behavioral analytics events. CI fails if the removed analytics markers return.

All source content remains present in generated HTML without JavaScript. JavaScript enhances navigation; it does not own the publication record.

## Visual system

The handbook uses the same warm near-black surfaces, cream text, compact mono labels, cards, chips, and restrained motion vocabulary used by Forge and Patterns. Product identity remains explicit:

- Handbook: cyan;
- Forge: red;
- Patterns: green.

Safety notices and review holds use distinct cyan and amber treatments defined in `assets/legal.css`.

## Validation

```bash
python3 -m compileall -q build.py handbook_builder scripts tests
node --check assets/handbook.js
python3 -m unittest discover -s tests
python3 scripts/check_links.py
python3 build.py
python3 scripts/check_generated_site.py site/index.html
```

`check_links.py` validates source targets. `check_generated_site.py` validates the deployable artifact and fails on duplicate IDs, missing fragments, relative `.md` links leaking into production, invalid search metadata, unresolved tokens, missing assets, missing publisher/legal controls, or behavioral analytics markers.

The `handbook-check` workflow runs the full sequence with Python 3.12 and Node 22, then uploads `site/` as a seven-day review artifact. Cloudflare Pages remains the deployment authority.
