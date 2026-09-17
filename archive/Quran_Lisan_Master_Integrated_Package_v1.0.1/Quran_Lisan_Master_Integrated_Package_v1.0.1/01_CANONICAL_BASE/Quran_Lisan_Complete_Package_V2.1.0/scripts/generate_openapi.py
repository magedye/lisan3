from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'contracts/python')); sys.path.insert(0,str(ROOT/'contracts/api'))
from app_contract import app
p=ROOT/'contracts/api/openapi.json'; p.write_text(json.dumps(app.openapi(),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(p)
