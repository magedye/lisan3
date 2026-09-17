from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[1]
def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
req=rows(ROOT/'registries/REQUIREMENTS_REGISTRY.csv')
tr=rows(ROOT/'acceptance/TRACEABILITY_MATRIX.csv')
tests=rows(ROOT/'acceptance/TEST_CATALOG.csv')
req_ids={r['id'] for r in req}; test_ids={r['test_id'] for r in tests}; tr_ids={r['requirement_id'] for r in tr}
assert req_ids==tr_ids, f'traceability missing/extra: {req_ids-tr_ids} {tr_ids-req_ids}'
for r in tr:
    tids=[x for x in r['test_ids'].split('|') if x]
    missing=[x for x in tids if x not in test_ids]
    if missing: raise AssertionError(f"{r['requirement_id']} unknown tests {missing}")
print(f'traceability: PASS ({len(req_ids)} requirements, {len(test_ids)} tests)')
