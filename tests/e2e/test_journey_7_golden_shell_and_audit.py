from playwright.sync_api import Page, expect

from backend.domain.models import AuditLog, ResearchRun, SemanticClaim


def test_journey_7_golden_shell_and_real_audit(page: Page, e2e_server: dict):
    session_factory = e2e_server["db_session"]
    with session_factory() as session:
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
                    epistemic_state="LOCK_INTERNAL_RESULT",
                    review_state="NOT_REVIEWED",
                    freshness_state="REVALIDATION_REQUIRED",
                    publication_state="PRIVATE_WORKING",
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
    expect(page.get_by_role("heading", name="مركز الانتباه — اسأل لسان (Ask Lisan)")).to_be_visible()
    expect(page.get_by_text("لا بيانات نموذجية", exact=True)).to_be_visible()

    page.get_by_placeholder("e.g. ضرب").fill("نور")
    page.get_by_role("button", name="Search — بحث").click()
    found_claim = page.locator(".found-panel")
    expect(found_claim).to_contain_text("المعرفي")
    expect(found_claim).to_contain_text("LOCK_INTERNAL_RESULT")
    expect(found_claim).to_contain_text("المراجعة")
    expect(found_claim).to_contain_text("NOT_REVIEWED")
    expect(found_claim).to_contain_text("الحداثة")
    expect(found_claim).to_contain_text("REVALIDATION_REQUIRED")
    expect(found_claim).to_contain_text("النشر")
    expect(found_claim).to_contain_text("PRIVATE_WORKING")

    page.get_by_role("link", name="سجل التدقيق").first.click()
    expect(page).to_have_url(f"{e2e_server['base_url']}/audit")
    expect(page.get_by_role("heading", name="سجل التدقيق")).to_be_visible()
    expect(page.get_by_text("RouteSmoke", exact=True)).to_be_visible()
    expect(page.get_by_text("READ_MODEL_AVAILABLE", exact=True)).to_be_visible()
