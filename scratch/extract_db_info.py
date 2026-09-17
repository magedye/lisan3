import sqlite3
import json

conn = sqlite3.connect('lisanapp.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

def fetch(query):
    cursor.execute(query)
    return [dict(row) for row in cursor.fetchall()]

data = {}

# Roots in the universe
structural = fetch("SELECT root, COUNT(*) as count FROM structural_tokens WHERE root IS NOT NULL GROUP BY root")
data['structural_roots'] = {r['root']: r['count'] for r in structural}

# Processed roots
runs = fetch("SELECT target_expression FROM research_runs")
data['processed_roots'] = list(set([r['target_expression'] for r in runs if r['target_expression']]))

# Claims and canonical states
claims = fetch("SELECT c.id, c.canonical_state, c.research_state, r.target_expression as root FROM semantic_claims c JOIN research_runs r ON c.research_run_id = r.id")
data['claims'] = claims

print(json.dumps(data, indent=2))
