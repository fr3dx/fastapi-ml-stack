### BUILD AND RUN THE STACK

# Define variables
$imageName = "localhost/fastapi-regression"
$containerName = "fastapi-regression"
$fullContainerName = "$containerName"+":latest"
$fullImageName = "$imageName"+":latest"

# Build the Podman images
Write-Host "Building Podman image..."
podman build --format docker -t $fullContainerName .

# Check if Podman build was successful
if ($LASTEXITCODE -ne 0) {
    Write-Host "Podman build failed. Exiting..."
    exit 1
}

Write-Host "Podman image built successfully."

# Start the Podman container
Write-Host "Starting Podman container..."
podman run -d -p 8000:8000 --name $containerName $fullImageName

# Wait for give the container some time to initialize
Start-Sleep -Seconds 3

# Check if the container is actually running
$containerStatus = podman ps -q --filter "name=$containerName"

if ([string]::IsNullOrEmpty($containerStatus)) {
    Write-Host "Podman container start failed or container not running. Exiting..."
    exit 1
}

Write-Host "Podman container started successfully."
