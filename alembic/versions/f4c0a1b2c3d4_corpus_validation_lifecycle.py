"""Add explicit Corpus validation lifecycle fields.

Revision ID: f4c0a1b2c3d4
Revises: 80330541af56
Create Date: 2026-08-23 23:40:00
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "f4c0a1b2c3d4"
down_revision: str | None = "80330541af56"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("quality_profiles") as batch_op:
        batch_op.add_column(sa.Column("purity_rating", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("purity_findings", sa.JSON(), nullable=True))

    with op.batch_alter_table("corpus_snapshots") as batch_op:
        batch_op.add_column(
            sa.Column(
                "source_role_status",
                sa.String(),
                nullable=False,
                server_default="SOURCE_ROLE_PENDING",
            )
        )
        batch_op.add_column(
            sa.Column(
                "artifact_presence_status",
                sa.String(),
                nullable=False,
                server_default="ARTIFACT_MISSING",
            )
        )
        batch_op.add_column(
            sa.Column("expected_canonical_text_hash", sa.String(), nullable=True)
        )
        batch_op.add_column(
            sa.Column(
                "hash_verification_status",
                sa.String(),
                nullable=False,
                server_default="HASH_UNVERIFIED",
            )
        )
        batch_op.add_column(
            sa.Column(
                "import_validation_status",
                sa.String(),
                nullable=False,
                server_default="IMPORT_PENDING",
            )
        )
        batch_op.add_column(
            sa.Column(
                "activation_status",
                sa.String(),
                nullable=False,
                server_default="CANONICAL_ACTIVATION_PENDING",
            )
        )
        batch_op.add_column(
            sa.Column("artifact_provenance", sa.String(), nullable=True)
        )
        batch_op.add_column(
            sa.Column(
                "fixture_only", sa.Boolean(), nullable=False, server_default=sa.true()
            )
        )


def downgrade() -> None:
    with op.batch_alter_table("corpus_snapshots") as batch_op:
        batch_op.drop_column("fixture_only")
        batch_op.drop_column("artifact_provenance")
        batch_op.drop_column("activation_status")
        batch_op.drop_column("import_validation_status")
        batch_op.drop_column("hash_verification_status")
        batch_op.drop_column("expected_canonical_text_hash")
        batch_op.drop_column("artifact_presence_status")
        batch_op.drop_column("source_role_status")

    with op.batch_alter_table("quality_profiles") as batch_op:
        batch_op.drop_column("purity_findings")
        batch_op.drop_column("purity_rating")
