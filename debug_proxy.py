import os
import time
import subprocess
import requests
import socket
import uvicorn
import threading
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from backend.infrastructure.database import Base, get_db
from backend.main import app

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]

api_port = get_free_port()
next_port = get_free_port()

test_engine = create_engine("sqlite:///e2e_debug.db")
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
Base.metadata.create_all(bind=test_engine)

def override_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = override_db

server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=api_port))
t = threading.Thread(target=server.run, daemon=True)
t.start()
time.sleep(1)

env = os.environ.copy()
env["BACKEND_URL"] = f"http://127.0.0.1:{api_port}"
p = subprocess.Popen(f"npm run start -- -p {next_port}", cwd="frontend", env=env, shell=True)
time.sleep(3)

print("FastAPI directly:")
res = requests.post(f"http://127.0.0.1:{api_port}/ask", json={"expression": "ضرب", "contract_type": "ROOT_CORE"})
print(res.status_code, res.text)

print("Next.js proxy:")
res = requests.post(f"http://127.0.0.1:{next_port}/api/ask", json={"expression": "ضرب", "contract_type": "ROOT_CORE"})
print(res.status_code, res.text)

p.terminate()
server.should_exit = True
