import hashlib
import json
import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.domain import models


class InternalSnapshotService:
    @staticmethod
    def create_snapshot(
        db: Session,
        claim: models.SemanticClaim,
        corpus_identity: str,
        methodology_version: str,
    ) -> models.InternalResultSnapshotRecord:
        """Create an immutable snapshot of an internal result before external comparison."""
        
        # Ensure we have the latest data
        evidence_refs = claim.supporting_evidence or []
        counterevidence_refs = claim.counterevidence or []
        # Get dependencies from dependency_records
        deps = db.query(models.DependencyRecord).filter(models.DependencyRecord.dependent_claim_id == claim.id).all()
        dependencies = [d.dependency_ref for d in deps]

        payload = {
            "claim_id": claim.id,
            "evidence_refs": sorted(evidence_refs),
            "counterevidence_refs": sorted(counterevidence_refs),
            "dependencies": sorted(dependencies),
            "corpus_identity": corpus_identity,
            "methodology_version": methodology_version,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        payload_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
        snapshot_hash = hashlib.sha256(payload_bytes).hexdigest()

        snapshot = models.InternalResultSnapshotRecord(
            id=f"snp_{uuid.uuid4().hex[:8]}",
            snapshot_id=f"snp_{snapshot_hash[:16]}",
            claim_id=claim.id,
            methodology_version=methodology_version,
            corpus_identity=corpus_identity,
            evidence_refs=evidence_refs,
            counterevidence_refs=counterevidence_refs,
            dependencies=dependencies,
            snapshot_hash=snapshot_hash,
            created_at=datetime.now(timezone.utc).replace(tzinfo=None)
        )
        
        db.add(snapshot)
        db.commit()
        db.refresh(snapshot)
        return snapshot
