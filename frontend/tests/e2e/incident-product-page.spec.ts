import { expect, test } from "@playwright/test";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const THIS_FILE = fileURLToPath(import.meta.url);
const REPO_ROOT = path.resolve(path.dirname(THIS_FILE), "../../..");
const EVIDENCE_ROOT = path.join(REPO_ROOT, "artifacts", "product_experience", "ux02");

test.describe("UX-02 incident AI advice language and collapse", () => {
  test.beforeAll(async () => {
    await mkdir(EVIDENCE_ROOT, { recursive: true });
  });

  test("renders conclusion-first incident page with collapsed AI advice source", async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 1000 });
    await page.goto("/incident/CASE-2847");

    const surface = page.getByTestId("incident-product-view");
    await expect(surface).toBeVisible();
    await expect(surface).toHaveAttribute("data-real-data", "false");
    await expect(surface).toHaveAttribute("data-live-qwen-api", "false");
    await expect(surface).toHaveAttribute("data-live-connectors", "false");
    await expect(surface).toHaveAttribute("data-production-writeback", "false");
    await expect(surface).toHaveAttribute("data-customer-visible-output", "false");
    const workbenchConsole = page.getByTestId("incident-workbench-console");
    await expect(workbenchConsole).toBeVisible();
    await expect(workbenchConsole.getByText("事件工作台")).toBeVisible();
    await expect(workbenchConsole.getByText("事件队列")).toBeVisible();
    await expect(workbenchConsole.getByText("事件时间线")).toBeVisible();
    await expect(page.getByRole("heading", { name: "SecuPilot 事件研判结果" })).toBeVisible();
    await expect(page.getByTestId("incident-current-outcome")).toContainText(
      "需要人工复核的高风险事件"
    );
    await expect(page.getByTestId("incident-recommended-action")).toContainText("不自动处置");
    const recommendedActionCard = page.getByTestId("incident-recommended-action-card");
    await expect(recommendedActionCard).toBeVisible();
    await expect(recommendedActionCard).toHaveAttribute("data-autonomous-action", "false");
    await expect(recommendedActionCard).toHaveAttribute("data-state-mutation", "none");
    await expect(recommendedActionCard).toHaveAttribute("data-production-writeback", "false");
    await expect(recommendedActionCard).toHaveAttribute("data-customer-visible-output", "false");
    await expect(recommendedActionCard).toContainText("先交给人工确认");
    await expect(recommendedActionCard).toContainText("为什么建议这样做");
    await expect(recommendedActionCard).toContainText("人工确认边界");
    await expect(recommendedActionCard).toContainText("不自动执行");
    const feedbackLoop = page.getByTestId("incident-recommendation-feedback-loop");
    await expect(feedbackLoop).toBeVisible();
    await expect(feedbackLoop).toHaveAttribute("data-artifact-write", "false");
    await expect(feedbackLoop).toHaveAttribute("data-backend-write", "false");
    await expect(feedbackLoop).toHaveAttribute("data-qwen-api-call", "false");
    await expect(feedbackLoop).toHaveAttribute("data-state-mutation", "none");
    await expect(feedbackLoop).toContainText("这条建议是否准确、有用、还缺什么");
    await expect(page.getByTestId("incident-feedback-accuracy-option")).toHaveCount(3);
    await expect(page.getByTestId("incident-feedback-usefulness-option")).toHaveCount(3);
    await expect(page.getByTestId("incident-feedback-missing-info-option")).toHaveCount(4);
    await page.getByRole("button", { name: /基本准确/ }).click();
    await page.getByRole("button", { name: /可以行动/ }).click();
    await page.getByLabel("资产负责人和业务影响").check();
    await page.getByTestId("incident-feedback-note").fill("建议清楚，还需要资产负责人确认影响范围。");
    await page.getByTestId("incident-feedback-summary").click();
    await expect(page.getByTestId("incident-feedback-summary")).toContainText("基本准确");
    await expect(page.getByTestId("incident-feedback-summary")).toContainText("可以行动");
    await expect(page.getByTestId("incident-feedback-summary")).toContainText("资产负责人和业务影响");
    await expect(page.getByTestId("incident-feedback-preview")).toContainText(
      '"accuracy": "ACCURATE"'
    );
    await expect(page.getByTestId("incident-feedback-preview")).toContainText(
      '"backend_write": false'
    );
    const qwenProviderPreview = page.getByTestId("incident-qwen-provider-dry-run");
    await expect(qwenProviderPreview).toBeVisible();
    await expect(qwenProviderPreview).toHaveAttribute("data-live-qwen-api", "false");
    await expect(qwenProviderPreview).toHaveAttribute("data-network-request", "false");
    await expect(qwenProviderPreview).toHaveAttribute("data-api-key-required", "false");
    await expect(qwenProviderPreview).toHaveAttribute("data-real-data", "false");
    await expect(qwenProviderPreview).toHaveAttribute("data-autonomous-qwen-action", "false");
    await expect(qwenProviderPreview).not.toHaveAttribute("open", "");
    await expect(qwenProviderPreview.locator("summary").first()).toContainText(
      "了解 AI 建议的工作方式"
    );
    await expect(page.locator("body")).not.toContainText(
      /Qwen dry-run|provider stub|HOLD 输入包|模拟延迟|stub 案例数|Dry-run 输出预览|模型接入预览/
    );
    await qwenProviderPreview.locator("summary").first().click();
    await expect(qwenProviderPreview).toHaveAttribute("open", "");
    await expect(page.getByTestId("incident-qwen-provider-mode")).toHaveCount(4);
    await expect(page.getByTestId("incident-qwen-runtime-scenario")).toHaveCount(4);
    await expect(page.getByTestId("incident-qwen-readiness-status")).toContainText(
      "建议引擎就绪"
    );
    await expect(page.getByTestId("incident-qwen-provider-summary")).toContainText(
      "AI 建议输出预览"
    );
    await expect(page.getByTestId("incident-qwen-provider-summary")).toContainText(
      "回退本地规则摘要"
    );
    await expect(page.getByTestId("incident-qwen-provider-summary")).toContainText(
      "提示稍后重试"
    );
    await expect(page.getByTestId("incident-qwen-no-live-sentinels")).toContainText("实时模型连接");
    await expect(page.getByTestId("incident-qwen-no-live-sentinels")).toContainText("外部网络");
    await expect(page.getByTestId("incident-qwen-no-live-sentinels")).toContainText("不会发送");
    await page.getByTestId("incident-qwen-provider-mode").filter({ hasText: "人工复核" }).click();
    await page.getByTestId("incident-qwen-runtime-scenario").filter({ hasText: "字段不合规" }).click();
    await expect(page.getByTestId("incident-qwen-provider-summary")).toContainText("人工复核");
    await expect(page.getByTestId("incident-qwen-provider-summary")).toContainText(
      "建议暂停，等待人工清理"
    );
    await expect(page.getByTestId("incident-qwen-provider-preview")).toContainText(
      '"selected_provider_mode": "human_review"'
    );
    await expect(page.getByTestId("incident-qwen-provider-preview")).toContainText(
      '"selected_runtime_scenario": "contract_error"'
    );
    await expect(page.getByTestId("incident-qwen-provider-preview")).toContainText(
      '"retry_policy": "manual_retry_only"'
    );
    await expect(page.getByTestId("incident-qwen-provider-preview")).toContainText(
      '"fallback_mode": "local_rules_summary"'
    );
    await expect(page.getByTestId("incident-qwen-provider-preview")).toContainText(
      '"network_request": false'
    );
    await expect(page.getByTestId("incident-qwen-provider-preview")).toContainText(
      '"api_key_required": false'
    );
    await qwenProviderPreview.locator("summary").first().click();
    await expect(qwenProviderPreview).not.toHaveAttribute("open", "");
    await expect(page.getByTestId("incident-evidence-details")).not.toHaveAttribute("open", "");
    await expect(page.getByTestId("incident-technical-reconciliation")).not.toHaveAttribute(
      "open",
      ""
    );
    await expect(page.getByLabel("Role selector")).toHaveCount(0);
    await expect(page.getByLabel("Mock fixture phase")).toHaveCount(0);
    await expect(page.getByTestId("vf-03-expert-mode-frame")).toHaveCount(0);
    await expect(page.locator("body")).not.toContainText(
      /\bP1\b|\bP2\b|\bP3\b|Mock Fixture|Expert Mode|raw_payload\s*[:=]|authorization\s*[:=]|token\s*[:=]|private_key\s*[:=]/i
    );
    await expect(page.locator("body")).not.toContainText(
      /Qwen dry-run|provider stub|HOLD 输入包|模拟延迟|stub 案例数|Dry-run 输出预览|模型接入预览/
    );

    const screenshotPath = path.join(EVIDENCE_ROOT, "incident-product-desktop.png");
    await page.screenshot({ fullPage: true, path: screenshotPath });
    const visibleText = await page.locator("body").innerText();
    await writeFile(
      path.join(EVIDENCE_ROOT, "incident-product-desktop.text.json"),
      JSON.stringify(
        {
          schema_version: "secupilot.ux02.incident_ai_advice_language_text.v1",
          route: "/incident/CASE-2847",
          viewport: "1440x1000",
          visible_text: visibleText
        },
        null,
        2
      ),
      "utf-8"
    );
  });

  test("renders mobile incident page without debug controls", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 1000 });
    await page.goto("/incident/CASE-2847");

    const surface = page.getByTestId("incident-product-view");
    await expect(surface).toBeVisible();
    await expect(page.getByTestId("incident-workbench-console")).toBeVisible();
    await expect(page.getByRole("heading", { name: "SecuPilot 事件研判结果" })).toBeVisible();
    await expect(page.getByTestId("incident-current-outcome")).toContainText(
      "需要人工复核的高风险事件"
    );
    const recommendedActionCard = page.getByTestId("incident-recommended-action-card");
    await expect(recommendedActionCard).toBeVisible();
    await expect(recommendedActionCard).toHaveAttribute("data-autonomous-action", "false");
    await expect(recommendedActionCard).toHaveAttribute("data-state-mutation", "none");
    await expect(recommendedActionCard).toHaveAttribute("data-production-writeback", "false");
    await expect(recommendedActionCard).toHaveAttribute("data-customer-visible-output", "false");
    await expect(recommendedActionCard).toContainText("先交给人工确认");
    const feedbackLoop = page.getByTestId("incident-recommendation-feedback-loop");
    await expect(feedbackLoop).toBeVisible();
    await expect(feedbackLoop).toHaveAttribute("data-backend-write", "false");
    await expect(feedbackLoop).toHaveAttribute("data-qwen-api-call", "false");
    await expect(feedbackLoop).toContainText("反馈摘要");
    const qwenProviderPreview = page.getByTestId("incident-qwen-provider-dry-run");
    await expect(qwenProviderPreview).toBeVisible();
    await expect(qwenProviderPreview).toHaveAttribute("data-live-qwen-api", "false");
    await expect(qwenProviderPreview).toHaveAttribute("data-network-request", "false");
    await expect(qwenProviderPreview).toHaveAttribute("data-api-key-required", "false");
    await expect(qwenProviderPreview).not.toHaveAttribute("open", "");
    await expect(qwenProviderPreview.locator("summary").first()).toContainText("AI 建议来源");
    await expect(page.getByTestId("incident-evidence-details")).not.toHaveAttribute("open", "");
    await expect(page.getByLabel("Role selector")).toHaveCount(0);
    await expect(page.getByLabel("Mock fixture phase")).toHaveCount(0);
    await expect(page.locator("body")).not.toContainText(
      /\bP1\b|\bP2\b|\bP3\b|Mock Fixture|Expert Mode|raw_payload\s*[:=]|authorization\s*[:=]|token\s*[:=]|private_key\s*[:=]/i
    );

    const screenshotPath = path.join(EVIDENCE_ROOT, "incident-product-mobile.png");
    await page.screenshot({ fullPage: true, path: screenshotPath });
    const visibleText = await page.locator("body").innerText();
    await writeFile(
      path.join(EVIDENCE_ROOT, "incident-product-mobile.text.json"),
      JSON.stringify(
        {
          schema_version: "secupilot.ux02.incident_ai_advice_language_text.v1",
          route: "/incident/CASE-2847",
          viewport: "390x1000",
          visible_text: visibleText
        },
        null,
        2
      ),
      "utf-8"
    );
  });
});
