import datetime
import uuid

from sqlalchemy.orm import Session

from ..models import (
    AuditLog,
    CorpusSnapshot,
    IsolationEvent,
    IsolationState,
    MethodologyRevision,
    ResearchRun,
)

# The permanent source boundary for internal Quranic induction. CLEAN may only be
# asserted when the run is demonstrably conducted within this boundary.
ALLOWED_SEMANTIC_SOURCES = ("ADMITTED_CANONICAL_QURAN", "SAME_RUN_ARTIFACTS")
PROHIBITED_SEMANTIC_SOURCES = (
    "EXTERNAL_LEXICON",
    "TAFSIR",
    "TRANSLATION",
    "PRIOR_PROJECT_ANSWER",
    "MODEL_MEMORY",
    "WEB_RETRIEVAL",
    "SEMANTIC_DICTIONARY",
)

NOT_ESTABLISHED = "NOT_ESTABLISHED"
ESTABLISHED = "ESTABLISHED"


class IsolationContaminationException(Exception):
    def __init__(self, message: str, run_id: str):
        self.message = message
        self.run_id = run_id
        super().__init__(self.message)


class IsolationEstablishmentRejected(Exception):
    """A CLEAN isolation could not be honestly established for the run."""

    def __init__(self, message: str, run_id: str):
        self.message = message
        self.run_id = run_id
        super().__init__(self.message)


class BlindLabIsolationService:
    @staticmethod
    def establish_semantic_isolation(
        db: Session,
        run_id: str,
        *,
        actor: str = "TRUSTED_LOCAL_USER",
        allowed_sources: list[str] | None = None,
    ) -> IsolationState:
        """Fail-closed establishment of the source boundary for a research run.

        A fresh run's isolation defaults to ``NOT_ESTABLISHED``. CLEAN is NOT a
        default and cannot be asserted merely because a preflight endpoint was
        called or because no contamination has yet been recorded. Establishment
        requires, and records as an immutable attestation:

        * the run exists and binds a production-valid corpus snapshot;
        * the bound methodology revision is CURRENT and source-bound;
        * the declared evidence sources are a subset of the permitted boundary;
        * the prohibited semantic-authority sources are recorded explicitly;
        * an input manifest pins corpus/methodology/source lineage;
        * an immutable ``AuditLog`` links the attesting actor and timestamp.

        Only on full success does the state transition ``NOT_ESTABLISHED ->
        ESTABLISHED`` with ``is_contaminated=CLEAN``. A run already recorded as
        contaminated cannot be (re)established as CLEAN.

        This does not claim a technical guarantee the application cannot enforce:
        it attests that the governed inputs were the permitted ones and records
        the boundary; actual prohibited-source exposure is a separate, blocking
        contamination event (see ``enforce_semantic_isolation`` /
        ``record_actual_contamination``).
        """
        # Imported lazily to avoid importing service siblings at module import.
        from backend.domain.services.corpus.authority import is_production_validated
        from backend.domain.services.methodology_authority import (
            methodology_authority_failures,
        )

        run = db.get(ResearchRun, run_id)
        if run is None:
            raise LookupError(f"ResearchRun {run_id} not found")

        snapshot = db.get(CorpusSnapshot, run.corpus_snapshot)
        if snapshot is None or not is_production_validated(snapshot):
            raise IsolationEstablishmentRejected(
                "Cannot establish isolation: the run's corpus snapshot is not "
                "production-valid.",
                run_id=run_id,
            )
        methodology = db.get(MethodologyRevision, run.methodology_revision)
        if methodology is None or methodology_authority_failures(methodology):
            raise IsolationEstablishmentRejected(
                "Cannot establish isolation: the run's methodology revision is not "
                "current and source-bound.",
                run_id=run_id,
            )

        declared = list(allowed_sources or ALLOWED_SEMANTIC_SOURCES)
        illegal = [s for s in declared if s not in ALLOWED_SEMANTIC_SOURCES]
        if illegal:
            raise IsolationEstablishmentRejected(
                "Cannot establish isolation: declared sources outside the permitted "
                f"boundary: {illegal}",
                run_id=run_id,
            )

        state = (
            db.query(IsolationState)
            .filter(IsolationState.research_run_id == run_id)
            .one_or_none()
        )
        if state is not None and state.is_contaminated == "PRIOR_CONTAMINATED":
            raise IsolationEstablishmentRejected(
                "Cannot establish CLEAN isolation: the run is already recorded as "
                "contaminated.",
                run_id=run_id,
            )

        manifest = {
            "corpus_snapshot": str(run.corpus_snapshot),
            "corpus_snapshot_hash": str(snapshot.canonical_text_hash),
            "corpus_snapshot_activation": str(snapshot.activation_status),
            "structural_source": snapshot.structural_source,
            "methodology_revision": str(run.methodology_revision),
            "methodology_source_reference": str(methodology.source_reference),
            "methodology_source_sha256": str(methodology.source_sha256),
            "allowed_sources": declared,
            "prohibited_sources": list(PROHIBITED_SEMANTIC_SOURCES),
            "target_contract": str(run.target_contract),
            "target_expression": str(run.target_expression),
        }

        attested_at = datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
        audit = AuditLog(
            id=f"aud_{uuid.uuid4().hex[:8]}",
            entity_id=run_id,
            entity_type="IsolationState",
            action="ESTABLISH_SOURCE_ISOLATION",
            previous_state=(
                str(state.establishment_status) if state is not None else NOT_ESTABLISHED
            ),
            new_state=ESTABLISHED,
            actor=actor,
            created_at=attested_at,
        )
        db.add(audit)
        db.flush()

        if state is None:
            state = IsolationState(
                id=f"iso_{uuid.uuid4().hex[:8]}",
                research_run_id=run_id,
                target_contract=run.target_contract,
                corpus_snapshot=run.corpus_snapshot,
                methodology_reference=run.methodology_revision,
            )
            db.add(state)
        state.allowed_sources = declared
        state.prohibited_sources = list(PROHIBITED_SEMANTIC_SOURCES)
        state.input_manifest = manifest
        state.is_contaminated = "CLEAN"
        state.establishment_status = ESTABLISHED
        state.attesting_actor = actor
        state.attested_at = attested_at
        state.audit_ref = audit.id

        db.commit()
        db.refresh(state)
        return state

    @staticmethod
    def enforce_semantic_isolation(db: Session, run_id: str):
        """
        Enforce the permanent source boundary for internal Quranic induction.

        Accepted project memory has a separate traceable read path. This method
        represents prohibited external semantic content entering evidence context.
        """
        run = db.get(ResearchRun, run_id)
        if run is None:
            raise LookupError(f"ResearchRun {run_id} not found")
        state = (
            db.query(IsolationState)
            .filter(IsolationState.research_run_id == run_id)
            .one_or_none()
        )
        if state is None:
            raise IsolationContaminationException(
                message="Source isolation has not been initialized.", run_id=run_id
            )
        event = IsolationEvent(
            id=f"evt_{uuid.uuid4().hex[:8]}",
            research_run_id=run_id,
            attempted_action="READ_PROHIBITED_EXTERNAL_SEMANTIC_SOURCE",
            was_blocked=True,
        )
        db.add(event)
        db.commit()
        raise IsolationContaminationException(
            message=(
                "Prohibited source read blocked: external semantic content cannot "
                "enter internal Quranic induction."
            ),
            run_id=run_id,
        )

    @staticmethod
    def record_actual_contamination(db: Session, run_id: str, reason: str):
        """
        Records actual prior exposure/injection affecting the analysis,
        not merely a successfully blocked request.
        """
        state = (
            db.query(IsolationState)
            .filter(IsolationState.research_run_id == run_id)
            .first()
        )
        if state and state.is_contaminated != "PRIOR_CONTAMINATED":
            state.is_contaminated = "PRIOR_CONTAMINATED"
            state.contamination_reason = reason
            db.commit()
