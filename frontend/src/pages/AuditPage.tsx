import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getAuditPack, type AuditEvent } from "../lib/api";

export function AuditPage() {
  const { jobId } = useParams<{ jobId: string }>();
  const [data, setData] = useState<Awaited<ReturnType<typeof getAuditPack>> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    if (!jobId) return;
    setLoading(true);
    getAuditPack(jobId)
      .then((d) => { if (!cancelled) { setData(d); setLoading(false); } })
      .catch((err) => { if (!cancelled) { setError((err as Error).message); setLoading(false); } });
    return () => { cancelled = true; };
  }, [jobId]);

  if (loading) return <div className="p-4 text-sm text-gray-500">Loading audit pack…</div>;
  if (error) return <div className="p-4 text-red-600">Error: {error}</div>;
  if (!data) return <div className="p-4 text-gray-500">No audit pack found</div>;

  return (
    <div className="max-w-4xl mx-auto p-4 space-y-6">
      <header className="border-b pb-4 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Audit Pack — {data.job_id}</h1>
          <p className="text-sm text-gray-600">{data.count} audit event(s)</p>
        </div>
        <Link to={`/shortlist/${data.job_id}`} className="text-blue-600 text-sm underline">
          ← Shortlist
        </Link>
      </header>

      {data.audit_events.length === 0 ? (
        <div className="bg-white rounded-lg border p-8 text-center text-gray-500 text-sm">
          No audit events recorded yet.
        </div>
      ) : (
        <div className="bg-white rounded-lg border divide-y">
          {data.audit_events.map((ev: AuditEvent, i) => (
            <div key={i} className="p-3 flex gap-3 text-sm">
              <span className="font-mono text-xs text-gray-500 shrink-0">
                {ev.timestamp ? new Date(ev.timestamp).toLocaleTimeString() : ""}
              </span>
              <div className="space-y-0.5">
                <div className="font-medium text-gray-800">{ev.event}</div>
                {ev.detail && <div className="text-gray-600 text-xs">{ev.detail}</div>}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}