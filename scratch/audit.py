import json
import sqlite3
import hashlib

# 1. Load CAMPAIGN_RESEARCH_LEDGER.json
ledger_path = 'artifacts/semantic-campaign/CAMPAIGN_RESEARCH_LEDGER.json'
with open(ledger_path, 'r', encoding='utf-8') as f:
    ledger = json.load(f)

# 'roots' key contains root objects: { "root_arabic": ..., "batch": ... }
historical_roots = {}
batches = {}
for root_id, root_data in ledger.get('roots', {}).items():
    batch = root_data.get('batch')
    if batch:
        historical_roots[root_id] = root_data
        batches.setdefault(batch, []).append(root_id)

print("Ledger roots count:", len(historical_roots))
for b, roots in batches.items():
    print(f"Batch {b}: {len(roots)} roots")

# Check DB semantic_claims
conn = sqlite3.connect('lisanapp.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

db_processed = [row[0] for row in cursor.execute("SELECT r.target_expression FROM semantic_claims c JOIN research_runs r ON c.research_run_id = r.id").fetchall()]
print("DB-native processed roots:", db_processed)

# Reconstruct Total Unique Historical Processed Roots
all_processed = set(historical_roots.keys())
all_processed.update(db_processed)

print("Total unique processed roots:", len(all_processed))

# Admitted structural roots
structural = [row[0] for row in cursor.execute("SELECT root, COUNT(*) FROM structural_tokens WHERE root IS NOT NULL GROUP BY root").fetchall()]
print("Total admitted structural roots:", len(structural))

unprocessed = [r for r in structural if r not in all_processed]
print("True unprocessed roots count:", len(unprocessed))

# Now check the previous 40-root proposal
with open('scratch/batch08_plan.json', 'r') as f:
    plan = json.load(f)

proposed = plan['batch_roots']
invalid = [r for r in proposed if r in all_processed]
print("Invalid roots in proposed 40:", invalid)

