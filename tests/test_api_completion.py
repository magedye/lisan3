from fastapi.testclient import TestClient

from backend.infrastructure.auth import LOCAL_OWNER_TOKEN
from backend.main import app

client = TestClient(app)

def test_api_reviews_endpoint_not_found():
    response = client.post(
        "/judgments/invalid_claim_id/reviews",
        json={
            "verdict": "VERIFIED",
            "scope_disposition": "FULL",
            "evidence_package_ref": "mock_pkg",
            "independence_metadata": {"reason": "ok"}
        },
        headers={"X-Lisan-Owner-Token": LOCAL_OWNER_TOKEN}
    )
    assert response.status_code == 404

def test_api_amend_claim_endpoint_not_found():
    response = client.post(
        "/claims/invalid_claim_id/amend",
        json={
            "correction_reason": "test correction"
        },
        headers={"X-Lisan-Owner-Token": LOCAL_OWNER_TOKEN}
    )
    assert response.status_code == 404
