import re

from playwright.sync_api import Page, expect

from backend.domain import models


def test_journey_2_blind_lab(page: Page, e2e_server: dict):
    """
    Journey 2: Blind Lab Isolation & Contamination Defense
    - Enter Blind Lab -> preflight -> verify isolation -> attempt prohibited prior access -> verify blocking.
    """
    base_url = e2e_server["base_url"]
    with e2e_server["db_session"]() as session:
        session.add_all(
            [
                models.MethodologyRevision(
                    id="method-e2e-j2",
                    methodology_id="method-e2e-j2",
                    revision="fixture",
                    lifecycle_state="CURRENT",
                    authority_reference="docs/canonical/LISAN_PLATFORM_CANONICAL_IMPLEMENTATION_REFERENCE.md",
                    source_reference="docs/canonical/LISAN_PLATFORM_CANONICAL_IMPLEMENTATION_REFERENCE.md",
                    source_sha256="adf86e1dddf0d97d540315ce50bacfb922e1398ac1d74bc0da7c341bf7ad4086",
                    allowed_use="QURAN_INTERNAL_CUMULATIVE_RUN",
                    research_run_eligible=True,
                ),
                models.CorpusOccurrence(
                    id="occ_e2e_blind_j2",
                    snapshot_id="snap_tanzil_1_1_ac0724796cbb",
                    expression="كتب",
                    verse_ref="fixture:1",
                    text="نص قرآني تجريبي مميز صراحة للاختبار",
                ),
                models.ResearchRun(
                    id="run_e2e_blind",
                    target_contract="ROOT_CORE",
                    target_expression="كتب",
                    methodology_revision="method-e2e-j2",
                    corpus_snapshot="snap_tanzil_1_1_ac0724796cbb",
                    authority_context={"source": "explicit-e2e-fixture"},
                ),
            ]
        )
        session.commit()

    # 1. Exercise an explicitly seeded fixture run; production Run Builder is
    # unavailable until canonical Corpus and Methodology authority exists.
    run_id = "run_e2e_blind"

    # Navigate to Blind Lab
    page.goto(f"{base_url}/run/{run_id}/blind")
    expect(page.locator("h1")).to_contain_text("المختبر المعزول")

    # 2. Preflight Isolation
    expect(page.get_by_role("heading", name="فحص العزل مطلوب")).to_be_visible()
    page.click("button:has-text('Start Preflight Isolation')")

    # Wait for reload and verify isolation status
    expect(page.get_by_label("العزل: CLEAN")).to_be_visible(timeout=10000)

    # 3. Add observation
    page.fill("input[placeholder='e.g. past tense verb, pattern fa\\'ala']", "كُتِبَ")
    page.fill(
        "input[placeholder='e.g. transitive, takes direct object']",
        "فعل ماض مبني للمجهول",
    )
    page.click("button:has-text('Save Observation')")
    expect(page.get_by_text(re.compile("سُجلت الملاحظة البنيوية"))).to_be_visible()

    # 4. Attempt prohibited semantic read
    blocked = page.request.get(
        f"{e2e_server['api_url']}/runs/{run_id}/read_semantic_dictionary"
    )
    assert blocked.status == 403

    # 5. Verify Isolation Remains CLEAN since the backend blocked the read
    page.reload()
    expect(page.get_by_label("العزل: CLEAN")).to_be_visible(timeout=10000)
