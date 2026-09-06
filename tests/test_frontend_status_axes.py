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
# The simplified contract replaces the four independent lifecycle axes with the
# two decision-bearing states (research + canonical) plus optional strength and
# verification facts. See SIMPLIFIED_AI_AUTHORITY_AND_GOVERNANCE_CONTRACT.md.
RESEARCH_STATUS_FACTS = (
    ("حالة البحث", "research", "research_state"),
    ("الحالة المعتمدة", "canonical", "canonical_state"),
)


@pytest.mark.parametrize(("label", "prop", "field"), RESEARCH_STATUS_FACTS)
def test_found_claim_renders_each_research_status_fact(
    label: str, prop: str, field: str
):
    home_source = HOME_PAGE.read_text(encoding="utf-8")
    component_source = STATUS_COMPONENT.read_text(encoding="utf-8")

    assert label in component_source
    assert f"{prop}={{result.claim.{field}}}" in home_source
