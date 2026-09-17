import json
import sqlite3

conn = sqlite3.connect('lisanapp.db')
c = conn.cursor()

manifest = json.load(open('artifacts/semantic-campaign/BATCH_08_MANIFEST.json'))
batch08_roots = [r['root_buckwalter'] for r in manifest['roots']]

runs = c.execute("SELECT id, target_expression FROM research_runs").fetchall()
b08_runs = [r for r in runs if r[1] in batch08_roots]

print(f"Total Batch 08 ResearchRuns in DB: {len(b08_runs)}")

claims = c.execute("SELECT id FROM semantic_claims").fetchall()
b08_claims = [c_id for c_id in claims if c_id[0] in [r[0] for r in b08_runs]]

print(f"Total Batch 08 Claims in DB: {len(b08_claims)}")
