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
async def predict(request: Request, x1: str = Form(...), x2: str = Form(...)):
    """
    Handle prediction requests from the frontend.
    
    Args:
        request (Request): The FastAPI request object that contains data sent from the frontend.
        x1 (str): The first feature value provided in the form, received as a string.
        x2 (str): The second feature value provided in the form, received as a string.
        
    Returns:
        TemplateResponse: Returns either the prediction results or an error page with a proper message.
        
    Notes:
        - The function processes input data and uses the pre-trained machine learning model to make predictions.
        - Error handling is implemented to catch issues like invalid input or problems with the model.
        - The function is designed to return HTML responses, compatible with HTMX for dynamic page updates.
    """
    try:
        # Attempt to convert the string inputs (x1 and x2) to floating-point numbers.
        x1_float = float(x1)
        x2_float = float(x2)
               
        # Prepare the input data in the format required by the model, which is a 2D NumPy array.
        input_data = np.array([[x1_float, x2_float]])
        print(f"Input data as NumPy array: {input_data}")  # Log the input data in array format for debugging.
        
        try:
            # Make a prediction using the loaded model, and round the results to 6 decimal places.
            prediction = model.predict(input_data)
            prediction = np.round(prediction, 6)  # Round predictions to 6 decimal places.
        except Exception as model_error:
            # Handle any errors occurring during the model prediction.
            print(f"Model prediction error: {model_error}") 
            raise RuntimeError(f"Model prediction failed: {str(model_error)}") 

        # Return the prediction results by rendering the 'result.html' template with the prediction data.
        return templates.TemplateResponse(
            "result.html",  # The template to render.
            {
                "request": request,  
                "prediction": {  # Pass the prediction results to the template.
                    "y1": prediction[0][0],  
                    "y2": prediction[0][1],  
                    "y3": prediction[0][2],  
                },
                "inputs": {"x1": x1_float, "x2": x2_float},  # Pass the inputs (x1 and x2) to the template.
            },
        )

    except ValueError as e:
        # This block catches errors if the conversion of inputs to float fails (e.g., if input is non-numeric).
        print(f"ValueError: {e}") 
        # Return an error page with a message indicating the input is invalid.
        return templates.TemplateResponse("error.html", {"request": request, "error": "Invalid input, please provide valid numbers."})

    except Exception as e:
        # This block handles any other unexpected errors that may occur in the process.
        print(f"Unexpected error: {e}") 
        # Return a generic error page indicating an internal server error.
        return templates.TemplateResponse("error.html", {"request": request, "error": "Internal server error"})
