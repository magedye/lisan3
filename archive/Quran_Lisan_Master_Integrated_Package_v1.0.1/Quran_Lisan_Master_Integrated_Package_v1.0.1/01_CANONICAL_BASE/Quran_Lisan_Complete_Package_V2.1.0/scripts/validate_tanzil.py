from pathlib import Path
import argparse,json,hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
prof=json.loads((ROOT/'sources/TANZIL_SOURCE_PROFILE.json').read_text(encoding='utf-8'))
ap=argparse.ArgumentParser(); ap.add_argument('file',nargs='?'); ap.add_argument('--profile-only',action='store_true'); args=ap.parse_args()
assert prof['sha256']=='ac0724796cbbda0f4801470fbbd11d0f3c5802067bae0493466d0128b0c667af'
assert prof['size_bytes']==1334737 and prof['verse_records']==6236 and prof['canonical_normalization']=='NONE'
if args.profile_only or not args.file:
    print('tanzil profile: PASS'); sys.exit(0)
p=Path(args.file); b=p.read_bytes();
if len(b)!=prof['size_bytes']: raise SystemExit('FAIL size')
if hashlib.sha256(b).hexdigest()!=prof['sha256']: raise SystemExit('FAIL sha256')
if b.startswith(b'\xef\xbb\xbf'): raise SystemExit('FAIL BOM')
text=b.decode('utf-8');
if '\r\n' in text or '\r' in text: raise SystemExit('FAIL newline')
records=[x for x in text.splitlines() if x and not x.startswith('#')]
if len(records)!=prof['verse_records']: raise SystemExit(f'FAIL verse records {len(records)}')
print('tanzil artifact: PASS')
