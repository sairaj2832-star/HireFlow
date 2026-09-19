import { useEffect, useState } from "react";
import { Route, Routes } from "react-router-dom";
import { health } from "./lib/api";

function Placeholder({ name }: { name: string }) {
  return <h1>{name}</h1>;
}

export default function App() {
  const [backend, setBackend] = useState<string>("checking…");

  useEffect(() => {
    let cancelled = false;
    health()
      .then((h) => {
        if (!cancelled) setBackend(`${h.status} v${h.version}`);
      })
      .catch(() => {
        if (!cancelled) setBackend("unreachable (start backend :8000)");
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div className="p-4">
      <header className="mb-4">
        <span className="text-sm text-gray-600">HireFlow B0 — backend: {backend}</span>
      </header>
      <Routes>
        <Route path="/" element={<Placeholder name="dashboard" />} />
        <Route path="/jd" element={<Placeholder name="jd" />} />
        <Route path="/candidates/:id" element={<Placeholder name="candidate-detail" />} />
        <Route path="/interview" element={<Placeholder name="interview" />} />
        <Route path="/query" element={<Placeholder name="query" />} />
        <Route path="/audit" element={<Placeholder name="audit" />} />
        <Route path="/policy" element={<Placeholder name="policy" />} />
        <Route path="/approvals" element={<Placeholder name="approvals" />} />
      </Routes>
    </div>
  );
}
