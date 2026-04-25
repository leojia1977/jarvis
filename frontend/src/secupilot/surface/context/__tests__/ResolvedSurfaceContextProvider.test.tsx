import { render, screen } from "@testing-library/react";
import { ResolvedSurfaceContextProvider } from "../ResolvedSurfaceContextProvider";
import { ResolvedSurfaceContext } from "../types";

function validContext(): ResolvedSurfaceContext {
  return {
    fixture_meta: {
      source: "fully_artificial",
      real_data_derived: false,
      contains_real_customer_data: false,
      input_revision: "v0.1",
      allowed_for: "mock-only bounded frontend implementation",
      not_allowed_for: ["production", "real-data", "external-pilot"]
    },
    session: {
      role: "P1"
    },
    surface: "P1_CASE_DETAIL",
    case: {
      case_id: "CASE-2847",
      case_state: "UNDER_INVESTIGATION",
      coverage_level: "L2",
      expert_mode_active: false
    },
    action_permissions: {
      submit_to_p2: "ALLOW"
    },
    resolved_visibility: {
      effective_visibility_level: "L2",
      pages: {
        case_detail: "ON"
      },
      fields: {
        summary: "ON",
        process_tree: "OFF"
      }
    },
    honesty: {
      what_would_raise_confidence: ["More synthetic telemetry."],
      what_would_disprove_current_verdict: ["Synthetic benign maintenance record."],
      unsupported_claims: ["Direct process evidence unavailable."]
    },
    audit_trail: [
      {
        audit_id: "AUDIT-2847-AR-001",
        event: "SYNTHETIC_CONTEXT_CREATED"
      }
    ],
    ui_messages: {
      summary: "Synthetic context only."
    }
  };
}

describe("ResolvedSurfaceContextProvider", () => {
  it("renders child surface placeholder for valid context", () => {
    render(
      <ResolvedSurfaceContextProvider input={validContext()}>
        {(context) => <div>Surface ready for {context.case.case_id}</div>}
      </ResolvedSurfaceContextProvider>
    );

    expect(screen.getByText("Surface ready for CASE-2847")).toBeInTheDocument();
    expect(screen.queryByRole("alert", { name: "Security Halt" })).not.toBeInTheDocument();
  });

  it("renders SH-08 for invalid context without rendering case evidence", () => {
    const invalid = {
      ...validContext(),
      surface: "P3_MANAGER"
    };

    render(
      <ResolvedSurfaceContextProvider input={invalid}>
        {() => <div>case evidence raw context should not render</div>}
      </ResolvedSurfaceContextProvider>
    );

    expect(screen.getByRole("alert", { name: "Security Halt" })).toBeInTheDocument();
    expect(screen.getByText("Security Halt")).toBeInTheDocument();
    expect(screen.getByText("SH-08")).toBeInTheDocument();
    expect(
      screen.getByText("Resolved surface context failed validation. Rendering stopped.")
    ).toBeInTheDocument();
    expect(screen.getByText("No case evidence is rendered in this state.")).toBeInTheDocument();
    expect(screen.queryByText("case evidence raw context should not render")).not.toBeInTheDocument();
    expect(screen.queryByText(/CASE-2847/)).not.toBeInTheDocument();
  });

  it("does not display raw context JSON or privileged payload in SH-08", () => {
    const invalid = {
      ...validContext(),
      localStorage: {
        role: "P3",
        raw_context: JSON.stringify({ secret: "never-render" })
      }
    };

    render(
      <ResolvedSurfaceContextProvider input={invalid}>
        {() => <div>valid child</div>}
      </ResolvedSurfaceContextProvider>
    );

    expect(screen.getByRole("alert", { name: "Security Halt" })).toBeInTheDocument();
    expect(screen.queryByText(/never-render/)).not.toBeInTheDocument();
    expect(screen.queryByText(/raw_context/)).not.toBeInTheDocument();
    expect(screen.queryByText(/localStorage/)).not.toBeInTheDocument();
  });

  it("reports sanitized halt code through the optional callback", () => {
    const onInvalidContext = vi.fn();

    render(
      <ResolvedSurfaceContextProvider input={{}} onInvalidContext={onInvalidContext}>
        {() => <div>valid child</div>}
      </ResolvedSurfaceContextProvider>
    );

    expect(onInvalidContext).toHaveBeenCalledWith(
      "SH-08_INVALID_CONTEXT_SHAPE",
      "fixture_meta is required"
    );
  });
});
