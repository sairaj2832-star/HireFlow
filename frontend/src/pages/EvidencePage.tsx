import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getEvidence, type EvidenceBox as EvidenceBoxType } from "../lib/api";
import { EvidenceBox } from "../components/EvidenceBox";

export function EvidencePage() {
  const { candidateId } = useParams<{ candidateId: string }>();
  const [data, setData] = useState<Awaited<ReturnType<typeof getEvidence>> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    if (!candidateId) return;
    setLoading(true);
    getEvidence(candidateId)
      .then((d) => { if (!cancelled) { setData(d); setLoading(false); } })
      .catch((err) => { if (!cancelled) { setError((err as Error).message); setLoading(false); } });
    return () => { cancelled = true; };
  }, [candidateId]);

  if (loading) return <div className="p-4 text-sm text-gray-500">Loading evidence…</div>;
  if (error) return <div className="p-4 text-red-600">Error: {error}</div>;
  if (!data) return <div className="p-4 text-gray-500">No evidence found</div>;

  return (
    <div className="max-w-4xl mx-auto p-4 space-y-6">
      <header className="border-b pb-4 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Evidence — {data.candidate_id}</h1>
          <p className="text-sm text-gray-600">Run: {data.run_id} | {data.boxes.length} box(es)</p>
        </div>
        <Link to={`/candidates/${data.candidate_id}`} className="text-blue-600 text-sm underline">
          ← Candidate detail
        </Link>
      </header>

      {data.boxes.length === 0 ? (
        <div className="bg-white rounded-lg border p-8 text-center text-gray-500 text-sm">
          No evidence boxes for this candidate yet.
        </div>
      ) : (
        <div className="space-y-4">
          {data.boxes.map((box: EvidenceBoxType, i) => (
            <div key={i} className="space-y-1">
              <div className="text-xs text-gray-500 font-mono">req: {box.req}</div>
              <EvidenceBox
                quote={box.span.quote}
                page={box.span.page}
                line={box.span.line}
                conf={box.conf}
                state={box.state}
                grade={box.judgment.grade}
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}