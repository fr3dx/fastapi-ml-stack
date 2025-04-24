# run_model_and_app.ps1

# 1. Step: Run model training script
Write-Host "Running model training script..."
python .\model.py

# Check if model training was successful
if ($LASTEXITCODE -ne 0) {
    Write-Host "Model training failed. Exiting..."
    exit 1
}

Write-Host "Model training completed successfully."

# 2. Step: Build the Podman image after model training
Write-Host "Building Podman image..."
podman build -t fastapi-regression:latest .

# Check if Podman build was successful
if ($LASTEXITCODE -ne 0) {
    Write-Host "Podman build failed. Exiting..."
    exit 1
}

Write-Host "Podman image built successfully."

# Check if Podman build was successful
Write-Host "Starting Podman image..."
podman run -d -p 8000:8000 fastapi-regression:latest

if ($LASTEXITCODE -ne 0) {
    Write-Host "Podman build failed. Exiting..."
    exit 1
}

Write-Host "Podman container started successfully."
