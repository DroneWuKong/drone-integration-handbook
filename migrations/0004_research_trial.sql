-- Operator activates one explicit, non-renewing trial only after verifying
-- the dedicated OpenAI project's hard spend limit and expiring credentials.
CREATE TABLE research_trial (
 id INTEGER PRIMARY KEY CHECK(id=1),
 enabled INTEGER NOT NULL DEFAULT 0 CHECK(enabled IN (0,1)),
 starts_ms INTEGER NOT NULL,
 ends_ms INTEGER NOT NULL,
 CHECK(ends_ms > starts_ms AND ends_ms-starts_ms <= 1209600000)
);
CREATE TABLE research_trial_dispatches (
 job_id TEXT PRIMARY KEY REFERENCES research_jobs(id),
 spec_id TEXT NOT NULL REFERENCES research_specs(id),
 started_ms INTEGER NOT NULL
);
CREATE INDEX research_trial_dispatch_time ON research_trial_dispatches(started_ms);
