"""Regression: retired research gates cannot be recreated through the API."""

from backend.main import app


def test_research_gate_surface_is_removed():
    paths = app.openapi()["paths"]
    assert "/runs/{run_id}/gates" not in paths
    assert all("GateReport" not in name for name in app.openapi()["components"]["schemas"])
