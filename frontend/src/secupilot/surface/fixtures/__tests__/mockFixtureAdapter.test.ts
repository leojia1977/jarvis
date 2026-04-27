import { validateResolvedSurfaceContext } from "../../context/validateResolvedSurfaceContext";
import { FIXTURE_REGISTRY_ENTRIES } from "../fixtureRegistry";
import { mockFixtureAdapter } from "../mockFixtureAdapter";

describe("mock fixture adapter QA expansion", () => {
  beforeEach(() => {
    window.history.pushState({}, "", "/case/CASE-2847?role=P3&coverage=L3&surface=P3_MANAGER");
    window.localStorage.setItem("role", "P3");
    window.localStorage.setItem("coverage", "L3");
    window.sessionStorage.setItem("surface", "P2_APPROVAL");
  });

  it("registers phase, boundary, poison-pill, and resolver-degradation fixtures", () => {
    expect(mockFixtureAdapter.listPhaseFixtures()).toEqual([
      "phase-00-p1-under-investigation",
      "phase-01-p1-submitted-waiting-on-p2",
      "phase-02-p2-pending-approval",
      "phase-03-p2-observation-window-active",
      "phase-04-p2-observation-expired-returned-pending",
      "phase-05-p2-approved-pending-execution",
      "phase-06-p3-manager-audit-summary",
      "phase-07-cross-surface-full-walkthrough"
    ]);
    expect(mockFixtureAdapter.listBoundaryFixtures()).toEqual([
      "boundary-p3-audit-summary-unavailable",
      "boundary-p2-cmdb-tags-unavailable",
      "boundary-dirty-update-during-observation-window",
      "boundary-concurrency-stale-approve-rejected"
    ]);
    expect(mockFixtureAdapter.listResolverDegradationFixtures()).toEqual([
      "resolver-l1-blast-radius-payload",
      "resolver-l1-lineage-confidence-degraded",
      "resolver-p3-technical-detail-redaction",
      "resolver-search-history-current-lower-than-recorded",
      "resolver-search-history-current-higher-than-recorded"
    ]);
    expect(mockFixtureAdapter.listPoisonPillFixtures()).toHaveLength(11);
  });

  it("validates every non-poison fixture by default", () => {
    const validFixtureIds = FIXTURE_REGISTRY_ENTRIES.filter(
      (entry) => entry.kind !== "poison_pill"
    ).map((entry) => entry.id);

    for (const fixtureId of validFixtureIds) {
      const context = mockFixtureAdapter.getFixture(fixtureId);
      expect(validateResolvedSurfaceContext(context)).toMatchObject({ ok: true });
    }
  });

  it("keeps Phase 07 as CROSS_SURFACE fixture-only walkthrough", () => {
    const context = mockFixtureAdapter.getFixture("phase-07-cross-surface-full-walkthrough");

    expect(context.surface).toBe("CROSS_SURFACE");
    expect(context.ui_messages.cross_surface_scope).toBe("fixture-only route handoff rehearsal");
    expect(context.resolved_visibility.pages.cross_surface_walkthrough).toBe("ON");
  });

  it("allows validate=false only for poison-pill rejection tests", () => {
    expect(() =>
      mockFixtureAdapter.getFixture("phase-00-p1-under-investigation", { validate: false })
    ).toThrow(/validate=false is only allowed/);

    const poisonContext = mockFixtureAdapter.getFixture("poison-missing-surface", {
      validate: false
    });

    expect(validateResolvedSurfaceContext(poisonContext)).toMatchObject({
      ok: false,
      code: "SH-08_INVALID_CONTEXT_SHAPE"
    });
  });

  it("rejects every poison pill through ContextValidator and default adapter validation", () => {
    for (const fixtureId of mockFixtureAdapter.listPoisonPillFixtures()) {
      expect(() => mockFixtureAdapter.getFixture(fixtureId)).toThrow(/failed validation/);

      const poisonContext = mockFixtureAdapter.getFixture(fixtureId, { validate: false });
      const result = validateResolvedSurfaceContext(poisonContext);
      expect(result.ok).toBe(false);
      if (!result.ok) {
        expect(result.code).toMatch(/^SH-08_/);
      }
    }
  });

  it("ignores URL and storage authority attempts while loading validated fixtures", () => {
    const context = mockFixtureAdapter.getFixture("phase-00-p1-under-investigation");

    expect(context.session.role).toBe("P1");
    expect(context.case.coverage_level).toBe("L2");
    expect(context.surface).toBe("P1_CASE_DETAIL");
    expect(Object.keys(context)).not.toEqual(expect.arrayContaining(["url_params", "storage"]));
  });

  it("degrades L1 blast radius to OFF without triggering SH-08", () => {
    const context = mockFixtureAdapter.getFixture("resolver-l1-blast-radius-payload");

    expect(context.case.coverage_level).toBe("L1");
    expect(context.resolved_visibility.effective_visibility_level).toBe("L1");
    expect(context.resolved_visibility.fields.blast_radius).toBe("OFF");
    expect(validateResolvedSurfaceContext(context)).toMatchObject({ ok: true });
  });

  it("keeps boundary concurrency stale approve rejected as inline-warning state", () => {
    const context = mockFixtureAdapter.getFixture("boundary-concurrency-stale-approve-rejected");

    expect(context.case.case_state).toBe("OBSERVATION_WINDOW");
    expect(context.action_request?.ar_status).toBe("OBSERVATION_WINDOW");
    expect(context.action_permissions.approve_action).toBe("DISABLED");
    expect(context.ui_messages.inline_warning).toContain("Stale approve was rejected");
  });

  it("keeps missing-signal notices sourced from ui_messages", () => {
    const p3Boundary = mockFixtureAdapter.getFixture("boundary-p3-audit-summary-unavailable");
    const p2Boundary = mockFixtureAdapter.getFixture("boundary-p2-cmdb-tags-unavailable");

    expect(p3Boundary.ui_messages.missing_signal_notice_source).toBe(
      'data-message-source="ui_messages"'
    );
    expect(p2Boundary.ui_messages.missing_signal_notice_source).toBe(
      'data-message-source="ui_messages"'
    );
  });

  it("does not let current search history visibility unlock recorded L3 fields", () => {
    const context = mockFixtureAdapter.getFixture(
      "resolver-search-history-current-higher-than-recorded"
    );

    expect(context.case.coverage_level).toBe("L3");
    expect(context.resolved_visibility.effective_visibility_level).toBe("L2");
    expect(context.resolved_visibility.fields.coverage_l3_fields).toBe("OFF");
  });
});
