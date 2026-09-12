"""Canonical Runtime Qualification — governed word-level pipeline + controls.

Covers the tracks that make the DB-native governed research path genuinely usable:

* Track F — the word_ref <-> StructuralToken evidence bridge and its negatives;
* Track G — host-derived word-level completeness (no imported "COMPLETE" string);
* Track I — canonicalization governance negative controls + unauthorized actor;
* the non-semantic end-to-end pipeline smoke test on a SYNTHETIC root.

The smoke/fixture root is deliberately NOT one of the five production roots and
all state lives in an ephemeral in-memory DB — never lisanapp.db, never a real
SemanticClaim for a production root.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.domain import models
from backend.domain.services.canonicalization import CanonicalizationPolicy
from backend.domain.services.research_coverage import confirmed_word_refs
from backend.domain.services.research_judgment import (
    derive_completeness,
    resolve_evidence_refs,
)
from backend.infrastructure.database import Base, get_db
from backend.main import app
from tests.governed_baseline import (
    AUTHORIZED_TANZIL_SNAPSHOT,
    seed_current_methodology,
    seed_production_valid_tanzil_snapshot,
    seed_structural_tokens,
)

PRODUCTION_ROOTS = {"ESw", "dnw", "flH", "fwh", "glm"}
SMOKE_ROOT = "ZZQ"  # synthetic; provably not a production root
OTHER_ROOT = "QQZ"  # a different synthetic root (wrong-root negative)
SMOKE_WORD_REFS = ["20:1:1:1", "20:2:1:1", "20:3:1:1"]
DISPUTED_WORD_REF = "20:4:1:1"
OTHER_ROOT_WORD_REF = "20:5:1:1"
SECOND_SNAPSHOT = "snap_other_fixture"

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
def governed_db():
    assert SMOKE_ROOT not in PRODUCTION_ROOTS  # guard: never a production root
    app.dependency_overrides[get_db] = override_db
    with SessionLocal() as db:
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(table.delete())
        db.commit()
        seed_production_valid_tanzil_snapshot(db)
        seed_current_methodology(db)
        # Word-level occurrence identity for the synthetic smoke root.
        seed_structural_tokens(db, AUTHORIZED_TANZIL_SNAPSHOT, SMOKE_ROOT, SMOKE_WORD_REFS)
        # A DISPUTED (non-confirmed) occurrence of the same root.
        seed_structural_tokens(
            db,
            AUTHORIZED_TANZIL_SNAPSHOT,
            SMOKE_ROOT,
            [DISPUTED_WORD_REF],
            attribution_status="DISPUTED",
        )
        # A confirmed occurrence of a DIFFERENT root (wrong-root negative).
        seed_structural_tokens(
            db, AUTHORIZED_TANZIL_SNAPSHOT, OTHER_ROOT, [OTHER_ROOT_WORD_REF]
        )
        # A token that only exists under a DIFFERENT snapshot (wrong-snapshot negative).
        db.add(
            models.CorpusSnapshot(
                id=SECOND_SNAPSHOT,
                canonical_text_source="TANZIL_QURAN_UTHMANI",
                canonical_text_version="other",
                canonical_text_hash="0" * 64,
            )
        )
        db.commit()
        seed_structural_tokens(db, SECOND_SNAPSHOT, SMOKE_ROOT, ["99:9:9:9"])
    yield
    app.dependency_overrides.clear()


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def make_run(expression: str = SMOKE_ROOT, contract: str = "ROOT_CONCEPT") -> str:
    resp = client.post(
        "/runs", json={"target_contract": contract, "target_expression": expression}
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["corpus_snapshot"] == AUTHORIZED_TANZIL_SNAPSHOT
    pre = client.post(f"/runs/{body['id']}/blind/preflight")
    assert pre.status_code == 200, pre.text
    assert pre.json()["establishment_status"] == "ESTABLISHED"
    assert pre.json()["is_contaminated"] == "CLEAN"
    return body["id"]


def _rejection_condition() -> dict[str, str]:
    return {
        "challenging_finding": "a concrete falsifier",
        "search_location": "all occurrences",
        "verification_method": "structural comparison",
        "confounder_control": "subtract form/construction/context",
        "failure_consequence": "reject or narrow the judgment",
    }


def root_payload(evidence_refs: list[str], *, counter: list[str] | None = None) -> dict:
    return {
        "contract_type": "ROOT_CONCEPT",
        "research_state": "PREFERRED",
        "claim_scope": "UNIVERSAL",
        "sampling_basis": None,
        "result_strength": "STRONG",
        "preferred_conclusion": "a falsifiable abstract root contribution",
        "root_concept": "synthetic abstract root contribution",
        "plain_explanation": "plain explanation",
        "semantic_boundary": "carries no form/context effect on the root",
        "layer_attribution": {"root": "the root contribution"},
        "supporting_evidence_refs": evidence_refs,
        "counterevidence_refs": counter or [],
        "unresolved_cases": [],
        "hard_cases": ["the hardest recorded occurrence"],
        "strongest_counterexample": "strongest counterexample",
        "strongest_competitor": "strongest competitor",
        "rejection_condition": _rejection_condition(),
        "falsification_status": "PASSED",
        "reopen_conditions": ["material new evidence"],
    }


def build_accepted_ready_claim() -> tuple[str, str]:
    """Full word-level pipeline to a VERIFIED, canonicalization-ready claim."""
    run_id = make_run()
    evidence = [f"token:{wr}" for wr in SMOKE_WORD_REFS]
    judgment = client.post(f"/runs/{run_id}/judgments", json=root_payload(evidence))
    assert judgment.status_code == 200, judgment.text
    assert judgment.json()["research_completeness"]["sufficient_for_claim"] is True
    assert judgment.json()["research_completeness"]["occurrence_unit"] == "word_ref"
    claim_id = judgment.json()["id"]
    verification = client.post(
        f"/judgments/{claim_id}/verification",
        json={
            "decision": "VERIFIED",
            "verification_type": "INDEPENDENT",
            "rationale": "independent verification of the current revision",
            "evidence_refs": evidence,
        },
    )
    assert verification.status_code == 200, verification.text
    return run_id, claim_id


def get_run(db, run_id: str) -> models.ResearchRun:
    return db.get(models.ResearchRun, run_id)


# --------------------------------------------------------------------------- #
# Track F — word_ref <-> StructuralToken evidence bridge
# --------------------------------------------------------------------------- #
def test_token_evidence_resolves_confirmed_word_ref():
    run_id = make_run()
    with SessionLocal() as db:
        run = get_run(db, run_id)
        res = resolve_evidence_refs(db, run, [f"token:{SMOKE_WORD_REFS[0]}"])
        assert res.valid
        assert res.token_word_refs == frozenset({SMOKE_WORD_REFS[0]})


def test_token_evidence_nonexistent_word_ref_fails():
    run_id = make_run()
    with SessionLocal() as db:
        run = get_run(db, run_id)
        res = resolve_evidence_refs(db, run, ["token:20:99:9:9"])
        assert not res.valid
        assert "absent or outside the run corpus" in res.reasons[0]


def test_token_evidence_wrong_root_fails():
    run_id = make_run()
    with SessionLocal() as db:
        run = get_run(db, run_id)
        res = resolve_evidence_refs(db, run, [f"token:{OTHER_ROOT_WORD_REF}"])
        assert not res.valid
        assert "not the run target root" in res.reasons[0]


def test_token_evidence_non_confirmed_attribution_fails():
    run_id = make_run()
    with SessionLocal() as db:
        run = get_run(db, run_id)
        res = resolve_evidence_refs(db, run, [f"token:{DISPUTED_WORD_REF}"])
        assert not res.valid
        assert "not a CONFIRMED structural occurrence" in res.reasons[0]


def test_token_evidence_wrong_snapshot_fails():
    # '99:9:9:9' exists only under SECOND_SNAPSHOT, not the run's snapshot.
    run_id = make_run()
    with SessionLocal() as db:
        run = get_run(db, run_id)
        res = resolve_evidence_refs(db, run, ["token:99:9:9:9"])
        assert not res.valid
        assert "absent or outside the run corpus" in res.reasons[0]


def test_token_evidence_verse_ref_substitution_fails():
    # A verse-level ref can never stand in for a word-level occurrence.
    run_id = make_run()
    with SessionLocal() as db:
        run = get_run(db, run_id)
        res = resolve_evidence_refs(db, run, ["token:20:1"])
        assert not res.valid


def test_external_prefix_evidence_cannot_be_smuggled():
    run_id = make_run()
    with SessionLocal() as db:
        run = get_run(db, run_id)
        for ref in ("tafsir:x", "file:/etc/passwd", "lexicon:root"):
            res = resolve_evidence_refs(db, run, [ref])
            assert not res.valid
            assert "not admissible" in res.reasons[0]


def test_duplicate_token_cannot_substitute_for_missing_coverage():
    # Two copies of one word_ref must not satisfy a 3-occurrence universal claim.
    run_id = make_run()
    dup = [f"token:{SMOKE_WORD_REFS[0]}", f"token:{SMOKE_WORD_REFS[0]}"]
    resp = client.post(f"/runs/{run_id}/judgments", json=root_payload(dup))
    assert resp.status_code == 422
    assert "coverage is insufficient" in resp.text


# --------------------------------------------------------------------------- #
# Track G — host-derived word-level completeness
# --------------------------------------------------------------------------- #
def test_completeness_is_word_level_and_host_derived():
    run_id = make_run()
    with SessionLocal() as db:
        run = get_run(db, run_id)
        eligible = set(confirmed_word_refs(db, run.corpus_snapshot, SMOKE_ROOT))
        assert eligible == set(SMOKE_WORD_REFS)  # DISPUTED + other-root excluded
        full = derive_completeness(
            db, run, "UNIVERSAL", None,
            frozenset(), frozenset(SMOKE_WORD_REFS), "ROOT_CONCEPT",
        )
        assert full["occurrence_unit"] == "word_ref"
        assert full["eligible_occurrence_count"] == 3
        assert full["sufficient_for_claim"] is True
        partial = derive_completeness(
            db, run, "UNIVERSAL", None,
            frozenset(), frozenset(SMOKE_WORD_REFS[:2]), "ROOT_CONCEPT",
        )
        assert partial["sufficient_for_claim"] is False


def test_universal_coverage_requires_every_confirmed_occurrence():
    run_id = make_run()
    partial = [f"token:{wr}" for wr in SMOKE_WORD_REFS[:2]]
    resp = client.post(f"/runs/{run_id}/judgments", json=root_payload(partial))
    assert resp.status_code == 422
    assert "coverage is insufficient" in resp.text


# --------------------------------------------------------------------------- #
# End-to-end non-semantic smoke test (synthetic root, ephemeral DB)
# --------------------------------------------------------------------------- #
def test_nonsemantic_pipeline_smoke_reaches_accepted():
    """production snapshot -> methodology -> run -> established isolation ->
    word-level evidence -> host completeness -> INDEPENDENT verification ->
    judgment validation -> canonicalization. Synthetic root only."""
    run_id, claim_id = build_accepted_ready_claim()
    # Premature canonicalization (before verification would be) is not the case
    # here; verification already recorded, so acceptance should now succeed.
    accepted = client.post(
        f"/judgments/{claim_id}/canonicalize",
        json={"rationale": "explicit trusted-local acceptance (synthetic smoke)"},
    )
    assert accepted.status_code == 200, accepted.text
    assert accepted.json()["canonical_state"] == "ACCEPTED"
    with SessionLocal() as db:
        audits = (
            db.query(models.AuditLog)
            .filter(
                models.AuditLog.entity_id == claim_id,
                models.AuditLog.action == "CANONICALIZE",
            )
            .count()
        )
        assert audits == 1


# --------------------------------------------------------------------------- #
# Track I — governance negative controls (one mutation per test)
# --------------------------------------------------------------------------- #
def _evaluate(db, claim_id: str) -> tuple[bool, tuple[str, ...]]:
    claim = db.get(models.SemanticClaim, claim_id)
    decision = CanonicalizationPolicy.evaluate(db, claim)
    return decision.accepted, decision.reasons


def test_control_happy_path_is_acceptable():
    _, claim_id = build_accepted_ready_claim()
    with SessionLocal() as db:
        accepted, reasons = _evaluate(db, claim_id)
        assert accepted, reasons


def test_control_rejects_non_production_snapshot():
    _, claim_id = build_accepted_ready_claim()
    with SessionLocal() as db:
        snap = db.get(models.CorpusSnapshot, AUTHORIZED_TANZIL_SNAPSHOT)
        snap.validation_status = "UNVERIFIED"
        accepted, reasons = _evaluate(db, claim_id)
        assert not accepted
        assert any("production-valid" in r for r in reasons)


def test_control_rejects_missing_methodology():
    _, claim_id = build_accepted_ready_claim()
    with SessionLocal() as db:
        run = db.get(models.SemanticClaim, claim_id).research_run
        db.delete(db.get(models.MethodologyRevision, run.methodology_revision))
        db.commit()
        accepted, reasons = _evaluate(db, claim_id)
        assert not accepted
        assert any("Methodology" in r for r in reasons)


def test_control_rejects_absent_isolation():
    _, claim_id = build_accepted_ready_claim()
    with SessionLocal() as db:
        run = db.get(models.SemanticClaim, claim_id).research_run
        db.query(models.IsolationState).filter(
            models.IsolationState.research_run_id == run.id
        ).delete()
        db.commit()
        accepted, reasons = _evaluate(db, claim_id)
        assert not accepted
        assert any("isolation is absent or contaminated" in r for r in reasons)


def test_control_rejects_unestablished_isolation():
    _, claim_id = build_accepted_ready_claim()
    with SessionLocal() as db:
        run = db.get(models.SemanticClaim, claim_id).research_run
        iso = (
            db.query(models.IsolationState)
            .filter(models.IsolationState.research_run_id == run.id)
            .one()
        )
        iso.establishment_status = "NOT_ESTABLISHED"  # CLEAN but never established
        db.commit()
        accepted, reasons = _evaluate(db, claim_id)
        assert not accepted
        assert any("never genuinely established" in r for r in reasons)


def test_control_rejects_contaminated_isolation():
    _, claim_id = build_accepted_ready_claim()
    with SessionLocal() as db:
        run = db.get(models.SemanticClaim, claim_id).research_run
        iso = (
            db.query(models.IsolationState)
            .filter(models.IsolationState.research_run_id == run.id)
            .one()
        )
        iso.is_contaminated = "PRIOR_CONTAMINATED"
        db.commit()
        accepted, reasons = _evaluate(db, claim_id)
        assert not accepted
        assert any("isolation is absent or contaminated" in r for r in reasons)


def test_control_rejects_missing_verification():
    _, claim_id = build_accepted_ready_claim()
    with SessionLocal() as db:
        db.query(models.VerificationRecord).filter(
            models.VerificationRecord.claim_id == claim_id
        ).delete()
        db.commit()
        accepted, reasons = _evaluate(db, claim_id)
        assert not accepted
        assert any("verification record is missing" in r for r in reasons)


def test_control_rejects_non_independent_verification():
    _, claim_id = build_accepted_ready_claim()
    with SessionLocal() as db:
        ver = (
            db.query(models.VerificationRecord)
            .filter(models.VerificationRecord.claim_id == claim_id)
            .one()
        )
        ver.verification_type = "SELF"
        db.commit()
        accepted, reasons = _evaluate(db, claim_id)
        assert not accepted
        assert any("not INDEPENDENT" in r for r in reasons)


def test_control_rejects_stale_verification():
    _, claim_id = build_accepted_ready_claim()
    with SessionLocal() as db:
        claim = db.get(models.SemanticClaim, claim_id)
        claim.revision_id = (claim.revision_id or 1) + 1  # bump past the verification
        db.commit()
        accepted, reasons = _evaluate(db, claim_id)
        assert not accepted
        assert any("stale" in r for r in reasons)


def test_control_rejects_ambiguous_corpus_dependency():
    _, claim_id = build_accepted_ready_claim()
    with SessionLocal() as db:
        db.query(models.DependencyRecord).filter(
            models.DependencyRecord.dependent_claim_id == claim_id,
            models.DependencyRecord.dependency_type == "CORPUS_SNAPSHOT",
        ).delete()
        db.commit()
        accepted, reasons = _evaluate(db, claim_id)
        assert not accepted
        assert any("corpus dependency is absent or ambiguous" in r for r in reasons)


def test_control_rejects_confirmed_counterexample_root_unity():
    run_id = make_run()
    evidence = [f"token:{wr}" for wr in SMOKE_WORD_REFS[:2]]
    # All three are supporting AND one is also counterevidence -> full coverage but
    # a confirmed occurrence opposes the concept.
    payload = root_payload(
        [f"token:{wr}" for wr in SMOKE_WORD_REFS],
        counter=[f"token:{SMOKE_WORD_REFS[2]}"],
    )
    resp = client.post(f"/runs/{run_id}/judgments", json=payload)
    assert resp.status_code == 200, resp.text
    claim_id = resp.json()["id"]
    client.post(
        f"/judgments/{claim_id}/verification",
        json={
            "decision": "VERIFIED",
            "verification_type": "INDEPENDENT",
            "rationale": "independent",
            "evidence_refs": evidence,
        },
    )
    with SessionLocal() as db:
        accepted, reasons = _evaluate(db, claim_id)
        assert not accepted
        assert any("root semantic unity" in r for r in reasons)


def test_control_unauthorized_actor_cannot_canonicalize():
    _, claim_id = build_accepted_ready_claim()
    with SessionLocal() as db:
        claim = db.get(models.SemanticClaim, claim_id)
        with pytest.raises(ValueError, match="not authorized"):
            CanonicalizationPolicy.canonicalize(
                db, claim, rationale="attempt", actor="AI_RUNTIME"
            )
        db.refresh(claim)
        assert claim.canonical_state == "NOT_CANONICAL"


def test_control_fixture_contract_cannot_become_canonical():
    # A synthetic fixture run must be refused real acceptance by policy even when
    # every other mechanic passes.
    run_id = make_run(contract="test_fixture_smoke")
    # test_fixture_ is not a word-level ROOT_CONCEPT, so drive via a direct claim
    # bound to the production snapshot to isolate the fixture guard.
    with SessionLocal() as db:
        run = db.get(models.ResearchRun, run_id)
        assert run.target_contract.startswith("test_fixture_")
        # minimal claim object to exercise the fixture guard path
        claim = models.SemanticClaim(
            id="jud_fixture_smoke",
            research_run_id=run.id,
            contract_type="ROOT_CONCEPT",
            research_state="PREFERRED",
            result_strength="STRONG",
            falsification_status="PASSED",
            claim_scope="UNIVERSAL",
            research_completeness={"sufficient_for_claim": True},
            plain_explanation="x",
            semantic_boundary="x",
            strongest_counterexample="x",
            strongest_competitor="x",
            supporting_evidence=[f"token:{SMOKE_WORD_REFS[0]}"],
            hard_cases=["x"],
            reopen_conditions=["x"],
            root_concept="x",
        )
        db.add(claim)
        db.commit()
        accepted, reasons = _evaluate(db, "jud_fixture_smoke")
        assert not accepted
        assert any("fixtures cannot become canonical" in r.lower() for r in reasons)
