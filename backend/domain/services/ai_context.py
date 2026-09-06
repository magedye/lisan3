from typing import Any

from sqlalchemy.orm import Session

from ..models import (
    CorpusOccurrence,
    Hypothesis,
    IsolationState,
    ObservationArtifact,
    ResearchRun,
    SemanticClaim,
)


class AIContextBuilder:
    """
    Builds the exact contextual payload allowed for the AI model during a specific run stage.
    The evidence context contains admitted Quran material and same-run artifacts
    only. Accepted project memory is labelled separately and never becomes evidence.
    """

    @staticmethod
    def build_research_context(db: Session, run_id: str) -> dict[str, Any]:
        run = db.query(ResearchRun).filter(ResearchRun.id == run_id).first()
        if not run:
            raise ValueError(f"Run {run_id} not found")
        isolation = (
            db.query(IsolationState)
            .filter(IsolationState.research_run_id == run_id)
            .one_or_none()
        )
        if isolation is None:
            raise ValueError("Source isolation has not been initialized")
        if isolation.is_contaminated != "CLEAN":
            raise PermissionError("Run has actual prohibited-source contamination")

        # Start with standard allowed context
        context = {
            "run_id": run.id,
            "target_contract": run.target_contract,
            "target_expression": run.target_expression,
            "methodology_revision": run.methodology_revision,
            "stage": run.current_stage,
        }

        context["source_policy"] = {
            "evidence_sources": ["ADMITTED_CANONICAL_QURAN", "SAME_RUN_ARTIFACTS"],
            "prohibited": [
                "MODEL_MEMORY_AS_EVIDENCE",
                "DICTIONARY_OR_TAFSIR_IN_INTERNAL_INDUCTION",
                "UNTRACED_PRIOR_ANSWERS",
            ],
        }

        # Load target-scoped admitted corpus artifacts.
        occurrences = (
            db.query(CorpusOccurrence)
            .filter(
                CorpusOccurrence.snapshot_id == run.corpus_snapshot,
                CorpusOccurrence.expression == run.target_expression,
            )
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

        accepted = (
            db.query(SemanticClaim)
            .join(ResearchRun, SemanticClaim.research_run_id == ResearchRun.id)
            .filter(
                ResearchRun.target_expression == run.target_expression,
                SemanticClaim.contract_type == "ROOT_CONCEPT",
                SemanticClaim.canonical_state == "ACCEPTED",
            )
            .order_by(SemanticClaim.accepted_at.desc(), SemanticClaim.created_at.desc())
            .first()
        )
        context["accepted_project_knowledge"] = (
            None
            if accepted is None
            else {
                "claim_id": accepted.id,
                "root_concept": accepted.root_concept,
                "role": "PROJECT_KNOWLEDGE_NOT_PRIMARY_EVIDENCE",
                "evidence_refs": list(accepted.supporting_evidence or []),
            }
        )

        return context
