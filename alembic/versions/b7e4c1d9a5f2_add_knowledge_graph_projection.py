"""Add R1 knowledge graph projection tables.

Revision ID: b7e4c1d9a5f2
Revises: f4c0a1b2c3d4
Create Date: 2026-08-24 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "b7e4c1d9a5f2"
down_revision: str | None = "f4c0a1b2c3d4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "knowledge_nodes",
        sa.Column("node_id", sa.String(), nullable=False),
        sa.Column("entity_type", sa.String(), nullable=False),
        sa.Column("entity_id", sa.String(), nullable=False),
        sa.Column("entity_revision", sa.String(), nullable=False),
        sa.Column("projection_revision", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("node_id"),
        sa.UniqueConstraint("entity_type", "entity_id", name="uq_knowledge_node_entity"),
    )
    op.create_table(
        "knowledge_edges",
        sa.Column("edge_id", sa.String(), nullable=False),
        sa.Column("source_node_id", sa.String(), nullable=False),
        sa.Column("edge_type", sa.String(), nullable=False),
        sa.Column("target_node_id", sa.String(), nullable=False),
        sa.Column("edge_origin", sa.String(), nullable=False),
        sa.Column("edge_status", sa.String(), nullable=False),
        sa.Column("provenance_ref", sa.String(), nullable=False),
        sa.Column("valid_from_revision", sa.String(), nullable=False),
        sa.Column("invalidated_at", sa.DateTime(), nullable=True),
        sa.CheckConstraint(
            "edge_origin IN ('DOMAIN_PROJECTION', 'GOVERNED_ASSERTION', 'DISCOVERY_CANDIDATE')",
            name="ck_knowledge_edge_origin",
        ),
        sa.CheckConstraint(
            "edge_status IN ('ACTIVE', 'INVALIDATED', 'GOVERNED', 'CANDIDATE')",
            name="ck_knowledge_edge_status",
        ),
        sa.CheckConstraint(
            "edge_type IN ('OCCURS_IN', 'SUPPORTS', 'CHALLENGES', 'DEPENDS_ON', "
            "'DERIVED_FROM', 'USES_CORPUS', 'USES_METHODOLOGY', 'EVALUATED_BY', "
            "'INVALIDATED_BY', 'GENERATED_IN', 'NEIGHBOR_OF', 'DISTINGUISHED_FROM')",
            name="ck_knowledge_edge_type",
        ),
        sa.ForeignKeyConstraint(["source_node_id"], ["knowledge_nodes.node_id"]),
        sa.ForeignKeyConstraint(["target_node_id"], ["knowledge_nodes.node_id"]),
        sa.PrimaryKeyConstraint("edge_id"),
    )


def downgrade() -> None:
    op.drop_table("knowledge_edges")
    op.drop_table("knowledge_nodes")
