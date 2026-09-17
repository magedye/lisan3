from pathlib import Path
import urllib.parse,urllib.request,argparse,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]; prof=json.loads((ROOT/'sources/TANZIL_SOURCE_PROFILE.json').read_text(encoding='utf-8'))
ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True); args=ap.parse_args()
url=prof['acquisition_endpoint']+'?'+urllib.parse.urlencode(prof['acquisition_profile'])
out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True); stage=out.with_suffix(out.suffix+'.staging')
with urllib.request.urlopen(url,timeout=60) as r: stage.write_bytes(r.read())
subprocess.check_call([sys.executable,str(ROOT/'scripts/validate_tanzil.py'),str(stage)])
stage.replace(out); print(out)
