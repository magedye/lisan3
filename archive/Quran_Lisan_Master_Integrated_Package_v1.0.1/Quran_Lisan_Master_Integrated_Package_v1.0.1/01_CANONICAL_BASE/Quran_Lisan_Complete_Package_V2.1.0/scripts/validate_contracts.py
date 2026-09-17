from pathlib import Path
import sys
from datetime import datetime, timezone
from pydantic import ValidationError
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'contracts/python'))
from quran_lisan_contracts.records import *
from quran_lisan_contracts.enums import *

def must_fail(fn,label):
    try: fn()
    except (ValidationError,ValueError): return
    raise AssertionError('expected failure: '+label)
now=datetime.now(timezone.utc)
must_fail(lambda: SourceIdentity(source_id='src_demo',name='x',source_class=SourceClass.QURAN_TEXT,source_role=SourceRole.CANONICAL_TEXT,version='1',unexpected='x'),'unknown fields')
must_fail(lambda: ConfidenceComponent(component_id='cmp_demo',name='x',band=ConfidenceBand.SUPPORTED,evaluated=True,reason='x',numeric_value=0.9),'numeric confidence without calibration')
must_fail(lambda: EvidenceRelation(evidence_relation_id='ev_demo',run_id='run_demo',direction=EvidenceDirection.SUPPORTS,role=EvidenceRole.TEXTUAL,note='x'),'evidence missing target/refs')
r=ExecutionReceipt(receipt_id='rec_demo',run_id='run_demo',actor=ExecutionActor.TOOL,actor_id='TL-01',actor_version='2.0.0',status=ExecutionStatus.SUCCEEDED,started_at=now,ended_at=now,input_digest='a',output_digest='b')
assert r.receipt_id=='rec_demo'
print('contracts: PASS')
