import {
  ArrowLeft,
  ChevronRight,
  History,
  Inbox,
  Lock,
  MessageSquareText,
  Search,
  Send,
  ShieldCheck,
  Activity,
  Unlock
} from "lucide-react";
import { FormEvent, KeyboardEvent, useEffect, useMemo, useRef, useState } from "react";
import {
  adaptCoreSurfaceFixturePhase,
  CORE_SURFACE_FIXTURE,
  CORE_SURFACE_FIXTURE_PHASE_OPTIONS,
  CORE_SURFACE_FIXTURE_PHASES,
  CoreSurfaceFixturePhase
} from "./secupilot/surface/fixtures/coreSurfaceFixtureAdapter";
import { mockFixtureAdapter } from "./secupilot/surface/fixtures/mockFixtureAdapter";
import {
  ARStatus,
  CaseState,
  CoverageLevel,
  ResolvedSurfaceContext,
  Role,
  SwitchState
} from "./secupilot/surface/context/types";

type Route = "inbox" | "case" | "search" | "coverage_health" | "approval" | "manager";
type EvidenceFrameId =
  | "process_evidence"
  | "lateral_topology"
  | "event_timeline"
  | "attack_lineage"
  | "technical_summary_fallback";
type EvidenceMode = "auto" | "manual";
type SubordinatePanel = "evidence" | "timeline" | "blast_radius";
type NarrativeKey = "WHAT" | "WHY" | "INTENT" | "HONESTY" | "DECISION";
type SearchFocusScope = "summary" | "approval_audit" | "history_audit";
type ExpertModeEntryState = "entry_skeleton" | "p1_restricted" | "not_applicable";
type ARStatusTone = "pending" | "approved" | "observing" | "rejected" | "locked" | "none";
type ARInteractionClass = "non-terminal" | "terminal" | "locked" | "none";
type ARActionAuthority = "p2-only" | "display-only";
type ApprovalAuditDerivedStatus =
  | "SUBMITTED"
  | "OPENED"
  | "OBSERVING"
  | "WINDOW_EXPIRED"
  | "APPROVED"
  | "UNAVAILABLE"
  | "UNSUPPORTED";
type ApprovalAuditSourceState = "records" | "empty" | "unavailable";
type ApprovalCtaId = "approve_action" | "reject_action" | "delay_action" | "observe_only_action";
type ApprovalDraftAction = "approve" | "reject" | "delay" | "observe";
type ClosedCaseDetailRole = Extract<Role, "P1" | "P2" | "P3">;

interface NavItem {
  label: string;
  routeKey: string;
  roles: Role[];
  icon: typeof Inbox;
  activeInSlice: boolean;
}

interface WorkbenchCase {
  id: string;
  title: string;
  verdict: string;
  risk: "High" | "Critical";
  coverage: CoverageLevel;
  nextStep: string;
  summary: string;
  state: CaseState;
  phaseNumber: number;
  phaseName: string;
  redlineFixtureId?: RedlineFixtureId;
  resolvedSurface: string;
  resolvedRole: Role;
  arStatus: ARStatus | null;
  triggerSource: string;
  freshness: string;
  actionRequest: string;
  trace: Array<{
    label: string;
    detail: string;
    provenance: string;
  }>;
  narrative: {
    what: string[];
    why: string[];
    intent: string[];
    honesty: string[];
    decision: string[];
  };
  evidenceFrames: Array<{
    id: EvidenceFrameId;
    title: string;
    provenance: string;
    summary: string;
  }>;
  redline: {
    uiMessages: ResolvedSurfaceContext["ui_messages"];
    visibilityFields: Record<string, SwitchState>;
    unsupportedClaims: string[];
  };
  honestyLayer: {
    unsupportedClaims: string[];
    confidenceSignals: string[];
    disproofSignals: string[];
  };
}

interface ClosedAuditEvent {
  id: string;
  label: string;
  detail: string;
}

interface FixtureSentence {
  sentence_id: string;
  text: string;
  evidence_panel_ref?: string;
}

interface FixtureNarrativeSection {
  section: string;
  sentences: FixtureSentence[];
}

interface FixtureEvidencePanel {
  panel_id: string;
  standard_title: string;
  provenance_chip: string;
  contains_host_level_raw_evidence?: boolean;
  p3_rendering?: string;
}

const FIXTURE = CORE_SURFACE_FIXTURE;
const FIXTURE_PHASES = CORE_SURFACE_FIXTURE_PHASES;
const E0_04C_REDLINE_FIXTURE_IDS = [
  "boundary-p3-audit-summary-unavailable",
  "boundary-p2-cmdb-tags-unavailable",
  "boundary-dirty-update-during-observation-window",
  "boundary-concurrency-stale-approve-rejected",
  "resolver-l1-blast-radius-payload",
  "resolver-p3-technical-detail-redaction"
] as const;
const P3_MANAGER_SUMMARY_REDLINE_FIXTURE_IDS = new Set<string>([
  "boundary-p3-audit-summary-unavailable",
  "resolver-p3-technical-detail-redaction"
]);
const EVIDENCE_FRAME_IDS: EvidenceFrameId[] = [
  "process_evidence",
  "lateral_topology",
  "event_timeline",
  "attack_lineage",
  "technical_summary_fallback"
];
const SEARCH_FOCUS_SCOPES: Array<{
  id: SearchFocusScope;
  label: string;
  description: string;
}> = [
  {
    id: "summary",
    label: "Summary",
    description: "Read-only case summary and guard facts."
  },
  {
    id: "approval_audit",
    label: "Approval audit",
    description: "Read-only approval-audit focus; no approval controls are attached."
  },
  {
    id: "history_audit",
    label: "History audit",
    description: "Read-only historical audit focus with recorded coverage preserved."
  }
];
type RedlineFixtureId = (typeof E0_04C_REDLINE_FIXTURE_IDS)[number];
type RenderableMockPhase = Pick<CoreSurfaceFixturePhase, "phase" | "name" | "expected_ui">;

const CASE_STATE_LABELS: Record<CaseState, string> = {
  UNDER_INVESTIGATION: "Under investigation",
  PENDING_APPROVAL: "Pending P2 review",
  OBSERVATION_WINDOW: "Observation window",
  APPROVED_PENDING_EXECUTION: "Approved pending execution",
  CLOSED: "Closed"
};

const CASE_STATE_HEADER_SKELETON: Partial<
  Record<
    CaseState,
    {
      title: string;
      description: string;
      visualFrame: string;
      lockState: string;
    }
  >
> = {
  OBSERVATION_WINDOW: {
    title: "Observation window readonly",
    description:
      "Case Detail reflects an active observation window without approving, rejecting, delaying, or executing.",
    visualFrame: "VF-11",
    lockState: "readonly-observation"
  },
  APPROVED_PENDING_EXECUTION: {
    title: "Approved pending execution locked",
    description:
      "Case Detail reflects approved-pending-execution as a locked display state; execution is not started here.",
    visualFrame: "VF-12",
    lockState: "terminal-display-lock"
  },
  CLOSED: {
    title: "Closed readonly",
    description:
      "Case Detail reflects a resolved CLOSED state with write controls physically absent.",
    visualFrame: "VF-13",
    lockState: "closed-readonly"
  }
};

const MOCK_STATE_SYNC_EVENT = "secupilot:mock-state-sync";
const MOCK_STATE_SYNC_SOURCES = new Set([
  "emitStateSync",
  "STATE_SYNC",
  "mock_state_sync",
  "storybook_fixture",
  "playwright_fixture"
]);
const CD_T06_CLOSED_AUDIT_EVENTS: ClosedAuditEvent[] = [
  {
    id: "AUD-001",
    label: "Case Created",
    detail: "Renderable CLOSED context source confirms the case exists before AR submission."
  },
  {
    id: "AUD-002",
    label: "AR Submitted",
    detail: "P1 submitted the action request into the governed approval path."
  },
  {
    id: "AUD-003",
    label: "Observe Only Selected",
    detail: "P2 selected an observation window rather than immediate execution."
  },
  {
    id: "AUD-004",
    label: "Observation Window Expired / RETURN_TO_PENDING_APPROVAL",
    detail: "State-sync returned the request to PENDING_APPROVAL without auto-execution."
  },
  {
    id: "AUD-005",
    label: "Approved / APPROVED_PENDING_EXECUTION",
    detail: "P2 approval reached approved-pending-execution before closeout."
  },
  {
    id: "AUD-006",
    label: "Case Closed / CLOSED / RESOLVED",
    detail: "The case is resolved and write controls remain absent."
  }
];

const AR_STATUS_DISPLAY: Record<
  ARStatus,
  {
    label: string;
    tone: Exclude<ARStatusTone, "none">;
    interactionClass: Exclude<ARInteractionClass, "none">;
  }
> = {
  PENDING_APPROVAL: {
    label: "Pending approval",
    tone: "pending",
    interactionClass: "non-terminal"
  },
  APPROVED_PENDING_EXECUTION: {
    label: "Approved pending execution",
    tone: "approved",
    interactionClass: "terminal"
  },
  OBSERVATION_WINDOW: {
    label: "Observation window",
    tone: "observing",
    interactionClass: "locked"
  },
  REJECTED: {
    label: "Rejected",
    tone: "rejected",
    interactionClass: "terminal"
  },
  WITHDRAWN: {
    label: "Withdrawn",
    tone: "locked",
    interactionClass: "locked"
  },
  CANCELLED: {
    label: "Cancelled",
    tone: "locked",
    interactionClass: "locked"
  }
};
const APPROVAL_CTA_LABELS: Array<{
  action: ApprovalDraftAction;
  id: ApprovalCtaId;
  label: string;
  shell: "strong-confirm" | "configuration";
}> = [
  { action: "approve", id: "approve_action", label: "Approve", shell: "strong-confirm" },
  { action: "reject", id: "reject_action", label: "Reject", shell: "strong-confirm" },
  { action: "delay", id: "delay_action", label: "Delay", shell: "configuration" },
  { action: "observe", id: "observe_only_action", label: "Observe", shell: "configuration" }
];
const APPROVAL_AUDIT_EVENT_STATUS_MAP: Record<string, ApprovalAuditDerivedStatus> = {
  APPROVED_AFTER_WINDOW: "APPROVED",
  AR_SUBMITTED: "SUBMITTED",
  OBSERVATION_WINDOW_EXPIRED: "WINDOW_EXPIRED",
  OBSERVE_ONLY_SELECTED: "OBSERVING",
  P2_OPENED_AR: "OPENED"
};
const APPROVAL_AUDIT_STATUS_DISPLAY: Record<
  ApprovalAuditDerivedStatus,
  { label: string; tone: ARStatusTone }
> = {
  SUBMITTED: { label: "AR submitted", tone: "pending" },
  OPENED: { label: "Opened by P2", tone: "pending" },
  OBSERVING: { label: "Observation selected", tone: "observing" },
  WINDOW_EXPIRED: { label: "Observation expired", tone: "pending" },
  APPROVED: { label: "Approved after window", tone: "approved" },
  UNAVAILABLE: { label: "Audit unavailable", tone: "none" },
  UNSUPPORTED: { label: "Unsupported audit event", tone: "locked" }
};
const COVERAGE_HEALTH_UI_MESSAGE_KEYS = [
  "fixture_status",
  "phase_name",
  "expected_ui",
  "mock_only_notice"
] as const;
const COVERAGE_HEALTH_NOTICE_ANCHORS = [
  {
    key: "mock_only_notice",
    label: "Missing signal notice",
    testId: "missing-signal-notice"
  },
  {
    key: "fixture_status",
    label: "Confidence notice",
    testId: "confidence-notice"
  },
  {
    key: "expected_ui",
    label: "Escalation hint",
    testId: "escalation-hint"
  }
] as const;
const SWITCH_STATE_ORDER: SwitchState[] = ["ON", "READONLY", "DEGRADED", "OFF"];

function getARStatusDisplay(
  arStatus: ARStatus | null,
  role: Role
): {
  actionAuthority: ARActionAuthority;
  interactionClass: ARInteractionClass;
  label: string;
  stateMigration: "none";
  tone: ARStatusTone;
} {
  if (!arStatus) {
    return {
      actionAuthority: "display-only",
      interactionClass: "none",
      label: "No AR submitted",
      stateMigration: "none",
      tone: "none"
    };
  }

  const display = AR_STATUS_DISPLAY[arStatus];
  return {
    ...display,
    actionAuthority:
      arStatus === "PENDING_APPROVAL" && role === "P2" ? "p2-only" : "display-only",
    stateMigration: "none"
  };
}

function formatUiMessageValue(value: string | string[] | null): string {
  if (Array.isArray(value)) {
    return value.join(" / ");
  }
  return value ?? "Unavailable";
}

function toRisk(value: string): "High" | "Critical" {
  return value.toUpperCase() === "CRITICAL" ? "Critical" : "High";
}

function toEvidenceFrameId(value: string | undefined): EvidenceFrameId {
  return EVIDENCE_FRAME_IDS.includes(value as EvidenceFrameId)
    ? (value as EvidenceFrameId)
    : "process_evidence";
}

function getFixtureSection(sectionKey: NarrativeKey): FixtureNarrativeSection | undefined {
  return FIXTURE.case.narrative_sections.find((section) => section.section === sectionKey);
}

function getFixtureSectionSentences(sectionKey: NarrativeKey): string[] {
  return getFixtureSection(sectionKey)?.sentences.map((sentence) => sentence.text) ?? [];
}

function getFixtureSectionEvidence(sectionKey: NarrativeKey, fallback: EvidenceFrameId): EvidenceFrameId {
  const ref = getFixtureSection(sectionKey)?.sentences[0]?.evidence_panel_ref;
  return ref ? toEvidenceFrameId(ref) : fallback;
}

function buildActionRequestSummary(
  phase: RenderableMockPhase,
  context: ResolvedSurfaceContext
): string {
  const arId = FIXTURE.ids.action_request_id;
  if (!context.action_request) {
    return `No action request submitted. Fixture AR ${arId} remains unavailable to P1 until submit.`;
  }
  if (phase.phase === 1) {
    return `${arId} - Waiting on P2 - submit action is read-only in this mock phase.`;
  }
  return `${arId} - ${context.action_request.ar_status} - resolved from mock phase ${phase.phase}.`;
}

function buildTrace(phase: RenderableMockPhase): WorkbenchCase["trace"] {
  const auditEvents = FIXTURE.audit_trail.slice(0, Math.max(0, Math.min(phase.phase, FIXTURE.audit_trail.length)));
  if (auditEvents.length === 0) {
    return [
      {
        label: "Fixture loaded",
        detail: `${FIXTURE.ids.case_id} is resolved from mock fixture v${FIXTURE.fixture_version}.`,
        provenance: "mock-only"
      },
      {
        label: "Source boundary",
        detail: "Role, coverage, and state come from resolved fixture context, not URL or browser storage.",
        provenance: "resolved context"
      }
    ];
  }
  return auditEvents.map((event) => ({
    label: event.event.replaceAll("_", " "),
    detail: `${event.actor_role} moved the mock case context to ${event.case_state_after}.`,
    provenance: event.audit_id
  }));
}

function buildEvidenceFrames(role: Role): WorkbenchCase["evidenceFrames"] {
  const omittedTechnicalPanels = FIXTURE.evidence_panels.filter(
    (panel) => role === "P3" && panel.contains_host_level_raw_evidence
  );
  const visibleFrames = FIXTURE.evidence_panels
    .filter((panel) => role !== "P3" || !panel.contains_host_level_raw_evidence)
    .map((panel) => ({
      id: toEvidenceFrameId(panel.panel_id),
      title: panel.standard_title,
      provenance: panel.provenance_chip,
      summary:
        role === "P3" && panel.p3_rendering
          ? panel.p3_rendering
          : `Mock fixture panel ${panel.panel_id}; provenance remains metadata only.`
    }));

  if (omittedTechnicalPanels.length === 0) {
    return visibleFrames;
  }

  return [
    ...visibleFrames,
    {
      id: "technical_summary_fallback",
      title: "Technical summary fallback",
      provenance: "summary fallback",
      summary:
        "Detailed technical records are outside this P3 surface. This read-only fallback keeps the case summary cautious and does not add operational certainty."
    }
  ];
}

function buildWorkbenchCase(
  phase: RenderableMockPhase,
  context: ResolvedSurfaceContext,
  redlineFixtureId?: RedlineFixtureId
): WorkbenchCase {
  const role = context.session.role;
  return {
    id: FIXTURE.ids.case_id,
    title: FIXTURE.case.title,
    verdict: `${FIXTURE.case.severity} mock case - ${phase.name}`,
    risk: toRisk(FIXTURE.case.severity),
    coverage: context.case.coverage_level,
    nextStep:
      phase.phase === 1
        ? "Waiting on P2 - submit action is read-only"
        : phase.expected_ui.join(" - "),
    summary: `${FIXTURE.case.trigger_source}. Phase ${phase.phase} is resolved from mock fixture v${FIXTURE.fixture_version}.`,
    state: context.case.case_state,
    phaseNumber: phase.phase,
    phaseName: phase.name,
    redlineFixtureId,
    resolvedSurface: context.surface,
    resolvedRole: role,
    arStatus: context.action_request?.ar_status ?? null,
    triggerSource: FIXTURE.case.source,
    freshness: `Mock fixture v${FIXTURE.fixture_version}; no live refresh`,
    actionRequest: buildActionRequestSummary(phase, context),
    trace: buildTrace(phase),
    narrative: {
      what: getFixtureSectionSentences("WHAT"),
      why: getFixtureSectionSentences("WHY"),
      intent: [
        `Mock fixture intent stays bounded to ${FIXTURE.case.trigger_source}; no additional attacker claim is synthesized.`
      ],
      honesty: [
        ...FIXTURE.case.honesty_layer.unsupported_claims,
        ...FIXTURE.case.honesty_layer.what_would_raise_confidence,
        ...FIXTURE.case.honesty_layer.what_would_disprove_current_verdict
      ],
      decision: [
        `Recommended action from fixture: ${FIXTURE.action_request_initial.recommended_action}.`,
        "P1 still cannot choose ActionMode; P2 remains the approval authority in later phases."
      ]
    },
    evidenceFrames: buildEvidenceFrames(role),
    redline: {
      uiMessages: context.ui_messages,
      visibilityFields: context.resolved_visibility.fields,
      unsupportedClaims: context.honesty.unsupported_claims
    },
    honestyLayer: {
      unsupportedClaims: context.honesty.unsupported_claims,
      confidenceSignals: context.honesty.what_would_raise_confidence,
      disproofSignals: context.honesty.what_would_disprove_current_verdict
    }
  };
}

function isRedlineFixtureId(value: string): value is RedlineFixtureId {
  return E0_04C_REDLINE_FIXTURE_IDS.includes(value as RedlineFixtureId);
}

function redlineFixturePhase(
  fixtureId: RedlineFixtureId,
  context: ResolvedSurfaceContext
): RenderableMockPhase {
  const expectedUi = context.ui_messages.expected_ui;
  return {
    phase: 100 + E0_04C_REDLINE_FIXTURE_IDS.indexOf(fixtureId),
    name: `Redline ${fixtureId}`,
    expected_ui: Array.isArray(expectedUi)
      ? expectedUi
      : [`Mock-only redline fixture ${fixtureId}`]
  };
}

const NAV_ITEMS: NavItem[] = [
  {
    label: "Inbox",
    routeKey: "inbox",
    roles: ["P0", "P1", "P2", "P3"],
    icon: Inbox,
    activeInSlice: true
  },
  {
    label: "Search / History",
    routeKey: "search_history",
    roles: ["P0", "P1", "P2", "P3"],
    icon: History,
    activeInSlice: true
  },
  {
    label: "Approval Queue",
    routeKey: "approval",
    roles: ["P2"],
    icon: ShieldCheck,
    activeInSlice: true
  },
  {
    label: "Coverage & Health",
    routeKey: "coverage_health",
    roles: ["P0", "P2"],
    icon: Activity,
    activeInSlice: true
  },
  {
    label: "Manager View",
    routeKey: "manager_view",
    roles: ["P3"],
    icon: ShieldCheck,
    activeInSlice: true
  }
];

function initialRoute(): { route: Route; caseId: string | null } {
  const path = window.location.pathname;
  const caseMatch = path.match(/^\/case\/([^/]+)$/);
  if (caseMatch) {
    return { route: "case", caseId: decodeURIComponent(caseMatch[1]) };
  }
  if (path === "/search") {
    return { route: "search", caseId: null };
  }
  if (path === "/approval") {
    return { route: "approval", caseId: null };
  }
  if (path === "/manager") {
    return { route: "manager", caseId: null };
  }
  if (path === "/coverage-health") {
    return { route: "coverage_health", caseId: null };
  }
  return { route: "inbox", caseId: null };
}

function isCoverageLevel(value: string | null): value is CoverageLevel {
  return value === "L0" || value === "L1" || value === "L2" || value === "L3";
}

function isSearchFocusScope(value: string | null): value is SearchFocusScope {
  return value === "summary" || value === "approval_audit" || value === "history_audit";
}

function coverageRank(level: CoverageLevel): number {
  return { L0: 0, L1: 1, L2: 2, L3: 3 }[level];
}

function clampCoverageRequest(
  requestedCoverage: CoverageLevel | null,
  recordedCoverage: CoverageLevel
): CoverageLevel {
  if (!requestedCoverage) {
    return recordedCoverage;
  }
  return coverageRank(requestedCoverage) > coverageRank(recordedCoverage)
    ? recordedCoverage
    : requestedCoverage;
}

function formatCoverageClampReason(
  recordedCoverage: CoverageLevel,
  currentCoverage: CoverageLevel,
  effectiveCoverage: CoverageLevel
): string {
  return `recorded = ${recordedCoverage} · current = ${currentCoverage} · effective = ${effectiveCoverage}`;
}

function auditRecordNumber(
  event: Record<string, unknown> | undefined,
  key: string
): number | null {
  const value = event?.[key];
  return typeof value === "number" ? value : null;
}

function auditRecordString(
  event: Record<string, unknown> | undefined,
  key: string
): string | null {
  const value = event?.[key];
  return typeof value === "string" ? value : null;
}

function getApprovalAuditDerivedStatus(
  event: Record<string, unknown> | undefined
): ApprovalAuditDerivedStatus {
  if (!event) {
    return "UNAVAILABLE";
  }
  const eventName = auditRecordString(event, "event");
  if (!eventName) {
    return "UNSUPPORTED";
  }
  return APPROVAL_AUDIT_EVENT_STATUS_MAP[eventName] ?? "UNSUPPORTED";
}

function uiMessageString(
  messages: ResolvedSurfaceContext["ui_messages"],
  key: string,
  fallback: string
): string {
  const value = messages[key];
  return typeof value === "string" ? value : fallback;
}

function isObservationWindowExpiredStateSync(detail: unknown): boolean {
  if (!detail || typeof detail !== "object") {
    return false;
  }

  const record = detail as Record<string, unknown>;
  const syncSource = record.state_sync_source ?? record.source;
  return (
    typeof syncSource === "string" &&
    MOCK_STATE_SYNC_SOURCES.has(syncSource) &&
    record.case_state === "PENDING_APPROVAL" &&
    record.ar_status === "PENDING_APPROVAL" &&
    record.observation_expiry_action === "RETURN_TO_PENDING_APPROVAL" &&
    (record.audit_event_id === "AUD-004" ||
      record.audit_event_type === "OBSERVATION_WINDOW_EXPIRED")
  );
}

function findObservationWindowExpiredPhase() {
  return FIXTURE_PHASES.find(
    (phase) =>
      phase.role === "P2" &&
      phase.case_state === "PENDING_APPROVAL" &&
      phase.ar_status === "PENDING_APPROVAL" &&
      phase.expected_ui.includes("no_auto_execute")
  );
}

function buildClosedCaseDetailProjection(
  activeCase: WorkbenchCase,
  role: ClosedCaseDetailRole
): WorkbenchCase {
  return {
    ...activeCase,
    state: "CLOSED",
    resolvedRole: role,
    resolvedSurface:
      role === "P3" ? "P3_MANAGER" : role === "P2" ? "P2_APPROVAL" : "P1_CASE_DETAIL",
    arStatus: "APPROVED_PENDING_EXECUTION",
    actionRequest:
      "Closed / resolved. Dialogue remains visible and read-only; write controls are absent.",
    phaseName: `${activeCase.phaseName} + CD-T06 CLOSED readonly projection`
  };
}

function resolveExpertModeEntry(
  role: Role,
  coverage: CoverageLevel
): {
  state: ExpertModeEntryState;
  roleVariant: "P0_TOGGLEABLE" | "P1_RESTRICTED" | "P2_TOGGLEABLE" | "P3_HIDDEN";
  badge: string;
  title: string;
  description: string;
} {
  if (role === "P3") {
    return {
      state: "not_applicable",
      roleVariant: "P3_HIDDEN",
      badge: "P3 hidden",
      title: "Expert mode unavailable",
      description: "P3 uses manager-readonly surfaces and does not receive this Global Shell entry."
    };
  }

  if (role === "P1") {
    return {
      state: "p1_restricted",
      roleVariant: "P1_RESTRICTED",
      badge: "P1 limited",
      title: "Expert Mode",
      description: `Expand current fields only. P1 remains limited to the current ${coverage} field set.`
    };
  }

  return {
    state: "entry_skeleton",
    roleVariant: role === "P0" ? "P0_TOGGLEABLE" : "P2_TOGGLEABLE",
    badge: `${role} skeleton`,
    title: "Expert Mode",
    description: `Expand current fields only. ${role} toggleable behavior remains a VF-03 skeleton.`
  };
}

interface AppProps {
  initialPhaseNumber?: number;
  initialClosedCaseDetailRole?: ClosedCaseDetailRole;
}

function App({
  initialPhaseNumber = FIXTURE_PHASES[0]?.phase ?? 0,
  initialClosedCaseDetailRole
}: AppProps = {}) {
  const [{ route, caseId }, setLocation] = useState(initialRoute);
  const [activePhaseNumber, setActivePhaseNumber] = useState(initialPhaseNumber);
  const [activeRedlineFixtureId, setActiveRedlineFixtureId] = useState<RedlineFixtureId | "">("");
  const [globalQuery, setGlobalQuery] = useState("");
  const [followUp, setFollowUp] = useState("");

  const activePhase =
    FIXTURE_PHASES.find((phase) => phase.phase === activePhaseNumber) ?? FIXTURE_PHASES[0];
  const activeContext = useMemo(
    () =>
      activeRedlineFixtureId
        ? mockFixtureAdapter.getFixture(activeRedlineFixtureId)
        : adaptCoreSurfaceFixturePhase(activePhase),
    [activePhase, activeRedlineFixtureId]
  );
  const activeRenderPhase = useMemo(
    () =>
      activeRedlineFixtureId
        ? redlineFixturePhase(activeRedlineFixtureId, activeContext)
        : activePhase,
    [activeContext, activePhase, activeRedlineFixtureId]
  );
  const role = activeContext.session.role;
  const cases = useMemo(
    () => [
      buildWorkbenchCase(
        activeRenderPhase,
        activeContext,
        activeRedlineFixtureId || undefined
      )
    ],
    [activeContext, activeRenderPhase, activeRedlineFixtureId]
  );
  const activeCase = useMemo(
    () => cases.find((item) => item.id === caseId) ?? cases[0],
    [caseId, cases]
  );
  const renderActiveCase = useMemo(
    () =>
      initialClosedCaseDetailRole
        ? buildClosedCaseDetailProjection(activeCase, initialClosedCaseDetailRole)
        : activeCase,
    [activeCase, initialClosedCaseDetailRole]
  );
  const navItems = NAV_ITEMS.filter((item) => item.roles.includes(role));

  function selectRole(nextRole: Role) {
    const nextPhase = FIXTURE_PHASES.find((phase) => phase.role === nextRole);
    if (nextPhase) {
      setActiveRedlineFixtureId("");
      setActivePhaseNumber(nextPhase.phase);
    }
  }

  function selectPhase(nextPhase: number) {
    setActiveRedlineFixtureId("");
    setActivePhaseNumber(nextPhase);
  }

  function selectRedlineFixture(fixtureId: string) {
    if (fixtureId === "" || isRedlineFixtureId(fixtureId)) {
      setActiveRedlineFixtureId(fixtureId);
    }
  }

  function navigate(nextRoute: Route, nextCaseId?: string) {
    const path =
      nextRoute === "case" && nextCaseId
        ? `/case/${nextCaseId}`
        : nextRoute === "approval"
          ? "/approval"
          : nextRoute === "manager"
            ? "/manager"
        : nextRoute === "search"
          ? "/search?tab=history"
          : nextRoute === "coverage_health"
            ? "/coverage-health"
            : "/inbox";
    window.history.pushState({}, "", path);
    setLocation({ route: nextRoute, caseId: nextCaseId ?? null });
  }

  useEffect(() => {
    if (route === "approval" && role === "P1") {
      navigate("inbox");
      return;
    }

    if (route === "approval" && role === "P3" && window.location.pathname !== "/manager") {
      window.history.replaceState({}, "", "/manager");
    }
  }, [role, route]);

  useEffect(() => {
    function handleMockStateSync(event: Event) {
      const detail = event instanceof CustomEvent ? event.detail : undefined;
      if (
        activeRedlineFixtureId ||
        activeContext.surface !== "P2_APPROVAL" ||
        activeContext.case.case_state !== "OBSERVATION_WINDOW" ||
        activeContext.action_request?.ar_status !== "OBSERVATION_WINDOW" ||
        !isObservationWindowExpiredStateSync(detail)
      ) {
        return;
      }

      const nextPhase = findObservationWindowExpiredPhase();
      if (nextPhase) {
        setActiveRedlineFixtureId("");
        setActivePhaseNumber(nextPhase.phase);
      }
    }

    window.addEventListener(MOCK_STATE_SYNC_EVENT, handleMockStateSync);
    return () => window.removeEventListener(MOCK_STATE_SYNC_EVENT, handleMockStateSync);
  }, [activeContext, activeRedlineFixtureId]);

  function submitGlobalQuery(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setGlobalQuery("");
  }

  function submitFollowUp(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setFollowUp("");
  }

  return (
    <main className="workbench-shell">
      <aside className="sidebar" aria-label="Primary navigation">
        <div className="brand-lockup">
          <span className="brand-mark">S</span>
          <div>
            <strong>SecuPilot</strong>
            <span>Case Workbench</span>
          </div>
        </div>

        <div className="role-switcher" aria-label="Role selector">
          {(["P0", "P1", "P2", "P3"] as Role[]).map((item) => {
            const hasFixturePhase = FIXTURE_PHASES.some((phase) => phase.role === item);
            return (
              <button
                aria-disabled={!hasFixturePhase}
                className={item === role ? "role active" : "role"}
                disabled={!hasFixturePhase}
                key={item}
                onClick={() => selectRole(item)}
                type="button"
              >
                {item}
              </button>
            );
          })}
        </div>

        <nav className="nav-list">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isSearchRoute = item.routeKey === "search_history";
            const isCoverageHealthRoute = item.routeKey === "coverage_health";
            const isApprovalRoute = item.routeKey === "approval";
            const isManagerRoute = item.routeKey === "manager_view";
            const isActive =
              item.routeKey === route ||
              (item.routeKey === "inbox" && route === "case") ||
              (isSearchRoute && route === "search") ||
              (isCoverageHealthRoute && route === "coverage_health") ||
              (isApprovalRoute && route === "approval") ||
              (isManagerRoute && route === "manager");
            const navRoute: Route = isSearchRoute
              ? "search"
              : isCoverageHealthRoute
                ? "coverage_health"
                : isApprovalRoute
                  ? "approval"
                  : isManagerRoute
                    ? "manager"
                    : "inbox";
            return (
              <button
                aria-disabled={!item.activeInSlice}
                className={isActive ? "nav-item active" : "nav-item"}
                key={item.routeKey}
                onClick={() => item.activeInSlice && navigate(navRoute)}
                type="button"
              >
                <Icon aria-hidden="true" size={18} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        <ExpertModeEntrySlot
          caseState={renderActiveCase.state}
          coverage={renderActiveCase.coverage}
          role={role}
        />
      </aside>

      <section className="content-shell">
        <header className="topbar">
          <form className="global-query" onSubmit={submitGlobalQuery} role="search">
            <Search aria-hidden="true" size={20} />
            <label className="sr-only" htmlFor="global-query">
              Global conversation input
            </label>
            <input
              id="global-query"
              onChange={(event) => setGlobalQuery(event.target.value)}
              placeholder="Ask about a case, host, approval, or signal gap"
              value={globalQuery}
            />
            <button aria-label="Submit global query" type="submit">
              <Send aria-hidden="true" size={18} />
            </button>
          </form>

          <div className="coverage-badge" aria-label="Coverage level" data-testid="coverage-badge">
            <span className="coverage-dot" />
            <span>Coverage {renderActiveCase.coverage}</span>
          </div>

          <MockContextSelector
            activeContext={activeContext}
            activePhase={activePhase}
            activeRedlineFixtureId={activeRedlineFixtureId}
            onPhaseChange={selectPhase}
            onRedlineFixtureChange={selectRedlineFixture}
          />
        </header>

        {route === "case" ? (
          <CaseDetail
            activeCase={renderActiveCase}
            followUp={followUp}
            key={`${renderActiveCase.id}-${renderActiveCase.phaseNumber}-${renderActiveCase.state}-${renderActiveCase.resolvedRole}`}
            onBack={() => navigate("inbox")}
            onFollowUpChange={setFollowUp}
            onFollowUpSubmit={submitFollowUp}
          />
        ) : route === "approval" ? (
          <ApprovalRouteShell activeCase={renderActiveCase} activeContext={activeContext} />
        ) : route === "manager" ? (
          <ManagerView
            activeCase={renderActiveCase}
            activeContext={activeContext}
            onRouteRedirect={(targetRoute) => navigate(targetRoute)}
          />
        ) : route === "search" ? (
          <SearchHistoryView
            activeCase={renderActiveCase}
            activeContext={activeContext}
            onNavigateToManager={() => navigate("manager")}
          />
        ) : route === "coverage_health" ? (
          <CoverageHealthView activeCase={renderActiveCase} activeContext={activeContext} />
        ) : (
          <InboxView
            cases={cases}
            onNavigateToApproval={() => navigate("approval")}
            onOpenCase={(nextCaseId) => navigate("case", nextCaseId)}
            role={role}
          />
        )}
      </section>
    </main>
  );
}

function ExpertModeEntrySlot({
  caseState,
  coverage,
  role
}: {
  caseState: CaseState;
  coverage: CoverageLevel;
  role: Role;
}) {
  const entry = resolveExpertModeEntry(role, coverage);

  if (entry.state === "not_applicable") {
    return null;
  }

  return (
    <section
      aria-labelledby="expert-mode-entry-title"
      className="expert-mode-frame"
      data-action-state="not-implemented"
      data-authority-source="resolved-surface-context"
      data-case-state={caseState}
      data-coverage-level={coverage}
      data-expert-mode="false"
      data-expert-mode-state={entry.state}
      data-role={role}
      data-testid="vf-03-expert-mode-frame"
      data-visual-state="skeleton"
    >
      <div className="expert-mode-entry" data-expert-mode="false" data-testid="expert-mode-entry">
        <div className="expert-mode-entry-title">
          <Lock aria-hidden="true" size={16} />
          <span id="expert-mode-entry-title">{entry.title}</span>
          <span className="expert-mode-entry-badge">{entry.badge}</span>
        </div>
        <button
          aria-label="Expert Mode"
          aria-pressed="false"
          className="expert-mode-toggle"
          data-action-state="inert"
          data-role-variant={entry.roleVariant}
          data-switch-state="OFF"
          data-testid="expert-mode-toggle"
          type="button"
        >
          <span aria-hidden="true" />
        </button>
      </div>
      <p>{entry.description}</p>
      <span className="expert-mode-entry-note">
        No route, permission upgrade, coverage bypass, OFF-field mount, or action binding.
      </span>
      <div
        className="expert-mode-degraded-field"
        data-switch-state="DEGRADED"
        data-testid="lineage-confidence"
      >
        <span>Lineage Confidence</span>
        <strong>DEGRADED</strong>
      </div>
      <section
        aria-label="Expert mode ON selector baseline"
        className="expert-mode-on-example"
        data-expert-mode="true"
        data-role-variant={entry.roleVariant}
        data-testid="expert-mode-on-example"
      >
        <div className="expert-mode-active-banner" data-testid="expert-mode-active-banner">
          Expert Mode ON example: current fields only; no coverage upgrade or new information.
        </div>
        <div className="expert-mode-field-grid">
          <div data-switch-state="ON" data-testid="expert-field-confidence-breakdown">
            Confidence Breakdown
          </div>
          <div data-switch-state="ON" data-testid="expert-field-inferred-node-count">
            Inferred Node Count
          </div>
          <div data-switch-state="ON" data-testid="expert-field-signal-quality">
            Signal Quality
          </div>
          <div data-switch-state="DEGRADED" data-testid="lineage-confidence-expert">
            Lineage Confidence remains DEGRADED
          </div>
        </div>
        <p className="expert-mode-off-annotation">
          L1 OFF fields stay absent: no card, no placeholder, no DOM.
        </p>
      </section>
    </section>
  );
}

export function ApprovalRouteShell({
  activeCase,
  activeContext
}: {
  activeCase: WorkbenchCase;
  activeContext: ResolvedSurfaceContext;
}) {
  const role = activeContext.session.role;
  const actionRequest = activeContext.action_request;
  const [activeApprovalDraft, setActiveApprovalDraft] = useState<ApprovalDraftAction | null>(null);
  const approvalDraftDialogRef = useRef<HTMLDivElement>(null);
  const approvalDraftCloseButtonRef = useRef<HTMLButtonElement>(null);
  const approvalDraftTriggerRef = useRef<HTMLButtonElement | null>(null);
  const arStatusDisplay = getARStatusDisplay(actionRequest?.ar_status ?? null, role);
  const isReadOnlyApprovalShell = role === "P0";
  const canRenderApprovalCtas =
    role === "P2" &&
    activeContext.surface === "P2_APPROVAL" &&
    actionRequest?.ar_status === "PENDING_APPROVAL" &&
    arStatusDisplay.actionAuthority === "p2-only";
  const canRenderApprovedPendingLock =
    role === "P2" &&
    activeContext.surface === "P2_APPROVAL" &&
    actionRequest?.ar_status === "APPROVED_PENDING_EXECUTION";
  const canRenderObservationWindowSkeleton =
    role === "P2" &&
    activeContext.surface === "P2_APPROVAL" &&
    actionRequest?.ar_status === "OBSERVATION_WINDOW";
  const observationWindowEvent = canRenderObservationWindowSkeleton
    ? activeContext.audit_trail.find((event) => event.event === "OBSERVE_ONLY_SELECTED")
    : undefined;
  const observationWindowMinutes =
    actionRequest?.observation_window_minutes ??
    auditRecordNumber(observationWindowEvent, "observation_window_minutes");
  const observationRemainingMinutes =
    actionRequest?.observation_window_remaining_minutes ?? observationWindowMinutes;
  const observationExpiryAction =
    actionRequest?.observation_expiry_action ??
    auditRecordString(observationWindowEvent, "observation_expiry_action") ??
    auditRecordString(observationWindowEvent, "expiry_action");
  const latestApprovalAuditEvent =
    activeContext.audit_trail.length > 0
      ? activeContext.audit_trail[activeContext.audit_trail.length - 1]
      : undefined;
  const approvalAuditSourceAvailability =
    activeContext.ui_messages.audit_trail_source_availability === "unavailable"
      ? "unavailable"
      : "available";
  const approvalAuditSourceState: ApprovalAuditSourceState =
    approvalAuditSourceAvailability === "unavailable"
      ? "unavailable"
      : latestApprovalAuditEvent
        ? "records"
        : "empty";
  const approvalAuditCount =
    approvalAuditSourceState === "unavailable"
      ? "unknown"
      : String(activeContext.audit_trail.length);
  const approvalAuditDerivedStatus =
    getApprovalAuditDerivedStatus(latestApprovalAuditEvent);
  const approvalAuditStatusDisplay =
    APPROVAL_AUDIT_STATUS_DISPLAY[approvalAuditDerivedStatus];
  const approvalAuditEventName =
    auditRecordString(latestApprovalAuditEvent, "event") ?? "Unavailable";
  const approvalAuditActorRole =
    auditRecordString(latestApprovalAuditEvent, "actor_role") ?? "Unavailable";
  const approvalAuditArStatus =
    auditRecordString(latestApprovalAuditEvent, "ar_status_after") ?? "Unavailable";
  const approvalAuditCaseState =
    auditRecordString(latestApprovalAuditEvent, "case_state_after") ?? "Unavailable";
  const approvalAuditId =
    auditRecordString(latestApprovalAuditEvent, "audit_id") ?? "Unavailable";
  const hasObservationWindowAudit = activeContext.audit_trail.some(
    (event) => auditRecordString(event, "event") === "OBSERVE_ONLY_SELECTED"
  );
  const hasObservationWindowExpiredAudit =
    auditRecordString(latestApprovalAuditEvent, "event") === "OBSERVATION_WINDOW_EXPIRED";
  const approvalAuditEmptyNotice = uiMessageString(
    activeContext.ui_messages,
    "approval_audit_empty_notice",
    "Approval audit source is available and contains zero records."
  );
  const approvalAuditUnavailableNotice = uiMessageString(
    activeContext.ui_messages,
    "audit_source_unavailable_notice",
    "Approval audit source is unavailable from governed ui_messages."
  );

  useEffect(() => {
    if (!canRenderApprovalCtas) {
      setActiveApprovalDraft(null);
    }
  }, [canRenderApprovalCtas]);

  useEffect(() => {
    if (activeApprovalDraft) {
      approvalDraftCloseButtonRef.current?.focus();
    }
  }, [activeApprovalDraft]);

  function openApprovalDraft(
    action: ApprovalDraftAction,
    trigger: HTMLButtonElement
  ) {
    approvalDraftTriggerRef.current = trigger;
    setActiveApprovalDraft(action);
  }

  function closeApprovalDraft() {
    setActiveApprovalDraft(null);
    window.setTimeout(() => approvalDraftTriggerRef.current?.focus(), 0);
  }

  function trapApprovalDraftDialogFocus(event: KeyboardEvent<HTMLDivElement>) {
    if (event.key === "Escape") {
      closeApprovalDraft();
      return;
    }

    if (event.key !== "Tab") {
      return;
    }

    const focusableItems = Array.from(
      approvalDraftDialogRef.current?.querySelectorAll<HTMLElement>(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      ) ?? []
    ).filter((item) => !item.hasAttribute("disabled"));

    if (focusableItems.length === 0) {
      event.preventDefault();
      return;
    }

    const firstItem = focusableItems[0];
    const lastItem = focusableItems[focusableItems.length - 1];

    if (event.shiftKey && document.activeElement === firstItem) {
      event.preventDefault();
      lastItem.focus();
      return;
    }

    if (!event.shiftKey && document.activeElement === lastItem) {
      event.preventDefault();
      firstItem.focus();
    }
  }

  const activeApprovalCta = APPROVAL_CTA_LABELS.find(
    (cta) => cta.action === activeApprovalDraft
  );
  const isConfigurationDraft = activeApprovalCta?.shell === "configuration";

  if (role === "P1" || role === "P3") {
    const redirectTarget = role === "P1" ? "/inbox" : "/manager";
    return (
      <section
        aria-labelledby="approval-title"
        className="page-region approval-surface"
        data-approval-scope="route-shell-guard-only"
        data-authority-source="resolved-surface-context"
        data-role={role}
        data-route-authority="resolved-surface-context"
        data-testid="approval-surface"
      >
        <article
          className="approval-route-guard"
          data-redirect-target={redirectTarget}
          data-route-guard="redirect-hard"
          data-testid="approval-route-guard"
        >
          <p className="section-kicker">Approval route guard</p>
          <h1 id="approval-title">Approval shell unavailable for {role}</h1>
          <p>
            Role authority is resolved from fixture context. This route does not infer P2
            approval authority from URL or storage.
          </p>
        </article>
      </section>
    );
  }

  return (
    <section
      aria-labelledby="approval-title"
      className="page-region approval-surface"
      data-approval-scope="route-shell-guard-only"
      data-approval-mode={isReadOnlyApprovalShell ? "readonly-container" : "primary-p2-shell"}
      data-authority-source="resolved-surface-context"
      data-role={role}
      data-route-authority="resolved-surface-context"
      data-testid="approval-surface"
    >
      <div className="approval-shell-header">
        <div>
          <p className="section-kicker">
            {isReadOnlyApprovalShell ? "P0 readonly approval container" : "P2 approval shell"}
          </p>
          <h1 id="approval-title">Approval Queue</h1>
          <p>
            {isReadOnlyApprovalShell
              ? "Read-only container only. Approval controls are outside AP-T01."
              : "Shell and guard only. Approval controls, transitions, and timers are outside AP-T01."}
          </p>
        </div>
        <span
          className={`ar-status-pill ${arStatusDisplay.tone}`}
          data-action-authority={arStatusDisplay.actionAuthority}
          data-ar-status={actionRequest?.ar_status ?? "NONE"}
          data-interaction-class={arStatusDisplay.interactionClass}
          data-mapping-source="D-02"
          data-state-migration={arStatusDisplay.stateMigration}
          data-testid="approval-ar-status-pill"
        >
          {arStatusDisplay.label}
        </span>
      </div>

      <article className="approval-shell-card" data-testid="approval-shell-card">
        <dl className="approval-facts">
          <div>
            <dt>Case</dt>
            <dd>{activeCase.id}</dd>
          </div>
          <div>
            <dt>Role</dt>
            <dd>{role}</dd>
          </div>
          <div>
            <dt>AR context</dt>
            <dd>{actionRequest ? actionRequest.ar_id : "Unavailable"}</dd>
          </div>
          <div>
            <dt>Control state</dt>
            <dd>
              {canRenderApprovalCtas
                ? "AP-T04/AP-T05 shell-only action boundary attached; state mutation is disabled"
                : canRenderApprovedPendingLock
                  ? "AP-T07 locked state skeleton attached; VF-12 visual PASS recorded"
                  : canRenderObservationWindowSkeleton
                    ? "AP-T06A observation-window readonly skeleton attached; controls disabled"
                    : "No approve, reject, delay, or observe controls attached"}
            </dd>
          </div>
        </dl>
        <section
          aria-labelledby="approval-audit-source-title"
          className="approval-audit-source-boundary"
          data-audit-count={approvalAuditCount}
          data-audit-source-state={approvalAuditSourceState}
          data-derived-status={approvalAuditDerivedStatus}
          data-derived-status-source="fixed-enum-mapping"
          data-display-mode="display-only"
          data-source-availability={approvalAuditSourceAvailability}
          data-source="activeContext.audit_trail"
          data-source-fields="audit_id,event,actor_role,case_state_after,ar_status_after"
          data-source-guard="source-data-availability"
          data-state-mutation="none"
          data-testid="approval-audit-source-boundary"
        >
          <div>
            <p className="section-kicker">AP-T08</p>
            <h2 id="approval-audit-source-title">Approval audit source boundary</h2>
            <p>
              Display-only audit facts are read from the resolved context. This boundary does not
              create approval state, Search / History output, or Manager summary output.
            </p>
          </div>
          {approvalAuditSourceState === "records" ? (
            <dl className="approval-audit-facts">
              <div>
                <dt>Latest audit</dt>
                <dd data-testid="approval-audit-latest-id">
                  <span data-testid={`audit-${approvalAuditId}`}>{approvalAuditId}</span>
                </dd>
              </div>
              <div>
                <dt>Event</dt>
                <dd data-testid="approval-audit-latest-event">{approvalAuditEventName}</dd>
              </div>
              <div>
                <dt>Actor role</dt>
                <dd data-testid="approval-audit-actor-role">{approvalAuditActorRole}</dd>
              </div>
              <div>
                <dt>Derived status</dt>
                <dd>
                  <span
                    className={`ar-status-pill ${approvalAuditStatusDisplay.tone}`}
                    data-derived-status={approvalAuditDerivedStatus}
                    data-derived-status-source="fixed-enum-mapping"
                    data-testid="approval-audit-derived-status"
                  >
                    {approvalAuditStatusDisplay.label}
                  </span>
                </dd>
              </div>
              <div>
                <dt>AR after event</dt>
                <dd data-testid="approval-audit-ar-status-after">{approvalAuditArStatus}</dd>
              </div>
              <div>
                <dt>Case state after</dt>
                <dd data-testid="approval-audit-case-state-after">{approvalAuditCaseState}</dd>
              </div>
              <div>
                <dt>Observation audit</dt>
                <dd data-testid="approval-audit-observation-presence">
                  {hasObservationWindowAudit ? "Present" : "Not present"}
                </dd>
              </div>
            </dl>
          ) : approvalAuditSourceState === "empty" ? (
            <div
              className="approval-audit-source-state"
              data-audit-row-count={activeContext.audit_trail.length}
              data-coverage-upgrade="not-suggested"
              data-message-source="ui_messages"
              data-source-state="empty"
              data-testid="approval-audit-empty-state"
            >
              <h3>Audit source empty</h3>
              <p>{approvalAuditEmptyNotice}</p>
            </div>
          ) : (
            <div
              className="approval-audit-source-state unavailable"
              data-audit-row-count="unknown"
              data-coverage-upgrade="not-suggested"
              data-message-source="ui_messages"
              data-source-state="unavailable"
              data-testid="approval-audit-unavailable-state"
            >
              <h3>Audit source unavailable</h3>
              <p
                data-message-source="ui_messages"
                data-testid="audit-source-unavailable-notice"
              >
                {approvalAuditUnavailableNotice}
              </p>
            </div>
          )}
        </section>
        {hasObservationWindowExpiredAudit ? (
          <aside
            aria-label="Observation window expired notice"
            className="observation-expired-notice"
            data-auto-execute="absent"
            data-case-state={activeContext.case.case_state}
            data-state-sync-source="mock_state_sync"
            data-testid="observation-expired-notice"
          >
            <strong>Observation window expired</strong>
            <span>
              STATE_SYNC returned this action request to PENDING_APPROVAL. No approval,
              execution, or launch path is inferred from the clock.
            </span>
          </aside>
        ) : null}
        {canRenderApprovalCtas ? (
          <div
            className="approval-cta-boundary"
            data-action-authority="p2-only"
            data-action-wiring="modal-only"
            data-ar-status={actionRequest?.ar_status ?? "NONE"}
            data-state-mutation="none"
            data-testid="approval-cta-boundary"
          >
            <div>
              <p className="section-kicker">AP-T04 / AP-T05</p>
              <h2>Approval action boundary</h2>
              <p>
                P2 may open bounded shell-only decision panels. They do not create ActionMode,
                call an API, or mutate AR state.
              </p>
            </div>
            <div className="approval-cta-grid" aria-label="Approval action boundary">
              {APPROVAL_CTA_LABELS.map((cta) => (
                <button
                  className="approval-cta"
                  data-action-id={cta.id}
                  data-action-permission={activeContext.action_permissions[cta.id] ?? "HIDDEN"}
                  data-action-wiring={cta.shell === "configuration" ? "config-shell-only" : "modal-only"}
                  data-state-mutation="none"
                  data-testid={`approval-cta-${cta.id}`}
                  key={cta.id}
                  onClick={(event) => openApprovalDraft(cta.action, event.currentTarget)}
                  type="button"
                >
                  {cta.label}
                </button>
              ))}
            </div>
          </div>
        ) : null}
        {canRenderApprovedPendingLock ? (
          <div
            className="approval-lock-boundary"
            data-action-controls="absent"
            data-ar-status={actionRequest.ar_status}
            data-state-migration="none"
            data-testid="approval-lock-boundary"
            data-vf-12-state="pending"
            data-visual-state="skeleton"
          >
            <p className="section-kicker">AP-T07</p>
            <h2>Approved pending execution</h2>
            <p>
              This request is locked and read-only in the frontend. Execution status, reopen,
              revoke, and withdraw behavior are outside this bounded slice.
            </p>
          </div>
        ) : null}
        {canRenderObservationWindowSkeleton ? (
          <div
            className="approval-observation-boundary"
            data-ar-status={actionRequest.ar_status}
            data-case-state={activeContext.case.case_state}
            data-real-backend-protocol="none"
            data-observation-window-readonly="true"
            data-state-migration="none"
            data-state-sync="mock-helper-only"
            data-state-sync-source="emitStateSync"
            data-testid="approval-observation-window-skeleton"
            data-timer-authority="none"
            data-vf-11-state="pass-input-skeleton-only"
            data-visual-state="skeleton"
          >
            <div data-testid="observation-window-banner">
              <p className="section-kicker">AP-T06A / VF-11</p>
              <h2>Observation window active</h2>
              <p>
                This is a static readonly observation-window skeleton. Remaining time is display
                evidence only; material state migration still requires governed state sync.
              </p>
              <span
                className="observation-window-lock-badge"
                data-testid="observation-window-lock-badge"
              >
                Read-only until STATE_SYNC
              </span>
            </div>
            <dl className="approval-observation-facts">
              <div>
                <dt>Total window</dt>
                <dd data-testid="observation-window-total">
                  {observationWindowMinutes === null ? "Unavailable" : `${observationWindowMinutes} min`}
                </dd>
              </div>
              <div>
                <dt>Remaining</dt>
                <dd data-testid="observation-window-remaining">
                  {observationRemainingMinutes === null
                    ? "Unavailable"
                    : `${observationRemainingMinutes} min`}
                </dd>
              </div>
              <div>
                <dt>Expiry action</dt>
                <dd data-testid="observation-expiry-action">
                  {observationExpiryAction ?? "Unavailable"}
                </dd>
              </div>
            </dl>
            <div
              aria-label="Readonly observation controls"
              className="approval-disabled-controls"
              data-action-wiring="none"
              data-state-mutation="none"
            >
              <button
                aria-disabled="true"
                data-testid="approve-mode-button"
                disabled
                type="button"
              >
                Approve
              </button>
              <button
                aria-disabled="true"
                data-testid="reject-mode-button"
                disabled
                type="button"
              >
                Reject
              </button>
              <button
                aria-disabled="true"
                data-testid="delay-decision-button"
                disabled
                type="button"
              >
                Delay
              </button>
              <button
                aria-disabled="true"
                data-testid="observe-only-button"
                disabled
                type="button"
              >
                Observe
              </button>
              {/* view-details-button: secondary case navigation, disabled during active observation window. */}
              <button
                aria-disabled="true"
                data-action-type="secondary-case-navigation"
                data-disabled-reason="active-observation-window"
                data-testid="view-details-button"
                disabled
                type="button"
              >
                View details
              </button>
            </div>
          </div>
        ) : null}
        {activeApprovalDraft && activeApprovalCta && actionRequest ? (
          <div className="approval-draft-dialog-backdrop" role="presentation">
            <div
              aria-labelledby="approval-draft-dialog-title"
              aria-modal="true"
              className="approval-draft-dialog"
              data-draft-action={activeApprovalDraft}
              data-state-mutation="none"
              data-testid={
                isConfigurationDraft
                  ? "approval-configuration-dialog"
                  : "approval-strong-confirm-dialog"
              }
              onKeyDown={trapApprovalDraftDialogFocus}
              ref={approvalDraftDialogRef}
              role="dialog"
            >
              <div>
                <p className="section-kicker">
                  {isConfigurationDraft ? "AP-T05 configuration shell" : "AP-T04 strong confirm"}
                </p>
                <h2 id="approval-draft-dialog-title">
                  {isConfigurationDraft
                    ? `${activeApprovalCta.label} configuration`
                    : `${activeApprovalCta.label} strong confirm`}
                </h2>
                <p>
                  This panel is a bounded frontend shell. It does not submit, schedule, or change
                  the action request.
                </p>
              </div>
              <dl className="approval-draft-facts">
                <div>
                  <dt>Case</dt>
                  <dd>{activeCase.id}</dd>
                </div>
                <div>
                  <dt>AR status</dt>
                  <dd>{actionRequest.ar_status}</dd>
                </div>
                <div>
                  <dt>Selected shell</dt>
                  <dd>{activeApprovalCta.label}</dd>
                </div>
                <div>
                  <dt>State change</dt>
                  <dd>None</dd>
                </div>
              </dl>
              {isConfigurationDraft ? (
                <div
                  className="approval-config-shell"
                  data-state-mutation="none"
                  data-testid="approval-delay-observe-config-shell"
                  data-timer-authority="none"
                >
                  <p>
                    Delay and observe values are not submitted here. Observation timing remains
                    STATE_SYNC-driven and cannot be advanced by the frontend.
                  </p>
                </div>
              ) : (
                <div
                  className="approval-strong-confirm-facts"
                  data-testid="approval-strong-confirm-facts"
                >
                  <p>
                    Strong confirmation facts are displayed before any future approval action can
                    be wired. Confirm is intentionally unavailable in this ticket.
                  </p>
                </div>
              )}
              <div className="approval-draft-dialog-actions">
                <button
                  data-testid="approval-draft-confirm"
                  data-state-mutation="none"
                  disabled
                  type="button"
                >
                  Confirm unavailable
                </button>
                <button
                  onClick={closeApprovalDraft}
                  ref={approvalDraftCloseButtonRef}
                  type="button"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        ) : null}
        {!actionRequest ? (
          <p
            className="approval-safe-empty"
            data-rendering-state="data-unavailable"
            data-testid="approval-safe-empty"
          >
            Action request context is unavailable. The shell remains read-only.
          </p>
        ) : null}
      </article>
    </section>
  );
}

export function ManagerView({
  activeCase,
  activeContext,
  onRouteRedirect
}: {
  activeCase: WorkbenchCase;
  activeContext: ResolvedSurfaceContext;
  onRouteRedirect?: (targetRoute: Route) => void;
}) {
  const role = activeContext.session.role;
  const redirectRoute: Route = role === "P2" ? "approval" : "inbox";
  const redirectTarget = redirectRoute === "approval" ? "/approval" : "/inbox";

  useEffect(() => {
    if (role !== "P3") {
      onRouteRedirect?.(redirectRoute);
    }
  }, [onRouteRedirect, redirectRoute, role]);

  if (role !== "P3") {
    return (
      <section
        aria-labelledby="manager-route-guard-title"
        className="page-region manager-view-surface"
        data-authority-source="resolved-surface-context"
        data-manager-entry="denied"
        data-manager-state-transfer="none"
        data-p0-p2-placeholders="absent"
        data-redirect-target={redirectTarget}
        data-role={role}
        data-route-action="no-entry-guard"
        data-route-guard="role-not-eligible"
        data-testid="manager-route-guard"
      >
        <p className="section-kicker">Manager route guard</p>
        <h1 id="manager-route-guard-title">Manager View unavailable</h1>
        <p>
          This route requires a resolved P3 manager context. URL and storage values cannot
          create manager authority.
        </p>
      </section>
    );
  }

  // Fixture audit trails are append-ordered; the latest event is the final item.
  const latestManagerAuditEvent =
    activeContext.audit_trail.length > 0
      ? activeContext.audit_trail[activeContext.audit_trail.length - 1]
      : undefined;
  const managerAuditDerivedStatus = getApprovalAuditDerivedStatus(latestManagerAuditEvent);
  const managerAuditStatusDisplay = APPROVAL_AUDIT_STATUS_DISPLAY[managerAuditDerivedStatus];
  const managerAuditId =
    auditRecordString(latestManagerAuditEvent, "audit_id") ?? "No audit record";
  const managerAuditEvent =
    auditRecordString(latestManagerAuditEvent, "event") ?? "No audit event";
  const managerAuditActorRole =
    auditRecordString(latestManagerAuditEvent, "actor_role") ?? "Unavailable";
  const managerAuditArStatusAfter =
    auditRecordString(latestManagerAuditEvent, "ar_status_after") ?? "Unavailable";
  const managerAuditCaseStateAfter =
    auditRecordString(latestManagerAuditEvent, "case_state_after") ?? "Unavailable";
  const managerHasObservationAudit = activeContext.audit_trail.some(
    (event) => auditRecordString(event, "event") === "OBSERVE_ONLY_SELECTED"
  );

  const kpiCards = [
    {
      id: "coverage",
      label: "Coverage baseline",
      value: activeCase.coverage,
      source: "resolved-surface-context",
      note: "Organization-visible coverage summary, not a field unlock."
    },
    {
      id: "mtta",
      label: "MTTA",
      value: "—",
      source: "data-unavailable",
      note: "No runtime metric source is attached in MV-T01."
    },
    {
      id: "noise-compression",
      label: "Noise compression",
      value: "—",
      source: "data-unavailable",
      note: "No frontend inference or static ROI number."
    },
    {
      id: "approval-throughput",
      label: "Approval throughput",
      value: "—",
      source: "data-unavailable",
      note: "No frontend-derived throughput; approval audit summary remains read-only."
    }
  ];

  return (
    <section
      aria-labelledby="manager-view-title"
      className="page-region manager-view-surface"
      data-authority-source="resolved-surface-context"
      data-handoff-payload="none"
      data-manager-scope="mv-t01-mv-t04-readonly-summary"
      data-p0-p2-placeholders="absent"
      data-role={role}
      data-testid="manager-view-surface"
    >
      <div className="manager-topline">
        <div>
          <p className="section-kicker">Manager View</p>
          <h1 id="manager-view-title">Manager Summary</h1>
          <p>
            P3 read-only management posture, derived from mock fixture context and bounded
            to MV-T01 page structure plus MV-T04 audit summary.
          </p>
        </div>
        <span
          className="manager-readonly-badge"
          data-testid="manager-readonly-badge"
          data-workflow-authority="none"
        >
          Read-only
        </span>
      </div>

      <div className="manager-layout" aria-label="Manager view regions">
        <aside
          aria-labelledby="manager-scope-title"
          className="manager-scope-rail"
          data-testid="manager-scope-rail"
        >
          <h2 id="manager-scope-title">Manager Scope</h2>
          <dl className="manager-facts">
            <div>
              <dt>Role</dt>
              <dd>{role}</dd>
            </div>
            <div>
              <dt>Coverage</dt>
              <dd>{activeCase.coverage}</dd>
            </div>
            <div>
              <dt>Case state</dt>
              <dd>{CASE_STATE_LABELS[activeCase.state]}</dd>
            </div>
          </dl>
          <div
            className="manager-boundary-note"
            data-approval-workflow="not-implemented"
            data-deep-link-handoff="route-only"
            data-testid="manager-readonly-boundary"
          >
            No approval queue, action controls, host raw evidence, or serialized handoff payload.
          </div>
        </aside>

        <article
          aria-labelledby="manager-brief-title"
          className="manager-brief-narrative"
          data-testid="manager-brief-narrative"
        >
          <h2 id="manager-brief-title">Manager Brief</h2>
          <section data-brief-section="what">
            <h3>WHAT</h3>
            <p>{activeCase.summary}</p>
          </section>
          <section data-brief-section="why">
            <h3>WHY</h3>
            <p>Coverage and AR status are shown as management context only.</p>
          </section>
          <section data-brief-section="honesty">
            <h3>HONESTY</h3>
            <p>
              KPI values without a governed source render as unavailable rather than inferred.
            </p>
          </section>
          <section data-brief-section="decision">
            <h3>DECISION</h3>
            <p>P3 may ask management follow-up questions; individual approval actions are absent.</p>
          </section>
        </article>

        <aside
          aria-labelledby="manager-summary-title"
          className="manager-context-summary"
          data-testid="manager-context-summary"
        >
          <h2 id="manager-summary-title">Context Summary</h2>
          <div className="manager-kpi-grid" data-testid="manager-kpi-grid">
            {kpiCards.map((card) => (
              <article
                className="manager-kpi-card"
                data-kpi-id={card.id}
                data-kpi-source={card.source}
                data-testid={`manager-kpi-card-${card.id}`}
                key={card.id}
              >
                <span>{card.label}</span>
                <strong>{card.value}</strong>
                <p>{card.note}</p>
              </article>
            ))}
          </div>
          <div
            className="manager-audit-boundary"
            data-approval-audit-summary="implemented"
            data-source="activeContext.audit_trail"
            data-state-mutation="none"
            data-testid="manager-audit-boundary"
          >
            <section
              aria-labelledby="manager-approval-audit-title"
              className="manager-approval-audit-summary"
              data-audit-count={activeContext.audit_trail.length}
              data-derived-status={managerAuditDerivedStatus}
              data-derived-status-source="fixed-enum-mapping"
              data-display-mode="read-only-summary"
              data-full-audit-chain="not-rendered"
              data-p0-p2-placeholders="absent"
              data-role={role}
              data-source="activeContext.audit_trail"
              data-source-fields="audit_id,event,actor_role,case_state_after,ar_status_after"
              data-source-order="AP-T08-before-SH-T08-before-MV-T04"
              data-source-surface="manager"
              data-state-mutation="none"
              data-testid="manager-approval-audit-summary"
            >
              <div>
                <h3 id="manager-approval-audit-title">Approval Audit Summary</h3>
                <p>
                  P3 read-only summary sourced from the existing approval audit trail.
                </p>
              </div>
              <dl className="manager-approval-audit-facts">
                <div>
                  <dt>Audit record</dt>
                  <dd data-testid="manager-approval-audit-latest-id">{managerAuditId}</dd>
                </div>
                <div>
                  <dt>Event</dt>
                  <dd data-testid="manager-approval-audit-latest-event">{managerAuditEvent}</dd>
                </div>
                <div>
                  <dt>Actor role</dt>
                  <dd data-testid="manager-approval-audit-actor-role">
                    {managerAuditActorRole}
                  </dd>
                </div>
                <div>
                  <dt>Derived status</dt>
                  <dd
                    data-derived-status={managerAuditDerivedStatus}
                    data-derived-status-source="fixed-enum-mapping"
                    data-testid="manager-approval-audit-derived-status"
                  >
                    {managerAuditStatusDisplay.label}
                  </dd>
                </div>
                <div>
                  <dt>AR status after</dt>
                  <dd data-testid="manager-approval-audit-ar-status-after">
                    {managerAuditArStatusAfter}
                  </dd>
                </div>
                <div>
                  <dt>Case state after</dt>
                  <dd data-testid="manager-approval-audit-case-state-after">
                    {managerAuditCaseStateAfter}
                  </dd>
                </div>
                <div>
                  <dt>Observation audit</dt>
                  <dd data-testid="manager-approval-audit-observation-presence">
                    {managerHasObservationAudit ? "Present" : "Not present"}
                  </dd>
                </div>
              </dl>
            </section>
          </div>
        </aside>
      </div>

      <section
        aria-labelledby="manager-dialogue-title"
        className="manager-dialogue-dock"
        data-chip-source="runtime-only"
        data-testid="manager-dialogue-dock"
      >
        <div>
          <h2 id="manager-dialogue-title">Dialogue Dock</h2>
          <p>Recommended chips are hidden until a governed runtime source supplies them.</p>
        </div>
        <form className="manager-dialogue-form">
          <label className="sr-only" htmlFor="manager-dialogue-input">
            Manager follow-up input
          </label>
          <input
            id="manager-dialogue-input"
            placeholder="Ask about management posture"
            readOnly
          />
          <button type="button">Send</button>
        </form>
      </section>
    </section>
  );
}

function MockContextSelector({
  activeContext,
  activePhase,
  activeRedlineFixtureId,
  onPhaseChange,
  onRedlineFixtureChange
}: {
  activeContext: ResolvedSurfaceContext;
  activePhase: CoreSurfaceFixturePhase;
  activeRedlineFixtureId: RedlineFixtureId | "";
  onPhaseChange: (phase: number) => void;
  onRedlineFixtureChange: (fixtureId: string) => void;
}) {
  return (
    <div
      className="mock-context"
      aria-label="Mock fixture resolved context"
      data-testid="resolved-context"
    >
      <label htmlFor="mock-phase-selector">Mock fixture phase</label>
      <select
        id="mock-phase-selector"
        onChange={(event) => onPhaseChange(Number(event.target.value))}
        value={activePhase.phase}
      >
        {CORE_SURFACE_FIXTURE_PHASE_OPTIONS.map((phase) => (
          <option key={phase.phase} value={phase.phase}>
            {`Phase ${phase.phase} - ${phase.surface} - ${phase.caseState}`}
          </option>
        ))}
      </select>
      <div className="resolved-context-pills">
        <span>{`Role ${activeContext.session.role}`}</span>
        <span>{activeContext.surface}</span>
        <span>{activeContext.case.case_state}</span>
        <span>{activeContext.action_request?.ar_status ?? "AR none"}</span>
      </div>
      <label htmlFor="mock-redline-selector">Mock redline fixture</label>
      <select
        id="mock-redline-selector"
        onChange={(event) => onRedlineFixtureChange(event.target.value)}
        value={activeRedlineFixtureId}
      >
        <option value="">Phase fixture baseline</option>
        {E0_04C_REDLINE_FIXTURE_IDS.map((fixtureId) => (
          <option key={fixtureId} value={fixtureId}>
            {fixtureId}
          </option>
        ))}
      </select>
    </div>
  );
}

function InboxView({
  cases,
  onNavigateToApproval,
  onOpenCase,
  role
}: {
  cases: WorkbenchCase[];
  onNavigateToApproval: () => void;
  onOpenCase: (caseId: string) => void;
  role: Role;
}) {
  const isP3Readonly = role === "P3";
  const canRenderApprovalNavigation = role === "P2";

  return (
    <section
      className="page-region"
      aria-labelledby="inbox-title"
      data-action-authority="none"
      data-inbox-mode={isP3Readonly ? "readonly" : "case-first"}
      data-role={role}
      data-testid="inbox-surface"
    >
      <div className="page-heading">
        <p>Case Inbox</p>
        <h1 id="inbox-title">Case-first intake</h1>
      </div>

      <div
        className="case-grid"
        data-testid={isP3Readonly ? "p3-readonly-inbox-variant" : "case-first-inbox-list"}
      >
        {cases.map((item) => (
          <article
            className={isP3Readonly ? "case-card readonly-case-card" : "case-card"}
            data-authority-source={isP3Readonly ? "resolved-surface-context" : undefined}
            data-testid={isP3Readonly ? `p3-readonly-inbox-card-${item.id}` : undefined}
            data-visual-state={isP3Readonly ? "skeleton" : undefined}
            data-work-queue-affordance={isP3Readonly ? "absent" : undefined}
            key={item.id}
          >
            <div className="case-card-topline">
              <span className={`risk ${item.risk.toLowerCase()}`}>{item.risk}</span>
              <span>{item.coverage}</span>
            </div>
            <h2>{item.title}</h2>
            <p>{item.verdict}</p>
            {canRenderApprovalNavigation ? (
              <aside
                aria-label="Approval navigation hint"
                className="inbox-approval-entry"
                data-action-mode="none"
                data-approval-authority-transfer="none"
                data-ar-hint-mode="display-only"
                data-ar-status-display={
                  item.arStatus ? AR_STATUS_DISPLAY[item.arStatus].label : "No AR"
                }
                data-route-authority="resolved-surface-context"
                data-state-mutation="none"
                data-target-route="/approval"
                data-testid={`inbox-approval-navigation-entry-${item.id}`}
              >
                <span>Approval context</span>
                <p>
                  {item.arStatus
                    ? `AR status: ${AR_STATUS_DISPLAY[item.arStatus].label}. Navigation only.`
                    : "No action request is active. Navigation only."}
                </p>
                <button
                  data-authority-payload="none"
                  data-testid={`inbox-approval-navigation-button-${item.id}`}
                  onClick={onNavigateToApproval}
                  type="button"
                >
                  Open approval context
                </button>
              </aside>
            ) : null}
            {isP3Readonly ? (
              <dl className="readonly-case-facts" aria-label="Inbox case facts">
                <div>
                  <dt>Case</dt>
                  <dd data-testid={`p3-readonly-inbox-case-id-${item.id}`}>{item.id}</dd>
                </div>
                <div>
                  <dt>Coverage</dt>
                  <dd data-testid={`p3-readonly-inbox-coverage-${item.id}`}>{item.coverage}</dd>
                </div>
                <div>
                  <dt>State</dt>
                  <dd data-testid={`p3-readonly-inbox-case-state-${item.id}`}>
                    {CASE_STATE_LABELS[item.state]}
                  </dd>
                </div>
              </dl>
            ) : null}
            <div className="next-step">{item.nextStep}</div>
            {isP3Readonly ? (
              <div
                className="readonly-inbox-notice"
                data-testid={`p3-readonly-inbox-notice-${item.id}`}
                role="note"
              >
                P3 readonly skeleton: summary fields only, with no case operation attached.
              </div>
            ) : (
              <button onClick={() => onOpenCase(item.id)} type="button">
                <span>Open case</span>
                <ChevronRight aria-hidden="true" size={18} />
              </button>
            )}
          </article>
        ))}
      </div>
    </section>
  );
}

function SearchHistoryView({
  activeCase,
  activeContext,
  onNavigateToManager
}: {
  activeCase: WorkbenchCase;
  activeContext: ResolvedSurfaceContext;
  onNavigateToManager: () => void;
}) {
  const queryParams = new URLSearchParams(window.location.search);
  const requestedCoverageParam = queryParams.get("coverage");
  const requestedCoverage = isCoverageLevel(requestedCoverageParam)
    ? requestedCoverageParam
    : null;
  const requestedFocusParam = queryParams.get("focus");
  const requestedFocus = isSearchFocusScope(requestedFocusParam) ? requestedFocusParam : "summary";
  const isAuditFocusRequested =
    requestedFocus === "approval_audit" || requestedFocus === "history_audit";
  const isAuditFocusDowngraded = activeContext.session.role !== "P3" && isAuditFocusRequested;
  const effectiveFocus = isAuditFocusDowngraded ? "summary" : requestedFocus;
  const recordedCoverage = activeContext.case.coverage_level;
  const currentCoverage = requestedCoverage ?? recordedCoverage;
  const effectiveCoverage = clampCoverageRequest(requestedCoverage, recordedCoverage);
  const clampReason = formatCoverageClampReason(
    recordedCoverage,
    currentCoverage,
    effectiveCoverage
  );
  const isClamped = currentCoverage !== effectiveCoverage || recordedCoverage !== effectiveCoverage;
  const isHistoricalUpgradeBlocked = coverageRank(currentCoverage) > coverageRank(recordedCoverage);
  const canRenderManagerHandoff =
    activeContext.session.role === "P3" &&
    (effectiveFocus === "approval_audit" || effectiveFocus === "history_audit");
  const canRenderHistoryApprovalAudit =
    activeContext.session.role === "P3" &&
    (effectiveFocus === "approval_audit" || effectiveFocus === "history_audit");
  const latestHistoryAuditEvent =
    activeContext.audit_trail.length > 0
      ? activeContext.audit_trail[activeContext.audit_trail.length - 1]
      : undefined;
  const historyAuditDerivedStatus = getApprovalAuditDerivedStatus(latestHistoryAuditEvent);
  const historyAuditStatusDisplay = APPROVAL_AUDIT_STATUS_DISPLAY[historyAuditDerivedStatus];
  const historyAuditId = auditRecordString(latestHistoryAuditEvent, "audit_id") ?? "Unavailable";
  const historyAuditEventName =
    auditRecordString(latestHistoryAuditEvent, "event") ?? "Unavailable";
  const historyAuditActorRole =
    auditRecordString(latestHistoryAuditEvent, "actor_role") ?? "Unavailable";
  const historyAuditCaseState =
    auditRecordString(latestHistoryAuditEvent, "case_state_after") ?? "Unavailable";
  const historyHasObservationWindowAudit = activeContext.audit_trail.some(
    (event) => auditRecordString(event, "event") === "OBSERVE_ONLY_SELECTED"
  );

  return (
    <section
      className="page-region history-surface"
      aria-labelledby="history-title"
      data-testid="history-surface"
    >
      <div className="page-heading">
        <p>Search / History</p>
        <h1 id="history-title">History guard</h1>
      </div>

      <article
        className="history-guard-panel"
        data-authority-source="resolved-surface-context"
        data-current-coverage={currentCoverage}
        data-effective-coverage={effectiveCoverage}
        data-recorded-coverage={recordedCoverage}
        data-requested-coverage={requestedCoverage ?? "none"}
        data-route-order="resolve-clamp-guard-render"
        data-route-source="frontend-route"
        data-testid="history-route-guard"
      >
        <div>
          <p className="section-kicker">SH-T03</p>
          <h2>Clamp-first history route</h2>
          <p>
            Route input is resolved, clamped to the recorded coverage ceiling, then rendered as a
            read-only history guard.
          </p>
        </div>
        <div
          aria-label="Dual coverage clamp labels"
          className="dual-coverage-label-block"
          data-current-coverage={currentCoverage}
          data-effective-visibility={effectiveCoverage}
          data-recorded-coverage={recordedCoverage}
          data-testid="dual-coverage-label-block"
        >
          <span data-testid="recorded-coverage-label">Recorded: {recordedCoverage}</span>
          <span data-testid="current-coverage-label">Current: {currentCoverage}</span>
          <span data-testid="effective-visibility-label">
            Effective: {effectiveCoverage}
          </span>
          <p data-testid="clamp-reason">{clampReason}</p>
          {isClamped ? (
            <p
              className="missing-signal-notice"
              data-message-source="ui_messages"
              data-testid="missing-signal-notice"
            >
              Some historical signals are unavailable at the effective visibility level.
            </p>
          ) : null}
          {isHistoricalUpgradeBlocked ? (
            <p
              className="historical-upgrade-blocked-notice"
              data-testid="historical-upgrade-blocked-notice"
            >
              This is history integrity protection, not a current coverage shortage.
              Higher current coverage does not unlock data that was not recorded.
            </p>
          ) : null}
        </div>
        <dl className="history-guard-facts" aria-label="History route guard facts">
          <div>
            <dt>Recorded coverage</dt>
            <dd>{recordedCoverage}</dd>
          </div>
          <div>
            <dt>Requested coverage</dt>
            <dd>{requestedCoverage ?? "none"}</dd>
          </div>
          <div>
            <dt>Effective coverage</dt>
            <dd>{effectiveCoverage}</dd>
          </div>
          <div>
            <dt>Authority</dt>
            <dd>ResolvedSurfaceContext</dd>
          </div>
        </dl>
      </article>

      <section
        aria-labelledby="history-focus-title"
        className="history-focus-scope-panel"
        data-effective-focus={effectiveFocus}
        data-focus-authority="hint-only"
        data-requested-focus={requestedFocusParam ?? "none"}
        data-testid="history-focus-scopes"
      >
        <div>
          <p className="section-kicker">SH-T05</p>
          <h2 id="history-focus-title">Read-only focus scopes</h2>
          <p>
            Focus is a display hint only. It does not change role, coverage, case state,
            ActionMode, or write authority.
          </p>
        </div>
        <ul aria-label="Allowed history focus scopes">
          {SEARCH_FOCUS_SCOPES.map((scope) => (
            <li
              aria-current={scope.id === effectiveFocus ? "true" : undefined}
              data-focus-scope={scope.id}
              data-testid="history-focus-scope"
              key={scope.id}
            >
              <span>{scope.label}</span>
              <p>{scope.description}</p>
            </li>
          ))}
        </ul>
      </section>

      {isAuditFocusDowngraded ? (
        <p
          className="history-focus-downgrade"
          data-effective-focus={effectiveFocus}
          data-requested-focus={requestedFocus}
          data-testid="history-focus-downgrade"
        >
          Audit focus is unavailable for this role; summary remains active.
        </p>
      ) : null}

      <section
        aria-label="History empty-state split"
        className="history-empty-state-split"
        data-frame-state="hf-sh-02-v0-2-pass"
        data-testid="history-empty-state-split"
      >
        <article
          className="history-empty-state"
          data-empty-state-kind="structural"
          data-empty-state-status="not-current-result"
          data-message-source="ui_messages"
          data-testid="structural-empty-state"
        >
          <p className="section-kicker">SH-T06</p>
          <h2>Structural empty</h2>
          <p>
            No matching historical case is available under the current visibility scope.
          </p>
        </article>
        <article
          className="history-empty-state"
          data-effective-visibility={effectiveCoverage}
          data-empty-state-kind="degraded"
          data-empty-state-status={isClamped ? "active" : "not-active"}
          data-message-source="ui_messages"
          data-recorded-coverage={recordedCoverage}
          data-testid="degraded-empty-state"
        >
          <p className="section-kicker">SH-T06</p>
          <h2>Degraded empty</h2>
          <p>
            {isClamped
              ? "Some historical fields are unavailable after coverage clamp; no field is reconstructed."
              : "No historical fields are omitted by coverage clamp for this route."}
          </p>
        </article>
      </section>

      {canRenderHistoryApprovalAudit ? (
        <section
          aria-labelledby="search-history-approval-audit-title"
          className="history-approval-audit-boundary"
          data-audit-count={activeContext.audit_trail.length}
          data-derived-status={historyAuditDerivedStatus}
          data-derived-status-source="fixed-enum-mapping"
          data-display-mode="read-only-summary"
          data-full-audit-chain="not-rendered"
          data-role="P3"
          data-source="activeContext.audit_trail"
          data-source-order="AP-T08-before-SH-T08"
          data-source-surface="history"
          data-state-mutation="none"
          data-testid="search-history-approval-audit-boundary"
        >
          <div>
            <p className="section-kicker">SH-T08</p>
            <h2 id="search-history-approval-audit-title">History approval audit boundary</h2>
            <p>
              Read-only audit summary sourced from resolved context. The full audit chain and
              approval controls are not rendered in Search / History.
            </p>
          </div>
          <dl className="history-approval-audit-facts">
            <div>
              <dt>Latest audit</dt>
              <dd data-testid="history-approval-audit-latest-id">{historyAuditId}</dd>
            </div>
            <div>
              <dt>Event</dt>
              <dd data-testid="history-approval-audit-latest-event">
                {historyAuditEventName}
              </dd>
            </div>
            <div>
              <dt>Actor role</dt>
              <dd data-testid="history-approval-audit-actor-role">{historyAuditActorRole}</dd>
            </div>
            <div>
              <dt>Derived status</dt>
              <dd>
                <span
                  className={`ar-status-pill ${historyAuditStatusDisplay.tone}`}
                  data-derived-status={historyAuditDerivedStatus}
                  data-derived-status-source="fixed-enum-mapping"
                  data-testid="history-approval-audit-derived-status"
                >
                  {historyAuditStatusDisplay.label}
                </span>
              </dd>
            </div>
            <div>
              <dt>Case state after</dt>
              <dd data-testid="history-approval-audit-case-state-after">
                {historyAuditCaseState}
              </dd>
            </div>
            <div>
              <dt>Observation audit</dt>
              <dd data-testid="history-approval-audit-observation-presence">
                {historyHasObservationWindowAudit ? "Present" : "Not present"}
              </dd>
            </div>
            <div>
              <dt>Terminal close</dt>
              <dd data-testid="history-approval-audit-terminal-close">Unavailable</dd>
            </div>
          </dl>
        </section>
      ) : null}

      {canRenderManagerHandoff ? (
        <article
          className="history-manager-handoff"
          data-authority-source="resolved-surface-context"
          data-handoff-payload="none"
          data-source-focus={effectiveFocus}
          data-source-surface="P3_SEARCH_HISTORY"
          data-storage-authority="none"
          data-target-route="/manager"
          data-testid="manager-deep-link-handoff"
          data-url-authority="none"
        >
          <div>
            <p className="section-kicker">MV-T03</p>
            <h2>Manager handoff</h2>
            <p>
              Route-only navigation to the existing P3 Manager View. The target keeps using
              resolved context; no audit payload is serialized through URL or storage.
            </p>
          </div>
          <button
            data-testid="manager-deep-link-button"
            data-state-mutation="none"
            onClick={onNavigateToManager}
            type="button"
          >
            Open Manager View
          </button>
        </article>
      ) : null}

      <article
        className="history-case-row historical-case-list-item"
        data-current-coverage={currentCoverage}
        data-current-visible={effectiveCoverage}
        data-detail-context-authority="case-route"
        data-effective-visibility-owned-by="case-detail"
        data-effective-visibility={effectiveCoverage}
        data-frame-state="hf-sh-01-02-vf14-v0-2-pass"
        data-handoff-state="not-implemented"
        data-list-item-context="summary-only"
        data-recorded-coverage={recordedCoverage}
        data-testid="historical-case-list-item"
        data-visual-state="skeleton"
      >
        <div className="history-case-row-main">
          <span data-testid="historical-list-case-id">{activeCase.id}</span>
          <h2 data-testid="historical-list-verdict">{activeCase.verdict}</h2>
          <p data-testid="historical-list-snippet">{activeCase.summary}</p>
        </div>
        <dl className="historical-list-meta" aria-label="Historical case list item metadata">
          <div>
            <dt>Timestamp</dt>
            <dd data-testid="historical-list-timestamp" data-timestamp-state="unavailable">
              Mock fixture timestamp unavailable
            </dd>
          </div>
          <div>
            <dt>Recorded coverage</dt>
            <dd data-testid="historical-list-recorded-coverage">{recordedCoverage}</dd>
          </div>
          <div>
            <dt>Current visible</dt>
            <dd data-testid="historical-list-current-visible">{effectiveCoverage}</dd>
          </div>
        </dl>
        <button
          className="view-approval-audit"
          data-guard="role-source-data"
          data-source="history"
          data-state-mutation="none"
          data-testid="view-approval-audit"
          type="button"
        >
          View approval audit
        </button>
        <p className="historical-list-boundary" data-testid="historical-list-boundary">
          List item is lightweight only; detail visibility resolves after a future case-route
          handoff.
        </p>
      </article>

      <p className="history-write-guard" data-testid="history-write-guard">
        Read-only history surface. No write actions are attached.
      </p>
    </section>
  );
}

export function CoverageHealthView({
  activeCase,
  activeContext
}: {
  activeCase: WorkbenchCase;
  activeContext: ResolvedSurfaceContext;
}) {
  const role = activeContext.session.role;
  const isAllowedRole = role === "P0" || role === "P2";
  const isP0CoverageAdmin = role === "P0";
  const coverage = activeContext.case.coverage_level;
  const effectiveVisibility = activeContext.resolved_visibility.effective_visibility_level;
  const visibilityEntries = Object.entries(activeContext.resolved_visibility.fields);
  const visibleOrDegradedFieldCount = visibilityEntries.filter(([, state]) => state !== "OFF").length;
  const fieldPresenceRate = `${visibleOrDegradedFieldCount}/${visibilityEntries.length}`;
  const fieldSwitchCounts = SWITCH_STATE_ORDER.map((state) => ({
    state,
    count: visibilityEntries.filter(([, value]) => value === state).length
  })).filter((item) => item.count > 0);
  const availableCoverageHealthMessages = COVERAGE_HEALTH_UI_MESSAGE_KEYS.map((key) => ({
    key,
    value: activeContext.ui_messages[key]
  })).filter((message) => message.value !== undefined);
  const sourceHealthMessages = [
    {
      key: "fixture_status",
      label: "Source availability",
      displayState: "degraded-placeholder",
      value: activeContext.ui_messages.fixture_status
    },
    {
      key: "mock_only_notice",
      label: "Source boundary",
      displayState: "unavailable-placeholder",
      value: activeContext.ui_messages.mock_only_notice
    }
  ].filter((message) => message.value !== undefined);
  const vf01NoticeCards = COVERAGE_HEALTH_NOTICE_ANCHORS.map((anchor) => ({
    ...anchor,
    value: activeContext.ui_messages[anchor.key]
  })).filter((anchor) => anchor.value !== undefined);

  return (
    <section
      className="page-region coverage-health-surface"
      aria-labelledby="coverage-health-title"
      data-authority-source="resolved-surface-context"
      data-live-health-source="none"
      data-role={role}
      data-route-authority="role-filtered-nav"
      data-testid="coverage-health-surface"
      data-vf-01-state={isP0CoverageAdmin ? "baseline-reconciled" : "pending"}
      data-visual-state={isP0CoverageAdmin ? "semantic-frame" : "skeleton"}
    >
      <div className="page-heading">
        <p>Coverage & Health</p>
        <h1 id="coverage-health-title">
          {isP0CoverageAdmin ? "Coverage health baseline" : "Coverage health skeleton"}
        </h1>
      </div>

      {!isAllowedRole ? (
        <article
          className="coverage-health-guard"
          data-route-guard="role-not-eligible"
          data-testid="coverage-health-route-guard"
        >
          <h2>Surface unavailable</h2>
          <p>
            Coverage & Health is not exposed for this role. Navigation must crop this entry rather
            than render a disabled operational surface.
          </p>
        </article>
      ) : (
        <div
          className="coverage-health-root"
          data-current-coverage={coverage}
          data-frame-scope={isP0CoverageAdmin ? "vf-01-p0-semantic" : "reduced-skeleton"}
          data-role={role}
          data-testid="coverage-health-root"
        >
          <article
            className="coverage-health-summary"
            data-testid="coverage-health-context-summary"
          >
            <div>
              <p className="section-kicker">{isP0CoverageAdmin ? "CH-T02 / VF-01" : "CH-T01"}</p>
              <h2>{isP0CoverageAdmin ? "Coverage administration baseline" : "Resolved context health"}</h2>
              <p>
                Skeleton-only health slots derived from the current mock context. No runtime
                health endpoint or external source is queried.
              </p>
            </div>
            <dl className="coverage-health-facts" aria-label="Coverage health facts">
              <div>
                <dt>Coverage ceiling</dt>
                <dd data-testid="coverage-health-ceiling-value">{coverage}</dd>
              </div>
              <div>
                <dt>Effective visible</dt>
                <dd data-testid="coverage-health-effective-value">{effectiveVisibility}</dd>
              </div>
              <div>
                <dt>Case state</dt>
                <dd data-testid="coverage-health-case-state">{CASE_STATE_LABELS[activeCase.state]}</dd>
              </div>
              <div>
                <dt>Fixture freshness</dt>
                <dd data-testid="coverage-health-fixture-freshness">{activeCase.freshness}</dd>
              </div>
            </dl>
          </article>

          {isP0CoverageAdmin ? (
            <>
              <section
                aria-label="Coverage health key indicators"
                className="coverage-health-kpi-grid"
                data-testid="coverage-health-kpi-grid"
              >
                <article data-testid="current-coverage-level">
                  <span>Current coverage</span>
                  <strong>{coverage}</strong>
                  <p>Hard ceiling for visible fields.</p>
                </article>
                <article data-testid="field-presence-rate">
                  <span>Field presence</span>
                  <strong>{fieldPresenceRate}</strong>
                  <p>Derived only from existing field switch states.</p>
                </article>
                <article data-testid="join-health-rate">
                  <span>Join health</span>
                  <strong>Mock-only</strong>
                  <p>Live joins are not queried in this bounded frame.</p>
                </article>
                <article data-testid="data-freshness-indicator">
                  <span>Data freshness</span>
                  <strong>{activeCase.freshness}</strong>
                  <p>Fixture freshness only; no live telemetry.</p>
                </article>
              </section>

              <section
                aria-label="Coverage health diagnostic frame"
                className="coverage-health-diagnostic-grid"
              >
                <article data-testid="capability-tier-reference">
                  <span>Tier reference</span>
                  <strong>{`Current ${coverage} / effective ${effectiveVisibility}`}</strong>
                  <p>Coverage level remains a hard ceiling and does not unlock OFF fields.</p>
                </article>
                <article data-testid="field-switch-matrix">
                  <span>Field switch matrix</span>
                  <ul>
                    {fieldSwitchCounts.map((item) => (
                      <li data-switch-state={item.state} key={item.state}>
                        <strong>{item.state}</strong>
                        <span>{item.count}</span>
                      </li>
                    ))}
                  </ul>
                </article>
                <article data-testid="capability-package-list">
                  <span>Capability packages</span>
                  <p>
                    No frontend unlock package is created. Existing visibility fields are displayed
                    as read-only switch evidence.
                  </p>
                </article>
                <article
                  data-message-source="ui_messages"
                  data-testid="ui-message-preview"
                >
                  <span>UI message preview</span>
                  <ul>
                    {vf01NoticeCards.map((notice) => (
                      <li
                        data-message-source="ui_messages"
                        data-testid={notice.testId}
                        data-ui-message-key={notice.key}
                        key={notice.testId}
                      >
                        <strong>{notice.label}</strong>
                        <p>{formatUiMessageValue(notice.value ?? null)}</p>
                      </li>
                    ))}
                  </ul>
                </article>
              </section>
            </>
          ) : null}

          <section
            aria-label="Coverage health skeleton slots"
            className="coverage-health-slot-grid"
            data-testid="coverage-health-slot-grid"
          >
            <article
              data-field="case.coverage_level"
              data-health-slot="coverage-ceiling"
              data-testid="coverage-health-ceiling-slot"
            >
              <span>Coverage ceiling</span>
              <strong>{coverage}</strong>
              <p>Coverage level remains the hard ceiling. This slot does not unlock OFF fields.</p>
            </article>
            <article
              data-health-slot="ui-messages"
              data-message-count={availableCoverageHealthMessages.length}
              data-message-source="ui_messages"
              data-rendering-state={
                availableCoverageHealthMessages.length > 0 ? "bounded-rendered" : "unavailable"
              }
              data-testid="coverage-health-ui-message-slot"
            >
              <span>Signal message slot</span>
              <strong>{availableCoverageHealthMessages.length} governed slots</strong>
              {availableCoverageHealthMessages.length > 0 ? (
                <ul className="coverage-health-ui-messages" aria-label="Coverage health messages">
                  {availableCoverageHealthMessages.map((message) => (
                    <li
                      data-message-source="ui_messages"
                      data-testid="coverage-health-ui-message"
                      data-ui-message-key={message.key}
                      key={message.key}
                    >
                      <span>{message.key}</span>
                      <p>{formatUiMessageValue(message.value ?? null)}</p>
                    </li>
                  ))}
                </ul>
              ) : (
                <p
                  data-message-source="ui_messages"
                  data-rendering-state="unavailable"
                  data-testid="coverage-health-ui-message-unavailable"
                >
                  No governed ui_messages are available in the current mock context.
                </p>
              )}
            </article>
            <article
              data-health-slot="source-health"
              data-live-health-source="none"
              data-live-source-health="not-implemented"
              data-message-source="ui_messages"
              data-source-health-mode="ui_messages_semantic"
              data-source-health-display-state={
                sourceHealthMessages.length > 0 ? "semantic-placeholders" : "unavailable"
              }
              data-testid="coverage-health-source-slot"
            >
              <span>Source health</span>
              <strong>Governed semantic display</strong>
              {sourceHealthMessages.length > 0 ? (
                <ul
                  className="coverage-health-source-messages"
                  data-testid="coverage-health-source-message-list"
                >
                  {sourceHealthMessages.map((message) => (
                    <li
                      data-message-source="ui_messages"
                      data-source-health-display="semantic-placeholder"
                      data-source-health-display-state={message.displayState}
                      data-testid="coverage-health-source-message"
                      data-ui-message-key={message.key}
                      key={message.key}
                    >
                      <span>{message.label}</span>
                      <p>{formatUiMessageValue(message.value ?? null)}</p>
                    </li>
                  ))}
                </ul>
              ) : (
                <p
                  data-message-source="ui_messages"
                  data-source-health-display-state="unavailable"
                  data-testid="coverage-health-source-message-unavailable"
                >
                  Source-health display is unavailable because no governed ui_messages are present.
                </p>
              )}
              <p data-testid="coverage-health-source-boundary-note">
                Semantic display only. No sensor, endpoint, or external source is read.
              </p>
            </article>
            <article
              data-cross-surface-hardening="deferred"
              data-health-slot="regression"
              data-testid="coverage-health-regression-slot"
            >
              <span>Regression lane</span>
              <strong>Deferred</strong>
              <p>Cross-surface hardening remains a later Sprint 4 regression lane.</p>
            </article>
          </section>
        </div>
      )}
    </section>
  );
}

function CaseDetail({
  activeCase,
  followUp,
  onBack,
  onFollowUpChange,
  onFollowUpSubmit
}: {
  activeCase: WorkbenchCase;
  followUp: string;
  onBack: () => void;
  onFollowUpChange: (value: string) => void;
  onFollowUpSubmit: (event: FormEvent<HTMLFormElement>) => void;
}) {
  const [activeEvidenceFrameId, setActiveEvidenceFrameId] =
    useState<EvidenceFrameId>(activeCase.evidenceFrames[0]?.id ?? "process_evidence");
  const [evidenceMode, setEvidenceMode] = useState<EvidenceMode>("auto");
  const [activeSubordinatePanel, setActiveSubordinatePanel] =
    useState<SubordinatePanel>("evidence");
  const [isHonestyExpanded, setIsHonestyExpanded] = useState(true);
  const [isEvidencePinned, setIsEvidencePinned] = useState(false);
  const [isActionRequestDialogOpen, setIsActionRequestDialogOpen] = useState(false);
  const [hasLocalActionRequestSubmission, setHasLocalActionRequestSubmission] = useState(false);
  const actionRequestTriggerRef = useRef<HTMLButtonElement>(null);
  const actionRequestDialogRef = useRef<HTMLDivElement>(null);
  const actionRequestPrimaryButtonRef = useRef<HTMLButtonElement>(null);
  const actionRequestSubmittedStateRef = useRef<HTMLParagraphElement>(null);

  const narrativeSections = [
    {
      key: "WHAT",
      items: activeCase.narrative.what,
      evidenceFrameId: getFixtureSectionEvidence("WHAT", "event_timeline"),
      evidenceLabel: "Event Timeline"
    },
    {
      key: "WHY",
      items: activeCase.narrative.why,
      evidenceFrameId: getFixtureSectionEvidence("WHY", "lateral_topology"),
      evidenceLabel: "Topology / Blast Radius Preview"
    },
    {
      key: "INTENT",
      items: activeCase.narrative.intent,
      evidenceFrameId: getFixtureSectionEvidence("INTENT", "attack_lineage"),
      evidenceLabel: "Attack Chain / Lineage & Confidence"
    },
    {
      key: "HONESTY",
      items: activeCase.narrative.honesty,
      evidenceFrameId: getFixtureSectionEvidence("HONESTY", "attack_lineage"),
      evidenceLabel: "Attack Chain / Lineage & Confidence"
    },
    {
      key: "DECISION",
      items: activeCase.narrative.decision,
      evidenceFrameId: "process_evidence" as EvidenceFrameId,
      evidenceLabel: "Process / Execution Evidence"
    }
  ];
  const activeEvidenceFrame =
    activeCase.evidenceFrames.find((frame) => frame.id === activeEvidenceFrameId) ??
    activeCase.evidenceFrames[0];
  const canUseNarrativeEvidence = evidenceMode === "auto" && !isEvidencePinned;
  const canSubmitP1ActionRequest =
    activeCase.resolvedSurface === "P1_CASE_DETAIL" &&
    activeCase.resolvedRole === "P1" &&
    activeCase.arStatus === null &&
    !hasLocalActionRequestSubmission &&
    activeCase.state !== "CLOSED";
  const arStatusDisplay = getARStatusDisplay(activeCase.arStatus, activeCase.resolvedRole);
  const caseStateHeaderSkeleton = CASE_STATE_HEADER_SKELETON[activeCase.state] ?? null;
  const isClosedCase = activeCase.state === "CLOSED";
  const canRenderBlastRadiusPanel = activeCase.coverage !== "L1";
  const honestyLayerContentId = `${activeCase.id}-honesty-layer-content`;
  const unsupportedClaimSet = useMemo(
    () => new Set(activeCase.redline.unsupportedClaims),
    [activeCase.redline.unsupportedClaims]
  );

  useEffect(() => {
    if (!canRenderBlastRadiusPanel && activeSubordinatePanel === "blast_radius") {
      setActiveSubordinatePanel("evidence");
    }
  }, [activeSubordinatePanel, canRenderBlastRadiusPanel]);

  useEffect(() => {
    if (isActionRequestDialogOpen) {
      actionRequestPrimaryButtonRef.current?.focus();
    }
  }, [isActionRequestDialogOpen]);

  useEffect(() => {
    if (hasLocalActionRequestSubmission) {
      actionRequestSubmittedStateRef.current?.focus();
    }
  }, [hasLocalActionRequestSubmission]);

  function handleNarrativeEvidenceTrigger(frameId: EvidenceFrameId) {
    if (!canUseNarrativeEvidence) {
      return;
    }
    setActiveEvidenceFrameId(frameId);
  }

  function selectManualEvidenceFrame(frameId: EvidenceFrameId) {
    setActiveEvidenceFrameId(frameId);
    setEvidenceMode("manual");
  }

  function closeActionRequestDialog() {
    setIsActionRequestDialogOpen(false);
    window.setTimeout(() => actionRequestTriggerRef.current?.focus(), 0);
  }

  function submitLocalActionRequest() {
    setHasLocalActionRequestSubmission(true);
    setIsActionRequestDialogOpen(false);
  }

  function trapActionRequestDialogFocus(event: KeyboardEvent<HTMLDivElement>) {
    if (event.key === "Escape") {
      closeActionRequestDialog();
      return;
    }

    if (event.key !== "Tab") {
      return;
    }

    const focusableItems = Array.from(
      actionRequestDialogRef.current?.querySelectorAll<HTMLElement>(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      ) ?? []
    ).filter((item) => !item.hasAttribute("disabled"));

    if (focusableItems.length === 0) {
      event.preventDefault();
      return;
    }

    const firstItem = focusableItems[0];
    const lastItem = focusableItems[focusableItems.length - 1];

    if (event.shiftKey && document.activeElement === firstItem) {
      event.preventDefault();
      lastItem.focus();
      return;
    }

    if (!event.shiftKey && document.activeElement === lastItem) {
      event.preventDefault();
      firstItem.focus();
    }
  }

  return (
    <section
      className="page-region case-detail"
      aria-labelledby="case-title"
      data-testid="case-detail-surface"
    >
      <button className="back-button" onClick={onBack} type="button">
        <ArrowLeft aria-hidden="true" size={18} />
        <span>Inbox</span>
      </button>

      <div className="case-header" data-testid="case-header">
        <div>
          <p data-testid="case-header-case-id">{activeCase.id}</p>
          <h1 id="case-title">{activeCase.title}</h1>
          <dl className="case-header-facts" aria-label="Case header facts">
            <div>
              <dt>Verdict</dt>
              <dd data-testid="case-header-verdict">{activeCase.verdict}</dd>
            </div>
            <div>
              <dt>Coverage</dt>
              <dd data-testid="case-header-coverage">{activeCase.coverage}</dd>
            </div>
          </dl>
        </div>
        <div className="case-state-header-block">
          <span
            className="state-pill"
            data-case-state={activeCase.state}
            data-closed-behavior={isClosedCase ? "implemented" : "not-claimed"}
            data-testid="case-state-pill"
          >
            {CASE_STATE_LABELS[activeCase.state]}
          </span>
          {caseStateHeaderSkeleton ? (
            <aside
              aria-label="Case state header skeleton"
              className="case-state-header-skeleton"
              data-ar-status={activeCase.arStatus ?? "NONE"}
              data-authority-source="resolved-surface-context"
              data-case-state={activeCase.state}
              data-closed-behavior={isClosedCase ? "implemented" : "not-claimed"}
              data-lock-state={caseStateHeaderSkeleton.lockState}
              data-state-mutation="none"
              data-testid="case-state-header-skeleton"
              data-visual-frame={caseStateHeaderSkeleton.visualFrame}
              data-visual-state="semantic-skeleton"
            >
              <strong>{caseStateHeaderSkeleton.title}</strong>
              <span>{caseStateHeaderSkeleton.description}</span>
            </aside>
          ) : null}
        </div>
      </div>

      {isClosedCase ? (
        <aside
          aria-label="Closed case readonly banner"
          className="closed-case-banner"
          data-authority-source="CD-T06-renderable-context-checklist-v0.1"
          data-case-state="CLOSED"
          data-readonly-state="CLOSED"
          data-testid="closed-case-banner"
        >
          <span
            className="state-pill"
            data-case-state="CLOSED"
            data-testid="closed-state-pill"
          >
            Closed
          </span>
          <span
            className="closed-state-badge"
            data-close-reason="RESOLVED"
            data-testid="closed-state-badge"
          >
            Resolved / read-only
          </span>
          <p data-testid="closed-case-readonly-notice">
            This case is closed. Write controls are not attached; the dialogue dock remains
            visible for readonly review only.
          </p>
        </aside>
      ) : null}

      <div className="case-workspace" aria-label="Case detail workspace">
        <aside className="case-rail" aria-label="Case rail">
          <section className="rail-section" aria-labelledby="case-lifecycle-title">
            <p className="section-kicker">Region B1</p>
            <h2 id="case-lifecycle-title">Case Lifecycle</h2>
            <span className="state-pill rail-state">{CASE_STATE_LABELS[activeCase.state]}</span>
            <dl className="rail-facts">
              <div>
                <dt>Trigger source</dt>
                <dd>{activeCase.triggerSource}</dd>
              </div>
              <div>
                <dt>Coverage</dt>
                <dd>{activeCase.coverage}</dd>
              </div>
              <div>
                <dt>Freshness</dt>
                <dd>{activeCase.freshness}</dd>
              </div>
            </dl>
          </section>

          <section className="rail-section" aria-labelledby="processing-trace-title">
            <p className="section-kicker">Region B2</p>
            <h2 id="processing-trace-title">Processing Trace</h2>
            <ol className="trace-list">
              {activeCase.trace.map((item) => (
                <li key={`${activeCase.id}-${item.label}`}>
                  <span>{item.label}</span>
                  <p>{item.detail}</p>
                  <small>{item.provenance}</small>
                </li>
              ))}
            </ol>
          </section>

          <section
            className="rail-section"
            aria-labelledby="action-request-title"
            data-testid="action-request-panel"
          >
            <p className="section-kicker">Region B3</p>
            <h2 id="action-request-title">Action Request</h2>
            <div
              aria-label="Action request status mapping"
              className="ar-status-row"
              data-state-migration="none"
            >
              <span
                className={`ar-status-pill ${arStatusDisplay.tone}`}
                data-action-authority={arStatusDisplay.actionAuthority}
                data-ar-status={activeCase.arStatus ?? "NONE"}
                data-interaction-class={arStatusDisplay.interactionClass}
                data-mapping-source="D-02"
                data-state-migration={arStatusDisplay.stateMigration}
                data-testid="ar-status-pill"
              >
                {arStatusDisplay.label}
              </span>
              <span className="ar-status-source">D-02 display mapping only</span>
            </div>
            <p>{activeCase.actionRequest}</p>
            {isClosedCase ? (
              <div
                className="closed-action-area"
                data-readonly-state="CLOSED"
                data-state-mutation="none"
                data-testid="closed-action-area"
              >
                <strong>No write actions attached</strong>
                <span>New AR submission, approval controls, notes, close requests, and escalation are absent.</span>
              </div>
            ) : null}
            {canSubmitP1ActionRequest ? (
              <div
                aria-label="P1 escalation and close request entries"
                className="p1-request-entry-skeleton"
                data-action-mode="not-selected-by-p1"
                data-authority-source="resolved-surface-context"
                data-close-execution="not-implemented"
                data-testid="p1-escalation-close-request-skeleton"
                data-visual-state="skeleton"
                role="group"
              >
                <div className="p1-request-entry" data-entry-type="escalation_to_p2">
                  <strong>Escalation entry</strong>
                  <span data-testid="p1-escalation-reason-field">
                    Escalation reason: required before P2 review.
                  </span>
                  <span data-testid="p1-recommended-action-field">
                    Recommended action: optional P2 reference only.
                  </span>
                  <span data-testid="p1-urgency-text-field">
                    Urgency text: controlled copy, not ActionMode.
                  </span>
                </div>
                <div
                  className="p1-request-entry"
                  data-entry-state="skeleton-only"
                  data-testid="p1-close-request-entry"
                >
                  <strong>Close-request entry</strong>
                  <span>Skeleton only; no close execution is attached.</span>
                </div>
              </div>
            ) : null}
            {hasLocalActionRequestSubmission ? (
              <p
                className="action-request-status"
                data-testid="p1-action-request-submitted-state"
                ref={actionRequestSubmittedStateRef}
                tabIndex={-1}
              >
                Submitted to P2 review. Waiting on P2 in this mock-only UI state.
              </p>
            ) : null}
            {canSubmitP1ActionRequest ? (
              <div className="action-request-actions">
                <button
                  className="secondary-action"
                  onClick={() => setIsActionRequestDialogOpen(true)}
                  ref={actionRequestTriggerRef}
                  type="button"
                >
                  Request P2 review
                </button>
              </div>
            ) : null}
            {!canSubmitP1ActionRequest && !hasLocalActionRequestSubmission ? (
              <p className="action-request-readonly">Read-only for this mock phase.</p>
            ) : null}
          </section>

          {isClosedCase && activeCase.resolvedRole !== "P3" ? (
            <ClosedAuditTrail />
          ) : null}
        </aside>

        <section className="narrative-spine" aria-labelledby="narrative-title">
          <div
            className="summary-panel"
            aria-label="Case summary"
            data-summary-layer="summary_layer"
            data-testid="summary-layer"
          >
            <div className="summary-kicker">Narrative spine</div>
            <h2
              data-summary-field="summary_layer.verdict"
              data-testid="summary-layer-verdict"
              id="narrative-title"
            >
              {activeCase.verdict}
            </h2>
            <p data-summary-field="summary_layer.summary" data-testid="summary-layer-summary">
              {activeCase.summary}
            </p>
          </div>

          {activeCase.resolvedRole === "P3" ? (
            <P3ExecutiveSummary activeCase={activeCase} />
          ) : null}

          <RedlineRenderabilityPanel activeCase={activeCase} />

          <div className="spine-sections">
            {narrativeSections.map((section) => {
              const isHonestySection = section.key === "HONESTY";
              const persistentHonestyItems = isHonestySection
                ? section.items.filter((item) => unsupportedClaimSet.has(item))
                : [];
              const visibleItems =
                isHonestySection && !isHonestyExpanded
                  ? persistentHonestyItems.length > 0
                    ? persistentHonestyItems
                    : section.items
                  : section.items;
              const foldedItemCount = section.items.length - visibleItems.length;

              return (
                <article
                  className={isHonestySection ? "spine-section honesty-layer" : "spine-section"}
                  data-expanded={isHonestySection ? String(isHonestyExpanded) : undefined}
                  data-persistent={isHonestySection ? "true" : undefined}
                  data-testid={isHonestySection ? "honesty-layer" : undefined}
                  key={section.key}
                >
                  <div className="spine-section-header">
                    <h3>{section.key}</h3>
                    <div className="spine-section-actions">
                      {isHonestySection ? (
                        <button
                          aria-controls={honestyLayerContentId}
                          aria-expanded={isHonestyExpanded}
                          onClick={() => setIsHonestyExpanded((value) => !value)}
                          type="button"
                        >
                          {isHonestyExpanded ? "Fold honesty details" : "Expand honesty details"}
                        </button>
                      ) : null}
                      <button
                        aria-label={`${section.key} evidence anchor`}
                        aria-disabled={!canUseNarrativeEvidence}
                        onClick={() => handleNarrativeEvidenceTrigger(section.evidenceFrameId)}
                        onFocus={() => handleNarrativeEvidenceTrigger(section.evidenceFrameId)}
                        onMouseEnter={() => handleNarrativeEvidenceTrigger(section.evidenceFrameId)}
                        type="button"
                      >
                        Show evidence
                      </button>
                    </div>
                  </div>
                  <div id={isHonestySection ? honestyLayerContentId : undefined}>
                    {visibleItems.map((item) => (
                      <p
                        data-testid={
                          isHonestySection && unsupportedClaimSet.has(item)
                            ? "honesty-unsupported-claim"
                            : undefined
                        }
                        key={`${section.key}-${item}`}
                      >
                        {item}
                      </p>
                    ))}
                    {isHonestySection && !isHonestyExpanded && foldedItemCount > 0 ? (
                      <p className="honesty-fold-notice" data-testid="honesty-fold-notice">
                        Additional confidence and disproof details are folded; unsupported
                        claims remain visible.
                      </p>
                    ) : null}
                  </div>
                </article>
              );
            })}
          </div>
        </section>

        <aside
          className="evidence-panel"
          aria-labelledby="evidence-panel-title"
          data-testid="evidence-panel"
        >
          <p className="section-kicker">Region D</p>
          <h2 id="evidence-panel-title">Contextual Evidence</h2>
          <div
            aria-label="Subordinate panel selector"
            className="subordinate-panel-toggle"
            data-testid="subordinate-panel-selector"
            role="group"
          >
            <button
              aria-pressed={activeSubordinatePanel === "evidence"}
              onClick={() => setActiveSubordinatePanel("evidence")}
              type="button"
            >
              Evidence
            </button>
            <button
              aria-pressed={activeSubordinatePanel === "timeline"}
              onClick={() => setActiveSubordinatePanel("timeline")}
              type="button"
            >
              Timeline
            </button>
            {canRenderBlastRadiusPanel ? (
              <button
                aria-pressed={activeSubordinatePanel === "blast_radius"}
                onClick={() => setActiveSubordinatePanel("blast_radius")}
                type="button"
              >
                Blast Radius
              </button>
            ) : null}
          </div>
          {activeSubordinatePanel === "evidence" ? (
            <EvidenceSubordinatePanel
              activeEvidenceFrame={activeEvidenceFrame}
              activeEvidenceFrameId={activeEvidenceFrameId}
            evidenceFrames={activeCase.evidenceFrames}
            evidenceMode={evidenceMode}
            isEvidencePinned={isEvidencePinned}
            coverage={activeCase.coverage}
            onEvidenceModeChange={setEvidenceMode}
            onFrameSelect={selectManualEvidenceFrame}
            onPinnedChange={setIsEvidencePinned}
          />
          ) : null}
          {activeSubordinatePanel === "timeline" ? (
            <TimelineSubordinatePanel trace={activeCase.trace} />
          ) : null}
          {activeSubordinatePanel === "blast_radius" && canRenderBlastRadiusPanel ? (
            <BlastRadiusSubordinatePanel activeCase={activeCase} />
          ) : null}
        </aside>
      </div>

      <form
        aria-label="Case dialogue dock"
        className="follow-up-input dialogue-dock"
        data-dialogue-state={isClosedCase ? "readonly" : "active"}
        data-testid="dialogue-dock"
        onSubmit={onFollowUpSubmit}
      >
        <div className="dialogue-source-strip" data-testid="dialogue-source-boundary">
          <span>{`Case ${activeCase.id}`}</span>
          <span>{`Evidence ${activeEvidenceFrame.title}`}</span>
          <span
            data-suggestion-source="ui_messages"
            data-suggestion-state="unavailable"
            data-testid="dialogue-runtime-placeholder"
          >
            Runtime suggestions unavailable
          </span>
        </div>
        <div className="dialogue-input-row">
          <MessageSquareText aria-hidden="true" size={20} />
          <label className="sr-only" htmlFor="case-follow-up">
            Case follow-up input
          </label>
          {isClosedCase ? (
            <>
              <textarea
                data-testid="dialogue-input-readonly"
                disabled
                id="case-follow-up"
                readOnly
                value="Historical dialogue is read-only; sending is disabled."
              />
              <button
                aria-label="Submit case follow-up disabled"
                data-testid="dialogue-send-disabled"
                disabled
                type="submit"
              >
                <Send aria-hidden="true" size={18} />
              </button>
            </>
          ) : (
            <>
              <input
                id="case-follow-up"
                onChange={(event) => onFollowUpChange(event.target.value)}
                placeholder="Ask a follow-up in this case context"
                value={followUp}
              />
              <button aria-label="Submit case follow-up" type="submit">
                <Send aria-hidden="true" size={18} />
              </button>
            </>
          )}
        </div>
        {isClosedCase ? (
          <p
            className="closed-dialogue-notice"
            data-testid="closed-dialogue-notice"
          >
            Dialogue is retained for review, but the closed case cannot accept new writes.
          </p>
        ) : null}
      </form>

      {isActionRequestDialogOpen ? (
        <div className="action-request-dialog-backdrop" role="presentation">
          <div
            aria-describedby="action-request-dialog-description"
            aria-labelledby="action-request-dialog-title"
            aria-modal="true"
            className="action-request-dialog"
            onKeyDown={trapActionRequestDialogFocus}
            ref={actionRequestDialogRef}
            role="dialog"
          >
            <h2 id="action-request-dialog-title">Submit Action Request to P2</h2>
            <p id="action-request-dialog-description">
              This sends a mock-only request for P2 review. P1 does not choose execution mode
              or perform the later decision step.
            </p>
            <div
              className="action-request-field-grid"
              data-action-mode="not-selected-by-p1"
              data-testid="p1-action-request-modal-fields"
            >
              <div data-testid="p1-modal-escalation-reason">Escalation reason: required</div>
              <div data-testid="p1-modal-recommended-action">
                Recommended action: optional P2 reference only
              </div>
              <div data-testid="p1-modal-urgency-text">
                Urgency text: controlled copy, not ActionMode
              </div>
            </div>
            <div className="action-request-dialog-actions">
              <button
                onClick={submitLocalActionRequest}
                ref={actionRequestPrimaryButtonRef}
                type="button"
              >
                Submit to P2
              </button>
              <button onClick={closeActionRequestDialog} type="button">
                Cancel
              </button>
            </div>
          </div>
        </div>
      ) : null}
    </section>
  );
}

function ClosedAuditTrail() {
  return (
    <section
      aria-labelledby="closed-audit-trail-title"
      className="closed-audit-trail"
      data-audit-source="CD-T06-renderable-context-checklist-v0.1"
      data-readonly-state="CLOSED"
      data-testid="full-audit-trail"
    >
      <p className="section-kicker">CD-T06</p>
      <h2 id="closed-audit-trail-title">Closed audit trail</h2>
      <ol>
        {CD_T06_CLOSED_AUDIT_EVENTS.map((event) => (
          <li
            data-audit-id={event.id}
            data-testid={`audit-${event.id}`}
            key={event.id}
          >
            <strong>{event.id}</strong>
            <span>{event.label}</span>
            <p>{event.detail}</p>
          </li>
        ))}
      </ol>
    </section>
  );
}

function P3ExecutiveSummary({ activeCase }: { activeCase: WorkbenchCase }) {
  const unsupportedClaims = activeCase.honestyLayer.unsupportedClaims;
  const confidenceSignals = activeCase.honestyLayer.confidenceSignals;
  const disproofSignals = activeCase.honestyLayer.disproofSignals;

  return (
    <section
      aria-labelledby="p3-executive-summary-title"
      className="p3-executive-summary"
      data-approval-audit-summary="not-implemented"
      data-component-scope="cd-t05-case-detail-only"
      data-manager-handoff="not-implemented"
      data-role="P3"
      data-source-boundary="summary-honesty-unsupported-confidence-disproof"
      data-testid="p3-executive-summary"
    >
      <div className="p3-executive-summary-header">
        <div>
          <p className="section-kicker">P3 Executive Summary</p>
          <h2 id="p3-executive-summary-title">Independent executive summary</h2>
          <p
            data-summary-field="summary_layer.verdict"
            data-testid="p3-executive-summary-verdict"
          >
            {activeCase.verdict}
          </p>
          <p
            data-summary-field="summary_layer.summary"
            data-testid="p3-executive-summary-summary"
          >
            {activeCase.summary}
          </p>
        </div>
        <span
          className="p3-executive-summary-badge"
          data-summary-field="summary_layer.coverage_level"
          data-testid="p3-executive-summary-coverage"
        >
          {activeCase.coverage} ceiling
        </span>
      </div>

      <section
        aria-labelledby="p3-executive-summary-caution-title"
        className="p3-executive-summary-caution"
        data-source-field="honesty_layer.unsupported_claims"
        data-testid="p3-executive-summary-caution"
      >
        <h3 id="p3-executive-summary-caution-title">Management caution</h3>
        {unsupportedClaims.length > 0 ? (
          <ul>
            {unsupportedClaims.map((claim) => (
              <li data-testid="p3-executive-summary-unsupported-claim" key={claim}>
                {claim}
              </li>
            ))}
          </ul>
        ) : (
          <p data-state="unavailable">No unsupported-claims projection is supplied.</p>
        )}
        <p data-testid="p3-executive-summary-caution-copy">
          Management language remains cautious; this component does not claim complete control
          or complete elimination.
        </p>
      </section>

      <div className="p3-executive-summary-signal-grid">
        <article
          data-source-field="honesty_layer.what_would_raise_confidence"
          data-testid="p3-executive-summary-confidence"
        >
          <h3>Would raise confidence</h3>
          {confidenceSignals.length > 0 ? (
            <ul>
              {confidenceSignals.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          ) : (
            <p data-state="unavailable">No confidence-raising projection is supplied.</p>
          )}
        </article>
        <article
          data-source-field="honesty_layer.what_would_disprove_current_verdict"
          data-testid="p3-executive-summary-disproof"
        >
          <h3>Would disprove current verdict</h3>
          {disproofSignals.length > 0 ? (
            <ul>
              {disproofSignals.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          ) : (
            <p data-state="unavailable">No disproof projection is supplied.</p>
          )}
        </article>
      </div>

      <div
        className="p3-executive-summary-boundary"
        data-forbidden-sources="absent"
        data-testid="p3-executive-summary-boundary"
      >
        Raw technical evidence, approval controls, action controls, audit summary, and
        cross-page manager output are not mounted in CD-T05.
      </div>

      {activeCase.state === "CLOSED" ? (
        <section
          aria-labelledby="p3-approval-audit-summary-title"
          className="p3-approval-audit-summary"
          data-display-mode="read-only-manager-summary"
          data-full-audit-chain="not-rendered"
          data-role="P3"
          data-source="manager-history-summary"
          data-state-mutation="none"
          data-testid="p3-approval-audit-summary"
        >
          <div
            className="manager-summary-root"
            data-testid="manager-summary-root"
          >
            <h3 id="p3-approval-audit-summary-title">Closed approval audit summary</h3>
            <p>
              Manager review receives a cautious CLOSED summary only. The full P1/P2 audit
              trail, host raw evidence, and approval workbench controls are not mounted.
            </p>
          </div>
        </section>
      ) : null}
    </section>
  );
}

function EvidenceSubordinatePanel({
  activeEvidenceFrame,
  activeEvidenceFrameId,
  coverage,
  evidenceFrames,
  evidenceMode,
  isEvidencePinned,
  onEvidenceModeChange,
  onFrameSelect,
  onPinnedChange
}: {
  activeEvidenceFrame: WorkbenchCase["evidenceFrames"][number];
  activeEvidenceFrameId: EvidenceFrameId;
  coverage: CoverageLevel;
  evidenceFrames: WorkbenchCase["evidenceFrames"];
  evidenceMode: EvidenceMode;
  isEvidencePinned: boolean;
  onEvidenceModeChange: (mode: EvidenceMode) => void;
  onFrameSelect: (frameId: EvidenceFrameId) => void;
  onPinnedChange: (value: (current: boolean) => boolean) => void;
}) {
  return (
    <section
      aria-label="Evidence subordinate panel"
      className="subordinate-panel-body"
      data-testid="evidence-subordinate-panel"
    >
      <div className="evidence-toolbar" aria-label="Evidence panel controls">
        <div className="evidence-mode-toggle" aria-label="Evidence mode" role="group">
          <button
            aria-pressed={evidenceMode === "auto"}
            onClick={() => onEvidenceModeChange("auto")}
            type="button"
          >
            Auto
          </button>
          <button
            aria-pressed={evidenceMode === "manual"}
            onClick={() => onEvidenceModeChange("manual")}
            type="button"
          >
            Manual
          </button>
        </div>
        <button
          aria-pressed={isEvidencePinned}
          className="pin-button"
          onClick={() => onPinnedChange((current) => !current)}
          type="button"
        >
          {isEvidencePinned ? (
            <Unlock aria-hidden="true" size={15} />
          ) : (
            <Lock aria-hidden="true" size={15} />
          )}
          <span>{isEvidencePinned ? "Unpin" : "Pin"}</span>
        </button>
      </div>
      <p className="evidence-mode">
        Read-only frame summaries with Auto / Manual and Pin controls.
      </p>
      {coverage === "L1" ? (
        <div
          aria-label="L1 lineage confidence degraded summary"
          className="lineage-degradation-summary"
          data-coverage-level="L1"
          data-field="evidence_layer.lineage_confidence"
          data-lineage-card="simplified-summary"
          data-switch-state="DEGRADED"
          data-testid="l1-lineage-degradation-summary"
          data-vf-10-state="pending"
          role="note"
        >
          <strong>Lineage confidence</strong>
          <span data-testid="lineage-degradation-state">DEGRADED at coverage L1</span>
          <span data-testid="lineage-degradation-boundary">
            Simplified summary only; no full lineage card, graph, tool, node, or new fact.
          </span>
        </div>
      ) : null}
      <article
        className="active-evidence-frame"
        aria-live="polite"
        data-evidence-frame-id={activeEvidenceFrame.id}
        data-testid={
          activeEvidenceFrame.id === "technical_summary_fallback"
            ? "p3-technical-panel-fallback"
            : "active-evidence-frame"
        }
      >
        <div>
          <h3>{activeEvidenceFrame.title}</h3>
          <span>{activeEvidenceFrame.provenance}</span>
        </div>
        <p>{activeEvidenceFrame.summary}</p>
        {isEvidencePinned ? <small>Pinned evidence frame</small> : null}
      </article>
      <div className="evidence-frame-switcher" aria-label="Evidence frame switcher">
        {evidenceFrames.map((frame) => (
          <button
            aria-pressed={frame.id === activeEvidenceFrameId}
            key={frame.id}
            onClick={() => onFrameSelect(frame.id)}
            type="button"
          >
            <span>{frame.title}</span>
            <small>{frame.provenance}</small>
          </button>
        ))}
      </div>
    </section>
  );
}

function TimelineSubordinatePanel({ trace }: { trace: WorkbenchCase["trace"] }) {
  return (
    <section
      aria-label="Timeline subordinate panel"
      className="subordinate-panel-body timeline-subordinate-panel"
      data-testid="timeline-subordinate-panel"
    >
      <p className="evidence-mode">
        Read-only timeline assembled from existing mock trace and audit metadata.
      </p>
      <ol className="subordinate-timeline">
        {trace.map((item) => (
          <li key={`${item.provenance}-${item.label}`}>
            <span>{item.label}</span>
            <p>{item.detail}</p>
            <small>{item.provenance}</small>
          </li>
        ))}
      </ol>
      <div
        aria-label="Inferred timeline node weakening slot"
        className="inferred-node-weakening-slot"
        data-direct-evidence-node="false"
        data-evidence-weight="weakened"
        data-inferred-node="true"
        data-testid="inferred-node-weakening-slot"
        data-vf-10-state="pending"
        data-visual-state="skeleton"
        role="note"
      >
        <strong>Inferred timeline node</strong>
        <span data-testid="inferred-node-weight-label">
          Weakened slot only; lower weight than direct evidence.
        </span>
        <span data-testid="inferred-node-source-boundary">
          No graph, tool, node, or new fact is created in this mock UI.
        </span>
      </div>
    </section>
  );
}

function BlastRadiusSubordinatePanel({ activeCase }: { activeCase: WorkbenchCase }) {
  return (
    <section
      aria-label="Blast Radius subordinate panel"
      className="subordinate-panel-body blast-radius-subordinate-panel"
      data-testid="blast-radius-subordinate-panel"
    >
      <p className="evidence-mode">
        Mock-safe blast radius summary. Coverage remains the hard ceiling for visible detail.
      </p>
      <dl className="blast-radius-facts">
        <div>
          <dt>Coverage</dt>
          <dd>{activeCase.coverage}</dd>
        </div>
        <div>
          <dt>Visible detail</dt>
          <dd>Fixture-level topology summary only</dd>
        </div>
        <div>
          <dt>Authority</dt>
          <dd>Resolved surface context, not URL or storage</dd>
        </div>
      </dl>
    </section>
  );
}

function RedlineRenderabilityPanel({ activeCase }: { activeCase: WorkbenchCase }) {
  if (!activeCase.redlineFixtureId) {
    return null;
  }

  const {
    inline_warning: inlineWarning,
    missing_signal_notice: missingSignalNotice,
    resolver_degradation: resolverDegradation,
    concurrency_state: concurrencyState
  } = activeCase.redline.uiMessages;
  const blastRadiusState = activeCase.redline.visibilityFields.blast_radius;
  const shouldRenderManagerSummary =
    activeCase.resolvedRole === "P3" ||
    P3_MANAGER_SUMMARY_REDLINE_FIXTURE_IDS.has(activeCase.redlineFixtureId);

  return (
    <section
      aria-label="Mock redline renderability"
      className="summary-panel"
      data-testid="app-redline-renderability"
    >
      <div className="summary-kicker">Mock-only redline</div>
      <h3>{activeCase.redlineFixtureId}</h3>
      <p>
        Static, read-only renderability for existing validated fixture registry states. This
        panel is not a production route authority.
      </p>

      {missingSignalNotice ? (
        <p data-message-source="ui_messages" data-testid="missing-signal-notice">
          {missingSignalNotice}
        </p>
      ) : null}

      {inlineWarning || concurrencyState ? (
        <p
          aria-disabled="true"
          data-concurrency-state={String(concurrencyState ?? "inline-warning")}
          data-testid="concurrency-inline-warning"
        >
          {String(inlineWarning ?? concurrencyState)}
        </p>
      ) : null}

      {resolverDegradation ? (
        <p data-testid="resolver-degradation-notice">{resolverDegradation}</p>
      ) : null}

      {blastRadiusState === "OFF" ? (
        <p data-testid="blast-radius-redline" data-visibility-state="OFF">
          Blast radius remains OFF under the current coverage ceiling.
        </p>
      ) : null}

      {shouldRenderManagerSummary ? (
        <section data-testid="manager-summary">
          <h4>Manager summary</h4>
          <p>Manager summary stays cautious and read-only for this mock fixture.</p>
          {activeCase.redline.unsupportedClaims.length > 0 ? (
            <p>{`Unsupported claims remain: ${activeCase.redline.unsupportedClaims.join(" / ")}`}</p>
          ) : null}
        </section>
      ) : null}
    </section>
  );
}

export default App;
