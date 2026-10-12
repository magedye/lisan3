"""fix_essential_neighbors_counterevidence_nullability

Revision ID: c171ee65e007
Revises: 2d7d33a9d337
Create Date: 2026-09-29 15:49:31.960571

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'c171ee65e007'
down_revision: str | None = '2d7d33a9d337'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    bind.execute(sa.text("UPDATE essential_neighbors SET counterevidence = '[]' WHERE counterevidence IS NULL"))
    with op.batch_alter_table("essential_neighbors") as batch_op:
        batch_op.alter_column(
            "counterevidence",
            existing_type=sa.JSON(),
            nullable=False,
            server_default="[]"
        )


def downgrade() -> None:
    with op.batch_alter_table("essential_neighbors") as batch_op:
        batch_op.alter_column(
            "counterevidence",
            existing_type=sa.JSON(),
            nullable=True,
            server_default=None
        )
