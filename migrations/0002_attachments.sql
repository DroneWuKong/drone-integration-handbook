CREATE TABLE IF NOT EXISTS attachments (
 id TEXT PRIMARY KEY, report_id TEXT NOT NULL REFERENCES reports(id),
 filename TEXT NOT NULL, content_type TEXT NOT NULL, bytes INTEGER NOT NULL,
 digest TEXT NOT NULL, object_key TEXT NOT NULL UNIQUE,
 state TEXT NOT NULL CHECK(state IN ('uploading','ready')), created TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS attachments_report ON attachments(report_id);
