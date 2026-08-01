# July 31, 2026 — Production Redeploy Record

## Purpose

Cloudflare Pages successfully built the legal-risk containment release on the pull-request preview branch, but the production hostname continued serving the earlier 147-reference artifact after pull request #39 was squash-merged.

This documentation-only commit intentionally creates a fresh push to the configured Cloudflare Pages production branch so the validated containment artifact is rebuilt from `main` and promoted to `uas-handbook.com`.

## Release source

- Containment pull request: [#39](https://github.com/DroneWuKong/drone-integration-handbook/pull/39)
- Containment merge commit: `a6ea10771d40926e036f847374e774e694148dde`
- Expected production build: 52 chapters/guides/legal pages, 39 platform profiles, 61 component references, 152 searchable references
- Expected privacy state: no handbook behavioral-analytics endpoint, exact-query transmission, generated session identifiers, scroll-depth events, or outbound-link text collection
- Expected legal controls: publisher identity, Orqa material-relationship disclosure, Privacy Notice, Terms and Safety Limitations, Corrections and Right of Reply, IP/Takedown policy, and publication-review holds

## Verification markers

A successful production promotion must satisfy all of the following on `https://uas-handbook.com/`:

1. The navigation reports **152 field references**.
2. Publisher/legal entries `#ch49` through `#ch53` are present.
3. The page identifies **Jeremiah Wong / Midwest Nice UAS LLC** as publisher.
4. The Privacy Notice states that handbook search is local to the loaded browser tab.
5. Held operational and compliance articles display publication-review notices rather than the withdrawn text.
6. The generated client does not contain `uas-forge.com/api/analytics/ingest`.

## Deployment model

Cloudflare Pages remains the deployment authority. GitHub Actions validates and archives the exact `site/` build, while a push to the production branch triggers the Cloudflare build and promotion. This record changes no handbook guidance or policy; it exists to make the production retry attributable and auditable.
