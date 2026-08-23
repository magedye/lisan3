import json
from pathlib import Path

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
    rendered = json.dumps(openapi_schema, indent=2, ensure_ascii=False) + "\n"
    targets = (
        Path("contracts/api/openapi.json"),
        Path("frontend/openapi.json"),
    )
    for target in targets:
        with target.open("w", encoding="utf-8", newline="\n") as output:
            output.write(rendered)
        print(f"OpenAPI spec generated at {target.as_posix()}")


if __name__ == "__main__":
    export_openapi()
