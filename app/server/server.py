from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn
import os
from database import init_db
from routers import health, tasks

# Load environment variables
load_dotenv()


# Initialize FastAPI app
app = FastAPI(
    title="Weekly Task Planner API",
    description="A FastAPI backend for managing weekly tasks with PostgreSQL database",
    version="0.1.0"
)

# Configure CORS for Angular frontend
# Get allowed origins from environment variable or use defaults
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
if allowed_origins_env:
    # Split by comma and strip whitespace from each origin
    allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]
else:
    allowed_origins = [
        "http://localhost:4200",  # Angular dev server
        "http://localhost:5173",  # Alternative port
    ]

print(f"CORS allowed origins: {allowed_origins}")  # Debug logging

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router)
app.include_router(tasks.router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    try:
        init_db()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Warning: Database initialization failed: {e}")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Weekly Task Planner API",
        "docs": "/docs",
        "health": "/api/health"
    }


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=5173,
        reload=True
    )
