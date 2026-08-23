from sqlalchemy.orm import Session

from backend.domain import models

PURITY_DIMENSIONS = (
    "DICTIONARY_FIRST",
    "CONTEXTUAL_LEAKAGE",
    "HERITAGE_BIAS",
    "TAFSIR_CONTAMINATION",
    "FORCED_UNIFICATION",
    "GENERIC_OVEREXTRACTION",
    "LETTER_SEMANTICS_OVERRELIANCE",
    "CIRCULAR_CONFIRMATION",
)


def evaluate_run_methodological_purity(
    run_id: str | None, db: Session
) -> tuple[int, str, list[dict], list[str]]:
    findings: list[dict] = []
    flags: list[str] = []
    purity_score = 100

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

    if not observations and not hypotheses:
        for dimension in PURITY_DIMENSIONS:
            findings.append(
                {
                    "dimension": dimension,
                    "status": "NOT_EVALUATED",
                    "severity": "CRITICAL",
                    "details": "Missing required observation or hypothesis evidence for purity evaluation.",
                }
            )
        return 0, "NOT_EVALUATED", findings, flags

    first_observation = min((item.created_at for item in observations), default=None)
    first_hypothesis = min((item.created_at for item in hypotheses), default=None)
    if first_hypothesis and (
        not first_observation or first_hypothesis < first_observation
    ):
        findings.append(
            {
                "dimension": "DICTIONARY_FIRST",
                "status": "FLAGGED",
                "severity": "HIGH",
                "details": "Hypothesis formulated prior to corpus observation (Dictionary First).",
            }
        )
        flags.append("dictionary_first")
        purity_score -= 30
    elif (
        first_observation and first_hypothesis and first_observation <= first_hypothesis
    ):
        findings.append(
            {
                "dimension": "DICTIONARY_FIRST",
                "status": "EVALUATED_CLEAN",
                "severity": "NONE",
                "details": "Corpus observations precede hypothesis.",
            }
        )
    else:
        findings.append(
            {
                "dimension": "DICTIONARY_FIRST",
                "status": "NOT_EVALUATED",
                "severity": "MEDIUM",
                "details": "Missing temporal evidence to evaluate sequence.",
            }
        )
        purity_score -= 10

    for dimension in PURITY_DIMENSIONS[1:]:
        findings.append(
            {
                "dimension": dimension,
                "status": "NOT_EVALUATED",
                "severity": "MEDIUM",
                "details": "Dimension currently unsupported by evidence extractors.",
            }
        )
        purity_score -= 10

    if purity_score >= 85:
        rating = "PURE"
    elif purity_score >= 65:
        rating = "NEAR_PURE"
    elif purity_score >= 40:
        rating = "SUSPICIOUS"
    else:
        rating = "CONTAMINATED"
    return max(purity_score, 0), rating, findings, flags


def evaluate_methodological_purity(
    claim: models.SemanticClaim, db: Session
) -> tuple[int, str, list[dict], list[str]]:
    return evaluate_run_methodological_purity(claim.research_run_id, db)
