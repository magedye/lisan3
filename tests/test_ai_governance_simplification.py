import hashlib
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.domain import models, schemas
from backend.domain.services.ai_tools import tool_dispatcher
from backend.domain.services.corpus.authority import CANONICAL_CORPUS_ADMISSIONS
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
        snapshot_id = admission.authorized_snapshot_id
        db.add_all(
            [
                models.CorpusOccurrence(
                    id=f"occ-{index}",
                    snapshot_id=snapshot_id,
                    expression="كتب",
                    verse_ref=f"2:{index}",
                    text=f"نص قرآني اختباري مضبوط {index}",
                )
                for index in range(1, 4)
            ]
            + [
                models.CorpusOccurrence(
                    id="occ-local",
                    snapshot_id=snapshot_id,
                    expression="كتاب",
                    verse_ref="2:4",
                    text="نص قرآني اختباري مضبوط للمفردة",
                ),
                models.CorpusOccurrence(
                    id="occ-verse",
                    snapshot_id=snapshot_id,
                    expression="2:5",
                    verse_ref="2:5",
                    text="نص قرآني اختباري مضبوط للآية",
                ),
                models.CorpusOccurrence(
                    id="occ-difference",
                    snapshot_id=snapshot_id,
                    expression="كتب|خط",
                    verse_ref="2:6",
                    text="نص قرآني اختباري مضبوط للمقارنة",
                ),
            ]
        )
        # Word-level root-occurrence identity for ROOT_CONCEPT research. The
        # governed root-occurrence unit is the confirmed StructuralToken word_ref
        # (from admitted morphology), NOT the verse-level CorpusOccurrence.
        db.add_all(
            [
                models.StructuralToken(
                    id=f"stok-katb-{index}",
                    snapshot_id=snapshot_id,
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
            ]
        )
        db.commit()
    yield
    app.dependency_overrides.clear()


def create_run(expression: str, contract: str) -> str:
    response = client.post(
        "/runs", json={"target_contract": contract, "target_expression": expression}
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["corpus_snapshot"] == "snap_tanzil_1_1_ac0724796cbb"
    assert body["methodology_revision"] == "method-current"
    assert body["authority_context"]["resolved_by"] == "ResearchRunAdmissionPolicy"
    preflight = client.post(f"/runs/{body['id']}/blind/preflight")
    assert preflight.status_code == 200, preflight.text
    assert preflight.json()["allowed_sources"] == [
        "ADMITTED_CANONICAL_QURAN",
        "SAME_RUN_ARTIFACTS",
    ]
    return body["id"]


def add_observation(run_id: str, occurrence_id: str) -> str:
    response = client.post(
        f"/runs/{run_id}/observations",
        json={
            "occurrence_ref": occurrence_id,
            "form": "FORM",
            "syntax": "SYNTAX",
            "local_context": "CONTEXT",
        },
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


def preferred_payload(
    contract: str,
    evidence_refs: list[str],
    layers: dict[str, str],
    *,
    scope: str = "LOCAL",
    strength: str = "MODERATE",
) -> dict:
    return {
        "contract_type": contract,
        "research_state": "PREFERRED",
        "claim_scope": scope,
        "sampling_basis": "عينة تغطي الأنماط المسجلة" if scope == "REPRESENTATIVE" else None,
        "result_strength": strength,
        "preferred_conclusion": "ترجيح دلالي مضبوط قابل للدحض",
        "root_concept": "مفهوم جذري اختباري" if contract == "ROOT_CONCEPT" else None,
        "plain_explanation": "شرح عربي مباشر",
        "semantic_boundary": "لا يحمل أثر الصيغة أو السياق على الجذر",
        "layer_attribution": layers,
        "supporting_evidence_refs": evidence_refs,
        "counterevidence_refs": [],
        "unresolved_cases": [],
        "hard_cases": ["أصعب موضع مسجل"],
        "strongest_counterexample": "أقوى مثال مضاد اختباري",
        "strongest_competitor": "أقوى بديل منافس",
        "rejection_condition": rejection_condition(),
        "falsification_status": "PASSED",
        "reopen_conditions": ["دليل جوهري جديد"],
    }


@pytest.mark.parametrize(
    ("expression", "contract", "occurrence", "layers"),
    [
        ("كتاب", "LEXEME", "occ-local", {"root": "كتب", "lexeme": "كتاب"}),
        (
            "كتاب",
            "LOCAL_MEANING",
            "occ-local",
            {
                "root": "كتب",
                "lexeme": "كتاب",
                "form": "اسم",
                "construction": "تركيب الموضع",
                "context": "سياق الموضع",
                "local_meaning": "المعنى هنا",
            },
        ),
        (
            "2:5",
            "VERSE_MEANING",
            "occ-verse",
            {
                "construction": "العلاقات",
                "context": "السياق الخطابي",
                "final_statement": "البيان النهائي",
            },
        ),
        (
            "كتب|خط",
            "SEMANTIC_DIFFERENCE",
            "occ-difference",
            {"lexeme": "المجال المشترك", "semantic_boundary": "الفارق"},
        ),
    ],
)
def test_ai_research_freedom_across_semantic_question_types(
    expression, contract, occurrence, layers
):
    run_id = create_run(expression, contract)
    observation_id = add_observation(run_id, occurrence)
    response = client.post(
        f"/runs/{run_id}/judgments",
        json=preferred_payload(contract, [f"observation:{observation_id}"], layers),
    )
    assert response.status_code == 200, response.text
    assert response.json()["research_state"] == "PREFERRED"
    assert response.json()["canonical_state"] == "NOT_CANONICAL"
    assert response.json()["research_completeness"]["sufficient_for_claim"] is True


def test_unresolved_is_valid_without_canonical_cost():
    run_id = create_run("كتب", "ROOT_CONCEPT")
    response = client.post(
        f"/runs/{run_id}/judgments",
        json={
            "contract_type": "ROOT_CONCEPT",
            "research_state": "UNRESOLVED",
            "claim_scope": "UNIVERSAL",
            "result_strength": "UNRESOLVED",
            "unresolved_cases": ["الأدلة لا تميز بين بديلين"],
        },
    )
    assert response.status_code == 200, response.text
    assert response.json()["research_state"] == "UNRESOLVED"
    assert response.json()["verification_state"] == "NOT_REQUIRED"


def test_external_source_is_blocked_by_runtime_and_not_disclosed():
    run_id = create_run("كتب", "ROOT_CONCEPT")
    response = client.get(f"/runs/{run_id}/read_semantic_dictionary")
    assert response.status_code == 403
    assert "secret semantic definition" not in response.text
    with SessionLocal() as db:
        event = db.query(models.IsolationEvent).one()
        assert event.was_blocked is True
        assert event.attempted_action == "READ_PROHIBITED_EXTERNAL_SEMANTIC_SOURCE"
        assert db.query(models.IsolationState).one().is_contaminated == "CLEAN"


def test_falsification_and_incomplete_universal_coverage_fail_deterministically():
    run_id = create_run("كتب", "ROOT_CONCEPT")
    observation_id = add_observation(run_id, "occ-1")
    payload = preferred_payload(
        "ROOT_CONCEPT",
        [f"observation:{observation_id}"],
        {"root": "كتب"},
        scope="UNIVERSAL",
    )
    payload["falsification_status"] = "NOT_RUN"
    response = client.post(f"/runs/{run_id}/judgments", json=payload)
    assert response.status_code == 422
    assert "coverage is insufficient" in response.text
    assert "passed falsification" in response.text


def test_missing_or_cross_run_evidence_cannot_be_invented():
    run_id = create_run("كتاب", "LEXEME")
    response = client.post(
        f"/runs/{run_id}/judgments",
        json=preferred_payload(
            "LEXEME", ["observation:does-not-exist"], {"root": "كتب", "lexeme": "كتاب"}
        ),
    )
    assert response.status_code == 422
    assert "absent or cross-run" in response.text


def test_strong_root_canonicalization_memory_and_new_evidence_reopen():
    run_id = create_run("كتب", "ROOT_CONCEPT")
    # ROOT_CONCEPT coverage is word-level: cite the confirmed StructuralToken
    # word_refs via the `token:` evidence bridge. A UNIVERSAL root claim requires
    # every confirmed word occurrence to be supported.
    evidence_refs = [f"token:2:{index}:1:1" for index in range(1, 4)]
    judgment_response = client.post(
        f"/runs/{run_id}/judgments",
        json=preferred_payload(
            "ROOT_CONCEPT",
            evidence_refs,
            {"root": "مساهمة الجذر المجردة"},
            scope="UNIVERSAL",
            strength="STRONG",
        ),
    )
    assert judgment_response.status_code == 200, judgment_response.text
    claim_id = judgment_response.json()["id"]
    premature = client.post(
        f"/judgments/{claim_id}/canonicalize", json={"rationale": "قرار مالك"}
    )
    assert premature.status_code == 403
    assert "verification" in premature.text.lower()

    verification = client.post(
        f"/judgments/{claim_id}/verification",
        json={
            "decision": "VERIFIED",
            "verification_type": "INDEPENDENT",
            "rationale": "تحقق مستقل من النسخة الحالية",
            "evidence_refs": evidence_refs,
        },
    )
    assert verification.status_code == 200, verification.text
    accepted = client.post(
        f"/judgments/{claim_id}/canonicalize",
        json={"rationale": "اعتماد صريح ضمن سلطة المشروع"},
    )
    assert accepted.status_code == 200, accepted.text
    assert accepted.json()["canonical_state"] == "ACCEPTED"
    assert accepted.json()["accepted_at"] is not None

    recalled = client.post(
        "/ask", json={"expression": "كتب", "contract_type": "ROOT_CONCEPT"}
    )
    assert recalled.status_code == 200
    assert recalled.json()["status"] == "ACCEPTED_RESULT"
    assert recalled.json()["claim"]["id"] == claim_id

    new_run = create_run("كتب", "ROOT_CONCEPT")
    add_observation(new_run, "occ-1")
    reopened = client.get(f"/judgments/{claim_id}")
    assert reopened.status_code == 200
    assert reopened.json()["canonical_state"] == "REOPEN_REQUIRED"
    recalled_after = client.post(
        "/ask", json={"expression": "كتب", "contract_type": "ROOT_CONCEPT"}
    )
    assert recalled_after.json()["status"] != "ACCEPTED_RESULT"


def test_unavailable_diagnostics_and_tools_are_honest_non_gates():
    run_id = create_run("كتاب", "LEXEME")
    observation_id = add_observation(run_id, "occ-local")
    response = client.post(
        f"/runs/{run_id}/judgments",
        json=preferred_payload(
            "LEXEME", [f"observation:{observation_id}"], {"root": "كتب", "lexeme": "كتاب"}
        ),
    )
    claim_id = response.json()["id"]
    diagnostics = client.get(f"/judgments/{claim_id}/diagnostics")
    assert diagnostics.status_code == 200
    assert len(
        [item for item in diagnostics.json()["findings"] if item["status"] == "NOT_EVALUATED"]
    ) == 8
    assert diagnostics.json()["hard_blockers"] == []
    assert tool_dispatcher.get_available_tools() == {}
    assert "/runs/{run_id}/gates" not in app.openapi()["paths"]


def test_ai_runtime_can_persist_judgment_but_has_no_acceptance_transition(monkeypatch):
    run_id = create_run("كتاب", "LEXEME")
    observation_id = add_observation(run_id, "occ-local")
    output = schemas.ResearchJudgmentCreate.model_validate(
        preferred_payload(
            "LEXEME", [f"observation:{observation_id}"], {"root": "كتب", "lexeme": "كتاب"}
        )
    )

    class FakeAgent:
        def __init__(self, _model, output_type):
            assert output_type is schemas.ResearchJudgmentCreate

        def run_sync(self, _prompt):
            return SimpleNamespace(output=output)

    monkeypatch.setattr("backend.main.Agent", FakeAgent)
    response = client.post(f"/runs/{run_id}/ai/research-judgment")
    assert response.status_code == 200, response.text
    assert response.json()["status"] == "CREATED"
    assert response.json()["judgment"]["canonical_state"] == "NOT_CANONICAL"
    assert response.json()["trace"]["tools_available"] == []
    assert all("canonicalize" not in path for path in app.openapi()["paths"] if "/ai/" in path)
