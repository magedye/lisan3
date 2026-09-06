"""Unified external-hypothesis register service (INT-EXT-001..007 / Request 01 §10).

One mechanism for every external claim. External sources generate hypotheses and
tests only; they never gain authority, carry no confidence field, and never enter
accepted project memory. Rule claims and an author's applications are recorded
separately so a strong rule with a strained example is not conflated.
"""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from backend.domain import models

# Documented, high-priority external axial-meaning source. High priority means
# "tested early", NOT "believed more" — it receives no authority bonus.
JABAL_SOURCE = "المعجم الاشتقاقي المؤصل لألفاظ القرآن الكريم"
JABAL_AUTHOR = "محمد حسن حسن جبل"
JABAL_LOCATOR = "https://usul.ai/ar/t/almajm-alashtqaqy-almusl"

_TERMINAL_STATUSES = {
    models.ExternalHypothesisStatus.SUPPORTED.value,
    models.ExternalHypothesisStatus.PARTIALLY_SUPPORTED.value,
    models.ExternalHypothesisStatus.NOT_SUPPORTED.value,
    models.ExternalHypothesisStatus.FALSIFIED.value,
    models.ExternalHypothesisStatus.UNRESOLVED.value,
}


class ExternalHypothesisService:
    @staticmethod
    def register(
        db: Session,
        *,
        claim_type: str,
        source: str,
        author: str,
        claim: str,
        target_scope: str,
        provenance: str,
        claim_role: str = models.ExternalClaimRole.RULE_CLAIM.value,
        source_locator: str | None = None,
        normalized_claim: str | None = None,
        test_plan: str | None = None,
        research_run_id: str | None = None,
    ) -> models.ExternalHypothesisRecord:
        record = models.ExternalHypothesisRecord(
            id=f"exh_{uuid.uuid4().hex[:8]}",
            claim_type=claim_type,
            source=source,
            author=author,
            source_locator=source_locator,
            claim=claim,
            normalized_claim=normalized_claim,
            target_scope=target_scope,
            claim_role=claim_role,
            status=models.ExternalHypothesisStatus.EXTERNAL_CANDIDATE.value,
            test_plan=test_plan,
            test_evidence_refs=[],
            counterevidence_refs=[],
            provenance=provenance,
            research_run_id=research_run_id,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def record_test_result(
        db: Session,
        record_id: str,
        *,
        status: str,
        result: str,
        test_evidence_refs: list[str] | None = None,
        counterevidence_refs: list[str] | None = None,
    ) -> models.ExternalHypothesisRecord:
        record = db.get(models.ExternalHypothesisRecord, record_id)
        if record is None:
            raise LookupError(f"External hypothesis {record_id} not found")
        if status not in _TERMINAL_STATUSES | {
            models.ExternalHypothesisStatus.TESTED.value
        }:
            raise ValueError(f"Invalid external hypothesis test status: {status}")
        record.status = status
        record.result = result
        if test_evidence_refs is not None:
            record.test_evidence_refs = test_evidence_refs
        if counterevidence_refs is not None:
            record.counterevidence_refs = counterevidence_refs
        db.commit()
        db.refresh(record)
        return record

    @classmethod
    def register_jabal_root_meaning(
        cls,
        db: Session,
        *,
        root: str,
        claim: str,
        research_run_id: str | None = None,
    ) -> models.ExternalHypothesisRecord:
        """Register Jabal's documented axial/root meaning as a high-priority
        ROOT_MEANING_CANDIDATE (RULE_CLAIM). No authority bonus is applied."""
        return cls.register(
            db,
            claim_type=models.ExternalClaimType.ROOT_MEANING_CANDIDATE.value,
            source=JABAL_SOURCE,
            author=JABAL_AUTHOR,
            source_locator=JABAL_LOCATOR,
            claim=claim,
            target_scope=root,
            provenance=f"external:{JABAL_AUTHOR}",
            claim_role=models.ExternalClaimRole.RULE_CLAIM.value,
            research_run_id=research_run_id,
        )
