from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
steps=['generate_schemas.py','generate_openapi.py','validate_contracts.py','validate_tool_gateway_contract.py','validate_registries.py','validate_traceability.py','validate_source_traceability.py','validate_prototype_fixture.py','validate_cap_go_contract.py']
for s in steps: subprocess.check_call([sys.executable,str(ROOT/'scripts'/s)])
subprocess.check_call([sys.executable,str(ROOT/'scripts/validate_tanzil.py'),'--profile-only'])
print('CLOSURE_SELF_TESTS: PASS')
print('NOTE: semantic/model tests, product integration tests, and CAP-GO-01 remain execution-phase tests.')
