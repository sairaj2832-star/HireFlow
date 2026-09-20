import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getCandidate, type Screening } from "../lib/api";

export function CandidateDetailPage() {
  const { candidateId } = useParams<{ candidateId: string }>();
  const [data, setData] = useState<Awaited<ReturnType<typeof getCandidate>> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    if (!candidateId) return;
    setLoading(true);
    getCandidate(candidateId)
      .then((d) => { if (!cancelled) { setData(d); setLoading(false); } })
      .catch((err) => { if (!cancelled) { setError((err as Error).message); setLoading(false); } });
    return () => { cancelled = true; };
  }, [candidateId]);

  if (loading) return <div className="p-4 text-sm text-gray-500">Loading candidate…</div>;
  if (error) return <div className="p-4 text-red-600">Error: {error}</div>;
  if (!data) return <div className="p-4 text-gray-500">Candidate not found</div>;

  return (
    <div className="max-w-4xl mx-auto p-4 space-y-6">
      <header className="border-b pb-4">
        <h1 className="text-2xl font-semibold">Candidate: {data.candidate_id}</h1>
        <div className="mt-2 flex gap-3">
          <Link to={`/evidence/${data.candidate_id}`} className="text-blue-600 text-sm underline">View Evidence →</Link>
          <Link to={`/interview/${data.candidate_id}`} className="text-green-600 text-sm underline">Interview →</Link>
        </div>
      </header>

      <section className="bg-white rounded-lg border p-4">
        <h2 className="text-lg font-medium mb-3">Screenings</h2>
        {data.screenings.length === 0 ? (
          <p className="text-gray-500 text-sm">No screenings yet</p>
        ) : (
          <div className="space-y-3">
            {data.screenings.map((s: Screening, i) => (
              <div key={i} className="flex flex-wrap justify-between items-center border-b pb-2 gap-2">
                <div>
                  <span className="font-mono text-xs text-gray-500">{s.run_id}</span>
                  <span className="ml-3 text-xs text-gray-400">job {s.job_id}</span>
                </div>
                <div className="flex items-center gap-3">
                  <span className={`px-2 py-0.5 text-xs rounded ${
                    s.tier === "A" ? "bg-green-100 text-green-800" :
                    s.tier === "B" ? "bg-yellow-100 text-yellow-800" :
                    "bg-red-100 text-red-800"
                  }`}>{s.tier}</span>
                  <span className="text-sm">composite: {s.composite.toFixed(3)}</span>
                  {s.needs_review && <span className="px-2 py-0.5 text-xs rounded bg-amber-100 text-amber-800">REVIEW</span>}
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      <nav className="flex gap-3">
        <Link to={`/evidence/${candidateId}`} className="px-4 py-2 bg-blue-600 text-white rounded text-sm">Evidence</Link>
        <Link to={`/interview/${candidateId}`} className="px-4 py-2 bg-green-600 text-white rounded text-sm">Interview</Link>
      </nav>
    </div>
  );
}