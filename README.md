# FastAPI + HTMX + Linear Regression

This project is a **FastAPI** web application with a **linear regression model**. It uses **HTMX** for dynamic content and is containerized with **Podman** (or Docker).

## Setup

- **Build stack**: `build_stack.ps1`
- **Build and run stack**: `build_and_run_stack.ps1`
- **Remove all containers/images**: `remove_all_container_images.ps1`

## API Example

POST request with PowerShell:
```powershell
Invoke-RestMethod -Method POST -Uri http://127.0.0.1:8000/predict -Body '{"features": [1.0, 1.0]}' -ContentType "application/json"
