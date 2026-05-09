import { expect, test } from "@playwright/test";
import { mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const THIS_FILE = fileURLToPath(import.meta.url);
const REPO_ROOT = path.resolve(path.dirname(THIS_FILE), "../../..");
const SCREENSHOT_ROOT = path.join(
  REPO_ROOT,
  "artifacts",
  "local_demo_packages",
  "local-offline-trial-rc-018-cn-review",
  "screenshots"
);

const FORBIDDEN_CUSTOMER_PATH_TEXT =
  /provider stub|dry provider|dry-run\/stub|mock_data|package manifest|技术对账|ECI-FIX|output_guard_scan|attack_path|PoC|exploit|payload/i;

async function assertCustomerPathCopy(locatorText: string) {
  expect(locatorText).not.toMatch(FORBIDDEN_CUSTOMER_PATH_TEXT);
}

test.describe("RC-018 customer path screenshot package", () => {
  test.beforeAll(async () => {
    await mkdir(SCREENSHOT_ROOT, { recursive: true });
  });

  test("captures seven customer-readable screenshots", async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 1100 });
    await page.goto("/s1-trial");
    const productHome = page.getByTestId("s1-customer-product-home");
    await expect(productHome).toBeVisible();
    await assertCustomerPathCopy(await productHome.innerText());
    await productHome.screenshot({
      path: path.join(SCREENSHOT_ROOT, "01_product_home_desktop.png")
    });

    await page.setViewportSize({ width: 390, height: 1000 });
    await page.goto("/s1-trial");
    const productHomeMobile = page.getByTestId("s1-customer-product-home");
    await expect(productHomeMobile).toBeVisible();
    await assertCustomerPathCopy(await productHomeMobile.innerText());
    await productHomeMobile.screenshot({
      path: path.join(SCREENSHOT_ROOT, "02_product_home_mobile.png")
    });

    await page.setViewportSize({ width: 1440, height: 1100 });
    await page.goto("/incident/CASE-2847");
    await expect(page.getByTestId("incident-workbench-console")).toBeVisible();
    await expect(page.getByTestId("incident-current-outcome")).toContainText("需要人工复核");
    await page.screenshot({
      fullPage: false,
      path: path.join(SCREENSHOT_ROOT, "03_incident_first_load_desktop.png")
    });

    await page.setViewportSize({ width: 390, height: 1000 });
    await page.goto("/incident/CASE-2847");
    await expect(page.getByTestId("incident-workbench-console")).toBeVisible();
    await page.screenshot({
      fullPage: false,
      path: path.join(SCREENSHOT_ROOT, "04_incident_first_load_mobile.png")
    });

    await page.setViewportSize({ width: 1440, height: 1100 });
    await page.goto("/incident/CASE-2847");
    const aiAdvice = page.getByTestId("incident-qwen-provider-dry-run");
    await aiAdvice.locator("summary").click();
    await expect(aiAdvice).toHaveAttribute("open", "");
    await assertCustomerPathCopy(await aiAdvice.innerText());
    await aiAdvice.screenshot({
      path: path.join(SCREENSHOT_ROOT, "05_ai_advice_source_expanded_desktop.png")
    });

    const eciVfeSummary = page.getByTestId("incident-eci-vfe-summary");
    await eciVfeSummary.locator("summary").click();
    await expect(eciVfeSummary).toHaveAttribute("open", "");
    await expect(eciVfeSummary).toContainText("攻击链判断");
    await expect(eciVfeSummary).toContainText("风险预警摘要");
    await expect(eciVfeSummary).toContainText("建议补证窗口");
    await assertCustomerPathCopy(await eciVfeSummary.innerText());
    await eciVfeSummary.screenshot({
      path: path.join(SCREENSHOT_ROOT, "06_eci_vfe_summary_expanded_desktop.png")
    });

    const feedbackPanel = page.getByTestId("incident-recommendation-feedback-loop");
    await expect(feedbackPanel).toBeVisible();
    await expect(feedbackPanel).toHaveAttribute("data-backend-write", "false");
    await expect(feedbackPanel).toHaveAttribute("data-production-writeback", "false");
    await assertCustomerPathCopy(await feedbackPanel.innerText());
    await feedbackPanel.screenshot({
      path: path.join(SCREENSHOT_ROOT, "07_feedback_preview_desktop.png")
    });
  });
});
