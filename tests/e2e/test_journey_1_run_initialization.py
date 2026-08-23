import re
from playwright.sync_api import Page, expect

def test_journey_1_run_initialization(page: Page, e2e_server: dict):
    """
    Journey 1: Governed Research
    - Ask Lisan -> insufficient evidence -> create ResearchRun -> verify persisted run state.
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
    
    # 2. Start a Governed ResearchRun
    page.click("button:has-text('Start Research Run')")
        
    # 3. Verify navigation to the run page
    expect(page).to_have_url(re.compile(r".*/run/.*"))
    expect(page.locator("span", has_text="PREFLIGHT")).to_be_visible()
