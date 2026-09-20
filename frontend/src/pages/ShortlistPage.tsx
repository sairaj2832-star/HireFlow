import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getShortlist, type RankedCandidate } from "../lib/api";

export function ShortlistPage() {
  const { jobId } = useParams<{ jobId: string }>();
  const [data, setData] = useState<Awaited<ReturnType<typeof getShortlist>> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    if (!jobId) return;
    setLoading(true);
    getShortlist(jobId)
      .then((d) => { if (!cancelled) { setData(d); setLoading(false); } })
      .catch((err) => { if (!cancelled) { setError((err as Error).message); setLoading(false); } });
    return () => { cancelled = true; };
  }, [jobId]);

  if (loading) return <div className="p-4 text-sm text-gray-500">Loading shortlist…</div>;
  if (error) return <div className="p-4 text-red-600">Error: {error}</div>;
  if (!data) return <div className="p-4 text-gray-500">No job selected</div>;

  const cohortCount = data.cohorts ? Object.keys(data.cohorts).length : 0;

  return (
    <div className="max-w-5xl mx-auto p-4 space-y-6">
      <header className="border-b pb-4">
        <h1 className="text-2xl font-semibold">Shortlist — {data.job_id}</h1>
        <p className="text-sm text-gray-600">
          Needs-review rate: {Math.round((data.needs_review_rate ?? 0) * 100)}% | Cohorts: {cohortCount}
        </p>
      </header>

      {data.ranked.length === 0 ? (
        <div className="bg-white rounded-lg border p-8 text-center text-gray-500 text-sm">
          No candidates screened yet.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {data.ranked.map((c: RankedCandidate) => (
            <Link
              key={c.candidate_id}
              to={`/candidates/${c.candidate_id}`}
              className="border rounded-lg p-4 bg-white space-y-2 hover:shadow hover:border-blue-300 transition"
            >
              <div className="flex justify-between items-center">
                <span className="font-semibold text-sm">{c.candidate_id}</span>
                <span className={`px-2 py-0.5 text-xs rounded ${
                  c.tier === "A" ? "bg-green-100 text-green-800" :
                  c.tier === "B" ? "bg-yellow-100 text-yellow-800" :
                  "bg-red-100 text-red-800"
                }`}>
                  {c.tier}
                </span>
              </div>
              <div className="text-sm text-gray-600">composite: {c.composite.toFixed(3)}</div>
              {c.needs_review && (
                <span className="px-2 py-0.5 text-xs rounded bg-amber-100 text-amber-800">NEEDS REVIEW</span>
              )}
              <div className="text-xs text-gray-500 space-y-1">
                {Object.entries(c.per_req).map(([req, grad]) => (
                  <div key={req} className="flex justify-between">
                    <span className="truncate mr-2">{req}</span>
                    <span className={grad.grade === "SUPPORTED" ? "text-green-600" : "text-red-600"}>{grad.grade}</span>
                  </div>
                ))}
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}