from pathlib import Path
import csv,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'prototype/structural-annotations/slm_full_fixture.csv'
with p.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
assert len(rows)==140
assert len({r['qac_word_ref'] for r in rows})==140
assert len({r['derived_form_group'] for r in rows})==16
assert all(r['root']=='س ل م' and r['semantic_evidence_allowed']=='false' for r in rows)
h=json.loads((ROOT/'prototype/held-out/SLM_HELD_OUT_CASES.json').read_text(encoding='utf-8'))
refs={r['qac_word_ref'] for r in rows}; assert len(h['cases'])==7 and set(h['cases'])<=refs
prof=json.loads((ROOT/'sources/external-dataset-registry/SYNONYMS_DATASET_PROFILE.json').read_text(encoding='utf-8'))
d=ROOT/'sources/datasets/Synonyms Dataset(1).xlsx'; got=hashlib.sha256(d.read_bytes()).hexdigest(); assert got==prof['sha256']
print('prototype fixtures: PASS')
