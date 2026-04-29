import { expect, test, type Page } from "@playwright/test";

async function openApprovalPhase(page: Page, phase: string) {
  await page.goto("/case/CASE-2847");
  await page.getByLabel("Mock fixture phase").selectOption(phase);
  await page.getByRole("button", { name: /Approval Queue/i }).click();
  await expect(page).toHaveURL(/\/approval$/);
  await expect(page.getByTestId("approval-surface")).toHaveAttribute(
    "data-authority-source",
    "resolved-surface-context"
  );
}

async function emitMockStateSync(page: Page) {
  await page.evaluate(() => {
    window.dispatchEvent(
      new CustomEvent("secupilot:mock-state-sync", {
        detail: {
          state_sync_source: "mock_state_sync",
          case_state: "PENDING_APPROVAL",
          ar_status: "PENDING_APPROVAL",
          action_mode: null,
          observation_window_remaining_minutes: 0,
          observation_expiry_action: "RETURN_TO_PENDING_APPROVAL",
          audit_event_id: "AUD-004",
          audit_event_type: "OBSERVATION_WINDOW_EXPIRED"
        }
      })
    );
  });
}

test.describe("AP-T12C full AP acceptance lane", () => {
  test("keeps the P2 approval route shell source-bound and non-mutating", async ({ page }) => {
    await openApprovalPhase(page, "2");

    const approvalSurface = page.getByTestId("approval-surface");
    const approvalShell = page.getByTestId("approval-shell-card");
    const statusPill = page.getByTestId("approval-ar-status-pill");
    const ctaBoundary = page.getByTestId("approval-cta-boundary");
    const auditBoundary = page.getByTestId("approval-audit-source-boundary");

    await expect(approvalSurface).toHaveAttribute("data-role", "P2");
    await expect(approvalSurface).toHaveAttribute("data-route-authority", "resolved-surface-context");
    await expect(statusPill).toHaveAttribute("data-ar-status", "PENDING_APPROVAL");
    await expect(statusPill).toHaveAttribute("data-mapping-source", "D-02");
    await expect(statusPill).toHaveAttribute("data-state-migration", "none");
    await expect(ctaBoundary).toHaveAttribute("data-action-authority", "p2-only");
    await expect(ctaBoundary).toHaveAttribute("data-state-mutation", "none");
    await expect(auditBoundary).toHaveAttribute("data-source", "activeContext.audit_trail");
    await expect(auditBoundary).toHaveAttribute("data-display-mode", "display-only");
    await expect(auditBoundary).toHaveAttribute(
      "data-derived-status-source",
      "fixed-enum-mapping"
    );

    for (const actionId of [
      "approve_action",
      "reject_action",
      "delay_action",
      "observe_only_action"
    ]) {
      await expect(page.getByTestId(`approval-cta-${actionId}`)).toHaveAttribute(
        "data-state-mutation",
        "none"
      );
    }

    await approvalShell.getByRole("button", { name: "Approve" }).click();
    const strongConfirm = page.getByTestId("approval-strong-confirm-dialog");
    await expect(strongConfirm).toHaveAttribute("data-draft-action", "approve");
    await expect(strongConfirm).toHaveAttribute("data-state-mutation", "none");
    await expect(page.getByTestId("approval-draft-confirm")).toBeDisabled();
    await expect(strongConfirm).not.toContainText(/IMMEDIATE|DELAYED|OBSERVE_ONLY/);
    await strongConfirm.getByRole("button", { name: "Close" }).click();

    await approvalShell.getByRole("button", { name: "Observe" }).click();
    const observeConfig = page.getByTestId("approval-configuration-dialog");
    await expect(observeConfig).toHaveAttribute("data-draft-action", "observe");
    await expect(observeConfig).toHaveAttribute("data-state-mutation", "none");
    await expect(page.getByTestId("approval-delay-observe-config-shell")).toHaveAttribute(
      "data-timer-authority",
      "none"
    );
    await expect(observeConfig).not.toContainText(/IMMEDIATE|DELAYED|OBSERVE_ONLY/);
  });

  test("requires mock STATE_SYNC rather than clock authority for observation-window exit", async ({
    page
  }) => {
    await openApprovalPhase(page, "3");

    const observationBoundary = page.getByTestId("approval-observation-window-skeleton");
    await expect(observationBoundary).toHaveAttribute("data-case-state", "OBSERVATION_WINDOW");
    await expect(observationBoundary).toHaveAttribute("data-ar-status", "OBSERVATION_WINDOW");
    await expect(observationBoundary).toHaveAttribute("data-timer-authority", "none");
    await expect(observationBoundary).toHaveAttribute("data-state-sync", "mock-helper-only");
    await expect(observationBoundary).toHaveAttribute("data-state-sync-source", "emitStateSync");
    await expect(observationBoundary).toHaveAttribute("data-real-backend-protocol", "none");
    await expect(page.getByTestId("view-details-button")).toBeDisabled();
    await expect(page.getByTestId("approval-cta-boundary")).toHaveCount(0);

    await emitMockStateSync(page);

    await expect(page.getByTestId("approval-observation-window-skeleton")).toHaveCount(0);
    await expect(page.getByTestId("approval-ar-status-pill")).toHaveAttribute(
      "data-ar-status",
      "PENDING_APPROVAL"
    );
    await expect(page.getByTestId("approval-cta-boundary")).toBeVisible();
    await expect(page.getByTestId("observation-expired-notice")).toHaveAttribute(
      "data-state-sync-source",
      "mock_state_sync"
    );
    await expect(page.getByTestId("observation-expired-notice")).toHaveAttribute(
      "data-auto-execute",
      "absent"
    );
  });

  test("preserves AP authority against URL and storage injection", async ({ page }) => {
    await page.addInitScript(() => {
      window.localStorage.setItem("role", "P2");
      window.localStorage.setItem("action_mode", "IMMEDIATE");
      window.sessionStorage.setItem("ar_status", "PENDING_APPROVAL");
    });

    await page.goto("/approval?role=P2&action_mode=IMMEDIATE&ar_status=PENDING_APPROVAL");

    await expect(page.getByTestId("resolved-context")).toContainText("Role P1");
    await expect(page.getByRole("region", { name: "Case-first intake" })).toBeVisible();
    await expect(page.getByTestId("approval-surface")).toHaveCount(0);
    await expect(page.locator("body")).not.toContainText(/\b(IMMEDIATE|DELAYED|OBSERVE_ONLY)\b/);
    await expect(page.getByRole("button", { name: /approve|reject|delay|observe/i })).toHaveCount(
      0
    );
  });
});
