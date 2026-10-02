# Autonomous evidence and prediction system

The handbook can run its claim-research, verification, adjudication and prediction-scoring path entirely in software. Live web research is an optional provider adapter. No hardware, flight controller or field device is required.

## Trust boundary

The model collects structured evidence. Deterministic application code decides whether the evidence meets a claim-type policy. A model response can never directly edit or publish handbook prose.

Each unresolved record produces two isolated jobs:

1. `researcher` seeks the strongest support and narrows the statement.
2. `verifier` independently attempts to falsify it, find superseding material and identify scope errors.

Both return the same strict evidence-packet schema. Trusted code then retrieves every cited source, enforces the per-claim domain allowlist, hashes the retrieved bytes, optionally archives them privately in R2, and replaces any digest supplied by the model. Model-provided hashes are never trusted.

The policy engine automatically:

- classifies obvious administrative metadata as `not-a-claim`;
- publishes a decision only when independent packets agree and claim-specific requirements pass;
- abstains when evidence is incomplete or confidence is below the threshold;
- escalates contradictions, regulatory ambiguity, safety-critical advice and unresolved counterevidence;
- records every result without modifying the public handbook.

The private `review.html` console combines field reports with the small exception queue. It shows the exact claim and handbook location and offers four explicit dispositions: accept a release proposal, reject it, require field evidence, or defer. The reviewer supplies one concise reason; retries are idempotent and the disposition is appended to the immutable event ledger. A disposition still does not publish content.

`publish: true` means the evidence packet qualifies for a release proposal. It does not bypass the versioned build, tests, deployment verification or correction history.

## Software-only operation

Build and plan a bounded cycle without credentials:

```sh
python3 build.py
python3 scripts/run_autonomous_evidence.py --provider software --maximum 10
```

This writes:

- `.local/autonomy/plan.json`: specs, jobs, automatic dispositions and summary;
- `.local/autonomy/requests/*.json`: exact background requests for inspection/replay.

Nothing is sent and `publication_changed` remains false. Tests use `SoftwareProvider` to replay evidence packets through the same validation, adjudication and forecast-scoring code.

## Live operation

The recommended production route keeps the OpenAI API key in the Cloudflare backend. A scheduler holds only the handbook reviewer token and submits a prepared run to:

```text
POST /api/autonomy/runs
```

The server:

1. validates the research spec and both strict background requests;
2. starts the bounded Responses API jobs;
3. stores response IDs in D1 before acknowledging the run;
4. accepts `response.completed` events only at `/api/autonomy/webhooks/openai`;
5. verifies the raw request with the OpenAI webhook signing secret and a five-minute replay window;
6. deduplicates webhook IDs;
7. retrieves the completed response server-side;
8. retrieves and hashes cited source bytes;
9. stores evidence packets and applies deterministic adjudication once both roles finish.

The scheduled workflow runs nightly, processes ten records/twenty jobs by default, and advances its cached cursor only when every job in the batch was acknowledged. Set the `AUTONOMY_BATCH_SIZE` repository variable, or choose a batch size from 1–50 on a manual run, to change the cost/rate envelope without editing code. Without both dispatcher secrets, it remains in software mode and does not advance or claim live research occurred.

Direct developer execution is also available:

```sh
OPENAI_API_KEY=... python3 scripts/run_autonomous_evidence.py \
  --provider openai --maximum 10 --start-limit 20
```

The model is configurable through `OPENAI_RESEARCH_MODEL`; the default is `gpt-5.5`. Requests use the Responses API, hosted `web_search`, background mode, required tool use, domain filters, source inclusion and strict JSON Schema output.

## Required production configuration

Apply migrations `0001` through `0003`, then configure:

| Location | Name | Purpose |
|---|---|---|
| Cloudflare secret | `OPENAI_API_KEY` | Starts and retrieves background research |
| Cloudflare secret | `OPENAI_WEBHOOK_SECRET` | Verifies OpenAI webhook events |
| Cloudflare secret | `REVIEW_TOKEN` | Protects private control and exception routes |
| Cloudflare binding | `REPORTS` | D1 research/job/packet/decision ledger |
| Cloudflare binding | `EVIDENCE` | Optional private R2 source snapshots and field evidence |
| GitHub secret | `AUTONOMY_DISPATCH_URL` | Exact production or isolated-preview origin |
| GitHub secret | `AUTONOMY_REVIEW_TOKEN` | Matches that environment's reviewer secret |
| GitHub variable | `OPENAI_RESEARCH_MODEL` | Optional evaluated model selection |
| GitHub variable | `AUTONOMY_BATCH_SIZE` | Optional nightly record limit, clamped to 1–50 |

Create an OpenAI project webhook for `response.completed` pointing at:

```text
https://<handbook-origin>/api/autonomy/webhooks/openai
```

Do not put `OPENAI_API_KEY` or `OPENAI_WEBHOOK_SECRET` in GitHub artifacts, public JavaScript, issue comments or repository variables.

## Prediction experiment

Predictions are immutable after registration and require an exact question, probability, data cutoff, target date, objective HTTPS resolution source and baseline probability. Resolution rejects a different source, so the success criterion cannot be swapped after seeing the outcome.

```sh
python3 scripts/score_predictions.py data/prediction-ledger.json register prediction.json
python3 scripts/score_predictions.py data/prediction-ledger.json resolve <id> true https://authority.example/outcome
```

Resolution records Brier scores for the AI and frozen baseline. The public evidence-lab dashboard shows no accuracy score until outcomes exist.

## Recovery and historical checks

- Specs, jobs, packets, decisions, webhook receipts and forecasts have stable identities.
- Run submission and webhook handling are idempotent.
- Duplicate events do not duplicate packets or decisions.
- Failed source retrieval or malformed output fails closed.
- Prior evidence remains immutable when a source or claim changes; a new source/claim revision creates a new research spec.
- Source monitoring compares current content with preserved fingerprints and reopens affected work rather than overwriting history.
- Hardware validation, if later added, must remain an explicit `field-observation` source class. It cannot replace or disable the software-only path.

## Verification

```sh
python3 -m unittest tests.test_autonomous -v
node --test tests/autonomy.test.mjs
python3 scripts/run_autonomous_evidence.py --provider software --maximum 5
python3 build.py
```

The Node test runs the complete dispatch → signed webhook → source snapshot → independent-packet → deterministic-decision sequence with software adapters.
