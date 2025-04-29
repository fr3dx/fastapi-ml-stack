from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from typing import Dict

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

# Route to serve the homepage with the 'index.html' template
@router.get("/")
async def home(request: Request) -> Jinja2Templates.TemplateResponse:
    """
    Renders the homepage using the 'index.html' template.
    
    Args:
        request (Request): The FastAPI request object.
        
    Returns:
        TemplateResponse: The rendered HTML template for the homepage.
    """
    return templates.TemplateResponse("index.html", {"request": request})
