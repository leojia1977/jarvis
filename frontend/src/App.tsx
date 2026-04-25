import {
  ArrowLeft,
  ChevronRight,
  History,
  Inbox,
  MessageSquareText,
  Search,
  Send,
  ShieldCheck
} from "lucide-react";
import { FormEvent, useMemo, useState } from "react";

type Role = "P0" | "P1" | "P2" | "P3";
type Route = "inbox" | "case";
type CoverageLevel = "L0" | "L1" | "L2" | "L3";

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
  state: "UNDER_INVESTIGATION" | "PENDING_APPROVAL";
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
    title: string;
    provenance: string;
    summary: string;
  }>;
}

const CASE_STATE_LABELS: Record<WorkbenchCase["state"], string> = {
  UNDER_INVESTIGATION: "Under investigation",
  PENDING_APPROVAL: "Pending P2 review"
};

const CASES: WorkbenchCase[] = [
  {
    id: "CASE-001",
    title: "Suspicious lateral movement on WKST-047",
    verdict: "Critical action required",
    risk: "Critical",
    coverage: "L2",
    nextStep: "Review summary and decide escalation",
    summary:
      "Multiple correlated process and identity signals indicate likely lateral movement. Evidence detail remains inside the case context.",
    state: "UNDER_INVESTIGATION",
    triggerSource: "Identity + EDR correlation",
    freshness: "Signals refreshed 4 min ago",
    actionRequest: "No pending request. P1 can prepare a request for P2 after review.",
    trace: [
      {
        label: "Triggered",
        detail: "Privilege change and remote service activity entered the case queue.",
        provenance: "Case signal"
      },
      {
        label: "Enriched",
        detail: "Host, identity, and nearby execution context were attached.",
        provenance: "Context layer"
      },
      {
        label: "Processing complete",
        detail: "Engine trace is available as provenance, not as lifecycle state.",
        provenance: "T1 / T3 / T5"
      }
    ],
    narrative: {
      what: [
        "WKST-047 started remote service activity after a privileged session changed hands.",
        "The case combines process execution, identity movement, and host context into one investigation object."
      ],
      why: [
        "The signals form a plausible lateral-movement path rather than a single isolated process event.",
        "Coverage is L2, so the page shows an impact preview without presenting it as a complete L3 topology."
      ],
      intent: [
        "The most likely operator intent is to establish execution reach on a neighboring system.",
        "The immediate concern is whether the same credential path appears on adjacent hosts."
      ],
      honesty: [
        "Unsupported claim: business impact is estimated from the available host context and is not confirmed by an owner.",
        "Confidence would rise if process ancestry and peer-host freshness are confirmed.",
        "Current coverage does not prove a full blast-radius chain."
      ],
      decision: [
        "P1 should read the evidence, add an investigation note if needed, and submit a request to P2 only if the escalation remains justified.",
        "No approval or final execution-mode decision belongs on this P1 surface."
      ]
    },
    evidenceFrames: [
      {
        title: "Process / Execution Evidence",
        provenance: "T3",
        summary: "Remote-service creation and child process signals are present; inferred links stay visually secondary."
      },
      {
        title: "Topology / Blast Radius Preview",
        provenance: "L2 preview",
        summary: "Neighboring host exposure is shown as a bounded preview, not as full advanced topology."
      },
      {
        title: "Event Timeline",
        provenance: "T1",
        summary: "Timeline anchors are ordered around the privileged session and remote activity window."
      },
      {
        title: "Attack Chain / Lineage & Confidence",
        provenance: "T5",
        summary: "Lineage confidence is sufficient for review, with unsupported claims kept visible."
      }
    ]
  },
  {
    id: "CASE-002",
    title: "Privileged script execution on DB-02",
    verdict: "High confidence investigation",
    risk: "High",
    coverage: "L1",
    nextStep: "Ask a follow-up before action request",
    summary:
      "A privileged script was observed during the current window. Lower coverage keeps deeper lineage out of the default view.",
    state: "PENDING_APPROVAL",
    triggerSource: "Script execution monitor",
    freshness: "Signals refreshed 11 min ago",
    actionRequest: "Request submitted to P2. P1 view remains read-only for approval outcome.",
    trace: [
      {
        label: "Triggered",
        detail: "Privileged script execution opened a case for review.",
        provenance: "Case signal"
      },
      {
        label: "Enriched",
        detail: "Coverage remains limited while identity context is still thin.",
        provenance: "Context layer"
      },
      {
        label: "Submitted",
        detail: "The case is waiting for P2 review; this is not a P1 approval surface.",
        provenance: "Case lifecycle"
      }
    ],
    narrative: {
      what: [
        "DB-02 ran a privileged script inside the current observation window.",
        "The case keeps the script event, host identity, and available context together for P1 review."
      ],
      why: [
        "The behavior is sensitive because it occurred on a database host with elevated privileges.",
        "Coverage is L1, so the page avoids presenting deeper lineage as known fact."
      ],
      intent: [
        "The available signal supports a cautious investigation posture, not a confident attribution.",
        "The next likely question is whether the script was expected maintenance or unauthorized execution."
      ],
      honesty: [
        "Unsupported claim: lateral movement is not established from the current L1 evidence.",
        "Confidence would rise if scheduled-change records and process ancestry are attached.",
        "Current coverage does not unlock a detailed lineage narrative."
      ],
      decision: [
        "P1 should keep the case context available and use the follow-up input for missing maintenance context.",
        "The submitted request waits for P2 review; P1 does not approve or reject it here."
      ]
    },
    evidenceFrames: [
      {
        title: "Process / Execution Evidence",
        provenance: "T3",
        summary: "The script execution is visible, while lower-confidence ancestry stays de-emphasized."
      },
      {
        title: "Topology / Blast Radius Preview",
        provenance: "L1 limited",
        summary: "No broad topology is shown because coverage is below the L2 baseline for this frame."
      },
      {
        title: "Event Timeline",
        provenance: "T1",
        summary: "The visible timeline centers on the script event and current case submission."
      },
      {
        title: "Attack Chain / Lineage & Confidence",
        provenance: "Limited",
        summary: "Lineage is intentionally constrained until stronger supporting evidence exists."
      }
    ]
  }
];

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

function App() {
  const [{ route, caseId }, setLocation] = useState(initialRoute);
  const [role, setRole] = useState<Role>("P1");
  const [globalQuery, setGlobalQuery] = useState("");
  const [followUp, setFollowUp] = useState("");

  const activeCase = useMemo(
    () => CASES.find((item) => item.id === caseId) ?? CASES[0],
    [caseId]
  );
  const navItems = NAV_ITEMS.filter((item) => item.roles.includes(role));

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
          {(["P0", "P1", "P2", "P3"] as Role[]).map((item) => (
            <button
              className={item === role ? "role active" : "role"}
              key={item}
              onClick={() => setRole(item)}
              type="button"
            >
              {item}
            </button>
          ))}
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

          <div className="coverage-badge" aria-label="Coverage level">
            <span className="coverage-dot" />
            <span>Coverage {activeCase.coverage}</span>
          </div>
        </header>

        {route === "case" ? (
          <CaseDetail
            activeCase={activeCase}
            followUp={followUp}
            onBack={() => navigate("inbox")}
            onFollowUpChange={setFollowUp}
            onFollowUpSubmit={submitFollowUp}
          />
        ) : (
          <InboxView cases={CASES} onOpenCase={(nextCaseId) => navigate("case", nextCaseId)} />
        )}
      </section>
    </main>
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
  const narrativeSections = [
    { key: "WHAT", items: activeCase.narrative.what },
    { key: "WHY", items: activeCase.narrative.why },
    { key: "INTENT", items: activeCase.narrative.intent },
    { key: "HONESTY", items: activeCase.narrative.honesty },
    { key: "DECISION", items: activeCase.narrative.decision }
  ];

  return (
    <section className="page-region case-detail" aria-labelledby="case-title">
      <button className="back-button" onClick={onBack} type="button">
        <ArrowLeft aria-hidden="true" size={18} />
        <span>Inbox</span>
      </button>

      <div className="case-header">
        <div>
          <p>{activeCase.id}</p>
          <h1 id="case-title">{activeCase.title}</h1>
        </div>
        <span className="state-pill">{CASE_STATE_LABELS[activeCase.state]}</span>
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

          <section className="rail-section" aria-labelledby="action-request-title">
            <p className="section-kicker">Region B3</p>
            <h2 id="action-request-title">Action Request</h2>
            <p>{activeCase.actionRequest}</p>
          </section>
        </aside>

        <section className="narrative-spine" aria-labelledby="narrative-title">
          <div className="summary-panel" aria-label="Case summary">
            <div className="summary-kicker">Narrative spine</div>
            <h2 id="narrative-title">{activeCase.verdict}</h2>
            <p>{activeCase.summary}</p>
          </div>

          <div className="spine-sections">
            {narrativeSections.map((section) => (
              <article className="spine-section" key={section.key}>
                <h3>{section.key}</h3>
                {section.items.map((item, index) => (
                  <p key={`${section.key}-${index}`}>{item}</p>
                ))}
              </article>
            ))}
          </div>
        </section>

        <aside className="evidence-panel" aria-labelledby="evidence-panel-title">
          <p className="section-kicker">Region D</p>
          <h2 id="evidence-panel-title">Contextual Evidence</h2>
          <p className="evidence-mode">Read-only frame summaries for this ticket</p>
          <div className="evidence-frame-list">
            {activeCase.evidenceFrames.map((frame) => (
              <article className="evidence-frame" key={frame.title}>
                <div>
                  <h3>{frame.title}</h3>
                  <span>{frame.provenance}</span>
                </div>
                <p>{frame.summary}</p>
              </article>
            ))}
          </div>
        </aside>
      </div>

      <form className="follow-up-input dialogue-dock" onSubmit={onFollowUpSubmit}>
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
      </form>
    </section>
  );
}

export default App;
