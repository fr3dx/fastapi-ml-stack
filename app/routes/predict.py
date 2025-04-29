from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from app.load_model import load_model, predict
from app.config import settings
import numpy as np
from typing import Dict, Union

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

# Load the pre-trained model
model = load_model(settings.model_path)

@router.post("/predict")
async def predict(
    request: Request,
    x1: str = Form(...),
    x2: str = Form(...)
) -> Jinja2Templates.TemplateResponse:
    """
    Handles prediction requests from the frontend, processes input data,
    and returns the prediction results.
    
    Args:
        request (Request): The FastAPI request object containing data from the frontend.
        x1 (str): The first input feature value from the form (received as a string).
        x2 (str): The second input feature value from the form (received as a string).
        
    Returns:
        TemplateResponse: The prediction results or an error page, depending on the outcome.
    """
    try:
        # Attempt to convert the input values (x1 and x2) to floating-point numbers.
        x1_float: float = float(x1)
        x2_float: float = float(x2)
               
        # Prepare the input data in a 2D NumPy array format, as expected by the model.
        input_data: np.ndarray = np.array([[x1_float, x2_float]])
        print(f"Input data as NumPy array: {input_data}")  # Debug log for input data.
        
        try:
            # Make the prediction using the loaded model and round the results to 6 decimal places.
            prediction: np.ndarray = model.predict(input_data)
            prediction = np.round(prediction, 6)  # Round predictions to 6 decimal places.
        except Exception as model_error:
            # Handle any errors encountered during model prediction.
            print(f"Model prediction error: {model_error}") 
            raise RuntimeError(f"Model prediction failed: {str(model_error)}") 

        # Return the prediction results, rendered using the 'result.html' template.
        return templates.TemplateResponse(
            "result.html",  # The template to render.
            {
                "request": request,  
                "prediction": {  # Pass the prediction results to the template.
                    "y1": prediction[0][0],  
                    "y2": prediction[0][1],  
                    "y3": prediction[0][2],  
                },
                "inputs": {"x1": x1_float, "x2": x2_float},  # Pass the input values (x1 and x2) to the template.
            },
        )

    # Error handling
    except ValueError as e:
        # Handle invalid input errors, such as non-numeric values.
        print(f"ValueError: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": "Invalid input. Please provide valid numbers."})

    except Exception as e:
        # Handle any other unexpected errors.
        print(f"Unexpected error: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": "Internal server error"})
