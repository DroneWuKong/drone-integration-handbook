CREATE TABLE IF NOT EXISTS reports (
 id TEXT PRIMARY KEY, token_hash TEXT NOT NULL, payload_hash TEXT NOT NULL,
 data TEXT NOT NULL CHECK(json_valid(data)), state TEXT NOT NULL DEFAULT 'new',
 version INTEGER NOT NULL DEFAULT 1, created TEXT NOT NULL, updated TEXT NOT NULL,
 history TEXT NOT NULL DEFAULT '[]' CHECK(json_valid(history))
);
CREATE INDEX IF NOT EXISTS reports_queue ON reports(created,id);
CREATE INDEX IF NOT EXISTS reports_state ON reports(state);
CREATE TABLE IF NOT EXISTS rate_limits (id TEXT PRIMARY KEY, count INTEGER NOT NULL, expires INTEGER NOT NULL);
