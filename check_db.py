from sqlalchemy import create_engine

from backend.infrastructure.database import Base

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(bind=engine)

# SQLAlchemy can expose the raw connection
conn = engine.raw_connection()
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(semantic_claims)")
print("Columns in memory db semantic_claims:", [col[1] for col in cursor.fetchall()])
conn.close()
