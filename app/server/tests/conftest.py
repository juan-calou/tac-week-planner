import pytest
import sqlite3
from pathlib import Path
from fastapi.testclient import TestClient
from server import app
from database import DATABASE_PATH, init_db

# Test database path
TEST_DB_PATH = Path(__file__).parent / "test_tasks.db"


@pytest.fixture(scope="function")
def test_db():
    """Create a test database for each test."""
    # Backup original database path
    import database
    original_path = database.DATABASE_PATH

    # Set test database path
    database.DATABASE_PATH = TEST_DB_PATH

    # Initialize test database
    init_db()

    yield TEST_DB_PATH

    # Cleanup: remove test database
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()

    # Restore original database path
    database.DATABASE_PATH = original_path


@pytest.fixture(scope="function")
def client(test_db):
    """Create a test client with test database."""
    # Update database module path for the test
    import database
    database.DATABASE_PATH = test_db

    with TestClient(app) as test_client:
        yield test_client
