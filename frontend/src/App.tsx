import { useEffect, useState } from "react";
import { Route, Routes } from "react-router-dom";
import { health } from "./lib/api";
import { IntakePage } from "./pages/IntakePage";
import { DashboardPage } from "./pages/DashboardPage";
import { ShortlistPage } from "./pages/ShortlistPage";
import { CandidateDetailPage } from "./pages/CandidateDetailPage";
import { EvidencePage } from "./pages/EvidencePage";
import { InterviewPage } from "./pages/InterviewPage";
import { ReportPage } from "./pages/ReportPage";
import { QueryPage } from "./pages/QueryPage";
import { AuditPage } from "./pages/AuditPage";

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
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b px-4 py-2 flex items-center justify-between">
        <span className="font-semibold text-gray-800">HireFlow</span>
        <span className="text-xs text-gray-500">backend: {backend}</span>
      </header>
      <Routes>
        <Route path="/" element={<IntakePage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/shortlist/:jobId" element={<ShortlistPage />} />
        <Route path="/candidates/:candidateId" element={<CandidateDetailPage />} />
        <Route path="/evidence/:candidateId" element={<EvidencePage />} />
        <Route path="/interview/:candidateId" element={<InterviewPage />} />
        <Route path="/report/:jobId" element={<ReportPage />} />
        <Route path="/query/:jobId" element={<QueryPage />} />
        <Route path="/audit/:jobId" element={<AuditPage />} />
      </Routes>
    </div>
  );
}