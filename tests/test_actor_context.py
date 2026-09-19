import pytest

from backend.domain.models import SemanticClaim
from backend.domain.services.actor_context import ActorContext, ActorRole
from backend.domain.services.canonicalization import CanonicalizationPolicy


def test_actor_context_require_role():
    # Setup
    sys_actor = ActorContext.system()
    owner_actor = ActorContext(identity="TRUSTED_LOCAL_OWNER", role=ActorRole.OWNER_OPERATOR)
    researcher_actor = ActorContext(role=ActorRole.RESEARCHER, identity="res1")

    # System actor should have SYSTEM_FIXTURE role
    assert sys_actor.role == ActorRole.SYSTEM_FIXTURE

    # require_role success
    ActorContext.require_role(researcher_actor, ActorRole.RESEARCHER)
    
    # OWNER_OPERATOR can bypass standard roles
    ActorContext.require_role(owner_actor, ActorRole.RESEARCHER)
    ActorContext.require_role(owner_actor, ActorRole.VERIFIER)

    # Negative test: incorrect role
    with pytest.raises(PermissionError, match="Action requires role REVIEWER"):
        ActorContext.require_role(researcher_actor, ActorRole.REVIEWER)

def test_canonicalize_requires_owner_operator(test_db):
    claim = SemanticClaim(id="test_claim", contract_type="ROOT_CONCEPT")
    test_db.add(claim)
    
    # Negative test: Canonicalize by RESEARCHER should fail
    researcher_actor = ActorContext(role=ActorRole.RESEARCHER, identity="res1")
    
    with pytest.raises(PermissionError, match="Action requires role OWNER_OPERATOR"):
        CanonicalizationPolicy.canonicalize(
            test_db, claim, rationale="Testing", actor_context=researcher_actor
        )

    # Negative test: Canonicalize by an OWNER_OPERATOR not in AUTHORIZED list
    unauth_owner = ActorContext(role=ActorRole.OWNER_OPERATOR, identity="SOME_HACKER")
    with pytest.raises(ValueError, match="is not authorized to canonicalize"):
        CanonicalizationPolicy.canonicalize(
            test_db, claim, rationale="Testing", actor_context=unauth_owner
        )
