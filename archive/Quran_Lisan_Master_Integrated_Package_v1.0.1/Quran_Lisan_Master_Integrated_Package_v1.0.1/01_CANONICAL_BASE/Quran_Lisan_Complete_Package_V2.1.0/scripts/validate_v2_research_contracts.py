from pathlib import Path
import sys
from pydantic import ValidationError
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'contracts/python'))
from quran_lisan_contracts import *

def must_fail(fn,label):
    try: fn()
    except (ValidationError,ValueError): return
    raise AssertionError('expected failure: '+label)

steps=[
 SemanticDerivationStep(step_id='stp_root',run_id='run_demo',stage=SemanticDerivationStage.ROOT_CONTRIBUTION,statement='x',establishment=ClaimEstablishment.SUPPORTED,evidence_scope='root'),
 SemanticDerivationStep(step_id='stp_ctx',run_id='run_demo',stage=SemanticDerivationStage.CONTEXT_REQUIREMENT,statement='y',establishment=ClaimEstablishment.SUPPORTED,evidence_scope='verse'),
 SemanticDerivationStep(step_id='stp_local',run_id='run_demo',stage=SemanticDerivationStage.LOCAL_MEANING,statement='z',establishment=ClaimEstablishment.TENTATIVE,evidence_scope='verse'),
]
SemanticDerivationChain(chain_id='chn_demo',run_id='run_demo',target_id='term_demo',analysis_unit='LOCAL_MEANING',steps=steps,final_statement='z')
must_fail(lambda: SemanticDerivationChain(chain_id='chn_bad',run_id='run_demo',target_id='term_demo',analysis_unit='LOCAL_MEANING',steps=list(reversed(steps))), 'out of order chain')
b=SemanticBoundary(boundary_id='bnd_demo',run_id='run_demo',target_id='root_demo',items=[SemanticBoundaryItem(boundary_item_id='bni_demo',category=BoundaryCategory.UNKNOWN,statement='غير محسوم',scope='root')])
assert b.items[0].category==BoundaryCategory.UNKNOWN
must_fail(lambda: MOADeepReviewReport(review_id='moa_demo',run_id='run_demo',findings=[MOARoleFinding(role=MOARole.ROOT_CORE_ANALYST,finding='x'),MOARoleFinding(role=MOARole.FALSIFICATION_ANALYST,finding='y')],aggregator_result='x',consensus_is_evidence=True),'MOA consensus evidence')
print('V2 research contracts: PASS')
