from dataclasses import dataclass
from enum import Enum


class ActorRole(str, Enum):
    RESEARCHER = "RESEARCHER"
    REVIEWER = "REVIEWER"
    VERIFIER = "VERIFIER"
    OWNER_OPERATOR = "OWNER_OPERATOR"
    SYSTEM_FIXTURE = "SYSTEM_FIXTURE"
    STEWARD = "STEWARD"
    ANONYMOUS = "ANONYMOUS"


@dataclass(frozen=True)
class ActorContext:
    """
    Structured context to enforce strict authority boundaries across domain services.
    Services must accept this context rather than arbitrary string actor names.
    """
    identity: str
    role: ActorRole

    @classmethod
    def system(cls) -> "ActorContext":
        return cls(identity="SYSTEM", role=ActorRole.SYSTEM_FIXTURE)

    @classmethod
    def require_role(cls, context: "ActorContext", role: ActorRole):
        if context.role != role and context.role != ActorRole.OWNER_OPERATOR:
            raise PermissionError(
                f"Action requires role {role.value}, but actor {context.identity} "
                f"has role {context.role.value}"
            )
