import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.domain import models
from backend.infrastructure.database import Base, get_db
from backend.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_overrides():
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()


client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Lisanapp Backend is running"}


def test_research_run_persistence():
    db = TestingSessionLocal()
    # Clean up before
    db.query(models.ResearchRun).delete()
    db.commit()

    # Create
    run = models.ResearchRun(
        id="run_test_1",
        target_contract="ROOT_CORE",
        target_expression="TEST",
        methodology_revision="1.0",
        corpus_snapshot="snap1",
        authority_context={"user": "local"},
    )
    db.add(run)
    db.commit()

    # Read
    saved_run = db.query(models.ResearchRun).filter_by(id="run_test_1").first()
    assert saved_run is not None
    assert saved_run.target_expression == "TEST"
    assert saved_run.current_stage == models.ResearchStage.PREFLIGHT.value

    # Test mapping round-trip and validation failure
    # Pydantic schemas enforce type safety
    from backend.domain.schemas import ResearchRunCreate

    try:
        ResearchRunCreate.model_validate(
            {
                "target_contract": "ROOT_CORE",
                "target_expression": "TEST",
                "corpus_snapshot": "snapshot_test",
                "authority_context": {},
                # missing required methodology_revision
            }
        )
        assert False, "Should fail validation"
    except ValueError:
        pass

    db.close()


def test_slice_a_end_to_end():
    db = TestingSessionLocal()
    db.query(models.SemanticClaim).delete()
    db.query(models.ResearchRun).delete()
    db.commit()

    cursor = engine.raw_connection().cursor()
    cursor.execute("PRAGMA table_info(semantic_claims)")
    cols = [col[1] for col in cursor.fetchall()]
    print("SCHEMA IN TEST_BACKEND:", cols)

    # 1. Ask Lisan (No evidence)
    response = client.post(
        "/ask", json={"expression": "ضرب", "contract_type": "ROOT_CORE"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "INSUFFICIENT_EVIDENCE"

    # 2. Create Research Run
    response = client.post(
        "/runs",
        json={
            "target_contract": "ROOT_CORE",
            "target_expression": "ضرب",
            "methodology_revision": "v7.1",
            "corpus_snapshot": "current",
            "authority_context": {"initiator": "local_user"},
        },
    )
    assert response.status_code == 200
    run_data = response.json()
    assert run_data["target_expression"] == "ضرب"
    assert "id" in run_data
    run_id = run_data["id"]

    # 3. Retrieve Durable Checkpoint
    response = client.get(f"/runs/{run_id}")
    assert response.status_code == 200
    retrieved = response.json()
    assert retrieved["id"] == run_id
    assert retrieved["current_stage"] == "PREFLIGHT"

    db.close()


def test_alembic_models_parity(tmp_path):
    import alembic.command
    import alembic.config
    from sqlalchemy import create_engine, inspect

    from backend.infrastructure.database import Base

    db_path = tmp_path / "test_alembic_parity.db"

    try:
        database_url = f"sqlite:///{db_path.as_posix()}"
        engine = create_engine(database_url)
        alembic_cfg = alembic.config.Config("alembic.ini")
        alembic_cfg.set_main_option("script_location", "alembic")
        alembic_cfg.set_main_option("sqlalchemy.url", database_url)

        alembic.command.upgrade(alembic_cfg, "head")

        inspector = inspect(engine)
        alembic_tables = set(inspector.get_table_names())

        model_tables = set(Base.metadata.tables.keys())
        alembic_tables.discard("alembic_version")

        assert alembic_tables == model_tables, (
            f"Mismatch between Alembic tables ({len(alembic_tables)}) and Model tables ({len(model_tables)}). Diff: {alembic_tables.symmetric_difference(model_tables)}"
        )
        for table_name, table in Base.metadata.tables.items():
            migrated_columns = {
                column["name"] for column in inspector.get_columns(table_name)
            }
            model_columns = set(table.columns.keys())
            assert migrated_columns == model_columns, (
                f"Column mismatch for {table_name}: "
                f"{migrated_columns.symmetric_difference(model_columns)}"
            )
    finally:
        if "engine" in locals():
            engine.dispose()
