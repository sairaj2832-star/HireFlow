import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getReport, type ReportSection } from "../lib/api";

export function ReportPage() {
  const { jobId } = useParams<{ jobId: string }>();
  const [data, setData] = useState<Awaited<ReturnType<typeof getReport>> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    if (!jobId) return;
    setLoading(true);
    getReport(jobId)
      .then((d) => { if (!cancelled) { setData(d); setLoading(false); } })
      .catch((err) => { if (!cancelled) { setError((err as Error).message); setLoading(false); } });
    return () => { cancelled = true; };
  }, [jobId]);

  if (loading) return <div className="p-4 text-sm text-gray-500">Loading report…</div>;
  if (error) return <div className="p-4 text-red-600">Error: {error}</div>;
  if (!data) return <div className="p-4 text-gray-500">No report found</div>;

  return (
    <div className="max-w-4xl mx-auto p-4 space-y-6">
      <header className="border-b pb-4 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Report — {data.job_id}</h1>
        </div>
        <Link to={`/shortlist/${data.job_id}`} className="text-blue-600 text-sm underline">
          ← Shortlist
        </Link>
      </header>

      {data.report.sections.length === 0 ? (
        <div className="bg-white rounded-lg border p-8 text-center text-gray-500 text-sm">
          No report sections available yet.
        </div>
      ) : (
        <div className="space-y-4">
          {data.report.sections.map((section: ReportSection, i) => (
            <section key={i} className="bg-white rounded-lg border p-4 space-y-2">
              <h2 className="text-lg font-medium text-gray-800">{section.title}</h2>
              <p className="text-sm text-gray-600 whitespace-pre-wrap">{section.content}</p>
            </section>
          ))}
        </div>
      )}
    </div>
  );
}