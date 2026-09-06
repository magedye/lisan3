"""Simplify semantic research authority and canonicalization state.

Revision ID: f1a6c3d9e204
Revises: c4d8b7e2a913
Create Date: 2026-09-06 00:00:00.000000
"""

import hashlib
import json
from collections.abc import Sequence
from datetime import datetime, timezone

import sqlalchemy as sa

from alembic import op

revision: str = "f1a6c3d9e204"
down_revision: str | None = "c4d8b7e2a913"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

METHODOLOGY_ID = "LISAN_QURANIC_SEMANTIC_EXTRACTION"
NEW_REVISION_ID = "LISAN_QURANIC_SEMANTIC_EXTRACTION@01784170cac4"
NEW_SOURCE_SHA256 = "01784170cac4e715c1477cb6a04a2c34b21c4bdb91705aa1eb6b2a896efcedbd"


def _json(value):
    if value is None:
        return None
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value
    return value


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
            "revision": "skill-sha256:01784170cac4",
            "authority_reference": "SIMPLIFIED_AI_AUTHORITY_AND_GOVERNANCE_CONTRACT.md",
            "source_reference": "skills/lisan-semantic-extraction/SKILL.md",
            "source_sha256": NEW_SOURCE_SHA256,
            "created_at": now,
        },
    )

    with op.batch_alter_table("semantic_claims") as batch_op:
        batch_op.drop_constraint("ck_semantic_claim_epistemic_state", type_="check")
        batch_op.drop_constraint("ck_semantic_claim_review_state", type_="check")
        batch_op.drop_constraint("ck_semantic_claim_freshness_state", type_="check")
        batch_op.drop_constraint("ck_semantic_claim_publication_state", type_="check")
        batch_op.add_column(
            sa.Column("research_state", sa.String(), nullable=False, server_default="UNRESOLVED")
        )
        batch_op.add_column(
            sa.Column("canonical_state", sa.String(), nullable=False, server_default="NOT_CANONICAL")
        )
        batch_op.add_column(
            sa.Column("result_strength", sa.String(), nullable=False, server_default="UNRESOLVED")
        )
        batch_op.add_column(
            sa.Column("verification_state", sa.String(), nullable=False, server_default="NOT_REQUIRED")
        )
        batch_op.add_column(
            sa.Column("falsification_status", sa.String(), nullable=False, server_default="NOT_REQUIRED")
        )
        batch_op.add_column(
            sa.Column("claim_scope", sa.String(), nullable=False, server_default="LOCAL")
        )
        batch_op.add_column(sa.Column("sampling_basis", sa.String(), nullable=True))
        batch_op.add_column(
            sa.Column("research_completeness", sa.JSON(), nullable=False, server_default="{}")
        )
        batch_op.add_column(sa.Column("preferred_conclusion", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("plain_explanation", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("semantic_boundary", sa.String(), nullable=True))
        batch_op.add_column(
            sa.Column("layer_attribution", sa.JSON(), nullable=False, server_default="{}")
        )
        batch_op.add_column(
            sa.Column("hard_cases", sa.JSON(), nullable=False, server_default="[]")
        )
        batch_op.add_column(sa.Column("strongest_counterexample", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("strongest_competitor", sa.String(), nullable=True))
        batch_op.add_column(
            sa.Column("reopen_conditions", sa.JSON(), nullable=False, server_default="[]")
        )
        batch_op.add_column(sa.Column("accepted_at", sa.DateTime(), nullable=True))

    rows = bind.execute(sa.text("SELECT * FROM semantic_claims ORDER BY id")).mappings().all()
    for row in rows:
        old_epistemic = row["epistemic_state"]
        if old_epistemic == "REJECTED":
            research_state = "REJECTED"
            result_strength = "WEAK"
        elif old_epistemic in {"TESTED", "SUPPORTED", "LOCK_INTERNAL_RESULT"}:
            research_state = "PREFERRED"
            result_strength = "MODERATE"
        else:
            research_state = "UNRESOLVED"
            result_strength = "UNRESOLVED"
        was_published = row["publication_state"] == "PUBLISHED"
        canonical_state = "REOPEN_REQUIRED" if was_published else "NOT_CANONICAL"
        verification_state = (
            "NOT_VERIFIED" if research_state == "PREFERRED" or was_published else "NOT_REQUIRED"
        )
        preferred_conclusion = (
            row["root_concept"]
            or row["root_meaning"]
            or row["root_definition"]
            or row["abstract_root_core"]
        )
        completeness = {
            "sufficient_for_claim": False,
            "migration_note": "Legacy free-text coverage was not treated as deterministic proof",
            "legacy_index_coverage": row["index_coverage"],
            "legacy_deep_analysis_coverage": row["deep_analysis_coverage"],
        }
        bind.execute(
            sa.text(
                "UPDATE semantic_claims SET research_state=:research_state, "
                "canonical_state=:canonical_state, result_strength=:result_strength, "
                "verification_state=:verification_state, falsification_status=:falsification_status, "
                "claim_scope='LOCAL', research_completeness=:completeness, "
                "preferred_conclusion=:preferred_conclusion, plain_explanation=:plain_explanation, "
                "layer_attribution=:layers, hard_cases=:hard_cases, "
                "reopen_conditions=:reopen_conditions, accepted_at=:accepted_at, "
                "rejection_condition=NULL WHERE id=:id"
            ),
            {
                "id": row["id"],
                "research_state": research_state,
                "canonical_state": canonical_state,
                "result_strength": result_strength,
                "verification_state": verification_state,
                "falsification_status": "NOT_RUN" if research_state == "PREFERRED" else "NOT_REQUIRED",
                "completeness": json.dumps(completeness, sort_keys=True),
                "preferred_conclusion": preferred_conclusion,
                "plain_explanation": row["root_definition"] or row["root_meaning"],
                "layers": json.dumps({}),
                "hard_cases": json.dumps([]),
                "reopen_conditions": json.dumps(
                    ["Revalidate legacy result under the simplified contract"]
                    if was_published
                    else []
                ),
                "accepted_at": row["created_at"] if was_published else None,
            },
        )
        before = {
            "epistemic_state": old_epistemic,
            "review_state": row["review_state"],
            "freshness_state": row["freshness_state"],
            "publication_state": row["publication_state"],
        }
        after = {
            "research_state": research_state,
            "canonical_state": canonical_state,
            "result_strength": result_strength,
            "verification_state": verification_state,
        }
        digest = hashlib.sha256(f"{row['id']}|{json.dumps(before, sort_keys=True)}".encode()).hexdigest()[:20]
        bind.execute(
            sa.text(
                "INSERT INTO audit_logs (id, entity_id, entity_type, action, previous_state, "
                "new_state, actor, created_at) VALUES (:id, :entity_id, 'ResearchJudgment', "
                "'SIMPLIFY_AI_GOVERNANCE_STATUS', :previous_state, :new_state, "
                "'ALEMBIC_F1A6C3D9E204', :created_at)"
            ),
            {
                "id": f"aud_simple_{digest}",
                "entity_id": row["id"],
                "previous_state": json.dumps(before, sort_keys=True),
                "new_state": json.dumps(after, sort_keys=True),
                "created_at": now,
            },
        )

    for column in ("supporting_evidence", "counterevidence", "unresolved_cases"):
        bind.execute(
            sa.text(f"UPDATE semantic_claims SET {column}='[]' WHERE {column} IS NULL")
        )
    with op.batch_alter_table("semantic_claims") as batch_op:
        for column in (
            "epistemic_state",
            "review_state",
            "freshness_state",
            "publication_state",
            "index_coverage",
            "deep_analysis_coverage",
            "abstract_root_core",
            "root_definition",
            "root_meaning",
        ):
            batch_op.drop_column(column)
        batch_op.alter_column(
            "rejection_condition",
            existing_type=sa.String(),
            type_=sa.JSON(),
            existing_nullable=True,
        )
        batch_op.alter_column("supporting_evidence", existing_type=sa.JSON(), nullable=False)
        batch_op.alter_column("counterevidence", existing_type=sa.JSON(), nullable=False)
        batch_op.alter_column("unresolved_cases", existing_type=sa.JSON(), nullable=False)
        batch_op.create_check_constraint(
            "ck_semantic_claim_research_state",
            "research_state IN ('PREFERRED', 'UNRESOLVED', 'REJECTED')",
        )
        batch_op.create_check_constraint(
            "ck_semantic_claim_canonical_state",
            "canonical_state IN ('NOT_CANONICAL', 'ACCEPTED', 'REOPEN_REQUIRED')",
        )
        batch_op.create_check_constraint(
            "ck_semantic_claim_result_strength",
            "result_strength IN ('WEAK', 'MODERATE', 'STRONG', 'UNRESOLVED')",
        )
        batch_op.create_check_constraint(
            "ck_semantic_claim_verification_state",
            "verification_state IN ('NOT_REQUIRED', 'NOT_VERIFIED', 'VERIFIED')",
        )
        batch_op.create_check_constraint(
            "ck_semantic_claim_falsification_status",
            "falsification_status IN ('NOT_REQUIRED', 'NOT_RUN', 'PASSED', 'FAILED')",
        )
        batch_op.create_check_constraint(
            "ck_semantic_claim_scope",
            "claim_scope IN ('UNIVERSAL', 'REPRESENTATIVE', 'LOCAL')",
        )

    gate_rows = bind.execute(sa.text("SELECT * FROM gate_reports ORDER BY id")).mappings().all()
    for row in gate_rows:
        payload = {
            key: (_json(row[key]) if key == "evidence_refs" else row[key])
            for key in row
            if key != "created_at"
        }
        digest = hashlib.sha256(f"gate|{row['id']}".encode()).hexdigest()[:20]
        bind.execute(
            sa.text(
                "INSERT INTO audit_logs (id, entity_id, entity_type, action, previous_state, "
                "new_state, actor, created_at) VALUES (:id, :entity_id, 'LegacyGateReport', "
                "'ARCHIVE_RETIRED_RESEARCH_GATE', NULL, :payload, "
                "'ALEMBIC_F1A6C3D9E204', :created_at)"
            ),
            {
                "id": f"aud_gate_{digest}",
                "entity_id": row["id"],
                "payload": json.dumps(payload, sort_keys=True),
                "created_at": row["created_at"] or now,
            },
        )
    op.drop_index(op.f("ix_gate_reports_id"), table_name="gate_reports")
    op.drop_table("gate_reports")

    op.rename_table("review_decisions", "verification_records")
    with op.batch_alter_table("verification_records") as batch_op:
        batch_op.alter_column("reviewer_identity", new_column_name="verifier_identity")
        batch_op.add_column(
            sa.Column(
                "verification_type",
                sa.String(),
                nullable=False,
                server_default="LEGACY_REVIEW_NOT_INDEPENDENT",
            )
        )
        batch_op.add_column(
            sa.Column("evidence_refs", sa.JSON(), nullable=False, server_default="[]")
        )
    bind.execute(
        sa.text(
            "UPDATE verification_records SET decision = CASE "
            "WHEN decision='APPROVED' THEN 'VERIFIED' ELSE 'REJECTED' END"
        )
    )
    with op.batch_alter_table("verification_records") as batch_op:
        batch_op.create_check_constraint(
            "ck_verification_record_decision",
            "decision IN ('VERIFIED', 'REJECTED')",
        )
    op.execute("DROP INDEX IF EXISTS ix_review_decisions_id")
    op.create_index(
        op.f("ix_verification_records_id"),
        "verification_records",
        ["id"],
        unique=False,
    )

    bind.execute(
        sa.text(
            "UPDATE research_runs SET current_stage = CASE "
            "WHEN current_stage IN ('DIFFERENTIATION', 'LOCKING') THEN 'CHALLENGE' "
            "ELSE 'RESEARCH' END, status = CASE WHEN status='LOCK_BLOCKED' THEN 'ACTIVE' ELSE status END"
        )
    )


def downgrade() -> None:
    bind = op.get_bind()

    op.create_table(
        "gate_reports",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("research_run_id", sa.String(), nullable=True),
        sa.Column("gate_code", sa.String(), nullable=False),
        sa.Column("display_name", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("evidence_refs", sa.JSON(), nullable=True),
        sa.Column("failure_reason", sa.String(), nullable=True),
        sa.Column("evaluated_revision", sa.String(), nullable=True),
        sa.Column("required_action", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["research_run_id"], ["research_runs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_gate_reports_id"), "gate_reports", ["id"], unique=False)
    gate_audits = bind.execute(
        sa.text(
            "SELECT id, new_state, created_at FROM audit_logs "
            "WHERE action='ARCHIVE_RETIRED_RESEARCH_GATE' "
            "AND actor='ALEMBIC_F1A6C3D9E204'"
        )
    ).mappings().all()
    for audit in gate_audits:
        payload = json.loads(audit["new_state"])
        bind.execute(
            sa.text(
                "INSERT INTO gate_reports (id, research_run_id, gate_code, display_name, status, "
                "evidence_refs, failure_reason, evaluated_revision, required_action, created_at) "
                "VALUES (:id, :research_run_id, :gate_code, :display_name, :status, "
                ":evidence_refs, :failure_reason, :evaluated_revision, :required_action, :created_at)"
            ),
            {
                **payload,
                "evidence_refs": json.dumps(payload.get("evidence_refs")),
                "created_at": audit["created_at"],
            },
        )

    with op.batch_alter_table("verification_records") as batch_op:
        batch_op.drop_constraint("ck_verification_record_decision", type_="check")
    bind.execute(
        sa.text(
            "UPDATE verification_records SET decision = CASE "
            "WHEN decision='VERIFIED' THEN 'APPROVED' ELSE 'REJECTED' END"
        )
    )
    op.execute("DROP INDEX IF EXISTS ix_verification_records_id")
    with op.batch_alter_table("verification_records") as batch_op:
        batch_op.drop_column("evidence_refs")
        batch_op.drop_column("verification_type")
        batch_op.alter_column("verifier_identity", new_column_name="reviewer_identity")
    op.rename_table("verification_records", "review_decisions")
    op.create_index(
        op.f("ix_review_decisions_id"), "review_decisions", ["id"], unique=False
    )

    with op.batch_alter_table("semantic_claims") as batch_op:
        for constraint in (
            "ck_semantic_claim_scope",
            "ck_semantic_claim_falsification_status",
            "ck_semantic_claim_verification_state",
            "ck_semantic_claim_result_strength",
            "ck_semantic_claim_canonical_state",
            "ck_semantic_claim_research_state",
        ):
            batch_op.drop_constraint(constraint, type_="check")
        batch_op.add_column(sa.Column("epistemic_state", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("review_state", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("freshness_state", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("publication_state", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("index_coverage", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("deep_analysis_coverage", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("abstract_root_core", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("root_definition", sa.String(), nullable=True))
        batch_op.add_column(sa.Column("root_meaning", sa.String(), nullable=True))

    rows = bind.execute(sa.text("SELECT * FROM semantic_claims ORDER BY id")).mappings().all()
    for row in rows:
        epistemic = {
            "PREFERRED": "LOCK_INTERNAL_RESULT",
            "REJECTED": "REJECTED",
            "UNRESOLVED": "UNRESOLVED",
        }[row["research_state"]]
        review = "APPROVED" if row["verification_state"] == "VERIFIED" else "NOT_REVIEWED"
        freshness = "REVALIDATION_REQUIRED" if row["canonical_state"] == "REOPEN_REQUIRED" else "CURRENT"
        publication = "PUBLISHED" if row["canonical_state"] == "ACCEPTED" else "PRIVATE_WORKING"
        completeness = _json(row["research_completeness"]) or {}
        bind.execute(
            sa.text(
                "UPDATE semantic_claims SET epistemic_state=:epistemic, review_state=:review, "
                "freshness_state=:freshness, publication_state=:publication, "
                "index_coverage=:index_coverage, deep_analysis_coverage=:deep_coverage, "
                "abstract_root_core=:conclusion, root_definition=:plain, root_meaning=:plain "
                "WHERE id=:id"
            ),
            {
                "id": row["id"],
                "epistemic": epistemic,
                "review": review,
                "freshness": freshness,
                "publication": publication,
                "index_coverage": json.dumps(completeness, sort_keys=True),
                "deep_coverage": json.dumps(completeness, sort_keys=True),
                "conclusion": row["preferred_conclusion"],
                "plain": row["plain_explanation"],
            },
        )

    with op.batch_alter_table("semantic_claims") as batch_op:
        for column in (
            "accepted_at",
            "reopen_conditions",
            "strongest_competitor",
            "strongest_counterexample",
            "hard_cases",
            "layer_attribution",
            "semantic_boundary",
            "plain_explanation",
            "preferred_conclusion",
            "research_completeness",
            "sampling_basis",
            "claim_scope",
            "falsification_status",
            "verification_state",
            "result_strength",
            "canonical_state",
            "research_state",
        ):
            batch_op.drop_column(column)
        batch_op.alter_column(
            "rejection_condition",
            existing_type=sa.JSON(),
            type_=sa.String(),
            existing_nullable=True,
        )
        batch_op.alter_column("supporting_evidence", existing_type=sa.JSON(), nullable=True)
        batch_op.alter_column("counterevidence", existing_type=sa.JSON(), nullable=True)
        batch_op.alter_column("unresolved_cases", existing_type=sa.JSON(), nullable=True)
        batch_op.create_check_constraint(
            "ck_semantic_claim_epistemic_state",
            "epistemic_state IN ('OBSERVATION', 'HYPOTHESIS', 'TESTED', 'SUPPORTED', "
            "'LOCK_BLOCKED', 'LOCK_INTERNAL_RESULT', 'REJECTED', 'UNRESOLVED')",
        )
        batch_op.create_check_constraint(
            "ck_semantic_claim_review_state",
            "review_state IN ('NOT_REVIEWED', 'REVIEW_REQUIRED', 'IN_REVIEW', "
            "'APPROVED', 'REJECTED', 'OWNER_DECISION_REQUIRED')",
        )
        batch_op.create_check_constraint(
            "ck_semantic_claim_freshness_state",
            "freshness_state IN ('CURRENT', 'STALE', 'INVALIDATED', 'REVALIDATION_REQUIRED')",
        )
        batch_op.create_check_constraint(
            "ck_semantic_claim_publication_state",
            "publication_state IN ('PRIVATE_WORKING', 'REVIEWABLE', 'PUBLISHABLE', "
            "'PUBLISHED', 'WITHDRAWN')",
        )
        for column in ("epistemic_state", "review_state", "freshness_state", "publication_state"):
            batch_op.alter_column(column, existing_type=sa.String(), nullable=False)

    bind.execute(
        sa.text(
            "DELETE FROM audit_logs WHERE action IN "
            "('SIMPLIFY_AI_GOVERNANCE_STATUS', 'ARCHIVE_RETIRED_RESEARCH_GATE') "
            "AND actor='ALEMBIC_F1A6C3D9E204'"
        )
    )
    bind.execute(sa.text("DELETE FROM methodology_revisions WHERE id=:id"), {"id": NEW_REVISION_ID})
    bind.execute(
        sa.text(
            "UPDATE methodology_revisions SET lifecycle_state='CURRENT', research_run_eligible=1 "
            "WHERE methodology_id=:methodology_id"
        ),
        {"methodology_id": METHODOLOGY_ID},
    )
