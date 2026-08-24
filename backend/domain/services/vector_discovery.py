import hashlib
import json
import sqlite3
from collections.abc import Sequence
from typing import Any

import sqlite_vec
from sqlalchemy import delete, select, text
from sqlalchemy.orm import Session

from backend.domain import models
from backend.domain.services.gates import INTERNAL_LOCK, has_valid_gate
from backend.domain.vector_contracts import (
    CandidateType,
    EmbeddingModelManifest,
    EmbeddingSpace,
    EvaluationVectorInput,
    RetrievalCandidate,
)


class VectorAccessForbidden(Exception):
    pass


class VectorProductionBoundaryError(Exception):
    pass


class VectorStateStale(Exception):
    pass


def _require_evaluation_manifest(
    manifest: EmbeddingModelManifest, space: EmbeddingSpace
) -> None:
    if manifest.governance_decision_ref:
        raise VectorProductionBoundaryError(
            "Governed production manifests cannot populate evaluation vector state"
        )
    if space not in manifest.allowed_spaces:
        raise VectorAccessForbidden(
            f"Embedding manifest does not authorize {space.value}"
        )


def _require_run_access(db: Session, run_id: str) -> models.ResearchRun:
    run = db.get(models.ResearchRun, run_id)
    if run is None:
        raise LookupError(f"ResearchRun {run_id} not found")
    isolation = (
        db.query(models.IsolationState)
        .filter(models.IsolationState.research_run_id == run_id)
        .one_or_none()
    )
    if isolation is None or str(isolation.is_contaminated) != "CLEAN":
        raise VectorAccessForbidden(
            "Vector access blocked: Blind Lab isolation is absent or contaminated"
        )
    if not has_valid_gate(db, run_id, INTERNAL_LOCK):
        raise VectorAccessForbidden(
            "Vector access blocked before Internal Lock; this is not contamination"
        )
    return run


def _serialize(vector: Sequence[float], dimensions: int) -> bytes:
    if len(vector) != dimensions:
        raise ValueError(
            f"Expected {dimensions} float32 values, received {len(vector)}"
        )
    return bytes(sqlite_vec.serialize_float32(list(vector)))


def _index_revision(
    run_id: str,
    space: EmbeddingSpace,
    manifest: EmbeddingModelManifest,
    vectors: Sequence[EvaluationVectorInput],
) -> str:
    inputs = []
    for item in sorted(vectors, key=lambda candidate: candidate.embedding_id):
        inputs.append(
            {
                "embedding_id": item.embedding_id,
                "entity_id": item.entity_id,
                "entity_type": item.entity_type,
                "provenance_class": item.provenance_class.value,
                "source_hash": item.source_hash,
                "source_revision": item.source_revision,
                "vector_float32": _serialize(item.vector, manifest.dimensions).hex(),
            }
        )
    payload = {
        "config_hash": manifest.config_hash,
        "inputs": inputs,
        "research_run_id": run_id,
        "space": space.value,
    }
    encoded = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()


def _record_id(run_id: str, space: EmbeddingSpace, embedding_id: str) -> str:
    identity = f"{run_id}\x1f{space.value}\x1f{embedding_id}".encode()
    return f"r2eval::{hashlib.sha256(identity).hexdigest()}"


def _load_sqlite_vec(db: Session) -> str:
    raw: Any = db.connection().connection.driver_connection
    try:
        return str(raw.execute("select vec_version()").fetchone()[0])
    except sqlite3.OperationalError:
        raw.enable_load_extension(True)
        try:
            sqlite_vec.load(raw)
        finally:
            raw.enable_load_extension(False)
        return str(raw.execute("select vec_version()").fetchone()[0])


class VectorDiscoveryService:
    @staticmethod
    def rebuild_evaluation(
        db: Session,
        *,
        run_id: str,
        space: EmbeddingSpace,
        manifest: EmbeddingModelManifest,
        vectors: Sequence[EvaluationVectorInput],
    ) -> str:
        _require_evaluation_manifest(manifest, space)
        _require_run_access(db, run_id)
        if any(not item.source_eligible for item in vectors):
            raise VectorAccessForbidden(
                "Ineligible sources cannot populate evaluation vector state"
            )
        revision = _index_revision(run_id, space, manifest, vectors)
        records = [
            models.SemanticEmbedding(
                id=_record_id(run_id, space, item.embedding_id),
                research_run_id=run_id,
                entity_type=item.entity_type,
                entity_id=item.entity_id,
                embedding_space=space.value,
                embedding_model=manifest.model_id,
                embedding_model_revision=manifest.revision,
                model_config_hash=manifest.config_hash,
                source_revision=item.source_revision,
                source_hash=item.source_hash,
                vector=_serialize(item.vector, manifest.dimensions),
                dimensions=manifest.dimensions,
                provenance_class=item.provenance_class.value,
                production_eligible=False,
                source_eligible=True,
                index_revision=revision,
                lifecycle_state="CURRENT",
            )
            for item in sorted(vectors, key=lambda candidate: candidate.embedding_id)
        ]
        db.execute(
            delete(models.SemanticEmbedding).where(
                models.SemanticEmbedding.research_run_id == run_id,
                models.SemanticEmbedding.embedding_space == space.value,
            )
        )
        db.add_all(records)
        db.commit()
        return revision

    @staticmethod
    def invalidate_mismatched(
        db: Session,
        *,
        run_id: str,
        space: EmbeddingSpace,
        manifest: EmbeddingModelManifest,
    ) -> int:
        _require_evaluation_manifest(manifest, space)
        records = db.scalars(
            select(models.SemanticEmbedding).where(
                models.SemanticEmbedding.research_run_id == run_id,
                models.SemanticEmbedding.embedding_space == space.value,
                models.SemanticEmbedding.lifecycle_state == "CURRENT",
            )
        ).all()
        changed = 0
        for record in records:
            reason = None
            if (
                str(record.embedding_model) != manifest.model_id
                or str(record.embedding_model_revision) != manifest.revision
            ):
                reason = "MODEL_REVISION_CHANGED"
            elif str(record.model_config_hash) != manifest.config_hash:
                reason = "MODEL_CONFIG_CHANGED"
            if reason:
                record_for_update: Any = record
                record_for_update.lifecycle_state = "STALE"
                record_for_update.invalidated_reason = reason
                changed += 1
        db.commit()
        return changed

    @staticmethod
    def delete_derived_state(
        db: Session, *, run_id: str, space: EmbeddingSpace | None = None
    ) -> int:
        statement = delete(models.SemanticEmbedding).where(
            models.SemanticEmbedding.research_run_id == run_id
        )
        if space is not None:
            statement = statement.where(
                models.SemanticEmbedding.embedding_space == space.value
            )
        result = db.execute(statement)
        db.commit()
        return int(result.rowcount or 0)

    @staticmethod
    def discover(
        db: Session,
        *,
        run_id: str,
        space: EmbeddingSpace,
        manifest: EmbeddingModelManifest,
        query_vector: Sequence[float],
        candidate_type: CandidateType,
        top_k: int,
    ) -> list[RetrievalCandidate]:
        _require_evaluation_manifest(manifest, space)
        _require_run_access(db, run_id)
        if top_k < 1 or top_k > 100:
            raise ValueError("top_k must be between 1 and 100")

        mismatched_current = db.scalar(
            select(models.SemanticEmbedding.id)
            .where(
                models.SemanticEmbedding.research_run_id == run_id,
                models.SemanticEmbedding.embedding_space == space.value,
                models.SemanticEmbedding.lifecycle_state == "CURRENT",
                (
                    (models.SemanticEmbedding.embedding_model != manifest.model_id)
                    | (
                        models.SemanticEmbedding.embedding_model_revision
                        != manifest.revision
                    )
                    | (
                        models.SemanticEmbedding.model_config_hash
                        != manifest.config_hash
                    )
                ),
            )
            .limit(1)
        )
        if mismatched_current is not None:
            raise VectorStateStale(
                "Current vector state does not match the requested model manifest"
            )

        _load_sqlite_vec(db)
        rows = db.execute(
            text(
                """
                SELECT id, entity_type, entity_id, source_revision, source_hash,
                       embedding_model, embedding_model_revision,
                       model_config_hash, index_revision, provenance_class,
                       vec_distance_cosine(vector, :query_vector) AS distance
                FROM semantic_embeddings
                WHERE research_run_id = :run_id
                  AND embedding_space = :embedding_space
                  AND embedding_model = :embedding_model
                  AND embedding_model_revision = :embedding_model_revision
                  AND model_config_hash = :model_config_hash
                  AND lifecycle_state = 'CURRENT'
                  AND source_eligible = 1
                  AND production_eligible = 0
                ORDER BY distance ASC, id ASC
                LIMIT :top_k
                """
            ),
            {
                "query_vector": _serialize(query_vector, manifest.dimensions),
                "run_id": run_id,
                "embedding_space": space.value,
                "embedding_model": manifest.model_id,
                "embedding_model_revision": manifest.revision,
                "model_config_hash": manifest.config_hash,
                "top_k": top_k,
            },
        ).mappings()
        return [
            RetrievalCandidate(
                candidate_id=f"candidate::{row['id']}",
                candidate_type=candidate_type,
                entity_ref=f"{row['entity_type']}:{row['entity_id']}",
                source_revision=row["source_revision"],
                embedding_space=space,
                embedding_model=row["embedding_model"],
                embedding_model_revision=row["embedding_model_revision"],
                distance=float(row["distance"]),
                similarity_score=max(-1.0, min(1.0, 1.0 - float(row["distance"]))),
                retrieval_reason="sqlite-vec synthetic evaluation candidate",
                provenance={
                    "class": row["provenance_class"],
                    "index_revision": row["index_revision"],
                    "model_config_hash": row["model_config_hash"],
                    "research_run_id": run_id,
                    "source_hash": row["source_hash"],
                },
            )
            for row in rows
        ]
