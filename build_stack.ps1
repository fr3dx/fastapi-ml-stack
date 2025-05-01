### BUILD THE STACK

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
