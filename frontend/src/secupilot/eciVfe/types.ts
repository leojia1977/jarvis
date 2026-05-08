export const ECI_VFE_SCHEMA_VERSION = "eci_vfe.v0.2" as const;

export type SourceType =
  | "EDR_EVENT"
  | "NETWORK_EVENT"
  | "AUTH_EVENT"
  | "SERVICE_BANNER"
  | "CODE_COMMENT"
  | "ASSET_REGISTRY"
  | "FIXTURE"
  | "HUMAN_REVIEW";

export type TrustLevel =
  | "TRUSTED_SYSTEM"
  | "BOUNDED_METADATA"
  | "UNTRUSTED_EXTERNAL_TEXT"
  | "UNTRUSTED_ATTACKER_CONTROLLED";

export type AuthoritySource =
  | "RULE_ENGINE"
  | "LLM_INFERENCE"
  | "ASSET_REGISTRY"
  | "HUMAN_REVIEW"
  | "FIXTURE";

export type Urgency = "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";

export type EciStageStatus =
  | "LOW_STAGE_MONITOR"
  | "INITIAL_ACCESS_SUSPECTED"
  | "LATERAL_MOVEMENT_SUSPECTED"
  | "IMMEDIATE_HUMAN_CONFIRMATION_REQUIRED"
  | "HIGH_STAGE_SUSPECTED_SHORT_OBSERVATION"
  | "INSUFFICIENT_EVIDENCE_WITH_PRIORITY_GAPS";

export type CorrelationDecision = "MATCH" | "WEAK_MATCH" | "NO_MATCH" | "HOLD_INSUFFICIENT_EVIDENCE";

export interface SourceTaggedField<TValue> {
  field_name: string;
  source_type: SourceType;
  trust_level: TrustLevel;
  raw_value_retained: false;
  sanitized_summary: string;
  value: TValue;
}

export interface AuthorityTaggedField<TValue> {
  value: TValue;
  source: AuthoritySource;
  confidence: number;
  evidence_refs: string[];
  is_authoritative: boolean;
  signoff_ref?: string;
}

export interface VfeQueryContext {
  requester_alias: string;
  requester_role: string;
  query_reason: string;
  asset_scope: "single_asset" | "case_linked_assets" | "bulk";
  asset_count: number;
  bulk_export: false;
  rate_limit_bucket: string;
  audit_required: true;
  high_value_asset_extra_review: boolean;
  cross_scope_query_requires_governance: boolean;
}

export interface EvidenceGap {
  gap: string;
  why_it_matters: string;
  recommended_query_type: string;
  allowed_scope: "metadata_only";
  urgency: Urgency;
  window_closes_in: string;
  deadline_basis:
    | "endpoint log rotation"
    | "SIEM ingestion delay"
    | "short-lived process evidence"
    | "volatile memory evidence"
    | "network flow retention"
    | "cloud audit delay"
    | "human business context needed";
  fallback_if_missed: string;
}

export interface PromptInjectionHandling {
  input_injection_detected: boolean;
  injection_source_field?: string;
  raw_injection_retained: false;
  sanitized_summary: string;
  forbidden_output_present: false;
  guard_status: "PASS" | "PASS_WITH_SANITIZATION";
}

export interface EciCaseFixture {
  schema_version: typeof ECI_VFE_SCHEMA_VERSION;
  fixture_id: string;
  fixture_meta: {
    source: "fully_artificial";
    real_data_derived: false;
    contains_real_customer_data: false;
    metadata_only: true;
    allowed_for: "local_offline_fixture_only";
  };
  case_id: string;
  title: string;
  source_fields: SourceTaggedField<string | number | boolean>[];
  expected_focus:
    | "EARLY_STAGE_RECON"
    | "INITIAL_ACCESS_TO_PERSISTENCE"
    | "LATERAL_MOVEMENT_SUSPECTED"
    | "PROMPT_INJECTION_SANITIZATION";
  prompt_injection_handling: PromptInjectionHandling;
  expected_evidence_gaps: EvidenceGap[];
  no_action_boundary: {
    human_review_required: true;
    automatic_containment_allowed: false;
    production_writeback_allowed: false;
  };
}

export interface VfeCaseFixture {
  schema_version: typeof ECI_VFE_SCHEMA_VERSION;
  fixture_id: string;
  fixture_meta: EciCaseFixture["fixture_meta"];
  forecast_id: string;
  title: string;
  query_context: VfeQueryContext;
  source_fields: SourceTaggedField<string | number | boolean>[];
  attack_path_defensive_summary: string;
  affected_abstract_asset_group: string;
  recommended_defensive_check: string;
  prompt_injection_handling: PromptInjectionHandling;
  expected_evidence_gaps: EvidenceGap[];
  no_action_boundary: EciCaseFixture["no_action_boundary"];
}

export interface EciChainAssessment {
  schema_version: typeof ECI_VFE_SCHEMA_VERSION;
  assessment_id: string;
  case_id: string;
  stage_label: AuthorityTaggedField<string>;
  stage_number: AuthorityTaggedField<number>;
  stage_status: AuthorityTaggedField<EciStageStatus>;
  confidence: AuthorityTaggedField<number>;
  evidence_refs: string[];
  evidence_gaps: EvidenceGap[];
  prompt_injection_handling: PromptInjectionHandling;
  human_review_required: true;
  automatic_containment_allowed: false;
}

export interface VfeForecastCandidate {
  schema_version: typeof ECI_VFE_SCHEMA_VERSION;
  forecast_id: string;
  query_context: VfeQueryContext;
  candidate_label: AuthorityTaggedField<string>;
  attack_path_defensive_summary: AuthorityTaggedField<string>;
  affected_abstract_asset_group: AuthorityTaggedField<string>;
  risk_rationale: AuthorityTaggedField<string>;
  recommended_defensive_check: AuthorityTaggedField<string>;
  evidence_gaps: EvidenceGap[];
  prompt_injection_handling: PromptInjectionHandling;
  human_validation_required: true;
}

export interface EciVfeCorrelation {
  schema_version: typeof ECI_VFE_SCHEMA_VERSION;
  correlation_id: string;
  case_id: string;
  forecast_id: string;
  correlation_decision: CorrelationDecision;
  hard_match: boolean;
  bounded_fuzzy_match: boolean;
  semantic_supporting_signal: boolean;
  semantic_similarity: number;
  case_upgrade_allowed: false;
  human_review_required: true;
  reason: string;
  evidence_refs: string[];
}

export function isNonAuthoritativeLlmField(field: AuthorityTaggedField<unknown>): boolean {
  return field.source !== "LLM_INFERENCE" || field.is_authoritative === false;
}

export function isMetadataOnlyFixture(fixture: EciCaseFixture | VfeCaseFixture): boolean {
  return (
    fixture.fixture_meta.source === "fully_artificial" &&
    fixture.fixture_meta.real_data_derived === false &&
    fixture.fixture_meta.contains_real_customer_data === false &&
    fixture.fixture_meta.metadata_only === true
  );
}
