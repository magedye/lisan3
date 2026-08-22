from playwright.sync_api import Page

from backend.domain import models


def test_journey_4_governance_review(page: Page, e2e_server: dict):
    """
    Journey 4: Governance Rule Change, Impact Analysis, & Transitive Invalidation
    - Rule/Proposal -> impact -> approved revision -> affected claim becomes REVALIDATION_REQUIRED -> unrelated claim unchanged.
    """
    base_url = e2e_server["base_url"]
    TestSession = e2e_server["db_session"]
    db = TestSession()

    try:
        # 1. Seed Governance Rule & Dependent Claims
        rule = models.GovernanceRule(
            id="rule_gov_01",
            rule_code="RULE_E2E_ROOT",
            description="Root core induction must precede contextual expansion.",
            active_revision=1,
        )
        db.add(rule)

        claim_dep = models.SemanticClaim(
            id="clm_gov_dep",
            contract_type="ROOT_CORE",
            epistemic_state="LOCK_INTERNAL_RESULT",
            review_state="NOT_REVIEWED",
            freshness_state="CURRENT",
            publication_state="PRIVATE_WORKING",
        )
        claim_unrelated = models.SemanticClaim(
            id="clm_gov_unrelated",
            contract_type="ROOT_CORE",
            epistemic_state="LOCK_INTERNAL_RESULT",
            review_state="NOT_REVIEWED",
            freshness_state="CURRENT",
            publication_state="PRIVATE_WORKING",
        )
        db.add_all([claim_dep, claim_unrelated])

        dep_rec = models.DependencyRecord(
            id="dep_rec_01",
            dependent_claim_id="clm_gov_dep",
            dependency_type="GOVERNANCE_RULE",
            dependency_ref="RULE_E2E_ROOT",
            dependency_revision=1,
        )
        db.add(dep_rec)
        db.commit()
    finally:
        db.close()

    # 2. Submit a ChangeProposal
    prop_res = page.request.post(
        f"{base_url}/governance/proposals",
        data={
            "rule_code": "RULE_E2E_ROOT",
            "proposed_changes": "Introduce strict non-circularity constraint in rejection conditions.",
        },
    )
    assert prop_res.status == 200
    prop_data = prop_res.json()
    prop_id = prop_data["id"]
    assert prop_data["impact_analysis"]["affected_claims_count"] >= 1

    # 3. Approve ChangeProposal
    app_res = page.request.post(f"{base_url}/governance/proposals/{prop_id}/approve")
    assert app_res.status == 200

    # 4. Verify Rule History shows active revision 2
    hist_res = page.request.get(f"{base_url}/governance/rules/RULE_E2E_ROOT/history")
    assert hist_res.status == 200
    hist_data = hist_res.json()
    assert hist_data["active_revision"] == 2
    assert len(hist_data["revisions"]) >= 1

    # 5. Verify Dependent Claim became REVALIDATION_REQUIRED and Unrelated remained CURRENT
    kn_dep = page.request.get(f"{base_url}/knowledge/explorer/clm_gov_dep")
    assert kn_dep.status == 200
    assert kn_dep.json()["freshness_state"] == "REVALIDATION_REQUIRED"

    kn_unrelated = page.request.get(f"{base_url}/knowledge/explorer/clm_gov_unrelated")
    assert kn_unrelated.status == 200
    assert kn_unrelated.json()["freshness_state"] == "CURRENT"

