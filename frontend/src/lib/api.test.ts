import { describe, expect, it, vi } from "vitest";
import { health, createJob, ingestCandidates } from "./api";

describe("api", () => {
  it("health returns ok", async () => {
    vi.stubGlobal(
      "fetch",
      async () =>
        new Response(JSON.stringify({ status: "ok", version: "0.1.0" }), { status: 200 }),
    );
    const j = await health();
    expect(j.status).toBe("ok");
    vi.unstubAllGlobals();
  });

  it("createJob posts jd_text", async () => {
    vi.stubGlobal(
      "fetch",
      async () =>
        new Response(
          JSON.stringify({ job_id: "job_1", requirements: [{ id: "REQ-01", text: "Python", cls: "hard", weight: 0.5, gate: "hard" }] }),
          { status: 201 },
        ),
    );
    const j = await createJob({ title: "T", jd_text: "Python" });
    expect(j.job_id).toBe("job_1");
    expect(j.requirements[0].id).toBe("REQ-01");
    vi.unstubAllGlobals();
  });

  it("ingestCandidates returns quarantined", async () => {
    vi.stubGlobal(
      "fetch",
      async () =>
        new Response(JSON.stringify({ candidate_ids: ["cand_1"], quarantined: ["cand_2"] }), { status: 200 }),
    );
    const r = await ingestCandidates("job_1", [new File(["hi"], "cv.txt")]);
    expect(r.quarantined).toContain("cand_2");
    vi.unstubAllGlobals();
  });
});