from playwright.sync_api import Page, expect

from backend.domain import models


def test_journey_3_purity_check(page: Page, e2e_server: dict, monkeypatch):
    """
    Journey 3: Claim Traceability & Methodological Purity Check
    - Claim -> Evidence/Counterevidence -> ResearchRun -> CorpusSnapshot/provenance -> 8-dimension Purity report.
    """
    base_url = e2e_server["base_url"]
    TestSession = e2e_server["db_session"]
    db = TestSession()

    try:
        # Seed test research run & claim
        run = models.ResearchRun(
            id="run_trace_01",
            target_contract="ROOT_CORE",
            target_expression="رحم",
            methodology_revision="v4.0",
            corpus_snapshot="snap_tanzil_01",
            authority_context={"source": "CANONICAL"},
            status="LOCK_INTERNAL_RESULT",
        )
        db.add(run)

        isolation = models.IsolationState(
            id="iso_trace_01",
            research_run_id=run.id,
            target_contract=run.target_contract,
            corpus_snapshot=run.corpus_snapshot,
            methodology_reference=run.methodology_revision,
            allowed_sources=["QURAN_CORPUS"],
            is_contaminated="CLEAN",
        )
        db.add(isolation)

        claim = models.SemanticClaim(
            id="clm_trace_01",
            research_run_id="run_trace_01",
            contract_type="ROOT_CORE",
            abstract_root_core="الرقة والتعطف الدال على الإحسان",
            epistemic_state="LOCK_INTERNAL_RESULT",
            review_state="NOT_REVIEWED",
            freshness_state="CURRENT",
            publication_state="PRIVATE_WORKING",
        )
        db.add(claim)

        dep = models.DependencyRecord(
            id="dep_trace_01",
            dependent_claim_id="clm_trace_01",
            dependency_type="CORPUS_SNAPSHOT",
            dependency_ref="snap_tanzil_01",
        )
        db.add(dep)

        audit = models.AuditLog(
            id="aud_trace_01",
            entity_id="clm_trace_01",
            entity_type="SemanticClaim",
            action="LOCK_INTERNAL",
            actor="RESEARCHER",
        )
        db.add(audit)
        
        hyp = models.Hypothesis(
            id="hyp_trace_01",
            research_run_id="run_trace_01",
            hypothesis_type="H1",
            target_contract="ROOT_CORE",
            statement="Test hypothesis",
        )
        db.add(hyp)
        db.commit()
    finally:
        db.close()

    monkeypatch.setattr(
        "backend.domain.services.claim_visibility.has_valid_gate", lambda *_args: True
    )

    # 1. Verify Claim Provenance Read Model
    page.goto(f"{base_url}/claims/clm_trace_01")
    expect(page.get_by_text("clm_trace_01", exact=True)).to_be_visible()

    expect(page.locator("#prov-corpus")).to_contain_text("snap_tanzil_01")
    expect(page.locator("#prov-deps")).to_contain_text("1 dependencies")
    expect(page.locator("#prov-audit")).to_contain_text("LOCK_INTERNAL")

    # 2. Verify Multidimensional Quality & 8-Dimension Purity Report
    expect(page.locator("#qual-rating")).to_contain_text("CONTAMINATED")
    expect(page.locator("#qual-findings")).to_contain_text("8 findings")
    expect(page.locator("#quality-availability")).to_contain_text("UNAVAILABLE")
    expect(page.get_by_text("QualityProfile unavailable", exact=False)).to_be_visible()

    # 3. Verify Reproduction Manifest
    expect(page.locator("#man-corpus")).to_contain_text("snap_tanzil_01")
    expect(page.locator("#man-deps")).to_contain_text("1 dependencies")
