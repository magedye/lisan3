"""Converge the governed corpus into the authoritative runtime DB (lisanapp.db).

Canonical Runtime Qualification Track — Track A (DB convergence).

The established blocker was a two-DB split, not missing data:
  - ``lisanapp.db``            : alembic-stamped, authoritative, holds the CURRENT
                                 source-bound methodology, but ZERO corpus rows.
  - ``data/campaign/runtime.db``: a NON-governed side store (no alembic_version,
                                 built via Base.metadata.create_all by tools/campaign.py)
                                 that happens to hold the corpus + structural tokens.

This tool makes the governed path TRUE by RE-DERIVING the corpus into the
authoritative DB from the authority-bound on-disk artifacts, using ONLY the
repository-native import/activation services. It never copies rows out of the
side store and never hand-edits a lifecycle status. Every step fails closed.

It is idempotent: re-running verifies the existing governed state instead of
duplicating it.

Run (defaults to the authoritative lisanapp.db):
    python -m tools.converge_runtime
    python -m tools.converge_runtime --json            # machine-readable evidence
    python -m tools.converge_runtime --db sqlite:///some/other.db   # explicit target

By design it refuses to run against ``data/campaign/runtime.db`` (the
non-governed side store) unless --allow-side-store is passed.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.domain import models
from backend.domain.services.corpus.activation import (
    AUTHORIZED_METHODOLOGY_ID,
    AUTHORIZED_SNAPSHOT_ID,
    CorpusActivationRejected,
    TanzilProductionActivationService,
)
from backend.domain.services.corpus.authority import (
    PRODUCTION_ACTIVE,
    is_production_validated,
    production_validation_failures,
)
from backend.domain.services.corpus.importer import TanzilPreActivationImporter
from backend.domain.services.corpus.qac_morphology import (
    QAC_EXTRACTION_VERSION,
    QacMorphologyImporter,
)
from backend.domain.services.methodology_authority import (
    eligible_methodology_revision_ids,
    methodology_authority_failures,
)
from backend.infrastructure.database import (
    SQLALCHEMY_DATABASE_URL,
    database_schema_status,
)


@dataclass
class ConvergenceEvidence:
    database_url: str
    schema_status: str
    schema_expected_revisions: list[str]
    schema_actual_revisions: list[str]
    tanzil_snapshot_id: str | None = None
    tanzil_occurrence_count: int = 0
    tanzil_import_created: bool | None = None
    activation_status: str | None = None
    validation_status: str | None = None
    is_production_validated: bool = False
    production_validation_failures: list[str] | None = None
    qac_tokens_persisted: int = 0
    qac_distinct_roots: int = 0
    qac_source_sha256: str | None = None
    methodology_eligible_ids: list[str] | None = None
    methodology_authority_failures: list[str] | None = None
    authorized_methodology_present: bool = False
    notes: list[str] | None = None

    def __post_init__(self) -> None:
        if self.notes is None:
            self.notes = []


class ConvergenceError(RuntimeError):
    pass


def converge(db, *, evidence: ConvergenceEvidence) -> ConvergenceEvidence:
    """Run the full governed convergence against an open Session."""
    # --- Guard: schema must be the canonical head (no ad-hoc create_all store). ---
    status = database_schema_status(db)
    evidence.schema_status = status["status"]
    evidence.schema_expected_revisions = status["expected_revisions"]
    evidence.schema_actual_revisions = status["actual_revisions"]
    if status["status"] != "CURRENT":
        raise ConvergenceError(
            "Target DB schema is not CURRENT (canonical Alembic head). "
            f"status={status['status']} expected={status['expected_revisions']} "
            f"actual={status['actual_revisions']} missing_tables={status['missing_tables']} "
            f"missing_columns={status['missing_columns']}. Run `alembic upgrade head` "
            "against the authoritative DB first; refusing to populate an ungoverned schema."
        )

    # If the governed snapshot is already production-valid, the import/activation
    # services (which require the PRE-activation PENDING state) must NOT be re-run;
    # verifying + re-deriving tokens is the idempotent path.
    existing = db.get(models.CorpusSnapshot, AUTHORIZED_SNAPSHOT_ID)
    already_active = (
        existing is not None
        and existing.activation_status == PRODUCTION_ACTIVE
        and is_production_validated(existing)
    )

    if already_active:
        snapshot = existing
        evidence.tanzil_snapshot_id = AUTHORIZED_SNAPSHOT_ID
        evidence.tanzil_occurrence_count = (
            db.query(models.CorpusOccurrence)
            .filter(models.CorpusOccurrence.snapshot_id == AUTHORIZED_SNAPSHOT_ID)
            .count()
        )
        evidence.tanzil_import_created = False
        evidence.notes.append(
            "Snapshot already PRODUCTION_ACTIVE and production-valid; governed "
            "import/activation skipped (idempotent re-run)."
        )
    else:
        # --- Step 1: Tanzil pre-activation import (re-derives snapshot from artifact). ---
        import_result = TanzilPreActivationImporter.import_candidate(db)
        evidence.tanzil_snapshot_id = str(import_result.snapshot.id)
        evidence.tanzil_occurrence_count = import_result.occurrence_count
        evidence.tanzil_import_created = import_result.created
        if import_result.snapshot.id != AUTHORIZED_SNAPSHOT_ID:
            raise ConvergenceError(
                "Tanzil import produced an unexpected snapshot id "
                f"{import_result.snapshot.id!r}; expected {AUTHORIZED_SNAPSHOT_ID!r}."
            )
        evidence.notes.append(
            "Tanzil snapshot "
            + ("created" if import_result.created else "already present / verified")
            + f" with {import_result.occurrence_count} verse-level CorpusOccurrence rows."
        )

        # --- Step 2: Governed production activation (never hand-edited). ---
        try:
            result = TanzilProductionActivationService.activate(db)
            snapshot = result.snapshot
            evidence.notes.append(
                "Tanzil production activation executed via "
                "TanzilProductionActivationService.activate (audit recorded)."
            )
        except CorpusActivationRejected as exc:
            raise ConvergenceError(f"Tanzil activation rejected: {exc}") from exc

    evidence.activation_status = str(snapshot.activation_status)
    evidence.validation_status = str(snapshot.validation_status)
    evidence.is_production_validated = is_production_validated(snapshot)
    evidence.production_validation_failures = list(
        production_validation_failures(snapshot)
    )
    if not evidence.is_production_validated:
        raise ConvergenceError(
            "Snapshot failed production validation after activation: "
            + "; ".join(evidence.production_validation_failures)
        )

    # --- Step 3: Materialize word-level structural tokens from admitted QAC. ---
    qac_result = QacMorphologyImporter.import_tokens(db, AUTHORIZED_SNAPSHOT_ID)
    evidence.qac_tokens_persisted = qac_result.tokens_persisted
    evidence.qac_distinct_roots = qac_result.distinct_roots
    evidence.qac_source_sha256 = qac_result.source_sha256
    if not qac_result.reconciliation.get("verse_sets_equal"):
        raise ConvergenceError(
            "QAC verse set did not reconcile with the admitted Tanzil snapshot: "
            + json.dumps(qac_result.reconciliation.get("unmatched_qac_verses", [])[:5])
        )
    persisted_tokens = (
        db.query(models.StructuralToken)
        .filter(
            models.StructuralToken.snapshot_id == AUTHORIZED_SNAPSHOT_ID,
            models.StructuralToken.extraction_version == QAC_EXTRACTION_VERSION,
        )
        .count()
    )
    evidence.notes.append(
        f"QAC import persisted {qac_result.tokens_persisted} tokens; "
        f"{persisted_tokens} now present for the snapshot/extraction."
    )

    # --- Step 4: Methodology authority (already co-located in the authoritative DB). ---
    eligible = eligible_methodology_revision_ids(db)
    evidence.methodology_eligible_ids = eligible
    evidence.authorized_methodology_present = AUTHORIZED_METHODOLOGY_ID in eligible
    authorized = db.get(models.MethodologyRevision, AUTHORIZED_METHODOLOGY_ID)
    evidence.methodology_authority_failures = (
        methodology_authority_failures(authorized) if authorized is not None else ["revision absent"]
    )
    if not evidence.authorized_methodology_present:
        raise ConvergenceError(
            "Authorized methodology revision is not eligible in the target DB: "
            f"{AUTHORIZED_METHODOLOGY_ID}; failures="
            f"{evidence.methodology_authority_failures}"
        )
    return evidence


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--db",
        default=SQLALCHEMY_DATABASE_URL,
        help="SQLAlchemy URL of the authoritative runtime DB (default: lisanapp.db).",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON evidence only.")
    parser.add_argument(
        "--allow-side-store",
        action="store_true",
        help="Permit running against data/campaign/runtime.db (normally refused).",
    )
    args = parser.parse_args(argv)

    if "runtime.db" in args.db and not args.allow_side_store:
        print(
            "REFUSED: target looks like the non-governed campaign side store "
            f"({args.db}). The authoritative runtime DB is lisanapp.db. "
            "Pass --allow-side-store only if you really mean it.",
            file=sys.stderr,
        )
        return 2

    engine = create_engine(args.db, connect_args={"check_same_thread": False})
    Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    evidence = ConvergenceEvidence(
        database_url=engine.url.render_as_string(hide_password=True),
        schema_status="UNKNOWN",
        schema_expected_revisions=[],
        schema_actual_revisions=[],
    )
    try:
        with Session() as db:
            converge(db, evidence=evidence)
    except ConvergenceError as exc:
        payload: dict[str, Any] = asdict(evidence)
        payload["error"] = str(exc)
        if args.json:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            print(f"CONVERGENCE BLOCKED: {exc}", file=sys.stderr)
        return 1
    finally:
        engine.dispose()

    payload = asdict(evidence)
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print("CANONICAL RUNTIME CONVERGENCE — OK")
        print(f"  database                : {evidence.database_url}")
        print(f"  schema                  : {evidence.schema_status} {evidence.schema_actual_revisions}")
        print(f"  tanzil snapshot         : {evidence.tanzil_snapshot_id}")
        print(f"  tanzil occurrences      : {evidence.tanzil_occurrence_count}")
        print(f"  activation / validation : {evidence.activation_status} / {evidence.validation_status}")
        print(f"  production-valid        : {evidence.is_production_validated}")
        print(f"  qac tokens persisted    : {evidence.qac_tokens_persisted}")
        print(f"  qac distinct roots      : {evidence.qac_distinct_roots}")
        print(f"  qac source sha256       : {evidence.qac_source_sha256}")
        print(f"  methodology eligible    : {evidence.methodology_eligible_ids}")
        print(f"  authorized methodology  : {evidence.authorized_methodology_present}")
        for note in evidence.notes or []:
            print(f"    - {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
