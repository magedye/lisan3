from datetime import datetime, timezone

from backend.domain.models import (
    CanonicalState,
    ClaimScope,
    FalsificationStatus,
    ResearchState,
    ResultStrength,
    VerificationState,
)
from backend.domain.schemas import SemanticClaimResponse


def test_root_concept_template_compliance():
    response = SemanticClaimResponse(
        id="test_claim",
        contract_type="ROOT_CORE",
        research_state=ResearchState.PREFERRED,
        canonical_state=CanonicalState.ACCEPTED,
        result_strength=ResultStrength.STRONG,
        verification_state=VerificationState.VERIFIED,
        falsification_status=FalsificationStatus.PASSED,
        claim_scope=ClaimScope.UNIVERSAL,
        revision_id=1,
        created_at=datetime.now(timezone.utc),
        research_completeness={},
        layer_attribution={},
        reopen_conditions=[],
    )
    dumped = response.model_dump()
    assert "root_concept" in dumped
    assert "plain_explanation" in dumped
    assert "semantic_boundary" in dumped
    assert "strongest_counterexample" in dumped
    assert "strongest_competitor" in dumped


def test_word_concept_template_compliance():
    response = SemanticClaimResponse(
        id="test_claim",
        contract_type="WORD_CONCEPT",
        research_state=ResearchState.PREFERRED,
        canonical_state=CanonicalState.ACCEPTED,
        result_strength=ResultStrength.STRONG,
        verification_state=VerificationState.VERIFIED,
        falsification_status=FalsificationStatus.PASSED,
        claim_scope=ClaimScope.UNIVERSAL,
        revision_id=1,
        created_at=datetime.now(timezone.utc),
        research_completeness={},
        layer_attribution={},
        reopen_conditions=[],
    )
    dumped = response.model_dump()
    assert "plain_explanation" in dumped
    assert "semantic_boundary" in dumped
