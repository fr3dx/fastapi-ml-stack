import joblib
import numpy as np
from typing import List, Any

# Function to load a machine learning model with error handling
def load_model(model_path: str) -> Any:
    """
    Load a trained model from the specified file path.

    Args:
        model_path (str): The path to the saved model file.
        
    Returns:
        model: The loaded machine learning model.
    
    Raises:
        RuntimeError: If there is an error during model loading.
    """
    try:
        model = joblib.load(model_path)  # Load the model using joblib
        print("Model successfully loaded.")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        raise RuntimeError(f"Failed to load model from {model_path}: {str(e)}")

# Function to make predictions using the loaded model
def predict(model: Any, input_data: List[float]) -> np.ndarray:
    """
    Make a prediction using the provided model and input data.

    Args:
        model: The machine learning model used for prediction.
        input_data (List[float]): A list of input features to be predicted.

    Returns:
        np.ndarray: The model’s prediction, rounded to 6 decimal places.
    """
    # Convert input data to a NumPy array and prepare it for prediction
    input_array = np.array([input_data])  
    
    # Get the model’s prediction and round the results to 6 decimal places
    prediction = model.predict(input_array)
    return np.round(prediction, 6)
