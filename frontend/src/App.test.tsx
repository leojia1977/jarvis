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

  it("resolves the history route through clamp-first guard without URL or storage authority", () => {
    window.history.pushState({}, "", "/search?tab=history&coverage=L3&role=P3");
    window.localStorage.setItem("role", "P3");
    window.sessionStorage.setItem("coverage", "L3");

    render(<App />);

    const historySurface = screen.getByTestId("history-surface");
    const routeGuard = screen.getByTestId("history-route-guard");

    expect(screen.getByRole("heading", { name: "History guard" })).toBeInTheDocument();
    expect(routeGuard).toHaveAttribute("data-route-order", "resolve-clamp-guard-render");
    expect(routeGuard).toHaveAttribute("data-authority-source", "resolved-surface-context");
    expect(routeGuard).toHaveAttribute("data-requested-coverage", "L3");
    expect(routeGuard).toHaveAttribute("data-recorded-coverage", "L2");
    expect(routeGuard).toHaveAttribute("data-effective-coverage", "L2");
    expect(screen.getByLabelText("Coverage level")).toHaveTextContent("Coverage L2");
    expect(screen.getByLabelText("Mock fixture resolved context")).toHaveTextContent("Role P1");
    expect(within(historySurface).getByTestId("history-write-guard")).toHaveTextContent(
      /No write actions are attached/i
    );
    expect(
      within(historySurface).queryByRole("button", { name: /approve|reject|delay|observe|close/i })
    ).not.toBeInTheDocument();
    expect(screen.queryByTestId("host-raw-evidence")).not.toBeInTheDocument();
  });

  it("navigates to the bounded history guard from the primary navigation", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(screen.getByRole("button", { name: /Search \/ History/i }));

    expect(window.location.pathname).toBe("/search");
    expect(window.location.search).toBe("?tab=history");
    expect(screen.getByTestId("history-route-guard")).toHaveAttribute(
      "data-effective-coverage",
      "L2"
    );
  });

  it("opens a case from Inbox into the case-first detail route", async () => {
    const user = userEvent.setup();
    render(<App />);

    expect(screen.getByRole("heading", { name: "Case-first intake" })).toBeInTheDocument();
    expect(screen.getByTestId("case-first-inbox-list")).toBeInTheDocument();
    expect(document.body).not.toHaveTextContent(/work queue|current case queue|approval queue/i);

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
    expect(screen.getByTestId("honesty-layer")).toHaveAttribute("data-persistent", "true");
    expect(screen.getByRole("heading", { name: "DECISION" })).toBeInTheDocument();
    const summaryLayer = screen.getByTestId("summary-layer");
    expect(summaryLayer).toHaveAttribute("data-summary-layer", "summary_layer");
    expect(within(summaryLayer).getByTestId("summary-layer-verdict")).toHaveAttribute(
      "data-summary-field",
      "summary_layer.verdict"
    );
    expect(within(summaryLayer).getByTestId("summary-layer-summary")).toHaveAttribute(
      "data-summary-field",
      "summary_layer.summary"
    );
    const caseHeader = screen.getByTestId("case-header");
    expect(within(caseHeader).getByTestId("case-header-case-id")).toHaveTextContent("CASE-2847");
    expect(within(caseHeader).getByTestId("case-header-verdict")).toHaveTextContent(
      /HIGH mock case/i
    );
    expect(within(caseHeader).getByTestId("case-header-coverage")).toHaveTextContent("L2");
    expect(within(caseHeader).getByTestId("case-state-pill")).toHaveTextContent(
      "Under investigation"
    );
    expect(
      screen.getByText(coreSurfaceFixture.case.honesty_layer.unsupported_claims[0])
    ).toBeInTheDocument();
    expect(screen.getByText(/Read-only frame summaries/i)).toBeInTheDocument();
    expect(screen.getByLabelText("Case follow-up input")).toBeInTheDocument();
    const evidencePanel = screen.getByRole("complementary", { name: "Contextual Evidence" });
    expect(within(evidencePanel).queryByRole("textbox")).not.toBeInTheDocument();
    expect(document.body).not.toHaveTextContent(/IMMEDIATE|DELAYED|OBSERVE_ONLY/);
  });

  it("keeps HONESTY unsupported claims visible when details are folded and restored", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(screen.getAllByRole("button", { name: /Open case/i })[0]);

    const honestyLayer = screen.getByTestId("honesty-layer");
    const unsupportedClaim = coreSurfaceFixture.case.honesty_layer.unsupported_claims[0];
    const confidenceDetail =
      coreSurfaceFixture.case.honesty_layer.what_would_raise_confidence[0];

    expect(honestyLayer).toHaveAttribute("data-expanded", "true");
    expect(within(honestyLayer).getByText(unsupportedClaim)).toBeInTheDocument();
    expect(within(honestyLayer).getByText(confidenceDetail)).toBeInTheDocument();

    await user.click(within(honestyLayer).getByRole("button", { name: "Fold honesty details" }));

    expect(honestyLayer).toHaveAttribute("data-expanded", "false");
    expect(within(honestyLayer).getByText(unsupportedClaim)).toBeInTheDocument();
    expect(within(honestyLayer).queryByText(confidenceDetail)).not.toBeInTheDocument();
    expect(within(honestyLayer).getByTestId("honesty-fold-notice")).toHaveTextContent(
      /unsupported claims remain visible/i
    );

    await user.click(within(honestyLayer).getByRole("button", { name: "Expand honesty details" }));

    expect(honestyLayer).toHaveAttribute("data-expanded", "true");
    expect(within(honestyLayer).getByText(confidenceDetail)).toBeInTheDocument();
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

  it("lets P1 submit a local mock-only Action Request to P2 without changing context authority", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(screen.getAllByRole("button", { name: /Open case/i })[0]);

    const phaseSelector = screen.getByLabelText("Mock fixture phase") as HTMLSelectElement;
    const resolvedContext = screen.getByLabelText("Mock fixture resolved context");
    const actionRequestPanel = screen.getByTestId("action-request-panel");

    expect(window.location.pathname).toBe("/case/CASE-2847");
    expect(phaseSelector).toHaveValue("0");
    expect(resolvedContext).toHaveTextContent("Role P1");
    expect(resolvedContext).toHaveTextContent("P1_CASE_DETAIL");
    expect(resolvedContext).toHaveTextContent("UNDER_INVESTIGATION");
    expect(resolvedContext).toHaveTextContent("AR none");
    const triggerButton = within(actionRequestPanel).getByRole("button", {
      name: "Request P2 review"
    });
    expect(triggerButton).toBeInTheDocument();

    await user.click(triggerButton);

    const dialog = screen.getByRole("dialog", { name: "Submit Action Request to P2" });
    const submitButton = within(dialog).getByRole("button", { name: "Submit to P2" });
    const cancelButton = within(dialog).getByRole("button", { name: "Cancel" });
    expect(submitButton).toHaveFocus();
    await user.tab();
    expect(cancelButton).toHaveFocus();
    await user.tab();
    expect(submitButton).toHaveFocus();
    expect(dialog).toHaveTextContent(/P1 does not choose execution mode/i);
    expect(dialog).not.toHaveTextContent(/IMMEDIATE|DELAYED|OBSERVE_ONLY/);
    expect(within(dialog).queryByRole("button", { name: /approve|reject|delay|observe/i })).not.toBeInTheDocument();

    await user.click(cancelButton);

    expect(screen.queryByRole("dialog", { name: "Submit Action Request to P2" })).not.toBeInTheDocument();
    expect(triggerButton).toHaveFocus();

    await user.click(triggerButton);
    const reopenedDialog = screen.getByRole("dialog", { name: "Submit Action Request to P2" });
    const reopenedSubmitButton = within(reopenedDialog).getByRole("button", { name: "Submit to P2" });
    expect(reopenedSubmitButton).toHaveFocus();

    await user.click(reopenedSubmitButton);

    expect(screen.queryByRole("dialog", { name: "Submit Action Request to P2" })).not.toBeInTheDocument();
    const submittedState = screen.getByTestId("p1-action-request-submitted-state");
    expect(submittedState).toHaveTextContent(
      /Submitted to P2 review.*Waiting on P2/i
    );
    expect(submittedState).toHaveFocus();
    expect(within(actionRequestPanel).queryByRole("button", { name: "Request P2 review" })).not.toBeInTheDocument();
    expect(window.location.pathname).toBe("/case/CASE-2847");
    expect(phaseSelector).toHaveValue("0");
    expect(resolvedContext).toHaveTextContent("Role P1");
    expect(resolvedContext).toHaveTextContent("P1_CASE_DETAIL");
    expect(resolvedContext).toHaveTextContent("UNDER_INVESTIGATION");
    expect(resolvedContext).toHaveTextContent("AR none");
    expect(screen.getByTestId("case-state-pill")).toHaveTextContent("Under investigation");
    expect(screen.queryByRole("button", { name: /Approval Queue/i })).not.toBeInTheDocument();
    expect(screen.getByRole("complementary", { name: "Contextual Evidence" })).toBeInTheDocument();
    expect(screen.getByLabelText("Case follow-up input")).toBeInTheDocument();
  });

  it("keeps existing AR phases read-only without a duplicate P1 submit CTA", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.selectOptions(screen.getByLabelText("Mock fixture phase"), "1");
    await user.click(screen.getAllByRole("button", { name: /Open case/i })[0]);

    const actionRequestPanel = screen.getByTestId("action-request-panel");

    expect(actionRequestPanel).toHaveTextContent(/Waiting on P2/i);
    expect(actionRequestPanel).toHaveTextContent(/Read-only/i);
    expect(within(actionRequestPanel).queryByRole("button", { name: "Request P2 review" })).not.toBeInTheDocument();
    expect(screen.queryByRole("dialog", { name: "Submit Action Request to P2" })).not.toBeInTheDocument();
    expect(screen.getByLabelText("Mock fixture resolved context")).toHaveTextContent("PENDING_APPROVAL");
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

  it("renders EP-T01 subordinate Evidence, Timeline, and Blast Radius panels without new routes", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(screen.getAllByRole("button", { name: /Open case/i })[0]);

    const evidencePanel = screen.getByRole("complementary", { name: "Contextual Evidence" });
    const subordinateSelector = within(evidencePanel).getByTestId("subordinate-panel-selector");

    expect(within(subordinateSelector).getByRole("button", { name: "Evidence" })).toHaveAttribute(
      "aria-pressed",
      "true"
    );
    expect(within(subordinateSelector).getByRole("button", { name: "Timeline" })).toBeInTheDocument();
    expect(within(subordinateSelector).getByRole("button", { name: "Blast Radius" })).toBeInTheDocument();
    expect(within(evidencePanel).getByTestId("evidence-subordinate-panel")).toBeInTheDocument();

    await user.click(within(subordinateSelector).getByRole("button", { name: "Timeline" }));

    const timelinePanel = within(evidencePanel).getByTestId("timeline-subordinate-panel");
    expect(timelinePanel).toHaveTextContent("Read-only timeline");
    expect(timelinePanel).toHaveTextContent(/Fixture loaded|moved the mock case context/i);
    expect(window.location.pathname).toBe("/case/CASE-2847");

    await user.click(within(subordinateSelector).getByRole("button", { name: "Blast Radius" }));

    const blastRadiusPanel = within(evidencePanel).getByTestId("blast-radius-subordinate-panel");
    expect(blastRadiusPanel).toHaveTextContent("Mock-safe blast radius summary");
    expect(blastRadiusPanel).toHaveTextContent("Coverage");
    expect(blastRadiusPanel).toHaveTextContent("L2");
    expect(screen.queryByRole("button", { name: /approve|reject|delay|observe/i })).not.toBeInTheDocument();
    expect(document.body).not.toHaveTextContent(/IMMEDIATE|DELAYED|OBSERVE_ONLY/);
    expect(screen.getByTestId("dialogue-dock")).toBeInTheDocument();
  });

  it("does not attach Blast Radius subordinate detail when coverage is L1", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.selectOptions(
      screen.getByLabelText("Mock redline fixture"),
      "resolver-l1-blast-radius-payload"
    );
    await user.click(screen.getAllByRole("button", { name: /Open case/i })[0]);

    const evidencePanel = screen.getByRole("complementary", { name: "Contextual Evidence" });
    const subordinateSelector = within(evidencePanel).getByTestId("subordinate-panel-selector");

    expect(screen.getByLabelText("Coverage level")).toHaveTextContent("Coverage L1");
    expect(within(subordinateSelector).queryByRole("button", { name: "Blast Radius" })).not.toBeInTheDocument();
    expect(within(evidencePanel).queryByTestId("blast-radius-subordinate-panel")).not.toBeInTheDocument();
    expect(screen.getByTestId("blast-radius-redline")).toHaveAttribute(
      "data-visibility-state",
      "OFF"
    );
  });

  it("keeps the Dialogue Dock source-boundary local without hardcoded recommendation chips", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(screen.getAllByRole("button", { name: /Open case/i })[0]);

    const dock = screen.getByTestId("dialogue-dock");
    const sourceBoundary = within(dock).getByTestId("dialogue-source-boundary");
    const runtimePlaceholder = within(dock).getByTestId("dialogue-runtime-placeholder");
    const followUpInput = within(dock).getByLabelText("Case follow-up input");

    expect(dock).toHaveAccessibleName("Case dialogue dock");
    expect(sourceBoundary).toHaveTextContent("Case CASE-2847");
    expect(sourceBoundary).toHaveTextContent(panelTitle("process_evidence"));
    expect(runtimePlaceholder).toHaveAttribute("data-suggestion-source", "ui_messages");
    expect(runtimePlaceholder).toHaveAttribute("data-suggestion-state", "unavailable");
    expect(runtimePlaceholder).not.toHaveAttribute("role", "button");
    expect(within(dock).getAllByRole("button")).toHaveLength(1);
    expect(within(dock).queryByTestId("dialogue-suggestion-chip")).not.toBeInTheDocument();
    expect(dock).not.toHaveTextContent(
      /CMDB|blast radius|ROI|queue window|remediation|approve|reject|delay|observe|IMMEDIATE|DELAYED|OBSERVE_ONLY/i
    );

    await user.type(followUpInput, "What evidence changed?");
    await user.click(within(dock).getByRole("button", { name: "Submit case follow-up" }));

    expect(followUpInput).toHaveValue("");
    expect(window.location.pathname).toBe("/case/CASE-2847");
    expect(screen.getByLabelText("Mock fixture resolved context")).toHaveTextContent("Role P1");
    expect(screen.getByLabelText("Mock fixture resolved context")).toHaveTextContent(
      "P1_CASE_DETAIL"
    );
    expect(within(dock).queryByTestId("dialogue-suggestion-chip")).not.toBeInTheDocument();

    const evidencePanel = screen.getByRole("complementary", { name: "Contextual Evidence" });
    await user.click(
      within(evidencePanel).getByRole("button", { name: new RegExp(panelTitle("event_timeline")) })
    );

    expect(sourceBoundary).toHaveTextContent(panelTitle("event_timeline"));
    expect(within(dock).queryByTestId("dialogue-suggestion-chip")).not.toBeInTheDocument();
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

  it("renders a cautious P3 technical summary fallback without host detail or write controls", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.selectOptions(screen.getByLabelText("Mock fixture phase"), "6");
    await user.click(screen.getAllByRole("button", { name: /Open case/i })[0]);

    const evidencePanel = screen.getByRole("complementary", { name: "Contextual Evidence" });
    await user.click(
      within(evidencePanel).getByRole("button", { name: /Technical summary fallback/i })
    );

    const fallback = within(evidencePanel).getByTestId("p3-technical-panel-fallback");
    expect(fallback).toHaveAttribute("data-evidence-frame-id", "technical_summary_fallback");
    expect(fallback).toHaveTextContent("Detailed technical records are outside this P3 surface");
    expect(fallback).toHaveTextContent("read-only fallback");
    expect(fallback).not.toHaveTextContent(/完全受控|已彻底消除|command line|process tree/i);
    expect(within(evidencePanel).queryByText(panelTitle("process_evidence"))).not.toBeInTheDocument();
    expect(screen.queryByTestId("host-raw-evidence")).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /approve|reject|delay|observe|close/i })).not.toBeInTheDocument();
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
