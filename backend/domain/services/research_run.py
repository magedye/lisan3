import uuid

from sqlalchemy.orm import Session

from backend.domain import models
from backend.domain.services.actor_context import ActorContext, ActorRole
from backend.domain.services.run_admission import ResearchRunAdmissionPolicy


class ResearchRunService:
    @staticmethod
    def create_run(
        db: Session,
        target_contract: str,
        target_expression: str,
        actor_context: ActorContext,
    ) -> models.ResearchRun:
        ActorContext.require_role(actor_context, ActorRole.RESEARCHER)
        authority = ResearchRunAdmissionPolicy.resolve(db)
        if not authority.accepted:
            raise ValueError(f"Run admission denied: {'; '.join(authority.reasons)}")

        full_authority_context = dict(authority.authority_context)
        full_authority_context["actor"] = actor_context.identity

        db_run = models.ResearchRun(
            id=f"run_{uuid.uuid4().hex[:8]}",
            target_contract=target_contract,
            target_expression=target_expression,
            methodology_revision=authority.methodology_revision_id,
            corpus_snapshot=authority.corpus_snapshot_id,
            authority_context=full_authority_context,
        )
        db.add(db_run)
        db.flush()
        return db_run
