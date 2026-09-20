export type Health = { status: string; version: string; wal_mode?: string };

export async function health(): Promise<Health> {
  const r = await fetch("/api/health" /* proxied to :8000 in dev */);
  if (!r.ok) throw new Error(`health ${r.status}`);
  return (await r.json()) as Health;
}

export type Requirement = {
  id: string;
  text: string;
  cls: "hard" | "soft";
  weight: number;
  gate: "hard" | "soft";
  evidence_needed?: string;
};

export type CreateJobResponse = {
  job_id: string;
  run_id: string;
  requirements: Requirement[];
};

export async function createJob(payload: { title: string; jd_text?: string }): Promise<CreateJobResponse> {
  const r = await fetch("/api/jobs", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!r.ok) throw new Error(`createJob ${r.status}`);
  return r.json() as Promise<CreateJobResponse>;
}

export type IngestCandidatesResponse = {
  candidate_ids: string[];
  quarantined: string[];
};

export async function ingestCandidates(jobId: string, files: File[]): Promise<IngestCandidatesResponse> {
  const fd = new FormData();
  files.forEach((f) => fd.append("files", f));
  const r = await fetch(`/api/jobs/${jobId}/candidates:ingest`, { method: "POST", body: fd });
  if (!r.ok) throw new Error(`ingest ${r.status}`);
  return r.json() as Promise<IngestCandidatesResponse>;
}

// ---- New: job list + combined intake ----

export type JobSummary = {
  job_id: string;
  run_id: string;
  requirements: Requirement[];
};

export async function getJobs(): Promise<JobSummary[]> {
  const r = await fetch("/api/jobs");
  if (!r.ok) throw new Error(`getJobs ${r.status}`);
  return r.json() as Promise<JobSummary[]>;
}

export type CreateJobAndIngestResponse = {
  job: CreateJobResponse;
  ingest: IngestCandidatesResponse;
};

export async function createJobAndIngest(payload: {
  title: string;
  jd_text?: string;
  files: File[];
}): Promise<CreateJobAndIngestResponse> {
  const job = await createJob({ title: payload.title, jd_text: payload.jd_text });
  const ingest = await ingestCandidates(job.job_id, payload.files);
  return { job, ingest };
}

// ---- Shortlist ----

export type RankedCandidate = {
  candidate_id: string;
  tier: string;
  composite: number;
  needs_review: boolean;
  per_req: Record<string, { grade: string; confidence: number }>;
};

export type ShortlistResponse = {
  job_id: string;
  ranked: RankedCandidate[];
  needs_review_rate: number;
  cohorts: Record<string, string[]>;
};

export async function getShortlist(jobId: string): Promise<ShortlistResponse> {
  const r = await fetch(`/api/jobs/${jobId}/shortlist`);
  if (!r.ok) throw new Error(`shortlist ${r.status}`);
  return r.json() as Promise<ShortlistResponse>;
}

// ---- Candidate ----

export type Screening = {
  candidate_id: string;
  run_id: string;
  job_id?: string;
  tier: string;
  composite: number;
  needs_review: boolean;
};

export type CandidateInfo = {
  candidate_id: string;
  screenings: Screening[];
};

export async function getCandidate(candidateId: string): Promise<CandidateInfo> {
  const r = await fetch(`/api/candidates/${candidateId}`);
  if (!r.ok) throw new Error(`candidate ${r.status}`);
  return r.json() as Promise<CandidateInfo>;
}

// ---- Evidence ----

export type EvidenceSpan = {
  quote: string;
  page: number;
  line: number;
};

export type EvidenceJudgment = {
  p: number;
  confidence: number;
  grade: string;
};

export type EvidenceBox = {
  req: string;
  span: EvidenceSpan;
  judgment: EvidenceJudgment;
  state: string;
  conf: number;
};

export type EvidenceResponse = {
  candidate_id: string;
  run_id: string;
  boxes: EvidenceBox[];
};

export async function getEvidence(candidateId: string): Promise<EvidenceResponse> {
  const r = await fetch(`/api/candidates/${candidateId}/evidence`);
  if (!r.ok) throw new Error(`evidence ${r.status}`);
  return r.json() as Promise<EvidenceResponse>;
}

// ---- Questions / Interview ----

export type Question = {
  question_id: string;
  requirement_id: string;
  gap_text: string;
  question: string;
};

export type QuestionsResponse = {
  candidate_id: string;
  questions: Question[];
};

export async function getQuestions(candidateId: string): Promise<QuestionsResponse> {
  const r = await fetch(`/api/candidates/${candidateId}/questions`);
  if (!r.ok) throw new Error(`questions ${r.status}`);
  return r.json() as Promise<QuestionsResponse>;
}

export async function generateQuestions(candidateId: string): Promise<QuestionsResponse> {
  const r = await fetch(`/api/candidates/${candidateId}/questions`, { method: "POST" });
  if (!r.ok) throw new Error(`generateQuestions ${r.status}`);
  return r.json() as Promise<QuestionsResponse>;
}

export type InterviewNoteResponse = {
  note_id: string;
  status: string;
};

export async function addInterviewNote(candidateId: string, note: string): Promise<InterviewNoteResponse> {
  const r = await fetch(`/api/candidates/${candidateId}/interview-notes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ note }),
  });
  if (!r.ok) throw new Error(`interview-notes ${r.status}`);
  return r.json() as Promise<InterviewNoteResponse>;
}

// ---- Report ----

export type ReportSection = {
  title: string;
  content: string;
};

export type ReportResponse = {
  job_id: string;
  report: { sections: ReportSection[] };
};

export async function getReport(jobId: string): Promise<ReportResponse> {
  const r = await fetch(`/api/jobs/${jobId}/report`);
  if (!r.ok) throw new Error(`report ${r.status}`);
  return r.json() as Promise<ReportResponse>;
}

// ---- Query ----

export type QueryResult = {
  candidate_id: string;
  score: number;
  tier: string;
};

export type QueryResponse = {
  job_id: string;
  results: QueryResult[];
};

export async function getQuery(jobId: string, filter: string, value: string): Promise<QueryResponse> {
  const r = await fetch(`/api/jobs/${jobId}/query?filter=${filter}&value=${value}`);
  if (!r.ok) throw new Error(`query ${r.status}`);
  return r.json() as Promise<QueryResponse>;
}

// ---- Audit pack ----

export type AuditEvent = {
  event: string;
  timestamp: string;
  detail: string;
};

export type AuditPackResponse = {
  job_id: string;
  audit_events: AuditEvent[];
  count: number;
};

export async function getAuditPack(jobId: string): Promise<AuditPackResponse> {
  const r = await fetch(`/api/jobs/${jobId}/audit-pack`);
  if (!r.ok) throw new Error(`audit-pack ${r.status}`);
  return r.json() as Promise<AuditPackResponse>;
}