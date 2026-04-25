export type Role = "P0" | "P1" | "P2" | "P3";
export type CoverageLevel = "L0" | "L1" | "L2" | "L3";

export type Surface =
  | "P1_CASE_DETAIL"
  | "P2_APPROVAL"
  | "P3_MANAGER"
  | "CROSS_SURFACE";

export type CaseState =
  | "UNDER_INVESTIGATION"
  | "PENDING_APPROVAL"
  | "OBSERVATION_WINDOW"
  | "APPROVED_PENDING_EXECUTION"
  | "CLOSED";

export type ARStatus =
  | "PENDING_APPROVAL"
  | "APPROVED_PENDING_EXECUTION"
  | "OBSERVATION_WINDOW"
  | "REJECTED"
  | "WITHDRAWN"
  | "CANCELLED";

export type ActionMode = "IMMEDIATE" | "DELAYED" | "OBSERVE_ONLY" | null;
export type SwitchState = "ON" | "DEGRADED" | "OFF" | "READONLY";

export type ActionPermission =
  | "ALLOW"
  | "CONFIRM"
  | "ESCALATE"
  | "DENY"
  | "READONLY"
  | "DISABLED"
  | "HIDDEN";

export type FixtureMeta = {
  source: "fully_artificial";
  real_data_derived: false;
  contains_real_customer_data: false;
  input_revision?: string;
  allowed_for: "mock-only bounded frontend implementation";
  not_allowed_for?: Array<"production" | "real-data" | "external-pilot">;
};

export type ResolvedSurfaceContext = {
  fixture_meta: FixtureMeta;
  session: {
    role: Role;
    review_surface?: string;
  };

  // surface is required and must be validated by ContextValidator.
  // Missing surface, unsupported surface, or surface/role mismatch must fail closed to SH-08.
  // Sprint 0 role-scoped surface allowlist:
  // - P1_CASE_DETAIL => role P1
  // - P2_APPROVAL => role P2
  // - P3_MANAGER => role P3
  // - CROSS_SURFACE => test harness / walkthrough only; no production routing authority.
  surface: Surface;

  case: {
    case_id: string;
    case_state: CaseState;
    coverage_level: CoverageLevel;
    expert_mode_active: boolean;
  };

  // action_request absent = no AR submitted.
  // action_mode === null = AR exists, but P2 has not decided ActionMode yet.
  // P1 must never set or choose IMMEDIATE / DELAYED / OBSERVE_ONLY.
  action_request?: {
    ar_id: string;
    ar_status: ARStatus;
    action_mode: ActionMode;
    observation_window_minutes?: number | null;
    observation_window_remaining_minutes?: number | null;
    observation_expiry_action?: "RETURN_TO_PENDING_APPROVAL" | null;
    version: string;
  };

  action_permissions: Record<string, ActionPermission>;
  resolved_visibility: {
    effective_visibility_level: CoverageLevel;
    pages: Record<string, SwitchState>;
    fields: Record<string, SwitchState>;
    allowed_actions?: Record<string, ActionPermission | string>;
  };
  honesty: {
    what_would_raise_confidence: string[];
    what_would_disprove_current_verdict: string[];
    unsupported_claims: string[];
  };
  audit_trail: Array<Record<string, unknown>>;
  ui_messages: Record<string, string | string[] | null>;
};

export type SecurityHaltCode =
  | "SH-08_INVALID_CONTEXT_SHAPE"
  | "SH-08_UNSUPPORTED_ENUM"
  | "SH-08_NON_ARTIFICIAL_FIXTURE"
  | "SH-08_REAL_DATA_DERIVED"
  | "SH-08_UNAUTHORIZED_CONTEXT_SOURCE"
  | "SH-08_P3_PRIVILEGED_PAYLOAD_PRESENT"
  | "SH-08_COVERAGE_CEILING_VIOLATION"
  | "SH-08_SURFACE_ROLE_MISMATCH"
  | "SH-08_CONFUSION_ATTACK_PAYLOAD"
  | "SH-08_UNEXPECTED_TOP_LEVEL_FIELD";

export type ValidationResult =
  | { ok: true; context: ResolvedSurfaceContext }
  | { ok: false; code: SecurityHaltCode; reason: string };
