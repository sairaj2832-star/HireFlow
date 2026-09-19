type Props = { quote: string; page: number; line: number; conf: number; state: string };

export function EvidenceBox({ quote, page, line, conf, state }: Props) {
  return (
    <div data-testid="evidence-box" className="border p-2 rounded">
      <p>{quote}</p>
      <span>
        p{page}:L{line} conf={conf} {state}
      </span>
    </div>
  );
}
