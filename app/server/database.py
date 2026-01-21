import os
import asyncio
from libsql_client import create_client_sync
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Turso database credentials from environment
TURSO_DATABASE_URL = os.getenv("TURSO_DATABASE_URL", "")
TURSO_AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN", "")

# Create Turso client
client = None
if TURSO_DATABASE_URL and TURSO_AUTH_TOKEN:
    try:
        # Convert libsql:// to https:// for HTTP protocol (more reliable than WebSocket)
        connection_url = TURSO_DATABASE_URL.replace("libsql://", "https://")
        client = create_client_sync(
            url=connection_url,
            auth_token=TURSO_AUTH_TOKEN
        )
        print("Connected to Turso database")
    except Exception as e:
        print(f"Failed to connect to Turso: {e}")
        client = None
else:
    print("Warning: TURSO_DATABASE_URL or TURSO_AUTH_TOKEN not set.")


def init_db():
    """Initialize the database and create tables if they don't exist."""
    if not client:
        print("No database client available")
        return

    try:
        # Create tasks table
        client.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                day_of_week TEXT NOT NULL,
                time_slot TEXT NOT NULL,
                task_type TEXT NOT NULL,
                completed INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization failed: {e}")
        raise


def get_db():
    """Get database client."""
    if not client:
        raise Exception("Database client not initialized")
    return client


def check_db_connection():
    """Check if database connection is working."""
    try:
        if client:
            result = client.execute("SELECT 1")
            return True
        return False
    except Exception:
        return False
