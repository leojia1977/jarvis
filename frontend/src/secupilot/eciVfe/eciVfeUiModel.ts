import chainAssessmentArtifact from "../../../../artifacts/eci_vfe_fixture_runs/rc001/chain_assessment.json";
import forecastCandidatesArtifact from "../../../../artifacts/eci_vfe_fixture_runs/rc001/forecast_candidates.json";
import outputGuardScanArtifact from "../../../../artifacts/eci_vfe_fixture_runs/rc001/output_guard_scan.json";

export interface EciEvidenceGapView {
  gap: string;
  urgency: string;
  windowClosesIn: string;
  fallbackIfMissed: string;
}

export interface VfeEvidenceGapView extends EciEvidenceGapView {
  deadlineBasis: string;
}

export interface EciChainIndicatorView {
  caseId: string;
  stageLabel: string;
  stageStatus: string;
  confidence: number;
  confidencePercent: string;
  evidenceGapCount: number;
  evidenceGaps: EciEvidenceGapView[];
}

export interface VfeForecastCardView {
  forecastId: string;
  candidateLabel: string;
  confidence: number;
  confidencePercent: string;
  attackPathDefensiveSummary: string;
  affectedAbstractAssetGroup: string;
  recommendedDefensiveCheck: string;
  evidenceGaps: VfeEvidenceGapView[];
}

interface EciChainAssessmentRecord {
  case_id: string;
  stage_label: { value: string };
  stage_status: { value: string };
  confidence: { value: number };
  evidence_gaps: Array<{
    gap: string;
    urgency: string;
    window_closes_in: string;
    fallback_if_missed: string;
  }>;
}

interface VfeForecastCandidateRecord {
  forecast_id: string;
  candidate_label: { value: string; confidence: number };
  attack_path_defensive_summary: { value: string };
  affected_abstract_asset_group: { value: string };
  recommended_defensive_check: { value: string };
  evidence_gaps: Array<{
    gap: string;
    urgency: string;
    window_closes_in: string;
    deadline_basis: string;
    fallback_if_missed: string;
  }>;
}

const CHAIN = chainAssessmentArtifact as {
  schema_version: string;
  assessments: EciChainAssessmentRecord[];
};

const FORECAST = forecastCandidatesArtifact as {
  schema_version: string;
  candidates: VfeForecastCandidateRecord[];
};

const OUTPUT_GUARD_SCAN = outputGuardScanArtifact as {
  status: string;
  blocking_finding_count: number;
};

function toPercent(value: number): string {
  return `${Math.round(value * 100)}%`;
}

function sanitizeStageLabel(value: string): string {
  return value.replace(/_/g, " ").toLowerCase();
}

function sanitizeStageStatus(value: string): string {
  return value.replace(/_/g, " ").toLowerCase();
}

function sanitizeCandidateLabel(value: string): string {
  return value.replace(/_/g, " ").toLowerCase();
}

function ensureOutputGuardPasses() {
  if (OUTPUT_GUARD_SCAN.status !== "PASS" || OUTPUT_GUARD_SCAN.blocking_finding_count > 0) {
    throw new Error("UI renders ECI output before output_guard_scan.json is PASS");
  }
}

function assertNoAttackerReadableText(value: string, field: string) {
  if (/(attack_path|exploit|payload|poc|authorization|bearer|topology reachability)/i.test(value)) {
    throw new Error(`forecast field includes forbidden attacker-readable text: ${field}`);
  }
}

export function buildEciChainIndicatorView(): EciChainIndicatorView[] {
  ensureOutputGuardPasses();

  return CHAIN.assessments.map((assessment) => {
    const evidenceGaps = assessment.evidence_gaps.map((gap) => ({
      gap: gap.gap,
      urgency: gap.urgency,
      windowClosesIn: gap.window_closes_in,
      fallbackIfMissed: gap.fallback_if_missed,
    }));

    return {
      caseId: assessment.case_id,
      stageLabel: sanitizeStageLabel(assessment.stage_label.value),
      stageStatus: sanitizeStageStatus(assessment.stage_status.value),
      confidence: assessment.confidence.value,
      confidencePercent: toPercent(assessment.confidence.value),
      evidenceGapCount: evidenceGaps.length,
      evidenceGaps,
    };
  });
}

export function buildVfeForecastCardView(): VfeForecastCardView[] {
  ensureOutputGuardPasses();

  return FORECAST.candidates.map((candidate) => {
    assertNoAttackerReadableText(
      candidate.attack_path_defensive_summary.value,
      "attack_path_defensive_summary"
    );

    const evidenceGaps = candidate.evidence_gaps.map((gap) => ({
      gap: gap.gap,
      urgency: gap.urgency,
      windowClosesIn: gap.window_closes_in,
      deadlineBasis: gap.deadline_basis,
      fallbackIfMissed: gap.fallback_if_missed,
    }));

    return {
      forecastId: candidate.forecast_id,
      candidateLabel: sanitizeCandidateLabel(candidate.candidate_label.value),
      confidence: candidate.candidate_label.confidence,
      confidencePercent: toPercent(candidate.candidate_label.confidence),
      attackPathDefensiveSummary: candidate.attack_path_defensive_summary.value,
      affectedAbstractAssetGroup: candidate.affected_abstract_asset_group.value,
      recommendedDefensiveCheck: candidate.recommended_defensive_check.value,
      evidenceGaps,
    };
  });
}
