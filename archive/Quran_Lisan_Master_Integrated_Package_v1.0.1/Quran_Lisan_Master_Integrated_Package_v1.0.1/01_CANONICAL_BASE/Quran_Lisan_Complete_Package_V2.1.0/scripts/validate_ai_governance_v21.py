from pathlib import Path
import sys,csv
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'contracts/python'))
from quran_lisan_contracts import *
from datetime import datetime, timezone

d=SemanticDecision(decision_id='dec_demo',run_id='run_demo',disposition=DecisionDisposition.UNRESOLVED,analysis_unit='ROOT_CONCEPT',completeness_profile_id='cmp_demo',concise_reason='insufficient')
assert d.authority_level==DecisionAuthorityLevel.RESEARCH_JUDGMENT

a=CanonicalAuthorization(authorization_id='auth_demo',run_id='run_demo',research_decision_id=d.decision_id,reviewer_actor_id='owner',decision=AuthorizationDecision.DEFER,decided_at=datetime.now(timezone.utc),rationale_brief='not yet canonical')
assert a.research_decision_id==d.decision_id

p=ROOT/'sources/AI_CAPABILITY_EVIDENCE_REGISTRY.csv'
with p.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
assert len(rows)>=8
assert all(r['explicit_limit'] for r in rows)
print('AI_GOVERNANCE_V2_1: PASS')
