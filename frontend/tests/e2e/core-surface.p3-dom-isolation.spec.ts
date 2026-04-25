import { expect, test } from "@playwright/test";

test.describe("LC-N P3 DOM isolation seed", () => {
  test("keeps host-level raw evidence and approval controls absent for P3", async ({ page }) => {
    await page.goto("/case/CASE-2847");
    await page.getByLabel("Mock fixture phase").selectOption("6");

    const resolvedContext = page.getByTestId("resolved-context");
    await expect(resolvedContext).toContainText("Role P3");
    await expect(resolvedContext).toContainText("P3_MANAGER");
    await expect(page.getByTestId("evidence-panel")).toBeVisible();
    await expect(page.getByTestId("host-raw-evidence")).toHaveCount(0);
    await expect(page.getByText("Process / Execution Evidence")).toHaveCount(0);
    await expect(page.getByText("进程证据")).toHaveCount(0);
    await expect(page.getByRole("button", { name: /Approval Queue/i })).toHaveCount(0);
    await expect(page.getByRole("button", { name: /approve|reject|delay|observe/i })).toHaveCount(0);
  });
});
