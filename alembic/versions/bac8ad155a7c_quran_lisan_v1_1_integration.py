"""Quran Lisan v1.1 integration

Revision ID: bac8ad155a7c
Revises: 50ccdbbf2a2e
Create Date: 2026-09-19 17:29:49.222373

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "bac8ad155a7c"
down_revision: str | None = "50ccdbbf2a2e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # 1. Create semantic_memory with full A15/C04 specification
    op.create_table(
        "semantic_memory",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("claim_id", sa.String(), nullable=False),
        sa.Column("target_type", sa.String(), nullable=False),
        sa.Column("target_expression", sa.String(), nullable=False),
        sa.Column(
            "reliability", sa.String(), nullable=False, server_default="PROVISIONAL"
        ),
        sa.Column("scope", sa.String(), nullable=False),
        sa.Column(
            "conflict_state", sa.String(), nullable=False, server_default="NO_CONFLICT"
        ),
        sa.Column("lifecycle", sa.String(), nullable=False, server_default="ACTIVE"),
        sa.Column(
            "result_strength", sa.String(), nullable=False, server_default="UNRESOLVED"
        ),
        sa.Column(
            "research_completeness",
            sa.String(),
            nullable=False,
            server_default="PARTIAL",
        ),
        sa.Column(
            "independent_verification",
            sa.String(),
            nullable=False,
            server_default="UNVERIFIED",
        ),
        sa.Column("evidence_refs", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column(
            "counterevidence_refs", sa.JSON(), nullable=False, server_default="[]"
        ),
        sa.Column("dependencies", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("reopen_if", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("parent_revision", sa.String(), nullable=True),
        sa.Column("revision_reason", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.CheckConstraint(
            "reliability IN ('TRUSTED', 'PROVISIONAL', 'DISPUTED', 'RETIRED')",
            name="ck_semantic_memory_reliability",
        ),
        sa.CheckConstraint(
            "scope IN ('UNIVERSAL', 'REPRESENTATIVE', 'LOCAL')",
            name="ck_semantic_memory_scope",
        ),
        sa.CheckConstraint(
            "target_type IN ('ROOT', 'LEXEME', 'FORM', 'CONSTRUCTION', 'LOCAL_MEANING', 'VERSE', 'CONCEPT', 'COMPARISON', 'PRACTICE')",
            name="ck_semantic_memory_target_type",
        ),
        sa.CheckConstraint(
            "lifecycle IN ('ACTIVE', 'REOPENED', 'SUPERSEDED', 'REJECTED')",
            name="ck_semantic_memory_lifecycle",
        ),
        sa.CheckConstraint(
            "conflict_state IN ('NO_CONFLICT', 'OPEN_CONFLICT', 'RESOLVED_CONFLICT')",
            name="ck_semantic_memory_conflict_state",
        ),
        sa.ForeignKeyConstraint(
            ["claim_id"],
            ["semantic_claims.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("semantic_memory", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_semantic_memory_id"), ["id"], unique=False)

    # 2. Add v1.1 canonical columns to essential_neighbors while preserving legacy columns
    with op.batch_alter_table("essential_neighbors", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("shared_features", sa.JSON(), nullable=False, server_default="[]")
        )
        batch_op.add_column(
            sa.Column("distinctive_difference", sa.String(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("layer_of_difference", sa.String(), nullable=True)
        )
        batch_op.add_column(
            sa.Column(
                "discriminating_evidence",
                sa.JSON(),
                nullable=False,
                server_default="[]",
            )
        )
        batch_op.add_column(sa.Column("status", sa.String(), nullable=True))

    # Migrate existing data forward without information loss
    op.execute("""
        UPDATE essential_neighbors
        SET distinctive_difference = positive_distinguishing_candidate
        WHERE distinctive_difference IS NULL AND positive_distinguishing_candidate IS NOT NULL
    """)
    op.execute("""
        UPDATE essential_neighbors
        SET discriminating_evidence = supporting_evidence
        WHERE discriminating_evidence = '[]' AND supporting_evidence IS NOT NULL
    """)
    op.execute("""
        UPDATE essential_neighbors
        SET status = 'UNRESOLVED'
        WHERE status IS NULL AND unresolved_distinction IS NOT NULL
    """)

    # 3. Add distinctive_residue, illustrative_verses, decisive_contexts to semantic_claims
    with op.batch_alter_table("semantic_claims", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("distinctive_residue", sa.String(), nullable=True)
        )
        batch_op.add_column(
            sa.Column(
                "illustrative_verses", sa.JSON(), nullable=False, server_default="[]"
            )
        )
        batch_op.add_column(
            sa.Column(
                "decisive_contexts", sa.JSON(), nullable=False, server_default="[]"
            )
        )
        batch_op.alter_column(
            "semantic_boundary",
            existing_type=sa.VARCHAR(),
            type_=sa.JSON(),
            nullable=False,
            server_default="{}",
        )


def downgrade() -> None:
    with op.batch_alter_table("semantic_claims", schema=None) as batch_op:
        batch_op.alter_column(
            "semantic_boundary",
            existing_type=sa.JSON(),
            type_=sa.VARCHAR(),
            nullable=True,
        )
        batch_op.drop_column("decisive_contexts")
        batch_op.drop_column("illustrative_verses")
        batch_op.drop_column("distinctive_residue")

    with op.batch_alter_table("essential_neighbors", schema=None) as batch_op:
        batch_op.drop_column("status")
        batch_op.drop_column("discriminating_evidence")
        batch_op.drop_column("layer_of_difference")
        batch_op.drop_column("distinctive_difference")
        batch_op.drop_column("shared_features")

    with op.batch_alter_table("semantic_memory", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_semantic_memory_id"))

    op.drop_table("semantic_memory")
