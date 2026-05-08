import { expect, test } from "@playwright/test";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const THIS_FILE = fileURLToPath(import.meta.url);
const REPO_ROOT = path.resolve(path.dirname(THIS_FILE), "../../..");
const EVIDENCE_ROOT = path.join(REPO_ROOT, "artifacts", "product_experience", "mvp69");

test.describe("MVP-69 recommended action card", () => {
  test.beforeAll(async () => {
    await mkdir(EVIDENCE_ROOT, { recursive: true });
  });

  test("renders conclusion-first incident page with a safe recommended action card", async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 1000 });
    await page.goto("/incident/CASE-2847");

    const surface = page.getByTestId("incident-product-view");
    await expect(surface).toBeVisible();
    await expect(surface).toHaveAttribute("data-real-data", "false");
    await expect(surface).toHaveAttribute("data-live-qwen-api", "false");
    await expect(surface).toHaveAttribute("data-live-connectors", "false");
    await expect(surface).toHaveAttribute("data-production-writeback", "false");
    await expect(surface).toHaveAttribute("data-customer-visible-output", "false");
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

    const screenshotPath = path.join(EVIDENCE_ROOT, "incident-product-desktop.png");
    await page.screenshot({ fullPage: true, path: screenshotPath });
    const visibleText = await page.locator("body").innerText();
    await writeFile(
      path.join(EVIDENCE_ROOT, "incident-product-desktop.text.json"),
      JSON.stringify(
        {
          schema_version: "secupilot.mvp69.recommended_action_card_text.v1",
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
          schema_version: "secupilot.mvp69.recommended_action_card_text.v1",
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
