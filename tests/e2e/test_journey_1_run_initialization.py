from playwright.sync_api import Page


def test_journey_1_run_initialization(page: Page, e2e_server: dict):
    """
    Journey 1: Governed Research
    - Ask Lisan -> insufficient evidence -> create ResearchRun -> verify persisted run state.
    """
    base_url = e2e_server["base_url"]

    # 1. Ask Lisan for an expression with no prior lock
    ask_res = page.request.post(
        f"{base_url}/ask",
        data={"expression": "ضرب", "contract_type": "ROOT_CORE"},
    )
    assert ask_res.status == 200
    ask_data = ask_res.json()
    assert ask_data["status"] == "INSUFFICIENT_EVIDENCE"
    assert ask_data["claim"] is None

    # 2. Start a Governed ResearchRun
    run_res = page.request.post(
        f"{base_url}/runs",
        data={
            "target_contract": "ROOT_CORE",
            "target_expression": "ضرب",
            "methodology_revision": "v4.0",
            "corpus_snapshot": "snap_initial",
            "authority_context": {"initiator": "governed_researcher"},
        },
    )
    assert run_res.status == 200
    run_data = run_res.json()
    run_id = run_data["id"]
    assert run_data["target_expression"] == "ضرب"
    assert run_data["current_stage"] == "PREFLIGHT"
    assert run_data["status"] == "ACTIVE"

    # 3. Fetch and verify persisted run state
    get_res = page.request.get(f"{base_url}/runs/{run_id}")
    assert get_res.status == 200
    persisted_run = get_res.json()
    assert persisted_run["id"] == run_id
    assert persisted_run["target_contract"] == "ROOT_CORE"
    assert persisted_run["target_expression"] == "ضرب"

