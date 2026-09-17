from __future__ import annotations
from pathlib import Path
import argparse, hashlib, zipfile, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]

def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,default=ROOT.parent/f'{ROOT.name}.zip')
    args=ap.parse_args()
    subprocess.check_call([sys.executable,str(ROOT/'scripts'/'validate_package.py')])
    out=args.output.resolve(); out.parent.mkdir(parents=True,exist_ok=True)
    if out.exists(): out.unlink()
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(ROOT.rglob('*')):
            if not p.is_file() or '__pycache__' in p.parts or p.suffix=='.pyc': continue
            arc=(Path(ROOT.name)/p.relative_to(ROOT)).as_posix()
            z.write(p,arc)
    digest=sha256(out)
    sidecar=Path(str(out)+'.sha256')
    sidecar.write_text(f'{digest}  {out.name}\n',encoding='utf-8')
    print(out)
    print(digest)
    print(sidecar)
if __name__=='__main__': main()
