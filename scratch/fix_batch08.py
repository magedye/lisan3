import json
import sqlite3
import hashlib

# 1. Load historical roots
with open('scratch/audit_out.json', 'r', encoding='utf-8') as f:
    audit_data = json.load(f)
historical_roots = set(audit_data['roots'])

# 2. Get all structural roots and their occurrences
conn = sqlite3.connect('lisanapp.db')
cursor = conn.cursor()
structural_rows = cursor.execute("SELECT root, COUNT(*) FROM structural_tokens WHERE root IS NOT NULL GROUP BY root").fetchall()

structural_roots = {r: c for r, c in structural_rows}
unprocessed_roots = {r: c for r, c in structural_roots.items() if r not in historical_roots}

print(f"Total Structural Roots: {len(structural_roots)}")
print(f"Historical Processed Roots: {len(historical_roots)}")
print(f"True Unprocessed Roots: {len(unprocessed_roots)}")

# 3. Create buckets for new selection
buckets = {
    'very sparse (1-5)': [],
    'sparse (6-20)': [],
    'medium (21-100)': [],
    'dense (101-300)': [],
    'very dense (>300)': []
}

for root, count in unprocessed_roots.items():
    if count <= 5: buckets['very sparse (1-5)'].append((root, count))
    elif count <= 20: buckets['sparse (6-20)'].append((root, count))
    elif count <= 100: buckets['medium (21-100)'].append((root, count))
    elif count <= 300: buckets['dense (101-300)'].append((root, count))
    else: buckets['very dense (>300)'].append((root, count))

for b in buckets.values():
    b.sort(key=lambda x: (x[1], x[0]))

# 4. Select 40 roots (8 from each bucket)
batch = []
for k, b in buckets.items():
    if len(b) >= 8:
        selected = b[:4] + b[-4:]
    else:
        selected = b
    batch.extend([(r, c, k) for r, c in selected])

while len(batch) < 40:
    for b in buckets['medium (21-100)']:
        if not any(r == b[0] for r, c, k in batch):
            batch.append((b[0], b[1], 'medium (21-100)'))
            if len(batch) >= 40: break

batch.sort(key=lambda x: x[0])
total_occurrences = sum(c for r, c, k in batch)
batch_roots = [r for r, c, k in batch]

hash_input = ','.join(batch_roots).encode('utf-8')
batch_hash = hashlib.sha256(hash_input).hexdigest()

out = {
    'batch_size': 40,
    'total_occurrences': total_occurrences,
    'batch_roots': batch_roots,
    'batch_hash': batch_hash,
    'details': batch
}

with open('scratch/batch08_repaired_plan.json', 'w') as f:
    json.dump(out, f, indent=2)

print("Repaired batch generated:", out['batch_hash'])

# 5. Check previous proposed overlapping roots
with open('scratch/batch08_plan.json', 'r') as f:
    old_plan = json.load(f)

invalid = [r for r in old_plan['batch_roots'] if r in historical_roots]
print("Invalid roots in old proposal:", len(invalid))
with open('scratch/invalid_roots.json', 'w') as f:
    json.dump(invalid, f)
