import uuid

from sqlalchemy.orm import Session

from backend.domain import models
from backend.domain.services.actor_context import ActorContext, ActorRole
from backend.domain.services.canonicalization import (
    reopen_accepted_results_for_new_evidence,
)


class ObservationService:
    @staticmethod
    def create_observation(
        db: Session,
        run_id: str,
        occurrence_ref: str,
        form: str,
        syntax: str,
        participant_roles: str,
        local_context: str,
        unresolved_ambiguity: str,
        actor_context: ActorContext,
    ) -> models.ObservationArtifact:
        ActorContext.require_role(actor_context, ActorRole.RESEARCHER)

        state = (
            db.query(models.IsolationState)
            .filter(models.IsolationState.research_run_id == run_id)
            .first()
        )
        if not state:
            raise ValueError("Run has no isolation preflight")
        if state.is_contaminated == "PRIOR_CONTAMINATED":
            raise PermissionError("Cannot record observation: Run is contaminated")

        run = (
            db.query(models.ResearchRun).filter(models.ResearchRun.id == run_id).first()
        )
        if run is None:
            raise LookupError("Run not found")

        occurrence = db.get(models.CorpusOccurrence, occurrence_ref)
        occurrence_valid = (
            occurrence is not None and occurrence.snapshot_id == run.corpus_snapshot
        )
        if not occurrence_valid:
            try:
                token = (
                    db.query(models.StructuralToken)
                    .filter(
                        models.StructuralToken.snapshot_id == run.corpus_snapshot,
                        models.StructuralToken.word_ref == occurrence_ref,
                    )
                    .first()
                )
                occurrence_valid = token is not None
            except Exception:
                pass

        if not occurrence_valid:
            raise ValueError(
                "Observation occurrence is absent or outside the run corpus"
            )

        db_artifact = models.ObservationArtifact(
            id=f"obs_{uuid.uuid4().hex[:8]}",
            research_run_id=run_id,
            occurrence_ref=occurrence_ref,
            form=form,
            syntax=syntax,
            participant_roles=participant_roles,
            local_context=local_context,
            unresolved_ambiguity=unresolved_ambiguity,
        )
        db.add(db_artifact)
        db.flush()

        reopen_accepted_results_for_new_evidence(db, run, db_artifact)
        return db_artifact
