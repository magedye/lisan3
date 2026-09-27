import pytest
from backend.domain.services.internal_snapshot import InternalSnapshotService
from backend.domain.services.tool_reality import ToolRealityService
from backend.domain.services.semantic_memory import SemanticMemoryService
from backend.domain.models import SemanticClaim, ResearchRun
from unittest.mock import MagicMock

def test_t01_t30_tool_execution_honesty(test_db):
    run = ResearchRun(id='run_t30', target_contract='ROOT_CORE', target_expression='test', methodology_revision='1', corpus_snapshot='1', authority_context={})
    test_db.add(run)
    test_db.commit()
    
    # Tool Reality Enforces actual execution
    with pytest.raises(ValueError, match='Tool cannot be SUCCEEDED if it was not actually executed'):
        ToolRealityService.record_tool_execution(
            db=test_db, run_id='run_t30', tool_id='vector_search', trigger='user',
            actual_execution=False, execution_status='SUCCEEDED', source_role='DISCOVERY'
        )

def test_t01_t37_external_snapshot_contamination(test_db):
    claim = SemanticClaim(id='claim_t37', research_run_id='run_t37', contract_type='ROOT_CORE')
    test_db.add(claim)
    test_db.commit()
    
    snapshot = InternalSnapshotService.create_snapshot(
        test_db, claim, corpus_identity='c1', methodology_version='v1'
    )
    assert snapshot.snapshot_hash is not None
    
    # Test immutability
    snapshot.evidence_refs = ['modified']
    with pytest.raises(ValueError, match='InternalResultSnapshotRecord is strictly immutable.'):
        test_db.add(snapshot)
        test_db.commit()
    test_db.rollback()

def test_t01_t41_latest_wins_memory_conflict(test_db):
    from backend.domain.services.semantic_memory import SemanticMemoryService
    from backend.domain import schemas
    claim1 = SemanticClaim(id='claim_1', contract_type='ROOT', result_strength='STRONG', falsification_status='PASSED')
    test_db.add(claim1)
    test_db.commit()
    
    mem1 = SemanticMemoryService.admit(test_db, schemas.SemanticMemoryCreate(
        claim_id='claim_1', target_type='ROOT', target_expression='test', scope='UNIVERSAL', reliability='TRUSTED', reopen_if=['x']
    ))
    
    claim2 = SemanticClaim(id='claim_2', contract_type='ROOT', result_strength='STRONG', falsification_status='PASSED')
    test_db.add(claim2)
    test_db.commit()
    
    # T41: New entry with same target_expression should detect conflict
    mem2 = SemanticMemoryService.admit(test_db, schemas.SemanticMemoryCreate(
        claim_id='claim_2', target_type='ROOT', target_expression='test', scope='UNIVERSAL', reliability='PROVISIONAL'
    ))
    assert mem2.conflict_state == 'OPEN_CONFLICT'

def test_t01_t43_dependency_reopen(test_db):
    from backend.domain.services.semantic_memory import SemanticMemoryService
    from backend.domain import schemas
    claim_a = SemanticClaim(id='claim_a', contract_type='ROOT')
    test_db.add(claim_a)
    test_db.commit()
    
    mem_a = SemanticMemoryService.admit(test_db, schemas.SemanticMemoryCreate(claim_id='claim_a', target_type='ROOT', target_expression='A', scope='LOCAL', reliability='PROVISIONAL'))
    
    claim_b = SemanticClaim(id='claim_b', contract_type='ROOT')
    test_db.add(claim_b)
    test_db.commit()
    
    mem_b = SemanticMemoryService.admit(test_db, schemas.SemanticMemoryCreate(claim_id='claim_b', target_type='ROOT', target_expression='B', scope='LOCAL', reliability='PROVISIONAL', dependencies=[mem_a.id]))
    
    # Reopen A
    mem_a_reopened = SemanticMemoryService.reopen(test_db, mem_a.id, schemas.SemanticMemoryReopenRequest(new_evidence_refs=[], counterevidence_refs=[], revision_reason='test'))
    
    test_db.refresh(mem_b)
    assert mem_b.reliability == 'DISPUTED'
    assert mem_b.conflict_state == 'OPEN_CONFLICT'

def test_t01_t53_fake_memory_save_disclosure(test_db):
    from backend.domain.services.semantic_memory import SemanticMemoryService
    from backend.domain import schemas
    claim = SemanticClaim(id='claim_t53', contract_type='ROOT', result_strength='WEAK')
    test_db.add(claim)
    test_db.commit()
    
    # Should fail admission to TRUSTED if not STRONG
    with pytest.raises(ValueError, match='Admission Gate Failed'):
        SemanticMemoryService.admit(test_db, schemas.SemanticMemoryCreate(
            claim_id='claim_t53', target_type='ROOT', target_expression='T53', scope='LOCAL', reliability='TRUSTED', reopen_if=['1']
        ))

