import re

from playwright.sync_api import Page, expect


def test_journey_1_run_initialization(page: Page, e2e_server: dict):
    """
    Journey 1: Governed Research entry boundary
    - Ask Lisan -> insufficient evidence -> exact governed Run Builder choices.
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

    # 2. Methodology and Corpus are resolved automatically by the host.
    import pathlib

    token = pathlib.Path(".lisan_owner_token").read_text(encoding="utf-8").strip()
    rejected = page.request.post(
        f"{e2e_server['api_url']}/runs",
        headers={"X-Lisan-Owner-Token": token},
        data={
            "target_contract": "ROOT_CORE",
            "target_expression": "ضرب",
            "methodology_revision": "ARBITRARY_METHOD",
            "corpus_snapshot": "NONEXISTENT_SNAPSHOT",
            "authority_context": {"source": "e2e"},
        },
    )
    assert rejected.status == 422

    page.get_by_role("button", name="Start Research Run — ابدأ تشغيل بحث").click()
    expect(page).to_have_url(re.compile(r"/run/run_[0-9a-f]+$"))
