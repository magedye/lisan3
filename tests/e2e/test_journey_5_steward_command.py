from playwright.sync_api import Page


def test_journey_5_steward_command(page: Page, e2e_server: dict):
    """
    Journey 5: Steward Command, Authority Boundaries, and Invariant Defense
    - Intent -> structured command -> governed execution -> audit log -> verify forbidden action fails.
    """
    base_url = e2e_server["base_url"]

    # 1. Execute Valid Governed Steward Command
    steward_res = page.request.post(
        f"{base_url}/steward/commands",
        data={
            "command_type": "METHODOLOGY_DIRECTIVE",
            "intent": "Mandate explicit negative boundary distinction before lock",
            "parameters": {"scope": "ALL_RUNS", "priority": "HIGH"},
        },
    )
    assert steward_res.status == 200
    cmd_data = steward_res.json()
    assert cmd_data["execution_status"] == "SUCCESS"
    cmd_id = cmd_data["id"]

    # 2. Verify Audit Log recorded the Steward action
    audit_res = page.request.get(f"{base_url}/audit?entity_type=StewardCommand&entity_id={cmd_id}")
    assert audit_res.status == 200
    audit_logs = audit_res.json()
    assert len(audit_logs) == 1
    assert audit_logs[0]["actor"] == "STEWARD"
    assert audit_logs[0]["action"] == "EXECUTE"

    # 3. Attempt Forbidden Steward Action (Force semantic truth / bypass invariants)
    forbidden_res = page.request.post(
        f"{base_url}/steward/commands",
        data={
            "command_type": "FORCE_ESTABLISH_SEMANTIC_TRUTH",
            "intent": "Bypass gate check and force lock directly",
            "parameters": {"target_expression": "اختلاق"},
        },
    )
    assert forbidden_res.status in [400, 403]
    assert "violates immutable domain constraints" in forbidden_res.json()["detail"].lower()

