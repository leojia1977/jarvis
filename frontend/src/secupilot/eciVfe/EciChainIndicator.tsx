import { buildEciChainIndicatorView } from "./eciVfeUiModel";
import { EciEvidenceGapPanel } from "./EciEvidenceGapPanel";

export function EciChainIndicator() {
  const cards = buildEciChainIndicatorView();

  return (
    <section
      aria-label="ECI chain indicators"
      data-testid="eci-chain-indicator-view"
      data-artifact-source="eci_vfe_fixture_rc001"
      data-output-guard-status="PASS"
      data-real-data="false"
      data-live-qwen-api="false"
      data-production-writeback="false"
    >
      <header>
        <p>ECI chain indicator</p>
        <h1>Incident chain status</h1>
        <p>
          Guard-passed local/offline fixture output. This page is review-only and does not
          authorize containment, remediation, or deployment.
        </p>
      </header>

      <div data-testid="eci-chain-indicator-grid">
        {cards.map((card) => (
          <article key={card.caseId} data-testid="eci-chain-indicator-card">
            <h2>{card.caseId}</h2>
            <p>{`Stage: ${card.stageLabel}`}</p>
            <p>{`Status: ${card.stageStatus}`}</p>
            <p>{`Confidence: ${card.confidencePercent}`}</p>
            <p>{`Evidence gaps: ${card.evidenceGapCount}`}</p>
            <EciEvidenceGapPanel caseId={card.caseId} gaps={card.evidenceGaps} />
          </article>
        ))}
      </div>
    </section>
  );
}
