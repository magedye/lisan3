import json

from fastapi.openapi.utils import get_openapi

from backend.main import app


def export_openapi():
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        description=app.description,
        routes=app.routes,
    )
    with open("contracts/api/openapi.json", "w") as f:
        json.dump(openapi_schema, f, indent=2)
    print("OpenAPI spec generated at contracts/api/openapi.json")


if __name__ == "__main__":
    export_openapi()
