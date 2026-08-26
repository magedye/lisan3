"""Durable, source-bound Methodology revision authority."""

import hashlib
from pathlib import Path
from typing import cast

from sqlalchemy.orm import Session

from backend.domain import models
from backend.infrastructure.database import REPOSITORY_ROOT

CURRENT = "CURRENT"
RETIRED = "RETIRED"
QURAN_INTERNAL_CUMULATIVE_RUN = "QURAN_INTERNAL_CUMULATIVE_RUN"


def _source_path(reference: str) -> Path | None:
    candidate = (REPOSITORY_ROOT / reference).resolve()
    try:
        candidate.relative_to(REPOSITORY_ROOT.resolve())
    except ValueError:
        return None
    return candidate


def methodology_authority_failures(
    revision: models.MethodologyRevision,
) -> list[str]:
    lifecycle_state = cast(str, revision.lifecycle_state)
    research_run_eligible = cast(bool, revision.research_run_eligible)
    allowed_use = cast(str, revision.allowed_use)
    source_reference = cast(str, revision.source_reference)
    source_sha256 = cast(str, revision.source_sha256)
    failures: list[str] = []
    if lifecycle_state != CURRENT:
        failures.append(
            f"Methodology revision lifecycle is '{lifecycle_state}', expected 'CURRENT'"
        )
    if not research_run_eligible:
        failures.append("Methodology revision is not eligible for ResearchRun admission")
    if allowed_use != QURAN_INTERNAL_CUMULATIVE_RUN:
        failures.append(
            "Methodology revision is not approved for QURAN_INTERNAL_CUMULATIVE_RUN"
        )

    source_path = _source_path(source_reference)
    if source_path is None:
        failures.append("Methodology source reference escapes the repository")
    elif not source_path.is_file():
        failures.append("Methodology source artifact is missing")
    else:
        actual_sha256 = hashlib.sha256(source_path.read_bytes()).hexdigest()
        if actual_sha256 != source_sha256:
            failures.append("Methodology source artifact hash does not match its revision")
    return failures


def eligible_methodology_revision_ids(db: Session) -> list[str]:
    revisions = (
        db.query(models.MethodologyRevision)
        .order_by(models.MethodologyRevision.id)
        .all()
    )
    return [
        cast(str, revision.id)
        for revision in revisions
        if not methodology_authority_failures(revision)
    ]
