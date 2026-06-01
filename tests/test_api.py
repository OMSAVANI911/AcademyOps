import os
import sys
import sqlite3
import pytest

# Tell Python to look inside the 'src' folder for our toolkit
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Point to a fake database BEFORE importing your code so we don't ruin real data
import repository
repository.DB_PATH = 'test_academyops.db'

from api import app
from repository import LeadRepository

@pytest.fixture
def setup_database():
    # Setup: Create a fresh, empty test database
    with sqlite3.connect(repository.DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL UNIQUE,
                source TEXT,
                stage TEXT NOT NULL,
                notes TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')
    yield
    # Teardown: Delete the fake database after tests run
    if os.path.exists(repository.DB_PATH):
        os.remove(repository.DB_PATH)

@pytest.fixture
def client(setup_database):
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_lead_api(client):
    """Test that the API can successfully create a new lead."""
    response = client.post('/api/v1/leads', json={
        "name": "Test Student",
        "phone": "555-9999",
        "source": "Website",
        "stage": "New"
    })
    assert response.status_code == 201
    assert "id" in response.get_json()

def test_get_leads_api(client):
    """Test that the API can list leads."""
    response = client.get('/api/v1/leads')
    assert response.status_code == 200
    assert "data" in response.get_json()

def test_duplicate_phone_error(setup_database):
    """Test that the repository rejects duplicate phone numbers."""
    repo = LeadRepository()
    repo.create("First User", "111-2222", "Web", "New")
    
    with pytest.raises(repository.DuplicateLeadError):
        repo.create("Duplicate User", "111-2222", "Web", "New")