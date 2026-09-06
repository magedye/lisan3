"""Regression: the only knowledge admission transition is canonicalization."""

from backend.main import app


def test_publication_surface_is_replaced_by_explicit_canonicalization():
    paths = app.openapi()["paths"]
    assert "/claims/{claim_id}/publish" not in paths
    assert "/judgments/{claim_id}/canonicalize" in paths
    request_schema = paths["/judgments/{claim_id}/canonicalize"]["post"]["requestBody"]
    assert "CanonicalizationRequest" in str(request_schema)
