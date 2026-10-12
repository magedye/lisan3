import hashlib
import json
import uuid

from sqlalchemy.orm import Session

from backend.domain.models import ClaimRevision, SemanticClaim, utc_now_naive
from backend.domain.services.actor_context import ActorContext


class ClaimRevisionService:
    @staticmethod
    def calculate_payload_hash(payload: dict) -> str:
        """Calculate a deterministic hash of the semantic payload."""
        payload_str = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(payload_str.encode("utf-8")).hexdigest()

    @staticmethod
    def create_successor(
        db: Session,
        claim: SemanticClaim,
        payload: dict,
        correction_reason: str,
        actor_context: ActorContext,
    ) -> ClaimRevision:
        """
        Create a new revision for a claim, freezing the predecessor.
        This enforces that N cannot be edited in place and N+1 is created.
        """
        # Validate predecessor exists
        predecessor = (
            db.query(ClaimRevision)
            .filter(
                ClaimRevision.claim_id == claim.id,
                ClaimRevision.revision_number == claim.revision_id,
            )
            .first()
        )

        if predecessor is None:
            raise ValueError(
                f"Predecessor revision {claim.revision_id} not found for claim {claim.id}"
            )

        if not predecessor.frozen_at:
            predecessor.frozen_at = utc_now_naive()
            db.add(predecessor)

        # Predecessor becomes superseded for new review applicability
        predecessor.superseded = True
        db.add(predecessor)

        # Create successor N+1
        new_revision_number = claim.revision_id + 1
        semantic_payload_hash = ClaimRevisionService.calculate_payload_hash(payload)

        successor = ClaimRevision(
            id=f"rev_{uuid.uuid4().hex[:8]}",
            claim_id=claim.id,
            revision_number=new_revision_number,
            predecessor_revision_id=predecessor.id,
            correction_reason=correction_reason,
            payload=payload,
            semantic_payload_hash=semantic_payload_hash,
            creation_actor=actor_context.identity,
            created_at=utc_now_naive(),
            frozen_at=None,
            superseded=False,
        )

        db.add(successor)
        db.flush()

        # Bind claim to new revision
        claim.revision_id = new_revision_number
        db.add(claim)

        return successor

    @staticmethod
    def freeze_revision(db: Session, revision: ClaimRevision) -> None:
        """Freeze a revision, making it immutable to further changes."""
        if not revision.frozen_at:
            revision.frozen_at = utc_now_naive()
            db.add(revision)

    @staticmethod
    def get_current_revision(db: Session, claim_id: str) -> ClaimRevision:
        """Identify and return the current active revision for a claim."""
        claim = db.query(SemanticClaim).filter(SemanticClaim.id == claim_id).first()
        if not claim:
            raise ValueError(f"Claim {claim_id} not found")

        current = (
            db.query(ClaimRevision)
            .filter(
                ClaimRevision.claim_id == claim_id,
                ClaimRevision.revision_number == claim.revision_id,
            )
            .first()
        )

        if not current:
            raise ValueError(
                f"Current revision {claim.revision_id} not found for claim {claim_id}"
            )

        return current

    @staticmethod
    def assert_revision_not_stale(
        db: Session, claim_id: str, revision_number: int
    ) -> None:
        """
        Prevent stale verification or review against an obsolete revision.
        Throws ValueError if the revision_number is not the current active revision.
        """
        claim = db.query(SemanticClaim).filter(SemanticClaim.id == claim_id).first()
        if not claim:
            raise ValueError(f"Claim {claim_id} not found")

        if claim.revision_id != revision_number:
            raise ValueError(
                f"Stale revision: revision {revision_number} is obsolete. "
                f"Current revision is {claim.revision_id}."
            )
