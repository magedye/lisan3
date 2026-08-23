import os
import socket
import threading
import time
import subprocess

import pytest
import uvicorn
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.infrastructure.database import Base, get_db
from backend.main import app


def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def e2e_server():
    api_port = 8000
    next_port = get_free_port()
    host = "127.0.0.1"

    db_path = "e2e_test.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    test_engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    
    import alembic.config
    import alembic.command
    alembic_cfg = alembic.config.Config("backend/alembic.ini")
    alembic_cfg.set_main_option("script_location", "backend/alembic")
    alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")
    alembic.command.upgrade(alembic_cfg, "head")

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

    # Start Next.js frontend
    env = os.environ.copy()
    env["BACKEND_URL"] = f"http://{host}:{api_port}"
    env["PORT"] = str(next_port)
    
    # Run Next.js in dev mode for tests to avoid needing a fresh build every time, 
    # but the prompt requires "Next.js production UI". We will assume `npm run build` 
    # has been run before the E2E tests, or we can just run `npm start`.
    frontend_process = subprocess.Popen(
        f"npm run start -- -p {next_port}",
        cwd="frontend",
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        shell=True
    )

    base_url = f"http://{host}:{next_port}"
    
    # Wait for Next.js to be ready
    import urllib.request
    import urllib.error
    max_retries = 20
    for _ in range(max_retries):
        try:
            urllib.request.urlopen(base_url)
            break
        except urllib.error.URLError:
            time.sleep(0.5)
    else:
        frontend_process.kill()
        raise RuntimeError(f"Next.js failed to start on {base_url} after {max_retries/2} seconds.")

    yield {"base_url": base_url, "db_session": TestSession, "engine": test_engine, "api_url": f"http://{host}:{api_port}"}

    server.should_exit = True
    thread.join(timeout=2.0)
    frontend_process.terminate()
    try:
        frontend_process.wait(timeout=2.0)
    except subprocess.TimeoutExpired:
        frontend_process.kill()
        
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except Exception:
            pass
