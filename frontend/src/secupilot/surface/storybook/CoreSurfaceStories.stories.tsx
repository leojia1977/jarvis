import type { Meta, StoryObj } from "@storybook/react-vite";
import App from "../../../App";
import {
  CORE_SURFACE_FIXTURE_PHASE_OPTIONS,
  CoreSurfaceFixturePhaseOption
} from "../fixtures/coreSurfaceFixtureAdapter";

function resetStoryRoute(path = "/case/CASE-2847") {
  if (typeof window !== "undefined") {
    window.history.replaceState({}, "", path);
  }
}

function StoryPhase({ phase, route = "/case/CASE-2847" }: { phase: number; route?: string }) {
  resetStoryRoute(route);
  return <App initialPhaseNumber={phase} />;
}

function PhaseCard({ phase }: { phase: CoreSurfaceFixturePhaseOption }) {
  return (
    <article
      style={{
        border: "1px solid #d8dee8",
        borderRadius: 8,
        padding: 16,
        background: "#ffffff",
        minHeight: 168
      }}
    >
      <p style={{ margin: "0 0 8px", fontSize: 12, color: "#607086" }}>
        {`Phase ${phase.phase} - ${phase.role} - ${phase.surface}`}
      </p>
      <h2 style={{ margin: "0 0 12px", fontSize: 18 }}>{phase.name}</h2>
      <dl style={{ display: "grid", gap: 8, margin: 0 }}>
        <div>
          <dt style={{ color: "#607086", fontSize: 12 }}>case_state</dt>
          <dd style={{ margin: 0 }}>{phase.caseState}</dd>
        </div>
        <div>
          <dt style={{ color: "#607086", fontSize: 12 }}>ar_status</dt>
          <dd style={{ margin: 0 }}>{phase.arStatus ?? "AR none"}</dd>
        </div>
        <div>
          <dt style={{ color: "#607086", fontSize: 12 }}>action_mode</dt>
          <dd style={{ margin: 0 }}>{phase.actionMode ?? "null"}</dd>
        </div>
      </dl>
    </article>
  );
}

function CrossSurfaceOverview() {
  resetStoryRoute("/inbox");
  return (
    <main
      style={{
        minHeight: "100vh",
        padding: 24,
        background: "#f6f8fb",
        color: "#172033",
        fontFamily:
          "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
      }}
    >
      <section style={{ maxWidth: 1120, margin: "0 auto" }}>
        <p style={{ margin: "0 0 8px", color: "#607086" }}>CASE-2847 / AR-2847-ISO-001</p>
        <h1 style={{ margin: "0 0 20px", fontSize: 28 }}>Core Surface Phase Walkthrough</h1>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
            gap: 16
          }}
        >
          {CORE_SURFACE_FIXTURE_PHASE_OPTIONS.map((phase) => (
            <PhaseCard key={phase.phase} phase={phase} />
          ))}
        </div>
      </section>
    </main>
  );
}

const meta = {
  title: "SecuPilot/Core Surface Stories",
  component: App,
  parameters: {
    layout: "fullscreen"
  }
} satisfies Meta<typeof App>;

export default meta;

type Story = StoryObj<typeof meta>;

export const P1InitialInvestigation: Story = {
  name: "P1 / Case Detail / Initial Investigation",
  render: () => <StoryPhase phase={0} />
};

export const P1WaitingOnP2: Story = {
  name: "P1 / Case Detail / Waiting On P2",
  render: () => <StoryPhase phase={1} />
};

export const P2PendingReview: Story = {
  name: "P2 / Approval / Pending Review",
  render: () => <StoryPhase phase={2} />
};

export const P2ObservationWindowActive: Story = {
  name: "P2 / Approval / Observation Window Active",
  render: () => <StoryPhase phase={3} />
};

export const P2WindowExpiredReturnPending: Story = {
  name: "P2 / Approval / Window Expired Return Pending",
  render: () => <StoryPhase phase={4} />
};

export const P2TerminalLock: Story = {
  name: "P2 / Approval / Terminal Lock",
  render: () => <StoryPhase phase={5} />
};

export const P3ReadonlyReview: Story = {
  name: "P3 / Manager / Readonly Review",
  render: () => <StoryPhase phase={6} />
};

export const CrossSurfacePhaseOverview: Story = {
  name: "Walkthrough / Core Surface Phase Overview",
  render: () => <CrossSurfaceOverview />
};
