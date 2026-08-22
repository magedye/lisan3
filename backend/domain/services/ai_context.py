from typing import Any

from sqlalchemy.orm import Session

from ..models import CorpusOccurrence, Hypothesis, ObservationArtifact, ResearchRun
from .isolation import BlindLabIsolationService, IsolationContaminationException


class AIContextBuilder:
    """
    Builds the exact contextual payload allowed for the AI model during a specific run stage.
    Critically, it enforces Blind Lab isolation. If INTERNAL_LOCK is not passed, it strictly
    excludes prohibited prior semantic artifacts (Root Cores, dictionary definitions, etc.).
    """

    @staticmethod
    def build_research_context(db: Session, run_id: str) -> dict[str, Any]:
        run = db.query(ResearchRun).filter(ResearchRun.id == run_id).first()
        if not run:
            raise ValueError(f"Run {run_id} not found")

        # Start with standard allowed context
        context = {
            "run_id": run.id,
            "target_contract": run.target_contract,
            "target_expression": run.target_expression,
            "methodology_revision": run.methodology_revision,
            "stage": run.current_stage,
        }

        # Load admitted corpus artifacts
        occurrences = (
            db.query(CorpusOccurrence)
            .filter(CorpusOccurrence.snapshot_id == run.corpus_snapshot)
            .all()
        )
        context["corpus_occurrences"] = [
            {"ref": o.id, "text": o.text} for o in occurrences
        ]

        # Load structural observations
        observations = (
            db.query(ObservationArtifact)
            .filter(ObservationArtifact.research_run_id == run_id)
            .all()
        )
        context["structural_observations"] = [
            {
                "ref": o.id,
                "occurrence_ref": o.occurrence_ref,
                "local_context": o.local_context,
            }
            for o in observations
        ]

        # Load hypotheses generated in this run
        hypotheses = (
            db.query(Hypothesis).filter(Hypothesis.research_run_id == run_id).all()
        )
        context["active_hypotheses"] = [
            {"id": h.id, "type": h.hypothesis_type, "statement": h.statement}
            for h in hypotheses
        ]

        # Enforce Blind Lab Isolation
        try:
            # Check if internal lock is achieved. If so, full semantic knowledge might be permitted.
            BlindLabIsolationService.enforce_semantic_isolation(db, run_id)
            context["semantic_knowledge_access"] = "GRANTED"
            # Here we would load semantic registries if requested, but for now we just flag it.
            context["prior_semantics"] = ["(Simulated admitted post-lock definitions)"]
        except IsolationContaminationException:
            # BLOCKED!
            context["semantic_knowledge_access"] = "BLIND_LAB_RESTRICTED"
            # Strictly do NOT append any prior dictionary or Root Core data.

        return context
