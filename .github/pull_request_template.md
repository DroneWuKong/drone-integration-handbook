## What changed

<!-- Describe the content or implementation change. -->

## Evidence and verification

<!-- List primary sources, test configuration, access dates, and evidence labels. -->

## Rights and provenance

- [ ] I created the contributed material or have authority to submit and license it.
- [ ] Third-party text, code, images, diagrams, tables, screenshots, datasets, and specifications are identified with their source and license or permission.
- [ ] I updated `THIRD_PARTY_NOTICES.md` when bundled third-party material was added or adapted.
- [ ] The contribution does not contain confidential, proprietary, classified, export-controlled, personal, or employer/customer-owned information I am not authorized to disclose.

## Relationships and editorial risk

- [ ] I disclosed any employment, consulting, advisory, ownership, sponsorship, free-equipment, reseller, or other material relationship relevant to this change.
- [ ] Manufacturer claims are labeled and are not presented as independent verification.
- [ ] Named adverse claims are supported by a preserved evidence record and framed as fact, inference, or opinion accurately.

## Safety and lawful-use review

- [ ] The change does not provide operational instructions intended to facilitate unlawful interference, surveillance, identification defeat, weapons use, targeting, or harm.
- [ ] Safety-critical commands, limits, wiring, and procedures are supported by current primary documentation or a documented test.
- [ ] Regulatory and compliance statements identify the authority, exact item or configuration, verification date, and scope limits.

## Validation

- [ ] `python3 -m compileall -q build.py handbook_builder scripts tests`
- [ ] `node --check assets/handbook.js`
- [ ] `python3 -m unittest discover -s tests`
- [ ] `python3 scripts/check_links.py`
- [ ] `python3 build.py`
- [ ] `python3 scripts/check_generated_site.py site/index.html`
