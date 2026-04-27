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
  CaseState,
  CoverageLevel,
  ResolvedSurfaceContext,
  Role,
  SwitchState
} from "./secupilot/surface/context/types";

type Route = "inbox" | "case" | "search";
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
  arStatus: string | null;
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
    routeKey: "approval_queue",
    roles: ["P2"],
    icon: ShieldCheck,
    activeInSlice: false
  },
  {
    label: "Coverage & Health",
    routeKey: "coverage_health",
    roles: ["P0", "P2"],
    icon: ShieldCheck,
    activeInSlice: false
  },
  {
    label: "Manager View",
    routeKey: "manager_view",
    roles: ["P3"],
    icon: ShieldCheck,
    activeInSlice: false
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
  return { route: "inbox", caseId: null };
}

function isCoverageLevel(value: string | null): value is CoverageLevel {
  return value === "L0" || value === "L1" || value === "L2" || value === "L3";
}

function isSearchFocusScope(value: string | null): value is SearchFocusScope {
  return value === "summary" || value === "approval_audit" || value === "history_audit";
}

function clampCoverageRequest(
  requestedCoverage: CoverageLevel | null,
  recordedCoverage: CoverageLevel
): CoverageLevel {
  if (!requestedCoverage) {
    return recordedCoverage;
  }
  const ranks: Record<CoverageLevel, number> = { L0: 0, L1: 1, L2: 2, L3: 3 };
  return ranks[requestedCoverage] > ranks[recordedCoverage]
    ? recordedCoverage
    : requestedCoverage;
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
}

function App({ initialPhaseNumber = FIXTURE_PHASES[0]?.phase ?? 0 }: AppProps = {}) {
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
        : nextRoute === "search"
          ? "/search?tab=history"
          : "/inbox";
    window.history.pushState({}, "", path);
    setLocation({ route: nextRoute, caseId: nextCaseId ?? null });
  }

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
            const isActive =
              item.routeKey === route ||
              (item.routeKey === "inbox" && route === "case") ||
              (isSearchRoute && route === "search");
            return (
              <button
                aria-disabled={!item.activeInSlice}
                className={isActive ? "nav-item active" : "nav-item"}
                key={item.routeKey}
                onClick={() => item.activeInSlice && navigate(isSearchRoute ? "search" : "inbox")}
                type="button"
              >
                <Icon aria-hidden="true" size={18} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        <ExpertModeEntrySlot
          caseState={activeCase.state}
          coverage={activeCase.coverage}
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
            <span>Coverage {activeCase.coverage}</span>
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
            activeCase={activeCase}
            followUp={followUp}
            key={`${activeCase.id}-${activeCase.phaseNumber}`}
            onBack={() => navigate("inbox")}
            onFollowUpChange={setFollowUp}
            onFollowUpSubmit={submitFollowUp}
          />
        ) : route === "search" ? (
          <SearchHistoryView activeCase={activeCase} activeContext={activeContext} />
        ) : (
          <InboxView
            cases={cases}
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
  onOpenCase,
  role
}: {
  cases: WorkbenchCase[];
  onOpenCase: (caseId: string) => void;
  role: Role;
}) {
  const isP3Readonly = role === "P3";

  return (
    <section
      className="page-region"
      aria-labelledby="inbox-title"
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
  activeContext
}: {
  activeCase: WorkbenchCase;
  activeContext: ResolvedSurfaceContext;
}) {
  const queryParams = new URLSearchParams(window.location.search);
  const requestedCoverageParam = queryParams.get("coverage");
  const requestedCoverage = isCoverageLevel(requestedCoverageParam)
    ? requestedCoverageParam
    : null;
  const requestedFocusParam = queryParams.get("focus");
  const effectiveFocus = isSearchFocusScope(requestedFocusParam) ? requestedFocusParam : "summary";
  const recordedCoverage = activeContext.case.coverage_level;
  const effectiveCoverage = clampCoverageRequest(requestedCoverage, recordedCoverage);

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

      <article
        className="history-case-row historical-case-list-item"
        data-current-visible={effectiveCoverage}
        data-detail-context-authority="case-route"
        data-effective-visibility-owned-by="case-detail"
        data-frame-state="hf-sh-01-vf-08-pending"
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
    !hasLocalActionRequestSubmission;
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
        <span className="state-pill" data-testid="case-state-pill">
          {CASE_STATE_LABELS[activeCase.state]}
        </span>
      </div>

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
            <p>{activeCase.actionRequest}</p>
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
          <input
            id="case-follow-up"
            onChange={(event) => onFollowUpChange(event.target.value)}
            placeholder="Ask a follow-up in this case context"
            value={followUp}
          />
          <button aria-label="Submit case follow-up" type="submit">
            <Send aria-hidden="true" size={18} />
          </button>
        </div>
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
