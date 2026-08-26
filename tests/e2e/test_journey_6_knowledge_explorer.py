from playwright.sync_api import Page, expect

from backend.domain import models


def test_journey_6_knowledge_explorer_uses_real_graph_projection(
    page: Page, e2e_server: dict, monkeypatch
):
    """R1: backend projection -> read-only React Flow -> provenance table."""
    monkeypatch.setattr(
        "backend.domain.services.claim_visibility.has_valid_gate", lambda *_args: True
    )
    db = e2e_server["db_session"]()
    try:
        snapshot = models.CorpusSnapshot(
            id="snap_e2e_graph",
            canonical_text_source="fixture",
            canonical_text_version="v1",
            canonical_text_hash="fixture-hash",
        )
        run = models.ResearchRun(
            id="run_e2e_graph",
            target_contract="ROOT_CORE",
            target_expression="علم",
            methodology_revision="method-e2e",
            corpus_snapshot=snapshot.id,
            authority_context={"source": "e2e"},
        )
        isolation = models.IsolationState(
            id="iso_e2e_graph",
            research_run_id=run.id,
            target_contract=run.target_contract,
            corpus_snapshot=snapshot.id,
            methodology_reference=run.methodology_revision,
            allowed_sources=["QURAN_CORPUS"],
            is_contaminated="CLEAN",
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
            dependency_ref=snapshot.id,
        )
        db.add_all([snapshot, run, isolation, claim, dependency])
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
