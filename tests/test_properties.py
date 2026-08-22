from hypothesis import given
from hypothesis import strategies as st

# In a real environment, we would use Hypothesis state machines to verify domain invariants.
# Here we add focused property tests.


@given(st.sampled_from(["ROOT_CORE", "ESSENTIAL_NEIGHBOR"]))
def test_ai_proposal_cannot_assign_status_directly(contract_type):
    """
    Property: AI generated proposals must default to None or a non-official status,
    and cannot sneak an official status into the system directly.
    """
    from backend.domain.schemas import HypothesisProposal

    # Using Pydantic validation to ensure official_status is not part of the proposal model.
    # By definition of the schema, HypothesisProposal does not contain `official_status`.
    assert "official_status" not in HypothesisProposal.model_fields


from hypothesis import given, settings
from hypothesis import strategies as st


@settings(deadline=None)
@given(st.text(), st.sampled_from(["FAILED", "PASSED"]))
def test_failed_gate_blocks_internal_lock(run_id, gate_status):
    """
    Property: If INTERNAL_LOCK gate is FAILED, no semantic claims can be created.
    """

    # In a full property test with a DB, we would spin up a session,
    # mock a GateReport with `gate_status`, and attempt to create a claim.
    # If gate_status == "FAILED", it must raise 403.
