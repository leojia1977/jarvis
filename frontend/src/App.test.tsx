import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import App from "./App";

describe("SecuPilot first-batch workbench slice", () => {
  beforeEach(() => {
    window.history.pushState({}, "", "/inbox");
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

    expect(window.location.pathname).toBe("/case/CASE-001");
    expect(screen.getByText("CASE-001")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: /Critical action required/i })).toBeInTheDocument();
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
    expect(screen.getAllByText(/Unsupported claim/i).length).toBeGreaterThan(0);
    expect(screen.getByText(/Read-only frame summaries/i)).toBeInTheDocument();
    expect(screen.getByLabelText("Case follow-up input")).toBeInTheDocument();
    const evidencePanel = screen.getByRole("complementary", { name: "Contextual Evidence" });
    expect(within(evidencePanel).queryByRole("textbox")).not.toBeInTheDocument();
    expect(document.body).not.toHaveTextContent(/IMMEDIATE|DELAYED|OBSERVE_ONLY/);
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
    expect(within(evidencePanel).getByRole("heading", { name: "Process / Execution Evidence" })).toBeInTheDocument();

    await user.click(within(evidencePanel).getByRole("button", { name: /Event Timeline/i }));

    expect(manualButton).toHaveAttribute("aria-pressed", "true");
    expect(within(evidencePanel).getByRole("heading", { name: "Event Timeline" })).toBeInTheDocument();

    await user.click(within(evidencePanel).getByRole("button", { name: "Pin" }));
    expect(within(evidencePanel).getByText("Pinned evidence frame")).toBeInTheDocument();

    const whyEvidenceAnchor = screen.getByRole("button", { name: "WHY evidence anchor" });
    expect(whyEvidenceAnchor).toHaveAttribute("aria-disabled", "true");
    await user.click(whyEvidenceAnchor);
    expect(within(evidencePanel).getByRole("heading", { name: "Event Timeline" })).toBeInTheDocument();

    await user.click(within(evidencePanel).getByRole("button", { name: "Unpin" }));
    await user.click(autoButton);
    expect(whyEvidenceAnchor).toHaveAttribute("aria-disabled", "false");
    await user.click(whyEvidenceAnchor);

    expect(autoButton).toHaveAttribute("aria-pressed", "true");
    expect(within(evidencePanel).getByRole("heading", { name: "Topology / Blast Radius Preview" })).toBeInTheDocument();
  });

  it("keeps the case follow-up input visible on low coverage cases", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(screen.getAllByRole("button", { name: /Open case/i })[1]);

    expect(window.location.pathname).toBe("/case/CASE-002");
    expect(screen.getByLabelText("Coverage level")).toHaveTextContent("Coverage L1");
    expect(screen.getByLabelText("Case follow-up input")).toBeInTheDocument();
  });
});
