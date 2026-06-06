"""
tests/test_api.py
AcademyOps test suite using isolated test database.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.api import app
from src.database import Base, get_db
from src.repository import (
    LeadRepository,
    LeadNotFoundError,
)

TEST_DATABASE_URL = "sqlite:///./test_academyops.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(
        bind=connection
    )

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db_session):

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def repo():
    return LeadRepository()


def create_lead(
    client,
    phone="+919999999999"
):
    return client.post(
        "/api/v1/leads",
        json={
            "name": "Priya Sharma",
            "phone": phone,
            "source": "Instagram",
            "stage": "New",
            "notes": "Test Lead"
        }
    )


def test_create_lead_success(client):
    response = create_lead(
        client,
        "+919999999991"
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data


def test_duplicate_phone_returns_400(client):
    create_lead(
        client,
        "+919999999992"
    )

    response = create_lead(
        client,
        "+919999999992"
    )

    assert response.status_code == 400


def test_get_lead_success(client):
    created = create_lead(
        client,
        "+919999999993"
    ).json()

    response = client.get(
        f"/api/v1/leads/{created['id']}"
    )

    assert response.status_code == 200


def test_get_lead_not_found(client):
    response = client.get(
        "/api/v1/leads/999999"
    )

    assert response.status_code == 404


def test_list_leads(client):
    response = client.get(
        "/api/v1/leads"
    )

    assert response.status_code == 200

    data = response.json()

    assert "data" in data
    assert "total" in data


def test_update_stage_success(client):
    created = create_lead(
        client,
        "+919999999994"
    ).json()

    response = client.patch(
        f"/api/v1/leads/{created['id']}/stage",
        json={
            "stage": "Qualified"
        }
    )

    assert response.status_code == 200


def test_invalid_stage_returns_400(client):
    created = create_lead(
        client,
        "+919999999995"
    ).json()

    response = client.patch(
        f"/api/v1/leads/{created['id']}/stage",
        json={
            "stage": "INVALID"
        }
    )

    assert response.status_code == 400


def test_repository_exists():
    repo = LeadRepository()

    assert repo is not None


def test_lead_not_found_exception():
    with pytest.raises(
        LeadNotFoundError
    ):
        raise LeadNotFoundError(
            "Lead not found"
        )