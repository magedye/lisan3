import re

from playwright.sync_api import Page, expect

from backend.domain.models import AuditLog, IsolationState, ResearchRun, SemanticClaim


def test_journey_7_golden_shell_and_audit(page: Page, e2e_server: dict):
    with e2e_server["db_session"]() as session:
        session.add_all(
            [
                ResearchRun(
                    id="run_e2e_status_axes",
                    target_contract="ROOT_CORE",
                    target_expression="نور",
                    methodology_revision="v4.0",
                    corpus_snapshot="snap_e2e_status_axes",
                    authority_context={"source": "e2e"},
                ),
                SemanticClaim(
                    id="claim_e2e_status_axes",
                    research_run_id="run_e2e_status_axes",
                    contract_type="ROOT_CORE",
                    research_state="PREFERRED",
                    canonical_state="NOT_CANONICAL",
                    verification_state="NOT_VERIFIED",
                ),
                IsolationState(
                    id="isolation_e2e_status_axes",
                    research_run_id="run_e2e_status_axes",
                    target_contract="ROOT_CORE",
                    corpus_snapshot="snap_e2e_status_axes",
                    methodology_reference="v4.0",
                    allowed_sources=["QURAN_CORPUS"],
                    is_contaminated="CLEAN",
                    establishment_status="ESTABLISHED",
                ),
                AuditLog(
                    id="aud_e2e_golden_shell",
                    entity_id="route_audit",
                    entity_type="RouteSmoke",
                    action="READ_MODEL_AVAILABLE",
                    actor="E2E",
                    new_state="VERIFIED",
                ),
            ]
        )
        session.commit()

    page.goto(e2e_server["base_url"])
    expect(page.get_by_role("navigation", name="التنقل الرئيسي")).to_be_visible()
    expect(
        page.get_by_role("heading", name="مركز الانتباه — اسأل لسان (Ask Lisan)")
    ).to_be_visible()
    expect(page.locator(".status-badge.status-positive")).to_contain_text(
        "بيانات فعلية فقط"
    )

    page.get_by_placeholder("e.g. ضرب").fill("نور")
    page.get_by_role("button", name="Search — بحث").click()

    found_claim = page.locator(".found-panel")
    expect(found_claim).to_be_visible()
    expect(found_claim).to_contain_text("حالة البحث")
    expect(found_claim).to_contain_text("PREFERRED")
    expect(found_claim).to_contain_text("الحالة المعتمدة")
    expect(found_claim).to_contain_text("NOT_CANONICAL")
    expect(found_claim).to_contain_text("التحقق")
    expect(found_claim).to_contain_text("NOT_VERIFIED")

    page.get_by_role("link", name=re.compile("التشغيل والتدقيق")).first.click()
    expect(page).to_have_url(f"{e2e_server['base_url']}/audit")
    expect(page.get_by_role("heading", name="سجل التدقيق")).to_be_visible()
    expect(page.get_by_text("RouteSmoke", exact=True)).to_be_visible()
    expect(
        page.get_by_role("cell", name="READ_MODEL_AVAILABLE", exact=True)
    ).to_be_visible()
