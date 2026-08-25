from pathlib import Path

import pytest

HOME_PAGE = Path(__file__).parents[1] / "frontend" / "src" / "app" / "page.tsx"
STATUS_COMPONENT = (
    Path(__file__).parents[1]
    / "frontend"
    / "src"
    / "components"
    / "status-axes.tsx"
)
STATUS_AXES = (
    ("المعرفي", "epistemic_state"),
    ("المراجعة", "review_state"),
    ("الحداثة", "freshness_state"),
    ("النشر", "publication_state"),
)


@pytest.mark.parametrize(("label", "field"), STATUS_AXES)
def test_found_claim_renders_each_independent_status_axis(label: str, field: str):
    home_source = HOME_PAGE.read_text(encoding="utf-8")
    component_source = STATUS_COMPONENT.read_text(encoding="utf-8")

    assert f'{field.split("_", maxsplit=1)[0]}:' in component_source
    assert label in component_source
    assert f"{field.split('_', maxsplit=1)[0]}={{result.claim.{field}}}" in home_source
