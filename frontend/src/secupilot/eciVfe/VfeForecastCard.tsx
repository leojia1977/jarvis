import { buildVfeForecastCardView } from "./eciVfeUiModel";

export function VfeForecastCard() {
  const cards = buildVfeForecastCardView();

  return (
    <section
      aria-label="VFE forecast cards"
      data-testid="vfe-forecast-card-view"
      data-artifact-source="eci_vfe_fixture_rc001"
      data-output-guard-status="PASS"
      data-real-data="false"
      data-live-qwen-api="false"
      data-production-writeback="false"
    >
      <header>
        <p>VFE forecast card</p>
        <h1>Defensive forecast summaries</h1>
        <p>
          Guard-passed local/offline fixture output. Forecast cards are review-only and do not
          authorize containment, remediation, deployment, or case-state upgrades.
        </p>
      </header>

      <div data-testid="vfe-forecast-card-grid">
        {cards.map((card) => (
          <article key={card.forecastId} data-testid="vfe-forecast-card">
            <h2>{card.candidateLabel}</h2>
            <p>{`Forecast: ${card.forecastId}`}</p>
            <p>{`Confidence: ${card.confidencePercent}`}</p>
            <p>{`Asset group: ${card.affectedAbstractAssetGroup}`}</p>
            <p>{card.attackPathDefensiveSummary}</p>
            <p>{`Defensive check: ${card.recommendedDefensiveCheck}`}</p>
            <section aria-label={`forecast evidence gaps ${card.forecastId}`}>
              <h3>Evidence gaps</h3>
              <ul>
                {card.evidenceGaps.map((gap, index) => (
                  <li key={`${card.forecastId}-${index}`} data-testid="vfe-forecast-gap-item">
                    <p>{gap.gap}</p>
                    <p>{`Urgency: ${gap.urgency}`}</p>
                    <p>{`Collection window: ${gap.windowClosesIn}`}</p>
                    <p>{`Deadline basis: ${gap.deadlineBasis}`}</p>
                    <p>{`Fallback: ${gap.fallbackIfMissed}`}</p>
                  </li>
                ))}
              </ul>
            </section>
          </article>
        ))}
      </div>
    </section>
  );
}
