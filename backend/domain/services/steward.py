"""Steward command dispatch boundary with honest outcome persistence."""

import uuid

from sqlalchemy.orm import Session

from backend.domain import models, schemas

FORBIDDEN_COMMANDS = frozenset(
    {
        "PASS_GATE",
        "FORCE_LOCK",
        "APPROVE_REVIEW",
        "PUBLISH_CLAIM",
        "ESTABLISH_ROOT_CORE",
    }
)
FORBIDDEN_INTENT_TERMS = frozenset({"ROOT_CORE", "BYPASS", "FORCE", "OVERRIDE"})


class StewardAuthorityRejected(Exception):
    pass


class StewardCommandService:
    @staticmethod
    def _record(
        db: Session,
        command: schemas.StewardCommandCreate,
        *,
        status: str,
        summary: str,
        audit_action: str,
    ) -> models.StewardCommand:
        command_id = f"steward_{uuid.uuid4().hex[:8]}"
        persisted = models.StewardCommand(
            id=command_id,
            command_type=command.command_type,
            intent=command.intent,
            parameters=command.parameters,
            evaluated_rules=None,
            execution_status=status,
            result_summary=summary,
        )
        db.add(persisted)
        db.add(
            models.AuditLog(
                id=f"aud_{uuid.uuid4().hex[:8]}",
                entity_id=command_id,
                entity_type="StewardCommand",
                action=audit_action,
                new_state=status,
                actor="STEWARD_COMMAND_SERVICE",
            )
        )
        db.commit()
        db.refresh(persisted)
        return persisted

    @classmethod
    def execute(
        cls, db: Session, command: schemas.StewardCommandCreate
    ) -> models.StewardCommand:
        intent = command.intent.upper()
        if command.command_type in FORBIDDEN_COMMANDS or any(
            term in intent for term in FORBIDDEN_INTENT_TERMS
        ):
            cls._record(
                db,
                command,
                status="REJECTED",
                summary="Rejected: command exceeds Steward authority.",
                audit_action="REJECT_AUTHORITY_BOUNDARY",
            )
            raise StewardAuthorityRejected(
                "Steward cannot bypass epistemic lifecycle gates, locks, review, or publication."
            )

        return cls._record(
            db,
            command,
            status="UNSUPPORTED",
            summary="Unsupported: no canonical executable Steward command is registered.",
            audit_action="REJECT_UNSUPPORTED",
        )
