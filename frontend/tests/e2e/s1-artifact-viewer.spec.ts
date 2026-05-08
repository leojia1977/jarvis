import { expect, test } from "@playwright/test";

test.describe("MVP-05 S1 artifact viewer smoke", () => {
  test("opens /s1-run from workbench nav with local-only boundaries", async ({ page }, testInfo) => {
    await page.goto("/inbox");
    await page.getByRole("button", { name: /S1 证据清单/i }).click();

    const surface = page.getByTestId("s1-artifact-view");

    await expect(page).toHaveURL(/\/s1-run$/);
    await expect(surface).toHaveAttribute("data-artifact-source", "static-mvp-fixture");
    await expect(surface).toHaveAttribute("data-runtime-source", "none");
    await expect(surface).toHaveAttribute("data-customer-visible-output", "false");
    await expect(surface).toHaveAttribute("data-production-writeback", "false");
    await expect(surface).toHaveAttribute("data-qwen-used", "false");
    await expect(page.getByTestId("s1-final-outcome-label")).toContainText(
      "带备注通过，可进入下一轮内部本地试用评审"
    );
    await expect(page.getByTestId("s1-final-outcome-code-link")).toContainText(
      "技术码已收起"
    );
    await expect(page.getByTestId("s1-final-outcome-code-link")).toHaveAttribute(
      "title",
      "技术码已收起，仅在“技术对账信息”展开后显示。"
    );
    await expect(page.getByRole("heading", { name: "本地离线试用结果" })).toBeVisible();
    await expect(page.getByTestId("s1-result-decision")).toContainText(
      "带备注通过，可进入下一轮内部本地试用评审"
    );
    await expect(page.getByTestId("s1-result-decision-explainer")).toContainText(
      "不代表客户发布或生产部署 GO"
    );
    await expect(page.getByTestId("s1-result-technical-code-link")).toContainText(
      "查看技术对账"
    );
    await expect(page.getByTestId("s1-technical-reconciliation-explainer")).toContainText(
      "点开后仅用于核对候选版本、运行编号、数据模式、离线 provider、证据哈希和状态码"
    );
    await expect(page.getByTestId("s1-run-next-step")).toContainText(
      "进入内部本地试用下一轮"
    );
    await expect(page.getByTestId("s1-run-next-step-code-link")).toContainText(
      "技术码已收起"
    );
    await expect(page.getByTestId("s1-customer-visible-output")).toContainText("否");
    await expect(page.getByTestId("s1-production-writeback")).toContainText("否");
    await expect(page.getByTestId("s1-production-deploy")).toContainText("否");
    const reviewPanel = page.getByTestId("s1-local-review-panel");
    await expect(reviewPanel).toHaveAttribute("data-review-scope", "LOCAL_OFFLINE_TRIAL_RC_016_CN");
    await expect(reviewPanel).toHaveAttribute("data-state-mutation", "none");
    await expect(reviewPanel).toHaveAttribute("data-artifact-write", "false");
    await expect(reviewPanel).toHaveAttribute("data-qwen-api-call", "false");
    await expect(page.getByTestId("s1-review-decision-option")).toHaveCount(4);
    await expect(page.getByTestId("s1-selected-review-decision")).toContainText(
      "PASS_TO_NEXT_LOCAL_RC"
    );
    await expect(page.getByTestId("s1-review-record-preview")).toContainText(
      '"customer_visible_output": false'
    );
    const handoffPanel = page.getByTestId("s1-review-handoff-panel");
    await expect(handoffPanel).toHaveAttribute("data-review-mode", "LOCAL_OFFLINE_REVIEW_ONLY");
    await expect(handoffPanel).toHaveAttribute(
      "data-review-package",
      "artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review"
    );
    await expect(handoffPanel).toHaveAttribute("data-state-mutation", "none");
    await expect(page.getByTestId("s1-review-required-check")).toHaveCount(10);
    await expect(page.getByTestId("s1-review-boundary-check")).toHaveCount(6);
    await expect(page.getByTestId("s1-artifact-row")).toHaveCount(5);
    await expect(page.getByTestId("s1-case-row")).toHaveCount(20);
    await expect(page.getByTestId("s1-technical-reconciliation")).not.toHaveAttribute("open", "");
    await expect(page.getByTestId("s1-technical-reconciliation-summary")).toContainText(
      "仅用于内部核验"
    );
    await page.locator("#s1-technical-reconciliation > summary").click();
    await expect(page.getByTestId("s1-technical-reconciliation")).toHaveAttribute("open", "");
    await expect(page.getByTestId("s1-provider")).toContainText("fixture");
    await expect(page.getByTestId("s1-reconciliation-candidate")).toContainText(
      "LOCAL_OFFLINE_TRIAL_RC_016_CN"
    );
    await expect(page.getByTestId("s1-reconciliation-data-mode")).toContainText(
      "SYNTHETIC_PACKAGE_ONLY"
    );
    await expect(page.getByTestId("s1-final-outcome-code")).toContainText(
      "S1_CLOSED_SHADOW_PASS_WITH_NOTES"
    );
    await expect(page.getByTestId("s1-run-next-step-code")).toContainText(
      "RC016_LOCAL_OFFLINE_REVIEW"
    );
    await expect(surface.getByRole("button", { name: /approve|deploy|publish/i })).toHaveCount(0);

    await page.screenshot({ fullPage: true, path: testInfo.outputPath("s1-run-smoke.png") });
  });

  test("renders /s1-run directly as readonly artifact fixture", async ({ page }) => {
    await page.goto("/s1-run");

    await expect(page.getByRole("heading", { name: "本地离线试用结果" })).toBeVisible();
    await expect(page.getByTestId("s1-technical-reconciliation")).not.toHaveAttribute("open", "");
    await page.locator("#s1-technical-reconciliation > summary").click();
    await expect(page.getByTestId("s1-technical-reconciliation")).toHaveAttribute("open", "");
    await expect(page.getByTestId("s1-run-id")).toContainText("S1-CLOSED-SHADOW-2026-04-30-001");
    await expect(page.getByTestId("s1-reconciliation-candidate")).toContainText(
      "LOCAL_OFFLINE_TRIAL_RC_016_CN"
    );
    await expect(page.getByTestId("s1-reconciliation-data-mode")).toContainText(
      "SYNTHETIC_PACKAGE_ONLY"
    );
    await expect(page.getByTestId("s1-qwen-used")).toContainText("否");
    await expect(page.getByTestId("s1-secret-retained")).toContainText("否");
    await expect(page.getByTestId("s1-raw-payload-retained")).toContainText("否");
    await expect(page.getByTestId("s1-production-connectors")).toContainText("否");
    await expect(page.getByTestId("s1-local-review-panel")).toHaveAttribute(
      "data-source-candidate",
      "LOCAL_OFFLINE_TRIAL_RC_015_CN"
    );
    await expect(page.getByTestId("s1-review-readme-path")).toContainText(
      "local-offline-trial-rc-016-cn-review/REVIEWER_START_HERE_中文.md"
    );
  });

  test("opens /s1-trial walkthrough with local-only launcher boundaries", async ({ page }) => {
    await page.goto("/inbox");
    await page.getByRole("button", { name: /本地试用/i }).click();

    const surface = page.getByTestId("s1-local-trial-view");

    await expect(page).toHaveURL(/\/s1-trial$/);
    await expect(page.getByRole("heading", { name: "SecuPilot 企业安全分析助理" })).toBeVisible();
    await expect(page.getByRole("heading", { name: "按你的工作目标进入" })).toBeVisible();
    await expect(page.getByTestId("s1-product-role-entry")).toHaveCount(4);
    await expect(page.getByTestId("s1-product-role-grid")).toContainText("一线研判");
    await expect(page.getByTestId("s1-product-role-grid")).toContainText("深度分析");
    await expect(page.getByTestId("s1-product-role-grid")).toContainText("管理审阅");
    await expect(page.getByTestId("s1-product-role-grid")).toContainText("部署与集成");
    await expect(page.getByTestId("s1-product-trust-strip")).toContainText(
      "不连接真实系统和 live Qwen/API"
    );
    await expect(page.getByLabel("Role selector")).toHaveCount(0);
    await expect(page.getByLabel("Mock fixture phase")).toHaveCount(0);
    await expect(page.getByTestId("vf-03-expert-mode-frame")).toHaveCount(0);
    await expect(surface).not.toContainText(/MVP-14|MVP-15|MVP-17|MVP-18|MVP-19/);
    await expect(surface).not.toContainText(/\bP1\b|\bP2\b|\bP3\b|Mock Fixture|Expert Mode/);
    await expect(surface).toHaveAttribute("data-real-data", "false");
    await expect(surface).toHaveAttribute("data-live-qwen-api", "false");
    await expect(surface).toHaveAttribute("data-live-connectors", "false");
    await expect(surface).toHaveAttribute("data-customer-visible-output", "false");
    await expect(surface).toHaveAttribute("data-production-writeback", "false");
    await expect(surface).toHaveAttribute("data-push", "false");
    await expect(page.getByTestId("s1-trial-candidate")).toContainText(
      "LOCAL_OFFLINE_TRIAL_RC_016_CN"
    );
    await expect(page.getByTestId("s1-trial-readiness")).toContainText(
      "GO_FOR_INTERNAL_LOCAL_OFFLINE_REVIEW_ONLY"
    );
    await expect(page.getByTestId("s1-trial-launch-command")).toContainText(
      "launch_s1_local_offline_trial.ps1"
    );
    await expect(page.getByTestId("s1-trial-package-path")).toContainText(
      "artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review"
    );
    await expect(page.getByTestId("s1-trial-start-here-path")).toContainText(
      "artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review/REVIEWER_START_HERE_中文.md"
    );
    await expect(page.getByTestId("s1-trial-step")).toHaveCount(5);
    const feedbackPanel = page.getByTestId("s1-feedback-panel");
    await expect(feedbackPanel).toHaveAttribute("data-artifact-write", "false");
    await expect(feedbackPanel).toHaveAttribute("data-backend-write", "false");
    await expect(feedbackPanel).toHaveAttribute("data-qwen-api-call", "false");
    await expect(page.getByTestId("s1-feedback-option")).toHaveCount(3);
    await expect(page.getByTestId("s1-feedback-preview")).toContainText(
      '"customer_visible_output": false'
    );
    const qwenContract = page.getByTestId("s1-qwen-provider-contract");
    await expect(qwenContract).toHaveAttribute("data-active-provider-mode", "qwen-cloud-disabled");
    await expect(qwenContract).toHaveAttribute("data-live-call-allowed", "false");
    await expect(page.getByTestId("s1-qwen-provider-mode")).toHaveCount(3);
    const qwenDryPreview = page.getByTestId("s1-qwen-dry-preview");
    await expect(qwenDryPreview).toHaveAttribute("data-provider-mode", "dry_contract_only");
    await expect(qwenDryPreview).toHaveAttribute("data-live-qwen-api", "false");
    await expect(qwenDryPreview).toHaveAttribute("data-live-connectors", "false");
    await expect(qwenDryPreview).toHaveAttribute("data-production-writeback", "false");
    await expect(qwenDryPreview).toHaveAttribute("data-autonomous-qwen-action", "false");
    await expect(page.getByTestId("s1-qwen-dry-data-mode")).toContainText("SYNTHETIC_ONLY");
    await expect(page.getByTestId("s1-qwen-dry-case-id")).toContainText("UAT-01");
    await expect(page.getByTestId("s1-qwen-dry-reviewer-action")).toContainText(
      "REVIEW_AND_SIGNOFF_REQUIRED"
    );
    await expect(surface.getByRole("button", { name: /approve|deploy|publish/i })).toHaveCount(0);
  });

  test("renders incident recommended action card with human-review boundary", async ({ page }) => {
    await page.goto("/incident/CASE-2847");

    const surface = page.getByTestId("incident-product-view");
    const recommendedActionCard = page.getByTestId("incident-recommended-action-card");

    await expect(surface).toHaveAttribute("data-real-data", "false");
    await expect(surface).toHaveAttribute("data-live-qwen-api", "false");
    await expect(surface).toHaveAttribute("data-live-connectors", "false");
    await expect(surface).toHaveAttribute("data-production-writeback", "false");
    await expect(recommendedActionCard).toHaveAttribute("data-autonomous-action", "false");
    await expect(recommendedActionCard).toHaveAttribute("data-customer-visible-output", "false");
    await expect(recommendedActionCard).toHaveAttribute("data-production-writeback", "false");
    await expect(recommendedActionCard).toHaveAttribute("data-state-mutation", "none");
    await expect(recommendedActionCard).toContainText("推荐动作");
    await expect(recommendedActionCard).toContainText("先交给人工确认，再决定是否处置");
    await expect(recommendedActionCard).toContainText("等待人工确认");
    await expect(recommendedActionCard).toContainText("不自动执行");
    await expect(recommendedActionCard).toContainText("人工确认边界");
    await expect(surface.getByRole("button", { name: /approve|deploy|publish/i })).toHaveCount(0);
  });
});
