"""Owner-authorized, fail-closed Tanzil production activation."""

import datetime
import json
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from sqlalchemy.orm import Session

from backend.domain import models
from backend.domain.services.corpus.authority import (
    CANONICAL_ACTIVATION_PENDING,
    PRODUCTION_ACTIVE,
    get_canonical_admission,
    import_validation_failures,
)
from backend.domain.services.corpus.importer import TanzilPreActivationImporter
from backend.domain.services.methodology_authority import (
    eligible_methodology_revision_ids,
)

AUTHORIZED_SNAPSHOT_ID = "snap_tanzil_1_1_ac0724796cbb"
# Aligned with the simplified-governance methodology revision seeded by
# alembic f1a6c3d9e204 (source-bound to the current SKILL.md sha256).
AUTHORIZED_METHODOLOGY_ID = "LISAN_QURANIC_SEMANTIC_EXTRACTION@01784170cac4"
ACTIVATION_ACTOR = "OWNER_AUTHORITY"
ACTIVATION_ACTION = "AUTHORIZE_TANZIL_PRODUCTION_ACTIVATION"
ACTIVATION_REASON = (
    "Owner authorized production activation for the exact governed Tanzil 1.1 "
    "snapshot after live prerequisite re-verification."
)


class CorpusActivationRejected(ValueError):
    """The requested activation does not satisfy canonical authority."""


@dataclass(frozen=True)
class CorpusActivationResult:
    snapshot: models.CorpusSnapshot
    audit_log: models.AuditLog
    activation_timestamp: datetime.datetime


class TanzilProductionActivationService:
    """Activate only the exact owner-authorized Tanzil snapshot."""

    @classmethod
    def activate(
        cls,
        db: Session,
        *,
        repository_root: Path | None = None,
    ) -> CorpusActivationResult:
        admission = get_canonical_admission("TANZIL_QURAN_UTHMANI")
        if admission is None:
            raise CorpusActivationRejected("Tanzil has no canonical admission record")
        if admission.activation_status != PRODUCTION_ACTIVE:
            raise CorpusActivationRejected(
                "Tanzil canonical admission is not authorized for production activation"
            )
        if admission.authorized_snapshot_id != AUTHORIZED_SNAPSHOT_ID:
            raise CorpusActivationRejected(
                "Tanzil authority does not bind the exact authorized snapshot"
            )
        if not admission.activation_decision_reference:
            raise CorpusActivationRejected(
                "Tanzil authority has no production activation decision reference"
            )

        snapshot = db.get(models.CorpusSnapshot, AUTHORIZED_SNAPSHOT_ID)
        if snapshot is None:
            raise CorpusActivationRejected(
                f"Authorized CorpusSnapshot '{AUTHORIZED_SNAPSHOT_ID}' does not exist"
            )
        if snapshot.activation_status != CANONICAL_ACTIVATION_PENDING:
            raise CorpusActivationRejected(
                "Authorized CorpusSnapshot is not in CANONICAL_ACTIVATION_PENDING"
            )
        if snapshot.validation_status != "PENDING":
            raise CorpusActivationRejected(
                "Authorized CorpusSnapshot is not in the pre-activation PENDING state"
            )

        verified = TanzilPreActivationImporter.import_candidate(
            db, repository_root=repository_root
        )
        if verified.created or verified.snapshot.id != AUTHORIZED_SNAPSHOT_ID:
            raise CorpusActivationRejected(
                "Activation verification did not reuse the exact authorized snapshot"
            )
        failures = import_validation_failures(snapshot)
        if failures:
            raise CorpusActivationRejected(
                "Tanzil import prerequisites failed: " + "; ".join(failures)
            )

        competing = (
            db.query(models.CorpusSnapshot)
            .filter(
                models.CorpusSnapshot.id != AUTHORIZED_SNAPSHOT_ID,
                models.CorpusSnapshot.activation_status == PRODUCTION_ACTIVE,
            )
            .order_by(models.CorpusSnapshot.id)
            .all()
        )
        if competing:
            ids = ", ".join(cast(str, item.id) for item in competing)
            raise CorpusActivationRejected(
                "A competing production-active CorpusSnapshot already exists: " + ids
            )

        eligible_methodologies = eligible_methodology_revision_ids(db)
        if AUTHORIZED_METHODOLOGY_ID not in eligible_methodologies:
            raise CorpusActivationRejected(
                "The authorized Methodology revision is not eligible for ResearchRun admission"
            )

        activated_at = datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
        prior_state = {
            "activation_status": cast(str, snapshot.activation_status),
            "validation_status": cast(str, snapshot.validation_status),
        }
        new_state = {
            "activation_status": PRODUCTION_ACTIVE,
            "artifact_bytes": admission.expected_bytes,
            "artifact_path": admission.artifact_reference,
            "artifact_sha256": admission.expected_hash,
            "artifact_version": admission.canonical_text_version,
            "authority_decision_reference": admission.activation_decision_reference,
            "identity_index_path": admission.identity_index_reference,
            "identity_index_sha256": admission.identity_index_sha256,
            "import_validation_status": snapshot.import_validation_status,
            "reason": ACTIVATION_REASON,
            "snapshot_id": AUTHORIZED_SNAPSHOT_ID,
            "surah_count": admission.expected_surah_count,
            "validation_status": "VALIDATED",
            "verification_revision": admission.verification_revision,
            "verse_count": admission.expected_verse_count,
        }
        snapshot.activation_status = PRODUCTION_ACTIVE
        snapshot.validation_status = "VALIDATED"
        audit_log = models.AuditLog(
            id="aud_tanzil_production_activation_ac0724796cbb",
            entity_id=AUTHORIZED_SNAPSHOT_ID,
            entity_type="CorpusSnapshot",
            action=ACTIVATION_ACTION,
            previous_state=json.dumps(prior_state, sort_keys=True),
            new_state=json.dumps(new_state, sort_keys=True),
            actor=ACTIVATION_ACTOR,
            created_at=activated_at,
        )
        db.add(audit_log)
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise
        db.refresh(snapshot)
        db.refresh(audit_log)
        return CorpusActivationResult(snapshot, audit_log, activated_at)
