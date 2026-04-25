import coreSurfaceFixture from "../../../../fixtures/secupilot_core_surface_fixture_v0_1.json";
import {
  ActionMode,
  ActionPermission,
  ARStatus,
  CaseState,
  CoverageLevel,
  ResolvedSurfaceContext,
  Role,
  Surface,
  SwitchState
} from "../context/types";
import { validateResolvedSurfaceContext } from "../context/validateResolvedSurfaceContext";

type SourceSurface = "P1_CASE_DETAIL" | "P2_APPROVAL_SURFACE" | "P3_MANAGER_VIEW";

export interface CoreSurfaceFixturePhase {
  phase: number;
  name: string;
  surface: SourceSurface;
  role: Role;
  case_state: CaseState;
  ar_status: ARStatus | null;
  expected_ui: string[];
}

interface CoreSurfaceFixture {
  fixture_version: string;
  status: "mock-only";
  ids: {
    case_id: string;
    action_request_id: string;
    audit_trail_id: string;
  };
  case: {
    case_id: string;
    coverage_level: CoverageLevel;
    effective_visibility_level: CoverageLevel;
    title: string;
    severity: string;
    source: string;
    trigger_source: string;
    narrative_sections: Array<{
      section: string;
      sentences: Array<{
        sentence_id: string;
        text: string;
        evidence_panel_ref?: string;
      }>;
    }>;
    honesty_layer: {
      unsupported_claims: string[];
      what_would_raise_confidence: string[];
      what_would_disprove_current_verdict: string[];
    };
  };
  evidence_panels: Array<{
    panel_id: string;
    standard_title: string;
    provenance_chip: string;
    contains_host_level_raw_evidence?: boolean;
    p3_rendering?: string;
  }>;
  action_request_initial: {
    action_request_id: string;
    status: ARStatus;
    action_mode: ActionMode;
    recommended_action: string;
    urgency_text: string;
    observation_window_minutes: number | null;
    observation_expiry_action: "RETURN_TO_PENDING_APPROVAL" | null;
  };
  audit_trail: Array<{
    audit_id: string;
    event: string;
    actor_role: Role | "SYSTEM";
    case_state_after: CaseState;
    ar_status_after: ARStatus;
    action_mode?: Exclude<ActionMode, null>;
    observation_window_minutes?: number;
    observation_expiry_action?: "RETURN_TO_PENDING_APPROVAL";
    expiry_action?: "RETURN_TO_PENDING_APPROVAL";
  }>;
  phases: CoreSurfaceFixturePhase[];
}

export interface CoreSurfaceFixturePhaseOption {
  phase: number;
  name: string;
  sourceSurface: SourceSurface;
  surface: Surface;
  role: Role;
  caseState: CaseState;
  arStatus: ARStatus | null;
  actionMode: ActionMode;
}

export const CORE_SURFACE_FIXTURE = coreSurfaceFixture as CoreSurfaceFixture;
export const CORE_SURFACE_FIXTURE_VERSION = CORE_SURFACE_FIXTURE.fixture_version;
export const CORE_SURFACE_FIXTURE_PHASES = CORE_SURFACE_FIXTURE.phases;

function fail(message: string): never {
  throw new Error(`Invalid core surface fixture: ${message}`);
}

function normalizeSurface(surface: SourceSurface): Surface {
  if (surface === "P1_CASE_DETAIL") {
    return "P1_CASE_DETAIL";
  }
  if (surface === "P2_APPROVAL_SURFACE") {
    return "P2_APPROVAL";
  }
  if (surface === "P3_MANAGER_VIEW") {
    return "P3_MANAGER";
  }
  return fail(`unsupported surface ${surface}`);
}

function actionModeForPhase(phase: CoreSurfaceFixturePhase): ActionMode {
  if (!phase.ar_status) {
    return null;
  }
  if (phase.phase === 3) {
    return "OBSERVE_ONLY";
  }
  if (phase.phase === 5) {
    return "IMMEDIATE";
  }
  return null;
}

function getObservationWindowEvent() {
  return CORE_SURFACE_FIXTURE.audit_trail.find(
    (event) => event.event === "OBSERVE_ONLY_SELECTED"
  );
}

function toActionRequest(
  phase: CoreSurfaceFixturePhase
): ResolvedSurfaceContext["action_request"] | undefined {
  if (!phase.ar_status) {
    return undefined;
  }

  const actionMode = actionModeForPhase(phase);
  const observationEvent = actionMode === "OBSERVE_ONLY" ? getObservationWindowEvent() : undefined;

  return {
    ar_id: CORE_SURFACE_FIXTURE.ids.action_request_id,
    ar_status: phase.ar_status,
    action_mode: actionMode,
    observation_window_minutes: observationEvent?.observation_window_minutes ?? null,
    // Mock-only: remaining starts equal to total because E0-02 does not run a live timer.
    observation_window_remaining_minutes:
      actionMode === "OBSERVE_ONLY" ? observationEvent?.observation_window_minutes ?? null : null,
    observation_expiry_action: observationEvent?.observation_expiry_action ?? null,
    version: `fixture-v${CORE_SURFACE_FIXTURE.fixture_version}-phase-${phase.phase}`
  };
}

function actionPermissionsForPhase(phase: CoreSurfaceFixturePhase): Record<string, ActionPermission> {
  if (phase.role === "P1") {
    return {
      submit_to_p2: phase.phase === 0 ? "ALLOW" : "DISABLED",
      approve_action: "HIDDEN",
      reject_action: "HIDDEN",
      observe_only_action: "HIDDEN",
      delay_action: "HIDDEN",
      manager_review: "HIDDEN"
    };
  }

  if (phase.role === "P2") {
    if (phase.case_state === "OBSERVATION_WINDOW") {
      return {
        submit_to_p2: "HIDDEN",
        approve_action: "DISABLED",
        reject_action: "DISABLED",
        observe_only_action: "READONLY",
        delay_action: "DISABLED",
        manager_review: "HIDDEN"
      };
    }

    if (phase.case_state === "APPROVED_PENDING_EXECUTION") {
      return {
        submit_to_p2: "HIDDEN",
        approve_action: "READONLY",
        reject_action: "READONLY",
        observe_only_action: "READONLY",
        delay_action: "READONLY",
        manager_review: "HIDDEN"
      };
    }

    return {
      submit_to_p2: "HIDDEN",
      approve_action: "CONFIRM",
      reject_action: "CONFIRM",
      observe_only_action: "ALLOW",
      delay_action: "ALLOW",
      manager_review: "HIDDEN"
    };
  }

  return {
    submit_to_p2: "HIDDEN",
    approve_action: "HIDDEN",
    reject_action: "HIDDEN",
    observe_only_action: "HIDDEN",
    delay_action: "HIDDEN",
    manager_review: "READONLY"
  };
}

function pageVisibilityForSurface(surface: Surface): Record<string, SwitchState> {
  return {
    case_detail: surface === "P1_CASE_DETAIL" ? "ON" : "READONLY",
    approval_surface: surface === "P2_APPROVAL" ? "ON" : "OFF",
    manager_view: surface === "P3_MANAGER" ? "ON" : "OFF"
  };
}

function fieldVisibilityForPhase(phase: CoreSurfaceFixturePhase): Record<string, SwitchState> {
  return {
    narrative_spine: "ON",
    contextual_evidence_summary: "ON",
    host_raw_evidence: "OFF",
    action_mode_controls: phase.role === "P2" && phase.case_state !== "OBSERVATION_WINDOW" ? "ON" : "OFF",
    coverage_l3_fields: "OFF",
    internal_graph_details: "OFF",
    tool_node_details: "OFF"
  };
}

function auditTrailForPhase(phase: CoreSurfaceFixturePhase): ResolvedSurfaceContext["audit_trail"] {
  const eventCount = Math.max(0, Math.min(phase.phase, CORE_SURFACE_FIXTURE.audit_trail.length));
  return CORE_SURFACE_FIXTURE.audit_trail.slice(0, eventCount).map((event) => ({
    audit_id: event.audit_id,
    event: event.event,
    actor_role: event.actor_role,
    case_state_after: event.case_state_after,
    ar_status_after: event.ar_status_after,
    action_mode: event.action_mode ?? null,
    observation_window_minutes: event.observation_window_minutes ?? null,
    observation_expiry_action: event.observation_expiry_action ?? event.expiry_action ?? null
  }));
}

function uiMessagesForPhase(phase: CoreSurfaceFixturePhase): ResolvedSurfaceContext["ui_messages"] {
  return {
    fixture_status: CORE_SURFACE_FIXTURE.status,
    phase_name: phase.name,
    expected_ui: phase.expected_ui,
    recommended_action: CORE_SURFACE_FIXTURE.action_request_initial.recommended_action,
    mock_only_notice:
      "Resolved from fully artificial mock fixture; no URL, storage, real data, or deployment authority."
  };
}

function phaseOption(phase: CoreSurfaceFixturePhase): CoreSurfaceFixturePhaseOption {
  return {
    phase: phase.phase,
    name: phase.name,
    sourceSurface: phase.surface,
    surface: normalizeSurface(phase.surface),
    role: phase.role,
    caseState: phase.case_state,
    arStatus: phase.ar_status,
    actionMode: actionModeForPhase(phase)
  };
}

export const CORE_SURFACE_FIXTURE_PHASE_OPTIONS =
  CORE_SURFACE_FIXTURE_PHASES.map(phaseOption);

export function getCoreSurfaceFixturePhase(phaseNumber: number): CoreSurfaceFixturePhase {
  const phase = CORE_SURFACE_FIXTURE_PHASES.find((item) => item.phase === phaseNumber);
  if (!phase) {
    return fail(`phase ${phaseNumber} is not present`);
  }
  return phase;
}

export function adaptCoreSurfaceFixturePhase(
  phaseOrNumber: CoreSurfaceFixturePhase | number
): ResolvedSurfaceContext {
  const phase =
    typeof phaseOrNumber === "number" ? getCoreSurfaceFixturePhase(phaseOrNumber) : phaseOrNumber;
  const surface = normalizeSurface(phase.surface);

  const context: ResolvedSurfaceContext = {
    fixture_meta: {
      source: "fully_artificial",
      real_data_derived: false,
      contains_real_customer_data: false,
      input_revision: `fixture-v${CORE_SURFACE_FIXTURE.fixture_version}`,
      allowed_for: "mock-only bounded frontend implementation",
      not_allowed_for: ["production", "real-data", "external-pilot"]
    },
    session: {
      role: phase.role
    },
    surface,
    case: {
      case_id: CORE_SURFACE_FIXTURE.ids.case_id,
      case_state: phase.case_state,
      coverage_level: CORE_SURFACE_FIXTURE.case.coverage_level,
      expert_mode_active: false
    },
    action_permissions: actionPermissionsForPhase(phase),
    resolved_visibility: {
      effective_visibility_level: CORE_SURFACE_FIXTURE.case.effective_visibility_level,
      pages: pageVisibilityForSurface(surface),
      fields: fieldVisibilityForPhase(phase)
    },
    honesty: {
      unsupported_claims: CORE_SURFACE_FIXTURE.case.honesty_layer.unsupported_claims,
      what_would_raise_confidence:
        CORE_SURFACE_FIXTURE.case.honesty_layer.what_would_raise_confidence,
      what_would_disprove_current_verdict:
        CORE_SURFACE_FIXTURE.case.honesty_layer.what_would_disprove_current_verdict
    },
    audit_trail: auditTrailForPhase(phase),
    ui_messages: uiMessagesForPhase(phase)
  };

  const actionRequest = toActionRequest(phase);
  if (actionRequest) {
    context.action_request = actionRequest;
  }

  const result = validateResolvedSurfaceContext(context);
  if (!result.ok) {
    return fail(`phase ${phase.phase} failed ${result.code}: ${result.reason}`);
  }

  return result.context;
}

export function adaptCoreSurfaceFixturePhases(): ResolvedSurfaceContext[] {
  return CORE_SURFACE_FIXTURE_PHASES.map((phase) => adaptCoreSurfaceFixturePhase(phase));
}
