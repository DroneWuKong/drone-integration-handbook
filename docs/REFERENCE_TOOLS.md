# Reference tools and evidence migration

Tracking goal: [#57](https://github.com/DroneWuKong/drone-integration-handbook/issues/57). This branch is a candidate implementation, not a completed production release. [#40](https://github.com/DroneWuKong/drone-integration-handbook/issues/40) remains the separate qualified-review/held-content dependency.

## Public evidence and identities

`data/reference-identities.json` freezes all 152 article/profile identities and all existing chapter, platform and component anchors. Permanent aliases use `#ref-<identity>`. Register a new unique identity and unused legacy anchor before publishing a new profile; discovery fails for an unregistered path. Keep an identity when moving a path and update the path registry. Never reuse an identity for a different subject.

`data/evidence.json` contains approved-for-public candidate source records and scoped managed claims. It is independent of the private Ai-Project source-of-record. Source IDs are permanent; records include primary URL, precise passage and access/review dates. A managed claim includes status, scope, revision, history and, where applicable, numerical value, unit and exact calculation inputs. A source/source-check label does not establish qualified review or field validation.

The link-budget mathematical tables are generated from this registry. Article prose, query records, CSV/JSON exports and sourced calculator examples use the same values. Every stored calculator claim is checked against the shared engine. No named-device presets or simulated field observations are invented.

Legacy table rows and digit-bearing paragraphs/list items are indexed with explicit **unreviewed** status, unknown verification dates, original field strings, candidate links and source-file revisions. Two-column rows also expose their original property/value as a named attribute, and reference-level filters aggregate distinct values without guessing a single value when contexts differ. They are not silently promoted into verified specifications. Every article also carries the migration notice for unresolved categorical statements. Their IDs hash article identity, passage type and text: edits create a new legacy passage ID. Promote a reviewed passage to a permanent managed claim ID and link the previous revision; legacy hashes are not immutable claim identities.

The automated inventory does **not** replace the remaining semantic citation audit, particularly statements in headings, graphics, code, comparative adjectives and linked documents. Existing visible citations in legacy prose remain visible but are not automatically treated as validated claim support.

Publication-hold bodies have no exported records or table rows. Their reference entries contain a hold notice only. Search and offline exports use that same filtered snapshot.

## Search and calculations

`reference.html` offers articles/profiles or individual records, all-term text search, kind/group/evidence filters, exact field-name matching, field-value containment, comparison of up to six records, shareable queries and CSV/JSON downloads. Unknown values stay unknown. CSV neutralizes spreadsheet-formula prefixes and includes full source metadata. Queries run in the browser.

`assets/reference-engine.js` is a pure software engine for power-unit conversion, free-space RF loss/budget, battery energy/ideal runtime, electrical load/rating headroom, wavelength and interface declarations. Units, formulas, limitations, sources, engine version and public release accompany results. Hypothetical inputs are labeled. Interface declarations are a planning prompt, not a compatibility approval. No tool requires hardware.

A single release digest covers public article sources, assets, identity/evidence data, templates, builder, function code, migrations and configuration. The article and tools pages embed it; deployment/CI commit markers come from the validated Cloudflare/GitHub commit environment, and source links use that exact revision when available. Local uncommitted candidates have a null commit marker.  the data loader rejects a mismatched snapshot. One public release can still have unresolved evidence—version coherence does not certify accuracy.

## Private reporting and review

Pages Functions route `/api/*` to `server/reports.mjs`. Bind a private D1 database as `REPORTS`, a strong secret as `REVIEW_TOKEN`, and optionally a private R2 bucket as `EVIDENCE`. Neither report data nor attachment storage is read by the public builder.

No-login submissions require consent, carry claim/release context, and support optional contact information. Field observations require declared configuration, observation date, conditions and measurement/method. Draft saving is explicit and local. Stored-report acknowledgment follows a database read-back. Exact retries share a client-generated UUID and private receipt token; altered content using the same identity is rejected. Server storage retains only the token hash. A lost response retries the exact original content.

Receipt status reveals state/timestamps only, with a bearer token. Review requires the reviewer secret and sends no-store responses. The queue supports pagination, state counts, reasons, duplicate targets, optimistic versions and append-only review history:

`new → triaged → needs-evidence / accepted → correction-prepared → published`

Rejection and duplicate decisions are terminal. Publication requires exact public URL/release and reviewer declarations of publisher approval and live verification; the API does not independently certify those declarations. Applicable evidence/qualified review remains a real human gate.

Optional attachments accept at most three 2 MiB PNG/JPEG/PDF/plain-text files per report, with type/signature checks, private object keys and token authorization. Storage acknowledgment follows the R2 write. Exact retry content uses the same attachment identity. Reviewers download files as octet streams; no public URLs or inline rendering are generated. Files remain untrusted evidence. Interrupted uploads retain a reserved slot for retry; a reviewer/operator must reconcile stale uploading rows before deletion. No automatic malware-scanning claim is made.

Abuse controls include same-origin checking, bounded streaming bodies, field limits, credential-pattern rejection and hourly submission counts keyed by a one-day hashed-IP window. These are basic controls, not a complete bot-defense service. Add edge rate limits if actual abuse warrants them.

With no private database binding, the service explicitly reports unavailable storage and the form offers a saved draft and existing publisher email. It never claims a report was stored. This fallback is not production acceptance of the new contribution workflow.

## Correction and maintenance

Run `python3 scripts/check_sources.py` manually. Its private/local state stores source fingerprints and deduplicated content-change, unavailable-source and review-due tasks. Fetch failure preserves the last good fingerprint. A reachable or unchanged source is not renewed fact verification. Reconcile tasks and past dispositions with the private Ai-Project evidence/review register before reopening or exporting a correction. No schedule or outbound notification is activated by this change.

Use `scripts/prepare_correction.py` with a managed claim, public statement, known sources, scope, review reason and optional nonsecret report ID. It creates an explicitly **draft** proposal, preserves the old claim, increments the proposed revision and refuses an existing output path. It does not edit published claims, import private report wording or copy attachments. Review public wording, source passages, exact commit and prior dispositions before applying it. Add a public nonprivileged correction summary and reviewed history; rebuild all surfaces, then record live verification in the private queue/register.

## Offline behavior and checks

Saving is explicit. The worker downloads public files, checks each SHA-256 against the release manifest, and activates only after the whole release succeeds. Failed installs delete the incomplete new cache and retain complete prior caches. API routes, review shells and reviewer scripts are excluded. Every active release serves its own complete cache. Browser storage can still be evicted; download exports for durable field records. No cached release should be treated as a current operational authorization.

Run:

```sh
python3 -m pip install -r requirements.txt
npm ci
python3 -m compileall -q build.py handbook_builder scripts tests
python3 -m unittest discover -s tests -v
npm test
python3 scripts/check_links.py
python3 build.py
python3 scripts/check_generated_site.py site/index.html
python3 scripts/check_evidence.py
npm run build:functions
npx playwright install --with-deps chromium
npm run test:browser
```

The browser check uses the actual API with a software-only SQLite/private-object adapter. It verifies mobile layout, query/compare/export, calculations, drafts, receipts, private attachments, review transitions, logout, complete offline saving, failed-update recovery, offline submission fallback, legacy links and article access with JavaScript disabled. Its results explicitly say production is unverified; it is not a Cloudflare or hardware test.
