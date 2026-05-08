import type { EciEvidenceGapView } from "./eciVfeUiModel";

export function EciEvidenceGapPanel({
  caseId,
  gaps,
}: {
  caseId: string;
  gaps: EciEvidenceGapView[];
}) {
  return (
    <section
      aria-label={`evidence gaps ${caseId}`}
      data-testid={`eci-evidence-gaps-${caseId}`}
      className="eci-evidence-gap-panel"
    >
      <h3>Evidence gaps</h3>
      <ul>
        {gaps.map((gap, index) => (
          <li key={`${caseId}-${index}`} data-testid="eci-evidence-gap-item">
            <p>{gap.gap}</p>
            <p>{`Urgency: ${gap.urgency}`}</p>
            <p>{`Collection window: ${gap.windowClosesIn}`}</p>
            <p>{`Fallback: ${gap.fallbackIfMissed}`}</p>
          </li>
        ))}
      </ul>
    </section>
  );
}
