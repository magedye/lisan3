"""Pre-analysis foundation stores: structural tokens, external hypothesis
register, campaign state.

Owner Request 01: persist the reusable descriptive knowledge base (INT-PRE-OWN-001),
the unified external-hypothesis register (INT-EXT-001..007), and durable campaign
checkpoint/resume state. Additive only — three new tables; no existing table,
column, or behaviour is changed.

Revision ID: b3d6e2f8c150
Revises: a2f5c1d7b940
Create Date: 2026-09-06 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "b3d6e2f8c150"
down_revision: str | None = "a2f5c1d7b940"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "structural_tokens",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("snapshot_id", sa.String(), nullable=False),
        sa.Column("word_ref", sa.String(), nullable=False),
        sa.Column("verse_ref", sa.String(), nullable=False),
        sa.Column("root", sa.String(), nullable=False),
        sa.Column("form", sa.String(), nullable=True),
        sa.Column("pos_tag", sa.String(), nullable=True),
        sa.Column("source_id", sa.String(), nullable=False),
        sa.Column("source_version", sa.String(), nullable=True),
        sa.Column("extraction_version", sa.String(), nullable=False),
        sa.Column(
            "attribution_status",
            sa.String(),
            nullable=False,
            server_default="CONFIRMED",
        ),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["snapshot_id"], ["corpus_snapshots.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint(
            "attribution_status IN ('CONFIRMED', 'DISPUTED', 'UNRESOLVED')",
            name="ck_structural_token_attribution_status",
        ),
        sa.UniqueConstraint(
            "snapshot_id",
            "word_ref",
            "extraction_version",
            name="uq_structural_token_identity",
        ),
    )
    op.create_index(
        "ix_structural_tokens_root", "structural_tokens", ["snapshot_id", "root"]
    )
    op.create_index(
        op.f("ix_structural_tokens_snapshot_id"),
        "structural_tokens",
        ["snapshot_id"],
    )

    op.create_table(
        "external_hypothesis_records",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("claim_type", sa.String(), nullable=False),
        sa.Column("source", sa.String(), nullable=False),
        sa.Column("author", sa.String(), nullable=False),
        sa.Column("source_locator", sa.String(), nullable=True),
        sa.Column("claim", sa.String(), nullable=False),
        sa.Column("normalized_claim", sa.String(), nullable=True),
        sa.Column("target_scope", sa.String(), nullable=False),
        sa.Column(
            "claim_role", sa.String(), nullable=False, server_default="RULE_CLAIM"
        ),
        sa.Column(
            "status", sa.String(), nullable=False, server_default="EXTERNAL_CANDIDATE"
        ),
        sa.Column("test_plan", sa.String(), nullable=True),
        sa.Column("test_evidence_refs", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("counterevidence_refs", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("result", sa.String(), nullable=True),
        sa.Column("provenance", sa.String(), nullable=False),
        sa.Column("research_run_id", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["research_run_id"], ["research_runs.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint(
            "claim_type IN ('ROOT_MEANING_CANDIDATE', 'FORM_EFFECT_CANDIDATE', "
            "'DERIVATIONAL_EFFECT_CANDIDATE', 'LETTER_EFFECT_CANDIDATE', "
            "'CONSTRUCTION_EFFECT_CANDIDATE', 'METHOD_RULE_CANDIDATE')",
            name="ck_external_hypothesis_claim_type",
        ),
        sa.CheckConstraint(
            "claim_role IN ('RULE_CLAIM', 'AUTHOR_APPLICATION')",
            name="ck_external_hypothesis_claim_role",
        ),
        sa.CheckConstraint(
            "status IN ('EXTERNAL_CANDIDATE', 'TESTED', 'SUPPORTED', "
            "'PARTIALLY_SUPPORTED', 'NOT_SUPPORTED', 'FALSIFIED', 'UNRESOLVED')",
            name="ck_external_hypothesis_status",
        ),
    )
    op.create_index(op.f("ix_external_hypothesis_records_id"), "external_hypothesis_records", ["id"])
    op.create_index(
        "ix_external_hypothesis_target",
        "external_hypothesis_records",
        ["claim_type", "target_scope"],
    )

    op.create_table(
        "campaign_states",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("campaign_id", sa.String(), nullable=False),
        sa.Column("methodology_revision", sa.String(), nullable=True),
        sa.Column("corpus_snapshot", sa.String(), nullable=True),
        sa.Column("queue", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("completed_roots", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("current_batch", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("findings", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("status", sa.String(), nullable=False, server_default="INITIALIZED"),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("campaign_id", name="uq_campaign_state_campaign_id"),
    )
    op.create_index(op.f("ix_campaign_states_id"), "campaign_states", ["id"])


def downgrade() -> None:
    op.drop_index(op.f("ix_campaign_states_id"), table_name="campaign_states")
    op.drop_table("campaign_states")
    op.drop_index("ix_external_hypothesis_target", table_name="external_hypothesis_records")
    op.drop_index(op.f("ix_external_hypothesis_records_id"), table_name="external_hypothesis_records")
    op.drop_table("external_hypothesis_records")
    op.drop_index(op.f("ix_structural_tokens_snapshot_id"), table_name="structural_tokens")
    op.drop_index("ix_structural_tokens_root", table_name="structural_tokens")
    op.drop_table("structural_tokens")
