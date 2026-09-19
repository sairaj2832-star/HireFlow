-- 001_ledger.sql — HireFlow ledger B0 (Report §5 ADR-001)
-- WAL is set via PRAGMA in migrate.py, not here; FTS5 tokenizer = unicode61.
-- Append-only: UPDATE/DELETE rejected by triggers; correction = supersedes_id.

CREATE TABLE IF NOT EXISTS source_records (
  id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL,
  kind TEXT NOT NULL CHECK(kind IN ('jd','resume','transcript','notes')),
  filename TEXT NOT NULL,
  mime TEXT NOT NULL,
  sha256 TEXT NOT NULL CHECK(length(sha256)=64),
  bytes INTEGER NOT NULL CHECK(bytes>=0),
  consent_tier TEXT NOT NULL,
  retention_until TEXT,
  created_at TEXT NOT NULL,
  event_hash TEXT,
  prev_hash TEXT
);

CREATE TABLE IF NOT EXISTS artifacts (
  id TEXT PRIMARY KEY,
  source_id TEXT NOT NULL,
  run_id TEXT NOT NULL,
  parser TEXT CHECK(parser IN ('mineru','pymupdf','tesseract_ocr')),
  parser_version TEXT,
  clean_text_ref TEXT,
  cleanse TEXT,
  event_hash TEXT,
  prev_hash TEXT
);

CREATE TABLE IF NOT EXISTS evidence_spans (
  id TEXT PRIMARY KEY,
  artifact_id TEXT,
  candidate_id TEXT,
  quote TEXT CHECK(length(quote)>=8 AND length(quote)<=600),
  loc TEXT,
  granularity TEXT,
  confidence REAL,
  verified TEXT,
  supersedes_id TEXT,
  event_hash TEXT,
  prev_hash TEXT
);

CREATE TABLE IF NOT EXISTS claims (
  id TEXT PRIMARY KEY,
  candidate_id TEXT,
  text TEXT,
  span_ids TEXT,
  polarity TEXT,
  extractor TEXT,
  supersedes_id TEXT,
  event_hash TEXT,
  prev_hash TEXT
);

CREATE TABLE IF NOT EXISTS assessments (
  id TEXT PRIMARY KEY,
  candidate_id TEXT,
  requirement_id TEXT,
  grade TEXT,
  uncertainty TEXT,
  p REAL,
  confidence REAL,
  claim_ids TEXT,
  policy_hash TEXT,
  judge TEXT,
  supersedes_id TEXT,
  event_hash TEXT,
  prev_hash TEXT
);

CREATE TABLE IF NOT EXISTS report_answers (
  id TEXT PRIMARY KEY,
  kind TEXT,
  candidate_ids TEXT,
  assessment_ids TEXT,
  body_md TEXT,
  version INTEGER,
  prev_version_id TEXT,
  version_diff TEXT,
  event_hash TEXT
);

CREATE TABLE IF NOT EXISTS run_versions (
  run_id TEXT PRIMARY KEY,
  code_sha TEXT,
  policy_hash TEXT,
  policy_version TEXT,
  models TEXT
);

CREATE TABLE IF NOT EXISTS approver_logs (
  id TEXT PRIMARY KEY,
  run_id TEXT,
  actor TEXT,
  action TEXT,
  target_ids TEXT,
  rationale TEXT,
  time_on_evidence_s INTEGER
);

-- Generic ledger event chain (hash-chained journal mirror).
CREATE TABLE IF NOT EXISTS ledger_events (
  seq INTEGER PRIMARY KEY AUTOINCREMENT,
  event_hash TEXT NOT NULL,
  prev_hash TEXT,
  canonical_json TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

-- FTS5 over evidence quotes (BM25 lexical path, Report §7 DQ8).
CREATE VIRTUAL TABLE IF NOT EXISTS evidence_spans_fts USING fts5(
  quote, content='evidence_spans', content_rowid='rowid',
  tokenize='unicode61'
);

-- Append-only triggers: reject UPDATE/DELETE on ledger tables.
CREATE TRIGGER IF NOT EXISTS trg_no_update_source_records BEFORE UPDATE ON source_records BEGIN SELECT RAISE(ABORT, 'append-only: UPDATE rejected'); END;
CREATE TRIGGER IF NOT EXISTS trg_no_delete_source_records BEFORE DELETE ON source_records BEGIN SELECT RAISE(ABORT, 'append-only: DELETE rejected'); END;
CREATE TRIGGER IF NOT EXISTS trg_no_update_artifacts BEFORE UPDATE ON artifacts BEGIN SELECT RAISE(ABORT, 'append-only: UPDATE rejected'); END;
CREATE TRIGGER IF NOT EXISTS trg_no_delete_artifacts BEFORE DELETE ON artifacts BEGIN SELECT RAISE(ABORT, 'append-only: DELETE rejected'); END;
CREATE TRIGGER IF NOT EXISTS trg_no_update_evidence_spans BEFORE UPDATE ON evidence_spans BEGIN SELECT RAISE(ABORT, 'append-only: UPDATE rejected'); END;
CREATE TRIGGER IF NOT EXISTS trg_no_delete_evidence_spans BEFORE DELETE ON evidence_spans BEGIN SELECT RAISE(ABORT, 'append-only: DELETE rejected'); END;
CREATE TRIGGER IF NOT EXISTS trg_no_update_claims BEFORE UPDATE ON claims BEGIN SELECT RAISE(ABORT, 'append-only: UPDATE rejected'); END;
CREATE TRIGGER IF NOT EXISTS trg_no_delete_claims BEFORE DELETE ON claims BEGIN SELECT RAISE(ABORT, 'append-only: DELETE rejected'); END;
CREATE TRIGGER IF NOT EXISTS trg_no_update_assessments BEFORE UPDATE ON assessments BEGIN SELECT RAISE(ABORT, 'append-only: UPDATE rejected'); END;
CREATE TRIGGER IF NOT EXISTS trg_no_delete_assessments BEFORE DELETE ON assessments BEGIN SELECT RAISE(ABORT, 'append-only: DELETE rejected'); END;
CREATE TRIGGER IF NOT EXISTS trg_no_update_report_answers BEFORE UPDATE ON report_answers BEGIN SELECT RAISE(ABORT, 'append-only: UPDATE rejected'); END;
CREATE TRIGGER IF NOT EXISTS trg_no_delete_report_answers BEFORE DELETE ON report_answers BEGIN SELECT RAISE(ABORT, 'append-only: DELETE rejected'); END;
