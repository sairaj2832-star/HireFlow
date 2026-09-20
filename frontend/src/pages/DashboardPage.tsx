import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { getJobs, type JobSummary } from "../lib/api";

export function DashboardPage() {
  const [jobs, setJobs] = useState<JobSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    getJobs()
      .then((j) => { if (!cancelled) { setJobs(j); setLoading(false); } })
      .catch((err) => { if (!cancelled) { setError((err as Error).message); setLoading(false); } });
    return () => { cancelled = true; };
  }, []);

  if (loading) return <div className="p-4">Loading jobs…</div>;
  if (error) return <div className="p-4 text-red-600">Error: {error}</div>;

  return (
    <div className="max-w-5xl mx-auto p-4 space-y-6">
      <header className="border-b pb-4 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">HireFlow Dashboard</h1>
          <p className="text-sm text-gray-600">Select a job to view its shortlist, evidence, interview, and report.</p>
        </div>
        <button
          onClick={() => navigate("/")}
          className="px-4 py-2 bg-blue-600 text-white rounded text-sm"
        >
          + New Job (Intake)
        </button>
      </header>

      {jobs.length === 0 ? (
        <div className="bg-white rounded-lg border p-8 text-center text-gray-500">
          No jobs yet. Click “+ New Job (Intake)” to create one.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {jobs.map((j) => (
            <div key={j.job_id} className="border rounded-lg p-4 bg-white space-y-3">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs text-gray-500">{j.job_id}</span>
                <span className="text-xs px-2 py-0.5 rounded bg-gray-100">{j.requirements.length} reqs</span>
              </div>
              <div className="text-sm text-gray-700 line-clamp-2">{j.run_id}</div>
              <div className="flex flex-wrap gap-2">
                <Link to={`/shortlist/${j.job_id}`} className="text-xs px-3 py-1.5 bg-blue-50 text-blue-700 rounded border border-blue-200">
                  Shortlist
                </Link>
                <Link to={`/report/${j.job_id}`} className="text-xs px-3 py-1.5 bg-green-50 text-green-700 rounded border border-green-200">
                  Report
                </Link>
                <Link to={`/query/${j.job_id}`} className="text-xs px-3 py-1.5 bg-purple-50 text-purple-700 rounded border border-purple-200">
                  Query
                </Link>
                <Link to={`/audit/${j.job_id}`} className="text-xs px-3 py-1.5 bg-gray-50 text-gray-700 rounded border border-gray-200">
                  Audit
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}