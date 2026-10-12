import argparse
import json
import os
import sys
from collections import Counter

# Ensure PYTHONPATH handles local imports natively
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def validate_closure(db_path, results_path, campaign_id):
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
        and r.authority_context.get("campaign") == campaign_id
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
    parser = argparse.ArgumentParser(description="Validate closure of a campaign.")
    parser.add_argument("--db", default="lisanapp.db", help="Path to SQLite database")
    parser.add_argument(
        "--results", required=True, help="Path to campaign results JSON"
    )
    parser.add_argument(
        "--campaign", required=True, help="Campaign ID to validate (e.g. batch08)"
    )

    args = parser.parse_args()

    db = os.path.abspath(args.db)
    res = os.path.abspath(args.results)

    if not validate_closure(db, res, args.campaign):
        sys.exit(1)
    sys.exit(0)
