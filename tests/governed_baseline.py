"""Shared helpers to seed a genuinely GOVERNED runtime baseline in a test DB.

Canonical Runtime Qualification support. These helpers construct the minimum
authority-bound state the governed pipeline legitimately requires:

  * a production-valid Tanzil CorpusSnapshot (the exact owner-authorized id,
    with every authority-bound field matching the canonical admission record so
    ``is_production_validated`` is genuinely True — NOT a hand-waved status);
  * the CURRENT, source-bound Methodology revision whose sha256 matches the live
    ``skills/lisan-semantic-extraction/SKILL.md``;
  * optional word-level ``StructuralToken`` rows for a given root so the
    word-level evidence bridge / completeness has real occurrence identity.

They do NOT fabricate provenance: the snapshot identity/hashes are the real
authority-bound values, the methodology hash is recomputed from the live file,
and structural tokens are explicit, caller-supplied word refs (a test fixture,
never the five production roots).
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path

from backend.domain import models
from backend.domain.services.corpus.authority import CANONICAL_CORPUS_ADMISSIONS

CURRENT_METHODOLOGY_ID = "method-current"
AUTHORIZED_TANZIL_SNAPSHOT = "snap_tanzil_1_1_ac0724796cbb"


def seed_production_valid_tanzil_snapshot(db) -> str:
    """Seed (idempotently) the owner-authorized, production-valid Tanzil snapshot."""
    admission = CANONICAL_CORPUS_ADMISSIONS["TANZIL_QURAN_UTHMANI"]
    if db.get(models.CorpusSnapshot, admission.authorized_snapshot_id) is None:
        db.add(
            models.CorpusSnapshot(
                id=admission.authorized_snapshot_id,
                canonical_text_source=admission.source_id,
                canonical_text_version=admission.canonical_text_version,
                canonical_text_hash=admission.expected_hash,
                validation_status="VALIDATED",
                source_role_status="SOURCE_ROLE_APPROVED",
                artifact_presence_status="ARTIFACT_PRESENT",
                expected_canonical_text_hash=admission.expected_hash,
                hash_verification_status="HASH_VERIFIED",
                import_validation_status="IMPORT_VALIDATED",
                activation_status="PRODUCTION_ACTIVE",
                artifact_provenance=admission.provenance_reference,
                artifact_reference=admission.artifact_reference,
                artifact_size_bytes=admission.expected_bytes,
                artifact_format=admission.artifact_format,
                artifact_verified_at=datetime.now(timezone.utc).replace(tzinfo=None),
                artifact_verification_revision=admission.verification_revision,
                identity_index_reference=admission.identity_index_reference,
                identity_index_sha256=admission.identity_index_sha256,
                verse_count=admission.expected_verse_count,
                canon_001_reconciliation=admission.canon_001_reconciliation,
                fixture_only=False,
            )
        )
        db.commit()
    return str(admission.authorized_snapshot_id)


def seed_current_methodology(db, revision_id: str = CURRENT_METHODOLOGY_ID) -> str:
    """Seed (idempotently) the CURRENT source-bound methodology revision."""
    if db.get(models.MethodologyRevision, revision_id) is None:
        skill = Path("skills/lisan-semantic-extraction/SKILL.md")
        digest = hashlib.sha256(skill.read_bytes()).hexdigest()
        db.add(
            models.MethodologyRevision(
                id=revision_id,
                methodology_id="LISAN_QURANIC_SEMANTIC_EXTRACTION",
                revision=f"skill-sha256:{digest[:12]}",
                lifecycle_state="CURRENT",
                authority_reference="SIMPLIFIED_AI_AUTHORITY_AND_GOVERNANCE_CONTRACT.md",
                source_reference=skill.as_posix(),
                source_sha256=digest,
                allowed_use="QURAN_INTERNAL_CUMULATIVE_RUN",
                research_run_eligible=True,
            )
        )
        db.commit()
    return revision_id


def seed_structural_tokens(
    db,
    snapshot_id: str,
    root: str,
    word_refs: list[str],
    *,
    extraction_version: str = "test-fixture-v1",
    attribution_status: str = "CONFIRMED",
    source_id: str = "TEST_STRUCTURAL_FIXTURE",
) -> list[str]:
    """Seed word-level StructuralToken rows for a root (a test fixture root only).

    ``word_refs`` are ``surah:ayah:word:segment`` strings. Returns the word_refs.
    """
    for word_ref in word_refs:
        verse_ref = ":".join(word_ref.split(":")[:2])
        db.add(
            models.StructuralToken(
                id=f"stok_{snapshot_id}_{word_ref.replace(':', '_')}_{extraction_version}",
                snapshot_id=snapshot_id,
                word_ref=word_ref,
                verse_ref=verse_ref,
                root=root,
                form="TEST_FORM",
                pos_tag="N",
                source_id=source_id,
                source_version="test",
                extraction_version=extraction_version,
                attribution_status=attribution_status,
            )
        )
    db.commit()
    return list(word_refs)
