from playwright.sync_api import Page


def test_journey_2_blind_lab(page: Page, e2e_server: dict):
    """
    Journey 2: Blind Lab Isolation & Contamination Defense
    - Enter Blind Lab -> preflight -> verify isolation -> attempt prohibited prior access -> verify blocking.
    """
    base_url = e2e_server["base_url"]

    # 1. Create a ResearchRun
    run_res = page.request.post(
        f"{base_url}/runs",
        data={
            "target_contract": "ROOT_CORE",
            "target_expression": "كتب",
            "methodology_revision": "v4.0",
            "corpus_snapshot": "snap_canonical_01",
            "authority_context": {"initiator": "governed_researcher"},
        },
    )
    assert run_res.status == 200
    run_id = run_res.json()["id"]

    # 2. Enter Blind Lab & Run Preflight
    preflight_res = page.request.post(
        f"{base_url}/runs/{run_id}/blind/preflight",
        data={
            "target_contract": "ROOT_CORE",
            "corpus_snapshot": "snap_canonical_01",
            "methodology_reference": "v4.0",
            "allowed_sources": ["QURAN_CORPUS"],
        },
    )
    assert preflight_res.status == 200
    iso_data = preflight_res.json()
    assert iso_data["is_contaminated"] == "CLEAN"

    # 3. Add valid structural observation
    obs_res = page.request.post(
        f"{base_url}/runs/{run_id}/observations",
        data={
            "occurrence_ref": "2:183:4",
            "form": "كُتِبَ",
            "syntax": "فعل ماض مبني للمجهول",
            "participant_roles": "المكتوب عليه: الصيام",
            "local_context": "كتب عليكم الصيام",
            "unresolved_ambiguity": "None",
        },
    )
    assert obs_res.status == 200

    # 4. Attempt prohibited semantic dictionary read before Internal Lock
    dict_res = page.request.get(f"{base_url}/runs/{run_id}/read_semantic_dictionary")
    assert dict_res.status == 403
    assert "Semantic knowledge cannot be accessed before authoritative internal lock" in dict_res.json()["detail"]

    # 5. Verify isolation status remains monitored
    iso_check = page.request.get(f"{base_url}/runs/{run_id}/blind")
    assert iso_check.status == 200
    assert iso_check.json()["is_contaminated"] == "CLEAN"

