import { expect, test } from "@playwright/test";

async function selectPhase(page: import("@playwright/test").Page, phase: string) {
  await page.getByLabel("Mock fixture phase").selectOption(phase);
}

test.describe("LC-P core surface phase seeds", () => {
  test("resolves P1, P2, terminal, and P3 phases from the fixture context only", async ({
    page
  }) => {
    await page.goto("/case/CASE-2847");

    const resolvedContext = page.getByTestId("resolved-context");
    await expect(page.getByTestId("coverage-badge")).toContainText("Coverage L2");
    await expect(page.getByTestId("case-detail-surface")).toBeVisible();
    await expect(resolvedContext).toContainText("Role P1");
    await expect(resolvedContext).toContainText("P1_CASE_DETAIL");
    await expect(resolvedContext).toContainText("UNDER_INVESTIGATION");

    await selectPhase(page, "1");
    await expect(resolvedContext).toContainText("Role P1");
    await expect(resolvedContext).toContainText("P1_CASE_DETAIL");
    await expect(resolvedContext).toContainText("PENDING_APPROVAL");
    await expect(page.getByTestId("action-request-panel")).toContainText("Waiting on P2");

    await selectPhase(page, "3");
    await expect(resolvedContext).toContainText("Role P2");
    await expect(resolvedContext).toContainText("P2_APPROVAL");
    await expect(resolvedContext).toContainText("OBSERVATION_WINDOW");
    await expect(page.getByTestId("case-state-pill")).toContainText("Observation window");
    await expect(page.getByTestId("action-request-panel")).toContainText("OBSERVATION_WINDOW");

    await selectPhase(page, "4");
    await expect(resolvedContext).toContainText("PENDING_APPROVAL");
    await expect(page.getByTestId("case-state-pill")).toContainText("Pending P2 review");

    await selectPhase(page, "5");
    await expect(resolvedContext).toContainText("APPROVED_PENDING_EXECUTION");
    await expect(page.getByTestId("case-state-pill")).toContainText("Approved pending execution");
    await expect(page.getByRole("button", { name: /withdraw/i })).toHaveCount(0);

    await selectPhase(page, "6");
    await expect(resolvedContext).toContainText("Role P3");
    await expect(resolvedContext).toContainText("P3_MANAGER");
    await expect(page.getByTestId("case-state-pill")).toContainText("Approved pending execution");
  });
});
