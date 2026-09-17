from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[1]; R=ROOT/'registries'
def rows(n):
    with (R/n).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
statuses={r['value'] for r in rows('STATUS_REGISTRY.csv') if r['domain']=='CONTRACT'}
for n in ['CONTROL_REGISTRY.csv','TERMINOLOGY_REGISTRY.csv','REQUIREMENTS_REGISTRY.csv','OPEN_QUESTIONS.csv']:
    for r in rows(n):
        s=r.get('status','')
        if s and s not in statuses: raise AssertionError(f'{n}: unknown status {s}')
assert not list(R.glob('FINAL_*')), 'duplicate FINAL_* registries prohibited'
assert len(rows('CONTROL_REGISTRY.csv'))==52
assert len(rows('REQUIREMENTS_REGISTRY.csv'))==95
assert len(rows('DECISION_REGISTER.csv'))==47
print('registries: PASS')
