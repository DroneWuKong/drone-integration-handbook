# Citation review workflow

This workflow converts the public handbook's unresolved evidence inventory into reproducible review batches. It does not treat automated extraction, risk scoring, links, or repeated wording as verification.

## Generate the queue

Build the site, then generate both a detailed JSON queue and a spreadsheet-safe CSV:

```sh
python3 build.py
python3 scripts/build_review_queue.py
```

The files are written under `.local/` and are also included in the seven-day `handbook-browser-<commit>` CI artifact. The CSV neutralizes spreadsheet formula prefixes. The JSON includes article batches, table membership, normalized duplicate clusters, exact in-passage links, and clearly separate article-level research links.

## Work order

| Priority | Meaning | First action |
|---|---|---|
| P0 | Multiple high-consequence signals, such as regulatory/safety plus performance or configuration | Check current primary authority and configuration scope before editing |
| P1 | One strong high-consequence signal or several material performance/configuration signals | Review in the same article/table batch |
| P2 | Technical data that still needs a source or explicit illustrative scope | Verify by table or repeated cluster where possible |
| P3 | General reference data, labels, dates, and low-risk catalog details | Review after higher priorities; remove nonclaims from the claim registry where appropriate |

Scores prioritize work only. They never approve, reject, or publish a claim. An in-passage source candidate may support the statement, may support only part of it, or may be stale. Article-level links are research leads and must not be cited without checking an exact passage.

## Review a batch

1. Open one article batch, starting with P0 and P1 records.
2. Review table rows together with their complete table and assumptions.
3. Prefer current primary authorities, standards, manufacturer manuals or first-party specifications. Record the exact passage, access date, conditions, version, unit, and relevant configuration.
4. For each material statement, support it, correct and scope it, mark it as an illustration, remove it, or retain visible unresolved status.
5. Promote accepted material to a permanent managed claim ID in `data/evidence.json`; do not reuse the extracted legacy hash as the permanent identity.
6. Rebuild and verify that article prose, search data, exports, calculator presets, and correction history agree.
7. Record the applicable reviewer disposition and publisher decision before production publication.

## Table treatments

Every published table has a deterministic treatment and explanation in `data/table-dispositions.json`:

- `calculator` for tables generated from managed calculation claims;
- `queryable-lookup` for property maps and identifier-led references;
- `guided-explanation` for troubleshooting and decision tables;
- `comparison` for multi-attribute option matrices;
- `removed/held` when a table is excluded from publication.

The treatment controls how readers should use a table. It does not validate the values inside it. `software-checked` applies only to the two generated mathematical tables; legacy tables remain `machine-classified` until their contents receive evidence review.
