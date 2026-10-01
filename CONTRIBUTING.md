# Contributing to The Drone Integration Handbook

The handbook is built by operators for operators. Corrections, field observations, primary-source research, diagrams, and carefully scoped technical references are welcome.

## Before contributing

By submitting a pull request, issue attachment, image, dataset, code change, or other contribution, you represent that:

1. you created the contribution or have authority to submit and license it;
2. it does not contain confidential, proprietary, classified, export-controlled, privacy-restricted, or employer/customer-owned information you are not authorized to disclose;
3. third-party text, code, images, screenshots, diagrams, tables, datasets, and specifications are identified with their source and license or written permission;
4. factual claims are supported and material uncertainty is stated;
5. any employment, consulting, advisory, sponsorship, ownership, free-equipment, reseller, or other material relationship relevant to the contribution is disclosed;
6. you understand the contribution will be public and preserved in repository history.

Do not submit secrets, credentials, personal data, nonpublic vulnerabilities, controlled technical data, or operational material intended to facilitate unlawful interference, surveillance, weapons use, or harm.

## What we are looking for

- **Corrections:** frequencies, pinouts, protocol details, commands, regulatory statements, product status, and citations.
- **Clarifications:** material that is technically accurate but ambiguous or easy to misuse.
- **Primary-source updates:** regulator guidance, accepted declarations, official lists, manufacturer manuals, standards, and public records.
- **Field observations:** configuration, date, conditions, result, failure mode, and limits.
- **New content:** chapters, diagrams, tables, or examples that fill a documented gap and pass the publication-risk review.
- **Right of reply:** documented corrections or responses from a company or identifiable person discussed in the handbook.

## Evidence labels

Use one of these labels when the distinction matters:

| Label | Meaning |
|---|---|
| Official-source verified | Current primary government, standards, accepted-declaration, or official-list evidence |
| Manufacturer-reported | Supplied or published by the company and not independently verified |
| Field-observed | Recorded from a stated configuration, date, and test or deployment |
| Inference / opinion | Editorial interpretation based on disclosed facts |
| Unknown / program-specific | Insufficient evidence or a result dependent on configuration, contract, agency, or jurisdiction |

Do not state that something is “compliant,” “safe,” “cleared,” “certified,” “legal,” “EAR99,” or “FOCI clean” without identifying the authority, exact item or configuration, source, verification date, and limits of the conclusion.

## How to contribute

### From a phone, without a GitHub account

Use **Report / add field evidence** or **Flag this** beside the relevant article or datum. The form prefills the exact reference/claim and release. Describe the issue and, when available, provide a public primary source or proposed wording. For field observations, include configuration/revisions/mode, observation date, conditions and measurement/method with units and uncertainty. Disclose a relevant relationship in the optional relationship field. A software test must be described as software, not field observation or manufacturer certification.

Save a local draft if the connection is unreliable. Submission is confirmed only when a private receipt is returned. Keep its token private. Optional evidence files are available after a confirmed report if private file storage is configured. If submission is unavailable, save the draft and email the publisher.

Web-form reports and attachments enter a private queue; they are not automatically public repository contributions. Public correction wording is reviewed separately. The rights, confidentiality, attribution and relationship requirements above still apply to what you share.


### Small corrections

1. Fork the repository.
2. Edit the relevant file.
3. Cite the supporting source or test record.
4. Submit a pull request explaining what was wrong and why the change is supported.

### New sections or chapters

1. Open an issue describing the proposed scope, sources, intended audience, and foreseeable misuse or safety concerns.
2. Resolve placement, stable numbering, and publication-risk questions before drafting extensive content.
3. Submit the article with claim-level sources and any required third-party notices.
4. Update the public content map, tests, and release documentation.

### Sensitive corrections

Do not open a public issue containing confidential, security-sensitive, personal, or controlled information. Email [jeremiah@midwestniceuas.com](mailto:jeremiah@midwestniceuas.com). Security vulnerabilities follow [`SECURITY.md`](SECURITY.md).

## Style guide

- **Write for the bench, but not past the evidence.** Be specific enough to be useful without inventing certainty.
- **Show the failure mode.** Explain what happens when a configuration is wrong.
- **Separate facts from claims and opinion.** Manufacturer marketing is not independent verification.
- **Use tables for reference data and prose for explanation.**
- **Use primary sources where available.** Preserve access dates for changing claims.
- **No marketing copy, personal attacks, or irrelevant biographies.**
- **No emojis or filler.**
- **Do not imply authorization.** Historical or technical description is not permission to violate aviation, spectrum, export, safety, privacy, or criminal law.

## Content that requires heightened review

The following may be declined, narrowed, or placed on publication hold:

- operational weapons, interception, targeting, electronic attack, ELINT, surveillance, or identification-defeat instructions;
- ordnance, explosive, safe-and-arm, or payload-injury procedures;
- export-controlled, military-intelligence, proprietary, or access-controlled material;
- safety-critical autonomous control or failure behavior without test evidence;
- regulatory compliance instructions without current primary authority;
- materially adverse claims about named companies or people without an evidence archive and fair framing;
- copied or adapted material without clear rights.

## Directory structure

```
fundamentals/    — RF fundamentals and spectrum context
firmware/        — Flight-controller firmware and protocols
field/           — Field operations and reviewed field guides
integration/     — Companion compute, mesh, TAK, and system integration
vendor/          — Procurement and marketplace guides
autonomy/        — Autonomy levels, datasets, perception, and control
components/      — Component and ecosystem references
platforms/       — Platform profiles by category
appendices/      — Quick-reference cards and lookup tables
legal/           — Publisher, privacy, correction, terms, and rights policies
templates/       — Site templates and printable material
assets/          — Styles, scripts, diagrams, and media
```

The authoritative published order is the `CHAPTERS` and `PARTS` registry in `handbook_builder/config.py`. Adding a Markdown file alone does not publish it.

## Licensing

- Original prose, diagrams, and reference data are generally submitted under CC BY-SA 4.0.
- Original code and build tooling are submitted under the MIT License.
- Third-party material retains its own license and must be documented.

See [`LICENSING.md`](LICENSING.md), [`LICENSE`](LICENSE), [`LICENSE-CODE`](LICENSE-CODE), and [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## Corrections and editorial policy

See [`legal/editorial-and-corrections-policy.md`](legal/editorial-and-corrections-policy.md). Payment, sponsorship, consulting, equipment access, or commercial pressure do not purchase favorable coverage or prevent correction.

## Managed public evidence and software checks

For a supported public claim, add a permanent source ID with its exact primary URL, passage, access date and review interval, then add a permanent claim ID with evidence category, statement or generated template, scope, source IDs, check date, revision/history and applicable units/calculation inputs. Preserve unknown configuration values. Use `[claim:<id>]` in prose and promote legacy hashed passages after review. Profiles need a permanent identity/unused alias in `data/reference-identities.json`. Reconcile changed table IDs in `data/table-dispositions.json`; an automatic treatment is not a semantic approval.

Run the checks in [docs/REFERENCE_TOOLS.md](docs/REFERENCE_TOOLS.md). Use the draft correction command there to preserve the old claim and prior dispositions. Existing evidence/qualified-review and publisher decisions remain required where applicable; software checks alone do not release held material.
