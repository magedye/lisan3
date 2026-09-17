from pathlib import Path
import csv, hashlib, sys, re
ROOT=Path(__file__).resolve().parents[1]
errors=[]
def sha(p):
 h=hashlib.sha256();
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()
# MST-001 compare V2.1 base against archived uploaded zip extraction hashes via current extracted reference list embedded in base manifest hashes where possible
base=ROOT/'01_CANONICAL_BASE/Quran_Lisan_Complete_Package_V2.1.0'
if not (base/'00_PACKAGE_AUTHORITY.md').exists(): errors.append('MST-001 missing V2.1 base')
# use a generated expected hash file
expected=ROOT/'07_ACCEPTANCE/V21_EXPECTED_FILE_HASHES.csv'
if expected.exists():
 with expected.open(encoding='utf-8-sig') as f:
  for r in csv.DictReader(f):
   p=base/r['path']
   if not p.exists() or sha(p)!=r['sha256']: errors.append('MST-001 mismatch '+r['path'])
# MST-002
intake=ROOT/'05_REGISTRIES/MASTER_POST_V2_1_INTAKE.csv'
if intake.exists():
 with intake.open(encoding='utf-8-sig') as f:
  for r in csv.DictReader(f):
   actor=(r.get('source_actor') or '').upper(); disp=(r.get('disposition') or '').upper(); appr=(r.get('approval_ref') or '').strip()
   if actor in ('ASSISTANT','AGENT') and disp=='ACCEPTED' and not appr:
    errors.append('MST-002 non-owner accepted without approval '+(r.get('intake_id') or '?'))
# active prompt checks
p=(ROOT/'04_RUNTIME_PROMPTS/CURRENT_LISAN_METHODOLOGY_PROMPT.md').read_text(encoding='utf-8')
c=(ROOT/'04_RUNTIME_PROMPTS/CURRENT_SEMANTIC_CAMPAIGN_PROMPT.md').read_text(encoding='utf-8')
first=(ROOT/'00_START_HERE/04_FIRST_CODEX_REQUEST.md').read_text(encoding='utf-8')
if 'كل موضع' not in p or 'أغلبية' not in p: errors.append('MST-003 universal presence wording absent')
if 'MULTIPLE_LEXICAL_UNITS' in p: errors.append('MST-003 deprecated final outcome present in active methodology prompt')
if 'المعرفة قبل الاجتهاد' not in p or 'Root Descriptive Profile' not in first: errors.append('MST-004 descriptive knowledge requirement absent')
if 'قول ابن فارس أو جبل أو غيرهما لا يغير المنهج بذاته' not in p: errors.append('MST-005 external authority boundary absent')
if 'لا تستخدم نسبة رقمية' not in p and 'لا تستخدم نسبة رقمية' not in c: errors.append('MST-006 numeric confidence prohibition absent')
for phrase in ['لا تبدأ الحملة الواسعة','لا push/merge/tag/release','لا UI redesign']:
 if phrase not in first: errors.append('MST-008 missing scope phrase '+phrase)
status=(ROOT/'00_START_HERE/02_CURRENT_STATUS_AND_VERDICT.md').read_text(encoding='utf-8')
if 'P1..P8' not in status or 'لم يعتمد' not in status: errors.append('MST-009 open P1..P8 not stated')
# archive identities
ids=ROOT/'05_REGISTRIES/SOURCE_PACKAGE_IDENTITIES.csv'
if not ids.exists(): errors.append('MST-007 source identities missing')
else:
 with ids.open(encoding='utf-8-sig') as f:
  if sum(1 for _ in csv.DictReader(f)) < 6: errors.append('MST-007 insufficient archived source identities')
# MST-010 owner reaffirmation: non-negotiable root semantic unity
dirfile=ROOT/'02_CURRENT_OWNER_DIRECTIVES/06_ROOT_SEMANTIC_UNITY_NON_NEGOTIABLE.md'
if not dirfile.exists(): errors.append('MST-010 missing non-negotiable root semantic unity directive')
else:
 d=dirfile.read_text(encoding='utf-8')
 if 'ROOT_SEMANTIC_UNITY = NON_NEGOTIABLE' not in d or 'MAJORITY_SUBSTITUTE = FORBIDDEN' not in d:
  errors.append('MST-010 directive lacks hard invariant tokens')
if 'ROOT_SEMANTIC_UNITY = NON_NEGOTIABLE' not in p:
 errors.append('MST-010 active methodology prompt lacks non-negotiable root unity')

if errors:
 print('MASTER_VALIDATION: FAIL')
 for e in errors: print('-',e)
 sys.exit(1)
print('MASTER_VALIDATION: PASS')
