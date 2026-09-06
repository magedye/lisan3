"""Durable campaign checkpoint / resume (Request 01 §14, Request 02 §14).

Persist campaign progress after every root so a session/runtime interruption
cannot lose the campaign. Resume never relies on conversation context: it reads
the durable ``CampaignState`` row and reports exactly what remains.
"""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session

from backend.domain import models


@dataclass(frozen=True)
class ResumeDescriptor:
    campaign_id: str
    status: str
    methodology_revision: str | None
    corpus_snapshot: str | None
    completed_count: int
    remaining_count: int
    next_root: str | None

    def as_dict(self) -> dict[str, object]:
        return {
            "campaign_id": self.campaign_id,
            "status": self.status,
            "methodology_revision": self.methodology_revision,
            "corpus_snapshot": self.corpus_snapshot,
            "completed_count": self.completed_count,
            "remaining_count": self.remaining_count,
            "next_root": self.next_root,
        }


class CampaignStateService:
    @staticmethod
    def initialize(
        db: Session,
        *,
        campaign_id: str,
        methodology_revision: str | None,
        corpus_snapshot: str | None,
        queue: list[str],
    ) -> models.CampaignState:
        existing = (
            db.query(models.CampaignState)
            .filter(models.CampaignState.campaign_id == campaign_id)
            .one_or_none()
        )
        if existing is not None:
            return existing
        state = models.CampaignState(
            id=f"camp_{campaign_id}",
            campaign_id=campaign_id,
            methodology_revision=methodology_revision,
            corpus_snapshot=corpus_snapshot,
            queue=list(queue),
            completed_roots=[],
            current_batch={},
            findings=[],
            status="INITIALIZED",
        )
        db.add(state)
        db.commit()
        db.refresh(state)
        return state

    @staticmethod
    def _load(db: Session, campaign_id: str) -> models.CampaignState:
        state = (
            db.query(models.CampaignState)
            .filter(models.CampaignState.campaign_id == campaign_id)
            .one_or_none()
        )
        if state is None:
            raise LookupError(f"Campaign {campaign_id} not found")
        return state

    @classmethod
    def checkpoint_root(
        cls,
        db: Session,
        campaign_id: str,
        root: str,
        *,
        findings: list | None = None,
    ) -> models.CampaignState:
        """Mark one root complete and persist immediately (idempotent)."""
        state = cls._load(db, campaign_id)
        completed = list(state.completed_roots or [])
        newly_completed = root not in completed
        if newly_completed:
            completed.append(root)
        state.completed_roots = completed
        state.queue = [r for r in (state.queue or []) if r not in set(completed)]
        # Append findings only on the first checkpoint of this root, so a
        # crash-retry / double-checkpoint does not duplicate findings.
        if findings and newly_completed:
            state.findings = list(state.findings or []) + list(findings)
        state.status = "COMPLETE" if not state.queue else "IN_PROGRESS"
        db.commit()
        db.refresh(state)
        return state

    @classmethod
    def resume(cls, db: Session, campaign_id: str) -> ResumeDescriptor:
        state = cls._load(db, campaign_id)
        queue = list(state.queue or [])
        return ResumeDescriptor(
            campaign_id=state.campaign_id,
            status=state.status,
            methodology_revision=state.methodology_revision,
            corpus_snapshot=state.corpus_snapshot,
            completed_count=len(state.completed_roots or []),
            remaining_count=len(queue),
            next_root=queue[0] if queue else None,
        )
