"""Regression: methodology diagnostics are not numeric or research gates."""

from backend.domain.services.purity import DIAGNOSTIC_DIMENSIONS
from backend.main import app


def test_eight_diagnostics_remain_named_without_purity_gate():
    assert len(DIAGNOSTIC_DIMENSIONS) == 8
    schema = app.openapi()["components"]["schemas"]["MethodologyDiagnosticsResponse"]
    serialized = str(schema)
    assert "purity_score" not in serialized
    assert "hard_blockers" in serialized
    assert "/runs/{run_id}/gates" not in app.openapi()["paths"]
