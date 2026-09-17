from __future__ import annotations
import csv, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
reg=ROOT/'contracts/tools/TOOL_REGISTRY.csv'
openapi=ROOT/'contracts/api/openapi.json'
with reg.open(encoding='utf-8-sig',newline='') as f:
    rows=list(csv.DictReader(f))
spec=json.loads(openapi.read_text(encoding='utf-8'))
errors=[]
for row in rows:
    path=row['path']; method=row['method'].lower()
    if path not in spec.get('paths',{}):
        errors.append(f"{row['tool_id']}: path missing from OpenAPI: {path}")
        continue
    if method not in spec['paths'][path]:
        errors.append(f"{row['tool_id']}: method mismatch registry={method.upper()} path={path}; OpenAPI={','.join(spec['paths'][path].keys())}")
if errors:
    raise SystemExit('TOOL_GATEWAY_CONTRACT: FAIL\n'+'\n'.join(errors))
print(f'TOOL_GATEWAY_CONTRACT: PASS ({len(rows)} tools)')
