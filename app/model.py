import numpy as np
from sklearn.linear_model import LinearRegression
import joblib
from typing import Any

# Input data (features) and corresponding outputs (targets)

# y1 = 3x₁ + 2x₂
# y2 = x₁ - x₂
# y3 = -x₁ + 4x₂

X: np.ndarray = np.array([
    [1.0, 2.0],
    [2.0, 1.0],
    [0.0, 3.0],
    [3.0, 0.0],
    [1.0, 1.0],
    [4.0, 1.0]
])

Y: np.ndarray = np.array([
    [7, -1, 7],
    [8, 1, 2],
    [6, -3, 12],
    [9, 3, -3],
    [5, 0, 3],
    [14, 3, 0]
])

# Create and train the linear regression model
model: LinearRegression = LinearRegression()
model.fit(X, Y)

# Save the trained model to a file
joblib.dump(model, 'app/regression_model.pkl')

# Test the model by making predictions with the same input
predictions: np.ndarray = model.predict(X)

# Print the predictions alongside the actual values for comparison
print("Predictions:\n", predictions)
print("Actual values:\n", Y)

# Optional: If you want to load and test the saved model
loaded_model: LinearRegression = joblib.load('app/regression_model.pkl')

# Test the model with a new input
new_input: np.ndarray = np.array([[2.0, 3.0]])  # Example test input
predicted_output: np.ndarray = loaded_model.predict(new_input)

# Print the new prediction
print("\nPrediction for new input [2.0, 3.0]:", predicted_output)
