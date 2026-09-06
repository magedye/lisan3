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


def seed_workspace(db, *, contaminated: bool = False):
    """Seed a run whose Research Judgment is release-gated only by the source
    boundary (Blind Lab isolation), not by any lifecycle lock or gate."""
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
        is_contaminated="PRIOR_CONTAMINATED" if contaminated else "CLEAN",
        contamination_reason="actual prohibited-source read" if contaminated else None,
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
        research_state="PREFERRED",
        canonical_state="NOT_CANONICAL",
        result_strength="STRONG",
        verification_state="NOT_VERIFIED",
        preferred_conclusion="قراءة اختبارية",
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
        [snapshot, run, isolation, observation, hypothesis, claim, rule, proposal, audit]
    )
    db.commit()
    return run, claim, snapshot, proposal


def test_attention_center_returns_only_persisted_records(test_db):
    run, claim, snapshot, proposal = seed_workspace(test_db)

    response = client.get("/attention")

    assert response.status_code == 200
    data = response.json()
    assert [item["id"] for item in data["recent_runs"]] == [run.id]
    # A STRONG preferred, not-yet-canonical judgment on a clean run is a real
    # canonicalization candidate.
    assert [item["id"] for item in data["canonicalization_candidates"]] == [claim.id]
    assert data["reopen_required_claims"] == []
    assert [item["id"] for item in data["pending_proposals"]] == [proposal.id]
    assert [item["id"] for item in data["corpus_snapshots"]] == [snapshot.id]
    assert "run_admission" in data


def test_run_workspace_hides_judgments_when_source_boundary_is_contaminated(test_db):
    run, claim, *_ = seed_workspace(test_db, contaminated=True)

    response = client.get(f"/runs/{run.id}/workspace")

    assert response.status_code == 200
    data = response.json()
    assert data["run"]["id"] == run.id
    assert len(data["observations"]) == 1
    assert len(data["hypotheses"]) == 1
    assert data["judgments_visible"] is False
    assert data["research_judgments"] == []
    assert claim.id not in response.text


def test_run_workspace_exposes_judgments_when_isolation_is_clean(test_db):
    run, claim, *_ = seed_workspace(test_db)

    response = client.get(f"/runs/{run.id}/workspace")

    assert response.status_code == 200
    data = response.json()
    assert data["judgments_visible"] is True
    assert [item["id"] for item in data["research_judgments"]] == [claim.id]


def test_direct_judgment_and_overview_fail_closed_when_contaminated(test_db):
    _, claim, snapshot, proposal = seed_workspace(test_db, contaminated=True)

    judgment_response = client.get(f"/judgments/{claim.id}")
    overview_response = client.get("/governance/overview")

    assert judgment_response.status_code == 403
    assert overview_response.status_code == 200
    overview = overview_response.json()
    assert overview["canonicalization_candidates"] == []
    assert overview["reopen_required"] == []
    assert [item["id"] for item in overview["proposals"]] == [proposal.id]
    assert [item["id"] for item in overview["corpus_snapshots"]] == [snapshot.id]


def test_direct_judgment_and_overview_release_when_isolation_is_clean(test_db):
    _, claim, *_ = seed_workspace(test_db)

    judgment_response = client.get(f"/judgments/{claim.id}")
    overview_response = client.get("/governance/overview")

    assert judgment_response.status_code == 200
    assert judgment_response.json()["research_state"] == "PREFERRED"
    overview = overview_response.json()
    assert [item["id"] for item in overview["canonicalization_candidates"]] == [claim.id]
