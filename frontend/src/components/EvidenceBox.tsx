type Props = {
  quote: string;
  page: number;
  line: number;
  conf: number;
  state: string;
  grade?: string;
};

export function EvidenceBox({ quote, page, line, conf, state, grade }: Props) {
  return (
    <div data-testid="evidence-box" className="border p-3 rounded-lg bg-white space-y-1">
      <p className="text-sm italic text-gray-800">"{quote}"</p>
      <div className="flex flex-wrap gap-4 text-xs text-gray-500">
        <span>p{page}:L{line}</span>
        <span>conf={conf}</span>
        {grade && <span>grade={grade}</span>}
        <span className="px-1.5 py-0.5 rounded bg-gray-100">{state}</span>
      </div>
    </div>
  );
}