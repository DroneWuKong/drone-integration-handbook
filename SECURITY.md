# Security Policy

Handbook content is licensed under CC BY-SA 4.0 — see the [LICENSE](LICENSE) file. Some platform-specific entries may carry additional restrictions.

## Reporting a vulnerability

Report security issues **privately** — do not open a public issue or PR.

- Email: jeremiah@midwestniceuas.com
- Include: affected repo/path, a description, reproduction steps, and impact.

Please allow time for triage and a fix before any disclosure.

## Secrets hygiene

Never commit credentials (tokens, API keys, passwords). Use environment
variables or a secret manager. If you find a committed secret, report it via
the contact above so it can be revoked and scrubbed from history.
