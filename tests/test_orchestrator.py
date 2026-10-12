import pytest

from backend.domain import models
from backend.domain.services.orchestrator import (
    CampaignOrchestrator,
    IllegalTransitionError,
    OrchestratorState,
)


def test_no_run_yields_planned(test_db):
    """Stage 12 requirement: no run -> planned / no isolation state."""
    state = CampaignOrchestrator.derive_root_state(test_db, "non_existent_run_id")
    assert state == OrchestratorState.PLANNED


def test_run_created_without_isolation(test_db):
    run = models.ResearchRun(
        id="run_orch_no_iso",
        target_contract="ROOT_CORE",
        target_expression="علم",
        methodology_revision="test-m-1",
        corpus_snapshot="test-s-1",
        authority_context={},
    )
    test_db.add(run)
    test_db.commit()

    state = CampaignOrchestrator.derive_root_state(test_db, "run_orch_no_iso")
    assert state == OrchestratorState.RUN_CREATED


def test_contaminated_run_yields_blocked(test_db):
    run = models.ResearchRun(
        id="run_orch_contam",
        target_contract="ROOT_CORE",
        target_expression="علم",
        methodology_revision="test-m-1",
        corpus_snapshot="test-s-1",
        authority_context={},
    )
    iso = models.IsolationState(
        id="iso_orch_contam",
        research_run_id="run_orch_contam",
        establishment_status="ESTABLISHED",
        is_contaminated="PRIOR_CONTAMINATED",
    )
    test_db.add_all([run, iso])
    test_db.commit()

    state = CampaignOrchestrator.derive_root_state(test_db, "run_orch_contam")
    assert state == OrchestratorState.BLOCKED


def test_incomplete_observations_prevents_claim_ready(test_db):
    """Stage 12 requirement: incomplete observations -> no claim-ready state."""
    run = models.ResearchRun(
        id="run_orch_iso_only",
        target_contract="ROOT_CORE",
        target_expression="علم",
        methodology_revision="test-m-1",
        corpus_snapshot="test-s-1",
        authority_context={},
    )
    iso = models.IsolationState(
        id="iso_orch_iso_only",
        research_run_id="run_orch_iso_only",
        establishment_status="ESTABLISHED",
        is_contaminated="CLEAN",
    )
    test_db.add_all([run, iso])
    test_db.commit()

    # Isolation established but 0 observations
    state = CampaignOrchestrator.derive_root_state(test_db, "run_orch_iso_only")
    assert state == OrchestratorState.ISOLATION_ESTABLISHED

    # Cannot jump to CLAIM_FROZEN without observations
    with pytest.raises(IllegalTransitionError):
        CampaignOrchestrator.transition(
            test_db, "run_orch_iso_only", OrchestratorState.CLAIM_FROZEN, actor="TEST"
        )


def test_stale_revision_requires_fresh_review(test_db):
    """Stage 12 requirement: stale revision -> no verification."""
    run = models.ResearchRun(
        id="run_orch_stale",
        target_contract="ROOT_CORE",
        target_expression="علم",
        methodology_revision="test-m-1",
        corpus_snapshot="test-s-1",
        authority_context={},
    )
    iso = models.IsolationState(
        id="iso_orch_stale",
        research_run_id="run_orch_stale",
        establishment_status="ESTABLISHED",
        is_contaminated="CLEAN",
    )
    claim = models.SemanticClaim(
        id="claim_orch_stale",
        research_run_id="run_orch_stale",
        contract_type="ROOT_CORE",
        revision_id=2,  # Current revision is 2
        research_state="PREFERRED",
        canonical_state="NOT_CANONICAL",
        verification_state="NOT_VERIFIED",
    )
    # Review was completed for revision 1 (STALE)
    stale_review = models.IndependentReview(
        id="rev_orch_stale_1",
        claim_id="claim_orch_stale",
        revision_id=1,
        reviewer_identity="TEST_REV",
        review_status="COMPLETED",
        verdict="AGREE",
    )
    test_db.add_all([run, iso, claim, stale_review])
    test_db.commit()

    state = CampaignOrchestrator.derive_root_state(test_db, "run_orch_stale")
    # Because the only review was for revision 1, current state must be CLAIM_FROZEN awaiting review for revision 2
    assert state == OrchestratorState.CLAIM_FROZEN


def test_illegal_canonicalization_without_verification(test_db):
    """Stage 12 requirement: no policy pass -> no canonicalization."""
    run = models.ResearchRun(
        id="run_orch_unverified",
        target_contract="ROOT_CORE",
        target_expression="علم",
        methodology_revision="test-m-1",
        corpus_snapshot="test-s-1",
        authority_context={},
    )
    iso = models.IsolationState(
        id="iso_orch_unverified",
        research_run_id="run_orch_unverified",
        establishment_status="ESTABLISHED",
        is_contaminated="CLEAN",
    )
    claim = models.SemanticClaim(
        id="claim_orch_unverified",
        research_run_id="run_orch_unverified",
        contract_type="ROOT_CORE",
        revision_id=1,
        research_state="PREFERRED",
        canonical_state="NOT_CANONICAL",
        verification_state="NOT_VERIFIED",
    )
    test_db.add_all([run, iso, claim])
    test_db.commit()

    # Attempting transition directly to CANONICALIZED without VERIFIED must fail
    with pytest.raises(IllegalTransitionError):
        CampaignOrchestrator.transition(
            test_db,
            "run_orch_unverified",
            OrchestratorState.CANONICALIZED,
            actor="TEST",
        )


def test_valid_lifecycle_transitions(test_db):
    run = models.ResearchRun(
        id="run_orch_valid",
        target_contract="ROOT_CORE",
        target_expression="علم",
        methodology_revision="test-m-1",
        corpus_snapshot="test-s-1",
        authority_context={},
    )
    iso = models.IsolationState(
        id="iso_orch_valid",
        research_run_id="run_orch_valid",
        establishment_status="ESTABLISHED",
        is_contaminated="CLEAN",
    )
    obs = models.ObservationArtifact(
        id="obs_orch_valid",
        research_run_id="run_orch_valid",
        occurrence_ref="ref1",
    )
    test_db.add_all([run, iso, obs])
    test_db.commit()

    assert (
        CampaignOrchestrator.derive_root_state(test_db, "run_orch_valid")
        == OrchestratorState.OBSERVATIONS_COMPLETE
    )

    CampaignOrchestrator.transition(
        test_db, "run_orch_valid", OrchestratorState.CLAIM_FROZEN, actor="TEST"
    )
    audit = test_db.query(models.AuditLog).filter_by(entity_id="run_orch_valid").first()
    assert audit is not None
    assert audit.action == "STATE_TRANSITION"
    assert audit.new_state == OrchestratorState.CLAIM_FROZEN.value
