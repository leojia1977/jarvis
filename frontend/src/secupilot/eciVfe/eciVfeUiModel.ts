import chainAssessmentArtifact from "../../../../artifacts/eci_vfe_fixture_runs/rc001/chain_assessment.json";
import outputGuardScanArtifact from "../../../../artifacts/eci_vfe_fixture_runs/rc001/output_guard_scan.json";

export interface EciEvidenceGapView {
  gap: string;
  urgency: string;
  windowClosesIn: string;
  fallbackIfMissed: string;
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

const CHAIN = chainAssessmentArtifact as {
  schema_version: string;
  assessments: EciChainAssessmentRecord[];
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

export function buildEciChainIndicatorView(): EciChainIndicatorView[] {
  if (OUTPUT_GUARD_SCAN.status !== "PASS" || OUTPUT_GUARD_SCAN.blocking_finding_count > 0) {
    throw new Error("UI renders ECI output before output_guard_scan.json is PASS");
  }

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
