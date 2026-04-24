import { render, screen } from "@testing-library/react";
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

  it("keeps the case follow-up input visible on low coverage cases", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(screen.getAllByRole("button", { name: /Open case/i })[1]);

    expect(window.location.pathname).toBe("/case/CASE-002");
    expect(screen.getByLabelText("Coverage level")).toHaveTextContent("Coverage L1");
    expect(screen.getByLabelText("Case follow-up input")).toBeInTheDocument();
  });
});
