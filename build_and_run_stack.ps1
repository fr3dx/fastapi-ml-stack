# Define the image and container name in a variable NOT READY
$imageName = "localhost/fastapi-regression"
$containerName = "fastapi-regression"
$fullImageName = "$imageName:latest"

# Step: Run model training script
Write-Host "Running model training script..."
python .\app\model.py

# Check if model training was successful
if ($LASTEXITCODE -ne 0) {
    Write-Host "Model training failed. Exiting..."
    exit 1
}

Write-Host "Model training completed successfully."

# Step: Build the Podman image after model training
Write-Host "Building Podman image..."
podman build -t fastapi-regression:latest .

# Check if Podman build was successful
if ($LASTEXITCODE -ne 0) {
    Write-Host "Podman build failed. Exiting..."
    exit 1
}

Write-Host "Podman image built successfully."

# Step: Start the Podman container
Write-Host "Starting Podman container..."
podman run -d -p 8000:8000 --name fastapi-regression localhost/fastapi-regression:latest

# Wait for 3 seconds to give the container some time to initialize
Start-Sleep -Seconds 3

# Check if the container is actually running (we can use podman ps to check this)
$containerStatus = podman ps -q --filter "name=fastapi-regression"

if ([string]::IsNullOrEmpty($containerStatus)) {
    Write-Host "Podman container start failed or container not running. Exiting..."
    exit 1
}

Write-Host "Podman container started successfully."
