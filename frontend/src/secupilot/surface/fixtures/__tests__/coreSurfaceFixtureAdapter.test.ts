import { validateResolvedSurfaceContext } from "../../context/validateResolvedSurfaceContext";
import {
  adaptCoreSurfaceFixturePhase,
  adaptCoreSurfaceFixturePhases,
  CORE_SURFACE_FIXTURE,
  CORE_SURFACE_FIXTURE_PHASE_OPTIONS,
  CORE_SURFACE_FIXTURE_VERSION
} from "../coreSurfaceFixtureAdapter";

describe("core surface mock fixture adapter", () => {
  beforeEach(() => {
    window.history.pushState({}, "", "/inbox");
    window.localStorage.clear();
    window.sessionStorage.clear();
  });

  it("records equivalent fixture integrity before adapting phase state", () => {
    expect(CORE_SURFACE_FIXTURE_VERSION).toBe("0.1");
    expect(CORE_SURFACE_FIXTURE.status).toBe("mock-only");
    expect(CORE_SURFACE_FIXTURE.ids.case_id).toBe("CASE-2847");
    expect(CORE_SURFACE_FIXTURE_PHASE_OPTIONS.map((phase) => phase.phase)).toEqual([
      0, 1, 2, 3, 4, 5, 6
    ]);
    expect(CORE_SURFACE_FIXTURE_PHASE_OPTIONS.map((phase) => phase.surface)).toEqual([
      "P1_CASE_DETAIL",
      "P1_CASE_DETAIL",
      "P2_APPROVAL",
      "P2_APPROVAL",
      "P2_APPROVAL",
      "P2_APPROVAL",
      "P3_MANAGER"
    ]);
  });

  it("returns seven contexts and validates every phase through E0-01 ContextValidator", () => {
    const contexts = adaptCoreSurfaceFixturePhases();

    expect(contexts).toHaveLength(7);
    for (const context of contexts) {
      expect(validateResolvedSurfaceContext(context)).toMatchObject({ ok: true });
    }
  });

  it("maps Phase 0 to P1 case detail with no submitted action request", () => {
    const context = adaptCoreSurfaceFixturePhase(0);

    expect(context.session.role).toBe("P1");
    expect(context.surface).toBe("P1_CASE_DETAIL");
    expect(context.case.case_state).toBe("UNDER_INVESTIGATION");
    expect(context.action_request).toBeUndefined();
  });

  it("maps Phase 1 to a submitted AR with null action mode", () => {
    const context = adaptCoreSurfaceFixturePhase(1);

    expect(context.session.role).toBe("P1");
    expect(context.action_request?.ar_status).toBe("PENDING_APPROVAL");
    expect(context.action_request?.action_mode).toBeNull();
  });

  it("maps Phase 2 to P2 approval with no selected action mode", () => {
    const context = adaptCoreSurfaceFixturePhase(2);

    expect(context.session.role).toBe("P2");
    expect(context.surface).toBe("P2_APPROVAL");
    expect(context.action_request?.ar_status).toBe("PENDING_APPROVAL");
    expect(context.action_request?.action_mode).toBeNull();
  });

  it("maps Phase 3 to observe-only observation window context", () => {
    const context = adaptCoreSurfaceFixturePhase(3);

    expect(context.case.case_state).toBe("OBSERVATION_WINDOW");
    expect(context.action_request?.ar_status).toBe("OBSERVATION_WINDOW");
    expect(context.action_request?.action_mode).toBe("OBSERVE_ONLY");
    expect(context.action_request?.observation_window_minutes).toBe(60);
    expect(context.action_request?.observation_expiry_action).toBe(
      "RETURN_TO_PENDING_APPROVAL"
    );
  });

  it("maps Phase 4 back to pending approval without browser timer authority", () => {
    window.localStorage.setItem("observation_window_remaining_minutes", "1");
    window.sessionStorage.setItem("action_mode", "IMMEDIATE");

    const context = adaptCoreSurfaceFixturePhase(4);

    expect(context.case.case_state).toBe("PENDING_APPROVAL");
    expect(context.action_request?.ar_status).toBe("PENDING_APPROVAL");
    expect(context.action_request?.action_mode).toBeNull();
    expect(Object.keys(context)).not.toEqual(expect.arrayContaining(["url", "storage"]));
  });

  it("maps Phase 5 to immediate action only under P2", () => {
    const context = adaptCoreSurfaceFixturePhase(5);

    expect(context.session.role).toBe("P2");
    expect(context.surface).toBe("P2_APPROVAL");
    expect(context.action_request?.action_mode).toBe("IMMEDIATE");
  });

  it("maps Phase 6 to P3 manager review without privileged raw technical payload", () => {
    const context = adaptCoreSurfaceFixturePhase(6);
    const serialized = JSON.stringify(context);

    expect(context.session.role).toBe("P3");
    expect(context.surface).toBe("P3_MANAGER");
    expect(context.action_permissions.manager_review).toBe("READONLY");
    expect(serialized).not.toContain("contains_host_level_raw_evidence");
    expect(serialized).not.toContain("process_tree");
    expect(serialized).not.toContain("raw_event_payload");
  });

  it("ignores URL and storage role or coverage injection as authority sources", () => {
    window.history.pushState({}, "", "/case/CASE-2847?role=P3&coverage=L3");
    window.localStorage.setItem("role", "P3");
    window.sessionStorage.setItem("coverage", "L3");

    const context = adaptCoreSurfaceFixturePhase(0);

    expect(context.session.role).toBe("P1");
    expect(context.case.coverage_level).toBe("L2");
    expect(context.surface).toBe("P1_CASE_DETAIL");
  });
});
