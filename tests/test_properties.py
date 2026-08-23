import uuid
from contextlib import contextmanager

from fastapi.testclient import TestClient
from hypothesis import given, settings
from hypothesis import strategies as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.domain import models, schemas
from backend.domain.services.gates import INTERNAL_LOCK, has_valid_gate
from backend.domain.services.registry_admission import SemanticRegistryAdmissionPolicy
from backend.infrastructure.database import Base, get_db
from backend.main import app


@contextmanager
def isolated_database():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = session_factory()
    try:
        yield db, session_factory
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def add_run_and_claim(db, suffix: str):
    run = models.ResearchRun(
        id=f"run_{suffix}",
        target_contract="ROOT_CORE",
        target_expression=suffix,
        methodology_revision="v4.0",
        corpus_snapshot=f"snap_{suffix}",
        authority_context={"source": "PROPERTY_TEST"},
        status="ACTIVE",
    )
    claim = models.SemanticClaim(
        id=f"claim_{suffix}",
        research_run_id=run.id,
        contract_type="ROOT_CORE",
        epistemic_state="UNRESOLVED",
        review_state="NOT_REVIEWED",
        freshness_state="CURRENT",
        publication_state="PRIVATE_WORKING",
    )
    db.add_all([run, claim])
    db.commit()
    return run, claim


@settings(deadline=None, max_examples=30)
@given(
    statement=st.text(min_size=1, max_size=80),
    target_contract=st.sampled_from(["ROOT_CORE", "ESSENTIAL_NEIGHBOR"]),
    evidence_refs=st.lists(st.text(min_size=1, max_size=12), max_size=4),
)
def test_ai_proposals_cannot_mutate_official_state(
    statement, target_contract, evidence_refs
):
    with isolated_database() as (db, _):
        _, claim = add_run_and_claim(db, uuid.uuid4().hex[:8])
        before = (
            claim.epistemic_state,
            claim.review_state,
            claim.freshness_state,
            claim.publication_state,
        )

        proposal = schemas.HypothesisProposal(
            hypothesis_type="H1",
            target_contract=target_contract,
            scope="generated-property",
            statement=statement,
            rationale="generated proposal only",
            supporting_evidence_refs=evidence_refs,
            unresolved_cases=[],
            rejection_condition=schemas.RejectionCondition(
                challenging_finding="counterexample",
                search_location="corpus",
                verification_method="compare admitted occurrences",
                confounder_control="same corpus snapshot",
                failure_consequence="reject hypothesis",
            ),
        )

        assert proposal.statement == statement
        assert proposal.target_contract == target_contract
        assert proposal.supporting_evidence_refs == evidence_refs
        assert not {
            "epistemic_state",
            "review_state",
            "freshness_state",
            "publication_state",
            "official_status",
    }.intersection(type(proposal).model_fields)
        db.refresh(claim)
        assert (
            claim.epistemic_state,
            claim.review_state,
            claim.freshness_state,
            claim.publication_state,
        ) == before


@settings(deadline=None, max_examples=40)
@given(
    attach_to_target=st.booleans(),
    attach_to_other=st.booleans(),
    dependency_type=st.sampled_from(
        ["CORPUS_SNAPSHOT", "GOVERNANCE_RULE", "HYPOTHESIS"]
    ),
    matching_ref=st.booleans(),
)
def test_traceability_requires_exact_entity_bound_corpus_dependency(
    attach_to_target, attach_to_other, dependency_type, matching_ref
):
    with isolated_database() as (db, _):
        run, claim = add_run_and_claim(db, uuid.uuid4().hex[:8])
        _, other_claim = add_run_and_claim(db, uuid.uuid4().hex[:8])

        if attach_to_target:
            db.add(
                models.DependencyRecord(
                    id=f"dep_target_{uuid.uuid4().hex[:8]}",
                    dependent_claim_id=claim.id,
                    dependency_type=dependency_type,
                    dependency_ref=(
                        run.corpus_snapshot if matching_ref else "wrong_snapshot"
                    ),
                )
            )
        if attach_to_other:
            db.add(
                models.DependencyRecord(
                    id=f"dep_other_{uuid.uuid4().hex[:8]}",
                    dependent_claim_id=other_claim.id,
                    dependency_type="CORPUS_SNAPSHOT",
                    dependency_ref=run.corpus_snapshot,
                )
            )
        db.commit()

        verdict = SemanticRegistryAdmissionPolicy.evaluate(db, claim)
        dependency_reasons = [
            reason
            for reason in verdict["reasons"]
            if "CORPUS_SNAPSHOT dependency" in reason
        ]
        target_has_exact_dependency = (
            attach_to_target and dependency_type == "CORPUS_SNAPSHOT" and matching_ref
        )
        if target_has_exact_dependency:
            assert dependency_reasons == []
        else:
            assert dependency_reasons
        assert verdict["status"] == "NOT_ELIGIBLE"


gate_statuses = st.lists(
    st.tuples(
        st.sampled_from(["PURITY_CHECK", "INTERNAL_LOCK"]),
        st.sampled_from(["PASSED", "FAILED", "BLOCKED"]),
        st.lists(st.text(min_size=1, max_size=16), max_size=3),
    ),
    min_size=1,
    max_size=8,
)


@settings(deadline=None, max_examples=35)
@given(gate_sequence=gate_statuses)
def test_forged_gate_sequences_cannot_reach_internal_lock(gate_sequence):
    with isolated_database() as (db, _):
        run, claim = add_run_and_claim(db, uuid.uuid4().hex[:8])
        for index, (gate_code, status, evidence_refs) in enumerate(gate_sequence):
            db.add(
                models.GateReport(
                    id=f"gate_{index}_{uuid.uuid4().hex[:6]}",
                    research_run_id=run.id,
                    gate_code=gate_code,
                    status=status,
                    evidence_refs=evidence_refs,
                    evaluated_revision=run.methodology_revision,
                )
            )
            db.commit()
            assert has_valid_gate(db, run.id, INTERNAL_LOCK) is False
            db.refresh(run)
            db.refresh(claim)
            assert run.status == "ACTIVE"
            assert claim.epistemic_state == "UNRESOLVED"


mutation_actions = st.lists(
    st.tuples(
        st.sampled_from(["SemanticClaim", "ResearchRun"]),
        st.sampled_from(
            ["LOCK_INTERNAL_RESULT", "PUBLISHED", "REJECTED", "REVALIDATION_REQUIRED"]
        ),
        st.text(min_size=1, max_size=20),
    ),
    min_size=1,
    max_size=6,
)


@settings(deadline=None, max_examples=25)
@given(actions=mutation_actions)
def test_public_audit_surface_cannot_authorize_generated_transitions(actions):
    with isolated_database() as (db, session_factory):
        run, claim = add_run_and_claim(db, uuid.uuid4().hex[:8])
        initial_run_status = run.status
        initial_claim_status = claim.epistemic_state

        def override_database():
            request_db = session_factory()
            try:
                yield request_db
            finally:
                request_db.close()

        app.dependency_overrides[get_db] = override_database
        try:
            client = TestClient(app)
            for entity_type, requested_state, actor in actions:
                entity_id = claim.id if entity_type == "SemanticClaim" else run.id
                response = client.post(
                    "/api/audit/log",
                    json={
                        "entity_id": entity_id,
                        "entity_type": entity_type,
                        "action": "MUTATE",
                        "previous_state": (
                            initial_claim_status
                            if entity_type == "SemanticClaim"
                            else initial_run_status
                        ),
                        "new_state": requested_state,
                        "actor": actor,
                    },
                )
                assert response.status_code == 404
        finally:
            app.dependency_overrides.clear()

        db.expire_all()
        assert db.get(models.ResearchRun, run.id).status == initial_run_status
        assert (
            db.get(models.SemanticClaim, claim.id).epistemic_state
            == initial_claim_status
        )
