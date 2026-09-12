"""Phase 0A — Master Admission & Pre-Analysis Foundation acceptance tests.

Binds the ten mandatory properties of the Phase 0A task to executable checks:

 1  direct textual facts are not model-generated
 2  deterministic counts are reproducible
 3  structural uncertainty is preserved
 4  one confirmed unexplained occurrence blocks an ACCEPTED root-wide concept
 5  no percentage/majority threshold bypasses universal presence
 6  external source claim cannot become semantic authority
 7  external hypothesis cannot masquerade as blind internal discovery
 8  assistant proposal cannot become owner-accepted silently
 9  V2.1/canonical preserved content is not silently rewritten
 10 unrelated current behavior remains green  (whole suite; not asserted here)

Tests 1-3 exercise the new deterministic Root Descriptive Profile read-model.
Tests 4-9 exercise the governed runtime through the same in-memory harness the
existing governance suite uses.
"""

import hashlib
from datetime import datetime, timezone
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.domain import models
from backend.domain.services.corpus.authority import CANONICAL_CORPUS_ADMISSIONS
from backend.domain.services.corpus.descriptive_profile import (
    ATTR_DISPUTED,
    EXTRACTION_METHOD,
    KnowledgeLevel,
    RootDescriptiveProfileService,
    StructuralToken,
)
from backend.infrastructure.database import Base, get_db
from backend.main import app

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base.metadata.create_all(engine)
client = TestClient(app)


def override_db():
    with SessionLocal() as db:
        yield db


@pytest.fixture(autouse=True)
def clean_database():
    app.dependency_overrides[get_db] = override_db
    with SessionLocal() as db:
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(table.delete())
        db.commit()
        admission = CANONICAL_CORPUS_ADMISSIONS["TANZIL_QURAN_UTHMANI"]
        db.add(
            models.CorpusSnapshot(
                id=admission.authorized_snapshot_id,
                canonical_text_source=admission.source_id,
                canonical_text_version=admission.canonical_text_version,
                canonical_text_hash=admission.expected_hash,
                validation_status="VALIDATED",
                source_role_status="SOURCE_ROLE_APPROVED",
                artifact_presence_status="ARTIFACT_PRESENT",
                expected_canonical_text_hash=admission.expected_hash,
                hash_verification_status="HASH_VERIFIED",
                import_validation_status="IMPORT_VALIDATED",
                activation_status="PRODUCTION_ACTIVE",
                artifact_provenance=admission.provenance_reference,
                artifact_reference=admission.artifact_reference,
                artifact_size_bytes=admission.expected_bytes,
                artifact_format=admission.artifact_format,
                artifact_verified_at=datetime.now(timezone.utc).replace(tzinfo=None),
                artifact_verification_revision=admission.verification_revision,
                identity_index_reference=admission.identity_index_reference,
                identity_index_sha256=admission.identity_index_sha256,
                verse_count=admission.expected_verse_count,
                canon_001_reconciliation=admission.canon_001_reconciliation,
                fixture_only=False,
            )
        )
        skill = Path("skills/lisan-semantic-extraction/SKILL.md")
        digest = hashlib.sha256(skill.read_bytes()).hexdigest()
        db.add(
            models.MethodologyRevision(
                id="method-current",
                methodology_id="LISAN_QURANIC_SEMANTIC_EXTRACTION",
                revision=f"skill-sha256:{digest[:12]}",
                lifecycle_state="CURRENT",
                authority_reference="SIMPLIFIED_AI_AUTHORITY_AND_GOVERNANCE_CONTRACT.md",
                source_reference=skill.as_posix(),
                source_sha256=digest,
                allowed_use="QURAN_INTERNAL_CUMULATIVE_RUN",
                research_run_eligible=True,
            )
        )
        db.add_all(
            models.CorpusOccurrence(
                id=f"occ-{index}",
                snapshot_id=admission.authorized_snapshot_id,
                expression="كتب",
                verse_ref=f"2:{index}",
                text=f"نص قرآني اختباري مضبوط {index}",
            )
            for index in range(1, 4)
        )
        # Word-level root-occurrence identity (the governed ROOT_CONCEPT unit).
        db.add_all(
            models.StructuralToken(
                id=f"stok-katb-{index}",
                snapshot_id=admission.authorized_snapshot_id,
                word_ref=f"2:{index}:1:1",
                verse_ref=f"2:{index}",
                root="كتب",
                form="N",
                pos_tag="N",
                source_id="TEST_STRUCTURAL_FIXTURE",
                source_version="test",
                extraction_version="test-fixture-v1",
                attribution_status="CONFIRMED",
            )
            for index in range(1, 4)
        )
        db.commit()
    yield
    app.dependency_overrides.clear()


# --------------------------------------------------------------------------- #
# Shared runtime helpers (mirror the governance suite).
# --------------------------------------------------------------------------- #
def create_run(expression: str, contract: str) -> str:
    response = client.post(
        "/runs", json={"target_contract": contract, "target_expression": expression}
    )
    assert response.status_code == 200, response.text
    run_id = response.json()["id"]
    preflight = client.post(f"/runs/{run_id}/blind/preflight")
    assert preflight.status_code == 200, preflight.text
    return run_id


def add_observation(run_id: str, occurrence_id: str) -> str:
    response = client.post(
        f"/runs/{run_id}/observations",
        json={"occurrence_ref": occurrence_id, "form": "FORM", "syntax": "SYN"},
    )
    assert response.status_code == 200, response.text
    return response.json()["id"]


def rejection_condition() -> dict[str, str]:
    return {
        "challenging_finding": "موضع صحيح لا يفسره الحكم",
        "search_location": "كل مواضع النطاق",
        "verification_method": "مقارنة التنبؤ بالدليل المستقل",
        "confounder_control": "طرح أثر الصيغة والتركيب والسياق",
        "failure_consequence": "رفض الحكم أو تضييق نطاقه",
    }


def preferred_root_payload(evidence_refs, *, strength="STRONG", unresolved=None):
    return {
        "contract_type": "ROOT_CONCEPT",
        "research_state": "PREFERRED",
        "claim_scope": "UNIVERSAL",
        "sampling_basis": None,
        "result_strength": strength,
        "preferred_conclusion": "ترجيح جذري قابل للدحض",
        "root_concept": "مساهمة الجذر المجردة",
        "plain_explanation": "شرح عربي مباشر",
        "semantic_boundary": "لا يحمل أثر الصيغة أو السياق على الجذر",
        "layer_attribution": {"root": "مساهمة الجذر"},
        "supporting_evidence_refs": evidence_refs,
        "counterevidence_refs": [],
        "unresolved_cases": unresolved or [],
        "hard_cases": ["أصعب موضع مسجل"],
        "strongest_counterexample": "أقوى مثال مضاد",
        "strongest_competitor": "أقوى بديل منافس",
        "rejection_condition": rejection_condition(),
        "falsification_status": "PASSED",
        "reopen_conditions": ["دليل جوهري جديد"],
    }


# --------------------------------------------------------------------------- #
# 1-3  Descriptive Knowledge Foundation (Root Descriptive Profile).
# --------------------------------------------------------------------------- #
def _slm_tokens(include_disputed: bool = False) -> list[StructuralToken]:
    """A deterministic structural-annotation fixture for root 'س ل م'."""
    tokens = [
        StructuralToken("2:233:53", "2:233", "س ل م", "FORM_II_VERB"),
        StructuralToken("4:65:18", "4:65", "س ل م", "FORM_II_VERB"),
        StructuralToken("2:112:3", "2:112", "س ل م", "FORM_IV_VERB"),
        StructuralToken("6:14:7", "6:14", "س ل م", "NOUN"),
        # a different root must never leak into the profile:
        StructuralToken("2:255:1", "2:255", "ع ل م", "NOUN"),
    ]
    if include_disputed:
        tokens.append(
            StructuralToken(
                "27:44:20", "27:44", "س ل م", "NOUN", attribution_status=ATTR_DISPUTED
            )
        )
    return tokens


def test_1_direct_textual_facts_are_not_model_generated():
    profile = RootDescriptiveProfileService.build(
        "س ل م",
        _slm_tokens(),
        source_id="QAC_MORPHOLOGY_WEB_V0_4_FIXTURE",
        source_version="v0.4",
        extraction_version="slm-fixture-v1",
    )
    # The extraction is pure deterministic aggregation, explicitly not an LLM.
    assert profile.extraction_method == EXTRACTION_METHOD
    assert "NO_LLM" in profile.extraction_method
    # Root-scoped locations/counts are reviewable structural annotations (their
    # membership depends on root attribution), never mislabelled direct facts.
    assert profile.knowledge_levels["occurrence_refs"] == (
        KnowledgeLevel.QUALIFIED_STRUCTURAL_ANNOTATION.value
    )
    assert profile.knowledge_levels["surah_distribution"] == (
        KnowledgeLevel.QUALIFIED_STRUCTURAL_ANNOTATION.value
    )
    # The profile is meaning-free: it exposes no semantic-conclusion field.
    assert not hasattr(profile, "root_concept")
    assert not hasattr(profile, "meaning")
    # The service module must not depend on any AI provider/runtime.
    import backend.domain.services.corpus.descriptive_profile as mod

    source = Path(mod.__file__).read_text(encoding="utf-8")
    assert "ai_provider" not in source and "pydantic_ai" not in source


def test_2_deterministic_counts_are_reproducible():
    first = RootDescriptiveProfileService.build("س ل م", _slm_tokens())
    second = RootDescriptiveProfileService.build("س ل م", _slm_tokens())
    # Byte-for-byte identical aggregation on repeat.
    assert first.as_dict() == second.as_dict()
    # Hand-computed expected counts (the foreign root is excluded).
    assert first.total_confirmed_occurrences == 4
    assert first.occurrence_refs == ("2:112:3", "2:233:53", "4:65:18", "6:14:7")
    assert first.surah_distribution == {"2": 2, "4": 1, "6": 1}
    forms = {f.form: f.count for f in first.forms}
    assert forms == {"FORM_II_VERB": 2, "FORM_IV_VERB": 1, "NOUN": 1}
    assert set(first.singleton_forms) == {"FORM_IV_VERB", "NOUN"}


def test_3_structural_uncertainty_is_preserved():
    profile = RootDescriptiveProfileService.build("س ل م", _slm_tokens(include_disputed=True))
    # The disputed attribution is surfaced, not silently counted as a fact.
    assert profile.total_confirmed_occurrences == 4
    assert profile.total_eligible_occurrences == 5
    refs = {d["word_ref"] for d in profile.disputed_annotations}
    assert refs == {"27:44:20"}
    assert "27:44:20" not in profile.occurrence_refs
    # Root/form attribution is a reviewable structural annotation, not a fact.
    assert profile.knowledge_levels["root"] == (
        KnowledgeLevel.QUALIFIED_STRUCTURAL_ANNOTATION.value
    )
    assert profile.knowledge_levels["forms"] == (
        KnowledgeLevel.QUALIFIED_STRUCTURAL_ANNOTATION.value
    )
    assert profile.knowledge_levels["disputed_annotations"] == (
        KnowledgeLevel.DISPUTED_STRUCTURAL_ANNOTATION.value
    )


# --------------------------------------------------------------------------- #
# 4-5  Root semantic unity / universal presence.
# --------------------------------------------------------------------------- #
def test_4_one_unexplained_occurrence_blocks_accepted_root_wide_concept():
    run_id = create_run("كتب", "ROOT_CONCEPT")
    # Word-level coverage: cite all three confirmed StructuralToken word_refs.
    evidence = [f"token:2:{i}:1:1" for i in range(1, 4)]
    # Fully covered UNIVERSAL root concept, but one occurrence stays unexplained.
    judgment = client.post(
        f"/runs/{run_id}/judgments",
        json=preferred_root_payload(evidence, unresolved=["الموضع 2:3 لم يُفسَّر بعد"]),
    )
    assert judgment.status_code == 200, judgment.text
    claim_id = judgment.json()["id"]
    assert judgment.json()["research_completeness"]["sufficient_for_claim"] is True

    verification = client.post(
        f"/judgments/{claim_id}/verification",
        json={
            "decision": "VERIFIED",
            "verification_type": "INDEPENDENT",
            "rationale": "تحقق مستقل",
            "evidence_refs": evidence,
        },
    )
    assert verification.status_code == 200, verification.text

    blocked = client.post(
        f"/judgments/{claim_id}/canonicalize", json={"rationale": "قرار مالك"}
    )
    assert blocked.status_code == 403
    assert "root semantic unity" in blocked.text
    # And it stays non-canonical.
    assert client.get(f"/judgments/{claim_id}").json()["canonical_state"] == "NOT_CANONICAL"


def test_4b_confirmed_counterexample_occurrence_blocks_universal_root_concept():
    # Phase 0B remediation: a confirmed occurrence recorded as counterevidence is
    # an occurrence the concept fails to explain; it must block acceptance and
    # must NOT count toward universal coverage.
    run_id = create_run("كتب", "ROOT_CONCEPT")
    supporting = [f"token:2:{i}:1:1" for i in (1, 2)]
    payload = preferred_root_payload(supporting)
    # 2:3:1:1 is a confirmed eligible word occurrence that opposes the concept.
    payload["counterevidence_refs"] = ["token:2:3:1:1"]
    resp = client.post(f"/runs/{run_id}/judgments", json=payload)
    # Coverage is derived from supporting evidence only, so occ-3 is missing ->
    # a universal claim cannot even be PREFERRED on 2-of-3 support.
    assert resp.status_code == 422
    assert "coverage is insufficient" in resp.text


def test_5_no_majority_threshold_bypasses_universal_presence():
    run_id = create_run("كتب", "ROOT_CONCEPT")
    # Majority coverage (2 of 3 eligible occurrences) must still fail a UNIVERSAL claim.
    evidence = [f"token:2:{i}:1:1" for i in range(1, 3)]
    response = client.post(
        f"/runs/{run_id}/judgments", json=preferred_root_payload(evidence)
    )
    assert response.status_code == 422
    assert "coverage is insufficient" in response.text
    # There is no percentage/threshold escape hatch in the judgment contract.
    from backend.domain.schemas import ResearchJudgmentCreate

    fields = ResearchJudgmentCreate.model_fields.keys()
    assert not any(
        token in name for name in fields for token in ("threshold", "percent", "majority")
    )


# --------------------------------------------------------------------------- #
# 6-7  External source / external hypothesis isolation.
# --------------------------------------------------------------------------- #
def test_6_external_source_claim_cannot_become_semantic_authority():
    run_id = create_run("كتب", "ROOT_CONCEPT")
    response = client.get(f"/runs/{run_id}/read_semantic_dictionary")
    assert response.status_code == 403
    assert "secret semantic definition" not in response.text
    with SessionLocal() as db:
        event = db.query(models.IsolationEvent).one()
        assert event.was_blocked is True
        assert event.attempted_action == "READ_PROHIBITED_EXTERNAL_SEMANTIC_SOURCE"
        assert db.query(models.IsolationState).one().is_contaminated == "CLEAN"


def test_7_external_hypothesis_cannot_masquerade_as_blind_internal():
    run_id = create_run("كتب", "ROOT_CONCEPT")

    def make(origin: str | None):
        payload = {
            "hypothesis_type": "H_JABAL" if origin == "EXTERNAL_CANDIDATE" else "H1",
            "target_contract": "ROOT_CONCEPT",
            "scope": "UNIVERSAL",
            "statement": "المعنى المحوري المنقول" if origin else "استقراء داخلي",
            "supporting_evidence_refs": [],
            "counterevidence_refs": [],
            "unresolved_cases": [],
            "rejection_condition": rejection_condition(),
            "provenance": "محمد حسن جبل" if origin else "BLIND_INTERNAL",
        }
        if origin is not None:
            payload["origin"] = origin
        return client.post(f"/runs/{run_id}/hypotheses", json=payload)

    external = make("EXTERNAL_CANDIDATE")
    assert external.status_code == 200, external.text
    assert external.json()["origin"] == "EXTERNAL_CANDIDATE"

    # Default origin is internal derivation; nothing is silently relabelled.
    internal = make(None)
    assert internal.status_code == 200, internal.text
    assert internal.json()["origin"] == "INDEPENDENT_INTERNAL_DERIVATION"

    # A hypothesis (external or not) has no canonical/acceptance transition and no
    # confidence field: an external candidate can never become project authority.
    assert "canonicalize" not in str(app.openapi()["paths"].get("/hypotheses/{hyp_id}", {}))
    assert not any(
        key in external.json() for key in ("confidence", "confidence_bonus", "canonical_state")
    )
    # An illegal origin value is rejected, not coerced to internal.
    bad = client.post(
        f"/runs/{run_id}/hypotheses",
        json={
            "hypothesis_type": "H1",
            "origin": "BLIND_INTERNAL_DISGUISE",
            "target_contract": "ROOT_CONCEPT",
            "scope": "UNIVERSAL",
            "statement": "x",
            "supporting_evidence_refs": [],
            "counterevidence_refs": [],
            "unresolved_cases": [],
            "rejection_condition": rejection_condition(),
            "provenance": "external",
        },
    )
    assert bad.status_code == 422


def test_7b_hypothesis_origin_is_write_once():
    # Phase 0B remediation: a persisted external candidate cannot be relabelled.
    run_id = create_run("كتب", "ROOT_CONCEPT")
    external = client.post(
        f"/runs/{run_id}/hypotheses",
        json={
            "hypothesis_type": "H_JABAL",
            "origin": "EXTERNAL_CANDIDATE",
            "target_contract": "ROOT_CONCEPT",
            "scope": "UNIVERSAL",
            "statement": "external",
            "supporting_evidence_refs": [],
            "counterevidence_refs": [],
            "unresolved_cases": [],
            "rejection_condition": rejection_condition(),
            "provenance": "جبل",
        },
    )
    hyp_id = external.json()["id"]
    with SessionLocal() as db:
        hyp = db.get(models.Hypothesis, hyp_id)
        hyp.origin = "INDEPENDENT_INTERNAL_DERIVATION"
        with pytest.raises(ValueError, match="write-once"):
            db.flush()
        db.rollback()


def test_7c_external_hypothesis_excluded_from_blind_internal_context():
    # Phase 0B remediation: external-origin hypotheses must not enter the blind
    # internal-induction context (else they masquerade as internal discovery).
    from backend.domain.services.ai_context import AIContextBuilder

    run_id = create_run("كتب", "ROOT_CONCEPT")
    for origin, statement in (
        ("INDEPENDENT_INTERNAL_DERIVATION", "internal induction"),
        ("EXTERNAL_CANDIDATE", "Jabal central meaning"),
    ):
        client.post(
            f"/runs/{run_id}/hypotheses",
            json={
                "hypothesis_type": "H1",
                "origin": origin,
                "target_contract": "ROOT_CONCEPT",
                "scope": "UNIVERSAL",
                "statement": statement,
                "supporting_evidence_refs": [],
                "counterevidence_refs": [],
                "unresolved_cases": [],
                "rejection_condition": rejection_condition(),
                "provenance": origin,
            },
        )
    with SessionLocal() as db:
        context = AIContextBuilder.build_research_context(db, run_id)
    statements = {h["statement"] for h in context["active_hypotheses"]}
    origins = {h["origin"] for h in context["active_hypotheses"]}
    assert statements == {"internal induction"}
    assert origins == {"INDEPENDENT_INTERNAL_DERIVATION"}


# --------------------------------------------------------------------------- #
# 8  Governed capture: assistant proposal cannot become owner-accepted silently.
# --------------------------------------------------------------------------- #
def test_8_assistant_proposal_cannot_become_owner_accepted_silently():
    rule = client.post(
        "/governance/rules",
        json={"rule_code": "R-ROOT-UNITY", "description": "root semantic unity"},
    )
    assert rule.status_code == 200, rule.text

    # A created proposal is always PROPOSED, even if the caller tries to force APPROVED.
    proposal = client.post(
        "/governance/proposals",
        json={
            "rule_code": "R-ROOT-UNITY",
            "proposed_changes": "tighten wording",
            "status": "APPROVED",
        },
    )
    assert proposal.status_code == 200, proposal.text
    proposal_id = proposal.json()["id"]
    assert proposal.json()["status"] == "PROPOSED"

    # Only the explicit approve endpoint can accept it, and it writes an approval record.
    approved = client.post(f"/governance/proposals/{proposal_id}/approve")
    assert approved.status_code == 200, approved.text
    assert approved.json()["status"] == "APPROVED"
    with SessionLocal() as db:
        # The approval writes a distinct immutable revision (rev 2) beyond the
        # initial creation revision (rev 1); acceptance is never silent.
        approval = (
            db.query(models.RuleRevision)
            .filter(
                models.RuleRevision.rule_code == "R-ROOT-UNITY",
                models.RuleRevision.changes_described == "tighten wording",
            )
            .one()
        )
        assert approval.revision_number == 2
        assert approval.approved_by == "LOCAL_USER"


# --------------------------------------------------------------------------- #
# 9  Canonical / imported content cannot be silently rewritten.
# --------------------------------------------------------------------------- #
def test_9_canonical_preserved_content_is_not_silently_rewritten():
    admission = CANONICAL_CORPUS_ADMISSIONS["TANZIL_QURAN_UTHMANI"]
    # Silently rewriting the admitted canonical text hash is rejected.
    with SessionLocal() as db:
        snapshot = db.get(models.CorpusSnapshot, admission.authorized_snapshot_id)
        assert snapshot is not None
        snapshot.canonical_text_hash = "0" * 64
        with pytest.raises(ValueError, match="does not match the canonical expected hash"):
            db.flush()
        db.rollback()

    # Rewriting admitted provenance metadata in place is rejected outright.
    with SessionLocal() as db:
        snapshot = db.get(models.CorpusSnapshot, admission.authorized_snapshot_id)
        snapshot.artifact_reference = "docs/canonical/FORGED.md"
        with pytest.raises(ValueError, match="not authority-bound"):
            db.flush()
        db.rollback()

    # Methodology revision provenance is immutable (source hash cannot drift).
    with SessionLocal() as db:
        methodology = db.get(models.MethodologyRevision, "method-current")
        methodology.source_sha256 = "f" * 64
        with pytest.raises(ValueError, match="immutable"):
            db.flush()
        db.rollback()
