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
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base.metadata.create_all(engine)
client = TestClient(app)


def override_get_db():
    with SessionLocal() as db:
        yield db


@pytest.fixture(autouse=True)
def test_db():
    app.dependency_overrides[get_db] = override_get_db
    with SessionLocal() as db:
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(table.delete())
        db.commit()
        yield db
    app.dependency_overrides.pop(get_db, None)


def _seed_unreleased_claim(db):
    suffix = uuid.uuid4().hex[:8]
    run = models.ResearchRun(
        id=f"run_release_{suffix}",
        target_contract="ROOT_CORE",
        target_expression=f"ASK_MARKER_{suffix}",
        methodology_revision="methodology-test-only",
        corpus_snapshot=f"snapshot_missing_{suffix}",
        authority_context={"profile": "adversarial-release"},
    )
    isolation = models.IsolationState(
        id=f"isolation_release_{suffix}",
        research_run_id=run.id,
        target_contract=run.target_contract,
        corpus_snapshot=run.corpus_snapshot,
        methodology_reference=run.methodology_revision,
        allowed_sources=["QURAN_CORPUS"],
        is_contaminated="CLEAN",
    )
    claim = models.SemanticClaim(
        id=f"claim_release_{suffix}",
        research_run_id=run.id,
        contract_type="ROOT_CORE",
        epistemic_state="LOCK_INTERNAL_RESULT",
        review_state="NOT_REVIEWED",
        freshness_state="CURRENT",
        publication_state="PRIVATE_WORKING",
        abstract_root_core=f"SEMANTIC_MARKER_{suffix}",
        supporting_evidence={"marker": f"EVIDENCE_MARKER_{suffix}"},
    )
    dependency = models.DependencyRecord(
        id=f"dependency_release_{suffix}",
        dependent_claim_id=claim.id,
        dependency_type="CORPUS_SNAPSHOT",
        dependency_ref=run.corpus_snapshot,
    )
    audit = models.AuditLog(
        id=f"audit_release_{suffix}",
        entity_id=claim.id,
        entity_type="SemanticClaim",
        action=f"AUDIT_MARKER_{suffix}",
        actor="ADVERSARIAL_TEST",
    )
    db.add_all([run, isolation, claim, dependency, audit])
    db.commit()
    return run, claim, audit


def _claim_derived_get_paths(run_id: str, claim_id: str) -> list[str]:
    return [
        f"/claims/{claim_id}",
        f"/claims/{claim_id}/provenance",
        f"/claims/{claim_id}/reproduction_manifest",
        f"/claims/{claim_id}/quality",
        f"/claims/{claim_id}/history",
        f"/knowledge/explorer/{claim_id}",
        f"/audit?entity_type=SemanticClaim&entity_id={claim_id}",
        f"/runs/{run_id}/knowledge-graph",
    ]


def test_unreleased_markers_cannot_escape_any_claim_derived_read_api(test_db):
    run, claim, audit = _seed_unreleased_claim(test_db)
    markers = [claim.abstract_root_core, claim.supporting_evidence["marker"], audit.action]

    ask = client.post(
        "/ask",
        json={"expression": run.target_expression, "contract_type": claim.contract_type},
    )
    assert ask.status_code == 200
    assert ask.json() == {"status": "INSUFFICIENT_EVIDENCE", "claim": None}

    for path in _claim_derived_get_paths(run.id, claim.id):
        response = client.get(path)
        assert response.status_code == 403, path
        assert not any(marker in response.text for marker in markers), path

    for path in ("/attention", "/governance/overview", "/audit"):
        response = client.get(path)
        assert response.status_code == 200, path
        assert not any(marker in response.text for marker in markers), path

    workspace = client.get(f"/runs/{run.id}/workspace")
    assert workspace.status_code == 200
    assert workspace.json()["claims_visible"] is False
    assert workspace.json()["claims"] == []
    assert not any(marker in workspace.text for marker in markers)


def test_same_claim_resources_become_available_after_release_conditions(
    test_db, monkeypatch
):
    run, claim, audit = _seed_unreleased_claim(test_db)
    monkeypatch.setattr(
        "backend.domain.services.claim_visibility.has_valid_gate", lambda *_args: True
    )

    ask = client.post(
        "/ask",
        json={"expression": run.target_expression, "contract_type": claim.contract_type},
    )
    assert ask.status_code == 200
    assert ask.json()["status"] == "FOUND"
    assert claim.abstract_root_core in ask.text
    assert claim.supporting_evidence["marker"] in ask.text

    for path in _claim_derived_get_paths(run.id, claim.id)[:-1]:
        response = client.get(path)
        assert response.status_code == 200, path

    assert audit.action in client.get("/audit").text
    assert claim.abstract_root_core in client.get("/attention").text
    assert claim.abstract_root_core in client.get("/governance/overview").text
    assert claim.abstract_root_core in client.get(f"/runs/{run.id}/workspace").text
