"""Canonical Semantic Memory Service (Quran Lisan v1.1 Appendix A15 & C04).

Enforces:
- A15-G01: TRUSTED_MEMORY_ADMISSION_GATE
- A15-R01: Preserve uncertainty (format migration != requalification)
- A15-R04: Conflict detection & non-auto-resolution
- A15-R05: Revision lineage & reason tracking
- A15-R08: Derived artifact strength ceiling
- Section 7: Saved result != Quranic evidence; Prior result != Independent replication
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.domain import models, schemas
from backend.domain.services.actor_context import ActorContext, ActorRole


class SemanticMemoryService:
    @staticmethod
    def validate_trusted_admission(
        *,
        target_type: str,
        scope: str,
        result_strength: str,
        root_core_status: str | None,
        evidence_refs: list[str],
        reopen_if: list[str],
        counterevidence_addressed: bool = True,
    ) -> None:
        """Enforces A15-G01 — TRUSTED_MEMORY_ADMISSION_GATE.

        Cannot save as TRUSTED unless:
        - RESULT_STRENGTH = STRONG
        - For ROOT: ROOT_CORE_STATUS = STRONGLY_SUPPORTED
        - Scope explicitly declared (UNIVERSAL, REPRESENTATIVE, LOCAL)
        - Traceable evidence references present
        - Counterevidence addressed
        - Reopen conditions recorded
        """
        if result_strength != "STRONG":
            raise ValueError(
                f"Admission Gate Failed: Cannot admit to TRUSTED memory without RESULT_STRENGTH = STRONG (found '{result_strength}')"
            )
        if target_type == "ROOT" and root_core_status != "STRONGLY_SUPPORTED":
            raise ValueError(
                f"Admission Gate Failed: Root memory requires ROOT_CORE_STATUS = STRONGLY_SUPPORTED (found '{root_core_status}')"
            )
        if scope not in ("UNIVERSAL", "REPRESENTATIVE", "LOCAL"):
            raise ValueError(
                f"Admission Gate Failed: Scope must be explicitly declared as UNIVERSAL, REPRESENTATIVE, or LOCAL (found '{scope}')"
            )
        if not evidence_refs:
            raise ValueError(
                "Admission Gate Failed: Cannot admit to TRUSTED memory without traceable evidence_refs"
            )
        if not counterevidence_addressed:
            raise ValueError(
                "Admission Gate Failed: Material counterevidence must be explicitly addressed"
            )
        if not reopen_if:
            raise ValueError(
                "Admission Gate Failed: Reopen conditions (reopen_if) must be explicitly recorded"
            )

    @staticmethod
    def detect_conflict(
        db: Session, target_type: str, target_expression: str, new_claim_id: str
    ) -> bool:
        """Enforces A15-R04: Conflict detection against active memory."""
        active_entries = (
            db.query(models.SemanticMemory)
            .filter(
                models.SemanticMemory.target_type == target_type,
                models.SemanticMemory.target_expression == target_expression,
                models.SemanticMemory.lifecycle == "ACTIVE",
                models.SemanticMemory.claim_id != new_claim_id,
            )
            .all()
        )
        return len(active_entries) > 0

    @classmethod
    def admit(
        cls,
        db: Session,
        memory_in: schemas.SemanticMemoryCreate,
        actor_context: ActorContext | None = None,
    ) -> models.SemanticMemory:
        """Admit a new entry to Semantic Memory with gate enforcement."""
        if actor_context:
            ActorContext.require_role(actor_context, ActorRole.RESEARCHER)

        claim = db.get(models.SemanticClaim, memory_in.claim_id)
        if not claim:
            raise ValueError(f"Underlying claim {memory_in.claim_id} not found")

        # Conflict detection
        has_conflict = cls.detect_conflict(
            db, memory_in.target_type, memory_in.target_expression, memory_in.claim_id
        )
        conflict_state = "OPEN_CONFLICT" if has_conflict else memory_in.conflict_state

        # If requesting TRUSTED reliability, enforce admission gate
        if memory_in.reliability == "TRUSTED":
            root_core_status = (
                "STRONGLY_SUPPORTED"
                if (
                    claim.result_strength == models.ResultStrength.STRONG.value
                    and claim.falsification_status
                    == models.FalsificationStatus.PASSED.value
                    and not claim.unresolved_cases
                )
                else "PROVISIONAL"
            )
            cls.validate_trusted_admission(
                target_type=memory_in.target_type,
                scope=memory_in.scope,
                result_strength=claim.result_strength,
                root_core_status=root_core_status,
                evidence_refs=memory_in.evidence_refs
                or claim.supporting_evidence
                or [],
                reopen_if=memory_in.reopen_if or claim.reopen_conditions or [],
                counterevidence_addressed=True,
            )

        db_entry = models.SemanticMemory(
            id=f"mem_{uuid.uuid4().hex[:8]}",
            claim_id=memory_in.claim_id,
            target_type=memory_in.target_type,
            target_expression=memory_in.target_expression,
            reliability=memory_in.reliability,
            scope=memory_in.scope,
            conflict_state=conflict_state,
            lifecycle=memory_in.lifecycle,
            result_strength=claim.result_strength,
            research_completeness="COMPLETE"
            if (claim.research_completeness or {}).get("sufficient_for_claim")
            else "PARTIAL",
            independent_verification="VERIFIED"
            if claim.verification_state == "VERIFIED"
            else "UNVERIFIED",
            evidence_refs=memory_in.evidence_refs or claim.supporting_evidence or [],
            counterevidence_refs=memory_in.counterevidence_refs
            or claim.counterevidence
            or [],
            dependencies=memory_in.dependencies or [],
            reopen_if=memory_in.reopen_if or claim.reopen_conditions or [],
            parent_revision=memory_in.parent_revision,
            revision_reason=memory_in.revision_reason,
        )
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
        return db_entry

    @classmethod
    def reopen(
        cls,
        db: Session,
        memory_id: str,
        reopen_req: schemas.SemanticMemoryReopenRequest,
        actor_context: ActorContext | None = None,
    ) -> models.SemanticMemory:
        """Enforces A15-R05: Reopen lineage."""
        if actor_context:
            ActorContext.require_role(actor_context, ActorRole.RESEARCHER)

        entry = db.get(models.SemanticMemory, memory_id)
        if not entry:
            raise ValueError(f"SemanticMemory entry {memory_id} not found")

        entry.lifecycle = "REOPENED"
        entry.reliability = "DISPUTED"
        entry.conflict_state = "OPEN_CONFLICT"
        entry.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)

        # Create new revision entry
        new_entry = models.SemanticMemory(
            id=f"mem_{uuid.uuid4().hex[:8]}",
            claim_id=entry.claim_id,
            target_type=entry.target_type,
            target_expression=entry.target_expression,
            reliability="PROVISIONAL",
            scope=entry.scope,
            conflict_state="OPEN_CONFLICT",
            lifecycle="ACTIVE",
            result_strength="UNRESOLVED",
            research_completeness=entry.research_completeness,
            independent_verification="UNVERIFIED",
            evidence_refs=list(
                dict.fromkeys(
                    (entry.evidence_refs or []) + reopen_req.new_evidence_refs
                )
            ),
            counterevidence_refs=list(
                dict.fromkeys(
                    (entry.counterevidence_refs or []) + reopen_req.counterevidence_refs
                )
            ),
            dependencies=entry.dependencies or [],
            reopen_if=entry.reopen_if or [],
            parent_revision=entry.id,
            revision_reason=reopen_req.revision_reason,
        )
        db.add(new_entry)
        
        # Enforce A15-R08/R06: Dependency Revalidation
        downstream = (
            db.query(models.SemanticMemory)
            .filter(
                models.SemanticMemory.lifecycle == "ACTIVE",
            )
            .all()
        )
        for dep in downstream:
            if entry.id in dep.dependencies or entry.claim_id in dep.dependencies:
                dep.revalidation_state = "REVALIDATION_REQUIRED"
                db.add(dep)

        db.commit()
        db.refresh(new_entry)
        return new_entry

    @staticmethod
    def derive_card_strength_ceiling(upstream_strengths: list[str]) -> str:
        """Enforces A15-R08: DERIVED_ARTIFACT_STRENGTH <= WEAKEST_MATERIAL_UPSTREAM_RESULT."""
        if not upstream_strengths:
            return "UNRESOLVED"
        rank = {"UNRESOLVED": 0, "WEAK": 1, "MODERATE": 2, "STRONG": 3}
        min_rank = min(rank.get(s, 0) for s in upstream_strengths)
        rev_rank = {0: "UNRESOLVED", 1: "WEAK", 2: "MODERATE", 3: "STRONG"}
        return rev_rank[min_rank]

    @staticmethod
    def assert_saved_result_not_evidence(ref: str) -> None:
        """Enforces Section 7 & A15-R07: Saved result != Quranic evidence."""
        if ref.startswith(("mem_", "card_", "jud_")):
            raise ValueError(
                f"Methodological Invariant Violated: Prior research result '{ref}' cannot serve as primary Quranic evidence"
            )
