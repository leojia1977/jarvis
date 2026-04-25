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
    expect(within(evidencePanel).queryByRole("button")).not.toBeInTheDocument();
    expect(within(evidencePanel).queryByRole("textbox")).not.toBeInTheDocument();
    expect(document.body).not.toHaveTextContent(/IMMEDIATE|DELAYED|OBSERVE_ONLY/);
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
