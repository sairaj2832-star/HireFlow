import { describe, expect, it, vi } from "vitest";
import { health } from "./api";

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
});
