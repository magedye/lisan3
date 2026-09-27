import pytest

from backend.domain.models import (
    CorpusSnapshot,
    MethodologyRevision,
    SemanticClaim,
)
from backend.domain.services.canonicalization import CanonicalizationPolicy
from backend.domain.services.run_admission import ResearchRunAdmissionPolicy


@pytest.fixture
def test_corpus_snapshot(test_db):
    snap = CorpusSnapshot(
        id="snap_word_concept",
        canonical_text_source="TANZIL_QURAN_UTHMANI",
        canonical_text_version="1.1",
        canonical_text_hash="hash",
        validation_status="PENDING",
        fixture_only=False,
    )
    test_db.add(snap)
    test_db.commit()
    return snap


@pytest.fixture
def test_methodology(test_db):
    meth = MethodologyRevision(
        id="meth_word_concept",
        methodology_id="m1",
        revision="1.0",
        lifecycle_state="CURRENT",
        authority_reference="test",
        source_reference="test",
        source_sha256="0" * 64,
        allowed_use="ALL",
    )
    test_db.add(meth)
    test_db.commit()
    return meth


def test_word_concept_spaces(test_db, test_corpus_snapshot, test_methodology):
    decision = ResearchRunAdmissionPolicy.evaluate(
        test_db,
        corpus_snapshot_id=test_corpus_snapshot.id,
        methodology_revision=test_methodology.id,
        target_contract="WORD_CONCEPT",
        target_expression="word concept",
    )
    assert not decision.accepted
    assert any("must not contain spaces" in r for r in decision.reasons)


def test_lexeme_spaces(test_db, test_corpus_snapshot, test_methodology):
    decision = ResearchRunAdmissionPolicy.evaluate(
        test_db,
        corpus_snapshot_id=test_corpus_snapshot.id,
        methodology_revision=test_methodology.id,
        target_contract="LEXEME",
        target_expression="multiple words",
    )
    assert not decision.accepted
    assert any("must be a single recognized lemma" in r for r in decision.reasons)


def test_lexeme_morphological_expansion(test_db):
    claim = SemanticClaim(
        id="lexeme_claim",
        contract_type="LEXEME",
        research_completeness={"morphological_expansion_performed": False},
    )
    test_db.add(claim)

    # Let's mock evaluate's other requirements and focus on the lexeme check
    decision = CanonicalizationPolicy.evaluate(test_db, claim)
    assert not decision.accepted
    assert any(
        "LEXEME requires full morphological expansion" in r for r in decision.reasons
    )

    claim.research_completeness = {"morphological_expansion_performed": True}
    test_db.add(claim)
    decision = CanonicalizationPolicy.evaluate(test_db, claim)
    # the check should no longer be in the reasons
    assert not any(
        "LEXEME requires full morphological expansion" in r for r in decision.reasons
    )
