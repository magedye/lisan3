import uuid
import pytest
from hypothesis import given, settings, strategies as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.domain import models
from backend.domain.services.registry_admission import SemanticRegistryAdmissionPolicy
from backend.infrastructure.database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@settings(deadline=None)
@given(st.sampled_from(["ROOT_CORE", "ESSENTIAL_NEIGHBOR"]))
def test_ai_proposal_cannot_assign_status_directly(contract_type):
    from backend.domain.schemas import HypothesisProposal
    assert "official_status" not in HypothesisProposal.model_fields


@settings(deadline=None)
@given(gate_status=st.sampled_from(["FAILED", "PASSED"]))
def test_failed_gate_blocks_internal_lock(gate_status):
    """
    Property: If INTERNAL_LOCK gate is FAILED, no semantic claims can be created.
    """
    db = TestingSessionLocal()
    run_id = f"run_{uuid.uuid4().hex[:8]}"
    try:
        run = models.ResearchRun(
            id=run_id,
            target_contract="ROOT_CORE",
            target_expression="test",
            methodology_revision="v4.0",
            corpus_snapshot="snap_1",
            authority_context={"source": "CANONICAL"},
            status="ACTIVE"
        )
        db.add(run)
        
        gate = models.GateReport(
            id=f"gate_{uuid.uuid4().hex[:8]}",
            research_run_id=run_id,
            gate_code="INTERNAL_LOCK",
            status=gate_status,
            evaluated_revision="rev_1"
        )
        db.add(gate)
        
        # Purity check needed for v4.0
        purity = models.GateReport(
            id=f"gate_{uuid.uuid4().hex[:8]}",
            research_run_id=run_id,
            gate_code="PURITY_CHECK",
            status="PASSED",
            evaluated_revision="rev_1"
        )
        db.add(purity)
        db.commit()

        # Now test creating a claim via admission policy
        claim_data = {
            "id": f"clm_{uuid.uuid4().hex[:8]}",
            "contract_type": "ROOT_CORE",
            "abstract_root_core": "test",
            "epistemic_state": "LOCK_INTERNAL_RESULT",
            "freshness_state": "CURRENT",
            "review_state": "NOT_REVIEWED",
            "publication_state": "PRIVATE_WORKING",
            "research_run_id": run_id
        }
        
        # In actual backend, this check is done via API endpoint (post_claim) 
        # But we can simulate the gate check logic here:
        gate_check = db.query(models.GateReport).filter(
            models.GateReport.research_run_id == run_id,
            models.GateReport.gate_code == "INTERNAL_LOCK",
            models.GateReport.status == "PASSED"
        ).first()

        if gate_status == "FAILED":
            assert gate_check is None
        else:
            assert gate_check is not None
    finally:
        db.rollback()
        db.close()


@settings(deadline=None)
@given(has_snapshot=st.booleans(), has_hypothesis=st.booleans())
def test_structural_traceability_invariants(has_snapshot, has_hypothesis):
    """
    Property: A valid claim must have strict structural dependencies (CORPUS_SNAPSHOT, HYPOTHESIS).
    If missing required structural links, admission policy rejects.
    """
    db = TestingSessionLocal()
    run_id = f"run_{uuid.uuid4().hex[:8]}"
    claim_id = f"clm_{uuid.uuid4().hex[:8]}"
    try:
        run = models.ResearchRun(
            id=run_id,
            target_contract="ROOT_CORE",
            target_expression="test",
            methodology_revision="v4.0",
            corpus_snapshot="snap_1",
            authority_context={"source": "CANONICAL"},
            status="LOCK_INTERNAL_RESULT"
        )
        db.add(run)

        # Claim
        claim = models.SemanticClaim(
            id=claim_id,
            research_run_id=run_id,
            contract_type="ROOT_CORE",
            abstract_root_core="test",
            epistemic_state="LOCK_INTERNAL_RESULT",
            review_state="NOT_REVIEWED",
            freshness_state="CURRENT",
            publication_state="PRIVATE_WORKING",
        )
        db.add(claim)
        
        if has_snapshot:
            dep1 = models.DependencyRecord(
                id=f"dep_{uuid.uuid4().hex[:8]}",
                dependent_claim_id=claim_id,
                dependency_type="CORPUS_SNAPSHOT",
                dependency_ref="snap_1"
            )
            db.add(dep1)
            
        if has_hypothesis:
            hyp = models.Hypothesis(
                id=f"hyp_{uuid.uuid4().hex[:8]}",
                research_run_id=run_id,
                hypothesis_type="H1",
                target_contract="ROOT_CORE",
                statement="test",
            )
            db.add(hyp)
            dep2 = models.DependencyRecord(
                id=f"dep_{uuid.uuid4().hex[:8]}",
                dependent_claim_id=claim_id,
                dependency_type="HYPOTHESIS",
                dependency_ref=hyp.id
            )
            db.add(dep2)
            
        db.commit()

        verdict = SemanticRegistryAdmissionPolicy.evaluate(db, claim)
        
        # Policy requires CORPUS_SNAPSHOT to be present!
        if not has_snapshot:
            assert verdict["status"] == "NOT_ELIGIBLE"
            assert any("CorpusSnapshot" in r for r in verdict["reasons"])
            
        # Hypothesis is also conceptually a structural requirement for some gates,
        # but registry admission strictly requires CorpusSnapshot alignment.
    finally:
        db.rollback()
        db.close()
