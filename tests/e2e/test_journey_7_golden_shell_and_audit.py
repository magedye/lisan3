from playwright.sync_api import Page, expect

from backend.domain.models import AuditLog


def test_journey_7_golden_shell_and_real_audit(page: Page, e2e_server: dict):
    session_factory = e2e_server["db_session"]
    with session_factory() as session:
        session.add(
            AuditLog(
                id="aud_e2e_golden_shell",
                entity_id="route_audit",
                entity_type="RouteSmoke",
                action="READ_MODEL_AVAILABLE",
                actor="E2E",
                new_state="VERIFIED",
            )
        )
        session.commit()

    page.goto(e2e_server["base_url"])
    expect(page.get_by_role("navigation", name="التنقل الرئيسي")).to_be_visible()
    expect(page.get_by_role("heading", name="مركز الانتباه — اسأل لسان (Ask Lisan)")).to_be_visible()
    expect(page.get_by_text("لا بيانات نموذجية", exact=True)).to_be_visible()

    page.get_by_role("link", name="سجل التدقيق").first.click()
    expect(page).to_have_url(f"{e2e_server['base_url']}/audit")
    expect(page.get_by_role("heading", name="سجل التدقيق")).to_be_visible()
    expect(page.get_by_text("RouteSmoke", exact=True)).to_be_visible()
    expect(page.get_by_text("READ_MODEL_AVAILABLE", exact=True)).to_be_visible()
