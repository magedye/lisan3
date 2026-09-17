import json
import sqlite3
import sys
import os

def load_historical_roots():
    ledger_path = 'artifacts/semantic-campaign/CAMPAIGN_RESEARCH_LEDGER.json'
    if not os.path.exists(ledger_path):
        return set()
    with open(ledger_path, 'r', encoding='utf-8') as f:
        ledger = json.load(f)
    # The 'roots' key contains a dictionary of all historical processed roots
    if 'roots' in ledger and isinstance(ledger['roots'], dict):
        return set(ledger['roots'].keys())
    return set()

def load_db_roots():
    if not os.path.exists('lisanapp.db'):
        return set()
    conn = sqlite3.connect('lisanapp.db')
    cursor = conn.cursor()
    try:
        # Load any roots that have been processed in the semantic_claims table
        rows = cursor.execute("SELECT r.target_expression FROM semantic_claims c JOIN research_runs r ON c.research_run_id = r.id WHERE r.target_expression IS NOT NULL").fetchall()
        return set(r[0] for r in rows)
    except sqlite3.OperationalError:
        return set()

def validate_population(candidate_roots_file):
    historical = load_historical_roots()
    db_native = load_db_roots()
    
    all_processed = historical.union(db_native)
    
    with open(candidate_roots_file, 'r', encoding='utf-8') as f:
        candidates = set(json.load(f))
        
    overlap = candidates.intersection(all_processed)
    if overlap:
        print(f"VALIDATION FAILED: Candidate population contains {len(overlap)} previously processed roots: {list(overlap)}")
        sys.exit(1)
    
    print("VALIDATION PASSED: candidate_batch ∩ historical_processed_roots = ∅")
    sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python validate_batch_population.py <candidate_roots.json>")
        sys.exit(1)
    validate_population(sys.argv[1])
