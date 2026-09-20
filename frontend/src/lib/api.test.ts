import { describe, expect, it, vi } from "vitest";
import {
  health,
  createJob,
  ingestCandidates,
  getJobs,
  createJobAndIngest,
  getShortlist,
  getCandidate,
  getEvidence,
  getQuestions,
  generateQuestions,
  addInterviewNote,
  getReport,
  getQuery,
  getAuditPack,
} from "./api";

function mockFetch(json: unknown, status = 200) {
  return vi.fn(async () => new Response(JSON.stringify(json), { status }));
}

describe("api", () => {
  it("health returns ok", async () => {
    vi.stubGlobal("fetch", mockFetch({ status: "ok", version: "0.1.0" }));
    const j = await health();
    expect(j.status).toBe("ok");
    vi.unstubAllGlobals();
  });

  it("createJob posts jd_text", async () => {
    vi.stubGlobal(
      "fetch",
      mockFetch({ job_id: "job_1", requirements: [{ id: "REQ-01", text: "Python", cls: "hard", weight: 0.5, gate: "hard" }] }, 201),
    );
    const j = await createJob({ title: "T", jd_text: "Python" });
    expect(j.job_id).toBe("job_1");
    expect(j.requirements[0].id).toBe("REQ-01");
    vi.unstubAllGlobals();
  });

  it("ingestCandidates returns quarantined", async () => {
    vi.stubGlobal("fetch", mockFetch({ candidate_ids: ["cand_1"], quarantined: ["cand_2"] }));
    const r = await ingestCandidates("job_1", [new File(["hi"], "cv.txt")]);
    expect(r.quarantined).toContain("cand_2");
    vi.unstubAllGlobals();
  });

  it("getJobs lists jobs", async () => {
    vi.stubGlobal(
      "fetch",
      mockFetch([{ job_id: "job_1", run_id: "run_1", requirements: [] }]),
    );
    const jobs = await getJobs();
    expect(jobs[0].job_id).toBe("job_1");
    vi.unstubAllGlobals();
  });

  it("getShortlist returns ranked", async () => {
    vi.stubGlobal(
      "fetch",
      mockFetch({
        job_id: "job_1",
        ranked: [{ candidate_id: "c1", tier: "A", composite: 0.9, needs_review: false, per_req: {} }],
        needs_review_rate: 0.1,
        cohorts: {},
      }),
    );
    const s = await getShortlist("job_1");
    expect(s.ranked[0].candidate_id).toBe("c1");
    expect(s.ranked[0].tier).toBe("A");
    vi.unstubAllGlobals();
  });

  it("getCandidate returns screenings", async () => {
    vi.stubGlobal(
      "fetch",
      mockFetch({
        candidate_id: "c1",
        screenings: [{ candidate_id: "c1", run_id: "r1", tier: "A", composite: 0.9, needs_review: false }],
      }),
    );
    const c = await getCandidate("c1");
    expect(c.screenings[0].tier).toBe("A");
    vi.unstubAllGlobals();
  });

  it("getEvidence returns boxes", async () => {
    vi.stubGlobal(
      "fetch",
      mockFetch({
        candidate_id: "c1",
        run_id: "r1",
        boxes: [
          {
            req: "REQ-01",
            span: { quote: "built APIs", page: 1, line: 3 },
            judgment: { p: 0.9, confidence: 0.8, grade: "SUPPORTED" },
            state: "VERIFIED",
            conf: 0.8,
          },
        ],
      }),
    );
    const e = await getEvidence("c1");
    expect(e.boxes[0].span.quote).toBe("built APIs");
    expect(e.boxes[0].judgment.grade).toBe("SUPPORTED");
    vi.unstubAllGlobals();
  });

  it("getQuestions returns list", async () => {
    vi.stubGlobal(
      "fetch",
      mockFetch({
        candidate_id: "c1",
        questions: [{ question_id: "q1", requirement_id: "REQ-01", gap_text: "missing", question: "Describe scale?" }],
      }),
    );
    const q = await getQuestions("c1");
    expect(q.questions[0].question).toContain("scale");
    vi.unstubAllGlobals();
  });

  it("generateQuestions posts", async () => {
    const fetchMock = mockFetch(
      { candidate_id: "c1", questions: [{ question_id: "q1", requirement_id: "REQ-01", gap_text: "", question: "Q?" }] },
    );
    vi.stubGlobal("fetch", fetchMock);
    const q = await generateQuestions("c1");
    expect(q.questions[0].question).toBe("Q?");
    expect(fetchMock).toHaveBeenCalledWith("/api/candidates/c1/questions", { method: "POST" });
    vi.unstubAllGlobals();
  });

  it("addInterviewNote posts note", async () => {
    const fetchMock = mockFetch({ note_id: "n1", status: "stored" });
    vi.stubGlobal("fetch", fetchMock);
    const n = await addInterviewNote("c1", "notes here");
    expect(n.note_id).toBe("n1");
    expect(fetchMock).toHaveBeenCalledWith(
      "/api/candidates/c1/interview-notes",
      expect.objectContaining({ method: "POST", body: JSON.stringify({ note: "notes here" }) }),
    );
    vi.unstubAllGlobals();
  });

  it("getReport returns sections", async () => {
    vi.stubGlobal(
      "fetch",
      mockFetch({
        job_id: "job_1",
        report: { sections: [{ title: "Summary", content: "ok" }] },
      }),
    );
    const r = await getReport("job_1");
    expect(r.report.sections[0].title).toBe("Summary");
    vi.unstubAllGlobals();
  });

  it("getQuery returns results", async () => {
    vi.stubGlobal(
      "fetch",
      mockFetch({ job_id: "job_1", results: [{ candidate_id: "c1", score: 0.9, tier: "A" }] }),
    );
    const q = await getQuery("job_1", "tier", "A");
    expect(q.results[0].candidate_id).toBe("c1");
    vi.unstubAllGlobals();
  });

  it("getAuditPack returns events", async () => {
    vi.stubGlobal(
      "fetch",
      mockFetch({ job_id: "job_1", audit_events: [{ event: "SCREEN", timestamp: "", detail: "d" }], count: 1 }),
    );
    const a = await getAuditPack("job_1");
    expect(a.audit_events[0].event).toBe("SCREEN");
    vi.unstubAllGlobals();
  });

  it("createJobAndIngest composes job + ingest", async () => {
    let call = 0;
    vi.stubGlobal(
      "fetch",
      vi.fn(async (input: string, init?: RequestInit) => {
        call++;
        if (call === 1) {
          expect(init?.method).toBe("POST");
          return new Response(JSON.stringify({ job_id: "job_x", run_id: "run_x", requirements: [] }), { status: 201 });
        }
        expect(init?.method).toBe("POST");
        expect(input).toContain("/api/jobs/job_x/candidates:ingest");
        return new Response(JSON.stringify({ candidate_ids: ["c1"], quarantined: [] }), { status: 200 });
      }),
    );
    const r = await createJobAndIngest({ title: "T", files: [new File(["x"], "cv.txt")] });
    expect(r.job.job_id).toBe("job_x");
    expect(r.ingest.candidate_ids).toContain("c1");
    vi.unstubAllGlobals();
  });
});