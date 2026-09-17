from pathlib import Path
import hashlib,json,zipfile,sys
ROOT=Path(__file__).resolve().parents[1]
# Excludes manifest from its own hash list and release ZIP/sidecar.
files=[]
for p in sorted(ROOT.rglob('*')):
    if not p.is_file() or p.name in {'PACKAGE_MANIFEST.json','SHA256SUMS.txt'}: continue
    if '__pycache__' in p.parts: continue
    rel=p.relative_to(ROOT).as_posix(); h=hashlib.sha256(p.read_bytes()).hexdigest(); files.append({'path':rel,'sha256':h,'size_bytes':p.stat().st_size})
manifest={'package':'Quran_Lisan_Implementation_Closure_Pack','version':'1.0.1','self_excluded':True,'files':files}
(ROOT/'PACKAGE_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# include manifest in checksums but not checksum file itself
sumfiles=files+[{'path':'PACKAGE_MANIFEST.json','sha256':hashlib.sha256((ROOT/'PACKAGE_MANIFEST.json').read_bytes()).hexdigest(),'size_bytes':(ROOT/'PACKAGE_MANIFEST.json').stat().st_size}]
(ROOT/'SHA256SUMS.txt').write_text(''.join(f"{e['sha256']}  {e['path']}\n" for e in sumfiles),encoding='utf-8')
print(f'manifest built: {len(files)} files')
