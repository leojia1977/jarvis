import { expect, type Page, test } from "@playwright/test";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const THIS_FILE = fileURLToPath(import.meta.url);
const REPO_ROOT = path.resolve(path.dirname(THIS_FILE), "../../..");
const SCREENSHOT_ROOT = path.join(
  REPO_ROOT,
  "artifacts",
  "s1_closed_shadow_runs",
  "2026-04-30-001",
  "playwright"
);

async function captureScreenshotEvidence(
  page: Page,
  fileName: string,
  route: "/s1-run" | "/s1-trial",
  viewport: string
) {
  const screenshotPath = path.join(SCREENSHOT_ROOT, fileName);
  await page.screenshot({
    fullPage: true,
    path: screenshotPath
  });
  const visibleText = await page.locator("body").innerText();
  await writeFile(
    path.join(SCREENSHOT_ROOT, fileName.replace(/\.png$/, ".text.json")),
    JSON.stringify(
      {
        schema_version: "secupilot.s1.screenshot_text_evidence.v1",
        file_name: fileName,
        route,
        viewport,
        visible_text: visibleText
      },
      null,
      2
    ),
    "utf-8"
  );
}

async function assertS1VisualBoundary(page: Page) {
  const surface = page.getByTestId("s1-artifact-view");
  await expect(surface).toBeVisible();
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
  const reviewPanel = page.getByTestId("s1-local-review-panel");
  await expect(reviewPanel).toBeVisible();
  await expect(reviewPanel).toHaveAttribute("data-review-scope", "LOCAL_OFFLINE_TRIAL_RC_020_CN");
  await expect(reviewPanel).toHaveAttribute("data-state-mutation", "none");
  await expect(reviewPanel).toHaveAttribute("data-artifact-write", "false");
  await expect(page.getByTestId("s1-selected-review-decision")).toContainText(
    "PASS_TO_NEXT_LOCAL_RC"
  );
  await expect(page.getByTestId("s1-technical-reconciliation")).not.toHaveAttribute("open", "");
  const handoffPanel = page.getByTestId("s1-review-handoff-panel");
  await expect(handoffPanel).toBeVisible();
  await expect(handoffPanel).toHaveAttribute("data-review-mode", "LOCAL_OFFLINE_REVIEW_ONLY");
  await expect(page.getByTestId("s1-review-required-check")).toHaveCount(10);
  await expect(page.getByTestId("s1-artifact-row")).toHaveCount(5);
  await expect(page.getByTestId("s1-case-row")).toHaveCount(20);
  await expect(surface.getByRole("button", { name: /approve|deploy|publish/i })).toHaveCount(0);
  await expect(page.locator("body")).not.toContainText(
    /raw_payload\s*[:=]|raw_evidence\s*[:=]|authorization\s*[:=]|token\s*[:=]|private_key\s*[:=]|writeback_action\s*[:=]/i
  );
}

async function assertS1TrialVisualBoundary(page: Page) {
  const surface = page.getByTestId("s1-local-trial-view");
  await expect(surface).toBeVisible();
  await expect(surface).toHaveAttribute("data-real-data", "false");
  await expect(surface).toHaveAttribute("data-live-qwen-api", "false");
  await expect(surface).toHaveAttribute("data-live-connectors", "false");
  await expect(surface).toHaveAttribute("data-customer-visible-output", "false");
  await expect(surface).toHaveAttribute("data-production-writeback", "false");
  await expect(surface).toHaveAttribute("data-push", "false");
  await expect(page.getByRole("heading", { name: "SecuPilot 企业安全分析助理" })).toBeVisible();
  await expect(page.getByText("客户试用入口 / 私有化预览")).toBeVisible();
  await expect(page.getByTestId("s1-private-preview-shell")).toContainText("私有化预览启动壳");
  await expect(page.getByTestId("s1-product-route-map-item")).toHaveCount(5);
  await expect(page.getByTestId("s1-product-role-entry")).toHaveCount(4);
  await expect(page.getByTestId("s1-product-role-grid")).toContainText("工程师视角");
  await expect(page.getByTestId("s1-product-role-grid")).toContainText("CTO / 部署视角");
  await expect(page.getByTestId("s1-product-trust-strip")).toContainText(
    "不连接真实系统和 live Qwen/API"
  );
  await expect(page.getByTestId("s1-trial-candidate")).toContainText(
    "LOCAL_OFFLINE_TRIAL_RC_020_CN"
  );
  await expect(page.getByTestId("s1-trial-package-path")).toContainText(
    "artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review"
  );
  await expect(page.getByLabel("Role selector")).toHaveCount(0);
  await expect(page.getByLabel("Mock fixture phase")).toHaveCount(0);
  await expect(page.getByTestId("vf-03-expert-mode-frame")).toHaveCount(0);
  await expect(surface).not.toContainText(/\bP1\b|\bP2\b|\bP3\b|Mock Fixture|Expert Mode/);
  await expect(page.locator("body")).not.toContainText(
    /raw_payload\s*[:=]|raw_evidence\s*[:=]|authorization\s*[:=]|token\s*[:=]|private_key\s*[:=]|writeback_action\s*[:=]/i
  );
}

test.describe("MVP-11 S1 artifact viewer visual smoke", () => {
  test.beforeAll(async () => {
    await mkdir(SCREENSHOT_ROOT, { recursive: true });
  });

  test("captures local-only desktop visual smoke", async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 1100 });
    await page.goto("/s1-run");

    await assertS1VisualBoundary(page);
    await captureScreenshotEvidence(page, "s1-run-desktop.png", "/s1-run", "1440x1100");
  });

  test("captures local-only mobile visual smoke", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 1000 });
    await page.goto("/s1-run");

    await assertS1VisualBoundary(page);
    await captureScreenshotEvidence(page, "s1-run-mobile.png", "/s1-run", "390x1000");
  });

  test("captures local trial desktop visual smoke", async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 1100 });
    await page.goto("/s1-trial");

    await assertS1TrialVisualBoundary(page);
    await captureScreenshotEvidence(page, "s1-trial-desktop.png", "/s1-trial", "1440x1100");
  });

  test("captures local trial mobile visual smoke", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 1000 });
    await page.goto("/s1-trial");

    await assertS1TrialVisualBoundary(page);
    await captureScreenshotEvidence(page, "s1-trial-mobile.png", "/s1-trial", "390x1000");
  });
});
