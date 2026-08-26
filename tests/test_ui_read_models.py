import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.domain import models
from backend.infrastructure.database import Base, get_db
from backend.main import app

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
client = TestClient(app)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def test_db():
    app.dependency_overrides[get_db] = override_get_db
    with TestingSessionLocal() as db:
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(table.delete())
        db.commit()
        yield db
    app.dependency_overrides.pop(get_db, None)


def seed_workspace(db):
    suffix = uuid.uuid4().hex[:6]
    snapshot = models.CorpusSnapshot(
        id=f"snap_ui_{suffix}",
        canonical_text_source="fixture",
        canonical_text_version="v1",
        canonical_text_hash="fixture-hash",
    )
    run = models.ResearchRun(
        id=f"run_ui_{suffix}",
        target_contract="ROOT_CORE",
        target_expression="علم",
        methodology_revision="method-ui",
        corpus_snapshot=snapshot.id,
        authority_context={"source": "test"},
    )
    isolation = models.IsolationState(
        id=f"iso_ui_{suffix}",
        research_run_id=run.id,
        target_contract=run.target_contract,
        corpus_snapshot=snapshot.id,
        methodology_reference=run.methodology_revision,
        allowed_sources=["QURAN_CORPUS"],
        is_contaminated="CLEAN",
    )
    observation = models.ObservationArtifact(
        id=f"obs_ui_{suffix}",
        research_run_id=run.id,
        occurrence_ref="occ_ui_1",
        form="فعل",
        syntax="متعد",
    )
    hypothesis = models.Hypothesis(
        id=f"hyp_ui_{suffix}",
        research_run_id=run.id,
        hypothesis_type="H1",
        target_contract="ROOT_CORE",
        scope="all occurrences",
        statement="فرضية قابلة للدحض",
        supporting_evidence_refs=[observation.id],
        counterevidence_refs=[],
        unresolved_cases=["case-1"],
        rejection_condition={
            "challenging_finding": "counterexample",
            "search_location": "corpus",
            "verification_method": "exact source check",
            "confounder_control": "same form",
            "failure_consequence": "reject hypothesis",
        },
        provenance="fixture:test_ui_read_models",
    )
    claim = models.SemanticClaim(
        id=f"claim_ui_{suffix}",
        research_run_id=run.id,
        contract_type="ROOT_CORE",
        epistemic_state="LOCK_INTERNAL_RESULT",
        review_state="NOT_REVIEWED",
        freshness_state="REVALIDATION_REQUIRED",
        publication_state="PRIVATE_WORKING",
        abstract_root_core="قراءة اختبارية",
    )
    rule = models.GovernanceRule(
        id=f"rule_ui_{suffix}",
        rule_code=f"RULE_UI_{suffix}",
        description="قاعدة اختبارية",
    )
    proposal = models.ChangeProposal(
        id=f"proposal_ui_{suffix}",
        rule_code=rule.rule_code,
        proposed_changes="تغيير مضبوط",
        impact_analysis={"affected_claims_count": 1},
        status="PROPOSED",
    )
    audit = models.AuditLog(
        id=f"audit_ui_{suffix}",
        entity_id=run.id,
        entity_type="ResearchRun",
        action="CHECKPOINT",
        actor="TEST",
    )
    db.add_all(
        [
            snapshot,
            run,
            isolation,
            observation,
            hypothesis,
            claim,
            rule,
            proposal,
            audit,
        ]
    )
    db.commit()
    return run, claim, snapshot, proposal


def test_attention_center_returns_only_persisted_records(test_db):
    run, _, snapshot, proposal = seed_workspace(test_db)

    response = client.get("/attention")

    assert response.status_code == 200
    data = response.json()
    assert [item["id"] for item in data["recent_runs"]] == [run.id]
    assert data["review_required_claims"] == []
    assert data["freshness_attention_claims"] == []
    assert [item["id"] for item in data["pending_proposals"]] == [proposal.id]
    assert [item["id"] for item in data["corpus_snapshots"]] == [snapshot.id]


def test_run_workspace_hides_claims_before_existing_lock_allows_release(test_db):
    run, claim, *_ = seed_workspace(test_db)

    response = client.get(f"/runs/{run.id}/workspace")

    assert response.status_code == 200
    data = response.json()
    assert data["run"]["id"] == run.id
    assert len(data["observations"]) == 1
    assert len(data["hypotheses"]) == 1
    assert data["claims_visible"] is False
    assert data["claims"] == []
    assert claim.id not in response.text


def test_run_workspace_exposes_claims_only_after_existing_release_checks(
    test_db, monkeypatch
):
    run, claim, *_ = seed_workspace(test_db)
    monkeypatch.setattr(
        "backend.domain.services.claim_visibility.has_valid_gate", lambda *_args: True
    )

    response = client.get(f"/runs/{run.id}/workspace")

    assert response.status_code == 200
    data = response.json()
    assert data["claims_visible"] is True
    assert [item["id"] for item in data["claims"]] == [claim.id]


def test_direct_claim_and_governance_overview_fail_closed_before_release(test_db):
    _, claim, snapshot, proposal = seed_workspace(test_db)

    claim_response = client.get(f"/claims/{claim.id}")
    overview_response = client.get("/governance/overview")

    assert claim_response.status_code == 403
    assert overview_response.status_code == 200
    overview = overview_response.json()
    assert overview["review_queue"] == []
    assert overview["freshness_queue"] == []
    assert [item["id"] for item in overview["proposals"]] == [proposal.id]
    assert [item["id"] for item in overview["corpus_snapshots"]] == [snapshot.id]


def test_direct_claim_and_governance_overview_release_after_existing_checks(
    test_db, monkeypatch
):
    _, claim, *_ = seed_workspace(test_db)
    monkeypatch.setattr(
        "backend.domain.services.claim_visibility.has_valid_gate", lambda *_args: True
    )

    claim_response = client.get(f"/claims/{claim.id}")
    overview_response = client.get("/governance/overview")

    assert claim_response.status_code == 200
    assert claim_response.json()["freshness_state"] == "REVALIDATION_REQUIRED"
    overview = overview_response.json()
    assert [item["id"] for item in overview["review_queue"]] == [claim.id]
    assert [item["id"] for item in overview["freshness_queue"]] == [claim.id]
