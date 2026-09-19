export type Health = { status: string; version: string; wal_mode?: string };

export async function health(): Promise<Health> {
  const r = await fetch("/api/health" /* proxied to :8000 in dev */);
  if (!r.ok) throw new Error(`health ${r.status}`);
  return (await r.json()) as Health;
}
