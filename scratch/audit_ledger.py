import json
import sqlite3
import hashlib

ledger_path = 'artifacts/semantic-campaign/CAMPAIGN_RESEARCH_LEDGER.json'
with open(ledger_path, 'r', encoding='utf-8') as f:
    ledger = json.load(f)

# The keys in ledger['roots'] might be the roots themselves (e.g. 'ktb')
# Let's see what batches they belong to.
batch_counts = {}
unique_roots = set()

for root, details in ledger['roots'].items():
    unique_roots.add(root)
    # The batch identifier might be inside details, e.g. details['batch_id'] or details.get('source_batch')
    # Let's inspect details keys safely:
    # Example: 'batch_05', 'batch_06', 'batch_07', 'batch_01', etc.
    # We will just collect the strings that look like batches.
    found_batch = None
    if 'campaign_id' in details:
        found_batch = details['campaign_id']
    elif 'batch' in details:
        found_batch = details['batch']
    elif 'source_batch' in details:
        found_batch = details['source_batch']
    elif 'batch_id' in details:
        found_batch = details['batch_id']
        
    if found_batch:
        batch_counts[found_batch] = batch_counts.get(found_batch, 0) + 1
    else:
        # try searching values
        for v in details.values():
            if isinstance(v, str) and 'batch' in v.lower():
                found_batch = v
                break
        if found_batch:
            batch_counts[found_batch] = batch_counts.get(found_batch, 0) + 1
        else:
            batch_counts['unknown'] = batch_counts.get('unknown', 0) + 1

# If there's 248 roots, let's output this directly to a file
with open('scratch/audit_out.json', 'w', encoding='utf-8') as f:
    json.dump({
        'unique_count': len(unique_roots),
        'batches': batch_counts,
        'roots': list(unique_roots)
    }, f, indent=2)

print("Parsed ledger.")
