"""
tests/test_api.py
Full pytest suite for AcademyOps.
"""

import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# --- ADD "src." BEFORE THESE IMPORTS ---
from src.database import Base, get_db
from src.api import app
from src.repository import LeadRepository

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_academyops.db")
TEST_DATABASE_URL = "sqlite:///./test_academyops.db"

test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=test_engine)

@pytest.fixture(scope="session", autouse=True)
def create_test_schema():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture()
def db_session():
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture()
def client(db_session):
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture()
def repo():
    return LeadRepository()

def _api_create_lead(client, **overrides) -> dict:
    payload = {
        "name": "Priya Sharma",
        "phone": "+919876543210",
        "source": "Instagram",
        "stage": "New",
        "notes": "Test Lead"
    }
    payload.update(overrides)
    return client.post("/api/v1/leads", json=payload).json()

def test_create_lead_success(client):
    data = _api_create_lead(client)
    assert "id" in data

def test_get_lead_not_found_returns_404(client):
    assert client.get("/api/v1/leads/999999").status_code == 404

def test_repository_get_raises_lead_not_found(db_session, repo):
    from src.repository import LeadNotFoundError
    with pytest.raises(LeadNotFoundError):
        repo.get(db_session, lead_id=999999)
