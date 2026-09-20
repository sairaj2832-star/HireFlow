import { useState } from "react";
import { createJob, ingestCandidates, type Requirement } from "../lib/api";

export function IntakePage() {
  const [job, setJob] = useState<{ job_id: string; run_id: string; requirements: Requirement[] } | null>(null);
  const [quarantined, setQuarantined] = useState<string[]>([]);
  const [jdText, setJdText] = useState("");
  const [candidateFiles, setCandidateFiles] = useState<File[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleCreateJob(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const j = await createJob({ title: "Backend Engineer", jd_text: jdText || undefined });
      setJob(j);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }

  async function handleIngestCandidates(e: React.FormEvent) {
    e.preventDefault();
    if (!job) {
      setError("Create a job first");
      return;
    }
    if (candidateFiles.length === 0) {
      setError("Select at least one candidate file");
      return;
    }
    setError(null);
    setLoading(true);
    try {
      const r = await ingestCandidates(job.job_id, candidateFiles);
      setQuarantined(r.quarantined);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-4xl mx-auto p-4 space-y-6">
      <header className="border-b pb-4">
        <h1 className="text-2xl font-semibold">Intake — JD + Candidate Pool</h1>
        <p className="text-sm text-gray-600">Upload a job description and candidate resumes. BRAKE1 will flag suspect uploads.</p>
      </header>

      {/* JD Upload */}
      <section className="bg-white rounded-lg border p-4 space-y-3">
        <h2 className="text-lg font-medium">Job Description</h2>
        <form onSubmit={handleCreateJob} className="space-y-3">
          <textarea
            value={jdText}
            onChange={(e) => setJdText(e.target.value)}
            placeholder="Paste JD text here… (or leave empty to upload file)"
            className="w-full min-h-[120px] p-2 border rounded font-mono text-sm"
            rows={6}
          />
          <button type="submit" disabled={loading} className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50">
            {loading ? "Creating…" : "Create Job & Parse Requirements"}
          </button>
        </form>
      </section>

      {/* Requirements List */}
      {job && (
        <section className="bg-white rounded-lg border p-4 space-y-3">
          <h2 className="text-lg font-medium">Requirements (REQ-01..N)</h2>
          <ul className="space-y-2">
            {job.requirements.map((r) => (
              <li key={r.id} className="text-sm border-l-2 pl-3 {r.gate === 'hard' ? 'border-red-500' : 'border-gray-400'}">
                <span className="font-mono text-blue-700">{r.id}</span>: {r.text}
                <span className="ml-2 px-1.5 py-0.5 text-xs rounded {r.gate === 'hard' ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-700'}">
                  {r.gate}
                </span>
                <span className="ml-2 text-xs text-gray-500">w={r.weight}</span>
              </li>
            ))}
          </ul>
        </section>
      )}

      {/* Candidate Pool Upload */}
      <section className="bg-white rounded-lg border p-4 space-y-3">
        <h2 className="text-lg font-medium">Candidate Pool</h2>
        <form onSubmit={handleIngestCandidates} className="space-y-3">
          <input
            type="file"
            multiple
            accept=".txt,.pdf"
            onChange={(e) => setCandidateFiles(Array.from(e.target.files || []))}
            className="w-full p-2 border rounded"
          />
          <p className="text-sm text-gray-600">
            Selected: {candidateFiles.length} file{candidateFiles.length !== 1 ? "s" : ""}
          </p>
          <button type="submit" disabled={loading || !job} className="px-4 py-2 bg-green-600 text-white rounded disabled:opacity-50">
            {loading ? "Ingesting…" : "Ingest Candidates"}
          </button>
        </form>
      </section>

      {/* Quarantine Banner */}
      {quarantined.length > 0 && (
        <div className="bg-amber-100 border border-amber-400 rounded-lg p-4">
          <div className="font-medium text-amber-900">⚠ Quarantined: {quarantined.join(", ")}</div>
          <div className="text-sm text-amber-800 mt-1">BRAKE1 suspect — hidden prompt / phantom text detected</div>
        </div>
      )}

      {error && (
        <div className="bg-red-100 border border-red-400 rounded-lg p-4 text-red-800">
          Error: {error}
        </div>
      )}
    </div>
  );
}