"""Fail-closed ResearchRun admission against current canonical authority."""

from dataclasses import dataclass

from sqlalchemy.orm import Session

from backend.domain import models
from backend.domain.services.corpus.authority import (
    is_production_validated,
    production_validation_failures,
)
from backend.domain.services.methodology_authority import (
    eligible_methodology_revision_ids,
    methodology_authority_failures,
)


@dataclass(frozen=True)
class RunAdmissionDecision:
    accepted: bool
    status: str
    reasons: tuple[str, ...]


class ResearchRunAdmissionPolicy:
    @staticmethod
    def eligible_corpus_snapshot_ids(db: Session) -> list[str]:
        return [
            str(snapshot.id)
            for snapshot in db.query(models.CorpusSnapshot)
            .order_by(models.CorpusSnapshot.id)
            .all()
            if is_production_validated(snapshot)
        ]

    @classmethod
    def current_state(cls, db: Session) -> dict[str, object]:
        corpus_ids = cls.eligible_corpus_snapshot_ids(db)
        methodology_ids = eligible_methodology_revision_ids(db)
        blockers: list[str] = []
        if not corpus_ids:
            blockers.append(
                "No authority-verified, production-active CorpusSnapshot is available"
            )
        if not methodology_ids:
            blockers.append("No eligible current Methodology revision is available")
        return {
            "available": not blockers,
            "corpus_snapshot_ids": corpus_ids,
            "methodology_revisions": methodology_ids,
            "blockers": blockers,
        }

    @staticmethod
    def evaluate(
        db: Session, corpus_snapshot_id: str, methodology_revision: str
    ) -> RunAdmissionDecision:
        snapshot = db.get(models.CorpusSnapshot, corpus_snapshot_id)
        methodology = db.get(models.MethodologyRevision, methodology_revision)
        invalid_references: list[str] = []
        if snapshot is None:
            invalid_references.append(
                f"CorpusSnapshot '{corpus_snapshot_id}' does not exist"
            )
        if methodology is None:
            invalid_references.append(
                f"Methodology revision '{methodology_revision}' does not exist"
            )
        if invalid_references:
            return RunAdmissionDecision(
                False,
                "INVALID_REFERENCE",
                tuple(invalid_references),
            )
        assert snapshot is not None
        assert methodology is not None

        reasons: list[str] = []
        if not is_production_validated(snapshot):
            if snapshot.validation_status != "VALIDATED":
                reasons.append(
                    f"CorpusSnapshot validation_status is '{snapshot.validation_status}', expected 'VALIDATED'"
                )
            reasons.extend(production_validation_failures(snapshot))
        reasons.extend(methodology_authority_failures(methodology))
        return RunAdmissionDecision(
            not reasons,
            "ADMITTED" if not reasons else "AUTHORITY_UNAVAILABLE",
            tuple(reasons),
        )
