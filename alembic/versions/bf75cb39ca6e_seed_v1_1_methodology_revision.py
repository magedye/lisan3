"""seed_v1_1_methodology_revision

Revision ID: bf75cb39ca6e
Revises: c171ee65e007
Create Date: 2026-09-29 15:59:51.601640

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'bf75cb39ca6e'
down_revision: str | None = 'c171ee65e007'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


from datetime import datetime, timezone

METHODOLOGY_ID = "LISAN_QURANIC_SEMANTIC_EXTRACTION"
NEW_REVISION_ID = "LISAN_QURANIC_SEMANTIC_EXTRACTION@b30ee619d8b8"
NEW_SOURCE_SHA256 = "b30ee619d8b8a97e2d9718023ca40ba7cab1a228a91c6e25748bf1c079943dd1"

def upgrade() -> None:
    bind = op.get_bind()
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    bind.execute(
        sa.text(
            "UPDATE methodology_revisions SET lifecycle_state='RETIRED', "
            "research_run_eligible=0 WHERE methodology_id=:methodology_id "
            "AND lifecycle_state='CURRENT'"
        ),
        {"methodology_id": METHODOLOGY_ID},
    )
    bind.execute(
        sa.text(
            "INSERT INTO methodology_revisions "
            "(id, methodology_id, revision, lifecycle_state, authority_reference, "
            "source_reference, source_sha256, allowed_use, research_run_eligible, created_at) "
            "VALUES (:id, :methodology_id, :revision, 'CURRENT', :authority_reference, "
            ":source_reference, :source_sha256, 'QURAN_INTERNAL_CUMULATIVE_RUN', 1, :created_at)"
        ),
        {
            "id": NEW_REVISION_ID,
            "methodology_id": METHODOLOGY_ID,
            "revision": "skill-sha256:b30ee619d8b8",
            "authority_reference": "LISAN_PLATFORM_CANONICAL_IMPLEMENTATION_REFERENCE.md",
            "source_reference": "skills/lisan-semantic-extraction/SKILL.md",
            "source_sha256": NEW_SOURCE_SHA256,
            "created_at": now,
        },
    )

def downgrade() -> None:
    bind = op.get_bind()
    bind.execute(
        sa.text("DELETE FROM methodology_revisions WHERE id=:id"),
        {"id": NEW_REVISION_ID},
    )
    bind.execute(
        sa.text(
            "UPDATE methodology_revisions SET lifecycle_state='CURRENT', "
            "research_run_eligible=1 WHERE id='LISAN_QURANIC_SEMANTIC_EXTRACTION@01784170cac4'"
        )
    )
