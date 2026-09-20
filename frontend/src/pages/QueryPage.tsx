import { useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getQuery, type QueryResult } from "../lib/api";

type FilterType = "tier" | "verified";

export function QueryPage() {
  const { jobId } = useParams<{ jobId: string }>();
  const [filterType, setFilterType] = useState<FilterType>("tier");
  const [filterValue, setFilterValue] = useState("A");
  const [data, setData] = useState<Awaited<ReturnType<typeof getQuery>> | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleQuery(e: React.FormEvent) {
    e.preventDefault();
    if (!jobId) return;
    setLoading(true);
    setError(null);
    try {
      const d = await getQuery(jobId, filterType, filterValue);
      setData(d);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-4xl mx-auto p-4 space-y-6">
      <header className="border-b pb-4 flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Query — {jobId}</h1>
        <Link to={`/shortlist/${jobId}`} className="text-blue-600 text-sm underline">
          ← Shortlist
        </Link>
      </header>

      <form onSubmit={handleQuery} className="bg-white rounded-lg border p-4 space-y-3">
        <div className="flex gap-3 items-end">
          <div>
            <label className="text-sm text-gray-600 block mb-1">Filter</label>
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value as FilterType)}
              className="border rounded p-1 text-sm"
            >
              <option value="tier">Tier</option>
              <option value="verified">Verified</option>
            </select>
          </div>
          <div>
            <label className="text-sm text-gray-600 block mb-1">Value</label>
            <input
              value={filterValue}
              onChange={(e) => setFilterValue(e.target.value)}
              className="border rounded p-1 text-sm w-32"
              placeholder="e.g. A"
            />
          </div>
          <button type="submit" disabled={loading} className="px-4 py-1.5 bg-blue-600 text-white rounded text-sm disabled:opacity-50">
            {loading ? "Querying…" : "Query"}
          </button>
        </div>
      </form>

      {error && (
        <div className="bg-red-100 border border-red-400 rounded-lg p-4 text-red-800">
          Error: {error}
        </div>
      )}

      {data && (
        <section className="bg-white rounded-lg border p-4 space-y-3">
          <h2 className="text-lg font-medium">Results ({data.results.length})</h2>
          {data.results.length === 0 ? (
            <p className="text-gray-500 text-sm">No results found</p>
          ) : (
            <div className="space-y-2">
              {data.results.map((r: QueryResult, i) => (
                <div key={i} className="flex justify-between items-center border-b pb-2">
                  <span className="font-mono text-sm">{r.candidate_id}</span>
                  <div className="flex gap-3 text-sm">
                    <span className={`px-2 py-0.5 rounded ${
                      r.tier === "A" ? "bg-green-100 text-green-800" :
                      r.tier === "B" ? "bg-yellow-100 text-yellow-800" :
                      "bg-red-100 text-red-800"
                    }`}>{r.tier}</span>
                    <span>score: {r.score.toFixed(3)}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      )}
    </div>
  );
}