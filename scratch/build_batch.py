import json
import hashlib
import random

data = json.load(open('scratch/db_output.json'))
processed = set(data['processed_roots'])
unprocessed = {k: v for k, v in data['structural_roots'].items() if k not in processed}

buckets = {
    'very sparse (1-5)': [],
    'sparse (6-20)': [],
    'medium (21-100)': [],
    'dense (101-300)': [],
    'very dense (>300)': []
}

for root, count in unprocessed.items():
    if count <= 5: buckets['very sparse (1-5)'].append((root, count))
    elif count <= 20: buckets['sparse (6-20)'].append((root, count))
    elif count <= 100: buckets['medium (21-100)'].append((root, count))
    elif count <= 300: buckets['dense (101-300)'].append((root, count))
    else: buckets['very dense (>300)'].append((root, count))

# Sort buckets deterministically
for b in buckets.values():
    b.sort(key=lambda x: (x[1], x[0]))

# Pick 8 from each (if possible) for a 40-root batch
batch = []
for k, b in buckets.items():
    # Pick a mix of low and high within the bucket deterministically
    if len(b) >= 8:
        selected = b[:4] + b[-4:]
    else:
        selected = b
    batch.extend([(r, c, k) for r, c in selected])

# If less than 40, pick more from medium
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

with open('scratch/batch08_plan.json', 'w') as f:
    json.dump(out, f, indent=2)

print("Batch generated:", out['batch_hash'])
