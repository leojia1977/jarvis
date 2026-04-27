import { expect, test, type Page } from "@playwright/test";

const OVER_CERTAIN_MANAGER_COPY =
  /\u5b8c\u5168\u53d7\u63a7|\u5df2\u5f7b\u5e95\u6d88\u9664/i;

const POISON_PILL_FIXTURE_IDS = [
  "poison-missing-surface",
  "poison-unsupported-surface",
  "poison-surface-role-mismatch",
  "poison-p1-action-mode-immediate",
  "poison-p1-p2-only-action-permission",
  "poison-p3-host-raw-evidence-payload",
  "poison-fixture-meta-real-data-derived",
  "poison-invalid-enum-case-state",
  "poison-invalid-enum-ar-status",
  "poison-missing-fixture-meta",
  "poison-unknown-top-level-authority-field"
];

async function openRedlineFixture(page: Page, fixtureId: string) {
  await page.goto("/case/CASE-2847");
  await page.getByLabel("Mock redline fixture").selectOption(fixtureId);
  await expect(page.getByTestId("app-redline-renderability")).toBeVisible();
}

test.describe("LC-B and LC-N static redline expansion", () => {
  test("renders missing-signal notice from ui_messages without unlocking hidden data", async ({
    page
  }) => {
    await openRedlineFixture(page, "boundary-p2-cmdb-tags-unavailable");

    const notice = page.getByTestId("missing-signal-notice");
    await expect(notice).toBeVisible();
    await expect(notice).toHaveAttribute("data-message-source", "ui_messages");
    await expect(page.getByTestId("app-redline-renderability")).toContainText(
      "boundary-p2-cmdb-tags-unavailable"
    );
    await expect(page.getByTestId("host-raw-evidence")).toHaveCount(0);
    await expect(page.getByRole("button", { name: /approve|reject|delay|observe/i })).toHaveCount(
      0
    );
  });

  test("renders stale-approve concurrency warning as static read-only feedback", async ({
    page
  }) => {
    await openRedlineFixture(page, "boundary-concurrency-stale-approve-rejected");

    const warning = page.getByTestId("concurrency-inline-warning");
    await expect(warning).toBeVisible();
    await expect(warning).toHaveAttribute("aria-disabled", "true");
    await expect(warning).toHaveAttribute("data-concurrency-state", "stale-approve-rejected");
    await expect(page.getByRole("button", { name: /approve|reject|delay|observe/i })).toHaveCount(
      0
    );
  });

  test("keeps blast radius off when resolver degradation is bounded by L1", async ({ page }) => {
    await openRedlineFixture(page, "resolver-l1-blast-radius-payload");

    await expect(page.getByTestId("coverage-badge")).toContainText("Coverage L1");
    await expect(page.getByTestId("resolver-degradation-notice")).toBeVisible();
    await expect(page.getByTestId("blast-radius-redline")).toHaveAttribute(
      "data-visibility-state",
      "OFF"
    );
    await expect(page.getByTestId("blast-radius-redline")).not.toContainText(
      /blast radius payload/i
    );
  });

  test("renders cautious P3 manager summary without raw host evidence", async ({ page }) => {
    await openRedlineFixture(page, "resolver-p3-technical-detail-redaction");

    const summary = page.getByTestId("manager-summary");
    await expect(summary).toBeVisible();
    await expect(summary).not.toContainText(OVER_CERTAIN_MANAGER_COPY);
    await expect(page.getByTestId("host-raw-evidence")).toHaveCount(0);
  });

  test("does not expose poison-pill fixtures through the app redline selector", async ({ page }) => {
    await page.goto("/case/CASE-2847");

    const redlineSelector = page.locator("#mock-redline-selector");
    const redlineOptions = redlineSelector.locator("option");
    await expect(redlineSelector).toBeVisible();
    await expect(redlineOptions).not.toHaveCount(0);

    const optionValues = await redlineOptions.evaluateAll((options) =>
      options.map((option) => (option as HTMLOptionElement).value)
    );

    for (const fixtureId of POISON_PILL_FIXTURE_IDS) {
      expect(optionValues).not.toContain(fixtureId);
    }
  });
});
