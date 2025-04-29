from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware
from app.routes import routes


# Initialize FastAPI application
app = FastAPI()

for router in routes:
    app.include_router(router)

# CORS configuration for security
# The origins list is split from the allowed_origins string in the settings and stripped of any extra whitespace.
origins = [origin.strip() for origin in settings.allowed_origins.split(",")]

# Add the CORSMiddleware to handle cross-origin resource sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins for cross-origin requests
    allow_credentials=True,  # Allows cookies to be included in cross-origin requests
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers in cross-origin requests
)

# Add the router with all application routes
app.include_router(router)

# Serve static files from the "app/static" directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")
