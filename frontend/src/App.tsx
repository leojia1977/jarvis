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

type Route = "inbox" | "case";
type EvidenceFrameId =
  | "process_evidence"
  | "lateral_topology"
  | "event_timeline"
  | "attack_lineage";
type EvidenceMode = "auto" | "manual";
type NarrativeKey = "WHAT" | "WHY" | "INTENT" | "HONESTY" | "DECISION";

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
  "attack_lineage"
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
  return FIXTURE.evidence_panels
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
    activeInSlice: false
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
  return { route: "inbox", caseId: null };
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
    const path = nextRoute === "case" && nextCaseId ? `/case/${nextCaseId}` : "/inbox";
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
            const isActive = item.routeKey === route || (item.routeKey === "inbox" && route === "case");
            return (
              <button
                aria-disabled={!item.activeInSlice}
                className={isActive ? "nav-item active" : "nav-item"}
                key={item.routeKey}
                onClick={() => item.activeInSlice && navigate("inbox")}
                type="button"
              >
                <Icon aria-hidden="true" size={18} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
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
        ) : (
          <InboxView cases={cases} onOpenCase={(nextCaseId) => navigate("case", nextCaseId)} />
        )}
      </section>
    </main>
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
  onOpenCase
}: {
  cases: WorkbenchCase[];
  onOpenCase: (caseId: string) => void;
}) {
  return (
    <section className="page-region" aria-labelledby="inbox-title">
      <div className="page-heading">
        <p>Case Inbox</p>
        <h1 id="inbox-title">Current case queue</h1>
      </div>

      <div className="case-grid">
        {cases.map((item) => (
          <article className="case-card" key={item.id}>
            <div className="case-card-topline">
              <span className={`risk ${item.risk.toLowerCase()}`}>{item.risk}</span>
              <span>{item.coverage}</span>
            </div>
            <h2>{item.title}</h2>
            <p>{item.verdict}</p>
            <div className="next-step">{item.nextStep}</div>
            <button onClick={() => onOpenCase(item.id)} type="button">
              <span>Open case</span>
              <ChevronRight aria-hidden="true" size={18} />
            </button>
          </article>
        ))}
      </div>
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

      <div className="case-header">
        <div>
          <p>{activeCase.id}</p>
          <h1 id="case-title">{activeCase.title}</h1>
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
          <div className="summary-panel" aria-label="Case summary">
            <div className="summary-kicker">Narrative spine</div>
            <h2 id="narrative-title">{activeCase.verdict}</h2>
            <p>{activeCase.summary}</p>
          </div>

          <RedlineRenderabilityPanel activeCase={activeCase} />

          <div className="spine-sections">
            {narrativeSections.map((section) => (
              <article className="spine-section" key={section.key}>
                <div className="spine-section-header">
                  <h3>{section.key}</h3>
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
                {section.items.map((item, index) => (
                  <p key={`${section.key}-${index}`}>{item}</p>
                ))}
              </article>
            ))}
          </div>
        </section>

        <aside
          className="evidence-panel"
          aria-labelledby="evidence-panel-title"
          data-testid="evidence-panel"
        >
          <p className="section-kicker">Region D</p>
          <h2 id="evidence-panel-title">Contextual Evidence</h2>
          <div className="evidence-toolbar" aria-label="Evidence panel controls">
            <div className="evidence-mode-toggle" aria-label="Evidence mode" role="group">
              <button
                aria-pressed={evidenceMode === "auto"}
                onClick={() => setEvidenceMode("auto")}
                type="button"
              >
                Auto
              </button>
              <button
                aria-pressed={evidenceMode === "manual"}
                onClick={() => setEvidenceMode("manual")}
                type="button"
              >
                Manual
              </button>
            </div>
            <button
              aria-pressed={isEvidencePinned}
              className="pin-button"
              onClick={() => setIsEvidencePinned((current) => !current)}
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
          <article className="active-evidence-frame" aria-live="polite">
            <div>
              <h3>{activeEvidenceFrame.title}</h3>
              <span>{activeEvidenceFrame.provenance}</span>
            </div>
            <p>{activeEvidenceFrame.summary}</p>
            {isEvidencePinned ? <small>Pinned evidence frame</small> : null}
          </article>
          <div className="evidence-frame-switcher" aria-label="Evidence frame switcher">
            {activeCase.evidenceFrames.map((frame) => (
              <button
                aria-pressed={frame.id === activeEvidenceFrameId}
                key={frame.id}
                onClick={() => selectManualEvidenceFrame(frame.id)}
                type="button"
              >
                <span>{frame.title}</span>
                <small>{frame.provenance}</small>
              </button>
            ))}
          </div>
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
