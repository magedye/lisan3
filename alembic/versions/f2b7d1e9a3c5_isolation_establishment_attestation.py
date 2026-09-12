"""Fail-closed blind-isolation establishment/attestation columns.

Canonical Runtime Qualification — Track E. Historically an IsolationState row
defaulted straight to is_contaminated='CLEAN', so a run was treated as isolated
with zero enforcement (a preflight endpoint created the CLEAN row). This adds an
independent establishment axis that defaults to NOT_ESTABLISHED and records the
attestation (permitted/prohibited sources, input manifest, attesting actor,
timestamp, immutable audit link). CLEAN alone no longer satisfies canonicalization;
establishment_status must be ESTABLISHED.

Additive only: six new columns on isolation_states; no existing column or row
semantics changed. No historical isolation is backfilled to CLEAN/ESTABLISHED
(both runtime DBs had zero isolation rows).

Revision ID: f2b7d1e9a3c5
Revises: b3d6e2f8c150
Create Date: 2026-09-12 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "f2b7d1e9a3c5"
down_revision: str | None = "b3d6e2f8c150"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "isolation_states",
        sa.Column(
            "establishment_status",
            sa.String(),
            nullable=False,
            server_default="NOT_ESTABLISHED",
        ),
    )
    op.add_column(
        "isolation_states", sa.Column("prohibited_sources", sa.JSON(), nullable=True)
    )
    op.add_column(
        "isolation_states", sa.Column("input_manifest", sa.JSON(), nullable=True)
    )
    op.add_column(
        "isolation_states", sa.Column("attesting_actor", sa.String(), nullable=True)
    )
    op.add_column(
        "isolation_states", sa.Column("attested_at", sa.DateTime(), nullable=True)
    )
    op.add_column(
        "isolation_states", sa.Column("audit_ref", sa.String(), nullable=True)
    )


def downgrade() -> None:
    with op.batch_alter_table("isolation_states") as batch_op:
        batch_op.drop_column("audit_ref")
        batch_op.drop_column("attested_at")
        batch_op.drop_column("attesting_actor")
        batch_op.drop_column("input_manifest")
        batch_op.drop_column("prohibited_sources")
        batch_op.drop_column("establishment_status")
