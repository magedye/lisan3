import uuid

from backend.domain import models
from backend.domain.services.provenance import ProvenanceService


def test_complete_provenance_graph(test_db):
    snapshot_id = f"snap_{uuid.uuid4().hex[:8]}"
    run_id = f"run_{uuid.uuid4().hex[:8]}"
    claim_id = f"claim_{uuid.uuid4().hex[:8]}"

    # Snapshot
    test_db.add(
        models.CorpusSnapshot(
            id=snapshot_id,
            canonical_text_source="test",
            canonical_text_version="1",
            canonical_text_hash="hash",
            activation_status="ACTIVE",
        )
    )

    # Run
    test_db.add(
        models.ResearchRun(
            id=run_id,
            target_contract="ROOT_CORE",
            target_expression="foo",
            methodology_revision="test-m-1",
            corpus_snapshot=snapshot_id,
            authority_context={},
        )
    )

    # Token/Occurrence
    test_db.add(
        models.CorpusOccurrence(
            id=f"occ_{uuid.uuid4().hex[:8]}",
            snapshot_id=snapshot_id,
            expression="foo",
            verse_ref="1:1",
            text="foo text",
        )
    )

    # Isolation
    test_db.add(
        models.IsolationState(
            id=f"iso_{uuid.uuid4().hex[:8]}",
            research_run_id=run_id,
            establishment_status="ESTABLISHED",
            corpus_snapshot=snapshot_id,
            audit_ref="aud_123",
            is_contaminated="CLEAN",
        )
    )

    # Observation
    test_db.add(
        models.ObservationArtifact(
            id=f"obs_{uuid.uuid4().hex[:8]}",
            research_run_id=run_id,
            occurrence_ref="1:1",
            form="form_test",
        )
    )

    # Claim
    test_db.add(
        models.SemanticClaim(
            id=claim_id,
            research_run_id=run_id,
            contract_type="ROOT_CORE",
            revision_id=1,
            canonical_state="NOT_CANONICAL",
            research_state="PREFERRED",
            verification_state="VERIFIED",
        )
    )

    # Claim Revision
    test_db.add(
        models.ClaimRevision(
            id=f"rev_{uuid.uuid4().hex[:8]}",
            claim_id=claim_id,
            revision_number=1,
            correction_reason="initial",
            payload={"dummy": True},
            semantic_payload_hash="dummy_hash",
            creation_actor="SYSTEM",
        )
    )

    # Independent Review
    test_db.add(
        models.IndependentReview(
            id=f"ir_{uuid.uuid4().hex[:8]}",
            claim_id=claim_id,
            revision_id=1,
            reviewer_identity="REV1",
            review_status="COMPLETED",
            verdict="AGREE",
        )
    )

    # Verification Record
    test_db.add(
        models.VerificationRecord(
            id=f"vr_{uuid.uuid4().hex[:8]}",
            claim_id=claim_id,
            verifier_identity="VER1",
            verification_type="INDEPENDENT",
            decision="VERIFIED",
            evaluated_claim_revision=1,
        )
    )

    # Audit Log
    test_db.add(
        models.AuditLog(
            id=f"aud_{uuid.uuid4().hex[:8]}",
            entity_id=claim_id,
            entity_type="SemanticClaim",
            action="STATE_TRANSITION",
            actor="TEST_USER",
            new_state="VERIFIED",
        )
    )

    test_db.commit()

    prov = ProvenanceService.get_run_provenance(test_db, run_id)
    assert prov["run_id"] == run_id
    assert prov["snapshot"]["id"] == snapshot_id
    assert prov["snapshot"]["activation"] == "ACTIVE"
    assert prov["isolation"]["status"] == "ESTABLISHED"
    assert len(prov["tokens"]) == 1
    assert len(prov["observations"]) == 1
    assert len(prov["claims"]) == 1

    claim_prov = prov["claims"][0]
    assert len(claim_prov["revisions"]) == 1
    assert len(claim_prov["reviews"]) == 1
    assert len(claim_prov["verifications"]) == 1
    assert len(claim_prov["audits"]) == 1


def test_broken_chain_provenance_handles_gracefully(test_db):
    """Stage 13 requirement: Tests must cover broken chains."""
    # 1. Non-existent run
    empty_prov = ProvenanceService.get_run_provenance(test_db, "non_existent_run")
    assert empty_prov["run_id"] == "non_existent_run"
    assert empty_prov["snapshot"] is None
    assert empty_prov["isolation"] is None
    assert empty_prov["tokens"] == []
    assert empty_prov["observations"] == []
    assert empty_prov["claims"] == []

    # 2. Run with dangling snapshot reference (broken snapshot edge)
    run_id = f"run_{uuid.uuid4().hex[:8]}"
    test_db.add(
        models.ResearchRun(
            id=run_id,
            target_contract="ROOT_CORE",
            target_expression="foo",
            methodology_revision="test-m-1",
            corpus_snapshot="missing_snapshot_id",
            authority_context={},
        )
    )
    test_db.commit()

    broken_prov = ProvenanceService.get_run_provenance(test_db, run_id)
    assert broken_prov["run_id"] == run_id
    assert broken_prov["snapshot"] is None
    assert broken_prov["tokens"] == []
    assert broken_prov["claims"] == []
