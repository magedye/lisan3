from pathlib import Path

import pytest

HOME_PAGE = Path(__file__).parents[1] / "frontend" / "src" / "app" / "page.tsx"
STATUS_AXES = (
    ("المعرفي", "epistemic_state"),
    ("المراجعة", "review_state"),
    ("الحداثة", "freshness_state"),
    ("النشر", "publication_state"),
)


@pytest.mark.parametrize(("label", "field"), STATUS_AXES)
def test_found_claim_renders_each_independent_status_axis(label: str, field: str):
    source = HOME_PAGE.read_text(encoding="utf-8")
    found_claim_view = source.split(
        'result?.status === "FOUND" && result.claim', maxsplit=1
    )[1]

    assert f"<dt>{label}</dt>" in found_claim_view
    assert f"{{result.claim.{field}}}" in found_claim_view
