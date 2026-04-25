import { expect, test } from "@playwright/test";

test.describe("LC-B and LC-N permission guard seeds", () => {
  test("ignores URL and browser storage attempts to inject role or coverage", async ({ page }) => {
    await page.addInitScript(() => {
      window.localStorage.setItem("role", "P3");
      window.localStorage.setItem("coverage", "L3");
      window.sessionStorage.setItem("role", "P3");
      window.sessionStorage.setItem("coverage", "L3");
    });

    await page.goto("/case/CASE-2847?role=P3&coverage=L3&surface=P3_MANAGER");

    const resolvedContext = page.getByTestId("resolved-context");
    await expect(page.getByTestId("coverage-badge")).toContainText("Coverage L2");
    await expect(resolvedContext).toContainText("Role P1");
    await expect(resolvedContext).toContainText("P1_CASE_DETAIL");
  });

  test("keeps P1 action mode decisions out of the rendered DOM", async ({ page }) => {
    await page.goto("/case/CASE-2847");

    await expect(page.getByTestId("resolved-context")).toContainText("Role P1");
    await expect(page.locator("body")).not.toContainText(/\b(IMMEDIATE|DELAYED|OBSERVE_ONLY)\b/);
  });

  test("does not expose approval operations from invalid deep links", async ({ page }) => {
    await page.goto("/approval?caseId=CASE-2847&role=P2&coverage=L3");

    await expect(page.getByTestId("coverage-badge")).toContainText("Coverage L2");
    await expect(page.getByTestId("resolved-context")).toContainText("Role P1");
    await expect(page.getByRole("button", { name: /Approval Queue/i })).toHaveCount(0);
    await expect(page.getByRole("button", { name: /approve|reject|delay|observe/i })).toHaveCount(0);
  });
});
