from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
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
    
    Attributes:
        allowed_origins (str): Comma-separated list of allowed CORS origins
        model_path (str): File path to the pre-trained machine learning model
    """
    allowed_origins: str = "http://localhost,http://127.0.0.1"  # Default allowed CORS origins
    model_path: str = "regression_model.pkl"  # Path to pre-trained ML model

    class Config:
        env_file = ".env"  # Load variables from .env file
        env_file_encoding = 'utf-8'  # Explicit encoding for .env file

# Initialize application settings from environment variables
settings = Settings()

# Create FastAPI application instance
app = FastAPI()

# Parse allowed origins from comma-separated string to list
origins = [origin.strip() for origin in settings.allowed_origins.split(",")]

# Configure CORS middleware to handle cross-origin requests
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
    print("Model successfully loaded.")  # Log successful model loading
except Exception as e:
    print(f"Error loading model: {e}")  # Log error details
    raise RuntimeError(f"Failed to load model from {settings.model_path}: {str(e)}")

# Configure Jinja2 templates for HTML rendering and static files serving
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Pydantic model for request data validation
class Features(BaseModel):
    """
    Input features for model prediction.
    
    Attributes:
        x1 (float): First feature value
        x2 (float): Second feature value
    """
    x1: float
    x2: float


# Homepage route serving HTML template
@app.get("/")
async def home(request: Request):
    """
    Render the homepage with index.html template.
    
    Args:
        request (Request): FastAPI request object
        
    Returns:
        TemplateResponse: Rendered HTML template
    """
    return templates.TemplateResponse("index.html", {"request": request})


# Prediction endpoint that handles form submissions
@app.post("/predict")
async def predict(request: Request, x1: float = Form(...), x2: float = Form(...)):
    """
    Handle prediction requests from the frontend.
    
    Args:
        request (Request): FastAPI request object
        x1 (float): First feature value from form
        x2 (float): Second feature value from form
        
    Returns:
        TemplateResponse: Either prediction results or error page
        
    Notes:
        - Processes input data through the loaded ML model
        - Handles various error scenarios gracefully
        - Returns HTML responses for HTMX compatibility
    """
    print(f"Input data: x1 = {x1}, x2 = {x2}")  # Log input values
    try:
        # Prepare input data as numpy array for model prediction
        input_data = np.array([[x1, x2]])
        print(f"Input data as NumPy array: {input_data}")  # Log transformed input
        
        try:
            # Make prediction and round results to 6 decimal places
            prediction = model.predict(input_data)
            print(f"Model prediction: {prediction}")  # Log raw prediction
            prediction = np.round(prediction, 6)
        except Exception as model_error:
            print(f"Model prediction error: {model_error}")  # Log model error
            raise RuntimeError(f"Model prediction failed: {str(model_error)}")

        # Return structured response as HTML for HTMX
        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "prediction": {
                    "y1": prediction[0][0],
                    "y2": prediction[0][1],
                    "y3": prediction[0][2],
                },
                "inputs": {"x1": x1, "x2": x2},
            },
        )

    except ValueError as e:
        print(f"ValueError: {e}")  # Log value errors
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})

    except RuntimeError as e:
        print(f"RuntimeError: {e}")  # Log runtime errors
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})

    except Exception as e:
        print(f"Unexpected error: {e}")  # Log unexpected errors
        return templates.TemplateResponse("error.html", {"request": request, "error": "Internal server error"})