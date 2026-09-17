from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'PACKAGE_MANIFEST.json').read_text(encoding='utf-8'))
for e in manifest['files']:
    p=ROOT/e['path'];
    if not p.is_file(): raise AssertionError('missing '+e['path'])
    h=hashlib.sha256(p.read_bytes()).hexdigest();
    if h!=e['sha256']: raise AssertionError('hash mismatch '+e['path'])
print(f"package manifest: PASS ({len(manifest['files'])} files)")
