import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import {
  getQuestions,
  generateQuestions,
  addInterviewNote,
  type Question,
} from "../lib/api";

export function InterviewPage() {
  const { candidateId } = useParams<{ candidateId: string }>();
  const [questions, setQuestions] = useState<Question[]>([]);
  const [note, setNote] = useState("");
  const [notes, setNotes] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [genLoading, setGenLoading] = useState(false);
  const [noteLoading, setNoteLoading] = useState(false);

  useEffect(() => {
    let cancelled = false;
    if (!candidateId) return;
    setLoading(true);
    getQuestions(candidateId)
      .then((d) => {
        if (!cancelled) { setQuestions(d.questions); setLoading(false); }
      })
      .catch(() => {
        // 404 = no questions generated yet — not a fatal error in this view
        if (!cancelled) { setQuestions([]); setLoading(false); }
      });
    return () => { cancelled = true; };
  }, [candidateId]);

  async function handleGenerate() {
    if (!candidateId) return;
    setGenLoading(true);
    setError(null);
    try {
      const d = await generateQuestions(candidateId);
      setQuestions(d.questions);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setGenLoading(false);
    }
  }

  async function handleSubmitNote(e: React.FormEvent) {
    e.preventDefault();
    if (!candidateId || !note.trim()) return;
    setNoteLoading(true);
    setError(null);
    try {
      const d = await addInterviewNote(candidateId, note);
      setNotes((prev) => [...prev, `${d.status}: ${note}`]);
      setNote("");
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setNoteLoading(false);
    }
  }

  if (loading) return <div className="p-4 text-sm text-gray-500">Loading interview…</div>;

  return (
    <div className="max-w-4xl mx-auto p-4 space-y-6">
      <header className="border-b pb-4 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Interview — {candidateId}</h1>
          <Link to={`/candidates/${candidateId}`} className="text-blue-600 text-sm underline">
            ← Candidate detail
          </Link>
        </div>
      </header>

      <section className="bg-white rounded-lg border p-4 space-y-4">
        <div className="flex justify-between items-center">
          <h2 className="text-lg font-medium">Questions</h2>
          <button
            onClick={handleGenerate}
            disabled={genLoading}
            className="px-3 py-1 bg-blue-600 text-white rounded text-sm disabled:opacity-50"
          >
            {genLoading ? "Generating…" : "Generate Questions"}
          </button>
        </div>
        {questions.length === 0 ? (
          <p className="text-gray-500 text-sm">No questions yet. Click generate to create gap-conditioned questions.</p>
        ) : (
          <ul className="space-y-2">
            {questions.map((q, i) => (
              <li key={q.question_id ?? i} className="border-l-2 pl-3 text-sm space-y-0.5">
                <div className="font-medium">Q{i + 1}:</div>
                <div>{q.question}</div>
                {q.gap_text && <div className="text-xs text-gray-500">gap: {q.gap_text}</div>}
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="bg-white rounded-lg border p-4 space-y-3">
        <h2 className="text-lg font-medium">Interview Notes</h2>
        <form onSubmit={handleSubmitNote} className="flex gap-2">
          <textarea
            value={note}
            onChange={(e) => setNote(e.target.value)}
            placeholder="Type your interview notes…"
            className="flex-1 min-h-[80px] p-2 border rounded text-sm"
            rows={4}
          />
          <button
            type="submit"
            disabled={noteLoading || !note.trim()}
            className="px-4 py-2 bg-green-600 text-white rounded text-sm self-end disabled:opacity-50"
          >
            {noteLoading ? "Saving…" : "Save Note"}
          </button>
        </form>
        {notes.length > 0 && (
          <div className="space-y-1">
            {notes.map((n, i) => (
              <p key={i} className="text-sm text-gray-600 bg-gray-50 p-2 rounded">{n}</p>
            ))}
          </div>
        )}
      </section>

      {error && (
        <div className="bg-red-100 border border-red-400 rounded-lg p-4 text-red-800">
          Error: {error}
        </div>
      )}
    </div>
  );
}