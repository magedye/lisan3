import json
import os
import sys
from collections import Counter

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def validate_closure(db_path, results_path):
    if not os.path.exists(results_path):
        print(f"FAILED: Results file not found at {results_path}")
        return False

    with open(results_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            print(f"FAILED: Invalid JSON in {results_path}")
            return False

    engine = create_engine(f"sqlite:///{db_path}")
    Session = sessionmaker(bind=engine)
    session = Session()

    from backend.domain.models import (
        ResearchRun,
        SemanticClaim,
        VerificationRecord,
    )

    reported_runs = {r["run_id"] for r in results}
    reported_claims = {r["claim_id"] for r in results}
    reported_verdicts = Counter(r["verdict"] for r in results)
    reported_canonical = Counter(r["canonical_state"] for r in results)

    all_runs = session.query(ResearchRun).all()
    db_runs = [
        r
        for r in all_runs
        if isinstance(r.authority_context, dict)
        and r.authority_context.get("campaign") == "batch08"
    ]
    db_run_ids = {r.id for r in db_runs}

    if reported_runs != db_run_ids:
        print(
            f"FAILED: DB runs count ({len(db_run_ids)}) != Reported ({len(reported_runs)})"
        )
        return False

    db_claims = (
        session.query(SemanticClaim)
        .filter(SemanticClaim.research_run_id.in_(db_run_ids))
        .all()
    )
    db_claim_ids = {c.id for c in db_claims}

    if reported_claims != db_claim_ids:
        print("FAILED: DB claims mismatch")
        return False

    db_verifications = (
        session.query(VerificationRecord)
        .filter(VerificationRecord.claim_id.in_(db_claim_ids))
        .all()
    )

    db_accepted = len([c for c in db_claims if c.canonical_state == "ACCEPTED"])
    if db_accepted != reported_canonical["ACCEPTED"]:
        print(
            f"FAILED: DB Accepted ({db_accepted}) != Reported ({reported_canonical['ACCEPTED']})"
        )
        return False

    print("SUCCESS: REPORTED_STATE == DB_DERIVED_STATE")
    return True


if __name__ == "__main__":
    db = os.path.abspath("lisanapp.db")
    res = os.path.abspath("artifacts/semantic-campaign/BATCH_08_CAMPAIGN_RESULTS.json")
    if not validate_closure(db, res):
        sys.exit(1)
    sys.exit(0)
