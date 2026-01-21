"""Vercel serverless function entry point."""
from mangum import Mangum
from server import app
from database import init_db

# Initialize database on cold start
try:
    init_db()
except Exception as e:
    print(f"Warning: Database initialization failed: {e}")

# Export handler for Vercel
handler = Mangum(app, lifespan="off")
