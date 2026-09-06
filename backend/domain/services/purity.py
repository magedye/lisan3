"""Methodological diagnostics; diagnostics are not research gates."""

from sqlalchemy.orm import Session

from backend.domain import models

DIAGNOSTIC_DIMENSIONS = (
    "DICTIONARY_FIRST",
    "CONTEXTUAL_LEAKAGE",
    "HERITAGE_BIAS",
    "TAFSIR_CONTAMINATION",
    "FORCED_UNIFICATION",
    "GENERIC_OVEREXTRACTION",
    "LETTER_SEMANTICS_OVERRELIANCE",
    "CIRCULAR_CONFIRMATION",
)


def evaluate_methodology_diagnostics(
    claim: models.SemanticClaim, db: Session
) -> tuple[list[dict], list[str], list[str]]:
    findings: list[dict] = []
    hard_blockers: list[str] = []
    warnings: list[str] = []
    run_id = claim.research_run_id

    isolation = (
        db.query(models.IsolationState)
        .filter(models.IsolationState.research_run_id == run_id)
        .one_or_none()
    )
    if isolation is not None and isolation.is_contaminated != "CLEAN":
        hard_blockers.append("PROHIBITED_SOURCE_CONTAMINATION")

    observations = (
        db.query(models.ObservationArtifact)
        .filter(models.ObservationArtifact.research_run_id == run_id)
        .all()
    )
    hypotheses = (
        db.query(models.Hypothesis)
        .filter(models.Hypothesis.research_run_id == run_id)
        .all()
    )
    first_observation = min((item.created_at for item in observations), default=None)
    first_hypothesis = min((item.created_at for item in hypotheses), default=None)

    if first_hypothesis and (
        first_observation is None or first_hypothesis < first_observation
    ):
        warnings.append("DICTIONARY_FIRST")
        findings.append(
            {
                "dimension": "DICTIONARY_FIRST",
                "status": "FLAGGED",
                "severity": "MEDIUM",
                "details": "A hypothesis predates the first persisted corpus observation.",
                "evidence_refs": [f"hypothesis:{hypotheses[0].id}"],
                "hard_blocker": False,
            }
        )
    elif first_observation and first_hypothesis:
        findings.append(
            {
                "dimension": "DICTIONARY_FIRST",
                "status": "EVALUATED_CLEAN",
                "severity": "NONE",
                "details": "Persisted corpus observation precedes hypothesis formation.",
                "evidence_refs": [
                    f"observation:{observations[0].id}",
                    f"hypothesis:{hypotheses[0].id}",
                ],
                "hard_blocker": False,
            }
        )
    else:
        findings.append(
            {
                "dimension": "DICTIONARY_FIRST",
                "status": "NOT_EVALUATED",
                "severity": "INFO",
                "details": "Ordered observation and hypothesis evidence is incomplete.",
                "evidence_refs": [],
                "hard_blocker": False,
            }
        )

    for dimension in DIAGNOSTIC_DIMENSIONS[1:]:
        findings.append(
            {
                "dimension": dimension,
                "status": "NOT_EVALUATED",
                "severity": "INFO",
                "details": "The required deterministic diagnostic extractor is unavailable.",
                "evidence_refs": [],
                "hard_blocker": False,
            }
        )
    if hard_blockers:
        findings.append(
            {
                "dimension": "SOURCE_ISOLATION",
                "status": "FLAGGED",
                "severity": "CRITICAL",
                "details": isolation.contamination_reason
                or "Actual prohibited-source contamination was recorded.",
                "evidence_refs": [f"isolation:{isolation.id}"],
                "hard_blocker": True,
            }
        )
    return findings, hard_blockers, warnings
