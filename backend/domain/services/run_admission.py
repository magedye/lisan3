"""Fail-closed ResearchRun admission against current canonical authority."""

from dataclasses import dataclass

from sqlalchemy.orm import Session

from backend.domain import models
from backend.domain.services.corpus.authority import (
    is_production_validated,
    production_validation_failures,
)

# No accepted Methodology revision registry or canonical fallback currently exists.
AUTHORIZED_METHODOLOGY_REVISIONS: tuple[str, ...] = ()


@dataclass(frozen=True)
class RunAdmissionDecision:
    accepted: bool
    status: str
    reasons: tuple[str, ...]


class ResearchRunAdmissionPolicy:
    @staticmethod
    def eligible_corpus_snapshot_ids(db: Session) -> list[str]:
        return [
            snapshot.id
            for snapshot in db.query(models.CorpusSnapshot)
            .order_by(models.CorpusSnapshot.id)
            .all()
            if is_production_validated(snapshot)
        ]

    @classmethod
    def current_state(cls, db: Session) -> dict[str, object]:
        corpus_ids = cls.eligible_corpus_snapshot_ids(db)
        blockers: list[str] = []
        if not corpus_ids:
            blockers.append(
                "No authority-verified, production-active CorpusSnapshot is available"
            )
        if not AUTHORIZED_METHODOLOGY_REVISIONS:
            blockers.append(
                "No canonical Methodology revision registry or fallback is available"
            )
        return {
            "available": not blockers,
            "corpus_snapshot_ids": corpus_ids,
            "methodology_revisions": list(AUTHORIZED_METHODOLOGY_REVISIONS),
            "blockers": blockers,
        }

    @staticmethod
    def evaluate(
        db: Session, corpus_snapshot_id: str, methodology_revision: str
    ) -> RunAdmissionDecision:
        snapshot = db.get(models.CorpusSnapshot, corpus_snapshot_id)
        if snapshot is None:
            return RunAdmissionDecision(
                False,
                "INVALID_REFERENCE",
                (f"CorpusSnapshot '{corpus_snapshot_id}' does not exist",),
            )

        reasons: list[str] = []
        if not is_production_validated(snapshot):
            if snapshot.validation_status != "VALIDATED":
                reasons.append(
                    f"CorpusSnapshot validation_status is '{snapshot.validation_status}', expected 'VALIDATED'"
                )
            reasons.extend(production_validation_failures(snapshot))
        if methodology_revision not in AUTHORIZED_METHODOLOGY_REVISIONS:
            reasons.append(
                "Methodology revision is unavailable because no canonical Methodology registry or fallback exists"
            )
        return RunAdmissionDecision(
            not reasons,
            "ADMITTED" if not reasons else "AUTHORITY_UNAVAILABLE",
            tuple(reasons),
        )

