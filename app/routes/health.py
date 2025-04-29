from fastapi import APIRouter
from typing import Dict

router = APIRouter()

# Endpoint for health check
@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    A simple health check endpoint to confirm that the API is up and running.
    
    Returns:
        JSON response: {"status": "ok"} if the service is healthy.
    """
    try:
        # You can perform any necessary health checks here, e.g., database connection, etc.
        return {"status": "ok"}  # Simple health check response
    except Exception as e:
        return {"status": "error", "message": str(e)}
