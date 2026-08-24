"""Add model-agnostic R2 vector evaluation infrastructure.

Revision ID: c9e2a7f4b6d1
Revises: b7e4c1d9a5f2
Create Date: 2026-08-24 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "c9e2a7f4b6d1"
down_revision: str | None = "b7e4c1d9a5f2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "semantic_embeddings",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("research_run_id", sa.String(), nullable=False),
        sa.Column("entity_type", sa.String(), nullable=False),
        sa.Column("entity_id", sa.String(), nullable=False),
        sa.Column("embedding_space", sa.String(), nullable=False),
        sa.Column("embedding_model", sa.String(), nullable=False),
        sa.Column("embedding_model_revision", sa.String(), nullable=False),
        sa.Column("model_config_hash", sa.String(), nullable=False),
        sa.Column("source_revision", sa.String(), nullable=False),
        sa.Column("source_hash", sa.String(), nullable=False),
        sa.Column("vector", sa.LargeBinary(), nullable=False),
        sa.Column("dimensions", sa.Integer(), nullable=False),
        sa.Column("provenance_class", sa.String(), nullable=False),
        sa.Column(
            "production_eligible",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column(
            "source_eligible", sa.Boolean(), nullable=False, server_default=sa.true()
        ),
        sa.Column("index_revision", sa.String(), nullable=False),
        sa.Column(
            "lifecycle_state", sa.String(), nullable=False, server_default="CURRENT"
        ),
        sa.Column("invalidated_reason", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "embedding_space IN ('VERSE_CONTEXT', 'STRUCTURAL_PROFILE', "
            "'HYPOTHESIS', 'CLAIM', 'ROOT_CANDIDATE', 'EXTERNAL_RESEARCH')",
            name="ck_semantic_embedding_space",
        ),
        sa.CheckConstraint(
            "provenance_class IN ('BENCHMARK_ONLY', 'SYNTHETIC_EVALUATION')",
            name="ck_semantic_embedding_provenance",
        ),
        sa.CheckConstraint(
            "production_eligible = 0",
            name="ck_semantic_embedding_evaluation_only",
        ),
        sa.CheckConstraint("dimensions > 0", name="ck_semantic_embedding_dimensions"),
        sa.CheckConstraint(
            "lifecycle_state IN ('CURRENT', 'STALE')",
            name="ck_semantic_embedding_lifecycle",
        ),
        sa.CheckConstraint(
            "(lifecycle_state = 'CURRENT' AND source_eligible = 1 "
            "AND invalidated_reason IS NULL) OR "
            "(lifecycle_state = 'STALE' AND invalidated_reason IS NOT NULL)",
            name="ck_semantic_embedding_current_eligibility",
        ),
        sa.ForeignKeyConstraint(["research_run_id"], ["research_runs.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "research_run_id",
            "entity_type",
            "entity_id",
            "embedding_space",
            "embedding_model",
            "embedding_model_revision",
            "model_config_hash",
            "source_revision",
            name="uq_semantic_embedding_identity",
        ),
    )
    op.create_index(
        "ix_semantic_embeddings_current_scope",
        "semantic_embeddings",
        [
            "research_run_id",
            "embedding_space",
            "lifecycle_state",
            "model_config_hash",
        ],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_semantic_embeddings_current_scope", table_name="semantic_embeddings"
    )
    op.drop_table("semantic_embeddings")
