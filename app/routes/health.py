from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()

# Endpoint for health check
@router.get("/health")
async def health_check():
    """
    A simple health check endpoint to confirm that the API is up and running.
    
    Returns:
        JSON response: {"status": "ok"} if the service is healthy.
    """
    try:
        # You can perform any necessary health checks here, e.g., database connection, etc.
        # For now, just return a simple 'ok' status
        return {"status": "ok"}  # This is a simple health check response

    except Exception as e:
        # In case of an error, return an error message with a non-200 status code
        return {"status": "error", "message": str(e)}

# Endpoint for prediction requests, triggered by form submissions