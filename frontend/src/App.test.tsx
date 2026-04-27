import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import coreSurfaceFixture from "../fixtures/secupilot_core_surface_fixture_v0_1.json";
import App from "./App";

function panelTitle(panelId: string) {
  return (
    coreSurfaceFixture.evidence_panels.find((panel) => panel.panel_id === panelId)
      ?.standard_title ?? panelId
  );
}

function firstSectionEvidenceRef(sectionKey: string, fallback: string) {
  return (
    coreSurfaceFixture.case.narrative_sections.find((section) => section.section === sectionKey)
      ?.sentences[0]?.evidence_panel_ref ?? fallback
  );
}

describe("SecuPilot first-batch workbench slice", () => {
  beforeEach(() => {
    window.history.pushState({}, "", "/inbox");
    window.localStorage.clear();
    window.sessionStorage.clear();
  });

  it("renders the global conversation input and coverage badge", () => {
    render(<App />);

    expect(screen.getByLabelText("Global conversation input")).toBeInTheDocument();
    expect(screen.getByLabelText("Coverage level")).toHaveTextContent("Coverage L2");
  });

  it("crops P1 navigation without disabled forbidden links", () => {
    render(<App />);

    expect(screen.getByRole("button", { name: /Inbox/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Search \/ History/i })).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /Approval Queue/i })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /Coverage & Health/i })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /Manager View/i })).not.toBeInTheDocument();
  });

  it("updates visible navigation when role changes", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(screen.getByRole("button", { name: "P2" }));

    expect(screen.getByRole("button", { name: /Approval Queue/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Coverage & Health/i })).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /Manager View/i })).not.toBeInTheDocument();
  });

  it("opens a case from Inbox into the case-first detail route", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(screen.getAllByRole("button", { name: /Open case/i })[0]);

    expect(window.location.pathname).toBe("/case/CASE-2847");
    expect(screen.getByText("CASE-2847")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: /HIGH mock case/i })).toBeInTheDocument();
  });

  it("renders the P1 Case Detail layout regions and narrative spine", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(screen.getAllByRole("button", { name: /Open case/i })[0]);

    expect(screen.getByRole("heading", { name: "Case Lifecycle" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Processing Trace" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Action Request" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "WHAT" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "WHY" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "INTENT" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "HONESTY" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "DECISION" })).toBeInTheDocument();
    expect(
      screen.getByText(coreSurfaceFixture.case.honesty_layer.unsupported_claims[0])
    ).toBeInTheDocument();
    expect(screen.getByText(/Read-only frame summaries/i)).toBeInTheDocument();
    expect(screen.getByLabelText("Case follow-up input")).toBeInTheDocument();
    const evidencePanel = screen.getByRole("complementary", { name: "Contextual Evidence" });
    expect(within(evidencePanel).queryByRole("textbox")).not.toBeInTheDocument();
    expect(document.body).not.toHaveTextContent(/IMMEDIATE|DELAYED|OBSERVE_ONLY/);
  });

  it("loads the core fixture and exposes a mock-only phase selector", async () => {
    const user = userEvent.setup();
    render(<App />);

    const phaseSelector = screen.getByLabelText("Mock fixture phase") as HTMLSelectElement;
    const resolvedContext = screen.getByLabelText("Mock fixture resolved context");

    expect(phaseSelector.options).toHaveLength(7);
    expect(resolvedContext).toHaveTextContent("Role P1");
    expect(resolvedContext).toHaveTextContent("P1_CASE_DETAIL");
    expect(screen.getByLabelText("Coverage level")).toHaveTextContent("Coverage L2");

    await user.selectOptions(phaseSelector, "1");

    expect(phaseSelector).toHaveValue("1");
    expect(screen.getByText(/Waiting on P2/i)).toBeInTheDocument();
    expect(screen.getAllByText(/PENDING_APPROVAL/i).length).toBeGreaterThan(0);
  });

  it("can render a governed initial phase for static Storybook stories", () => {
    render(<App initialPhaseNumber={3} />);

    expect(screen.getByLabelText("Mock fixture resolved context")).toHaveTextContent("Role P2");
    expect(screen.getByLabelText("Mock fixture resolved context")).toHaveTextContent("P2_APPROVAL");
    expect(screen.getByLabelText("Mock fixture resolved context")).toHaveTextContent(
      "OBSERVATION_WINDOW"
    );
  });

  it("supports P1 evidence Auto, Manual, and Pin controls without hover-only access", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(screen.getAllByRole("button", { name: /Open case/i })[0]);

    const evidencePanel = screen.getByRole("complementary", { name: "Contextual Evidence" });
    const autoButton = within(evidencePanel).getByRole("button", { name: "Auto" });
    const manualButton = within(evidencePanel).getByRole("button", { name: "Manual" });

    expect(autoButton).toHaveAttribute("aria-pressed", "true");
    expect(within(evidencePanel).getByRole("button", { name: "Pin" })).toBeInTheDocument();
    expect(
      within(evidencePanel).getByRole("heading", { name: panelTitle("process_evidence") })
    ).toBeInTheDocument();

    await user.click(
      within(evidencePanel).getByRole("button", { name: new RegExp(panelTitle("event_timeline")) })
    );

    expect(manualButton).toHaveAttribute("aria-pressed", "true");
    expect(
      within(evidencePanel).getByRole("heading", { name: panelTitle("event_timeline") })
    ).toBeInTheDocument();

    await user.click(within(evidencePanel).getByRole("button", { name: "Pin" }));
    expect(within(evidencePanel).getByText("Pinned evidence frame")).toBeInTheDocument();

    const whyEvidenceAnchor = screen.getByRole("button", { name: "WHY evidence anchor" });
    expect(whyEvidenceAnchor).toHaveAttribute("aria-disabled", "true");
    await user.click(whyEvidenceAnchor);
    expect(
      within(evidencePanel).getByRole("heading", { name: panelTitle("event_timeline") })
    ).toBeInTheDocument();

    await user.click(within(evidencePanel).getByRole("button", { name: "Unpin" }));
    await user.click(autoButton);
    expect(whyEvidenceAnchor).toHaveAttribute("aria-disabled", "false");
    await user.click(whyEvidenceAnchor);

    expect(autoButton).toHaveAttribute("aria-pressed", "true");
    expect(
      within(evidencePanel).getByRole("heading", {
        name: panelTitle(firstSectionEvidenceRef("WHY", "lateral_topology"))
      })
    ).toBeInTheDocument();
  });

  it("keeps fixture authority over URL and storage role or coverage injection", () => {
    window.history.pushState({}, "", "/case/CASE-2847?coverage=L3");
    window.localStorage.setItem("role", "P3");
    window.sessionStorage.setItem("coverage", "L3");

    render(<App />);

    expect(screen.getByLabelText("Coverage level")).toHaveTextContent("Coverage L2");
    expect(screen.getByLabelText("Mock fixture resolved context")).toHaveTextContent("Role P1");
  });

  it("keeps P3 host-level raw evidence DOM absent in the Phase 6 resolved context", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.selectOptions(screen.getByLabelText("Mock fixture phase"), "6");
    await user.click(screen.getAllByRole("button", { name: /Open case/i })[0]);

    expect(screen.getByLabelText("Mock fixture resolved context")).toHaveTextContent("Role P3");
    expect(screen.getByLabelText("Mock fixture resolved context")).toHaveTextContent("P3_MANAGER");
    expect(screen.queryByText(panelTitle("process_evidence"))).not.toBeInTheDocument();
    expect(screen.queryByTestId("host-raw-evidence")).not.toBeInTheDocument();
    expect(screen.getByLabelText("Case follow-up input")).toBeInTheDocument();
  });

  it("renders missing-signal redline notices from ui_messages only", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.selectOptions(
      screen.getByLabelText("Mock redline fixture"),
      "boundary-p2-cmdb-tags-unavailable"
    );
    await user.click(screen.getAllByRole("button", { name: /Open case/i })[0]);

    const notice = screen.getByTestId("missing-signal-notice");
    expect(notice).toHaveAttribute("data-message-source", "ui_messages");
    expect(notice).toHaveTextContent("CMDB tags unavailable in mock fixture.");
    expect(screen.getByTestId("app-redline-renderability")).toHaveTextContent(
      "Static, read-only renderability"
    );
  });

  it("renders stale approve rejection as a disabled inline warning without workflow controls", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.selectOptions(
      screen.getByLabelText("Mock redline fixture"),
      "boundary-concurrency-stale-approve-rejected"
    );
    await user.click(screen.getAllByRole("button", { name: /Open case/i })[0]);

    const warning = screen.getByTestId("concurrency-inline-warning");
    expect(warning).toHaveAttribute("aria-disabled", "true");
    expect(warning).toHaveAttribute("data-concurrency-state", "stale-approve-rejected");
    expect(warning).toHaveTextContent("Stale approve was rejected");
    expect(screen.queryByRole("button", { name: /approve|reject|delay|observe/i })).not.toBeInTheDocument();
  });

  it("renders resolver degradation without unlocking L1 blast radius", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.selectOptions(
      screen.getByLabelText("Mock redline fixture"),
      "resolver-l1-blast-radius-payload"
    );
    await user.click(screen.getAllByRole("button", { name: /Open case/i })[0]);

    expect(screen.getByLabelText("Coverage level")).toHaveTextContent("Coverage L1");
    expect(screen.getByTestId("resolver-degradation-notice")).toHaveTextContent(
      "coverage L1 keeps blast_radius OFF"
    );
    expect(screen.getByTestId("blast-radius-redline")).toHaveAttribute(
      "data-visibility-state",
      "OFF"
    );
  });

  it("renders a cautious P3 manager summary without host raw evidence or over-certainty", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.selectOptions(
      screen.getByLabelText("Mock redline fixture"),
      "resolver-p3-technical-detail-redaction"
    );
    await user.click(screen.getAllByRole("button", { name: /Open case/i })[0]);

    const managerSummary = screen.getByTestId("manager-summary");
    expect(managerSummary).toHaveTextContent("Manager summary stays cautious");
    expect(managerSummary).not.toHaveTextContent(/完全受控|已彻底消除/i);
    expect(screen.queryByTestId("host-raw-evidence")).not.toBeInTheDocument();
  });

  it("does not expose poison-pill fixtures as app renderability options", () => {
    render(<App />);

    const redlineSelector = screen.getByLabelText("Mock redline fixture") as HTMLSelectElement;
    const optionValues = Array.from(redlineSelector.options).map((option) => option.value);

    expect(optionValues.some((value) => value.startsWith("poison-"))).toBe(false);
  });
});
