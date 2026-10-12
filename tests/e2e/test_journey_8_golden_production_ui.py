from playwright.sync_api import Page, expect

from backend.domain import models


def test_journey_8_golden_production_routes_are_rtl_responsive_and_real(
    page: Page, e2e_server: dict
):
    with e2e_server["db_session"]() as session:
        methodology = models.MethodologyRevision(
            id="method-e2e-j8",
            methodology_id="method-e2e-j8",
            revision="fixture",
            lifecycle_state="CURRENT",
            authority_reference="docs/canonical/LISAN_PLATFORM_CANONICAL_IMPLEMENTATION_REFERENCE.md",
            source_reference="docs/canonical/LISAN_PLATFORM_CANONICAL_IMPLEMENTATION_REFERENCE.md",
            source_sha256="adf86e1dddf0d97d540315ce50bacfb922e1398ac1d74bc0da7c341bf7ad4086",
            allowed_use="QURAN_INTERNAL_CUMULATIVE_RUN",
            research_run_eligible=True,
        )
        run = models.ResearchRun(
            id="run_e2e_ui",
            target_contract="ROOT_CORE",
            target_expression="علم",
            methodology_revision="method-e2e-ui-j8",
            corpus_snapshot="snap_tanzil_1_1_ac0724796cbb",
            authority_context={"source": "e2e"},
            current_stage="RESEARCH",
        )
        isolation = models.IsolationState(
            id="iso_e2e_ui",
            research_run_id=run.id,
            target_contract=run.target_contract,
            corpus_snapshot="snap_tanzil_1_1_ac0724796cbb",
            methodology_reference=run.methodology_revision,
            allowed_sources=["QURAN_CORPUS"],
            is_contaminated="CLEAN",
            establishment_status="ESTABLISHED",
        )
        claim = models.SemanticClaim(
            id="claim_e2e_ui",
            research_run_id=run.id,
            contract_type="ROOT_CORE",
            research_state="PREFERRED",
            canonical_state="NOT_CANONICAL",
            verification_state="NOT_VERIFIED",
            supporting_evidence=["fixture:evidence"],
            counterevidence=["fixture:counterevidence"],
        )
        audit = models.AuditLog(
            id="audit_e2e_ui",
            entity_id=claim.id,
            entity_type="SemanticClaim",
            action="MARK_STALE",
            actor="E2E",
            new_state="STALE",
        )
        session.add_all([methodology, run, isolation, claim, audit])
        session.commit()

    page.goto(f"{e2e_server['base_url']}/run/run_e2e_ui")
    assert page.locator("html").get_attribute("dir") == "rtl"
    expect(page.get_by_role("heading", name="تشغيل البحث: علم")).to_be_visible()
    expect(page.get_by_text("RESEARCH", exact=True).first).to_be_visible()
    page.get_by_role("tab", name="الأحكام البحثية").click()
    expect(page.get_by_text("PREFERRED", exact=True).first).to_be_visible()
    expect(page.get_by_text("NOT_CANONICAL", exact=True).first).to_be_visible()
    expect(page.get_by_role("heading", name="الأدلة المعارضة").first).to_be_visible()

    page.goto(f"{e2e_server['base_url']}/claims/claim_e2e_ui")
    expect(
        page.get_by_role("heading", name="الأدلة المعارضة")
        .locator("xpath=ancestor::section[1]")
        .locator("pre")
    ).to_contain_text("fixture:counterevidence")
    expect(page.get_by_text("claim_e2e_ui", exact=True)).to_be_visible()

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
