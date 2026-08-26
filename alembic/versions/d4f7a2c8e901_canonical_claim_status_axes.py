"""Enforce and reconcile the four canonical SemanticClaim status axes.

Revision ID: d4f7a2c8e901
Revises: c9e2a7f4b6d1
Create Date: 2026-08-26 00:00:00.000000
"""

import hashlib
import json
from collections.abc import Sequence
from datetime import datetime, timezone

import sqlalchemy as sa

from alembic import op

revision: str = "d4f7a2c8e901"
down_revision: str | None = "c9e2a7f4b6d1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

CANONICAL = {
    "epistemic_state": {
        "OBSERVATION",
        "HYPOTHESIS",
        "TESTED",
        "SUPPORTED",
        "LOCK_BLOCKED",
        "LOCK_INTERNAL_RESULT",
        "REJECTED",
        "UNRESOLVED",
    },
    "review_state": {
        "NOT_REVIEWED",
        "REVIEW_REQUIRED",
        "IN_REVIEW",
        "APPROVED",
        "REJECTED",
        "OWNER_DECISION_REQUIRED",
    },
    "freshness_state": {
        "CURRENT",
        "STALE",
        "INVALIDATED",
        "REVALIDATION_REQUIRED",
    },
    "publication_state": {
        "PRIVATE_WORKING",
        "REVIEWABLE",
        "PUBLISHABLE",
        "PUBLISHED",
        "WITHDRAWN",
    },
}
DEFAULTS = {
    "epistemic_state": "UNRESOLVED",
    "review_state": "NOT_REVIEWED",
    "freshness_state": "CURRENT",
    "publication_state": "PRIVATE_WORKING",
}
LEGACY_MAP = {
    "review_state": {"PENDING_REVIEW": "REVIEW_REQUIRED"},
    "publication_state": {
        "UNPUBLISHED": "PRIVATE_WORKING",
        "BLOCKED": "PRIVATE_WORKING",
    },
}


def _reconciled(axis: str, value: str | None) -> str:
    if value in CANONICAL[axis]:
        return str(value)
    if value is None:
        return DEFAULTS[axis]
    mapped = LEGACY_MAP.get(axis, {}).get(value)
    if mapped is not None:
        return mapped
    raise RuntimeError(
        f"Cannot reconcile noncanonical {axis} value {value!r} without inventing meaning"
    )


def upgrade() -> None:
    bind = op.get_bind()
    rows = bind.execute(
        sa.text(
            "SELECT id, epistemic_state, review_state, freshness_state, "
            "publication_state FROM semantic_claims"
        )
    ).mappings()
    for row in rows:
        before = {axis: row[axis] for axis in CANONICAL}
        after = {axis: _reconciled(axis, before[axis]) for axis in CANONICAL}
        if before == after:
            continue
        bind.execute(
            sa.text(
                "UPDATE semantic_claims SET epistemic_state=:epistemic_state, "
                "review_state=:review_state, freshness_state=:freshness_state, "
                "publication_state=:publication_state WHERE id=:id"
            ),
            {"id": row["id"], **after},
        )
        digest = hashlib.sha256(
            f"{row['id']}|{json.dumps(before, sort_keys=True)}".encode()
        ).hexdigest()[:20]
        bind.execute(
            sa.text(
                "INSERT INTO audit_logs "
                "(id, entity_id, entity_type, action, previous_state, new_state, "
                "actor, created_at) VALUES (:id, :entity_id, 'SemanticClaim', "
                "'RECONCILE_CANONICAL_STATUS_AXES', :previous_state, :new_state, "
                "'ALEMBIC_D4F7A2C8E901', :created_at)"
            ),
            {
                "id": f"aud_axis_{digest}",
                "entity_id": row["id"],
                "previous_state": json.dumps(before, sort_keys=True),
                "new_state": json.dumps(after, sort_keys=True),
                "created_at": datetime.now(timezone.utc).replace(tzinfo=None),
            },
        )

    with op.batch_alter_table("semantic_claims") as batch_op:
        for axis in CANONICAL:
            batch_op.alter_column(axis, existing_type=sa.String(), nullable=False)
        batch_op.create_check_constraint(
            "ck_semantic_claim_epistemic_state",
            "epistemic_state IN ('OBSERVATION', 'HYPOTHESIS', 'TESTED', "
            "'SUPPORTED', 'LOCK_BLOCKED', 'LOCK_INTERNAL_RESULT', 'REJECTED', "
            "'UNRESOLVED')",
        )
        batch_op.create_check_constraint(
            "ck_semantic_claim_review_state",
            "review_state IN ('NOT_REVIEWED', 'REVIEW_REQUIRED', 'IN_REVIEW', "
            "'APPROVED', 'REJECTED', 'OWNER_DECISION_REQUIRED')",
        )
        batch_op.create_check_constraint(
            "ck_semantic_claim_freshness_state",
            "freshness_state IN ('CURRENT', 'STALE', 'INVALIDATED', "
            "'REVALIDATION_REQUIRED')",
        )
        batch_op.create_check_constraint(
            "ck_semantic_claim_publication_state",
            "publication_state IN ('PRIVATE_WORKING', 'REVIEWABLE', 'PUBLISHABLE', "
            "'PUBLISHED', 'WITHDRAWN')",
        )


def downgrade() -> None:
    bind = op.get_bind()
    with op.batch_alter_table("semantic_claims") as batch_op:
        batch_op.drop_constraint(
            "ck_semantic_claim_publication_state", type_="check"
        )
        batch_op.drop_constraint("ck_semantic_claim_freshness_state", type_="check")
        batch_op.drop_constraint("ck_semantic_claim_review_state", type_="check")
        batch_op.drop_constraint("ck_semantic_claim_epistemic_state", type_="check")
        for axis in CANONICAL:
            batch_op.alter_column(axis, existing_type=sa.String(), nullable=True)

    audits = bind.execute(
        sa.text(
            "SELECT id, entity_id, previous_state, new_state FROM audit_logs "
            "WHERE action='RECONCILE_CANONICAL_STATUS_AXES' "
            "AND actor='ALEMBIC_D4F7A2C8E901'"
        )
    ).mappings()
    for audit in audits:
        before = json.loads(audit["previous_state"])
        after = json.loads(audit["new_state"])
        current = bind.execute(
            sa.text(
                "SELECT epistemic_state, review_state, freshness_state, "
                "publication_state FROM semantic_claims WHERE id=:id"
            ),
            {"id": audit["entity_id"]},
        ).mappings().first()
        if current is not None and dict(current) == after:
            bind.execute(
                sa.text(
                    "UPDATE semantic_claims SET epistemic_state=:epistemic_state, "
                    "review_state=:review_state, freshness_state=:freshness_state, "
                    "publication_state=:publication_state WHERE id=:id"
                ),
                {"id": audit["entity_id"], **before},
            )
        bind.execute(sa.text("DELETE FROM audit_logs WHERE id=:id"), {"id": audit["id"]})
