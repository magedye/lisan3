"""Add governed Tanzil pre-activation provenance and corpus identity constraints.

Revision ID: c4d8b7e2a913
Revises: e8b3f6a1c204
Create Date: 2026-08-26 18:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "c4d8b7e2a913"
down_revision: str | None = "e8b3f6a1c204"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    connection = op.get_bind()
    incomplete = connection.execute(
        sa.text(
            "SELECT COUNT(*) FROM corpus_occurrences "
            "WHERE snapshot_id IS NULL OR verse_ref IS NULL OR text IS NULL"
        )
    ).scalar_one()
    if incomplete:
        raise RuntimeError(
            "Cannot add corpus occurrence identity constraints: "
            f"{incomplete} incomplete rows exist"
        )

    with op.batch_alter_table("corpus_snapshots") as batch_op:
        batch_op.add_column(sa.Column("artifact_reference", sa.String(), nullable=True))
        batch_op.add_column(
            sa.Column("artifact_size_bytes", sa.Integer(), nullable=True)
        )
        batch_op.add_column(sa.Column("artifact_format", sa.String(), nullable=True))
        batch_op.add_column(
            sa.Column("artifact_verified_at", sa.DateTime(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("artifact_verification_revision", sa.String(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("identity_index_reference", sa.String(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("identity_index_sha256", sa.String(), nullable=True)
        )
        batch_op.add_column(sa.Column("verse_count", sa.Integer(), nullable=True))
        batch_op.add_column(
            sa.Column("canon_001_reconciliation", sa.String(), nullable=True)
        )
        batch_op.create_unique_constraint(
            "uq_corpus_snapshot_artifact_identity",
            [
                "canonical_text_source",
                "canonical_text_version",
                "canonical_text_hash",
            ],
        )
        batch_op.create_check_constraint(
            "ck_corpus_snapshot_artifact_size_positive",
            "artifact_size_bytes IS NULL OR artifact_size_bytes > 0",
        )
        batch_op.create_check_constraint(
            "ck_corpus_snapshot_verse_count_positive",
            "verse_count IS NULL OR verse_count > 0",
        )

    with op.batch_alter_table("corpus_occurrences") as batch_op:
        batch_op.alter_column(
            "snapshot_id", existing_type=sa.String(), nullable=False
        )
        batch_op.alter_column("verse_ref", existing_type=sa.String(), nullable=False)
        batch_op.alter_column("text", existing_type=sa.String(), nullable=False)
        batch_op.create_foreign_key(
            "fk_corpus_occurrence_snapshot",
            "corpus_snapshots",
            ["snapshot_id"],
            ["id"],
        )
        batch_op.create_unique_constraint(
            "uq_corpus_occurrence_snapshot_verse",
            ["snapshot_id", "verse_ref"],
        )


def downgrade() -> None:
    with op.batch_alter_table("corpus_occurrences") as batch_op:
        batch_op.drop_constraint(
            "uq_corpus_occurrence_snapshot_verse", type_="unique"
        )
        batch_op.drop_constraint("fk_corpus_occurrence_snapshot", type_="foreignkey")
        batch_op.alter_column("text", existing_type=sa.String(), nullable=True)
        batch_op.alter_column("verse_ref", existing_type=sa.String(), nullable=True)
        batch_op.alter_column(
            "snapshot_id", existing_type=sa.String(), nullable=True
        )

    with op.batch_alter_table("corpus_snapshots") as batch_op:
        batch_op.drop_constraint(
            "ck_corpus_snapshot_verse_count_positive", type_="check"
        )
        batch_op.drop_constraint(
            "ck_corpus_snapshot_artifact_size_positive", type_="check"
        )
        batch_op.drop_constraint(
            "uq_corpus_snapshot_artifact_identity", type_="unique"
        )
        batch_op.drop_column("canon_001_reconciliation")
        batch_op.drop_column("verse_count")
        batch_op.drop_column("identity_index_sha256")
        batch_op.drop_column("identity_index_reference")
        batch_op.drop_column("artifact_verification_revision")
        batch_op.drop_column("artifact_verified_at")
        batch_op.drop_column("artifact_format")
        batch_op.drop_column("artifact_size_bytes")
        batch_op.drop_column("artifact_reference")
