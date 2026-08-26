from playwright.sync_api import Page, expect

from backend.domain import models


def test_journey_4_governance_review(page: Page, e2e_server: dict, monkeypatch):
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

        run = models.ResearchRun(
            id="run_gov_review",
            target_contract="ROOT_CORE",
            target_expression="governance",
            methodology_revision="method-e2e-fixture",
            corpus_snapshot="snapshot-e2e-fixture",
            authority_context={"source": "e2e"},
        )
        isolation = models.IsolationState(
            id="isolation_gov_review",
            research_run_id=run.id,
            target_contract=run.target_contract,
            corpus_snapshot=run.corpus_snapshot,
            methodology_reference=run.methodology_revision,
            allowed_sources=["QURAN_CORPUS"],
            is_contaminated="CLEAN",
        )
        db.add_all([run, isolation])

        claim_dep = models.SemanticClaim(
            id="clm_gov_dep",
            research_run_id=run.id,
            contract_type="ROOT_CORE",
            epistemic_state="LOCK_INTERNAL_RESULT",
            review_state="NOT_REVIEWED",
            freshness_state="CURRENT",
            publication_state="PRIVATE_WORKING",
        )
        claim_unrelated = models.SemanticClaim(
            id="clm_gov_unrelated",
            research_run_id=run.id,
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

    monkeypatch.setattr(
        "backend.domain.services.claim_visibility.has_valid_gate", lambda *_args: True
    )

    # 2. Submit a ChangeProposal
    page.goto(f"{base_url}/governance")
    expect(page.locator("h1")).to_contain_text("Governance Center")
    
    page.fill("#proposal-rule-code", "RULE_E2E_ROOT")
    page.fill("#proposed-changes", "Introduce strict non-circularity constraint in rejection conditions.")
    page.click("button:has-text('Submit Proposal')")

    # 3. Approve ChangeProposal
    expect(
        page.get_by_role("status").filter(has_text="Proposal ID:")
    ).to_be_visible(timeout=10000)
    page.click("button:has-text('Approve Proposal')")
    with page.expect_response(
        lambda response: response.request.method == "POST"
        and "/governance/proposals/" in response.url
        and response.url.endswith("/approve")
    ) as approval_response:
        page.get_by_role("button", name="تأكيد الاعتماد").click()
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
