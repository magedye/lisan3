from playwright.sync_api import Page, expect

from backend.domain import models


def test_journey_6_knowledge_explorer_uses_real_graph_projection(
    page: Page, e2e_server: dict
):
    """R1: backend projection -> read-only React Flow -> provenance table."""
    db = e2e_server["db_session"]()
    try:
        methodology = models.MethodologyRevision(
            id="method-e2e-j6",
            methodology_id="method-e2e-j6",
            revision="fixture",
            lifecycle_state="CURRENT",
            authority_reference="docs/canonical/LISAN_PLATFORM_CANONICAL_IMPLEMENTATION_REFERENCE.md",
            source_reference="docs/canonical/LISAN_PLATFORM_CANONICAL_IMPLEMENTATION_REFERENCE.md",
            source_sha256="adf86e1dddf0d97d540315ce50bacfb922e1398ac1d74bc0da7c341bf7ad4086",
            allowed_use="QURAN_INTERNAL_CUMULATIVE_RUN",
            research_run_eligible=True,
        )
        run = models.ResearchRun(
            id="run_e2e_graph",
            target_contract="ROOT_CORE",
            target_expression="علم",
            methodology_revision="method-e2e",
            corpus_snapshot="snap_tanzil_1_1_ac0724796cbb",
            authority_context={"source": "e2e"},
        )
        isolation = models.IsolationState(
            id="iso_e2e_graph",
            research_run_id=run.id,
            target_contract=run.target_contract,
            corpus_snapshot="snap_tanzil_1_1_ac0724796cbb",
            methodology_reference=run.methodology_revision,
            allowed_sources=["QURAN_CORPUS"],
            is_contaminated="CLEAN",
            establishment_status="ESTABLISHED",
        )
        claim = models.SemanticClaim(
            id="claim_e2e_graph",
            research_run_id=run.id,
            contract_type="ROOT_CORE",
        )
        dependency = models.DependencyRecord(
            id="dep_e2e_graph",
            dependent_claim_id=claim.id,
            dependency_type="CORPUS_SNAPSHOT",
            dependency_ref="snap_tanzil_1_1_ac0724796cbb",
        )
        db.add_all([methodology, run, isolation, claim, dependency])
        db.commit()
    finally:
        db.close()

    rebuild = page.request.post(
        f"{e2e_server['api_url']}/runs/run_e2e_graph/knowledge-graph/rebuild"
    )
    assert rebuild.status == 200
    assert rebuild.json()["analysis"]["node_count"] > 0

    page.goto(f"{e2e_server['base_url']}/run/run_e2e_graph/knowledge")
    expect(page.locator("h1")).to_contain_text("مستكشف المعرفة")
    expect(page.get_by_test_id("knowledge-graph-flow")).to_be_visible()
    expect(page.get_by_test_id("graph-provenance-table")).to_contain_text("USES_CORPUS")
    expect(page.get_by_test_id("graph-authority-notice")).to_contain_text(
        "not semantic truth"
    )
