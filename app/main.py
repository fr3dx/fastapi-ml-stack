from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import numpy as np
import joblib
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
import os

# Configuration settings loaded from environment variables
class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables.
    Default values are used if not specified in .env file.
    """
    allowed_origins: str = "http://localhost,http://127.0.0.1"  # Default allowed CORS origins
    model_path: str = "regression_model.pkl"  # Path to pre-trained ML model
    
    class Config:
        env_file = ".env"  # Load variables from .env file
        env_file_encoding = 'utf-8'  # Explicit encoding for .env file

# Initialize application settings
settings = Settings()

# Create FastAPI application instance
app = FastAPI()

# Parse allowed origins from comma-separated string to list
origins = [origin.strip() for origin in settings.allowed_origins.split(",")]

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allow cookies in cross-origin requests
    allow_methods=["*"],     # Allow all HTTP methods
    allow_headers=["*"],     # Allow all HTTP headers
)

# Load pre-trained ML model with error handling
try:
    model = joblib.load(settings.model_path)
except Exception as e:
    raise RuntimeError(f"Failed to load model from {settings.model_path}: {str(e)}")

# Configure Jinja2 templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Request model for prediction endpoint
class Features(BaseModel):
    """Input features for model prediction"""
    features: list[float]  # List of feature values

# Homepage route serving HTML template
@app.get("/")
async def home(request: Request):
    """Render homepage with index.html template"""
    return templates.TemplateResponse("index.html", {"request": request})

# Prediction endpoint
@app.post("/predict")
async def predict(data: Features):
    """
    Make predictions using the pre-trained model.
    
    Args:
        data: Features model containing list of input features
        
    Returns:
        JSONResponse: Contains predictions and input values
        or error message with appropriate status code
    """
    try:
        # Validate input features
        if len(data.features) != 2:
            raise ValueError("Exactly 2 features required")
            
        # Convert and prepare input data
        x1 = float(data.features[0])
        x2 = float(data.features[1])
        input_data = np.array([[x1, x2]])
        
        # Make prediction and round results
        prediction = model.predict(input_data)
        prediction = np.round(prediction, 6)

        # Return structured response
        return JSONResponse(content={
            'predictions': {
                'y1': prediction[0][0],
                'y2': prediction[0][1],
                'y3': prediction[0][2]
            },
            'inputs': {
                'x1': x1,
                'x2': x2
            }
        })
    except ValueError as e:
        # Handle client-side errors (400 Bad Request)
        return JSONResponse(status_code=400, content={"error": str(e)})
    except Exception as e:
        # Handle server-side errors (500 Internal Server Error)
        return JSONResponse(status_code=500, content={"error": "Internal server error"})