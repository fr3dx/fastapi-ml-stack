### BUILD THE STACK

# Define variables
$imageName = "localhost/fastapi-regression"
$containerName = "fastapi-regression"
$fullContainerName = "$containerName"+":latest"
$fullImageName = "$imageName"+":latest"

# Run model training script
Write-Host "Running model training script..."
python .\app\model.py

# Check if model training was successful
if ($LASTEXITCODE -ne 0) {
    Write-Host "Model training failed. Exiting..."
    exit 1
}

Write-Host "Model training completed successfully."

# Build the Podman image after model training
Write-Host "Building Podman image..."
podman build -t $fullContainerName .

# Check if Podman build was successful
if ($LASTEXITCODE -ne 0) {
    Write-Host "Podman build failed. Exiting..."
    exit 1
}

Write-Host "Podman image built successfully."
