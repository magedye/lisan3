from datetime import datetime, timedelta, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.domain import models
from backend.domain.services.registry_admission import SemanticRegistryAdmissionPolicy
from backend.infrastructure.database import Base
from backend.main import evaluate_methodological_purity

# Setup mock DB
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def test_purity_not_evaluated_if_missing_evidence():
    db = TestingSessionLocal()
    claim = models.SemanticClaim(
        id="c1", research_run_id="run1", contract_type="ROOT_CORE"
    )
    score, rating, findings, _flags = evaluate_methodological_purity(claim, db)

    assert score == 0
    assert rating == "NOT_EVALUATED"
    assert all(f["status"] == "NOT_EVALUATED" for f in findings)

    db.close()


def test_purity_dictionary_first_flagged():
    db = TestingSessionLocal()
    run_id = "run_dict_first"

    # Hypothesis is created BEFORE observation -> DICTIONARY FIRST
    now = datetime.now(timezone.utc)
    hyp = models.Hypothesis(
        id="h1", research_run_id=run_id, created_at=now - timedelta(days=2)
    )
    obs = models.ObservationArtifact(
        id="o1",
        research_run_id=run_id,
        occurrence_ref="ref1",
        created_at=now - timedelta(days=1),
    )
    claim = models.SemanticClaim(
        id="c2", research_run_id=run_id, contract_type="ROOT_CORE"
    )

    db.add_all([hyp, obs, claim])
    db.commit()

    score, _rating, findings, flags = evaluate_methodological_purity(claim, db)
    dict_first_finding = next(
        f for f in findings if f["dimension"] == "DICTIONARY_FIRST"
    )

    assert dict_first_finding["status"] == "FLAGGED"
    assert "dictionary_first" in flags
    assert score < 100

    db.close()


def test_purity_blocks_admission():
    # If a claim has a failing PURITY_CHECK gate, it should be blocked from admission
    db = TestingSessionLocal()
    run = models.ResearchRun(
        id="run_admission",
        target_contract="ROOT_CORE",
        target_expression="xyz",
        methodology_revision="v1",
        corpus_snapshot="snap1",
        authority_context={"role": "TEST"},
        status="LOCK_INTERNAL_RESULT",
    )

    snap = models.CorpusSnapshot(
        id="snap1",
        canonical_text_source="TANZIL",
        canonical_text_version="v1",
        canonical_text_hash="abc",
        validation_status="UNVERIFIED",
    )

    claim = models.SemanticClaim(
        id="clm_admission",
        research_run_id="run_admission",
        contract_type="ROOT_CORE",
        epistemic_state="LOCK_INTERNAL_RESULT",
        review_state="APPROVED",
        freshness_state="CURRENT",
        revision_id=1,
    )

    review = models.ReviewDecision(
        id="rev_1",
        claim_id="clm_admission",
        reviewer_identity="user1",
        decision="APPROVED",
        evaluated_claim_revision=1,
    )

    # Missing PURITY_CHECK gate
    db.add_all([run, snap, claim, review])
    db.commit()

    result = SemanticRegistryAdmissionPolicy.evaluate(db, claim)
    assert result["status"] == "NOT_ELIGIBLE"
    assert any(
        "Missing required PASSED GateReport for 'PURITY_CHECK'" in r
        for r in result["reasons"]
    )

    db.close()
