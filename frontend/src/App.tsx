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
}

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
    state: "UNDER_INVESTIGATION"
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
    state: "PENDING_APPROVAL"
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
        <span className="state-pill">{activeCase.state.replaceAll("_", " ")}</span>
      </div>

      <section className="summary-panel" aria-label="Case summary">
        <div className="summary-kicker">Summary</div>
        <h2>{activeCase.verdict}</h2>
        <p>{activeCase.summary}</p>
      </section>

      <form className="follow-up-input" onSubmit={onFollowUpSubmit}>
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
