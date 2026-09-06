"""Small property checks for the simplified authority model."""

from hypothesis import given
from hypothesis import strategies as st
from pydantic import ValidationError

from backend.domain.schemas import ResearchJudgmentCreate


@given(st.sampled_from(["PREFERRED", "UNRESOLVED", "REJECTED"]))
def test_research_judgment_input_has_no_canonical_authority(state):
    payload = {
        "contract_type": "ROOT_CONCEPT",
        "research_state": state,
        "claim_scope": "LOCAL",
        "result_strength": "UNRESOLVED" if state == "UNRESOLVED" else "WEAK",
        "canonical_state": "ACCEPTED",
    }
    try:
        ResearchJudgmentCreate.model_validate(payload)
    except ValidationError as exc:
        assert "canonical_state" in str(exc)
    else:
        raise AssertionError("AI/caller input must not accept canonical_state")
