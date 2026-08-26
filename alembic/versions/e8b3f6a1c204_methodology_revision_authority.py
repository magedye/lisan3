"""Add durable, source-bound Methodology revision authority.

Revision ID: e8b3f6a1c204
Revises: d4f7a2c8e901
Create Date: 2026-08-26 12:00:00.000000
"""

from collections.abc import Sequence
from datetime import datetime, timezone

import sqlalchemy as sa

from alembic import op

revision: str = "e8b3f6a1c204"
down_revision: str | None = "d4f7a2c8e901"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

METHODOLOGY_REVISION_ID = (
    "LISAN_QURANIC_SEMANTIC_EXTRACTION@6bb1c10a0f9a"
)
SOURCE_SHA256 = "43c0a40b3f465fa95695607c2de838effd07946966c57ad15275d0051e92a288"


def upgrade() -> None:
    table = op.create_table(
        "methodology_revisions",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("methodology_id", sa.String(), nullable=False),
        sa.Column("revision", sa.String(), nullable=False),
        sa.Column("lifecycle_state", sa.String(), nullable=False),
        sa.Column("authority_reference", sa.String(), nullable=False),
        sa.Column("source_reference", sa.String(), nullable=False),
        sa.Column("source_sha256", sa.String(), nullable=False),
        sa.Column("allowed_use", sa.String(), nullable=False),
        sa.Column("research_run_eligible", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "lifecycle_state IN ('CURRENT', 'RETIRED')",
            name="ck_methodology_revision_lifecycle",
        ),
        sa.CheckConstraint(
            "length(source_sha256) = 64",
            name="ck_methodology_revision_source_sha256",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "methodology_id",
            "revision",
            name="uq_methodology_revision_identity",
        ),
    )
    op.create_index(
        "ix_methodology_revisions_methodology_id",
        "methodology_revisions",
        ["methodology_id"],
        unique=False,
    )
    op.bulk_insert(
        table,
        [
            {
                "id": METHODOLOGY_REVISION_ID,
                "methodology_id": "LISAN_QURANIC_SEMANTIC_EXTRACTION",
                "revision": "git-blob:6bb1c10a0f9a09bf9a59c29c45e2252efc9832fb",
                "lifecycle_state": "CURRENT",
                "authority_reference": (
                    "docs/canonical/"
                    "LISAN_PLATFORM_CANONICAL_IMPLEMENTATION_REFERENCE.md"
                    "#methodology-revision-authority"
                ),
                "source_reference": "skills/lisan-semantic-extraction/SKILL.md",
                "source_sha256": SOURCE_SHA256,
                "allowed_use": "QURAN_INTERNAL_CUMULATIVE_RUN",
                "research_run_eligible": True,
                "created_at": datetime(2026, 8, 26, 12, 0, 0, tzinfo=timezone.utc),
            }
        ],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_methodology_revisions_methodology_id",
        table_name="methodology_revisions",
    )
    op.drop_table("methodology_revisions")
