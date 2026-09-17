from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'contracts/python'))
from quran_lisan_contracts import records, tools
from pydantic import BaseModel
OUT=ROOT/'contracts/schemas'; OUT.mkdir(parents=True,exist_ok=True)
models=[]
for mod in (records,tools):
    for name,obj in vars(mod).items():
        if isinstance(obj,type) and issubclass(obj,BaseModel) and obj not in (BaseModel,records.StrictRecord,tools.ToolModel): models.append((name,obj))
seen=set()
for name,obj in sorted(models):
    if name in seen: continue
    seen.add(name)
    (OUT/f'{name}.schema.json').write_text(json.dumps(obj.model_json_schema(),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'generated {len(seen)} schemas')
