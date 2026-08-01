# Private Source of Record and Public Export Boundary

**Public publisher:** Jeremiah Wong / Midwest Nice UAS LLC  
**Public repository:** `DroneWuKong/drone-integration-handbook`  
**Private source-of-record repository:** `DroneWuKong/Ai-Project`

## Repository roles

This public repository contains the exact text approved for publication at `uas-handbook.com`, the public build system, nonprivileged review summaries, corrections, and public release history.

The private `Ai-Project` repository contains the internal handbook mirror/extensions, research, evidence, proprietary configurations, review records, claim ledgers, permissions, test evidence, and publisher decisions used to decide whether material may be exported publicly.

`DroneWuKong/droneclear_Forge` is a separate public product containing the Forge application, public implementation-guide hub, and sanitized hardware/platform data. It is not the canonical source for the long-form public Handbook.

## Public repository does not contain the complete internal record

The public repository should not contain:

- attorney-client communications or attorney work product;
- export-controlled, classified, customer-restricted, or contract-controlled technical information;
- raw restricted-portal manuals;
- proprietary vendor configurations;
- credentials, keys, or private infrastructure details;
- private reviewer notes;
- customer, proposal, deal, or contact records;
- private competitive-intelligence annotations;
- implementation detail excluded from an approved public scope.

A public PR may contain a nonprivileged summary identifying:

- review domain;
- reviewer qualification category;
- review date;
- exact commit reviewed;
- approved public scope;
- explicitly excluded scope;
- internal record ID;
- publisher decision and date.

The detailed evidence and review record remains private or in a more-restricted system approved for the applicable handling.

## Export states

| State | Meaning |
|---|---|
| `HOLD` | Existing public path/anchor is retained, but substantive guidance is withheld pending review |
| `DRAFT_REWRITE` | A public PR contains a proposed lower-risk rewrite; it is not approved merely because CI passes |
| `QUALIFIED_REVIEWED` | Applicable reviewer approved an exact commit and defined public scope |
| `PUBLISHER_APPROVED` | Jeremiah Wong approved that exact reviewed revision for public release |
| `PUBLIC_MERGED` | Public PR merged; production verification may remain |
| `PRODUCTION_VERIFIED` | Custom domain exposes the approved revision and expected privacy/legal controls |
| `RETIRED` | Former public content will not return in its prior form |

CI proves structural and regression requirements. It does not replace subject-matter review or publisher approval.

## Immutable pre-containment record

The exact public versions that existed before the July 31, 2026 containment release are fixed by:

```text
repository: DroneWuKong/drone-integration-handbook
commit: d761264e680a4caf52fca2be618cf0ea0dfb02a3
```

The private source-of-record maintains the article-to-blob register and private review status. The public Git history remains a separate records-preservation and remediation question; removing text from `main` does not remove prior commits, clones, forks, PR refs, artifacts, or caches.

## Publication workflow

```text
private source/evidence
  → provenance and handling review
  → qualified review where required
  → Jeremiah Wong publisher decision
  → public PR and nonprivileged summary
  → CI/generated-site validation
  → merge
  → production verification
  → private manifest/register update
```

Substantive edits after reviewer approval require renewed review unless the reviewer expressly approves the change set.

## Relationship to public review files

Files under `docs/reviews/` are intended as public, nonprivileged review summaries and checklists. They are not the complete private evidence package and should not be treated as legal opinions, export classifications, procurement determinations, or customer authorizations.

The publication-hold tracker is [`docs/LEGAL_REVIEW_HOLDS.md`](LEGAL_REVIEW_HOLDS.md). The public correction and right-of-reply process is [`legal/editorial-and-corrections-policy.md`](../legal/editorial-and-corrections-policy.md).

Questions, corrections, or review proposals: [jeremiah@midwestniceuas.com](mailto:jeremiah@midwestniceuas.com).
