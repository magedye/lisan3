import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
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


def test_unknown_or_unadmitted_run_authority_cannot_create_research_run(test_db):
    payload = {
        "target_contract": "ROOT_CORE",
        "target_expression": "test",
        "methodology_revision": "ARBITRARY_METHODOLOGY",
        "corpus_snapshot": "NONEXISTENT_SNAPSHOT",
        "authority_context": {"profile": "adversarial-admission"},
    }
    unknown = client.post("/runs", json=payload)
    assert unknown.status_code == 422
    assert test_db.query(models.ResearchRun).count() == 0

    snapshot = models.CorpusSnapshot(
        id="snapshot_pending_admission",
        canonical_text_source="TANZIL_QURAN_UTHMANI",
        canonical_text_version="v1.0.2",
        canonical_text_hash="unverified",
    )
    test_db.add(snapshot)
    test_db.commit()
    payload["corpus_snapshot"] = snapshot.id

    unavailable = client.post("/runs", json=payload)
    assert unavailable.status_code == 503
    assert "Methodology" in unavailable.json()["detail"]
    assert test_db.query(models.ResearchRun).count() == 0

    attention = client.get("/attention")
    assert attention.status_code == 200
    admission = attention.json()["run_admission"]
    assert admission["available"] is False
    assert admission["corpus_snapshot_ids"] == []
    assert admission["methodology_revisions"] == []


def test_arbitrary_steward_command_is_honestly_unsupported_and_audited(test_db):
    response = client.post(
        "/steward/commands",
        json={
            "command_type": "ARBITRARY_COMMAND",
            "intent": "arbitrary input",
            "parameters": {"marker": "NO_FAKE_SUCCESS"},
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["execution_status"] == "UNSUPPORTED"
    assert data["evaluated_rules"] is None
    assert "PASS" not in response.text
    assert '"SUCCESS"' not in response.text

    audit = client.get(
        f"/audit?entity_type=StewardCommand&entity_id={data['id']}"
    )
    assert audit.status_code == 200
    assert [(item["action"], item["new_state"]) for item in audit.json()] == [
        ("REJECT_UNSUPPORTED", "UNSUPPORTED")
    ]


def test_forbidden_steward_command_records_only_actual_rejection(test_db):
    response = client.post(
        "/steward/commands",
        json={
            "command_type": "FORCE_LOCK",
            "intent": "Force the Internal Lock",
            "parameters": {},
        },
    )
    assert response.status_code == 403

    command = test_db.query(models.StewardCommand).one()
    assert command.execution_status == "REJECTED"
    assert command.evaluated_rules is None
    audit = (
        test_db.query(models.AuditLog)
        .filter(models.AuditLog.entity_id == command.id)
        .one()
    )
    assert audit.action == "REJECT_AUTHORITY_BOUNDARY"
    assert audit.new_state == "REJECTED"


def test_claim_creation_and_review_persist_only_independent_canonical_axes(
    test_db, monkeypatch
):
    run, existing_claim, _ = _seed_unreleased_claim(test_db)
    monkeypatch.setattr("backend.main.has_valid_gate", lambda *_args: True)

    created = client.post(
        f"/runs/{run.id}/claims",
        json={"contract_type": "ROOT_CORE", "research_run_id": run.id},
    )
    assert created.status_code == 200
    assert {
        axis: created.json()[axis]
        for axis in (
            "epistemic_state",
            "review_state",
            "freshness_state",
            "publication_state",
        )
    } == {
        "epistemic_state": "LOCK_INTERNAL_RESULT",
        "review_state": "NOT_REVIEWED",
        "freshness_state": "CURRENT",
        "publication_state": "PRIVATE_WORKING",
    }

    publication_before = existing_claim.publication_state
    rejected = client.post(
        f"/claims/{existing_claim.id}/reviews",
        json={
            "reviewer_identity": "reviewer",
            "decision": "REJECTED",
            "rationale": "adversarial regression",
        },
    )
    assert rejected.status_code == 200
    test_db.refresh(existing_claim)
    assert existing_claim.review_state == "REJECTED"
    assert existing_claim.publication_state == publication_before


def test_database_rejects_noncanonical_claim_axis_values(test_db):
    test_db.add(
        models.SemanticClaim(
            id="claim_invalid_axis",
            contract_type="ROOT_CORE",
            epistemic_state="UNRESOLVED",
            review_state="PENDING_REVIEW",
            freshness_state="CURRENT",
            publication_state="UNPUBLISHED",
        )
    )
    with pytest.raises(IntegrityError):
        test_db.commit()
    test_db.rollback()


def test_missing_quality_profile_never_manufactures_quality_metrics(
    test_db, monkeypatch
):
    _, claim, _ = _seed_unreleased_claim(test_db)
    monkeypatch.setattr(
        "backend.domain.services.claim_visibility.has_valid_gate", lambda *_args: True
    )

    response = client.get(f"/claims/{claim.id}/quality")
    assert response.status_code == 200
    data = response.json()
    assert data["available"] is False
    assert data["source"] == "DERIVED_METHODOLOGICAL_PURITY_ONLY"
    assert data["corpus_coverage"] is None
    assert data["deep_analysis_coverage"] is None
    assert data["reproducibility_score"] is None
    assert data["unresolved_conflict_burden"] is None
    assert data["synthetic_data_leak"] is None
    assert data["external_data_leak"] is None
    assert test_db.query(models.QualityProfile).count() == 0


def test_stored_quality_profile_is_returned_without_overwriting_metrics(
    test_db, monkeypatch
):
    _, claim, _ = _seed_unreleased_claim(test_db)
    monkeypatch.setattr(
        "backend.domain.services.claim_visibility.has_valid_gate", lambda *_args: True
    )
    test_db.add(
        models.QualityProfile(
            id="quality_stored",
            claim_id=claim.id,
            purity_score=41,
            purity_rating="SUSPICIOUS",
            purity_findings=[],
            synthetic_data_leak=True,
            external_data_leak=False,
            corpus_coverage=23,
            deep_analysis_coverage=34,
            reproducibility_score=45,
            unresolved_conflict_burden=56,
            methodological_purity_flags=["stored-flag"],
            evaluation_summary="Stored governed evaluation",
        )
    )
    test_db.commit()

    response = client.get(f"/claims/{claim.id}/quality")
    assert response.status_code == 200
    data = response.json()
    assert data["available"] is True
    assert data["source"] == "PERSISTED_QUALITY_PROFILE"
    assert data["purity_score"] == 41
    assert data["corpus_coverage"] == 23
    assert data["deep_analysis_coverage"] == 34
    assert data["reproducibility_score"] == 45
