import { expect, test } from "@playwright/test";
import { mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const THIS_FILE = fileURLToPath(import.meta.url);
const REPO_ROOT = path.resolve(path.dirname(THIS_FILE), "../../..");
const SCREENSHOT_ROOT = path.join(
  REPO_ROOT,
  "artifacts",
  "eci_vfe_fixture_runs",
  "rc001",
  "screenshots"
);

test.describe("ECI/VFE chain indicator visual smoke", () => {
  test.beforeAll(async () => {
    await mkdir(SCREENSHOT_ROOT, { recursive: true });
  });

  test("captures chain indicator desktop screenshot", async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 1100 });
    await page.goto("/eci-vfe-chain");

    const surface = page.getByTestId("eci-chain-indicator-view");
    await expect(surface).toBeVisible();
    await expect(surface).toHaveAttribute("data-output-guard-status", "PASS");
    await expect(surface).toHaveAttribute("data-real-data", "false");
    await expect(surface).toHaveAttribute("data-live-qwen-api", "false");
    await expect(surface).toHaveAttribute("data-production-writeback", "false");
    await expect(page.getByRole("heading", { name: "Incident chain status" })).toBeVisible();
    await expect(page.getByTestId("eci-chain-indicator-card")).toHaveCount(6);

    await page.screenshot({
      fullPage: true,
      path: path.join(SCREENSHOT_ROOT, "eci-chain-indicator-desktop.png"),
    });
  });

  test("captures chain indicator mobile screenshot", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 1000 });
    await page.goto("/eci-vfe-chain");

    const surface = page.getByTestId("eci-chain-indicator-view");
    await expect(surface).toBeVisible();
    await expect(surface).toHaveAttribute("data-output-guard-status", "PASS");
    await expect(surface).toHaveAttribute("data-real-data", "false");
    await expect(surface).toHaveAttribute("data-live-qwen-api", "false");
    await expect(surface).toHaveAttribute("data-production-writeback", "false");
    await expect(page.getByTestId("eci-chain-indicator-card")).toHaveCount(6);

    await page.screenshot({
      fullPage: true,
      path: path.join(SCREENSHOT_ROOT, "eci-chain-indicator-mobile.png"),
    });
  });
});
