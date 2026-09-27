import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from backend.domain import models

class ToolRealityService:
    @staticmethod
    def record_tool_execution(
        db: Session,
        run_id: str,
        tool_id: str,
        trigger: str,
        actual_execution: bool,
        execution_status: str,
        source_role: str,
        output_ref: str = None,
        what_it_can_reveal: str = None,
        what_it_cannot_prove: str = None,
        evidence_effect: str = None,
    ) -> models.ToolReceipt:
        """Enforce Slice H: Tool Reality. Differentiate between TOOL_REQUESTED and TOOL_EXECUTED."""
        if not actual_execution and execution_status == "SUCCEEDED":
            raise ValueError("Tool cannot be SUCCEEDED if it was not actually executed")

        receipt = models.ToolReceipt(
            id=f"tr_{uuid.uuid4().hex[:8]}",
            research_run_id=run_id,
            tool_id=tool_id,
            trigger=trigger,
            actual_execution=actual_execution,
            execution_status=execution_status,
            source_role=source_role,
            output_ref=output_ref,
            what_it_can_reveal=what_it_can_reveal,
            what_it_cannot_prove=what_it_cannot_prove,
            evidence_effect=evidence_effect,
            created_at=datetime.now(timezone.utc).replace(tzinfo=None)
        )
        db.add(receipt)
        db.commit()
        db.refresh(receipt)
        return receipt

    @staticmethod
    def validate_tool_reality_for_claim(db: Session, run_id: str, required_tools: list[str]):
        """Ensure that before a claim is validated, required tools were ACTUALLY executed and succeeded."""
        executed_tools = db.query(models.ToolReceipt).filter(
            models.ToolReceipt.research_run_id == run_id,
            models.ToolReceipt.actual_execution == True,
            models.ToolReceipt.execution_status == "SUCCEEDED"
        ).all()
        
        executed_tool_ids = {t.tool_id for t in executed_tools}
        missing = set(required_tools) - executed_tool_ids
        
        if missing:
            raise ValueError(f"Tool Reality Violation: Required tools {missing} were not actually executed or did not succeed.")
