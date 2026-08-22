import sys

from schemathesis.cli import execute


def run_fuzzer():
    # Execute schemathesis on our FastAPI application via its OpenAPI spec
    # We use ASGI directly instead of starting a live server to be faster and simpler in CI
    print("Running API contract fuzzing on Lisanapp backend...")
    
    args = [
        "run", 
        "--app", "backend.main:app", 
        "/openapi.json", 
        "--checks", "not_a_server_error",
        "--hypothesis-max-examples", "10", 
        "--endpoints", "^/governance/.*|^/claims/.*/publish" 
    ]
    
    sys.exit(execute(args))

if __name__ == "__main__":
    run_fuzzer()
