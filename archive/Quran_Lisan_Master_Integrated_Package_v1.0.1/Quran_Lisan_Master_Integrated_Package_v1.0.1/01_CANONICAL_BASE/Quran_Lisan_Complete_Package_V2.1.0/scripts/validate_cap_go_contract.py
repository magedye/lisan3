from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
cat=json.loads((ROOT/'cap-go-01/CAP_GO_TEST_CATALOG.json').read_text(encoding='utf-8'))
schema=json.loads((ROOT/'cap-go-01/RESULT_SCHEMA.json').read_text(encoding='utf-8'))
assert cat['version']=='1.0.1' and cat['status']=='NOT_EXECUTED'
assert len(cat['tests'])==10 and len({t['test_id'] for t in cat['tests']})==10
assert all(t['result']=='NOT_EXECUTED' for t in cat['tests'])
assert schema['properties']['overall']['enum']==['PASS','FAIL']
print('CAP-GO contract: PASS (protocol defined, not executed)')
