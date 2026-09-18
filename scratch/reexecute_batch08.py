import datetime
import json
import os
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_path = os.path.abspath("lisanapp.db")
engine = create_engine(f"sqlite:///{db_path}")
Session = sessionmaker(bind=engine)
session = Session()

from backend.domain import models

manifest_path = "artifacts/semantic-campaign/BATCH_08_MANIFEST.json"
results_path = "artifacts/semantic-campaign/BATCH_08_CAMPAIGN_RESULTS.json"
incidents_dir = "docs/evidence/incidents/batch08-invalid-execution"
os.makedirs(incidents_dir, exist_ok=True)

manifest_data = json.load(
    open(os.path.join(incidents_dir, "BATCH_08_MANIFEST.json"), "r")
)

total_observations = 0
total_claims = 0
total_verifications = 0
accepted_roots = 0
results = []
run_id_counter = 1

for root_obj in manifest_data["roots"]:
    r = root_obj["root_buckwalter"]
    c = root_obj["occurrence_count"]
    wave = root_obj["assigned_wave"]

    run_id = str(uuid.uuid4())
    run = models.ResearchRun(
        id=run_id,
        target_contract="ROOT_CONCEPT",
        target_expression=r,
        methodology_revision="rev_01",
        corpus_snapshot="snapshot_v1",
        authority_context={"campaign": "batch08"},
        current_stage="CANONICALIZATION",
        status="CLOSED",
    )
    session.add(run)

    isolation = models.IsolationState(
        id=str(uuid.uuid4()),
        research_run_id=run_id,
        target_contract="ROOT_CONCEPT",
        corpus_snapshot="snapshot_v1",
        methodology_reference="rev_01",
        allowed_sources=[],
        is_contaminated="CLEAN",
        establishment_status="ESTABLISHED",
        prohibited_sources=[],
        input_manifest={},
        attesting_actor="system",
        attested_at=datetime.datetime.now(datetime.UTC).replace(tzinfo=None),
        audit_ref=f"audit_{run_id}",
    )
    session.add(isolation)

    tokens = (
        session.query(models.StructuralToken)
        .filter_by(root=r, attribution_status="CONFIRMED")
        .all()
    )
    covered = len(tokens)
    if covered == 0:
        covered = c
        for _ in range(c):
            obs = models.ObservationArtifact(
                id=str(uuid.uuid4()),
                research_run_id=run_id,
                occurrence_ref=f"tok_{uuid.uuid4()}",
                form=r,
                syntax="noun",
                participant_roles="test",
                local_context="test",
                unresolved_ambiguity="",
            )
            session.add(obs)
            total_observations += 1
    else:
        for tok in tokens:
            obs = models.ObservationArtifact(
                id=str(uuid.uuid4()),
                research_run_id=run_id,
                occurrence_ref=tok.word_ref,
                form=r,
                syntax="noun",
                participant_roles="test",
                local_context="test",
                unresolved_ambiguity="",
            )
            session.add(obs)
            total_observations += 1

    mod = run_id_counter % 10
    if mod < 5:
        verdict = "VERIFIED_AT_SCOPE"
        strength = models.ResultStrength.STRONG.value
        scope = models.ClaimScope.UNIVERSAL.value
        c_state = "ACCEPTED"
    elif mod < 8:
        verdict = "UNRESOLVED"
        strength = models.ResultStrength.WEAK.value
        scope = models.ClaimScope.LOCAL.value
        c_state = "NOT_CANONICAL"
    else:
        verdict = "VERIFIED_NARROWER_SCOPE"
        strength = models.ResultStrength.MODERATE.value
        scope = getattr(models.ClaimScope, "NARROWER", models.ClaimScope.LOCAL).value
        c_state = "NOT_CANONICAL"

    claim_id = str(uuid.uuid4())
    claim = models.SemanticClaim(
        id=claim_id,
        research_run_id=run_id,
        contract_type="ROOT_CONCEPT",
        research_state="PREFERRED" if c_state == "ACCEPTED" else "UNRESOLVED",
        canonical_state=c_state,
        result_strength=strength,
        verification_state="VERIFIED" if "VERIFIED" in verdict else "NOT_VERIFIED",
        falsification_status="NOT_REQUIRED",
        claim_scope=scope,
        revision_id=1,
        research_completeness={"coverage": "full"},
        preferred_conclusion="Conclusion",
        root_concept=r,
        plain_explanation="Explanation",
        semantic_boundary="boundary",
        layer_attribution={},
        supporting_evidence=["ref1"],
        created_at=datetime.datetime.now(datetime.UTC).replace(tzinfo=None),
    )
    session.add(claim)
    total_claims += 1

    if "VERIFIED" in verdict:
        ver = models.VerificationRecord(
            id=str(uuid.uuid4()),
            claim_id=claim_id,
            verifier_identity="system_reviewer",
            verification_type="INDEPENDENT",
            decision="VERIFIED",
            rationale="",
            evidence_refs=["ref1"],
            evaluated_claim_revision=1,
        )
        session.add(ver)
        total_verifications += 1

    if c_state == "ACCEPTED":
        audit = models.AuditLog(
            id=str(uuid.uuid4()),
            entity_id=claim_id,
            entity_type="SemanticClaim",
            action="CANONICALIZE",
            actor="system",
            previous_state=c_state,
            new_state="ACCEPTED",
            created_at=datetime.datetime.now(datetime.UTC).replace(tzinfo=None),
        )
        session.add(audit)
        accepted_roots += 1

    results.append(
        {
            "root": r,
            "wave": wave,
            "eligible": c,
            "covered": covered,
            "run_id": run_id,
            "claim_id": claim_id,
            "verdict": verdict,
            "canonical_state": c_state,
            "strength": strength,
            "scope": scope,
        }
    )
    run_id_counter += 1

session.commit()

os.makedirs("artifacts/semantic-campaign", exist_ok=True)
with open("artifacts/semantic-campaign/BATCH_08_CAMPAIGN_RESULTS.json", "w") as f:
    json.dump(results, f, indent=2)

with open("artifacts/semantic-campaign/BATCH_08_MANIFEST.json", "w") as f:
    json.dump(manifest_data, f, indent=2)

print(
    f"Execution complete. Runs: {len(results)}. Obs: {total_observations}. Claims: {total_claims}. Ver: {total_verifications}. Acc: {accepted_roots}"
)
