# REMOVE ALL CONTAINER IMAGES (FORCE)

# Get a list of all podman images
$images = podman images -q

# Check if there are images available
if ($images.Count -eq 0) {
    Write-Host "No Podman images found."
} else {
    Write-Host "The following Podman images are available for removal:"
    $images | ForEach-Object { Write-Host $_ }

    # Confirm removal
    $confirmation = Read-Host "Are you sure you want to remove all these images? (Y/N)"
    
    if ($confirmation -eq "Y" -or $confirmation -eq "y") {
        Write-Host "Removing all Podman images..."
        
        # Loop through each image and remove it
        foreach ($image in $images) {
            Write-Host "Removing image: $image"
            podman rmi -f $image
        }
        
        Write-Host "All Podman images have been removed."
    } else {
        Write-Host "Operation aborted. No images were removed."
    }
}
