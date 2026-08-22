from playwright.sync_api import Page

from backend.domain import models


def test_journey_3_purity_check(page: Page, e2e_server: dict):
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
        db.commit()
    finally:
        db.close()

    # 1. Verify Claim Provenance Read Model
    prov_res = page.request.get(f"{base_url}/claims/clm_trace_01/provenance")
    assert prov_res.status == 200
    prov_data = prov_res.json()
    assert prov_data["claim"]["id"] == "clm_trace_01"
    assert prov_data["corpus_snapshot"] == "snap_tanzil_01"
    assert len(prov_data["dependencies"]) == 1
    assert len(prov_data["audit_trail"]) == 1

    # 2. Verify Multidimensional Quality & 8-Dimension Purity Report
    qual_res = page.request.get(f"{base_url}/claims/clm_trace_01/quality")
    assert qual_res.status == 200
    qual_data = qual_res.json()
    assert qual_data["purity_score"] == 100
    assert qual_data["purity_rating"] == "PURE"
    assert len(qual_data["purity_findings"]) == 8

    # 3. Verify Reproduction Manifest
    manifest_res = page.request.get(f"{base_url}/claims/clm_trace_01/reproduction_manifest")
    assert manifest_res.status == 200
    manifest_data = manifest_res.json()
    assert manifest_data["claim_id"] == "clm_trace_01"
    assert manifest_data["corpus_snapshot_id"] == "snap_tanzil_01"
    assert len(manifest_data["dependencies"]) == 1

