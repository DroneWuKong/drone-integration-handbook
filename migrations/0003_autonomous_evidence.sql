CREATE TABLE IF NOT EXISTS research_specs (
 id TEXT PRIMARY KEY, claim_id TEXT NOT NULL, release TEXT NOT NULL,
 claim_type TEXT NOT NULL, risk TEXT NOT NULL, data TEXT NOT NULL CHECK(json_valid(data)),
 state TEXT NOT NULL CHECK(state IN ('planned','researching','adjudicating','complete','abstained','exception')),
 created TEXT NOT NULL, updated TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS research_specs_claim ON research_specs(claim_id,release);
CREATE INDEX IF NOT EXISTS research_specs_state ON research_specs(state,updated);

CREATE TABLE IF NOT EXISTS research_jobs (
 id TEXT PRIMARY KEY, spec_id TEXT NOT NULL REFERENCES research_specs(id),
 role TEXT NOT NULL CHECK(role IN ('researcher','verifier')),
 provider TEXT NOT NULL, response_id TEXT UNIQUE,
 state TEXT NOT NULL CHECK(state IN ('planned','queued','in_progress','completed','failed','expired','cancelled')),
 attempts INTEGER NOT NULL DEFAULT 0, last_error TEXT,
 created TEXT NOT NULL, updated TEXT NOT NULL,
 UNIQUE(spec_id,role)
);
CREATE INDEX IF NOT EXISTS research_jobs_state ON research_jobs(state,updated);

CREATE TABLE IF NOT EXISTS evidence_packets (
 id TEXT PRIMARY KEY, job_id TEXT NOT NULL UNIQUE REFERENCES research_jobs(id),
 claim_id TEXT NOT NULL, role TEXT NOT NULL CHECK(role IN ('researcher','verifier')),
 data TEXT NOT NULL CHECK(json_valid(data)), digest TEXT NOT NULL,
 created TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS evidence_packets_claim ON evidence_packets(claim_id,role);

CREATE TABLE IF NOT EXISTS evidence_decisions (
 id TEXT PRIMARY KEY, spec_id TEXT NOT NULL UNIQUE REFERENCES research_specs(id),
 claim_id TEXT NOT NULL, publication_state TEXT NOT NULL,
 publish INTEGER NOT NULL CHECK(publish IN (0,1)),
 human_intervention INTEGER NOT NULL CHECK(human_intervention IN (0,1)),
 data TEXT NOT NULL CHECK(json_valid(data)), created TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS evidence_decisions_state ON evidence_decisions(publication_state,human_intervention);

CREATE TABLE IF NOT EXISTS evidence_events (
 id TEXT PRIMARY KEY, entity_type TEXT NOT NULL, entity_id TEXT NOT NULL,
 event_type TEXT NOT NULL, data TEXT NOT NULL CHECK(json_valid(data)), created TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS evidence_events_entity ON evidence_events(entity_type,entity_id,created);

CREATE TABLE IF NOT EXISTS webhook_events (
 id TEXT PRIMARY KEY, event_type TEXT NOT NULL, response_id TEXT,
 state TEXT NOT NULL CHECK(state IN ('received','processed','ignored','failed')),
 created TEXT NOT NULL, updated TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS prediction_ledger (
 id TEXT PRIMARY KEY, data TEXT NOT NULL CHECK(json_valid(data)),
 state TEXT NOT NULL CHECK(state IN ('open','resolved','void')),
 target_date TEXT NOT NULL, registered TEXT NOT NULL, resolved TEXT
);
CREATE INDEX IF NOT EXISTS prediction_due ON prediction_ledger(state,target_date);
