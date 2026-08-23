import uuid
from dataclasses import dataclass

from sqlalchemy.orm import Session

from backend.domain import models
from backend.domain.services.corpus.authority import is_production_validated
from backend.domain.services.purity import evaluate_run_methodological_purity

PURITY_CHECK = "PURITY_CHECK"
INTERNAL_LOCK = "INTERNAL_LOCK"
SUPPORTED_GATES = frozenset({PURITY_CHECK, INTERNAL_LOCK})


@dataclass(frozen=True)
class GateEvaluation:
    gate_code: str
    status: str
    evidence_refs: list[str]
    failure_reason: str | None
    evaluated_revision: str
    required_action: str | None


def _purity_evaluation(db: Session, run: models.ResearchRun) -> GateEvaluation:
    _, rating, findings, _ = evaluate_run_methodological_purity(run.id, db)
    blocking_dimensions = [
        finding["dimension"]
        for finding in findings
        if finding["status"] != "EVALUATED_CLEAN"
    ]
    observations = (
        db.query(models.ObservationArtifact)
        .filter(models.ObservationArtifact.research_run_id == run.id)
        .all()
    )
    hypotheses = (
        db.query(models.Hypothesis)
        .filter(models.Hypothesis.research_run_id == run.id)
        .all()
    )
    evidence_refs = sorted(
        [f"observation:{item.id}" for item in observations]
        + [f"hypothesis:{item.id}" for item in hypotheses]
    )
    passed = not blocking_dimensions and rating == "PURE"
    return GateEvaluation(
        gate_code=PURITY_CHECK,
        status="PASSED" if passed else "FAILED",
        evidence_refs=evidence_refs,
        failure_reason=(
            None
            if passed
            else "Purity dimensions not clean: " + ", ".join(blocking_dimensions)
        ),
        evaluated_revision=run.methodology_revision,
        required_action=None
        if passed
        else "Resolve every FLAGGED or NOT_EVALUATED dimension",
    )


def _latest_gate(db: Session, run_id: str, gate_code: str):
    return (
        db.query(models.GateReport)
        .filter(
            models.GateReport.research_run_id == run_id,
            models.GateReport.gate_code == gate_code,
        )
        .order_by(models.GateReport.created_at.desc(), models.GateReport.id.desc())
        .first()
    )


def _matches(record: models.GateReport | None, evaluation: GateEvaluation) -> bool:
    return bool(
        record
        and record.status == evaluation.status
        and (record.evidence_refs or []) == evaluation.evidence_refs
        and record.evaluated_revision == evaluation.evaluated_revision
    )


def evaluate_gate(db: Session, run_id: str, gate_code: str) -> GateEvaluation:
    if gate_code not in SUPPORTED_GATES:
        raise ValueError(f"Unsupported gate code: {gate_code}")
    run = db.get(models.ResearchRun, run_id)
    if run is None:
        raise LookupError(f"ResearchRun {run_id} not found")
    if gate_code == PURITY_CHECK:
        return _purity_evaluation(db, run)

    failures: list[str] = []
    evidence_refs: list[str] = []
    purity_evaluation = _purity_evaluation(db, run)
    purity_record = _latest_gate(db, run_id, PURITY_CHECK)
    if purity_evaluation.status != "PASSED" or not _matches(
        purity_record, purity_evaluation
    ):
        failures.append("PURITY_CHECK is absent, stale, forged, or failed")
    elif purity_record is not None:
        evidence_refs.append(f"gate:{purity_record.id}")

    snapshot = db.get(models.CorpusSnapshot, run.corpus_snapshot)
    if snapshot is None or not is_production_validated(snapshot):
        failures.append(
            "CorpusSnapshot is not authority-verified and production-active"
        )
    else:
        evidence_refs.append(f"corpus:{snapshot.id}")

    isolation = (
        db.query(models.IsolationState)
        .filter(models.IsolationState.research_run_id == run_id)
        .one_or_none()
    )
    if isolation is None or isolation.is_contaminated != "CLEAN":
        failures.append("Blind Lab isolation is absent or contaminated")
    else:
        evidence_refs.append(f"isolation:{isolation.id}")

    passed = not failures
    return GateEvaluation(
        gate_code=INTERNAL_LOCK,
        status="PASSED" if passed else "FAILED",
        evidence_refs=sorted(evidence_refs),
        failure_reason=None if passed else "; ".join(failures),
        evaluated_revision=run.methodology_revision,
        required_action=None
        if passed
        else "Satisfy canonical Purity, Corpus, and isolation prerequisites",
    )


def record_gate_evaluation(
    db: Session, run_id: str, gate_code: str
) -> models.GateReport:
    evaluation = evaluate_gate(db, run_id, gate_code)
    record = models.GateReport(
        id=f"gate_{uuid.uuid4().hex[:8]}",
        research_run_id=run_id,
        gate_code=evaluation.gate_code,
        status=evaluation.status,
        evidence_refs=evaluation.evidence_refs,
        failure_reason=evaluation.failure_reason,
        evaluated_revision=evaluation.evaluated_revision,
        required_action=evaluation.required_action,
    )
    db.add(record)
    return record


def has_valid_gate(db: Session, run_id: str, gate_code: str) -> bool:
    evaluation = evaluate_gate(db, run_id, gate_code)
    return evaluation.status == "PASSED" and _matches(
        _latest_gate(db, run_id, gate_code), evaluation
    )
