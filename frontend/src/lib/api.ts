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