import { test, expect } from "@playwright/test";

test.describe("Automated Sandbox Verification Suite", () => {
  test("Visual & Functional Invariants", async ({ page }) => {
    const errorLogs: string[] = [];
    page.on("console", (msg) => {
      if (msg.type() === "error") errorLogs.push(msg.text());
    });
    page.on("pageerror", (err) => errorLogs.push(err.message));

    // 1. Navigation & Hydration
    const response = await page.goto("http://localhost:4173", {
      waitUntil: "networkidle",
    });
    expect(response?.status()).toBe(200);

    // 2. Zero Uncaught Console Errors
    expect(errorLogs).toEqual([]);

    // 3. Document Title Presence
    await expect(page).toHaveTitle(/^(?!\s*$).+/);

    // 4. Layout Overflow Detection (Zero Horizontal Scrollbar)
    const isOverflowing = await page.evaluate(() => {
      return document.documentElement.scrollWidth > window.innerWidth;
    });
    expect(isOverflowing).toBe(false);

    // 5. Visual Artifact Capture
    await page.screenshot({ path: "/tmp/artifacts/preview.png", fullPage: true });
  });
});
