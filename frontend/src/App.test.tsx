import { act, render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { vi } from "vitest";
import coreSurfaceFixture from "../fixtures/secupilot_core_surface_fixture_v0_1.json";
import App, { ApprovalRouteShell, CoverageHealthView, ManagerView } from "./App";
import { validateResolvedSurfaceContext } from "./secupilot/surface/context/validateResolvedSurfaceContext";
import { adaptCoreSurfaceFixturePhase } from "./secupilot/surface/fixtures/coreSurfaceFixtureAdapter";
import type { ResolvedSurfaceContext } from "./secupilot/surface/context/types";

const APPROVED_PENDING_EXECUTION_PHASE = 5;
const OBSERVATION_WINDOW_PHASE = 3;

function emitMockStateSync(detail: Record<string, unknown>) {
  act(() => {
    window.dispatchEvent(new CustomEvent("secupilot:mock-state-sync", { detail }));
  });
}

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

function buildP0CoverageHealthContext(): ResolvedSurfaceContext {
  const context = adaptCoreSurfaceFixturePhase(0);
  const p0Context: ResolvedSurfaceContext = {
    ...context,
    session: {
      ...context.session,
      role: "P0"
    },
    surface: "CROSS_SURFACE",
    resolved_visibility: {
      ...context.resolved_visibility,
      pages: {
        ...context.resolved_visibility.pages,
        coverage_health: "ON"
      }
    }
  };
  const result = validateResolvedSurfaceContext(p0Context);
  if (!result.ok) {
    throw new Error(`P0 coverage test context failed ${result.code}: ${result.reason}`);
  }
  return result.context;
}

function buildP0ReadonlyApprovalTestHarnessContext(): ResolvedSurfaceContext {
  const context = adaptCoreSurfaceFixturePhase(2);
  const p0ReadonlyActionPermissions = Object.fromEntries(
    Object.keys(context.action_permissions).map((key) => [key, "READONLY"])
  ) as ResolvedSurfaceContext["action_permissions"];
  const p0ReadonlyAllowedActions = Object.fromEntries(
    Object.keys(context.resolved_visibility.allowed_actions ?? context.action_permissions).map(
      (key) => [key, "READONLY"]
    )
  ) as NonNullable<ResolvedSurfaceContext["resolved_visibility"]["allowed_actions"]>;
  const p0Context: ResolvedSurfaceContext = {
    ...context,
    session: {
      ...context.session,
      role: "P0"
    },
    surface: "CROSS_SURFACE",
    action_request: context.action_request
      ? {
          ...context.action_request,
          action_mode: null
        }
      : undefined,
    action_permissions: p0ReadonlyActionPermissions,
    resolved_visibility: {
      ...context.resolved_visibility,
      pages: {
        ...context.resolved_visibility.pages,
        approval: "READONLY"
      },
      allowed_actions: p0ReadonlyAllowedActions
    }
  };
  const result = validateResolvedSurfaceContext(p0Context);
  if (!result.ok) {
    throw new Error(
      `AP-T02 P0 readonly approval test harness failed ${result.code}: ${result.reason}`
    );
  }
  return result.context;
}

function buildApprovalRouteCase(
  context: ResolvedSurfaceContext
): Parameters<typeof ApprovalRouteShell>[0]["activeCase"] {
  return {
    id: context.case.case_id
  } as Parameters<typeof ApprovalRouteShell>[0]["activeCase"];
}

function buildApprovalAuditSourceContext(
  state: "empty" | "unavailable"
): ResolvedSurfaceContext {
  const context = adaptCoreSurfaceFixturePhase(2);
  const nextContext: ResolvedSurfaceContext = {
    ...context,
    audit_trail: [],
    ui_messages: {
      ...context.ui_messages,
      audit_trail_source_availability: state === "unavailable" ? "unavailable" : "available",
      approval_audit_empty_notice:
        "Approval audit source is readable and contains zero records.",
      audit_source_unavailable_notice:
        "Approval audit source is unavailable from governed ui_messages."
    }
  };
  const result = validateResolvedSurfaceContext(nextContext);
  if (!result.ok) {
    throw new Error(`AP-T09 audit source test context failed ${result.code}: ${result.reason}`);
  }
  return result.context;
}

describe("SecuPilot first-batch workbench slice", () => {
  beforeEach(() => {
    window.history.pushState({}, "", "/inbox");
    window.localStorage.clear();
    window.sessionStorage.clear();
  });

  afterEach(() => {
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
    expect(screen.getByRole("button", { name: /S1 证据/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /本地试用/i })).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /Approval Queue/i })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /Coverage & Health/i })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /Manager View/i })).not.toBeInTheDocument();
  });

  it("updates visible navigation when role changes", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(screen.getByRole("button", { name: "P2" }));

    expect(screen.getByRole("button", { name: /S1 证据/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /本地试用/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Approval Queue/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Coverage & Health/i })).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /Manager View/i })).not.toBeInTheDocument();
  });

  it("opens the S1 artifact viewer from the workbench without action controls", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(screen.getByRole("button", { name: /S1 证据/i }));

    const surface = screen.getByTestId("s1-artifact-view");

    expect(window.location.pathname).toBe("/s1-run");
    expect(surface).toHaveAttribute("data-artifact-source", "static-mvp-fixture");
    expect(surface).toHaveAttribute("data-runtime-source", "none");
    expect(surface).toHaveAttribute("data-customer-visible-output", "false");
    expect(surface).toHaveAttribute("data-production-writeback", "false");
    expect(surface).toHaveAttribute("data-qwen-used", "false");
    expect(screen.getByTestId("s1-final-outcome-label")).toHaveTextContent(
      "带备注通过，可进入下一轮内部本地试用评审"
    );
    expect(screen.getByTestId("s1-final-outcome-code-link")).toHaveTextContent(
      "技术码已收起"
    );
    expect(screen.getByTestId("s1-final-outcome-code-link")).toHaveAttribute(
      "title",
      expect.stringContaining("S1_CLOSED_SHADOW_PASS_WITH_NOTES")
    );
    expect(screen.getByRole("heading", { name: "本地离线试用结果" })).toBeInTheDocument();
    expect(screen.getByTestId("s1-result-decision")).toHaveTextContent(
      "带备注通过，可进入下一轮内部本地试用评审"
    );
    expect(screen.getByTestId("s1-result-decision-explainer")).toHaveTextContent(
      "不代表客户发布或生产部署 GO"
    );
    expect(screen.getByTestId("s1-result-technical-code-link")).toHaveTextContent(
      "查看技术对账"
    );
    expect(screen.getByTestId("s1-run-next-step")).toHaveTextContent(
      "进入内部本地试用下一轮"
    );
    expect(screen.getByTestId("s1-run-next-step-code-link")).toHaveTextContent(
      "技术码已收起"
    );
    expect(screen.getByTestId("s1-run-id")).toHaveTextContent(
      "S1-CLOSED-SHADOW-2026-04-30-001"
    );
    expect(screen.getByTestId("s1-provider")).toHaveTextContent("fixture");
    expect(screen.getByTestId("s1-case-count")).toHaveTextContent("20");
    expect(screen.getByTestId("s1-safety-finding-count")).toHaveTextContent("0");
    expect(screen.getByTestId("s1-customer-visible-output")).toHaveTextContent("否");
    expect(screen.getByTestId("s1-production-writeback")).toHaveTextContent("否");
    expect(screen.getByTestId("s1-qwen-autonomy")).toHaveTextContent("否");
    expect(screen.getByTestId("s1-qwen-used")).toHaveTextContent("否");
    expect(screen.getByTestId("s1-production-deploy")).toHaveTextContent("否");
    const reviewPanel = screen.getByTestId("s1-local-review-panel");
    expect(reviewPanel).toHaveAttribute("data-review-scope", "LOCAL_OFFLINE_TRIAL_RC_011_CN");
    expect(reviewPanel).toHaveAttribute("data-source-candidate", "LOCAL_OFFLINE_TRIAL_RC_010_CN");
    expect(reviewPanel).toHaveAttribute("data-state-mutation", "none");
    expect(reviewPanel).toHaveAttribute("data-artifact-write", "false");
    expect(reviewPanel).toHaveAttribute("data-qwen-api-call", "false");
    expect(reviewPanel).toHaveAttribute("data-connector-call", "false");
    expect(screen.getAllByTestId("s1-review-decision-option")).toHaveLength(4);
    expect(screen.getByTestId("s1-selected-review-decision")).toHaveTextContent(
      "PASS_TO_NEXT_LOCAL_RC"
    );
    expect(screen.getByTestId("s1-review-record-preview")).toHaveTextContent(
      '"artifact_write": false'
    );
    expect(screen.getByTestId("s1-review-record-preview")).toHaveTextContent(
      '"qwen_api_call": false'
    );
    const handoffPanel = screen.getByTestId("s1-review-handoff-panel");
    expect(handoffPanel).toHaveAttribute("data-review-mode", "LOCAL_OFFLINE_REVIEW_ONLY");
    expect(handoffPanel).toHaveAttribute(
      "data-review-package",
      "artifacts/local_demo_packages/local-offline-trial-rc-011-cn-review"
    );
    expect(handoffPanel).toHaveAttribute("data-state-mutation", "none");
    expect(handoffPanel).toHaveAttribute("data-qwen-api-call", "false");
    expect(screen.getByTestId("s1-review-zip-name")).toHaveTextContent(
      "local-offline-trial-rc-011-cn-review-package-20260507.zip"
    );
    expect(screen.getAllByTestId("s1-review-required-check")).toHaveLength(10);
    expect(screen.getAllByTestId("s1-review-boundary-check")).toHaveLength(6);
    expect(screen.getAllByTestId("s1-artifact-row")).toHaveLength(5);
    expect(screen.getAllByTestId("s1-case-row")).toHaveLength(20);
    expect(screen.getByTestId("s1-technical-reconciliation")).not.toHaveAttribute("open");
    expect(screen.getByTestId("s1-final-outcome-code")).toHaveTextContent(
      "S1_CLOSED_SHADOW_PASS_WITH_NOTES"
    );
    expect(screen.getByTestId("s1-run-next-step-code")).toHaveTextContent(
      "RC011_LOCAL_OFFLINE_REVIEW"
    );
    expect(within(surface).queryByRole("button", { name: /approve|deploy|publish/i }))
      .not.toBeInTheDocument();
  });

  it("opens the S1 local offline trial walkthrough without external authority", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(screen.getByRole("button", { name: /本地试用/i }));

    const surface = screen.getByTestId("s1-local-trial-view");

    expect(window.location.pathname).toBe("/s1-trial");
    expect(screen.getByRole("heading", { name: "SecuPilot 本地离线试用中心" }))
      .toBeInTheDocument();
    expect(screen.queryByLabelText("Role selector")).not.toBeInTheDocument();
    expect(screen.queryByLabelText("Mock fixture phase")).not.toBeInTheDocument();
    expect(screen.queryByTestId("vf-03-expert-mode-frame")).not.toBeInTheDocument();
    expect(surface).not.toHaveTextContent(/MVP-14|MVP-15|MVP-17|MVP-18|MVP-19/);
    expect(surface).toHaveAttribute("data-real-data", "false");
    expect(surface).toHaveAttribute("data-live-qwen-api", "false");
    expect(surface).toHaveAttribute("data-live-connectors", "false");
    expect(surface).toHaveAttribute("data-customer-visible-output", "false");
    expect(surface).toHaveAttribute("data-production-writeback", "false");
    expect(surface).toHaveAttribute("data-push", "false");
    expect(screen.getByTestId("s1-trial-candidate")).toHaveTextContent(
      "LOCAL_OFFLINE_TRIAL_RC_011_CN"
    );
    expect(screen.getByTestId("s1-trial-readiness")).toHaveTextContent(
      "GO_FOR_INTERNAL_LOCAL_OFFLINE_REVIEW_ONLY"
    );
    expect(screen.getByTestId("s1-trial-route")).toHaveTextContent("/s1-trial");
    expect(screen.getByTestId("s1-trial-launcher-script")).toHaveTextContent(
      "scripts/launch_s1_local_offline_trial.ps1"
    );
    expect(screen.getByTestId("s1-trial-launch-command")).toHaveTextContent(
      "launch_s1_local_offline_trial.ps1"
    );
    expect(screen.getByTestId("s1-trial-package-path")).toHaveTextContent(
      "artifacts/local_demo_packages/local-offline-trial-rc-011-cn-review"
    );
    expect(screen.getByTestId("s1-trial-start-here-path")).toHaveTextContent(
      "artifacts/local_demo_packages/local-offline-trial-rc-011-cn-review/REVIEWER_START_HERE_中文.md"
    );
    expect(screen.getAllByTestId("s1-trial-step")).toHaveLength(5);
    const feedbackPanel = screen.getByTestId("s1-feedback-panel");
    expect(feedbackPanel).toHaveAttribute("data-artifact-write", "false");
    expect(feedbackPanel).toHaveAttribute("data-backend-write", "false");
    expect(feedbackPanel).toHaveAttribute("data-qwen-api-call", "false");
    expect(screen.getAllByTestId("s1-feedback-option")).toHaveLength(3);
    expect(screen.getByTestId("s1-feedback-preview")).toHaveTextContent(
      '"artifact_write": false'
    );
    const qwenContract = screen.getByTestId("s1-qwen-provider-contract");
    expect(qwenContract).toHaveAttribute("data-active-provider-mode", "qwen-cloud-disabled");
    expect(qwenContract).toHaveAttribute("data-live-call-allowed", "false");
    expect(screen.getByTestId("s1-qwen-active-mode")).toHaveTextContent(
      "qwen-cloud-disabled"
    );
    expect(screen.getAllByTestId("s1-qwen-provider-mode")).toHaveLength(3);
    const qwenDryPreview = screen.getByTestId("s1-qwen-dry-preview");
    expect(qwenDryPreview).toHaveAttribute("data-provider-mode", "dry_contract_only");
    expect(qwenDryPreview).toHaveAttribute("data-live-qwen-api", "false");
    expect(qwenDryPreview).toHaveAttribute("data-live-connectors", "false");
    expect(qwenDryPreview).toHaveAttribute("data-production-writeback", "false");
    expect(qwenDryPreview).toHaveAttribute("data-autonomous-qwen-action", "false");
    expect(screen.getByTestId("s1-qwen-dry-data-mode")).toHaveTextContent("SYNTHETIC_ONLY");
    expect(screen.getByTestId("s1-qwen-dry-case-id")).toHaveTextContent("UAT-01");
    expect(screen.getByTestId("s1-qwen-dry-reviewer-action")).toHaveTextContent(
      "REVIEW_AND_SIGNOFF_REQUIRED"
    );
    expect(screen.getByTestId("s1-qwen-dry-model-summary")).toHaveTextContent(
      "Synthetic metadata"
    );
    expect(within(surface).queryByRole("button", { name: /approve|deploy|publish/i }))
      .not.toBeInTheDocument();
  });

  it("updates the S1 local review record preview without artifact writes", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(screen.getByRole("button", { name: /S1 证据/i }));
    await user.click(screen.getByRole("button", { name: /HOLD_FOR_FIXES/ }));
    await user.clear(screen.getByTestId("s1-review-notes"));
    await user.type(screen.getByTestId("s1-review-notes"), "Hold pending RC-002 reviewer note.");

    const reviewPanel = screen.getByTestId("s1-local-review-panel");
    const preview = screen.getByTestId("s1-review-record-preview");

    expect(screen.getByTestId("s1-selected-review-decision")).toHaveTextContent("HOLD_FOR_FIXES");
    expect(preview).toHaveTextContent('"decision": "HOLD_FOR_FIXES"');
    expect(preview).toHaveTextContent('"notes": "Hold pending RC-002 reviewer note."');
    expect(preview).toHaveTextContent('"state_mutation": "none"');
    expect(preview).toHaveTextContent('"artifact_write": false');
    expect(preview).toHaveTextContent('"customer_visible_output": false');
    expect(preview).toHaveTextContent('"production_writeback": false');
    expect(within(reviewPanel).queryByRole("button", { name: /approve|deploy|publish/i }))
      .not.toBeInTheDocument();
  });

  it("opens P2 shell-only approval decision panels without state mutation", async () => {
    const user = userEvent.setup();
    render(<App initialPhaseNumber={2} />);

    await user.click(screen.getByRole("button", { name: /Approval Queue/i }));

    const surface = screen.getByTestId("approval-surface");
    const shell = screen.getByTestId("approval-shell-card");
    const statusPill = screen.getByTestId("approval-ar-status-pill");
    const ctaBoundary = screen.getByTestId("approval-cta-boundary");

    expect(window.location.pathname).toBe("/approval");
    expect(surface).toHaveAttribute("data-role", "P2");
    expect(surface).toHaveAttribute("data-authority-source", "resolved-surface-context");
    expect(surface).toHaveAttribute("data-approval-scope", "route-shell-guard-only");
    expect(statusPill).toHaveAttribute("data-ar-status", "PENDING_APPROVAL");
    expect(statusPill).toHaveAttribute("data-action-authority", "p2-only");
    expect(statusPill).toHaveAttribute("data-mapping-source", "D-02");
    expect(statusPill).toHaveAttribute("data-state-migration", "none");
    expect(ctaBoundary).toHaveAttribute("data-action-authority", "p2-only");
    expect(ctaBoundary).toHaveAttribute("data-action-wiring", "modal-only");
    expect(ctaBoundary).toHaveAttribute("data-state-mutation", "none");
    const auditBoundary = screen.getByTestId("approval-audit-source-boundary");
    const auditDerivedStatus = screen.getByTestId("approval-audit-derived-status");
    expect(auditBoundary).toHaveAttribute("data-source", "activeContext.audit_trail");
    expect(auditBoundary).toHaveAttribute("data-display-mode", "display-only");
    expect(auditBoundary).toHaveAttribute("data-state-mutation", "none");
    expect(auditBoundary).toHaveAttribute("data-derived-status-source", "fixed-enum-mapping");
    expect(auditBoundary).toHaveAttribute("data-derived-status", "OPENED");
    expect(auditBoundary).toHaveAttribute(
      "data-source-fields",
      "audit_id,event,actor_role,case_state_after,ar_status_after"
    );
    expect(auditDerivedStatus).toHaveAttribute("data-derived-status", "OPENED");
    expect(auditDerivedStatus).toHaveTextContent("Opened by P2");
    expect(screen.getByTestId("approval-audit-latest-id")).toHaveTextContent("AUD-002");
    expect(screen.getByTestId("approval-audit-latest-event")).toHaveTextContent("P2_OPENED_AR");
    expect(screen.getByTestId("approval-audit-actor-role")).toHaveTextContent("P2");
    expect(screen.getByTestId("approval-audit-ar-status-after")).toHaveTextContent(
      "PENDING_APPROVAL"
    );
    expect(screen.getByTestId("approval-audit-case-state-after")).toHaveTextContent(
      "PENDING_APPROVAL"
    );
    expect(screen.getByTestId("approval-audit-observation-presence")).toHaveTextContent(
      "Not present"
    );
    expect(screen.queryByTestId("manager-approval-audit-summary")).not.toBeInTheDocument();
    expect(within(shell).getByRole("button", { name: "Approve" })).toBeEnabled();
    expect(within(shell).getByRole("button", { name: "Reject" })).toBeEnabled();
    expect(within(shell).getByRole("button", { name: "Delay" })).toBeEnabled();
    expect(within(shell).getByRole("button", { name: "Observe" })).toBeEnabled();
    for (const button of within(ctaBoundary).getAllByRole("button")) {
      expect(button).toHaveAttribute("data-state-mutation", "none");
      expect(button).toHaveAttribute(
        "data-action-wiring",
        /delay|observe/i.test(button.textContent ?? "") ? "config-shell-only" : "modal-only"
      );
    }

    await user.click(within(shell).getByRole("button", { name: "Approve" }));

    const confirmDialog = screen.getByRole("dialog", { name: "Approve strong confirm" });
    expect(confirmDialog).toHaveAttribute("data-draft-action", "approve");
    expect(confirmDialog).toHaveAttribute("data-state-mutation", "none");
    expect(within(confirmDialog).getByTestId("approval-strong-confirm-facts")).toHaveTextContent(
      /Confirm is intentionally unavailable/i
    );
    expect(within(confirmDialog).getByTestId("approval-draft-confirm")).toBeDisabled();
    expect(confirmDialog).not.toHaveTextContent(/IMMEDIATE|DELAYED|OBSERVE_ONLY/);
    expect(within(confirmDialog).getByRole("button", { name: "Close" })).toHaveFocus();

    await user.click(within(confirmDialog).getByRole("button", { name: "Close" }));

    expect(screen.queryByRole("dialog", { name: "Approve strong confirm" }))
      .not.toBeInTheDocument();
    expect(within(shell).getByRole("button", { name: "Approve" })).toHaveFocus();

    await user.click(within(shell).getByRole("button", { name: "Observe" }));

    const configDialog = screen.getByRole("dialog", { name: "Observe configuration" });
    expect(configDialog).toHaveAttribute("data-draft-action", "observe");
    expect(configDialog).toHaveAttribute("data-state-mutation", "none");
    expect(within(configDialog).getByTestId("approval-delay-observe-config-shell"))
      .toHaveAttribute("data-timer-authority", "none");
    expect(within(configDialog).getByTestId("approval-draft-confirm")).toBeDisabled();
    expect(configDialog).not.toHaveTextContent(/IMMEDIATE|DELAYED|OBSERVE_ONLY/);

    await user.keyboard("{Escape}");

    expect(screen.queryByRole("dialog", { name: "Observe configuration" }))
      .not.toBeInTheDocument();
  });

  it("renders AP-T09 audit empty state without inventing audit rows or coverage upgrades", () => {
    const context = buildApprovalAuditSourceContext("empty");
    render(
      <ApprovalRouteShell
        activeCase={buildApprovalRouteCase(context)}
        activeContext={context}
      />
    );

    const auditBoundary = screen.getByTestId("approval-audit-source-boundary");
    const emptyState = screen.getByTestId("approval-audit-empty-state");

    expect(auditBoundary).toHaveAttribute("data-source", "activeContext.audit_trail");
    expect(auditBoundary).toHaveAttribute("data-source-guard", "source-data-availability");
    expect(auditBoundary).toHaveAttribute("data-source-availability", "available");
    expect(auditBoundary).toHaveAttribute("data-audit-source-state", "empty");
    expect(auditBoundary).toHaveAttribute("data-audit-count", "0");
    expect(emptyState).toHaveAttribute("data-message-source", "ui_messages");
    expect(emptyState).toHaveAttribute("data-source-state", "empty");
    expect(emptyState).toHaveAttribute("data-audit-row-count", "0");
    expect(emptyState).toHaveAttribute("data-coverage-upgrade", "not-suggested");
    expect(emptyState).toHaveTextContent("Approval audit source is readable");
    expect(emptyState).not.toHaveTextContent(/coverage|upgrade|unlock|L3/i);
    expect(screen.queryByTestId("approval-audit-latest-id")).not.toBeInTheDocument();
    expect(screen.queryByTestId("approval-audit-derived-status")).not.toBeInTheDocument();
    expect(screen.queryByTestId("coverage-upgrade-prompt")).not.toBeInTheDocument();
  });

  it("renders AP-T09 audit unavailable state from ui_messages without latest facts", () => {
    const context = buildApprovalAuditSourceContext("unavailable");
    render(
      <ApprovalRouteShell
        activeCase={buildApprovalRouteCase(context)}
        activeContext={context}
      />
    );

    const auditBoundary = screen.getByTestId("approval-audit-source-boundary");
    const unavailableState = screen.getByTestId("approval-audit-unavailable-state");
    const unavailableNotice = screen.getByTestId("audit-source-unavailable-notice");

    expect(auditBoundary).toHaveAttribute("data-source", "activeContext.audit_trail");
    expect(auditBoundary).toHaveAttribute("data-source-guard", "source-data-availability");
    expect(auditBoundary).toHaveAttribute("data-source-availability", "unavailable");
    expect(auditBoundary).toHaveAttribute("data-audit-source-state", "unavailable");
    expect(auditBoundary).toHaveAttribute("data-audit-count", "unknown");
    expect(unavailableState).toHaveAttribute("data-message-source", "ui_messages");
    expect(unavailableState).toHaveAttribute("data-source-state", "unavailable");
    expect(unavailableState).toHaveAttribute("data-coverage-upgrade", "not-suggested");
    expect(unavailableNotice).toHaveAttribute("data-message-source", "ui_messages");
    expect(unavailableNotice).toHaveTextContent(
      "Approval audit source is unavailable from governed ui_messages."
    );
    expect(unavailableState).not.toHaveTextContent(/coverage|upgrade|unlock|L3/i);
    expect(screen.queryByTestId("approval-audit-latest-id")).not.toBeInTheDocument();
    expect(screen.queryByTestId("approval-audit-derived-status")).not.toBeInTheDocument();
    expect(screen.queryByTestId("coverage-upgrade-prompt")).not.toBeInTheDocument();
  });

  it("renders AP-T02 P0 approval as readonly from the governed test harness only", () => {
    const context = buildP0ReadonlyApprovalTestHarnessContext();
    render(
      <ApprovalRouteShell
        activeCase={buildApprovalRouteCase(context)}
        activeContext={context}
      />
    );

    const surface = screen.getByTestId("approval-surface");
    const shell = screen.getByTestId("approval-shell-card");
    const statusPill = screen.getByTestId("approval-ar-status-pill");
    const auditBoundary = screen.getByTestId("approval-audit-source-boundary");

    expect(surface).toHaveAttribute("data-role", "P0");
    expect(surface).toHaveAttribute("data-approval-mode", "readonly-container");
    expect(surface).toHaveAttribute("data-authority-source", "resolved-surface-context");
    expect(surface).toHaveAttribute("data-route-authority", "resolved-surface-context");
    expect(surface).toHaveAttribute("data-approval-scope", "route-shell-guard-only");
    expect(statusPill).toHaveAttribute("data-ar-status", "PENDING_APPROVAL");
    expect(statusPill).toHaveAttribute("data-action-authority", "display-only");
    expect(statusPill).toHaveAttribute("data-mapping-source", "D-02");
    expect(statusPill).toHaveAttribute("data-state-migration", "none");
    expect(auditBoundary).toHaveAttribute("data-source", "activeContext.audit_trail");
    expect(auditBoundary).toHaveAttribute("data-display-mode", "display-only");
    expect(auditBoundary).toHaveAttribute("data-state-mutation", "none");
    expect(new Set(Object.values(context.action_permissions))).toEqual(new Set(["READONLY"]));
    expect(new Set(Object.values(context.resolved_visibility.allowed_actions ?? {}))).toEqual(
      new Set(["READONLY"])
    );
    expect(screen.queryByTestId("approval-cta-boundary")).not.toBeInTheDocument();
    expect(
      within(shell).queryByRole("button", { name: /approve|reject|delay|observe/i })
    ).not.toBeInTheDocument();
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(window.location.search).toBe("");
    expect(window.localStorage.getItem("role")).toBeNull();
    expect(window.localStorage.getItem("ar_status")).toBeNull();
    expect(window.sessionStorage.getItem("action_mode")).toBeNull();
    expect(document.body).not.toHaveTextContent(/IMMEDIATE|DELAYED|OBSERVE_ONLY/);
  });

  it("renders AP-T07 approved-pending execution as a locked semantic skeleton", async () => {
    const user = userEvent.setup();
    render(<App initialPhaseNumber={APPROVED_PENDING_EXECUTION_PHASE} />);

    await user.click(screen.getByRole("button", { name: /Approval Queue/i }));

    const surface = screen.getByTestId("approval-surface");
    const statusPill = screen.getByTestId("approval-ar-status-pill");
    const lockBoundary = screen.getByTestId("approval-lock-boundary");

    expect(surface).toHaveAttribute("data-role", "P2");
    expect(statusPill).toHaveAttribute("data-ar-status", "APPROVED_PENDING_EXECUTION");
    expect(lockBoundary).toHaveAttribute("data-ar-status", "APPROVED_PENDING_EXECUTION");
    expect(lockBoundary).toHaveAttribute("data-visual-state", "skeleton");
    expect(lockBoundary).toHaveAttribute("data-vf-12-state", "pending");
    expect(lockBoundary).toHaveAttribute("data-action-controls", "absent");
    expect(screen.queryByTestId("approval-cta-boundary")).not.toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /approve|reject|delay|observe|revoke|withdraw|reopen/i })
    ).not.toBeInTheDocument();
  });

  it("renders AP-T06A observation window as a read-only static skeleton", async () => {
    const user = userEvent.setup();
    render(<App initialPhaseNumber={OBSERVATION_WINDOW_PHASE} />);

    await user.click(screen.getByRole("button", { name: /Approval Queue/i }));

    const statusPill = screen.getByTestId("approval-ar-status-pill");
    const observationBoundary = screen.getByTestId("approval-observation-window-skeleton");

    expect(statusPill).toHaveAttribute("data-ar-status", "OBSERVATION_WINDOW");
    expect(observationBoundary).toHaveAttribute("data-ar-status", "OBSERVATION_WINDOW");
    expect(observationBoundary).toHaveAttribute("data-case-state", "OBSERVATION_WINDOW");
    expect(observationBoundary).toHaveAttribute("data-observation-window-readonly", "true");
    expect(observationBoundary).toHaveAttribute("data-timer-authority", "none");
    expect(observationBoundary).toHaveAttribute("data-state-sync", "mock-helper-only");
    expect(observationBoundary).toHaveAttribute("data-state-sync-source", "emitStateSync");
    expect(observationBoundary).toHaveAttribute("data-real-backend-protocol", "none");
    expect(observationBoundary).toHaveAttribute("data-state-migration", "none");
    expect(observationBoundary).toHaveAttribute("data-vf-11-state", "pass-input-skeleton-only");
    expect(screen.getByTestId("observation-window-banner")).toBeInTheDocument();
    expect(screen.getByTestId("observation-window-lock-badge")).toHaveTextContent(
      "Read-only until STATE_SYNC"
    );
    expect(screen.getByTestId("approval-audit-source-boundary"))
      .toHaveAttribute("data-derived-status", "OBSERVING");
    expect(screen.getByTestId("approval-audit-derived-status"))
      .toHaveAttribute("data-derived-status-source", "fixed-enum-mapping");
    expect(screen.getByTestId("approval-audit-observation-presence")).toHaveTextContent(
      "Present"
    );
    expect(screen.getByTestId("observation-window-total")).toHaveTextContent("60 min");
    expect(screen.getByTestId("observation-window-remaining")).toHaveTextContent("60 min");
    expect(screen.getByTestId("observation-expiry-action")).toHaveTextContent(
      "RETURN_TO_PENDING_APPROVAL"
    );
    expect(screen.queryByTestId("approval-cta-boundary")).not.toBeInTheDocument();
    for (const id of [
      "approve-mode-button",
      "reject-mode-button",
      "delay-decision-button",
      "observe-only-button",
      "view-details-button"
    ]) {
      expect(screen.getByTestId(id)).toBeDisabled();
      expect(screen.getByTestId(id)).toHaveAttribute("aria-disabled", "true");
    }
    expect(screen.getByTestId("view-details-button")).toHaveAttribute(
      "data-disabled-reason",
      "active-observation-window"
    );
  });

  it("requires mock STATE_SYNC rather than clock fast-forward to exit observation window", async () => {
    const user = userEvent.setup();
    render(<App initialPhaseNumber={OBSERVATION_WINDOW_PHASE} />);

    await user.click(screen.getByRole("button", { name: /Approval Queue/i }));

    act(() => {
      window.dispatchEvent(
        new CustomEvent("secupilot:mock-clock-fast-forward", {
          detail: { milliseconds: 60 * 60 * 1000 }
        })
      );
    });

    expect(screen.getByTestId("approval-observation-window-skeleton")).toHaveAttribute(
      "data-case-state",
      "OBSERVATION_WINDOW"
    );
    expect(screen.getByTestId("approval-ar-status-pill")).toHaveAttribute(
      "data-ar-status",
      "OBSERVATION_WINDOW"
    );
    expect(screen.queryByTestId("approval-lock-boundary")).not.toBeInTheDocument();

    emitMockStateSync({
      state_sync_source: "mock_state_sync",
      case_state: "PENDING_APPROVAL",
      ar_status: "PENDING_APPROVAL",
      action_mode: null,
      observation_window_remaining_minutes: 0,
      observation_expiry_action: "RETURN_TO_PENDING_APPROVAL",
      audit_event_id: "AUD-004",
      audit_event_type: "OBSERVATION_WINDOW_EXPIRED"
    });

    await waitFor(() =>
      expect(screen.getByTestId("approval-ar-status-pill")).toHaveAttribute(
        "data-ar-status",
        "PENDING_APPROVAL"
      )
    );
    expect(screen.queryByTestId("approval-observation-window-skeleton")).not.toBeInTheDocument();
    expect(screen.getByTestId("approval-cta-boundary")).toBeInTheDocument();
    expect(screen.getByTestId("observation-expired-notice")).toHaveAttribute(
      "data-state-sync-source",
      "mock_state_sync"
    );
    expect(screen.getByTestId("observation-expired-notice")).toHaveAttribute(
      "data-auto-execute",
      "absent"
    );
    expect(screen.getByTestId("audit-AUD-004")).toHaveTextContent("AUD-004");
    expect(screen.queryByTestId("approval-lock-boundary")).not.toBeInTheDocument();
    expect(screen.queryByTestId("auto-execute-label")).not.toBeInTheDocument();
    expect(screen.queryByTestId("auto-execution-progress")).not.toBeInTheDocument();
  });

  it("keeps AP static boundaries non-mutating for AP-T11A", async () => {
    const user = userEvent.setup();
    const pendingRender = render(<App initialPhaseNumber={2} />);

    await user.click(screen.getByRole("button", { name: /Approval Queue/i }));

    const ctaBoundary = screen.getByTestId("approval-cta-boundary");
    const auditBoundary = screen.getByTestId("approval-audit-source-boundary");

    expect(ctaBoundary).toHaveAttribute("data-state-mutation", "none");
    expect(auditBoundary).toHaveAttribute("data-display-mode", "display-only");
    expect(auditBoundary).toHaveAttribute("data-state-mutation", "none");
    const ctaButtons = within(ctaBoundary).queryAllByRole("button");
    expect(ctaButtons.length).toBeGreaterThan(0);
    for (const button of ctaButtons) {
      expect(button).toHaveAttribute("data-state-mutation", "none");
    }

    await user.click(screen.getByRole("button", { name: "Approve" }));

    const confirmDialog = screen.getByRole("dialog", { name: "Approve strong confirm" });
    expect(confirmDialog).toHaveAttribute("data-state-mutation", "none");
    expect(within(confirmDialog).getByTestId("approval-draft-confirm")).toBeDisabled();

    await user.click(within(confirmDialog).getByRole("button", { name: "Close" }));
    await user.click(screen.getByRole("button", { name: "Delay" }));

    const configDialog = screen.getByRole("dialog", { name: "Delay configuration" });
    expect(configDialog).toHaveAttribute("data-state-mutation", "none");
    expect(within(configDialog).getByTestId("approval-delay-observe-config-shell"))
      .toHaveAttribute("data-timer-authority", "none");
    expect(within(configDialog).getByTestId("approval-draft-confirm")).toBeDisabled();

    pendingRender.unmount();
    window.history.pushState({}, "", "/inbox");

    const observationRender = render(<App initialPhaseNumber={OBSERVATION_WINDOW_PHASE} />);

    await user.click(screen.getByRole("button", { name: /Approval Queue/i }));

    const observationBoundary = screen.getByTestId("approval-observation-window-skeleton");
    expect(observationBoundary).toHaveAttribute("data-state-sync", "mock-helper-only");
    expect(observationBoundary).toHaveAttribute("data-state-sync-source", "emitStateSync");
    expect(observationBoundary).toHaveAttribute("data-state-migration", "none");
    expect(observationBoundary).toHaveAttribute("data-timer-authority", "none");
    expect(screen.queryByTestId("approval-cta-boundary")).not.toBeInTheDocument();
    expect(screen.getByTestId("approval-audit-source-boundary"))
      .toHaveAttribute("data-state-mutation", "none");
    for (const id of [
      "approve-mode-button",
      "reject-mode-button",
      "delay-decision-button",
      "observe-only-button",
      "view-details-button"
    ]) {
      expect(screen.getByTestId(id)).toBeDisabled();
    }

    observationRender.unmount();
    window.history.pushState({}, "", "/inbox");

    render(<App initialPhaseNumber={APPROVED_PENDING_EXECUTION_PHASE} />);

    await user.click(screen.getByRole("button", { name: /Approval Queue/i }));

    expect(screen.getByTestId("approval-lock-boundary")).toHaveAttribute(
      "data-action-controls",
      "absent"
    );
    expect(screen.queryByTestId("approval-cta-boundary")).not.toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /approve|reject|delay|observe|revoke|withdraw|reopen/i })
    ).not.toBeInTheDocument();
  });

  it("hard redirects non-P2 approval route access without URL or storage authority", async () => {
    window.history.pushState({}, "", "/approval?role=P2&action_mode=IMMEDIATE");
    window.localStorage.setItem("role", "P2");
    window.sessionStorage.setItem("action_mode", "IMMEDIATE");

    render(<App />);

    await waitFor(() => expect(window.location.pathname).toBe("/inbox"));
    expect(screen.queryByTestId("approval-surface")).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /Approval Queue/i })).not.toBeInTheDocument();
    expect(screen.getByLabelText("Mock fixture resolved context")).toHaveTextContent("Role P1");
  });

  it("redirects P3 approval route access to manager path without manager content", async () => {
    window.history.pushState({}, "", "/approval");
    render(<App initialPhaseNumber={6} />);

    await waitFor(() => expect(window.location.pathname).toBe("/manager"));

    const surface = screen.getByTestId("approval-surface");
    const guard = screen.getByTestId("approval-route-guard");

    expect(surface).toHaveAttribute("data-role", "P3");
    expect(surface).toHaveAttribute("data-approval-scope", "route-shell-guard-only");
    expect(guard).toHaveAttribute("data-route-guard", "redirect-hard");
    expect(guard).toHaveAttribute("data-redirect-target", "/manager");
    expect(within(surface).queryByRole("button")).not.toBeInTheDocument();
    expect(screen.queryByTestId("manager-view-surface")).not.toBeInTheDocument();
  });

  it("opens the P2 Coverage & Health skeleton without live health behavior", async () => {
    const user = userEvent.setup();
    render(<App initialPhaseNumber={3} />);

    await user.click(screen.getByRole("button", { name: /Coverage & Health/i }));

    const surface = screen.getByTestId("coverage-health-surface");
    const contextSummary = screen.getByTestId("coverage-health-context-summary");
    const ceilingSlot = screen.getByTestId("coverage-health-ceiling-slot");
    const uiMessageSlot = screen.getByTestId("coverage-health-ui-message-slot");
    const sourceSlot = screen.getByTestId("coverage-health-source-slot");
    const regressionSlot = screen.getByTestId("coverage-health-regression-slot");

    expect(window.location.pathname).toBe("/coverage-health");
    expect(surface).toHaveAttribute("data-role", "P2");
    expect(surface).toHaveAttribute("data-authority-source", "resolved-surface-context");
    expect(surface).toHaveAttribute("data-route-authority", "role-filtered-nav");
    expect(surface).toHaveAttribute("data-vf-01-state", "pending");
    expect(surface).toHaveAttribute("data-visual-state", "skeleton");
    expect(surface).toHaveAttribute("data-live-health-source", "none");
    expect(contextSummary).toHaveTextContent("No runtime health endpoint or external source is queried");
    expect(screen.getByTestId("coverage-health-ceiling-value")).toHaveTextContent("L2");
    expect(screen.getByTestId("coverage-health-effective-value")).toHaveTextContent("L2");
    expect(screen.getByTestId("coverage-health-case-state")).toHaveTextContent(
      "Observation window"
    );
    expect(screen.getByTestId("coverage-health-fixture-freshness")).toHaveTextContent(
      "Mock fixture"
    );
    expect(ceilingSlot).toHaveAttribute("data-field", "case.coverage_level");
    expect(ceilingSlot).toHaveTextContent("does not unlock OFF fields");
    expect(uiMessageSlot).toHaveAttribute("data-rendering-state", "bounded-rendered");
    expect(uiMessageSlot).toHaveAttribute("data-message-source", "ui_messages");
    expect(uiMessageSlot).toHaveAttribute("data-message-count", "4");
    expect(screen.getAllByTestId("coverage-health-ui-message")).toHaveLength(4);
    expect(
      screen.getAllByText(
        "Resolved from fully artificial mock fixture; no URL, storage, real data, or deployment authority."
      )
    ).toHaveLength(2);
    expect(uiMessageSlot).not.toHaveTextContent("recommended_action");
    expect(sourceSlot).toHaveAttribute("data-source-health-mode", "ui_messages_semantic");
    expect(sourceSlot).toHaveAttribute("data-message-source", "ui_messages");
    expect(sourceSlot).toHaveAttribute("data-live-health-source", "none");
    expect(sourceSlot).toHaveAttribute("data-live-source-health", "not-implemented");
    expect(screen.getAllByTestId("coverage-health-source-message")).toHaveLength(2);
    expect(screen.getByTestId("coverage-health-source-boundary-note")).toHaveTextContent(
      "Semantic display only"
    );
    expect(regressionSlot).toHaveAttribute("data-cross-surface-hardening", "deferred");
    expect(within(surface).queryByRole("button")).not.toBeInTheDocument();
    expect(
      within(surface).queryByRole("button", { name: /approve|reject|delay|observe|close/i })
    ).not.toBeInTheDocument();
  });

  it("renders the VF-01 P0 Coverage & Health semantic frame from governed ui_messages", () => {
    const p0Context = buildP0CoverageHealthContext();
    const p0Case = {
      state: p0Context.case.case_state,
      freshness: "Mock fixture"
    } as Parameters<typeof CoverageHealthView>[0]["activeCase"];

    render(<CoverageHealthView activeCase={p0Case} activeContext={p0Context} />);

    const surface = screen.getByTestId("coverage-health-surface");
    const root = screen.getByTestId("coverage-health-root");
    const uiMessagePreview = screen.getByTestId("ui-message-preview");
    const missingSignalNotice = screen.getByTestId("missing-signal-notice");
    const confidenceNotice = screen.getByTestId("confidence-notice");
    const escalationHint = screen.getByTestId("escalation-hint");
    const sourceSlot = screen.getByTestId("coverage-health-source-slot");

    expect(surface).toHaveAttribute("data-role", "P0");
    expect(surface).toHaveAttribute("data-authority-source", "resolved-surface-context");
    expect(surface).toHaveAttribute("data-vf-01-state", "baseline-reconciled");
    expect(surface).toHaveAttribute("data-visual-state", "semantic-frame");
    expect(surface).toHaveAttribute("data-live-health-source", "none");
    expect(root).toHaveAttribute("data-current-coverage", "L2");
    expect(root).toHaveAttribute("data-frame-scope", "vf-01-p0-semantic");
    expect(screen.getByTestId("current-coverage-level")).toHaveTextContent("L2");
    expect(screen.getByTestId("field-presence-rate")).toHaveTextContent("2/7");
    expect(screen.getByTestId("join-health-rate")).toHaveTextContent("Live joins are not queried");
    expect(screen.getByTestId("data-freshness-indicator")).toHaveTextContent("Mock fixture");
    expect(screen.getByTestId("capability-tier-reference")).toHaveTextContent(
      "Coverage level remains a hard ceiling"
    );
    expect(screen.getByTestId("field-switch-matrix")).toHaveTextContent("OFF");
    expect(screen.getByTestId("capability-package-list")).toHaveTextContent(
      "No frontend unlock package is created"
    );
    expect(uiMessagePreview).toHaveAttribute("data-message-source", "ui_messages");
    expect(missingSignalNotice).toHaveAttribute("data-message-source", "ui_messages");
    expect(missingSignalNotice).toHaveAttribute("data-ui-message-key", "mock_only_notice");
    expect(confidenceNotice).toHaveAttribute("data-message-source", "ui_messages");
    expect(confidenceNotice).toHaveAttribute("data-ui-message-key", "fixture_status");
    expect(escalationHint).toHaveAttribute("data-message-source", "ui_messages");
    expect(escalationHint).toHaveAttribute("data-ui-message-key", "expected_ui");
    expect(sourceSlot).toHaveAttribute("data-health-slot", "source-health");
    expect(sourceSlot).toHaveAttribute("data-source-health-mode", "ui_messages_semantic");
    expect(sourceSlot).toHaveAttribute("data-message-source", "ui_messages");
    expect(sourceSlot).toHaveAttribute("data-live-health-source", "none");
    expect(sourceSlot).toHaveTextContent("Governed semantic display");
    expect(sourceSlot).not.toHaveTextContent(
      /current connection normal|realtime source health|live telemetry|runtime readiness|backend health truth/i
    );
    expect(screen.queryByTestId("hardcoded-unlock-copy")).not.toBeInTheDocument();
    expect(screen.queryByTestId("frontend-generated-upgrade-copy")).not.toBeInTheDocument();
    expect(screen.queryByTestId("coverage-upgrade-prompt")).not.toBeInTheDocument();
    expect(screen.queryByTestId("real-data-sample-row")).not.toBeInTheDocument();
    expect(screen.queryByTestId("secret-or-connector-config")).not.toBeInTheDocument();
    expect(within(surface).queryByRole("button")).not.toBeInTheDocument();
  });

  it("renders P1 expert mode as an inert restricted skeleton", () => {
    render(<App />);

    const expertFrame = screen.getByTestId("vf-03-expert-mode-frame");
    const expertEntry = screen.getByTestId("expert-mode-entry");
    const expertToggle = screen.getByTestId("expert-mode-toggle");
    const onExample = screen.getByTestId("expert-mode-on-example");

    expect(expertFrame).toHaveAttribute("data-testid", "vf-03-expert-mode-frame");
    expect(expertFrame).toHaveAttribute("data-expert-mode", "false");
    expect(expertFrame).toHaveAttribute("data-case-state", "UNDER_INVESTIGATION");
    expect(expertFrame).toHaveAttribute("data-coverage-level", "L2");
    expect(expertFrame).toHaveAttribute("data-role", "P1");
    expect(expertFrame).toHaveAttribute("data-expert-mode-state", "p1_restricted");
    expect(expertFrame).toHaveAttribute("data-authority-source", "resolved-surface-context");
    expect(expertFrame).toHaveAttribute("data-action-state", "not-implemented");
    expect(expertFrame).toHaveAttribute("data-visual-state", "skeleton");
    expect(expertEntry).toHaveAttribute("data-expert-mode", "false");
    expect(expertToggle).toHaveAttribute("aria-pressed", "false");
    expect(expertToggle).toHaveAttribute("data-role-variant", "P1_RESTRICTED");
    expect(expertToggle).toHaveAttribute("data-action-state", "inert");
    expect(expertFrame).toHaveTextContent("P1 remains limited to the current L2 field set");
    expect(expertFrame).toHaveTextContent("No route, permission upgrade, coverage bypass");
    expect(screen.getByTestId("lineage-confidence")).toHaveAttribute(
      "data-switch-state",
      "DEGRADED"
    );
    expect(onExample).toHaveAttribute("data-expert-mode", "true");
    expect(screen.getByTestId("expert-mode-active-banner")).toBeInTheDocument();
    expect(screen.getByTestId("expert-field-confidence-breakdown")).toHaveAttribute(
      "data-switch-state",
      "ON"
    );
    expect(screen.getByTestId("lineage-confidence-expert")).toHaveAttribute(
      "data-switch-state",
      "DEGRADED"
    );
    expect(screen.queryByTestId("expert-mode-unlock-off-field")).not.toBeInTheDocument();
    expect(screen.queryByTestId("coverage-upgrade-prompt")).not.toBeInTheDocument();
    expect(screen.queryByTestId("blast-radius-expert-unlock")).not.toBeInTheDocument();
  });

  it("keeps the P2 expert mode entry as skeleton-only and omits it for P3", () => {
    const { unmount } = render(<App initialPhaseNumber={3} />);

    const p2ExpertFrame = screen.getByTestId("vf-03-expert-mode-frame");
    const p2ExpertEntry = screen.getByTestId("expert-mode-entry");
    const p2ExpertToggle = screen.getByTestId("expert-mode-toggle");
    expect(p2ExpertFrame).toHaveAttribute("data-role", "P2");
    expect(p2ExpertFrame).toHaveAttribute("data-expert-mode", "false");
    expect(p2ExpertFrame).toHaveAttribute("data-expert-mode-state", "entry_skeleton");
    expect(p2ExpertToggle).toHaveAttribute("data-role-variant", "P2_TOGGLEABLE");
    expect(p2ExpertEntry).toHaveTextContent("P2 skeleton");

    unmount();
    render(<App initialPhaseNumber={6} />);

    expect(screen.queryByTestId("vf-03-expert-mode-frame")).not.toBeInTheDocument();
    expect(screen.queryByTestId("expert-mode-entry")).not.toBeInTheDocument();
    expect(screen.queryByTestId("expert-mode-toggle")).not.toBeInTheDocument();
    expect(screen.getByLabelText("Mock fixture resolved context")).toHaveTextContent("Role P3");
    expect(screen.queryByRole("button", { name: /Coverage & Health/i })).not.toBeInTheDocument();
  });

  it("guards manual Coverage & Health route access for P3 without rendering operations", () => {
    window.history.pushState({}, "", "/coverage-health");

    render(<App initialPhaseNumber={6} />);

    const surface = screen.getByTestId("coverage-health-surface");
    const guard = screen.getByTestId("coverage-health-route-guard");

    expect(surface).toHaveAttribute("data-role", "P3");
    expect(surface).toHaveAttribute("data-visual-state", "skeleton");
    expect(guard).toHaveAttribute("data-route-guard", "role-not-eligible");
    expect(guard).toHaveTextContent("not exposed for this role");
    expect(within(surface).queryByRole("button")).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /Coverage & Health/i })).not.toBeInTheDocument();
  });

  it("resolves the history route through clamp-first guard without URL or storage authority", () => {
    window.history.pushState({}, "", "/search?tab=history&coverage=L3&role=P3&focus=raw_technical");
    window.localStorage.setItem("role", "P3");
    window.sessionStorage.setItem("coverage", "L3");

    render(<App />);

    const historySurface = screen.getByTestId("history-surface");
    const routeGuard = screen.getByTestId("history-route-guard");
    const focusScopes = screen.getByTestId("history-focus-scopes");
    const scopeItems = screen.getAllByTestId("history-focus-scope");
    const historicalListItem = within(historySurface).getByTestId("historical-case-list-item");
    const coverageLabels = screen.getByTestId("dual-coverage-label-block");
    const structuralEmptyState = screen.getByTestId("structural-empty-state");
    const degradedEmptyState = screen.getByTestId("degraded-empty-state");
    const approvalAuditAnchor = screen.getByTestId("view-approval-audit");

    expect(screen.getByRole("heading", { name: "History guard" })).toBeInTheDocument();
    expect(routeGuard).toHaveAttribute("data-route-order", "resolve-clamp-guard-render");
    expect(routeGuard).toHaveAttribute("data-authority-source", "resolved-surface-context");
    expect(routeGuard).toHaveAttribute("data-requested-coverage", "L3");
    expect(routeGuard).toHaveAttribute("data-current-coverage", "L3");
    expect(routeGuard).toHaveAttribute("data-recorded-coverage", "L2");
    expect(routeGuard).toHaveAttribute("data-effective-coverage", "L2");
    expect(coverageLabels).toHaveAttribute("data-recorded-coverage", "L2");
    expect(coverageLabels).toHaveAttribute("data-current-coverage", "L3");
    expect(coverageLabels).toHaveAttribute("data-effective-visibility", "L2");
    expect(screen.getByTestId("recorded-coverage-label")).toHaveTextContent("Recorded: L2");
    expect(screen.getByTestId("current-coverage-label")).toHaveTextContent("Current: L3");
    expect(screen.getByTestId("effective-visibility-label")).toHaveTextContent("Effective: L2");
    expect(screen.getByTestId("clamp-reason")).toHaveTextContent(
      "recorded = L2 · current = L3 · effective = L2"
    );
    expect(screen.getByTestId("missing-signal-notice")).toHaveAttribute(
      "data-message-source",
      "ui_messages"
    );
    expect(screen.getByTestId("historical-upgrade-blocked-notice")).toHaveTextContent(
      /history integrity protection/i
    );
    expect(structuralEmptyState).toHaveAttribute("data-empty-state-kind", "structural");
    expect(structuralEmptyState).toHaveAttribute(
      "data-empty-state-status",
      "not-current-result"
    );
    expect(structuralEmptyState).toHaveAttribute("data-message-source", "ui_messages");
    expect(structuralEmptyState).toHaveTextContent(/No matching historical case/i);
    expect(structuralEmptyState).not.toHaveTextContent(/^No data$/i);
    expect(degradedEmptyState).toHaveAttribute("data-empty-state-kind", "degraded");
    expect(degradedEmptyState).toHaveAttribute("data-empty-state-status", "active");
    expect(degradedEmptyState).toHaveAttribute("data-message-source", "ui_messages");
    expect(degradedEmptyState).toHaveAttribute("data-effective-visibility", "L2");
    expect(degradedEmptyState).toHaveTextContent(/coverage clamp/i);
    expect(degradedEmptyState).not.toHaveTextContent(/^No data$/i);
    expect(degradedEmptyState).not.toHaveTextContent(/No matching historical case/i);
    expect(focusScopes).toHaveAttribute("data-focus-authority", "hint-only");
    expect(focusScopes).toHaveAttribute("data-requested-focus", "raw_technical");
    expect(focusScopes).toHaveAttribute("data-effective-focus", "summary");
    expect(scopeItems).toHaveLength(3);
    expect(scopeItems.map((item) => item.getAttribute("data-focus-scope"))).toEqual([
      "summary",
      "approval_audit",
      "history_audit"
    ]);
    expect(scopeItems.map((item) => item.textContent)).toEqual([
      "SummaryRead-only case summary and guard facts.",
      "Approval auditRead-only approval-audit focus; no approval controls are attached.",
      "History auditRead-only historical audit focus with recorded coverage preserved."
    ]);
    expect(scopeItems[0]).toHaveAttribute("aria-current", "true");
    expect(historicalListItem).toHaveAttribute("data-list-item-context", "summary-only");
    expect(historicalListItem).toHaveAttribute("data-detail-context-authority", "case-route");
    expect(historicalListItem).toHaveAttribute("data-effective-visibility-owned-by", "case-detail");
    expect(historicalListItem).toHaveAttribute("data-current-coverage", "L3");
    expect(historicalListItem).toHaveAttribute("data-effective-visibility", "L2");
    expect(historicalListItem).toHaveAttribute("data-handoff-state", "not-implemented");
    expect(historicalListItem).toHaveAttribute("data-visual-state", "skeleton");
    expect(historicalListItem).toHaveAttribute(
      "data-frame-state",
      "hf-sh-01-02-vf14-v0-2-pass"
    );
    expect(historicalListItem).toHaveAttribute("data-recorded-coverage", "L2");
    expect(historicalListItem).toHaveAttribute("data-current-visible", "L2");
    expect(within(historicalListItem).getByTestId("historical-list-case-id")).toHaveTextContent("CASE-2847");
    expect(within(historicalListItem).getByTestId("historical-list-verdict")).toHaveTextContent(
      "HIGH mock case"
    );
    expect(within(historicalListItem).getByTestId("historical-list-snippet")).toHaveTextContent(
      /Mock fixture/i
    );
    expect(within(historicalListItem).getByTestId("historical-list-timestamp")).toHaveAttribute(
      "data-timestamp-state",
      "unavailable"
    );
    expect(within(historicalListItem).getByTestId("historical-list-recorded-coverage")).toHaveTextContent("L2");
    expect(within(historicalListItem).getByTestId("historical-list-current-visible")).toHaveTextContent("L2");
    expect(within(historicalListItem).getByTestId("historical-list-boundary")).toHaveTextContent(
      /detail visibility resolves after a future case-route handoff/i
    );
    expect(approvalAuditAnchor).toHaveAttribute("data-source", "history");
    expect(approvalAuditAnchor).toHaveAttribute("data-guard", "role-source-data");
    expect(approvalAuditAnchor).toHaveAttribute("data-state-mutation", "none");
    expect(screen.getByLabelText("Coverage level")).toHaveTextContent("Coverage L2");
    expect(screen.getByLabelText("Mock fixture resolved context")).toHaveTextContent("Role P1");
    expect(within(historySurface).getByTestId("history-write-guard")).toHaveTextContent(
      /No write actions are attached/i
    );
    expect(
      within(historySurface).queryByRole("button", { name: /approve|reject|delay|observe|close/i })
    ).not.toBeInTheDocument();
    expect(screen.queryByTestId("host-raw-evidence")).not.toBeInTheDocument();
    expect(screen.queryByTestId("coverage-upgrade-unlock")).not.toBeInTheDocument();
    expect(screen.queryByTestId("historical-field-upgrade-banner")).not.toBeInTheDocument();
  });

  it("downgrades P1 approval audit focus to summary without creating authority", () => {
    window.history.pushState({}, "", "/search?tab=history&focus=approval_audit");

    render(<App />);

    const focusScopes = screen.getByTestId("history-focus-scopes");
    const summaryScope = screen
      .getAllByTestId("history-focus-scope")
      .find((item) => item.getAttribute("data-focus-scope") === "summary");
    const downgrade = screen.getByTestId("history-focus-downgrade");

    expect(focusScopes).toHaveAttribute("data-requested-focus", "approval_audit");
    expect(focusScopes).toHaveAttribute("data-effective-focus", "summary");
    expect(summaryScope).toHaveAttribute("aria-current", "true");
    expect(downgrade).toHaveAttribute("data-requested-focus", "approval_audit");
    expect(downgrade).toHaveAttribute("data-effective-focus", "summary");
    expect(focusScopes).toHaveTextContent("Focus is a display hint only");
    expect(focusScopes).toHaveTextContent("no approval controls are attached");
    expect(screen.getByLabelText("Mock fixture resolved context")).toHaveTextContent("Role P1");
    expect(screen.getByLabelText("Coverage level")).toHaveTextContent("Coverage L2");
    expect(screen.queryByTestId("search-history-approval-audit-boundary")).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /approve|reject|delay|observe|close/i })).not.toBeInTheDocument();
  });

  it("downgrades P1 history audit focus without creating write authority", () => {
    window.history.pushState({}, "", "/search?tab=history&focus=history_audit");

    render(<App />);

    const focusScopes = screen.getByTestId("history-focus-scopes");
    const summaryScope = screen
      .getAllByTestId("history-focus-scope")
      .find((item) => item.getAttribute("data-focus-scope") === "summary");

    expect(focusScopes).toHaveAttribute("data-requested-focus", "history_audit");
    expect(focusScopes).toHaveAttribute("data-effective-focus", "summary");
    expect(summaryScope).toHaveAttribute("aria-current", "true");
    expect(screen.getByTestId("history-focus-downgrade")).toHaveAttribute(
      "data-requested-focus",
      "history_audit"
    );
    expect(screen.getByTestId("history-write-guard")).toHaveTextContent(
      "Read-only history surface. No write actions are attached."
    );
    expect(screen.queryByTestId("search-history-approval-audit-boundary")).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /approve|reject|delay|observe|close/i })).not.toBeInTheDocument();
  });

  it("routes P3 audit focus to Manager View without serialized handoff authority", async () => {
    const user = userEvent.setup();
    window.history.pushState({}, "", "/search?tab=history&focus=approval_audit");

    render(<App initialPhaseNumber={6} />);

    const handoff = screen.getByTestId("manager-deep-link-handoff");
    const auditBoundary = screen.getByTestId("search-history-approval-audit-boundary");

    expect(auditBoundary).toHaveAttribute("data-role", "P3");
    expect(auditBoundary).toHaveAttribute("data-source", "activeContext.audit_trail");
    expect(auditBoundary).toHaveAttribute("data-source-surface", "history");
    expect(auditBoundary).toHaveAttribute("data-source-order", "AP-T08-before-SH-T08");
    expect(auditBoundary).toHaveAttribute("data-display-mode", "read-only-summary");
    expect(auditBoundary).toHaveAttribute("data-full-audit-chain", "not-rendered");
    expect(auditBoundary).toHaveAttribute("data-state-mutation", "none");
    expect(screen.getByTestId("history-approval-audit-latest-id")).toHaveTextContent("AUD-005");
    expect(screen.getByTestId("history-approval-audit-latest-event")).toHaveTextContent(
      "APPROVED_AFTER_WINDOW"
    );
    expect(screen.getByTestId("history-approval-audit-actor-role")).toHaveTextContent("P2");
    expect(screen.getByTestId("history-approval-audit-derived-status")).toHaveAttribute(
      "data-derived-status",
      "APPROVED"
    );
    expect(screen.getByTestId("history-approval-audit-observation-presence")).toHaveTextContent(
      "Present"
    );
    expect(screen.getByTestId("history-approval-audit-terminal-close")).toHaveTextContent(
      "Unavailable"
    );
    expect(handoff).toHaveAttribute("data-authority-source", "resolved-surface-context");
    expect(handoff).toHaveAttribute("data-source-surface", "P3_SEARCH_HISTORY");
    expect(handoff).toHaveAttribute("data-source-focus", "approval_audit");
    expect(handoff).toHaveAttribute("data-target-route", "/manager");
    expect(handoff).toHaveAttribute("data-handoff-payload", "none");
    expect(handoff).toHaveAttribute("data-url-authority", "none");
    expect(handoff).toHaveAttribute("data-storage-authority", "none");
    expect(screen.queryByTestId("manager-view-surface")).not.toBeInTheDocument();

    await user.click(screen.getByTestId("manager-deep-link-button"));

    const managerSurface = screen.getByTestId("manager-view-surface");

    expect(window.location.pathname).toBe("/manager");
    expect(window.location.search).toBe("");
    expect(managerSurface).toHaveAttribute("data-authority-source", "resolved-surface-context");
    expect(managerSurface).toHaveAttribute("data-handoff-payload", "none");
    expect(screen.getByTestId("manager-readonly-boundary")).toHaveAttribute(
      "data-deep-link-handoff",
      "route-only"
    );
    expect(screen.getByTestId("manager-audit-boundary")).toHaveAttribute(
      "data-approval-audit-summary",
      "implemented"
    );
    const managerAuditSummary = screen.getByTestId("manager-approval-audit-summary");
    expect(managerAuditSummary).toHaveAttribute("data-role", "P3");
    expect(managerAuditSummary).toHaveAttribute("data-source", "activeContext.audit_trail");
    expect(managerAuditSummary).toHaveAttribute("data-display-mode", "read-only-summary");
    expect(managerAuditSummary).toHaveAttribute("data-state-mutation", "none");
    expect(managerAuditSummary).toHaveAttribute(
      "data-derived-status-source",
      "fixed-enum-mapping"
    );
    expect(managerAuditSummary).toHaveAttribute("data-derived-status", "APPROVED");
    expect(managerAuditSummary).toHaveAttribute("data-full-audit-chain", "not-rendered");
    expect(managerAuditSummary).toHaveAttribute("data-p0-p2-placeholders", "absent");
    expect(screen.getByTestId("manager-approval-audit-latest-id")).toHaveTextContent("AUD-005");
    expect(screen.getByTestId("manager-approval-audit-latest-event")).toHaveTextContent(
      "APPROVED_AFTER_WINDOW"
    );
    expect(screen.getByTestId("manager-approval-audit-actor-role")).toHaveTextContent("P2");
    expect(screen.getByTestId("manager-approval-audit-derived-status")).toHaveAttribute(
      "data-derived-status",
      "APPROVED"
    );
    expect(screen.getByTestId("manager-approval-audit-ar-status-after")).toHaveTextContent(
      "APPROVED_PENDING_EXECUTION"
    );
    expect(screen.getByTestId("manager-approval-audit-case-state-after")).toHaveTextContent(
      "APPROVED_PENDING_EXECUTION"
    );
    expect(screen.getByTestId("manager-approval-audit-observation-presence")).toHaveTextContent(
      "Present"
    );
    expect(screen.queryByTestId("full-audit-trail")).not.toBeInTheDocument();
    expect(screen.queryByTestId("host-raw-evidence")).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /approve|reject|delay|observe|close/i }))
      .not.toBeInTheDocument();
  });

  it("exposes the same route-only Manager handoff for P3 history audit focus", () => {
    window.history.pushState({}, "", "/search?tab=history&focus=history_audit");

    render(<App initialPhaseNumber={6} />);

    const handoff = screen.getByTestId("manager-deep-link-handoff");

    expect(handoff).toHaveAttribute("data-source-focus", "history_audit");
    expect(handoff).toHaveAttribute("data-target-route", "/manager");
    expect(handoff).toHaveAttribute("data-handoff-payload", "none");
    expect(handoff).toHaveAttribute("data-url-authority", "none");
    expect(handoff).toHaveAttribute("data-storage-authority", "none");
  });

  it("does not expose Manager handoff outside P3 audit focus", () => {
    window.history.pushState({}, "", "/search?tab=history&focus=summary");

    render(<App initialPhaseNumber={6} />);

    expect(screen.getByTestId("history-focus-scopes")).toHaveAttribute(
      "data-effective-focus",
      "summary"
    );
    expect(screen.queryByTestId("manager-deep-link-handoff")).not.toBeInTheDocument();
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
    expect(screen.getByTestId("inbox-surface")).toHaveAttribute("data-role", "P1");
    expect(screen.getByTestId("inbox-surface")).toHaveAttribute("data-inbox-mode", "case-first");
    expect(screen.getByTestId("case-first-inbox-list")).toBeInTheDocument();
    expect(screen.getAllByRole("button", { name: /Open case/i })).toHaveLength(1);
    expect(document.body).not.toHaveTextContent(/work queue|current case queue|approval queue/i);
    expect(screen.queryByTestId("inbox-approval-navigation-entry-CASE-2847"))
      .not.toBeInTheDocument();

    await user.click(screen.getAllByRole("button", { name: /Open case/i })[0]);

    expect(window.location.pathname).toBe("/case/CASE-2847");
    expect(screen.getByText("CASE-2847")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: /HIGH mock case/i })).toBeInTheDocument();
  });

  it("offers P2 Inbox approval navigation without carrying approval authority", async () => {
    const user = userEvent.setup();
    render(<App initialPhaseNumber={2} />);

    const inboxSurface = screen.getByTestId("inbox-surface");
    const entry = screen.getByTestId("inbox-approval-navigation-entry-CASE-2847");
    const button = screen.getByTestId("inbox-approval-navigation-button-CASE-2847");

    expect(inboxSurface).toHaveAttribute("data-role", "P2");
    expect(inboxSurface).toHaveAttribute("data-action-authority", "none");
    expect(entry).toHaveAttribute("data-ar-hint-mode", "display-only");
    expect(entry).toHaveAttribute("data-ar-status-display", "Pending approval");
    expect(entry).toHaveAttribute("data-action-mode", "none");
    expect(entry).toHaveAttribute("data-state-mutation", "none");
    expect(entry).toHaveAttribute("data-approval-authority-transfer", "none");
    expect(entry).toHaveAttribute("data-target-route", "/approval");
    expect(button).toHaveAttribute("data-authority-payload", "none");
    expect(entry).not.toHaveTextContent(/IMMEDIATE|DELAYED|OBSERVE_ONLY/);

    await user.click(button);

    expect(window.location.pathname).toBe("/approval");
    expect(window.location.search).toBe("");
    expect(window.localStorage.getItem("role")).toBeNull();
    expect(window.sessionStorage.getItem("action_mode")).toBeNull();
    expect(screen.getByTestId("approval-surface")).toBeInTheDocument();
  });

  it("renders the P3 inbox as a read-only skeleton without operation affordance", () => {
    render(<App initialPhaseNumber={6} />);

    const inboxSurface = screen.getByTestId("inbox-surface");
    const readonlyVariant = screen.getByTestId("p3-readonly-inbox-variant");
    const readonlyCard = screen.getByTestId("p3-readonly-inbox-card-CASE-2847");
    const readonlyNotice = screen.getByTestId("p3-readonly-inbox-notice-CASE-2847");

    expect(inboxSurface).toHaveAttribute("data-role", "P3");
    expect(inboxSurface).toHaveAttribute("data-inbox-mode", "readonly");
    expect(readonlyCard).toHaveAttribute("data-authority-source", "resolved-surface-context");
    expect(readonlyCard).toHaveAttribute("data-visual-state", "skeleton");
    expect(readonlyCard).toHaveAttribute("data-work-queue-affordance", "absent");
    expect(screen.getByTestId("p3-readonly-inbox-case-id-CASE-2847")).toHaveTextContent(
      "CASE-2847"
    );
    expect(screen.getByTestId("p3-readonly-inbox-coverage-CASE-2847")).toHaveTextContent("L2");
    expect(screen.getByTestId("p3-readonly-inbox-case-state-CASE-2847")).toHaveTextContent(
      "Approved pending execution"
    );
    expect(readonlyNotice).toHaveTextContent(/P3 readonly skeleton/i);
    expect(within(readonlyVariant).queryByRole("button")).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /Open case/i })).not.toBeInTheDocument();
    expect(
      within(readonlyVariant).queryByRole("button", {
        name: /approve|reject|delay|observe|close/i
      })
    ).not.toBeInTheDocument();
  });

  it("opens the P3 Manager View as an independent read-only structure", async () => {
    const user = userEvent.setup();
    render(<App initialPhaseNumber={6} />);

    await user.click(screen.getByRole("button", { name: /Manager View/i }));

    const surface = screen.getByTestId("manager-view-surface");
    const scopeRail = screen.getByTestId("manager-scope-rail");
    const narrative = screen.getByTestId("manager-brief-narrative");
    const summary = screen.getByTestId("manager-context-summary");
    const dialogueDock = screen.getByTestId("manager-dialogue-dock");

    expect(window.location.pathname).toBe("/manager");
    expect(surface).toHaveAttribute("data-role", "P3");
    expect(surface).toHaveAttribute("data-authority-source", "resolved-surface-context");
    expect(surface).toHaveAttribute("data-manager-scope", "mv-t01-mv-t04-readonly-summary");
    expect(surface).toHaveAttribute("data-p0-p2-placeholders", "absent");
    expect(scopeRail).toHaveTextContent("Manager Scope");
    expect(narrative).toHaveTextContent("WHAT");
    expect(narrative).toHaveTextContent("HONESTY");
    expect(summary).toHaveTextContent("Context Summary");
    expect(dialogueDock).toHaveAttribute("data-chip-source", "runtime-only");
    expect(screen.getByTestId("manager-readonly-badge")).toHaveAttribute(
      "data-workflow-authority",
      "none"
    );
    expect(screen.getByTestId("manager-audit-boundary")).toHaveAttribute(
      "data-approval-audit-summary",
      "implemented"
    );
    expect(screen.getByTestId("manager-approval-audit-summary")).toHaveAttribute(
      "data-source",
      "activeContext.audit_trail"
    );
    expect(screen.getByTestId("manager-approval-audit-summary")).toHaveAttribute(
      "data-state-mutation",
      "none"
    );
    expect(within(surface).queryByRole("button", { name: /approve|reject|delay|observe/i }))
      .not.toBeInTheDocument();
    expect(screen.queryByTestId("host-raw-evidence")).not.toBeInTheDocument();
  });

  it("renders Manager KPI shells without frontend-inferred metric values", () => {
    window.history.pushState({}, "", "/manager");

    render(<App initialPhaseNumber={6} />);

    expect(screen.getByTestId("manager-kpi-card-coverage")).toHaveAttribute(
      "data-kpi-source",
      "resolved-surface-context"
    );
    expect(screen.getByTestId("manager-kpi-card-coverage")).toHaveTextContent("L2");

    for (const testId of [
      "manager-kpi-card-mtta",
      "manager-kpi-card-noise-compression",
      "manager-kpi-card-approval-throughput"
    ]) {
      const card = screen.getByTestId(testId);
      expect(card).toHaveAttribute("data-kpi-source", "data-unavailable");
      expect(card).toHaveTextContent("—");
    }

    expect(document.body).not.toHaveTextContent(/MTTR|ROI 10|queue count|完全受控|已彻底消除/i);
  });

  it("does not let URL or storage create Manager View authority", async () => {
    window.history.pushState({}, "", "/manager?role=P3");
    window.localStorage.setItem("role", "P3");
    window.sessionStorage.setItem("surface", "P3_MANAGER");

    render(<App />);

    await waitFor(() => expect(window.location.pathname).toBe("/inbox"));

    expect(screen.getByTestId("inbox-surface")).toHaveAttribute("data-role", "P1");
    expect(screen.queryByTestId("manager-route-guard")).not.toBeInTheDocument();
    expect(screen.queryByTestId("manager-view-surface")).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /Manager View/i })).not.toBeInTheDocument();
  });

  it("keeps P0/P2 Manager entry denied without degraded Manager variants", async () => {
    window.history.pushState({}, "", "/manager?role=P3");
    window.localStorage.setItem("manager_state", "P3_MANAGER");
    window.sessionStorage.setItem("manager_handoff", "approval_audit");

    render(<App initialPhaseNumber={2} />);

    await waitFor(() => expect(window.location.pathname).toBe("/approval"));

    expect(screen.getByTestId("approval-surface")).toBeInTheDocument();
    expect(screen.queryByTestId("manager-view-surface")).not.toBeInTheDocument();
    expect(screen.queryByTestId("manager-approval-audit-summary")).not.toBeInTheDocument();
    expect(screen.queryByTestId("host-raw-evidence")).not.toBeInTheDocument();
    expect(document.body).not.toHaveTextContent(/P0 readonly manager|P2 readonly manager/i);

    const p0Context = buildP0CoverageHealthContext();
    const p0Case = buildApprovalRouteCase(p0Context);
    const onRouteRedirect = vi.fn();

    render(
      <ManagerView
        activeCase={p0Case}
        activeContext={p0Context}
        onRouteRedirect={onRouteRedirect}
      />
    );

    const p0Guard = screen.getAllByTestId("manager-route-guard").at(-1);
    expect(p0Guard).toHaveAttribute("data-role", "P0");
    expect(p0Guard).toHaveAttribute("data-manager-entry", "denied");
    expect(p0Guard).toHaveAttribute("data-redirect-target", "/inbox");
    expect(p0Guard).toHaveAttribute("data-manager-state-transfer", "none");
    expect(p0Guard).toHaveAttribute("data-p0-p2-placeholders", "absent");
    await waitFor(() => expect(onRouteRedirect).toHaveBeenCalledWith("inbox"));
  });

  it("maps case AR status through D-02 display semantics without state migration", () => {
    window.history.pushState({}, "", "/case/CASE-2847");

    render(<App initialPhaseNumber={2} />);

    const actionPanel = screen.getByTestId("action-request-panel");
    const statusPill = screen.getByTestId("ar-status-pill");

    expect(statusPill).toHaveAttribute("data-ar-status", "PENDING_APPROVAL");
    expect(statusPill).toHaveAttribute("data-action-authority", "p2-only");
    expect(statusPill).toHaveAttribute("data-interaction-class", "non-terminal");
    expect(statusPill).toHaveAttribute("data-mapping-source", "D-02");
    expect(statusPill).toHaveAttribute("data-state-migration", "none");
    expect(within(actionPanel).queryByRole("button", { name: /approve|reject|delay|observe/i }))
      .not.toBeInTheDocument();
  });

  it("keeps non-pending AR statuses display-only in case detail", () => {
    window.history.pushState({}, "", "/case/CASE-2847");

    render(<App initialPhaseNumber={5} />);

    const actionPanel = screen.getByTestId("action-request-panel");
    const statusPill = screen.getByTestId("ar-status-pill");

    expect(statusPill).toHaveAttribute("data-ar-status", "APPROVED_PENDING_EXECUTION");
    expect(statusPill).toHaveAttribute("data-action-authority", "display-only");
    expect(statusPill).toHaveAttribute("data-interaction-class", "terminal");
    expect(statusPill).toHaveAttribute("data-state-migration", "none");
    expect(within(actionPanel).queryByRole("button", { name: /approve|reject|delay|observe/i }))
      .not.toBeInTheDocument();
  });

  it("renders CD-T06A observation-window state header skeleton without CLOSED claim", () => {
    window.history.pushState({}, "", "/case/CASE-2847");

    render(<App initialPhaseNumber={3} />);

    const statePill = screen.getByTestId("case-state-pill");
    const stateHeader = screen.getByTestId("case-state-header-skeleton");

    expect(statePill).toHaveAttribute("data-case-state", "OBSERVATION_WINDOW");
    expect(statePill).toHaveAttribute("data-closed-behavior", "not-claimed");
    expect(stateHeader).toHaveAttribute("data-case-state", "OBSERVATION_WINDOW");
    expect(stateHeader).toHaveAttribute("data-ar-status", "OBSERVATION_WINDOW");
    expect(stateHeader).toHaveAttribute("data-visual-frame", "VF-11");
    expect(stateHeader).toHaveAttribute("data-lock-state", "readonly-observation");
    expect(stateHeader).toHaveAttribute("data-state-mutation", "none");
    expect(stateHeader).toHaveAttribute("data-closed-behavior", "not-claimed");
    expect(stateHeader).toHaveTextContent("Observation window readonly");
    expect(stateHeader).not.toHaveTextContent("Closed");
    expect(screen.queryByRole("button", { name: /approve|reject|delay|observe|execute/i }))
      .not.toBeInTheDocument();
  });

  it("renders CD-T06A approved-pending state header skeleton as display lock only", () => {
    window.history.pushState({}, "", "/case/CASE-2847");

    render(<App initialPhaseNumber={5} />);

    const stateHeader = screen.getByTestId("case-state-header-skeleton");

    expect(stateHeader).toHaveAttribute("data-case-state", "APPROVED_PENDING_EXECUTION");
    expect(stateHeader).toHaveAttribute("data-ar-status", "APPROVED_PENDING_EXECUTION");
    expect(stateHeader).toHaveAttribute("data-visual-frame", "VF-12");
    expect(stateHeader).toHaveAttribute("data-lock-state", "terminal-display-lock");
    expect(stateHeader).toHaveAttribute("data-state-mutation", "none");
    expect(stateHeader).toHaveAttribute("data-closed-behavior", "not-claimed");
    expect(stateHeader).toHaveTextContent("Approved pending execution locked");
    expect(stateHeader).toHaveTextContent(/execution is not started here/i);
    expect(stateHeader).not.toHaveTextContent("Closed");
    expect(screen.queryByRole("button", { name: /approve|reject|delay|observe|execute/i }))
      .not.toBeInTheDocument();
  });

  it("renders CD-T06 CLOSED Case Detail as readonly with full P1/P2 audit trail", () => {
    window.history.pushState({}, "", "/case/CASE-2847");

    render(<App initialPhaseNumber={5} initialClosedCaseDetailRole="P2" />);

    expect(screen.getByTestId("closed-case-banner")).toHaveAttribute(
      "data-case-state",
      "CLOSED"
    );
    expect(screen.getByTestId("closed-state-pill")).toHaveAttribute(
      "data-case-state",
      "CLOSED"
    );
    expect(screen.getByTestId("closed-state-badge")).toHaveAttribute(
      "data-close-reason",
      "RESOLVED"
    );
    expect(screen.getByTestId("case-state-header-skeleton")).toHaveAttribute(
      "data-visual-frame",
      "VF-13"
    );
    expect(screen.getByTestId("case-state-header-skeleton")).toHaveAttribute(
      "data-closed-behavior",
      "implemented"
    );
    expect(screen.getByTestId("closed-action-area")).toHaveAttribute(
      "data-readonly-state",
      "CLOSED"
    );
    expect(screen.getByTestId("full-audit-trail")).toHaveAttribute(
      "data-audit-source",
      "CD-T06-renderable-context-checklist-v0.1"
    );
    for (const id of ["AUD-001", "AUD-002", "AUD-003", "AUD-004", "AUD-005", "AUD-006"]) {
      expect(screen.getByTestId(`audit-${id}`)).toBeInTheDocument();
    }
    for (const forbidden of [
      "approve-mode-button",
      "reject-mode-button",
      "submit-ar-button",
      "add-note-button",
      "close-request-button",
      "escalate-button",
      "withdraw-approval-btn",
      "decision-composer-actions"
    ]) {
      expect(screen.queryByTestId(forbidden)).not.toBeInTheDocument();
    }
    expect(screen.getByTestId("closed-dialogue-notice")).toBeInTheDocument();
    expect(screen.getByTestId("dialogue-input-readonly")).toBeDisabled();
    expect(screen.getByTestId("dialogue-send-disabled")).toBeDisabled();
  });

  it("renders CD-T06 P3 CLOSED summary without full audit trail or technical drawers", () => {
    window.history.pushState({}, "", "/case/CASE-2847");

    render(<App initialPhaseNumber={6} initialClosedCaseDetailRole="P3" />);

    expect(screen.getByTestId("closed-case-banner")).toBeInTheDocument();
    expect(screen.getByTestId("p3-approval-audit-summary")).toHaveAttribute("data-role", "P3");
    expect(screen.getByTestId("p3-approval-audit-summary")).toHaveAttribute(
      "data-full-audit-chain",
      "not-rendered"
    );
    expect(screen.getByTestId("manager-summary-root")).toBeInTheDocument();
    expect(screen.queryByTestId("full-audit-trail")).not.toBeInTheDocument();
    expect(screen.queryByTestId("host-raw-evidence")).not.toBeInTheDocument();
    expect(screen.queryByTestId("p2-evidence-drawer")).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /approve|reject|delay|observe|close/i }))
      .not.toBeInTheDocument();
    expect(screen.getByTestId("dialogue-input-readonly")).toBeDisabled();
    expect(screen.getByTestId("dialogue-send-disabled")).toBeDisabled();
  });

  it("ignores URL and storage attempts to inject AR status or action mode", () => {
    window.history.pushState(
      {},
      "",
      "/case/CASE-2847?ar_status=PENDING_APPROVAL&action_mode=IMMEDIATE"
    );
    window.localStorage.setItem("ar_status", "PENDING_APPROVAL");
    window.sessionStorage.setItem("action_mode", "IMMEDIATE");

    render(<App />);

    const statusPill = screen.getByTestId("ar-status-pill");

    expect(statusPill).toHaveAttribute("data-ar-status", "NONE");
    expect(statusPill).toHaveAttribute("data-action-authority", "display-only");
    expect(statusPill).toHaveAttribute("data-state-migration", "none");
    expect(document.body).not.toHaveTextContent(/IMMEDIATE|DELAYED|OBSERVE_ONLY/);
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
    expect(screen.queryByTestId("p3-executive-summary")).not.toBeInTheDocument();
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

  it("renders a P3 independent executive summary inside Case Detail from allowed fields only", () => {
    window.history.pushState({}, "", "/case/CASE-2847");

    render(<App initialPhaseNumber={6} />);

    const summary = screen.getByTestId("p3-executive-summary");
    const unsupportedClaims = within(summary).getAllByTestId(
      "p3-executive-summary-unsupported-claim"
    );

    expect(summary).toHaveAttribute("data-role", "P3");
    expect(summary).toHaveAttribute("data-component-scope", "cd-t05-case-detail-only");
    expect(summary).toHaveAttribute(
      "data-source-boundary",
      "summary-honesty-unsupported-confidence-disproof"
    );
    expect(summary).toHaveAttribute("data-manager-handoff", "not-implemented");
    expect(summary).toHaveAttribute("data-approval-audit-summary", "not-implemented");
    expect(within(summary).getByTestId("p3-executive-summary-verdict")).toHaveAttribute(
      "data-summary-field",
      "summary_layer.verdict"
    );
    expect(within(summary).getByTestId("p3-executive-summary-summary")).toHaveAttribute(
      "data-summary-field",
      "summary_layer.summary"
    );
    expect(within(summary).getByTestId("p3-executive-summary-coverage")).toHaveAttribute(
      "data-summary-field",
      "summary_layer.coverage_level"
    );
    expect(within(summary).getByTestId("p3-executive-summary-caution")).toHaveAttribute(
      "data-source-field",
      "honesty_layer.unsupported_claims"
    );
    expect(within(summary).getByTestId("p3-executive-summary-confidence")).toHaveAttribute(
      "data-source-field",
      "honesty_layer.what_would_raise_confidence"
    );
    expect(within(summary).getByTestId("p3-executive-summary-disproof")).toHaveAttribute(
      "data-source-field",
      "honesty_layer.what_would_disprove_current_verdict"
    );
    expect(unsupportedClaims[0]).toHaveTextContent(
      coreSurfaceFixture.case.honesty_layer.unsupported_claims[0]
    );
    expect(summary).toHaveTextContent(
      coreSurfaceFixture.case.honesty_layer.what_would_raise_confidence[0]
    );
    expect(summary).toHaveTextContent(
      coreSurfaceFixture.case.honesty_layer.what_would_disprove_current_verdict[0]
    );
  });

  it("keeps CD-T05 forbidden sources and over-certain copy out of the P3 summary", () => {
    window.history.pushState({}, "", "/case/CASE-2847");

    render(<App initialPhaseNumber={6} />);

    const summary = screen.getByTestId("p3-executive-summary");

    expect(within(summary).queryByTestId("host-raw-evidence")).not.toBeInTheDocument();
    expect(within(summary).queryByTestId("manager-approval-audit-summary")).not.toBeInTheDocument();
    expect(within(summary).queryByRole("button", { name: /approve|reject|delay|observe/i }))
      .not.toBeInTheDocument();
    expect(within(summary).queryByText(/blast radius|lineage confidence|process raw/i))
      .not.toBeInTheDocument();
    expect(summary).not.toHaveTextContent(/完全受控|已彻底消除/i);
    expect(summary).not.toHaveTextContent(/MTTA|MTTR|ROI|queue count/i);
    expect(screen.queryByTestId("p3-executive-summary")).toBeInTheDocument();
    expect(screen.queryByTestId("manager-view-surface")).not.toBeInTheDocument();
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
    const requestEntrySkeleton = within(actionRequestPanel).getByTestId(
      "p1-escalation-close-request-skeleton"
    );
    expect(requestEntrySkeleton).toHaveAttribute(
      "data-authority-source",
      "resolved-surface-context"
    );
    expect(requestEntrySkeleton).toHaveAttribute("data-visual-state", "skeleton");
    expect(requestEntrySkeleton).toHaveAttribute("data-action-mode", "not-selected-by-p1");
    expect(requestEntrySkeleton).toHaveAttribute("data-close-execution", "not-implemented");
    expect(
      within(requestEntrySkeleton).getByText("Escalation entry").closest("[data-entry-type]")
    ).toHaveAttribute("data-entry-type", "escalation_to_p2");
    expect(within(requestEntrySkeleton).getByTestId("p1-escalation-reason-field")).toHaveTextContent(
      /required/i
    );
    expect(
      within(requestEntrySkeleton).getByTestId("p1-recommended-action-field")
    ).toHaveTextContent(/P2 reference only/i);
    expect(within(requestEntrySkeleton).getByTestId("p1-urgency-text-field")).toHaveTextContent(
      /not ActionMode/i
    );
    expect(within(requestEntrySkeleton).getByTestId("p1-close-request-entry")).toHaveAttribute(
      "data-entry-state",
      "skeleton-only"
    );
    expect(
      within(actionRequestPanel).queryByRole("button", {
        name: /approve|reject|delay|observe|close/i
      })
    ).not.toBeInTheDocument();

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
    expect(within(dialog).getByTestId("p1-action-request-modal-fields")).toHaveAttribute(
      "data-action-mode",
      "not-selected-by-p1"
    );
    expect(within(dialog).getByTestId("p1-modal-escalation-reason")).toHaveTextContent(
      /required/i
    );
    expect(within(dialog).getByTestId("p1-modal-recommended-action")).toHaveTextContent(
      /P2 reference only/i
    );
    expect(within(dialog).getByTestId("p1-modal-urgency-text")).toHaveTextContent(
      /not ActionMode/i
    );
    expect(dialog).not.toHaveTextContent(/IMMEDIATE|DELAYED|OBSERVE_ONLY/);
    expect(within(dialog).queryByRole("button", { name: /approve|reject|delay|observe|close/i })).not.toBeInTheDocument();

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
    expect(
      within(actionRequestPanel).queryByTestId("p1-escalation-close-request-skeleton")
    ).not.toBeInTheDocument();
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
    const inferredNodeSlot = within(timelinePanel).getByTestId("inferred-node-weakening-slot");
    expect(inferredNodeSlot).toHaveAttribute("data-inferred-node", "true");
    expect(inferredNodeSlot).toHaveAttribute("data-direct-evidence-node", "false");
    expect(inferredNodeSlot).toHaveAttribute("data-evidence-weight", "weakened");
    expect(inferredNodeSlot).toHaveAttribute("data-visual-state", "skeleton");
    expect(inferredNodeSlot).toHaveAttribute("data-vf-10-state", "pending");
    expect(within(inferredNodeSlot).getByTestId("inferred-node-weight-label")).toHaveTextContent(
      /lower weight than direct evidence/i
    );
    expect(
      within(inferredNodeSlot).getByTestId("inferred-node-source-boundary")
    ).toHaveTextContent(/No graph, tool, node, or new fact/i);
    expect(window.location.pathname).toBe("/case/CASE-2847");
    expect(screen.queryByRole("button", { name: /approve|reject|delay|observe|close/i })).not.toBeInTheDocument();
    expect(document.body).not.toHaveTextContent(/IMMEDIATE|DELAYED|OBSERVE_ONLY/);

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
    const lineageSummary = within(evidencePanel).getByTestId("l1-lineage-degradation-summary");
    expect(lineageSummary).toHaveAttribute("data-field", "evidence_layer.lineage_confidence");
    expect(lineageSummary).toHaveAttribute("data-switch-state", "DEGRADED");
    expect(lineageSummary).toHaveAttribute("data-coverage-level", "L1");
    expect(lineageSummary).toHaveAttribute("data-lineage-card", "simplified-summary");
    expect(lineageSummary).toHaveAttribute("data-vf-10-state", "pending");
    expect(within(lineageSummary).getByTestId("lineage-degradation-state")).toHaveTextContent(
      /DEGRADED at coverage L1/i
    );
    expect(within(lineageSummary).getByTestId("lineage-degradation-boundary")).toHaveTextContent(
      /no full lineage card, graph, tool, node, or new fact/i
    );
    expect(within(subordinateSelector).queryByRole("button", { name: "Blast Radius" })).not.toBeInTheDocument();
    expect(within(evidencePanel).queryByTestId("blast-radius-subordinate-panel")).not.toBeInTheDocument();
    expect(within(evidencePanel).queryByTestId("full-lineage-card")).not.toBeInTheDocument();
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
    window.history.pushState({}, "", "/case/CASE-2847");
    render(<App initialPhaseNumber={6} />);

    expect(screen.getByLabelText("Mock fixture resolved context")).toHaveTextContent("Role P3");
    expect(screen.getByLabelText("Mock fixture resolved context")).toHaveTextContent("P3_MANAGER");
    expect(screen.queryByText(panelTitle("process_evidence"))).not.toBeInTheDocument();
    expect(screen.queryByTestId("host-raw-evidence")).not.toBeInTheDocument();
    expect(screen.getByLabelText("Case follow-up input")).toBeInTheDocument();
  });

  it("renders a cautious P3 technical summary fallback without host detail or write controls", async () => {
    const user = userEvent.setup();
    window.history.pushState({}, "", "/case/CASE-2847");
    render(<App initialPhaseNumber={6} />);

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
    expect(screen.getByTestId("l1-lineage-degradation-summary")).toHaveAttribute(
      "data-switch-state",
      "DEGRADED"
    );
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
    window.history.pushState({}, "", "/case/CASE-2847");
    render(<App initialPhaseNumber={6} />);

    await user.selectOptions(
      screen.getByLabelText("Mock redline fixture"),
      "resolver-p3-technical-detail-redaction"
    );

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
