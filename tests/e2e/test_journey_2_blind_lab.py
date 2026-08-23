import re

from playwright.sync_api import Page, expect


def test_journey_2_blind_lab(page: Page, e2e_server: dict):
    """
    Journey 2: Blind Lab Isolation & Contamination Defense
    - Enter Blind Lab -> preflight -> verify isolation -> attempt prohibited prior access -> verify blocking.
    """
    base_url = e2e_server["base_url"]

    # 1. Ask Lisan and Create ResearchRun
    page.goto(base_url)
    page.fill("input[placeholder='e.g. ضرب']", "كتب")
    page.click("button:has-text('Search')")
    expect(page.locator("h3:has-text('Insufficient Evidence')")).to_be_visible(
        timeout=10000
    )

    page.click("button:has-text('Start Research Run')")
    expect(page).to_have_url(re.compile(r".*/run/.*"))

    # Extract Run ID from URL
    run_url = page.url
    run_id = run_url.split("/")[-1]

    # Navigate to Blind Lab
    page.goto(f"{base_url}/run/{run_id}/blind")
    expect(page.locator("h1")).to_contain_text("Blind Lab Isolation")

    # 2. Preflight Isolation
    expect(page.locator("text=Isolation Preflight Required")).to_be_visible()
    page.click("button:has-text('Start Preflight Isolation')")

    # Wait for reload and verify isolation status
    expect(page.locator("span", has_text="Isolation: CLEAN")).to_be_visible(
        timeout=10000
    )

    # 3. Add observation
    page.fill("input[placeholder='e.g. past tense verb, pattern fa\\'ala']", "كُتِبَ")
    page.fill(
        "input[placeholder='e.g. transitive, takes direct object']",
        "فعل ماض مبني للمجهول",
    )
    page.once("dialog", lambda dialog: dialog.accept())  # accept the success alert
    page.click("button:has-text('Save Observation')")

    # Wait for the observation to be processed
    # In a real test, we would verify it appeared in a list, but the UI just shows an alert

    # 4. Attempt prohibited semantic read
    page.click("button:has-text('Simulate Prohibited Semantic Read')")

    # 5. Verify Isolation Remains CLEAN since the backend blocked the read
    expect(page.locator("span", has_text="Isolation: CLEAN")).to_be_visible(
        timeout=10000
    )
