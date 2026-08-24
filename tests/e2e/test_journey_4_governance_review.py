from playwright.sync_api import Page, expect

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
    page.goto(f"{base_url}/governance")
    expect(page.locator("h1")).to_contain_text("Governance Center")
    
    page.fill("input[placeholder='Rule Code']", "RULE_E2E_ROOT")
    page.fill("textarea[placeholder='Proposed changes']", "Introduce strict non-circularity constraint in rejection conditions.")
    page.click("button:has-text('Submit Proposal')")

    # 3. Approve ChangeProposal
    expect(page.locator("text=Proposal ID: ")).to_be_visible(timeout=10000)
    with page.expect_response(
        lambda response: response.request.method == "POST"
        and "/governance/proposals/" in response.url
        and response.url.endswith("/approve")
    ) as approval_response:
        page.click("button:has-text('Approve Proposal')")
    assert approval_response.value.status == 200

    # 4. Verify Rule History shows active revision 2
    page.click("button:has-text('Check History')")
    expect(page.locator("#active-revision")).to_contain_text("Revision: 2", timeout=10000)
    expect(page.locator("#revisions-count")).to_contain_text("Revisions: ")

    # 5. Verify Dependent Claim became REVALIDATION_REQUIRED and Unrelated remained CURRENT
    # (Since there is no UI for knowledge explorer yet, we fall back to API for this assertion)
    kn_dep = page.request.get(f"{e2e_server['api_url']}/knowledge/explorer/clm_gov_dep")
    assert kn_dep.status == 200
    assert kn_dep.json()["freshness_state"] == "REVALIDATION_REQUIRED"

    kn_unrelated = page.request.get(f"{e2e_server['api_url']}/knowledge/explorer/clm_gov_unrelated")
    assert kn_unrelated.status == 200
    assert kn_unrelated.json()["freshness_state"] == "CURRENT"
