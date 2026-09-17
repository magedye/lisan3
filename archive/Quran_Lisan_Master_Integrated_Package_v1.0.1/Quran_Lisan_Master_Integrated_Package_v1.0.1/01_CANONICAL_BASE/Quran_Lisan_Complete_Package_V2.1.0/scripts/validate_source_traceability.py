from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[1]
with (ROOT/'registries/SOURCE_TRACEABILITY.csv').open(encoding='utf-8-sig',newline='') as f:
    rows=list(csv.DictReader(f))
keys={(r['object_kind'],r['object_id']) for r in rows}
missing=[]
for file,kind in [('REQUIREMENTS_REGISTRY.csv','REQUIREMENT'),('CONTROL_REGISTRY.csv','CONTROL'),('DECISION_REGISTER.csv','DECISION')]:
    with (ROOT/'registries'/file).open(encoding='utf-8-sig',newline='') as f:
        for r in csv.DictReader(f):
            id_=r.get('id')
            if (kind,id_) not in keys: missing.append(f'{kind}:{id_}')
if missing:
    raise SystemExit('SOURCE_TRACEABILITY: FAIL missing '+';'.join(missing))
print(f'SOURCE_TRACEABILITY: PASS ({len(rows)} rows)')
