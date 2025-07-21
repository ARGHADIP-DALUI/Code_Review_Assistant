import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.code_review import Base
from app.api.v1.endpoints.submit_code import get_db
from app.main import app

# Use same SQLite file as production
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"  # ✅ update if needed

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Recreate tables before each session
@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

# Dependency override
@pytest.fixture()
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    from fastapi.testclient import TestClient
    return TestClient(app)
