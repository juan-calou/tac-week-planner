from fastapi import APIRouter
from datetime import datetime
from database import check_db_connection
from models import HealthCheck

router = APIRouter()


@router.get("/api/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint to verify API and database connectivity."""
    db_status = "connected" if check_db_connection() else "disconnected"

    return HealthCheck(
        status="healthy" if db_status == "connected" else "unhealthy",
        database=db_status,
        timestamp=datetime.now()
    )
