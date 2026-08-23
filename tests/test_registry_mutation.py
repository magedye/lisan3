from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.domain import models
from backend.domain.services import registry_admission
from backend.domain.services.registry_admission import SemanticRegistryAdmissionPolicy
from backend.infrastructure.database import Base


def test_registry_admission_decision_matrix():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(engine)
    db = session_factory()
    snapshot_authority = patch.object(
        registry_admission, "is_production_validated", return_value=True
    )
    gate_authority = patch.object(
        registry_admission, "has_valid_gate", return_value=True
    )
    snapshot_authority.start()
    gate_mock = gate_authority.start()

    def build_case(suffix: str):
        snapshot_id = f"snapshot_{suffix}"
        db.execute(
            models.CorpusSnapshot.__table__.insert().values(
                id=snapshot_id,
                canonical_text_source="TANZIL_QURAN_UTHMANI",
                canonical_text_version="v1.0.2",
                canonical_text_hash="a" * 64,
                validation_status="VALIDATED",
                source_role_status="SOURCE_ROLE_APPROVED",
                artifact_presence_status="ARTIFACT_PRESENT",
                expected_canonical_text_hash="a" * 64,
                hash_verification_status="HASH_VERIFIED",
                import_validation_status="IMPORT_VALIDATED",
                activation_status="PRODUCTION_ACTIVE",
                artifact_provenance="canonical:test-authority",
                fixture_only=False,
            )
        )
        run = models.ResearchRun(
            id=f"run_{suffix}",
            target_contract="ROOT_CORE",
            target_expression="test",
            methodology_revision="v4.0",
            corpus_snapshot=snapshot_id,
            authority_context={"source": "CANONICAL"},
            status="LOCK_INTERNAL_RESULT",
        )
        claim = models.SemanticClaim(
            id=f"claim_{suffix}",
            research_run_id=run.id,
            contract_type="ROOT_CORE",
            epistemic_state="LOCK_INTERNAL_RESULT",
            review_state="APPROVED",
            freshness_state="CURRENT",
            publication_state="PRIVATE_WORKING",
            revision_id=1000,
        )
        review = models.ReviewDecision(
            id=f"review_{suffix}",
            claim_id=claim.id,
            reviewer_identity="reviewer",
            decision="APPROVED",
            evaluated_claim_revision=1000,
        )
        dependency = models.DependencyRecord(
            id=f"dependency_{suffix}",
            dependent_claim_id=claim.id,
            dependency_type="CORPUS_SNAPSHOT",
            dependency_ref=snapshot_id,
        )
        db.add_all([run, claim, review, dependency])
        db.commit()
        return run, claim, review, dependency

    def reasons(claim):
        return SemanticRegistryAdmissionPolicy.evaluate(db, claim)["reasons"]

    _, valid_claim, _, _ = build_case("valid")
    base_time = datetime.now(timezone.utc)
    db.add_all(
        [
            models.ReviewDecision(
                id="review_valid_lower_decision",
                claim_id=valid_claim.id,
                reviewer_identity="reviewer",
                decision="AAA_INVALID",
                evaluated_claim_revision=999,
                created_at=base_time + timedelta(seconds=1),
            ),
            models.ReviewDecision(
                id="review_valid_higher_decision",
                claim_id=valid_claim.id,
                reviewer_identity="reviewer",
                decision="ZZZ_INVALID",
                evaluated_claim_revision=999,
                created_at=base_time + timedelta(seconds=2),
            ),
            models.ReviewDecision(
                id="review_lower_claim",
                claim_id="aaa_claim",
                reviewer_identity="reviewer",
                decision="APPROVED",
                evaluated_claim_revision=999,
                created_at=base_time + timedelta(seconds=3),
            ),
            models.ReviewDecision(
                id="review_higher_claim",
                claim_id="zzz_claim",
                reviewer_identity="reviewer",
                decision="APPROVED",
                evaluated_claim_revision=999,
                created_at=base_time + timedelta(seconds=4),
            ),
            models.DependencyRecord(
                id="dependency_valid_lower_type",
                dependent_claim_id=valid_claim.id,
                dependency_type="AAA_INVALID",
                dependency_ref="ignored",
            ),
            models.DependencyRecord(
                id="dependency_valid_higher_type",
                dependent_claim_id=valid_claim.id,
                dependency_type="ZZZ_INVALID",
                dependency_ref="ignored",
            ),
            models.DependencyRecord(
                id="dependency_lower_claim",
                dependent_claim_id="aaa_claim",
                dependency_type="CORPUS_SNAPSHOT",
                dependency_ref="ignored",
            ),
            models.DependencyRecord(
                id="dependency_higher_claim",
                dependent_claim_id="zzz_claim",
                dependency_type="CORPUS_SNAPSHOT",
                dependency_ref="ignored",
            ),
        ]
    )
    db.commit()
    assert (
        db.query(models.DependencyRecord)
        .filter(
            models.DependencyRecord.dependent_claim_id == valid_claim.id,
            models.DependencyRecord.dependency_type == "CORPUS_SNAPSHOT",
        )
        .count()
        == 1
    )
    assert SemanticRegistryAdmissionPolicy.evaluate(db, valid_claim) == {
        "status": "ELIGIBLE",
        "reasons": [],
    }

    _, claim, _, _ = build_case("epistemic")
    claim.epistemic_state = "ZZZ_INVALID"
    assert any("epistemic state" in reason for reason in reasons(claim))

    _, claim, _, _ = build_case("epistemic_lower")
    claim.epistemic_state = "AAA_INVALID"
    assert any("epistemic state" in reason for reason in reasons(claim))

    _, claim, _, _ = build_case("review_state")
    claim.review_state = "AAA_INVALID"
    assert any("review state" in reason for reason in reasons(claim))

    _, claim, _, _ = build_case("review_state_higher")
    claim.review_state = "ZZZ_INVALID"
    assert any("review state" in reason for reason in reasons(claim))

    _, claim, review, _ = build_case("review_revision")
    review.evaluated_claim_revision = 1001
    db.commit()
    assert any("current claim revision" in reason for reason in reasons(claim))

    _, claim, review, _ = build_case("review_revision_lower")
    review.evaluated_claim_revision = 999
    db.commit()
    assert any("current claim revision" in reason for reason in reasons(claim))

    _, claim, _, _ = build_case("freshness")
    claim.freshness_state = "AAA_INVALID"
    assert any("freshness state" in reason for reason in reasons(claim))

    _, claim, _, _ = build_case("freshness_higher")
    claim.freshness_state = "ZZZ_INVALID"
    assert any("freshness state" in reason for reason in reasons(claim))

    run, claim, _, _ = build_case("snapshot_status")
    db.execute(
        update(models.CorpusSnapshot)
        .where(models.CorpusSnapshot.id == run.corpus_snapshot)
        .values(validation_status="ZZZ_INVALID")
    )
    db.commit()
    assert any("validation_status" in reason for reason in reasons(claim))

    run, claim, _, _ = build_case("snapshot_status_lower")
    db.execute(
        update(models.CorpusSnapshot)
        .where(models.CorpusSnapshot.id == run.corpus_snapshot)
        .values(validation_status="AAA_INVALID")
    )
    db.commit()
    assert any("validation_status" in reason for reason in reasons(claim))

    _, claim, _, dependency = build_case("missing_dependency")
    db.delete(dependency)
    db.commit()
    assert any("exactly one CORPUS_SNAPSHOT" in reason for reason in reasons(claim))

    run, claim, _, dependency = build_case("wrong_dependency")
    dependency.dependency_ref = "zzzz_wrong_snapshot"
    db.commit()
    assert any(run.corpus_snapshot in reason for reason in reasons(claim))

    run, claim, _, dependency = build_case("wrong_dependency_lower")
    dependency.dependency_ref = "aaa_wrong_snapshot"
    db.commit()
    assert any(run.corpus_snapshot in reason for reason in reasons(claim))

    _, claim, _, _ = build_case("missing_review")
    db.query(models.ReviewDecision).filter(
        models.ReviewDecision.claim_id == claim.id
    ).delete()
    db.add_all(
        [
            models.ReviewDecision(
                id="review_missing_lower",
                claim_id="aaa_missing_review",
                reviewer_identity="reviewer",
                decision="APPROVED",
                evaluated_claim_revision=1000,
            ),
            models.ReviewDecision(
                id="review_missing_higher",
                claim_id="zzz_missing_review",
                reviewer_identity="reviewer",
                decision="APPROVED",
                evaluated_claim_revision=1000,
            ),
        ]
    )
    db.commit()
    assert any("No APPROVED ReviewDecision" in reason for reason in reasons(claim))

    _, claim, _, _ = build_case("missing_run")
    claim.research_run_id = "run_missing"
    db.add(
        models.ResearchRun(
            id="run_zzz_missing",
            target_contract="ROOT_CORE",
            target_expression="decoy",
            methodology_revision="v4.0",
            corpus_snapshot="snapshot_decoy",
            authority_context={},
        )
    )
    db.commit()
    assert any("valid ResearchRun" in reason for reason in reasons(claim))

    run, claim, _, _ = build_case("missing_snapshot")
    run.corpus_snapshot = "snapshot_missing"
    db.execute(
        models.CorpusSnapshot.__table__.insert().values(
            id="snapshot_zzz_missing",
            canonical_text_source="TANZIL_QURAN_UTHMANI",
            canonical_text_version="v1.0.2",
            canonical_text_hash="a" * 64,
            validation_status="VALIDATED",
            fixture_only=False,
        )
    )
    db.commit()
    assert any("has no CorpusSnapshot" in reason for reason in reasons(claim))

    _, claim, _, _ = build_case("extra_dependency")
    db.add(
        models.DependencyRecord(
            id="dependency_extra",
            dependent_claim_id=claim.id,
            dependency_type="CORPUS_SNAPSHOT",
            dependency_ref="snapshot_extra_dependency",
        )
    )
    db.commit()
    assert any("exactly one CORPUS_SNAPSHOT" in reason for reason in reasons(claim))

    run, claim, _, _ = build_case("entity_isolation")
    other = models.SemanticClaim(
        id="claim_entity_other",
        research_run_id=run.id,
        contract_type="ROOT_CORE",
    )
    db.add(other)
    db.add(
        models.DependencyRecord(
            id="dependency_entity_other",
            dependent_claim_id=other.id,
            dependency_type="CORPUS_SNAPSHOT",
            dependency_ref=run.corpus_snapshot,
        )
    )
    own_dependency = (
        db.query(models.DependencyRecord)
        .filter(models.DependencyRecord.dependent_claim_id == claim.id)
        .one()
    )
    db.delete(own_dependency)
    db.commit()
    assert any("exactly one CORPUS_SNAPSHOT" in reason for reason in reasons(claim))

    _, claim, _, _ = build_case("fixture")
    run = db.get(models.ResearchRun, claim.research_run_id)
    run.target_contract = "test_fixture_root_core"
    db.commit()
    assert any("Synthetic fixtures" in reason for reason in reasons(claim))

    _, claim, _, _ = build_case("gates")
    gate_mock.side_effect = lambda _db, _run_id, gate_code: gate_code != "INTERNAL_LOCK"
    assert any("INTERNAL_LOCK" in reason for reason in reasons(claim))
    gate_mock.side_effect = lambda _db, _run_id, gate_code: gate_code != "PURITY_CHECK"
    assert any("PURITY_CHECK" in reason for reason in reasons(claim))

    db.close()
    engine.dispose()
    gate_authority.stop()
    snapshot_authority.stop()


if __name__ == "__main__":
    test_registry_admission_decision_matrix()
