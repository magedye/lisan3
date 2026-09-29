"""Add revalidation_state

Revision ID: 2d7d33a9d337
Revises: 81f038292b62
Create Date: 2026-09-27 22:07:01.261999

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '2d7d33a9d337'
down_revision: str | None = '81f038292b62'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table('semantic_memory', schema=None) as batch_op:
        batch_op.add_column(sa.Column('revalidation_state', sa.String(), nullable=False, server_default="CURRENT"))


def downgrade() -> None:
    with op.batch_alter_table('semantic_memory', schema=None) as batch_op:
        batch_op.drop_column('revalidation_state')
