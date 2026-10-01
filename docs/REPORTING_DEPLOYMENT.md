# Reporting deployment and production acceptance

Candidate for goal [#57](https://github.com/DroneWuKong/drone-integration-handbook/issues/57). Cloudflare authentication was unavailable in the implementation session, so no private production database, bucket, secret, migrations or live contribution service is claimed.

## Provision isolated resources

Use an authenticated Cloudflare account for the existing `uas-handbook` Pages project. Create separate preview and production D1 databases. Optional attachments need separate **private** R2 buckets with public access disabled. Set a cryptographically random reviewer secret independently in each environment; never put it in Git, client JavaScript, issue comments or logs.

Bind:
- `REPORTS`: the environment's D1 database.
- `EVIDENCE`: the optional environment's private R2 bucket.
- `REVIEW_TOKEN`: the environment's secret.

The checked-in Wrangler file presently has no resource IDs. Complete real bindings in that file before deploying this feature; do not assume dashboard values override a source-controlled deployment configuration. Use current [Pages configuration](https://developers.cloudflare.com/pages/functions/wrangler-configuration/) and [binding documentation](https://developers.cloudflare.com/pages/functions/bindings/) for the actual account. Preview must not share production reports, files or reviewer authorization.

D1 binding shape:

```json
{
  "d1_databases": [{
    "binding": "REPORTS",
    "database_name": "<environment database name>",
    "database_id": "<actual database UUID>",
    "migrations_dir": "migrations"
  }],
  "r2_buckets": [{
    "binding": "EVIDENCE",
    "bucket_name": "<private environment bucket>"
  }]
}
```

Apply both migrations to each intended remote database using its environment/configuration, then verify them. The existing tables contain private data; future destructive migrations require their own data-preservation review.

```sh
npx wrangler d1 migrations apply REPORTS --remote --config <environment configuration>
```

See [current D1 migration commands](https://developers.cloudflare.com/d1/wrangler-commands/). Keep database backups/private object exports out of the public repository.

## Preview acceptance

1. Run all candidate checks in `REFERENCE_TOOLS.md`.
2. Deploy the exact reviewed branch to an isolated Pages preview.
3. Verify `/release.json`, embedded page release and `assets/reference-data.json` agree, and their commit marker matches the deployed exact commit (Cloudflare `CF_PAGES_COMMIT_SHA`).
4. Verify `/api/capabilities` enables submission/review and optional attachments as configured.
5. Submit a clearly labeled software-only test discrepancy. Download its receipt; verify persistence through a fresh browser session and exact retry.
6. Confirm unauthorized review/download access fails. Review the report through correction-prepared with evidence and reason; test duplicate and conflicting edits.
7. Verify optional file upload/retry and reviewer download; confirm no report, token or file enters public search, exports, build artifacts, caches or analytics.
8. Test the full mobile, keyboard and offline flow on the actual preview. SQLite adapter results are necessary but do not replace platform validation.
9. Obtain applicable qualified review and Jeremiah Wong's decision for the exact candidate commit; keep detailed evidence private and publish only a nonprivileged summary.

## Exact production acceptance

After authorized review and isolated preview acceptance, deploy that exact release. The completion goal stays open until the remaining citation/table audit and feature acceptance also pass.

- Custom domain `https://uas-handbook.com/` exposes the exact release.
- Existing legacy and permanent profile links resolve; current holds remain notices.
- Search, mathematical tables, presets and exported claims agree.
- A no-login phone contribution is durably stored and privately reviewable.
- An approved correction has a linked public history and the queue records the exact verified publication release.
- Coherent offline download and failed-update recovery work on the custom domain.
- Production and preview databases/buckets remain isolated; no private information leaks.

Record the actual deployed commit/release, Pages deployment identifier, verification time, commands and outcomes in the nonprivileged release summary and private source-of-record. Do not mark production verified from CI alone.

## Rollback and retention

Preserve the prior deployment/release manifest and private database backup before release. A rollback changes public code/content, not report ownership: retain existing private reports/attachments and use backward-compatible schema migrations. Do not roll back schema by dropping tables. Verify the restored custom-domain release and the receipt/reviewer routes; keep unresolved report/correction history intact.

Complete offline caches are versioned and retained after a failed new download. On a material hold/retraction, reconcile historical cached releases under the publication/records policy; do not republish withdrawn bodies for rollback convenience. Browser caches are not the authoritative publication record.

For approved deletion/privacy requests, an authenticated operator must reconcile the report, its attachment rows and corresponding private R2 objects under the existing retention policy. There is no unauthenticated deletion endpoint. Investigate stale uploading rows before removing reservations; an interrupted upload may be retried.
