from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.domain import models
from backend.domain.services import gates
from backend.infrastructure.database import Base


def test_gate_evaluation_decision_matrix():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(engine)
    db = session_factory()

    run = models.ResearchRun(
        id="run_m_gate_target",
        target_contract="ROOT_CORE",
        target_expression="test",
        methodology_revision="v4.0",
        corpus_snapshot="snapshot_m_gate_target",
        authority_context={"source": "CANONICAL"},
        status="ACTIVE",
    )
    lower_run = models.ResearchRun(
        id="run_a_gate_other",
        target_contract="ROOT_CORE",
        target_expression="other",
        methodology_revision="v3.9",
        corpus_snapshot="snapshot_a_gate_other",
        authority_context={"source": "CANONICAL"},
        status="ACTIVE",
    )
    upper_run = models.ResearchRun(
        id="run_z_gate_other",
        target_contract="ROOT_CORE",
        target_expression="other upper",
        methodology_revision="v4.1",
        corpus_snapshot="snapshot_z_gate_other",
        authority_context={"source": "CANONICAL"},
        status="ACTIVE",
    )
    db.add_all([lower_run, run, upper_run])
    db.execute(
        models.CorpusSnapshot.__table__.insert().values(
            id=run.corpus_snapshot,
            canonical_text_source="TANZIL_QURAN_UTHMANI",
            canonical_text_version="v1.0.2",
            canonical_text_hash="b" * 64,
            validation_status="UNVERIFIED",
            fixture_only=True,
        )
    )
    isolation = models.IsolationState(
        id="isolation_gate_target",
        research_run_id=run.id,
        target_contract="ROOT_CORE",
        corpus_snapshot=run.corpus_snapshot,
        methodology_reference=run.methodology_revision,
        allowed_sources=["CORPUS"],
        is_contaminated="CLEAN",
    )
    db.add(isolation)
    db.add_all(
        [
            models.IsolationState(
                id="isolation_gate_lower",
                research_run_id=lower_run.id,
                is_contaminated="CLEAN",
            ),
            models.IsolationState(
                id="isolation_gate_upper",
                research_run_id=upper_run.id,
                is_contaminated="CLEAN",
            ),
        ]
    )
    db.commit()

    try:
        gates.evaluate_gate(db, "missing_run", gates.PURITY_CHECK)
    except LookupError:
        pass
    else:
        raise AssertionError("Missing runs must fail gate evaluation")

    try:
        gates.evaluate_gate(db, run.id, "UNSUPPORTED_GATE")
    except ValueError:
        pass
    else:
        raise AssertionError("Unknown gates must fail closed")

    dynamic_purity_code = "".join(["PURITY", "_CHECK"])  # noqa: FLY002
    assert dynamic_purity_code == gates.PURITY_CHECK
    assert dynamic_purity_code is not gates.PURITY_CHECK
    assert (
        gates.evaluate_gate(db, run.id, dynamic_purity_code).gate_code
        == gates.PURITY_CHECK
    )

    purity_failure = gates.evaluate_gate(db, run.id, gates.PURITY_CHECK)
    assert purity_failure.status == "FAILED"
    assert purity_failure.evidence_refs == []
    assert purity_failure.failure_reason is not None
    assert "DICTIONARY_FIRST" in purity_failure.failure_reason
    assert purity_failure.evaluated_revision == run.methodology_revision
    assert purity_failure.required_action is not None
    try:
        purity_failure.status = "PASSED"  # pyright: ignore[reportAttributeAccessIssue]
    except FrozenInstanceError:
        pass
    else:
        raise AssertionError("Gate evaluations must be immutable")

    forged = models.GateReport(
        id="gate_forged",
        research_run_id=run.id,
        gate_code=gates.PURITY_CHECK,
        status="PASSED",
        evidence_refs=["client:forged"],
        evaluated_revision=run.methodology_revision,
        created_at=datetime.now(timezone.utc) - timedelta(seconds=10),
    )
    other_gate = models.GateReport(
        id="gate_other_run",
        research_run_id=lower_run.id,
        gate_code=gates.PURITY_CHECK,
        status="PASSED",
        evidence_refs=[],
        evaluated_revision=lower_run.methodology_revision,
        created_at=datetime.now(timezone.utc) + timedelta(seconds=10),
    )
    db.add_all([forged, other_gate])
    db.commit()
    assert gates.has_valid_gate(db, run.id, gates.PURITY_CHECK) is False

    clean_findings = [
        {"dimension": dimension, "status": "EVALUATED_CLEAN"}
        for dimension in (
            "DICTIONARY_FIRST",
            "CONTEXTUAL_LEAKAGE",
            "HERITAGE_BIAS",
            "TAFSIR_CONTAMINATION",
            "FORCED_UNIFICATION",
            "GENERIC_OVEREXTRACTION",
            "LETTER_SEMANTICS_OVERRELIANCE",
            "CIRCULAR_CONFIRMATION",
        )
    ]
    observation = models.ObservationArtifact(
        id="observation_gate_target",
        research_run_id=run.id,
        occurrence_ref="occurrence:1",
    )
    hypothesis = models.Hypothesis(
        id="hypothesis_gate_target",
        research_run_id=run.id,
        hypothesis_type="H1",
        target_contract="ROOT_CORE",
        statement="test",
    )
    db.add_all([observation, hypothesis])
    for suffix, decoy_run in (("lower", lower_run), ("upper", upper_run)):
        db.add_all(
            [
                models.ObservationArtifact(
                    id=f"observation_gate_{suffix}",
                    research_run_id=decoy_run.id,
                    occurrence_ref=f"occurrence:{suffix}",
                ),
                models.Hypothesis(
                    id=f"hypothesis_gate_{suffix}",
                    research_run_id=decoy_run.id,
                    hypothesis_type="H1",
                    target_contract="ROOT_CORE",
                    statement=suffix,
                ),
            ]
        )
    db.commit()

    # Every comparison is exercised on both lexical sides, and equal strings are
    # reconstructed to ensure object identity can never substitute for equality.
    dynamic_clean = "".join(["EVALUATED", "_CLEAN"])  # noqa: FLY002
    dynamic_pure = "".join(["PU", "RE"])  # noqa: FLY002
    clean_findings_dynamic = [
        {"dimension": finding["dimension"], "status": dynamic_clean}
        for finding in clean_findings
    ]
    with patch.object(
        gates,
        "evaluate_run_methodological_purity",
        return_value=(100, dynamic_pure, clean_findings_dynamic, []),
    ):
        assert gates.evaluate_gate(db, run.id, gates.PURITY_CHECK).status == "PASSED"
    for impure_rating in ("AAA", "ZZZ"):
        with patch.object(
            gates,
            "evaluate_run_methodological_purity",
            return_value=(0, impure_rating, clean_findings, []),
        ):
            assert (
                gates.evaluate_gate(db, run.id, gates.PURITY_CHECK).status == "FAILED"
            )
    for dirty_status in ("AAA_FLAGGED", "ZZZ_NOT_EVALUATED"):
        dirty_findings = [dict(item) for item in clean_findings]
        dirty_findings[0]["status"] = dirty_status
        with patch.object(
            gates,
            "evaluate_run_methodological_purity",
            return_value=(0, "PURE", dirty_findings, []),
        ):
            assert (
                gates.evaluate_gate(db, run.id, gates.PURITY_CHECK).status == "FAILED"
            )

    expected = gates.GateEvaluation(
        gate_code=gates.PURITY_CHECK,
        status="PASSED",
        evidence_refs=["observation:target"],
        failure_reason=None,
        evaluated_revision="m",
        required_action=None,
    )
    for wrong_status in ("AAA", "ZZZ"):
        assert not gates._matches(
            models.GateReport(
                status=wrong_status,
                evidence_refs=expected.evidence_refs,
                evaluated_revision=expected.evaluated_revision,
            ),
            expected,
        )
    for wrong_evidence in (["aaa"], ["zzz"]):
        assert not gates._matches(
            models.GateReport(
                status=expected.status,
                evidence_refs=wrong_evidence,
                evaluated_revision=expected.evaluated_revision,
            ),
            expected,
        )
    for wrong_revision in ("a", "z"):
        assert not gates._matches(
            models.GateReport(
                status=expected.status,
                evidence_refs=expected.evidence_refs,
                evaluated_revision=wrong_revision,
            ),
            expected,
        )

    purity_patch = patch.object(
        gates,
        "evaluate_run_methodological_purity",
        return_value=(100, "PURE", clean_findings, []),
    )
    corpus_patch = patch.object(gates, "is_production_validated", return_value=True)
    purity_patch.start()
    corpus_mock = corpus_patch.start()
    try:
        purity_record = gates.record_gate_evaluation(db, run.id, gates.PURITY_CHECK)
        purity_record.created_at = datetime.now(timezone.utc) + timedelta(seconds=20)
        db.commit()
        assert purity_record.status == "PASSED"
        assert purity_record.required_action is None
        assert len(purity_record.id.removeprefix("gate_")) == 8
        assert purity_record.evidence_refs == [
            "hypothesis:hypothesis_gate_target",
            "observation:observation_gate_target",
        ]
        assert gates.has_valid_gate(db, run.id, gates.PURITY_CHECK) is True

        decoy_gates = [
            models.GateReport(
                id="gate_decoy_lower_run",
                research_run_id=lower_run.id,
                gate_code=gates.PURITY_CHECK,
                status="PASSED",
                evidence_refs=[],
                evaluated_revision=lower_run.methodology_revision,
                created_at=datetime.now(timezone.utc) + timedelta(minutes=5),
            ),
            models.GateReport(
                id="gate_decoy_upper_run",
                research_run_id=upper_run.id,
                gate_code=gates.PURITY_CHECK,
                status="PASSED",
                evidence_refs=[],
                evaluated_revision=upper_run.methodology_revision,
                created_at=datetime.now(timezone.utc) + timedelta(minutes=5),
            ),
            models.GateReport(
                id="gate_decoy_lower_code",
                research_run_id=run.id,
                gate_code="AAA_GATE",
                status="PASSED",
                evidence_refs=[],
                evaluated_revision=run.methodology_revision,
                created_at=datetime.now(timezone.utc) + timedelta(minutes=5),
            ),
            models.GateReport(
                id="gate_decoy_upper_code",
                research_run_id=run.id,
                gate_code="ZZZ_GATE",
                status="PASSED",
                evidence_refs=[],
                evaluated_revision=run.methodology_revision,
                created_at=datetime.now(timezone.utc) + timedelta(minutes=5),
            ),
        ]
        db.add_all(decoy_gates)
        db.commit()
        assert gates._latest_gate(db, run.id, gates.PURITY_CHECK).id == purity_record.id
        for decoy in decoy_gates:
            db.delete(decoy)
        db.commit()

        original_evidence = list(purity_record.evidence_refs)
        purity_record.evidence_refs = ["forged"]
        db.commit()
        assert gates.has_valid_gate(db, run.id, gates.PURITY_CHECK) is False
        purity_record.evidence_refs = original_evidence
        db.commit()

        purity_record.evaluated_revision = "stale"
        db.commit()
        assert gates.has_valid_gate(db, run.id, gates.PURITY_CHECK) is False
        purity_record.evaluated_revision = run.methodology_revision
        db.commit()

        internal_record = gates.record_gate_evaluation(db, run.id, gates.INTERNAL_LOCK)
        db.commit()
        assert internal_record.status == "PASSED"
        assert internal_record.required_action is None
        assert internal_record.evidence_refs == [
            f"corpus:{run.corpus_snapshot}",
            f"gate:{purity_record.id}",
            f"isolation:{isolation.id}",
        ]
        assert gates.has_valid_gate(db, run.id, gates.INTERNAL_LOCK) is True

        dynamic_passed = "".join(["PASS", "ED"])  # noqa: FLY002
        dynamic_success = gates.GateEvaluation(
            gate_code=gates.PURITY_CHECK,
            status=dynamic_passed,
            evidence_refs=list(purity_record.evidence_refs),
            failure_reason=None,
            evaluated_revision=run.methodology_revision,
            required_action=None,
        )
        with patch.object(gates, "evaluate_gate", return_value=dynamic_success):
            assert gates.has_valid_gate(db, run.id, gates.PURITY_CHECK) is True

        for non_passed in ("AAA", "ZZZ"):
            nonpassing_evaluation = gates.GateEvaluation(
                gate_code=gates.PURITY_CHECK,
                status=non_passed,
                evidence_refs=[],
                failure_reason="not passed",
                evaluated_revision=run.methodology_revision,
                required_action="fix",
            )
            nonpassing_record = models.GateReport(
                id=f"gate_internal_nonpassing_{non_passed}",
                research_run_id=run.id,
                gate_code=gates.PURITY_CHECK,
                status=non_passed,
                evidence_refs=[],
                evaluated_revision=run.methodology_revision,
                created_at=datetime.now(timezone.utc) + timedelta(minutes=2),
            )
            db.add(nonpassing_record)
            db.commit()
            with patch.object(
                gates, "_purity_evaluation", return_value=nonpassing_evaluation
            ):
                assert (
                    gates.evaluate_gate(db, run.id, gates.INTERNAL_LOCK).status
                    == "FAILED"
                )
            db.delete(nonpassing_record)
            db.commit()

        dynamic_internal_success = gates.GateEvaluation(
            gate_code=gates.PURITY_CHECK,
            status=dynamic_passed,
            evidence_refs=list(purity_record.evidence_refs),
            failure_reason=None,
            evaluated_revision=run.methodology_revision,
            required_action=None,
        )
        with patch.object(
            gates, "_purity_evaluation", return_value=dynamic_internal_success
        ):
            assert (
                gates.evaluate_gate(db, run.id, gates.INTERNAL_LOCK).status == "PASSED"
            )

        for contaminated_status in ("AAA_CONTAMINATED", "ZZZ_CONTAMINATED"):
            isolation.is_contaminated = contaminated_status
            db.commit()
            contaminated = gates.evaluate_gate(db, run.id, gates.INTERNAL_LOCK)
            assert contaminated.status == "FAILED"
            assert contaminated.required_action is not None
            assert contaminated.failure_reason is not None
            assert "contaminated" in contaminated.failure_reason
        isolation.is_contaminated = "CLEAN"
        db.commit()

        corpus_mock.return_value = False
        corpus_failure = gates.evaluate_gate(db, run.id, gates.INTERNAL_LOCK)
        assert corpus_failure.status == "FAILED"
        assert corpus_failure.failure_reason is not None
        assert "production-active" in corpus_failure.failure_reason
        corpus_mock.return_value = True

        purity_record.status = "FAILED"
        db.commit()
        purity_dependency_failure = gates.evaluate_gate(db, run.id, gates.INTERNAL_LOCK)
        assert purity_dependency_failure.status == "FAILED"
        assert purity_dependency_failure.failure_reason is not None
        assert "PURITY_CHECK" in purity_dependency_failure.failure_reason

        # A matching non-PASSED record must never become authorizing merely due
        # to lexical ordering of status strings.
        for non_passed in ("AAA", "ZZZ"):
            synthetic = gates.GateEvaluation(
                gate_code=gates.PURITY_CHECK,
                status=non_passed,
                evidence_refs=[],
                failure_reason="synthetic failure",
                evaluated_revision=run.methodology_revision,
                required_action="fix",
            )
            matching = models.GateReport(
                id=f"gate_synthetic_{non_passed}",
                research_run_id=run.id,
                gate_code=gates.PURITY_CHECK,
                status=non_passed,
                evidence_refs=[],
                evaluated_revision=run.methodology_revision,
                created_at=datetime.now(timezone.utc) + timedelta(minutes=1),
            )
            db.add(matching)
            db.commit()
            with patch.object(gates, "evaluate_gate", return_value=synthetic):
                assert gates.has_valid_gate(db, run.id, gates.PURITY_CHECK) is False
            db.delete(matching)
            db.commit()
    finally:
        corpus_patch.stop()
        purity_patch.stop()

    db.close()
    engine.dispose()


if __name__ == "__main__":
    test_gate_evaluation_decision_matrix()
