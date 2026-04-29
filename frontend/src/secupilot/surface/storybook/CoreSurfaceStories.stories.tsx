import type { Meta, StoryObj } from "@storybook/react-vite";
import type { ReactNode } from "react";
import App from "../../../App";
import {
  CORE_SURFACE_FIXTURE_PHASE_OPTIONS,
  CoreSurfaceFixturePhaseOption
} from "../fixtures/coreSurfaceFixtureAdapter";
import { mockFixtureAdapter } from "../fixtures/mockFixtureAdapter";

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

function storyLabel(value: unknown) {
  if (Array.isArray(value)) {
    return value.join(" / ");
  }

  if (value === null || value === undefined) {
    return "none";
  }

  return String(value);
}

function RegistryFixtureCard({ fixtureId }: { fixtureId: string }) {
  const context = mockFixtureAdapter.getFixture(fixtureId);
  const expectedUi = context.ui_messages.expected_ui;
  const warning =
    context.ui_messages.inline_warning ??
    context.ui_messages.missing_signal_notice ??
    context.ui_messages.resolver_degradation ??
    context.ui_messages.mock_only_notice ??
    null;

  return (
    <article
      style={{
        border: "1px solid #d8dee8",
        borderRadius: 8,
        padding: 16,
        background: "#ffffff",
        minHeight: 190
      }}
    >
      <p style={{ margin: "0 0 8px", fontSize: 12, color: "#607086" }}>{fixtureId}</p>
      <h2 style={{ margin: "0 0 12px", fontSize: 18 }}>{context.ui_messages.phase_name ?? context.surface}</h2>
      <dl style={{ display: "grid", gap: 8, margin: 0 }}>
        <div>
          <dt style={{ color: "#607086", fontSize: 12 }}>authority</dt>
          <dd style={{ margin: 0 }}>
            {`${context.session.role} / ${context.surface} / coverage ${context.case.coverage_level}`}
          </dd>
        </div>
        <div>
          <dt style={{ color: "#607086", fontSize: 12 }}>case_state</dt>
          <dd style={{ margin: 0 }}>{context.case.case_state}</dd>
        </div>
        <div>
          <dt style={{ color: "#607086", fontSize: 12 }}>ar_status / action_mode</dt>
          <dd style={{ margin: 0 }}>
            {`${context.action_request?.ar_status ?? "AR none"} / ${context.action_request?.action_mode ?? "null"}`}
          </dd>
        </div>
        <div>
          <dt style={{ color: "#607086", fontSize: 12 }}>expected_ui</dt>
          <dd style={{ margin: 0 }}>{storyLabel(expectedUi)}</dd>
        </div>
        <div>
          <dt style={{ color: "#607086", fontSize: 12 }}>guardrail</dt>
          <dd style={{ margin: 0 }}>{storyLabel(warning)}</dd>
        </div>
      </dl>
    </article>
  );
}

function RegistrySection({ title, fixtureIds }: { title: string; fixtureIds: string[] }) {
  return (
    <section style={{ marginBottom: 28 }}>
      <h2 style={{ margin: "0 0 12px", fontSize: 20 }}>{title}</h2>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
          gap: 16
        }}
      >
        {fixtureIds.map((fixtureId) => (
          <RegistryFixtureCard key={fixtureId} fixtureId={fixtureId} />
        ))}
      </div>
    </section>
  );
}

function PoisonPillInventory() {
  const fixtureIds = mockFixtureAdapter.listPoisonPillFixtures();

  return (
    <section style={{ marginBottom: 28 }}>
      <h2 style={{ margin: "0 0 12px", fontSize: 20 }}>Fail-Closed Poison Pill Inventory</h2>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
          gap: 12
        }}
      >
        {fixtureIds.map((fixtureId) => (
          <article
            key={fixtureId}
            style={{
              border: "1px solid #d8dee8",
              borderRadius: 8,
              padding: 14,
              background: "#ffffff"
            }}
          >
            <p style={{ margin: "0 0 8px", fontSize: 12, color: "#607086" }}>not renderable</p>
            <h3 style={{ margin: 0, fontSize: 15 }}>{fixtureId}</h3>
            <p style={{ margin: "8px 0 0", color: "#4b5b72", fontSize: 13 }}>
              Expected validation: fail-closed SH-08. Storybook must not load this context.
            </p>
          </article>
        ))}
      </div>
    </section>
  );
}

function RegistryStoryShell({ children, title }: { children: ReactNode; title: string }) {
  resetStoryRoute("/fixture-registry");
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
      <section style={{ maxWidth: 1180, margin: "0 auto" }}>
        <p style={{ margin: "0 0 8px", color: "#607086" }}>
          Mock-only / validated fixture registry / Sprint 0
        </p>
        <h1 style={{ margin: "0 0 20px", fontSize: 28 }}>{title}</h1>
        {children}
      </section>
    </main>
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

export const APT12CPendingReviewRoute: Story = {
  name: "AP-T12C / Acceptance / P2 Pending Route",
  render: () => <StoryPhase phase={2} route="/approval" />
};

export const APT12CObservationWindowRoute: Story = {
  name: "AP-T12C / Acceptance / Observation Window Route",
  render: () => <StoryPhase phase={3} route="/approval" />
};

export const APT12CWindowExpiredRoute: Story = {
  name: "AP-T12C / Acceptance / Window Expired Route",
  render: () => <StoryPhase phase={4} route="/approval" />
};

export const APT12CTerminalLockRoute: Story = {
  name: "AP-T12C / Acceptance / Terminal Lock Route",
  render: () => <StoryPhase phase={5} route="/approval" />
};

export const P3ReadonlyReview: Story = {
  name: "P3 / Manager / Readonly Review",
  render: () => <StoryPhase phase={6} />
};

export const CrossSurfacePhaseOverview: Story = {
  name: "Walkthrough / Core Surface Phase Overview",
  render: () => <CrossSurfaceOverview />
};

export const FixtureRegistryValidatedPhases: Story = {
  name: "Registry / Validated Phase Fixtures",
  render: () => (
    <RegistryStoryShell title="Validated Phase Fixtures">
      <RegistrySection title="Phase Registry" fixtureIds={mockFixtureAdapter.listPhaseFixtures()} />
    </RegistryStoryShell>
  )
};

export const FixtureRegistryBoundaryCases: Story = {
  name: "Registry / Boundary Cases",
  render: () => (
    <RegistryStoryShell title="Boundary Case Fixtures">
      <RegistrySection title="Boundary Cases" fixtureIds={mockFixtureAdapter.listBoundaryFixtures()} />
    </RegistryStoryShell>
  )
};

export const FixtureRegistryResolverDegradation: Story = {
  name: "Registry / Resolver Degradation",
  render: () => (
    <RegistryStoryShell title="Resolver Degradation Fixtures">
      <RegistrySection
        title="Resolver Degradation"
        fixtureIds={mockFixtureAdapter.listResolverDegradationFixtures()}
      />
    </RegistryStoryShell>
  )
};

export const FixtureRegistryPoisonPillInventory: Story = {
  name: "Registry / Fail-Closed Poison Pill Inventory",
  render: () => (
    <RegistryStoryShell title="Fail-Closed Poison Pill Inventory">
      <PoisonPillInventory />
    </RegistryStoryShell>
  )
};

export const FixtureRegistryNegativeBoundaryOverview: Story = {
  name: "Registry / Negative Boundary Overview",
  render: () => (
    <RegistryStoryShell title="Negative And Boundary Fixture Overview">
      <RegistrySection title="Boundary Cases" fixtureIds={mockFixtureAdapter.listBoundaryFixtures()} />
      <RegistrySection
        title="Resolver Degradation"
        fixtureIds={mockFixtureAdapter.listResolverDegradationFixtures()}
      />
      <PoisonPillInventory />
    </RegistryStoryShell>
  )
};
