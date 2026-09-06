"""Add hypothesis origin marker (internal derivation vs external candidate).

Enforces INT-EXT-001..007 (external hypothesis policy §9): a known-source
external candidate must declare itself and can never masquerade as blind internal
discovery. Additive only — one nullable-with-default column plus a value check.
No existing column, table, or behaviour is changed; rows default to
INDEPENDENT_INTERNAL_DERIVATION so nothing is silently relabelled.

Revision ID: a2f5c1d7b940
Revises: f1a6c3d9e204
Create Date: 2026-09-06 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "a2f5c1d7b940"
down_revision: str | None = "f1a6c3d9e204"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_DEFAULT_ORIGIN = "INDEPENDENT_INTERNAL_DERIVATION"


def upgrade() -> None:
    with op.batch_alter_table("hypotheses") as batch_op:
        batch_op.add_column(
            sa.Column(
                "origin",
                sa.String(),
                nullable=False,
                server_default=_DEFAULT_ORIGIN,
            )
        )
        batch_op.create_check_constraint(
            "ck_hypothesis_origin",
            "origin IN ('INDEPENDENT_INTERNAL_DERIVATION', 'EXTERNAL_CANDIDATE')",
        )


def downgrade() -> None:
    with op.batch_alter_table("hypotheses") as batch_op:
        batch_op.drop_constraint("ck_hypothesis_origin", type_="check")
        batch_op.drop_column("origin")
