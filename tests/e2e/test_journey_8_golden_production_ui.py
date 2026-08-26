from playwright.sync_api import Page, expect

from backend.domain import models


def test_journey_8_golden_production_routes_are_rtl_responsive_and_real(
    page: Page, e2e_server: dict, monkeypatch
):
    monkeypatch.setattr(
        "backend.domain.services.claim_visibility.has_valid_gate", lambda *_args: True
    )
    with e2e_server["db_session"]() as session:
        snapshot = models.CorpusSnapshot(
            id="snap_e2e_ui",
            canonical_text_source="fixture",
            canonical_text_version="v1",
            canonical_text_hash="fixture-hash",
        )
        run = models.ResearchRun(
            id="run_e2e_ui",
            target_contract="ROOT_CORE",
            target_expression="علم",
            methodology_revision="method-e2e-ui",
            corpus_snapshot=snapshot.id,
            authority_context={"source": "e2e"},
            current_stage="HYPOTHESIS_GENERATION",
        )
        isolation = models.IsolationState(
            id="iso_e2e_ui",
            research_run_id=run.id,
            target_contract=run.target_contract,
            corpus_snapshot=snapshot.id,
            methodology_reference=run.methodology_revision,
            allowed_sources=["QURAN_CORPUS"],
            is_contaminated="CLEAN",
        )
        claim = models.SemanticClaim(
            id="claim_e2e_ui",
            research_run_id=run.id,
            contract_type="ROOT_CORE",
            abstract_root_core="صياغة اختبارية معلّمة صراحة",
            epistemic_state="LOCK_INTERNAL_RESULT",
            review_state="REVIEW_REQUIRED",
            freshness_state="STALE",
            publication_state="PRIVATE_WORKING",
            supporting_evidence={"refs": ["fixture:evidence"]},
            counterevidence={"refs": ["fixture:counterevidence"]},
        )
        audit = models.AuditLog(
            id="audit_e2e_ui",
            entity_id=claim.id,
            entity_type="SemanticClaim",
            action="MARK_STALE",
            actor="E2E",
            new_state="STALE",
        )
        session.add_all([snapshot, run, isolation, claim, audit])
        session.commit()

    page.goto(f"{e2e_server['base_url']}/run/run_e2e_ui")
    assert page.locator("html").get_attribute("dir") == "rtl"
    expect(page.get_by_role("heading", name="تشغيل البحث: علم")).to_be_visible()
    expect(page.get_by_text("HYPOTHESIS_GENERATION", exact=True).first).to_be_visible()
    page.get_by_role("tab", name="البوابات والنتائج").click()
    expect(page.get_by_text("LOCK_INTERNAL_RESULT", exact=True)).to_be_visible()
    expect(page.get_by_text("REVIEW_REQUIRED", exact=True)).to_be_visible()
    expect(page.get_by_text("STALE", exact=True)).to_be_visible()
    expect(page.get_by_text("PRIVATE_WORKING", exact=True)).to_be_visible()
    expect(page.get_by_role("heading", name="الأدلة المعارضة")).to_be_visible()

    page.goto(f"{e2e_server['base_url']}/claims/claim_e2e_ui")
    expect(
        page.get_by_role("heading", name="الأدلة المعارضة")
        .locator("xpath=ancestor::section[1]")
        .locator("pre")
    ).to_contain_text("fixture:counterevidence")
    expect(page.get_by_text("هذه الدعوى ليست CURRENT.", exact=True)).to_be_visible()

    page.goto(f"{e2e_server['base_url']}/audit")
    page.fill("#audit-entity-type", "SemanticClaim")
    page.fill("#audit-entity-id", "claim_e2e_ui")
    page.get_by_role("button", name="تطبيق").click()
    expect(page.get_by_role("cell", name="MARK_STALE", exact=True)).to_be_visible()

    controls = page.locator("input, select, textarea")
    for index in range(controls.count()):
        control = controls.nth(index)
        assert control.get_attribute("id") or control.get_attribute("name")

    page.set_viewport_size({"width": 390, "height": 844})
    page.goto(e2e_server["base_url"])
    menu = page.get_by_role("button", name="القائمة")
    expect(menu).to_be_visible()
    menu.click()
    expect(page.get_by_role("navigation", name="التنقل الرئيسي")).to_be_visible()
