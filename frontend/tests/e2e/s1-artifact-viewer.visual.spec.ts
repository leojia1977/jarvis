import { expect, type Page, test } from "@playwright/test";
import { mkdir } from "node:fs/promises";
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

async function assertS1VisualBoundary(page: Page) {
  const surface = page.getByTestId("s1-artifact-view");
  await expect(surface).toBeVisible();
  await expect(surface).toHaveAttribute("data-artifact-source", "static-mvp-fixture");
  await expect(surface).toHaveAttribute("data-runtime-source", "none");
  await expect(surface).toHaveAttribute("data-customer-visible-output", "false");
  await expect(surface).toHaveAttribute("data-production-writeback", "false");
  await expect(surface).toHaveAttribute("data-qwen-used", "false");
  await expect(page.getByTestId("s1-final-outcome")).toContainText(
    "S1_CLOSED_SHADOW_PASS_WITH_NOTES"
  );
  const reviewPanel = page.getByTestId("s1-local-review-panel");
  await expect(reviewPanel).toBeVisible();
  await expect(reviewPanel).toHaveAttribute("data-review-scope", "LOCAL_OFFLINE_TRIAL_RC_008_CN");
  await expect(reviewPanel).toHaveAttribute("data-state-mutation", "none");
  await expect(reviewPanel).toHaveAttribute("data-artifact-write", "false");
  await expect(page.getByTestId("s1-selected-review-decision")).toContainText(
    "PASS_TO_NEXT_LOCAL_RC"
  );
  await expect(page.getByTestId("s1-review-record-preview")).toContainText(
    '"production_writeback": false'
  );
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

test.describe("MVP-11 S1 artifact viewer visual smoke", () => {
  test.beforeAll(async () => {
    await mkdir(SCREENSHOT_ROOT, { recursive: true });
  });

  test("captures local-only desktop visual smoke", async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 1100 });
    await page.goto("/s1-run");

    await assertS1VisualBoundary(page);
    await page.screenshot({
      fullPage: true,
      path: path.join(SCREENSHOT_ROOT, "s1-run-desktop.png")
    });
  });

  test("captures local-only mobile visual smoke", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 1000 });
    await page.goto("/s1-run");

    await assertS1VisualBoundary(page);
    await page.screenshot({
      fullPage: true,
      path: path.join(SCREENSHOT_ROOT, "s1-run-mobile.png")
    });
  });
});
