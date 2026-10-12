import pytest
import schemathesis
from hypothesis import settings

from backend.main import app

# Load schema from ASGI app
schema = schemathesis.openapi.from_asgi("/openapi.json", app)
# Apply the Slice G filter
schema = schema.include(path_regex="^/governance/.*|^/claims/.*/publish")

@schema.parametrize()
@settings(max_examples=10)
def test_api(case):
    response = case.call()
    case.validate_response(response, checks=(schemathesis.checks.not_a_server_error,))

if __name__ == "__main__":
    import sys

    import pytest
    sys.exit(pytest.main(["-v", __file__]))
