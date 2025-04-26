# FastAPI + HTMX + Linear Regression

This project is a **FastAPI**-based web application powered by a **multi-output linear regression model**, trained using `scikit-learn`. It includes a simple **HTMX** frontend for user interaction and is fully containerized using **Podman** or **Docker**.

## Tech stack

- **Python 3.11**
- **FastAPI**
- **HTMX**
- **scikit-learn**
- **Pydantic**
- **Podman** or **Docker**


## Features

- **Regression Model**: Predicts 3 outputs (y₁, y₂, y₃) from 2 inputs (x₁, x₂):
  - y₁ = 3x₁ + 2x₂  
  - y₂ = x₁ − x₂  
  - y₃ = −x₁ + 4x₂  
- **API Endpoint**: `/predict` — accepts a JSON body with `features: [x1, x2]`, returns predicted `y1`, `y2`, and `y3`
- **Frontend**: HTMX-powered form with real-time result display
- **Containerized Stack**: Model training and API are containerized and reproducible

## Backend Overview

- `/predict`: POST endpoint for prediction
- `/`: Serves the HTMX frontend
- `regression_model.pkl`: Trained and saved multi-output regression model
- `Features` and `Predictions`: Defined using Pydantic for type safety and validation
- `.env` support with `pydantic.BaseSettings` (for future config separation)

## Setup

Use PowerShell scripts for stack management:

| Task | Script |
|------|--------|
| Build containers only | `build_stack.ps1` |
| Build and run full stack | `build_and_run_stack.ps1` |
| Remove all containers and images | `remove_all_container_images.ps1` |

## API Usage Example

Send a POST request with two input features:

```powershell
Invoke-RestMethod -Method POST -Uri http://127.0.0.1:8000/predict -Body '{"features": [1.0, 1.0]}' -ContentType "application/json"

