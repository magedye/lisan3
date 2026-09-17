from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
exclude={'PACKAGE_MANIFEST.json','SHA256SUMS.txt'}
files=[]
for p in sorted(ROOT.rglob('*')):
    if not p.is_file() or p.name in exclude or '__pycache__' in p.parts: continue
    rel=p.relative_to(ROOT).as_posix(); files.append({'path':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size_bytes':p.stat().st_size})
manifest={'package':'Quran_Lisan_Complete_Package_V2.1.0','version':'2.1.0','self_excluded':True,'files':files}
(ROOT/'PACKAGE_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
allf=files+[{'path':'PACKAGE_MANIFEST.json','sha256':hashlib.sha256((ROOT/'PACKAGE_MANIFEST.json').read_bytes()).hexdigest(),'size_bytes':(ROOT/'PACKAGE_MANIFEST.json').stat().st_size}]
(ROOT/'SHA256SUMS.txt').write_text(''.join(f"{e['sha256']}  {e['path']}\n" for e in allf),encoding='utf-8')
print('V2 manifest built',len(files))
