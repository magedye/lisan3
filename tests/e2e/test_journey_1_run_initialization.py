from playwright.sync_api import Page, expect


def test_journey_1_run_initialization(page: Page, e2e_server: dict):
    """
    Journey 1: Governed Research entry boundary
    - Ask Lisan -> insufficient evidence -> honest Run Builder unavailable state.
    """
    base_url = e2e_server["base_url"]

    # 1. Ask Lisan for an expression with no prior lock
    page.goto(base_url)
    expect(page.locator("h1")).to_contain_text("اسأل لسان (Ask Lisan)")

    # Fill out the form
    page.fill("input[placeholder='e.g. ضرب']", "ضرب")
    page.select_option("select", "ROOT_CORE")

    # Click search and wait for result
    page.click("button:has-text('Search')")

    # Expect insufficient evidence message
    expect(page.locator("h3:has-text('Insufficient Evidence')")).to_be_visible()

    # 2. A governed Methodology revision exists, but current canonical authority
    # has no admitted production Corpus, so no Run Builder controls are exposed.
    unavailable = page.locator("#run-admission-unavailable")
    expect(unavailable).to_contain_text("Run Builder unavailable")
    expect(unavailable).to_contain_text(
        "No authority-verified, production-active CorpusSnapshot"
    )
    expect(page.locator("#run-methodology")).to_have_count(0)
    expect(page.locator("#run-corpus")).to_have_count(0)

    rejected = page.request.post(
        f"{e2e_server['api_url']}/runs",
        data={
            "target_contract": "ROOT_CORE",
            "target_expression": "ضرب",
            "methodology_revision": "ARBITRARY_METHOD",
            "corpus_snapshot": "NONEXISTENT_SNAPSHOT",
            "authority_context": {"source": "e2e"},
        },
    )
    assert rejected.status == 422
