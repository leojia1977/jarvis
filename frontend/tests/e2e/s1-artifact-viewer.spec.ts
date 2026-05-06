import { expect, test } from "@playwright/test";

test.describe("MVP-05 S1 artifact viewer smoke", () => {
  test("opens /s1-run from workbench nav with local-only boundaries", async ({ page }, testInfo) => {
    await page.goto("/inbox");
    await page.getByRole("button", { name: /S1 Run/i }).click();

    const surface = page.getByTestId("s1-artifact-view");

    await expect(page).toHaveURL(/\/s1-run$/);
    await expect(surface).toHaveAttribute("data-artifact-source", "static-mvp-fixture");
    await expect(surface).toHaveAttribute("data-runtime-source", "none");
    await expect(surface).toHaveAttribute("data-customer-visible-output", "false");
    await expect(surface).toHaveAttribute("data-production-writeback", "false");
    await expect(surface).toHaveAttribute("data-qwen-used", "false");
    await expect(page.getByTestId("s1-final-outcome")).toContainText(
      "S1_CLOSED_SHADOW_PASS_WITH_NOTES"
    );
    await expect(page.getByTestId("s1-provider")).toContainText("fixture");
    await expect(page.getByTestId("s1-customer-visible-output")).toContainText("NO");
    await expect(page.getByTestId("s1-production-writeback")).toContainText("NO");
    await expect(page.getByTestId("s1-production-deploy")).toContainText("NO");
    const reviewPanel = page.getByTestId("s1-local-review-panel");
    await expect(reviewPanel).toHaveAttribute("data-review-scope", "LOCAL_OFFLINE_TRIAL_RC_004");
    await expect(reviewPanel).toHaveAttribute("data-state-mutation", "none");
    await expect(reviewPanel).toHaveAttribute("data-artifact-write", "false");
    await expect(reviewPanel).toHaveAttribute("data-qwen-api-call", "false");
    await expect(page.getByTestId("s1-review-decision-option")).toHaveCount(4);
    await expect(page.getByTestId("s1-selected-review-decision")).toContainText(
      "PASS_WITH_NOTES_TO_NEXT_LOCAL_RC"
    );
    await expect(page.getByTestId("s1-review-record-preview")).toContainText(
      '"customer_visible_output": false'
    );
    const handoffPanel = page.getByTestId("s1-review-handoff-panel");
    await expect(handoffPanel).toHaveAttribute("data-review-mode", "LOCAL_OFFLINE_REVIEW_ONLY");
    await expect(handoffPanel).toHaveAttribute(
      "data-review-package",
      "artifacts/local_demo_packages/s1-closed-shadow-local-offline-trial-rc-004"
    );
    await expect(handoffPanel).toHaveAttribute("data-state-mutation", "none");
    await expect(page.getByTestId("s1-review-required-check")).toHaveCount(8);
    await expect(page.getByTestId("s1-review-boundary-check")).toHaveCount(6);
    await expect(page.getByTestId("s1-artifact-row")).toHaveCount(5);
    await expect(page.getByTestId("s1-case-row")).toHaveCount(20);
    await expect(surface.getByRole("button", { name: /approve|deploy|publish/i })).toHaveCount(0);

    await page.screenshot({ fullPage: true, path: testInfo.outputPath("s1-run-smoke.png") });
  });

  test("renders /s1-run directly as readonly artifact fixture", async ({ page }) => {
    await page.goto("/s1-run");

    await expect(page.getByRole("heading", { name: "S1 Closed Shadow Run" })).toBeVisible();
    await expect(page.getByTestId("s1-run-id")).toContainText("S1-CLOSED-SHADOW-2026-04-30-001");
    await expect(page.getByTestId("s1-qwen-used")).toContainText("NO");
    await expect(page.getByTestId("s1-secret-retained")).toContainText("NO");
    await expect(page.getByTestId("s1-raw-payload-retained")).toContainText("NO");
    await expect(page.getByTestId("s1-production-connectors")).toContainText("NO");
    await expect(page.getByTestId("s1-local-review-panel")).toHaveAttribute(
      "data-source-candidate",
      "LOCAL_OFFLINE_TRIAL_RC_003"
    );
    await expect(page.getByTestId("s1-review-readme-path")).toContainText(
      "s1-closed-shadow-local-offline-trial-rc-004/REVIEWER_README.md"
    );
  });
});
