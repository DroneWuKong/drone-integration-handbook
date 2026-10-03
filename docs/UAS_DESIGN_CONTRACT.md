# UAS family design contract — 2026-10-03

User direction: consistent experience with distinct color identity, following the mobile screenshots of Forge, Patterns and Handbook.

| Area | Brand | Accent | Tinted surface |
| --- | --- | --- | --- |
| Research | Patterns | `#86dfab` | `#11251a` |
| Build | Forge | `#f4c56a` | `#241e12` |
| Learn | Handbook | `#83dded` | `#10242a` |

`uas-design.css` is byte-identical in Forge's `forge-source/` and Handbook's `assets/`. Change the contract in both repos together. Both builders content-version stylesheet URLs. There is no runtime cross-domain stylesheet dependency; each site remains independently deployable and Handbook remains available offline.

Shared rules: warm black background, neutral surfaces, system text, monospace brand/eyebrow, 8px control corners, 12px card corners, 44px navigation and action controls, 30–46px page headings, 24px section headings, 16px introductions. Phones use a dedicated three-column Research / Build / Learn row, with a border and inset line for the current area. Labels and `aria-current` complement color. Page tools remain specific to their task (including Handbook search).

The shared shell applies across Forge/Patterns routes. Homepage content uses opt-in classes so dense specialist tools and their status colors retain their own semantics. Handbook chapter identities, search and reader layout are retained. Home actions precede the full, visible informational notice; notice wording is unchanged. No storage schemas, APIs, data classifications, private gates or legal claims change.

Research basis:
- W3C Reflow: https://www.w3.org/WAI/WCAG22/Understanding/reflow.html — test at 320 CSS px.
- W3C Target Size: https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html — minimum 24px; shared controls use 44px.
- W3C Use of Color: https://www.w3.org/WAI/WCAG21/Understanding/use-of-color.html — labels, borders and current-location semantics supplement color.
- W3C Contrast: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html — check text against actual accent and surface colors.

Acceptance: CI browser journeys cover 320/390/1440px at default and 130% reading size, assert header controls fit and receive pointer hits, capture screenshots, and retain menu focus, search and saved-build regression journeys. Visual review of the hosted candidate precedes release. Test scope is software UI, not validation of aircraft or underlying intelligence.
