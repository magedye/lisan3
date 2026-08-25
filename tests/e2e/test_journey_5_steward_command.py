from playwright.sync_api import Page, expect


def test_journey_5_steward_command(page: Page, e2e_server: dict):
    """
    Journey 5: Steward Command, Authority Boundaries, and Invariant Defense
    - Intent -> structured command -> governed execution -> audit log -> verify forbidden action fails.
    """
    base_url = e2e_server["base_url"]

    # Navigate to Steward Center
    page.goto(f"{base_url}/steward")
    expect(page.locator("h1")).to_contain_text("Steward Command Center")

    # 1. Preview and execute a valid governed Steward command
    page.fill("#steward-command-type", "METHODOLOGY_DIRECTIVE")
    page.fill("#steward-intent", "Request explicit negative boundary verification")
    page.fill("#steward-parameters", '{"scope":"CURRENT_RUN"}')
    page.click("button:has-text('Preview Governed Command')")
    page.click("button:has-text('Execute Command')")
    page.get_by_role("button", name="إرسال للتحقق والتنفيذ").click()
    expect(page.locator("#cmd-status")).to_contain_text("SUCCESS", timeout=10000)

    # 2. Verify Audit Log recorded the Steward action
    page.click("button:has-text('View Audit Logs')")
    expect(page.locator(".log-actor").first).to_contain_text("STEWARD")
    expect(page.locator(".log-action").first).to_contain_text("EXECUTE")

    # 3. Attempt Forbidden Steward Action (Force semantic truth / bypass invariants)
    page.fill("#steward-command-type", "FORCE_ESTABLISH_SEMANTIC_TRUTH")
    page.fill("#steward-intent", "Bypass gate check and force lock directly")
    page.fill("#steward-parameters", "{}")
    page.click("button:has-text('Preview Governed Command')")
    page.click("button:has-text('Execute Command')")
    page.get_by_role("button", name="إرسال للتحقق والتنفيذ").click()
    expect(page.locator("#cmd-error")).to_contain_text(
        "violates immutable domain constraints", ignore_case=True, timeout=10000
    )
