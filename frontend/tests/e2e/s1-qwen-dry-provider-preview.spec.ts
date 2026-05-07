import { expect, test } from "@playwright/test";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "../../..");
const PREVIEW_ROOT = path.join(
  REPO_ROOT,
  "artifacts",
  "qwen_provider_dry_ui_preview",
  "2026-05-07"
);

test.describe("MVP-31 Qwen dry provider UI preview", () => {
  test.beforeEach(async () => {
    await mkdir(PREVIEW_ROOT, { recursive: true });
  });

  test("renders dry provider input/output preview without live authority", async ({ page }) => {
    await page.goto("/s1-trial");

    const preview = page.getByTestId("s1-qwen-dry-preview");
    await expect(preview).toBeVisible();
    await expect(preview).toHaveAttribute("data-provider-mode", "dry_contract_only");
    await expect(preview).toHaveAttribute("data-live-qwen-api", "false");
    await expect(preview).toHaveAttribute("data-live-connectors", "false");
    await expect(preview).toHaveAttribute("data-production-writeback", "false");
    await expect(preview).toHaveAttribute("data-autonomous-qwen-action", "false");
    await expect(preview).toHaveAttribute("data-secret-material-allowed", "false");
    await expect(page.getByTestId("s1-qwen-dry-data-mode")).toContainText("SYNTHETIC_ONLY");
    await expect(page.getByTestId("s1-qwen-dry-case-id")).toContainText("UAT-01");
    await expect(page.getByTestId("s1-qwen-dry-reviewer-action")).toContainText(
      "REVIEW_AND_SIGNOFF_REQUIRED"
    );
    await expect(page.getByTestId("s1-qwen-dry-model-summary")).toContainText(
      "Synthetic metadata"
    );
    await expect(preview).not.toContainText(/raw_payload|action_command|Authorization:|Bearer /i);
    await expect(preview.getByRole("button", { name: /send|call|connect|deploy|publish/i }))
      .toHaveCount(0);

    const screenshotPath = path.join(PREVIEW_ROOT, "s1-qwen-dry-provider-preview.png");
    await preview.screenshot({ path: screenshotPath });
    await writeFile(
      path.join(PREVIEW_ROOT, "s1-qwen-dry-provider-preview.text.json"),
      JSON.stringify(
        {
          schema_version: "secupilot.s1.qwen_dry_provider_preview_text.v1",
          route: "/s1-trial",
          provider_mode: "dry_contract_only",
          live_qwen_api: false,
          live_connectors: false,
          production_writeback: false,
          autonomous_qwen_action: false,
          visible_text: await preview.innerText()
        },
        null,
        2
      ),
      "utf-8"
    );
  });
});
