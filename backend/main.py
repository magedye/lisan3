import uuid
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException as StarletteHTTPException

from .domain import models, schemas
from .domain.services.canonicalization import (
    CanonicalizationPolicy,
    accepted_root_result,
    reopen_accepted_results_for_new_evidence,
)
from .domain.services.claim_visibility import ClaimReleasePolicy
from .domain.services.knowledge_graph import (
    PROJECTION_REVISION,
    GraphAccessForbidden,
    GraphSourceNotFound,
    KnowledgeGraphService,
)
from .domain.services.purity import evaluate_methodology_diagnostics
from .domain.services.research_judgment import (
    ResearchJudgmentService,
    resolve_evidence_refs,
)
from .domain.services.run_admission import ResearchRunAdmissionPolicy
from .domain.services.steward import StewardAuthorityRejected, StewardCommandService
from .infrastructure.database import database_schema_status, get_db

app = FastAPI(
    title="Lisanapp API",
    description="Canonical backend for Lisan Semantic Extraction and Governance",
    version="1.0.0",
    responses={
        400: {"model": schemas.ErrorResponse, "description": "Bad Request"},
        403: {"model": schemas.ErrorResponse, "description": "Forbidden"},
        404: {"model": schemas.ErrorResponse, "description": "Not Found"},
        422: {"model": schemas.ErrorResponse, "description": "Validation Error"},
        500: {"model": schemas.ErrorResponse, "description": "Internal Server Error"},
    },
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    detail_str = str(exc)
    return JSONResponse(
        status_code=422,
        content={"status": "ERROR", "message": detail_str, "detail": detail_str},
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "ERROR",
            "message": str(exc.detail),
            "detail": str(exc.detail),
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    error_message = repr(exc) if not isinstance(exc, str) else exc
    return JSONResponse(
        status_code=500,
        content={
            "status": "ERROR",
            "message": "Internal Server Error",
            "detail": "Internal Server Error",
        },
    )


# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _claim_responses(claims: list[models.SemanticClaim]):
    return [
        schemas.SemanticClaimResponse.model_validate(claim, from_attributes=True)
        for claim in claims
    ]


def _run_claims_visible(db: Session, run_id: str) -> bool:
    return ClaimReleasePolicy.evaluate_run(db, run_id).released


def _released_claims(
    db: Session, claims: list[models.SemanticClaim]
) -> list[models.SemanticClaim]:
    return ClaimReleasePolicy.filter_released_claims(db, claims)


def _require_released_claim(db: Session, claim_id: str) -> models.SemanticClaim:
    claim = db.get(models.SemanticClaim, claim_id)
    if claim is None:
        raise HTTPException(status_code=404, detail="Claim not found")
    decision = ClaimReleasePolicy.evaluate_claim(db, claim)
    if not decision.released:
        raise HTTPException(
            status_code=403,
            detail="Research Judgment is not visible because its source boundary is invalid",
        )
    return claim


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Lisanapp Backend is running"}


@app.post("/ask", response_model=schemas.AskLisanResponse)
def ask_lisan(request: schemas.AskLisanRequest, db: Session = Depends(get_db)):
    if request.contract_type == "ROOT_CONCEPT":
        accepted = accepted_root_result(db, request.expression)
        if accepted is not None:
            return schemas.AskLisanResponse(
                status="ACCEPTED_RESULT",
                claim=schemas.SemanticClaimResponse.model_validate(
                    accepted, from_attributes=True
                ),
            )

    claims = (
        db.query(models.SemanticClaim)
        .join(models.ResearchRun)
        .filter(
            models.ResearchRun.target_expression == request.expression,
            models.SemanticClaim.contract_type == request.contract_type,
        )
        .order_by(
            models.SemanticClaim.canonical_state.desc(),
            models.SemanticClaim.created_at.desc(),
        )
        .all()
    )
    released = _released_claims(db, claims)
    claim = next(
        (
            item
            for item in released
            if item.canonical_state == models.CanonicalState.ACCEPTED.value
        ),
        None,
    ) or next(
        (
            item
            for item in released
            if item.research_state == models.ResearchState.PREFERRED.value
        ),
        None,
    )

    if claim:
        return schemas.AskLisanResponse(
            status=(
                "ACCEPTED_RESULT"
                if claim.canonical_state == models.CanonicalState.ACCEPTED.value
                else "PREFERRED_RESEARCH_RESULT"
            ),
            claim=schemas.SemanticClaimResponse.model_validate(
                claim, from_attributes=True
            ),
        )

    return schemas.AskLisanResponse(status="INSUFFICIENT_EVIDENCE", claim=None)


@app.post(
    "/runs",
    response_model=schemas.ResearchRunResponse,
    responses={503: {"description": "Governed run authority unavailable"}},
)
def create_run(run: schemas.ResearchRunCreate, db: Session = Depends(get_db)):
    authority = ResearchRunAdmissionPolicy.resolve(db)
    if not authority.accepted:
        raise HTTPException(
            status_code=503,
            detail="Run admission denied: " + "; ".join(authority.reasons),
        )
    run_id = f"run_{uuid.uuid4().hex[:8]}"
    db_run = models.ResearchRun(
        id=run_id,
        target_contract=run.target_contract,
        target_expression=run.target_expression,
        methodology_revision=authority.methodology_revision_id,
        corpus_snapshot=authority.corpus_snapshot_id,
        authority_context=authority.authority_context,
    )
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    return db_run


@app.get(
    "/methodologies",
    response_model=list[schemas.MethodologyRevisionResponse],
)
def list_methodology_revisions(db: Session = Depends(get_db)):
    return (
        db.query(models.MethodologyRevision)
        .order_by(
            models.MethodologyRevision.methodology_id,
            models.MethodologyRevision.revision,
        )
        .all()
    )


@app.get("/attention", response_model=schemas.AttentionCenterResponse)
def get_attention_center(db: Session = Depends(get_db)):
    """Read-only projection of persisted work that currently needs attention."""
    recent_runs = (
        db.query(models.ResearchRun)
        .order_by(models.ResearchRun.updated_at.desc())
        .limit(8)
        .all()
    )
    canonicalization_candidates = (
        db.query(models.SemanticClaim)
        .filter(
            models.SemanticClaim.research_state == "PREFERRED",
            models.SemanticClaim.canonical_state == "NOT_CANONICAL",
            models.SemanticClaim.result_strength == "STRONG",
        )
        .order_by(models.SemanticClaim.created_at.desc())
        .limit(8)
        .all()
    )
    reopen_required_claims = (
        db.query(models.SemanticClaim)
        .filter(models.SemanticClaim.canonical_state == "REOPEN_REQUIRED")
        .order_by(models.SemanticClaim.created_at.desc())
        .limit(8)
        .all()
    )
    pending_proposals = (
        db.query(models.ChangeProposal)
        .filter(models.ChangeProposal.status == "PROPOSED")
        .order_by(models.ChangeProposal.created_at.desc())
        .limit(8)
        .all()
    )
    recent_changes = (
        db.query(models.AuditLog)
        .order_by(models.AuditLog.created_at.desc())
        .limit(8)
        .all()
    )
    corpus_snapshots = (
        db.query(models.CorpusSnapshot)
        .order_by(models.CorpusSnapshot.created_at.desc())
        .limit(20)
        .all()
    )
    return schemas.AttentionCenterResponse(
        recent_runs=recent_runs,
        canonicalization_candidates=_claim_responses(
            _released_claims(db, canonicalization_candidates)
        ),
        reopen_required_claims=_claim_responses(
            _released_claims(db, reopen_required_claims)
        ),
        pending_proposals=pending_proposals,
        recent_changes=ClaimReleasePolicy.filter_released_audit_logs(
            db, recent_changes
        ),
        corpus_snapshots=corpus_snapshots,
        run_admission=ResearchRunAdmissionPolicy.current_state(db),
    )


@app.get("/runs/{run_id}", response_model=schemas.ResearchRunResponse)
def get_run(run_id: str, db: Session = Depends(get_db)):
    db_run = (
        db.query(models.ResearchRun).filter(models.ResearchRun.id == run_id).first()
    )
    if not db_run:
        raise HTTPException(status_code=404, detail="Run not found")
    return db_run


@app.get("/runs/{run_id}/workspace", response_model=schemas.RunWorkspaceResponse)
def get_run_workspace(run_id: str, db: Session = Depends(get_db)):
    """Aggregate persisted run artifacts without bypassing Blind Lab release."""
    db_run = (
        db.query(models.ResearchRun).filter(models.ResearchRun.id == run_id).first()
    )
    if not db_run:
        raise HTTPException(status_code=404, detail="Run not found")

    isolation_state = (
        db.query(models.IsolationState)
        .filter(models.IsolationState.research_run_id == run_id)
        .first()
    )
    observations = (
        db.query(models.ObservationArtifact)
        .filter(models.ObservationArtifact.research_run_id == run_id)
        .order_by(models.ObservationArtifact.created_at.asc())
        .all()
    )
    hypotheses = (
        db.query(models.Hypothesis)
        .filter(models.Hypothesis.research_run_id == run_id)
        .order_by(models.Hypothesis.created_at.asc())
        .all()
    )
    hypothesis_ids = [item.id for item in hypotheses]
    neighbors = (
        db.query(models.EssentialNeighbor)
        .filter(models.EssentialNeighbor.hypothesis_id.in_(hypothesis_ids))
        .order_by(models.EssentialNeighbor.created_at.asc())
        .all()
        if hypothesis_ids
        else []
    )
    claims_visible = _run_claims_visible(db, run_id)
    claims = (
        db.query(models.SemanticClaim)
        .filter(models.SemanticClaim.research_run_id == run_id)
        .order_by(models.SemanticClaim.created_at.asc())
        .all()
        if claims_visible
        else []
    )
    audit_events = (
        db.query(models.AuditLog)
        .filter(models.AuditLog.entity_id == run_id)
        .order_by(models.AuditLog.created_at.desc())
        .all()
    )
    return schemas.RunWorkspaceResponse(
        run=db_run,
        isolation_state=isolation_state,
        observations=observations,
        hypotheses=hypotheses,
        neighbors=neighbors,
        research_judgments=_claim_responses(claims),
        judgments_visible=claims_visible,
        audit_events=audit_events,
    )


@app.get("/runs/{run_id}/blind", response_model=schemas.IsolationStateResponse)
def get_blind_lab_state(run_id: str, db: Session = Depends(get_db)):
    state = (
        db.query(models.IsolationState)
        .filter(models.IsolationState.research_run_id == run_id)
        .first()
    )
    if not state:
        raise HTTPException(status_code=404, detail="Isolation state not found")
    return state


@app.post(
    "/runs/{run_id}/blind/preflight", response_model=schemas.IsolationStateResponse
)
def start_isolation_preflight(
    run_id: str, db: Session = Depends(get_db)
):
    run = db.query(models.ResearchRun).filter(models.ResearchRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    db_state = models.IsolationState(
        id=f"iso_{uuid.uuid4().hex[:8]}",
        research_run_id=run_id,
        target_contract=run.target_contract,
        corpus_snapshot=run.corpus_snapshot,
        methodology_reference=run.methodology_revision,
        allowed_sources=["ADMITTED_CANONICAL_QURAN", "SAME_RUN_ARTIFACTS"],
        is_contaminated="CLEAN",
    )
    db.add(db_state)

    # Update run stage
    run.current_stage = models.ResearchStage.RESEARCH.value
    db.commit()
    db.refresh(db_state)
    return db_state


@app.get("/runs/{run_id}/corpus", response_model=list[schemas.CorpusOccurrenceResponse])
def get_corpus_occurrences(run_id: str, db: Session = Depends(get_db)):
    state = (
        db.query(models.IsolationState)
        .filter(models.IsolationState.research_run_id == run_id)
        .first()
    )
    if not state:
        raise HTTPException(status_code=400, detail="Run has no isolation preflight")

    if state.is_contaminated == "PRIOR_CONTAMINATED":
        raise HTTPException(
            status_code=403, detail="Cannot access corpus: Run is contaminated"
        )

    run = db.query(models.ResearchRun).filter(models.ResearchRun.id == run_id).first()

    occurrences = (
        db.query(models.CorpusOccurrence)
        .filter(
            models.CorpusOccurrence.snapshot_id == state.corpus_snapshot,
            models.CorpusOccurrence.expression == run.target_expression,
        )
        .all()
    )

    return occurrences


@app.post(
    "/runs/{run_id}/observations", response_model=schemas.ObservationArtifactResponse
)
def record_observation(
    run_id: str,
    artifact: schemas.ObservationArtifactCreate,
    db: Session = Depends(get_db),
):
    state = (
        db.query(models.IsolationState)
        .filter(models.IsolationState.research_run_id == run_id)
        .first()
    )
    if not state:
        raise HTTPException(status_code=400, detail="Run has no isolation preflight")

    if state.is_contaminated == "PRIOR_CONTAMINATED":
        raise HTTPException(
            status_code=403, detail="Cannot record observation: Run is contaminated"
        )

    run = db.query(models.ResearchRun).filter(models.ResearchRun.id == run_id).first()
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    occurrence = db.get(models.CorpusOccurrence, artifact.occurrence_ref)
    if occurrence is None or occurrence.snapshot_id != run.corpus_snapshot:
        raise HTTPException(
            status_code=422,
            detail="Observation occurrence is absent or outside the run corpus",
        )
    db_artifact = models.ObservationArtifact(
        id=f"obs_{uuid.uuid4().hex[:8]}",
        research_run_id=run_id,
        occurrence_ref=artifact.occurrence_ref,
        form=artifact.form,
        syntax=artifact.syntax,
        participant_roles=artifact.participant_roles,
        local_context=artifact.local_context,
        unresolved_ambiguity=artifact.unresolved_ambiguity,
    )
    db.add(db_artifact)

    db.flush()
    reopen_accepted_results_for_new_evidence(db, run, db_artifact)
    db.commit()
    db.refresh(db_artifact)
    return db_artifact


# --- Test Endpoint for Isolation Mock ---
from .domain.services.isolation import (
    BlindLabIsolationService,
    IsolationContaminationException,
)


@app.get("/runs/{run_id}/read_semantic_dictionary")
def read_semantic_dictionary(run_id: str, db: Session = Depends(get_db)):
    try:
        BlindLabIsolationService.enforce_semantic_isolation(db, run_id)
        return {"data": "This is a secret semantic definition"}
    except LookupError as exc:
        raise HTTPException(status_code=404, detail="Run not found") from exc
    except IsolationContaminationException as e:
        raise HTTPException(status_code=403, detail=str(e)) from e


@app.post("/runs/{run_id}/record_contamination")
def trigger_actual_contamination(
    run_id: str, reason: str, db: Session = Depends(get_db)
):
    BlindLabIsolationService.record_actual_contamination(db, run_id, reason)
    return {"status": "Contaminated"}


# --- Slice C Endpoints ---


@app.post("/runs/{run_id}/hypotheses", response_model=schemas.HypothesisResponse)
def create_hypothesis(
    run_id: str, hypothesis: schemas.HypothesisCreate, db: Session = Depends(get_db)
):
    run = db.query(models.ResearchRun).filter(models.ResearchRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    state = (
        db.query(models.IsolationState)
        .filter(models.IsolationState.research_run_id == run_id)
        .first()
    )
    if state is None:
        raise HTTPException(status_code=400, detail="Run has no source-isolation preflight")
    if state.is_contaminated == "PRIOR_CONTAMINATED":
        raise HTTPException(
            status_code=403, detail="Cannot create hypothesis: Run is contaminated"
        )

    evidence = resolve_evidence_refs(
        db,
        run,
        hypothesis.supporting_evidence_refs + hypothesis.counterevidence_refs,
    )
    if not evidence.valid:
        raise HTTPException(status_code=422, detail="; ".join(evidence.reasons))
    db_hyp = models.Hypothesis(
        id=f"hyp_{uuid.uuid4().hex[:8]}",
        research_run_id=run_id,
        hypothesis_type=hypothesis.hypothesis_type,
        target_contract=hypothesis.target_contract,
        scope=hypothesis.scope,
        statement=hypothesis.statement,
        supporting_evidence_refs=hypothesis.supporting_evidence_refs,
        counterevidence_refs=hypothesis.counterevidence_refs,
        unresolved_cases=hypothesis.unresolved_cases,
        rejection_condition=hypothesis.rejection_condition.model_dump(),
        provenance=hypothesis.provenance,
    )
    db.add(db_hyp)

    db.commit()
    db.refresh(db_hyp)
    return db_hyp


@app.post(
    "/hypotheses/{hyp_id}/neighbors", response_model=schemas.EssentialNeighborResponse
)
def add_neighbor(
    hyp_id: str,
    neighbor: schemas.EssentialNeighborCreate,
    db: Session = Depends(get_db),
):
    db_hyp = db.query(models.Hypothesis).filter(models.Hypothesis.id == hyp_id).first()
    if not db_hyp:
        raise HTTPException(status_code=404, detail="Hypothesis not found")

    run_id = db_hyp.research_run_id
    state = (
        db.query(models.IsolationState)
        .filter(models.IsolationState.research_run_id == run_id)
        .first()
    )
    if state is None:
        raise HTTPException(status_code=400, detail="Run has no source-isolation preflight")
    if state.is_contaminated == "PRIOR_CONTAMINATED":
        raise HTTPException(
            status_code=403, detail="Cannot differentiate: Run is contaminated"
        )

    db_neighbor = models.EssentialNeighbor(
        id=f"nbr_{uuid.uuid4().hex[:8]}",
        hypothesis_id=hyp_id,
        shared_domain=neighbor.shared_domain,
        positive_distinguishing_candidate=neighbor.positive_distinguishing_candidate,
        relevant_differentiation_axes=neighbor.relevant_differentiation_axes,
        substitution_probe=neighbor.substitution_probe,
        boundary_negative_cases=neighbor.boundary_negative_cases,
        supporting_evidence=neighbor.supporting_evidence,
        counterevidence=neighbor.counterevidence,
        unresolved_distinction=neighbor.unresolved_distinction,
    )
    db.add(db_neighbor)

    run = db.query(models.ResearchRun).filter(models.ResearchRun.id == run_id).first()
    run.current_stage = models.ResearchStage.CHALLENGE.value

    db.commit()
    db.refresh(db_neighbor)
    return db_neighbor


@app.post(
    "/runs/{run_id}/judgments", response_model=schemas.SemanticClaimResponse
)
def create_research_judgment(
    run_id: str,
    judgment: schemas.ResearchJudgmentCreate,
    db: Session = Depends(get_db),
):
    run = db.query(models.ResearchRun).filter(models.ResearchRun.id == run_id).first()
    if run is None:
        raise HTTPException(status_code=404, detail="ResearchRun not found")
    try:
        return ResearchJudgmentService.create(
            db, run, judgment, actor="TRUSTED_LOCAL_RESEARCHER"
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/judgments/{claim_id}", response_model=schemas.SemanticClaimResponse)
def get_research_judgment(claim_id: str, db: Session = Depends(get_db)):
    return _require_released_claim(db, claim_id)


@app.post(
    "/judgments/{claim_id}/verification",
    response_model=schemas.VerificationRecordResponse,
)
def record_independent_verification(
    claim_id: str,
    verification: schemas.VerificationRecordCreate,
    db: Session = Depends(get_db),
):
    claim = db.get(models.SemanticClaim, claim_id)
    if not claim:
        raise HTTPException(status_code=404, detail="Research Judgment not found")
    if verification.decision == "VERIFIED" and verification.verification_type != "INDEPENDENT":
        raise HTTPException(
            status_code=422,
            detail="A VERIFIED decision requires verification_type=INDEPENDENT",
        )
    run = db.get(models.ResearchRun, claim.research_run_id)
    if run is None:
        raise HTTPException(status_code=422, detail="ResearchRun not found")
    evidence = resolve_evidence_refs(db, run, verification.evidence_refs)
    if not evidence.valid:
        raise HTTPException(status_code=422, detail="; ".join(evidence.reasons))
    record = models.VerificationRecord(
        id=f"ver_{uuid.uuid4().hex[:8]}",
        claim_id=claim_id,
        verifier_identity="TRUSTED_LOCAL_INDEPENDENT_VERIFIER",
        verification_type=verification.verification_type,
        decision=verification.decision,
        rationale=verification.rationale,
        evidence_refs=verification.evidence_refs,
        evaluated_claim_revision=claim.revision_id,
    )
    db.add(record)
    claim.verification_state = (
        models.VerificationState.VERIFIED.value
        if verification.decision == "VERIFIED"
        else models.VerificationState.NOT_VERIFIED.value
    )
    db.add(
        models.AuditLog(
            id=f"aud_{uuid.uuid4().hex[:8]}",
            entity_id=claim.id,
            entity_type="ResearchJudgment",
            action="RECORD_INDEPENDENT_VERIFICATION",
            previous_state=None,
            new_state=claim.verification_state,
            actor="TRUSTED_LOCAL_INDEPENDENT_VERIFIER",
        )
    )
    db.commit()
    db.refresh(record)
    return record


@app.post(
    "/judgments/{claim_id}/canonicalize",
    response_model=schemas.SemanticClaimResponse,
)
def canonicalize_research_judgment(
    claim_id: str,
    request: schemas.CanonicalizationRequest,
    db: Session = Depends(get_db),
):
    claim = db.get(models.SemanticClaim, claim_id)
    if not claim:
        raise HTTPException(status_code=404, detail="Research Judgment not found")
    try:
        return CanonicalizationPolicy.canonicalize(
            db, claim, rationale=request.rationale
        )
    except ValueError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


# --- AI Pipeline Endpoints ---
from pydantic_ai import Agent

from .domain.services.ai_context import AIContextBuilder
from .domain.services.ai_provider import get_ai_model, get_provider_name
from .domain.services.ai_tools import tool_dispatcher
from .domain.services.skill_loader import SemanticSkillLoader


@app.post(
    "/runs/{run_id}/ai/research-judgment",
    response_model=schemas.AIResearchJudgmentResponse,
)
def ai_create_research_judgment(run_id: str, db: Session = Depends(get_db)):
    """
    Execute the model as a research actor. Deterministic host validation decides
    whether its structured Research Judgment may be persisted; it can never
    perform canonicalization.
    """
    run = db.query(models.ResearchRun).filter(models.ResearchRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    context = AIContextBuilder.build_research_context(db, run_id)
    model = get_ai_model()
    provider_name = get_provider_name()
    skill_snapshot = SemanticSkillLoader.load_skill()
    skill_version = skill_snapshot.revision_hash if skill_snapshot else "unknown-skill"

    prompt = (
        "Create a Research Judgment under the active semantic skill. Use only "
        "the supplied evidence context; never invent evidence, tool execution, "
        f"or coverage. Return UNRESOLVED when necessary. Context: {context}"
    )

    try:
        agent = Agent(model, output_type=schemas.ResearchJudgmentCreate)
        result = agent.run_sync(prompt)
        judgment_input = result.output
        judgment = ResearchJudgmentService.create(
            db, run, judgment_input, actor="AI_RESEARCH_RUNTIME"
        )
        record = models.AIExecutionRecord(
            id=f"ai_{uuid.uuid4().hex[:8]}",
            research_run_id=run_id,
            analysis_stage="RESEARCH_JUDGMENT",
            provider=provider_name,
            model="default",
            skill_version=skill_version,
            prompt_revision="LISAN3_AI_AUTHORITY_V3_2026_09_06",
            tools_available=list(tool_dispatcher.get_available_tools().keys()),
            input_artifact_refs=[str(context.get("run_id"))],
            output_artifact_refs=[f"judgment:{judgment.id}"],
            execution_status="SUCCESS",
        )
        response_status = "CREATED"
        failure_reason = None
    except ValueError as exc:
        record = models.AIExecutionRecord(
            id=f"ai_{uuid.uuid4().hex[:8]}",
            research_run_id=run_id,
            analysis_stage="RESEARCH_JUDGMENT",
            provider=provider_name,
            model="default",
            skill_version=skill_version,
            prompt_revision="LISAN3_AI_AUTHORITY_V3_2026_09_06",
            tools_available=list(tool_dispatcher.get_available_tools().keys()),
            input_artifact_refs=[str(context.get("run_id"))],
            execution_status="VALIDATION_FAILED",
            error_message=str(exc),
        )
        judgment = None
        response_status = "VALIDATION_FAILED"
        failure_reason = str(exc)
    except Exception as exc:
        record = models.AIExecutionRecord(
            id=f"ai_{uuid.uuid4().hex[:8]}",
            research_run_id=run_id,
            analysis_stage="RESEARCH_JUDGMENT",
            provider=provider_name,
            model="default",
            skill_version=skill_version,
            prompt_revision="LISAN3_AI_AUTHORITY_V3_2026_09_06",
            tools_available=list(tool_dispatcher.get_available_tools().keys()),
            input_artifact_refs=[str(context.get("run_id"))],
            execution_status="FAILED",
            error_message=str(exc),
        )
        judgment = None
        response_status = "EXECUTION_FAILED"
        failure_reason = str(exc)

    db.add(record)
    db.commit()
    db.refresh(record)
    return schemas.AIResearchJudgmentResponse(
        status=response_status,
        trace=schemas.AIExecutionRecordResponse.model_validate(
            record, from_attributes=True
        ),
        judgment=(
            schemas.SemanticClaimResponse.model_validate(judgment, from_attributes=True)
            if judgment is not None
            else None
        ),
        failure_reason=failure_reason,
    )


# --- Governance Endpoints (Slice E) ---


@app.get("/governance/overview", response_model=schemas.GovernanceOverviewResponse)
def get_governance_overview(db: Session = Depends(get_db)):
    """Read-only governance, review, and source-admission projection."""
    rules = (
        db.query(models.GovernanceRule)
        .order_by(models.GovernanceRule.rule_code.asc())
        .limit(100)
        .all()
    )
    proposals = (
        db.query(models.ChangeProposal)
        .order_by(models.ChangeProposal.created_at.desc())
        .limit(100)
        .all()
    )
    canonicalization_candidates = (
        db.query(models.SemanticClaim)
        .filter(
            models.SemanticClaim.research_state == "PREFERRED",
            models.SemanticClaim.result_strength == "STRONG",
            models.SemanticClaim.canonical_state == "NOT_CANONICAL",
        )
        .order_by(models.SemanticClaim.created_at.desc())
        .limit(100)
        .all()
    )
    reopen_required = (
        db.query(models.SemanticClaim)
        .filter(models.SemanticClaim.canonical_state == "REOPEN_REQUIRED")
        .order_by(models.SemanticClaim.created_at.desc())
        .limit(100)
        .all()
    )
    corpus_snapshots = (
        db.query(models.CorpusSnapshot)
        .order_by(models.CorpusSnapshot.created_at.desc())
        .limit(100)
        .all()
    )
    return schemas.GovernanceOverviewResponse(
        rules=rules,
        proposals=proposals,
        canonicalization_candidates=_claim_responses(
            _released_claims(db, canonicalization_candidates)
        ),
        reopen_required=_claim_responses(_released_claims(db, reopen_required)),
        corpus_snapshots=corpus_snapshots,
    )


@app.post("/governance/rules", response_model=schemas.GovernanceRuleResponse)
def create_rule(rule: schemas.GovernanceRuleCreate, db: Session = Depends(get_db)):
    from sqlalchemy.exc import IntegrityError

    db_rule = models.GovernanceRule(
        id=f"rule_{uuid.uuid4().hex[:8]}",
        rule_code=rule.rule_code,
        description=rule.description,
        active_revision=1,
    )
    db.add(db_rule)
    db_revision = models.RuleRevision(
        id=f"rev_{uuid.uuid4().hex[:8]}",
        rule_code=rule.rule_code,
        revision_number=1,
        changes_described="Initial creation",
        approved_by="LOCAL_USER",
    )
    db.add(db_revision)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="Governance rule already exists or invalid"
        )
    db.refresh(db_rule)
    return db_rule


@app.post("/governance/proposals", response_model=schemas.ChangeProposalResponse)
def create_change_proposal(
    proposal: schemas.ChangeProposalCreate, db: Session = Depends(get_db)
):
    # Simple impact analysis
    affected_dependencies = (
        db.query(models.DependencyRecord)
        .filter(
            models.DependencyRecord.dependency_type == "GOVERNANCE_RULE",
            models.DependencyRecord.dependency_ref == proposal.rule_code,
        )
        .count()
    )

    db_proposal = models.ChangeProposal(
        id=f"prop_{uuid.uuid4().hex[:8]}",
        rule_code=proposal.rule_code,
        proposed_changes=proposal.proposed_changes,
        impact_analysis={"affected_claims_count": affected_dependencies},
        status="PROPOSED",
    )
    db.add(db_proposal)
    db.commit()
    db.refresh(db_proposal)
    return db_proposal


@app.post(
    "/governance/proposals/{proposal_id}/approve",
    response_model=schemas.ChangeProposalResponse,
)
def approve_proposal(proposal_id: str, db: Session = Depends(get_db)):
    proposal = (
        db.query(models.ChangeProposal)
        .filter(models.ChangeProposal.id == proposal_id)
        .first()
    )
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    rule = (
        db.query(models.GovernanceRule)
        .filter(models.GovernanceRule.rule_code == proposal.rule_code)
        .first()
    )
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    proposal.status = "APPROVED"
    rule.active_revision += 1

    # New immutable revision
    db_revision = models.RuleRevision(
        id=f"rev_{uuid.uuid4().hex[:8]}",
        rule_code=rule.rule_code,
        revision_number=rule.active_revision,
        changes_described=proposal.proposed_changes,
        approved_by="LOCAL_USER",
    )
    db.add(db_revision)

    # Transitive Invalidation
    dependencies = (
        db.query(models.DependencyRecord)
        .filter(
            models.DependencyRecord.dependency_type == "GOVERNANCE_RULE",
            models.DependencyRecord.dependency_ref == rule.rule_code,
            models.DependencyRecord.dependency_revision < rule.active_revision,
        )
        .all()
    )

    for dep in dependencies:
        claim = (
            db.query(models.SemanticClaim)
            .filter(models.SemanticClaim.id == dep.dependent_claim_id)
            .first()
        )
        if claim and claim.canonical_state == "ACCEPTED":
            claim.canonical_state = "REOPEN_REQUIRED"
            claim.verification_state = "NOT_VERIFIED"
            claim.revision_id += 1
            db.add(
                models.AuditLog(
                    id=f"aud_{uuid.uuid4().hex[:8]}",
                    entity_id=claim.id,
                    entity_type="ResearchJudgment",
                    action="REOPEN_FOR_GOVERNING_REVISION",
                    previous_state="ACCEPTED",
                    new_state="REOPEN_REQUIRED",
                    actor="GOVERNANCE_IMPACT_POLICY",
                )
            )

    db.commit()
    db.refresh(proposal)
    return proposal


# --- Steward Endpoints (Slice F) ---


@app.post("/steward/commands", response_model=schemas.StewardCommandResponse)
def execute_steward_command(
    cmd: schemas.StewardCommandCreate, db: Session = Depends(get_db)
):
    try:
        return StewardCommandService.execute(db, cmd)
    except StewardAuthorityRejected as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


# --- Knowledge & Operations


@app.get(
    "/knowledge/explorer/{claim_id}", response_model=schemas.KnowledgeExplorerJudgment
)
def get_knowledge_explorer(claim_id: str, db: Session = Depends(get_db)):
    """
    Returns an aggregated read-only view of a given semantic node.
    """
    claim = _require_released_claim(db, claim_id)

    run = (
        db.query(models.ResearchRun)
        .filter(models.ResearchRun.id == claim.research_run_id)
        .first()
    )

    dependencies = (
        db.query(models.DependencyRecord)
        .filter(models.DependencyRecord.dependent_claim_id == claim_id)
        .all()
    )

    # Check rules that might invalidate this claim (reverse lookup)
    affected_by = []
    for dep in dependencies:
        affected_by.append(dep.dependency_ref)

    return schemas.KnowledgeExplorerJudgment(
        claim_id=claim.id,
        contract_type=claim.contract_type,
        target_expression=run.target_expression if run else "UNKNOWN",
        research_state=claim.research_state,
        canonical_state=claim.canonical_state,
        result_strength=claim.result_strength,
        verification_state=claim.verification_state,
        dependencies=dependencies,
        affected_by=affected_by,
    )


def _graph_response(run_id: str, db: Session) -> schemas.KnowledgeGraphResponse:
    nodes, edges, analysis = KnowledgeGraphService.read(db, run_id)
    return schemas.KnowledgeGraphResponse(
        run_id=run_id,
        projection_revision=PROJECTION_REVISION,
        nodes=[schemas.GraphKnowledgeNodeResponse.model_validate(node) for node in nodes],
        edges=[
            schemas.GraphKnowledgeEdgeResponse(
                edge_id=edge.edge_id,
                source_node_id=edge.source_node_id,
                edge_type=edge.edge_type,
                target_node_id=edge.target_node_id,
                edge_origin=edge.edge_origin,
                edge_status=edge.edge_status,
                provenance_ref=edge.provenance_ref,
                valid_from_revision=edge.valid_from_revision,
                invalidated_at=edge.invalidated_at,
                presentation_label=KnowledgeGraphService.presentation_label(edge),
            )
            for edge in edges
        ],
        analysis=schemas.GraphAnalysisResponse(**analysis),
        authority_notice=(
            "Graph connectivity is derived projection, not semantic truth or "
            "epistemic confidence."
        ),
    )


@app.get(
    "/runs/{run_id}/knowledge-graph", response_model=schemas.KnowledgeGraphResponse
)
def get_knowledge_graph(run_id: str, db: Session = Depends(get_db)):
    """Return a Blind-Lab-safe, read-only graph slice for an internally locked run."""
    try:
        return _graph_response(run_id, db)
    except GraphSourceNotFound as exc:
        raise HTTPException(status_code=404, detail="Run not found") from exc
    except GraphAccessForbidden as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@app.post(
    "/runs/{run_id}/knowledge-graph/rebuild",
    response_model=schemas.KnowledgeGraphRebuildResponse,
)
def rebuild_knowledge_graph(run_id: str, db: Session = Depends(get_db)):
    """Explicitly rebuilds the disposable graph projection after Blind Lab release."""
    try:
        KnowledgeGraphService.require_read_access(db, run_id)
        KnowledgeGraphService.rebuild(db)
        graph = _graph_response(run_id, db)
        return schemas.KnowledgeGraphRebuildResponse(**graph.model_dump(), rebuilt=True)
    except GraphSourceNotFound as exc:
        raise HTTPException(status_code=404, detail="Run not found") from exc
    except GraphAccessForbidden as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


# --- Provenance API ---


@app.get("/judgments/{claim_id}/provenance")
def get_claim_provenance(claim_id: str, db: Session = Depends(get_db)):
    """
    Traces a semantic claim back to its roots: Dependencies, Run, and Snapshots.
    """
    claim = _require_released_claim(db, claim_id)

    deps = (
        db.query(models.DependencyRecord)
        .filter(models.DependencyRecord.dependent_claim_id == claim_id)
        .all()
    )

    run = (
        db.query(models.ResearchRun)
        .filter(models.ResearchRun.id == claim.research_run_id)
        .first()
    )

    # Audit trail for this claim
    audit_trail = (
        db.query(models.AuditLog)
        .filter(models.AuditLog.entity_id == claim_id)
        .order_by(models.AuditLog.created_at.asc())
        .all()
    )

    provenance_tree = {
        "claim": {
            "id": claim.id,
            "contract_type": claim.contract_type,
            "research_state": claim.research_state,
            "canonical_state": claim.canonical_state,
            "result_strength": claim.result_strength,
            "verification_state": claim.verification_state,
            "research_completeness": claim.research_completeness,
        },
        "dependencies": [
            {
                "type": d.dependency_type,
                "ref": d.dependency_ref,
                "rev": d.dependency_revision,
            }
            for d in deps
        ],
        "research_run": None,
        "corpus_snapshot": None,
        "audit_trail": [
            {
                "action": a.action,
                "actor": a.actor,
                "new_state": a.new_state,
                "timestamp": a.created_at.isoformat(),
            }
            for a in audit_trail
        ],
    }

    if run:
        provenance_tree["research_run"] = {
            "id": run.id,
            "methodology_revision": run.methodology_revision,
        }
        provenance_tree["corpus_snapshot"] = run.corpus_snapshot

    return provenance_tree


@app.get(
    "/judgments/{claim_id}/reproduction-manifest",
    response_model=schemas.ReproductionManifestResponse,
)
def get_reproduction_manifest(claim_id: str, db: Session = Depends(get_db)):
    """
    Returns the complete information required to reproduce a claim, fulfilling Slice G requirements.
    """
    claim = _require_released_claim(db, claim_id)

    deps = (
        db.query(models.DependencyRecord)
        .filter(models.DependencyRecord.dependent_claim_id == claim_id)
        .all()
    )
    ai_records = (
        db.query(models.AIExecutionRecord)
        .filter(models.AIExecutionRecord.research_run_id == claim.research_run_id)
        .all()
    )
    run = (
        db.query(models.ResearchRun)
        .filter(models.ResearchRun.id == claim.research_run_id)
        .first()
    )

    return {
        "claim_id": claim.id,
        "target_expression": run.target_expression if run else None,
        "methodology_revision": run.methodology_revision if run else None,
        "corpus_snapshot_id": run.corpus_snapshot if run else None,
        "ai_execution_traces": [r.id for r in ai_records],
        "dependencies": [
            {
                "type": d.dependency_type,
                "ref": d.dependency_ref,
                "rev": d.dependency_revision,
            }
            for d in deps
        ],
        "generated_at": datetime.now(timezone.utc),
    }


@app.get(
    "/judgments/{claim_id}/diagnostics",
    response_model=schemas.MethodologyDiagnosticsResponse,
)
def get_methodology_diagnostics(claim_id: str, db: Session = Depends(get_db)):
    claim = _require_released_claim(db, claim_id)
    findings, hard_blockers, warnings = evaluate_methodology_diagnostics(claim, db)
    return schemas.MethodologyDiagnosticsResponse(
        claim_id=claim_id,
        findings=findings,
        hard_blockers=hard_blockers,
        warnings=warnings,
        evaluated_at=datetime.now(timezone.utc),
    )


# --- Audit & History Read Models (Slice G) ---


@app.get("/audit", response_model=list[schemas.AuditLogResponse])
def list_audit_logs(
    entity_type: str | None = None,
    entity_id: str | None = None,
    limit: int = Query(50, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """
    Returns audit records with optional filters by entity_type and entity_id.
    """
    query = db.query(models.AuditLog)
    if entity_type:
        query = query.filter(models.AuditLog.entity_type == entity_type)
    if entity_id:
        query = query.filter(models.AuditLog.entity_id == entity_id)
    logs = query.order_by(models.AuditLog.created_at.desc()).limit(limit).all()
    if entity_id:
        claim = db.get(models.SemanticClaim, entity_id)
        if claim is not None and not ClaimReleasePolicy.is_claim_released(db, claim):
            raise HTTPException(
                status_code=403,
                detail="Claim audit is not released from Blind Lab isolation",
            )
    return ClaimReleasePolicy.filter_released_audit_logs(db, logs)


@app.get("/judgments/{claim_id}/history", response_model=schemas.ClaimHistoryResponse)
def get_claim_history(claim_id: str, db: Session = Depends(get_db)):
    """
    Returns the complete history and revision timeline of a SemanticClaim.
    """
    claim = _require_released_claim(db, claim_id)

    verifications = (
        db.query(models.VerificationRecord)
        .filter(models.VerificationRecord.claim_id == claim_id)
        .order_by(models.VerificationRecord.created_at.desc())
        .all()
    )
    audits = (
        db.query(models.AuditLog)
        .filter(models.AuditLog.entity_id == claim_id)
        .order_by(models.AuditLog.created_at.desc())
        .all()
    )

    revisions = [
        schemas.ClaimRevisionItem(
            revision_id=claim.revision_id,
            research_state=claim.research_state,
            canonical_state=claim.canonical_state,
            result_strength=claim.result_strength,
            verification_state=claim.verification_state,
            falsification_status=claim.falsification_status,
            created_at=claim.created_at,
        )
    ]

    return schemas.ClaimHistoryResponse(
        claim_id=claim.id,
        current_revision=claim.revision_id,
        revisions=revisions,
        verification_records=verifications,
        audit_events=audits,
    )


@app.get(
    "/governance/rules/{rule_code}/history", response_model=schemas.RuleHistoryResponse
)
def get_rule_history(rule_code: str, db: Session = Depends(get_db)):
    """
    Returns the revision history and change proposals for a governance rule.
    """
    rule = (
        db.query(models.GovernanceRule)
        .filter(models.GovernanceRule.rule_code == rule_code)
        .first()
    )
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    revisions = (
        db.query(models.RuleRevision)
        .filter(models.RuleRevision.rule_code == rule_code)
        .order_by(models.RuleRevision.revision_number.desc())
        .all()
    )
    proposals = (
        db.query(models.ChangeProposal)
        .filter(models.ChangeProposal.rule_code == rule_code)
        .order_by(models.ChangeProposal.created_at.desc())
        .all()
    )

    return schemas.RuleHistoryResponse(
        rule_code=rule.rule_code,
        description=rule.description,
        active_revision=rule.active_revision,
        revisions=revisions,
        proposals=proposals,
    )


# --- AI Execution Traces Read Model (Slice G) ---


@app.get(
    "/runs/{run_id}/ai/traces", response_model=list[schemas.AIExecutionRecordResponse]
)
def get_run_ai_traces(run_id: str, db: Session = Depends(get_db)):
    """
    Returns AI execution traces for a research run, exposing only governed technical metadata.
    """
    return (
        db.query(models.AIExecutionRecord)
        .filter(models.AIExecutionRecord.research_run_id == run_id)
        .order_by(models.AIExecutionRecord.created_at.asc())
        .all()
    )


@app.get("/ai/traces/{trace_id}", response_model=schemas.AIExecutionRecordResponse)
def get_ai_trace_by_id(trace_id: str, db: Session = Depends(get_db)):
    """
    Returns a specific AI execution record by ID.
    """
    record = (
        db.query(models.AIExecutionRecord)
        .filter(models.AIExecutionRecord.id == trace_id)
        .first()
    )
    if not record:
        raise HTTPException(status_code=404, detail="AI trace not found")
    return record


@app.get("/runs/{run_id}/manifest")
def get_run_reproduction_manifest(run_id: str, db: Session = Depends(get_db)):
    """
    Returns the Reproduction Manifest for a ResearchRun.
    """
    run = db.query(models.ResearchRun).filter(models.ResearchRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    return {
        "run_id": run.id,
        "corpus_snapshot": run.corpus_snapshot,
        "methodology_revision": run.methodology_revision,
        "tools_available": tool_dispatcher.get_available_tools(),
        "ai_model": get_provider_name(),
        "research_gates": [],
        "reproduction_level": "TRACEABLE_INPUTS",
        "replay_guarantee": "NOT_EXACT_AI_REPLAY",
    }


# --- Operational / Health ---


@app.get(
    "/operations/health",
    responses={503: {"description": "Database schema is not ready"}},
)
def get_system_health(db: Session = Depends(get_db)):
    """
    System health and configuration dump.
    """
    database = database_schema_status(db)
    payload = {
        "status": "HEALTHY" if database["status"] == "CURRENT" else "BLOCKED",
        "configuration": {
            "environment": "trusted_local_single_user",
            "ai_governance": "enforced",
            "auth": "mocked",
        },
        "database": database,
    }
    if database["status"] != "CURRENT":
        return JSONResponse(status_code=503, content=payload)
    return payload


# Globally add 400, 401, 403, 404, 409 responses for OpenAPI schema validation
for route in app.routes:
    if hasattr(route, "responses"):
        route.responses.update(
            {
                400: {"description": "Bad Request"},
                401: {"description": "Unauthorized"},
                403: {"description": "Forbidden"},
                404: {"description": "Not Found"},
                409: {"description": "Conflict"},
            }
        )
