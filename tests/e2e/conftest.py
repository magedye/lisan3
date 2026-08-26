import os
import socket
import subprocess
import threading
import time
from pathlib import Path

import pytest
import uvicorn
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.domain.services.corpus.activation import TanzilProductionActivationService
from backend.domain.services.corpus.importer import TanzilPreActivationImporter
from backend.infrastructure.database import get_db
from backend.main import app


def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def e2e_server(tmp_path_factory):
    api_port = get_free_port()
    next_port = get_free_port()
    host = "127.0.0.1"

    db_path = tmp_path_factory.mktemp("lisan-e2e") / "e2e_test.db"

    test_engine = create_engine(
        f"sqlite:///{db_path.as_posix()}",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    import alembic.command
    import alembic.config

    alembic_cfg = alembic.config.Config("alembic.ini")
    alembic_cfg.set_main_option("script_location", "alembic")
    alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path.as_posix()}")
    alembic.command.upgrade(alembic_cfg, "head")

    with TestSession() as session:
        TanzilPreActivationImporter.import_candidate(session)
        TanzilProductionActivationService.activate(session)

    def override_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_db

    server_config = uvicorn.Config(app, host=host, port=api_port, log_level="error")
    server = uvicorn.Server(server_config)

    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    env = os.environ.copy()
    env["BACKEND_URL"] = f"http://{host}:{api_port}"
    env["PORT"] = str(next_port)

    frontend_dir = Path("frontend").resolve()
    next_entrypoint = frontend_dir / "node_modules" / "next" / "dist" / "bin" / "next"
    subprocess.run(
        ["node", str(next_entrypoint), "build"],
        cwd=frontend_dir,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )
    frontend_process = subprocess.Popen(
        ["node", str(next_entrypoint), "start", "-p", str(next_port)],
        cwd=frontend_dir,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        shell=False,
    )

    base_url = f"http://{host}:{next_port}"

    # Wait for Next.js to be ready
    import urllib.error
    import urllib.request

    max_retries = 20
    for _ in range(max_retries):
        try:
            urllib.request.urlopen(base_url)
            break
        except urllib.error.URLError:
            time.sleep(0.5)
    else:
        frontend_process.kill()
        raise RuntimeError(
            f"Next.js failed to start on {base_url} after {max_retries / 2} seconds."
        )

    yield {
        "base_url": base_url,
        "db_session": TestSession,
        "engine": test_engine,
        "api_url": f"http://{host}:{api_port}",
    }

    frontend_process.terminate()
    try:
        frontend_process.wait(timeout=10.0)
    except subprocess.TimeoutExpired:
        frontend_process.kill()
        frontend_process.wait(timeout=10.0)

    server.should_exit = True
    thread.join(timeout=10.0)
    app.dependency_overrides.pop(get_db, None)
    test_engine.dispose()
