import { ResolvedSurfaceContext, SecurityHaltCode } from "../types";
import { validateResolvedSurfaceContext } from "../validateResolvedSurfaceContext";

function baseContext(): ResolvedSurfaceContext {
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
      submit_to_p2: "ALLOW",
      approve_action_request: "HIDDEN"
    },
    resolved_visibility: {
      effective_visibility_level: "L2",
      pages: {
        case_detail: "ON",
        approval_queue: "OFF"
      },
      fields: {
        summary: "ON",
        blast_radius: "OFF"
      },
      allowed_actions: {
        submit_to_p2: "ALLOW"
      }
    },
    honesty: {
      what_would_raise_confidence: ["Additional host telemetry from 192.0.2.42."],
      what_would_disprove_current_verdict: ["Synthetic maintenance record exists."],
      unsupported_claims: ["Direct process evidence is unavailable."]
    },
    audit_trail: [
      {
        audit_id: "AUDIT-2847-AR-001",
        actor: "jsmith@corp.example",
        event: "SYNTHETIC_CONTEXT_CREATED"
      }
    ],
    ui_messages: {
      case_summary: "Synthetic case context loaded.",
      dialogue_chip_source: "[runtime: ui_messages / lao_jia_context]"
    }
  };
}

function cloneContext(overrides?: Partial<ResolvedSurfaceContext>): ResolvedSurfaceContext {
  return {
    ...structuredClone(baseContext()),
    ...overrides
  };
}

function expectHalt(input: unknown, code: SecurityHaltCode) {
  const result = validateResolvedSurfaceContext(input);
  expect(result.ok).toBe(false);
  if (!result.ok) {
    expect(result.code).toBe(code);
  }
}

describe("validateResolvedSurfaceContext", () => {
  it("accepts valid P1, P2, and P3 contexts", () => {
    const p1 = cloneContext();
    const p2 = cloneContext({
      session: { role: "P2" },
      surface: "P2_APPROVAL",
      case: {
        case_id: "CASE-2847",
        case_state: "PENDING_APPROVAL",
        coverage_level: "L2",
        expert_mode_active: false
      },
      action_request: {
        ar_id: "AR-2847-ISO-001",
        ar_status: "PENDING_APPROVAL",
        action_mode: null,
        version: "1"
      },
      action_permissions: {
        approve_action_request: "CONFIRM",
        reject_action_request: "DENY",
        observe_only: "ALLOW"
      }
    });
    const p3 = cloneContext({
      session: { role: "P3" },
      surface: "P3_MANAGER",
      action_permissions: {
        approve_action_request: "HIDDEN",
        manager_summary: "READONLY"
      },
      resolved_visibility: {
        effective_visibility_level: "L2",
        pages: {
          manager_view: "READONLY"
        },
        fields: {
          audit_summary: "READONLY",
          host_raw_evidence: "OFF"
        }
      }
    });

    expect(validateResolvedSurfaceContext(p1).ok).toBe(true);
    expect(validateResolvedSurfaceContext(p2).ok).toBe(true);
    expect(validateResolvedSurfaceContext(p3).ok).toBe(true);
  });

  it("accepts action_request absence and null action_mode as separate valid states", () => {
    const noActionRequest = cloneContext();
    delete noActionRequest.action_request;

    const submittedButUndecided = cloneContext({
      case: {
        case_id: "CASE-2847",
        case_state: "PENDING_APPROVAL",
        coverage_level: "L2",
        expert_mode_active: false
      },
      action_request: {
        ar_id: "AR-2847-ISO-001",
        ar_status: "PENDING_APPROVAL",
        action_mode: null,
        version: "1"
      }
    });

    expect(validateResolvedSurfaceContext(noActionRequest).ok).toBe(true);
    expect(validateResolvedSurfaceContext(submittedButUndecided).ok).toBe(true);
  });

  it("fails closed when fixture metadata is missing or not fully artificial", () => {
    const missingMeta = cloneContext() as Record<string, unknown>;
    delete missingMeta.fixture_meta;

    expectHalt(missingMeta, "SH-08_INVALID_CONTEXT_SHAPE");
    expectHalt(
      {
        ...cloneContext(),
        fixture_meta: {
          ...baseContext().fixture_meta,
          source: "sampled_customer_export"
        }
      },
      "SH-08_NON_ARTIFICIAL_FIXTURE"
    );

    const realDataDerived = cloneContext();
    realDataDerived.fixture_meta = {
      ...realDataDerived.fixture_meta,
      real_data_derived: true as false
    };
    expectHalt(realDataDerived, "SH-08_REAL_DATA_DERIVED");
  });

  it("fails closed for missing or unsupported surface", () => {
    const missingSurface = cloneContext() as Record<string, unknown>;
    delete missingSurface.surface;

    expectHalt(missingSurface, "SH-08_INVALID_CONTEXT_SHAPE");
    expectHalt({ ...cloneContext(), surface: "P2_APPROVAL_SURFACE" }, "SH-08_UNSUPPORTED_ENUM");
  });

  it("fails closed for surface-role mismatch and confusion attack payloads", () => {
    expectHalt(
      cloneContext({
        session: { role: "P1" },
        surface: "P3_MANAGER"
      }),
      "SH-08_SURFACE_ROLE_MISMATCH"
    );

    expectHalt(
      cloneContext({
        action_permissions: {
          approve_action_request: "ALLOW"
        }
      }),
      "SH-08_CONFUSION_ATTACK_PAYLOAD"
    );

    expectHalt(
      cloneContext({
        action_request: {
          ar_id: "AR-2847-ISO-001",
          ar_status: "PENDING_APPROVAL",
          action_mode: "IMMEDIATE",
          version: "1"
        }
      }),
      "SH-08_CONFUSION_ATTACK_PAYLOAD"
    );
  });

  it("fails closed for missing required fields and unsupported enum values", () => {
    const missingPermissions = cloneContext() as Record<string, unknown>;
    delete missingPermissions.action_permissions;

    expectHalt(missingPermissions, "SH-08_INVALID_CONTEXT_SHAPE");
    expectHalt(
      cloneContext({
        case: {
          case_id: "CASE-2847",
          case_state: "UNDER_INVESTIGATION",
          coverage_level: "L9" as "L2",
          expert_mode_active: false
        }
      }),
      "SH-08_UNSUPPORTED_ENUM"
    );
  });

  it("fails closed for unexpected top-level fields and URL or storage authority attempts", () => {
    expectHalt(
      {
        ...cloneContext(),
        debug_payload: true
      },
      "SH-08_UNEXPECTED_TOP_LEVEL_FIELD"
    );

    expectHalt(
      {
        ...cloneContext(),
        localStorage: {
          role: "P3",
          coverage_level: "L3"
        }
      },
      "SH-08_UNAUTHORIZED_CONTEXT_SOURCE"
    );
  });

  it("fails closed for P3 host raw evidence payloads before rendering", () => {
    const p3Context = cloneContext({
      session: { role: "P3" },
      surface: "P3_MANAGER",
      action_permissions: {
        manager_summary: "READONLY"
      },
      audit_trail: [
        {
          host_raw_evidence: {
            process_tree: ["synthetic-proc.exe"]
          }
        }
      ]
    });

    expectHalt(p3Context, "SH-08_P3_PRIVILEGED_PAYLOAD_PRESENT");
  });

  it("fails closed when any surface carries raw technical payload", () => {
    const p1Context = cloneContext({
      audit_trail: [
        {
          raw_evidence: {
            process_tree: ["synthetic-proc.exe"]
          }
        }
      ]
    });

    expectHalt(p1Context, "SH-08_P3_PRIVILEGED_PAYLOAD_PRESENT");
  });

  it("allows CROSS_SURFACE only as mock-only walkthrough context", () => {
    const crossSurface = cloneContext({
      surface: "CROSS_SURFACE",
      session: {
        role: "P2",
        review_surface: "test-harness"
      }
    });

    expect(validateResolvedSurfaceContext(crossSurface).ok).toBe(true);
  });

  it("fails closed for coverage ceiling promotion attempts", () => {
    expectHalt(
      cloneContext({
        case: {
          case_id: "CASE-2847",
          case_state: "UNDER_INVESTIGATION",
          coverage_level: "L1",
          expert_mode_active: false
        },
        resolved_visibility: {
          effective_visibility_level: "L2",
          pages: {
            case_detail: "ON"
          },
          fields: {
            blast_radius: "ON"
          }
        }
      }),
      "SH-08_COVERAGE_CEILING_VIOLATION"
    );
  });

  it("fails closed when context contains real-data-like fixture markers", () => {
    const realLookingContext = cloneContext({
      ui_messages: {
        customer_domain: "investigate prod.example-real.com"
      }
    });

    expectHalt(realLookingContext, "SH-08_REAL_DATA_DERIVED");
  });
});
