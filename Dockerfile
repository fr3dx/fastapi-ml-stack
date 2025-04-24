# ----------------------
# Stage 1: Builder
# ----------------------
    FROM python:3.11-slim as builder

    # Add /root/.local/bin to the PATH
    ENV PATH=/root/.local/bin:$PATH
    # Make sure debconf doesn't try to ask questions interactively
    ENV DEBIAN_FRONTEND=noninteractive

    # Set the working directory
    WORKDIR /app
    
    # Copy only the requirements file to leverage Docker cache
    COPY app/requirements.txt .
    
    # Install system dependencies and Python packages, and avoid using root for pip install
    RUN pip install --no-cache-dir --user -r requirements.txt
    
    # ----------------------
    # Stage 2: Final image
    # ----------------------
    FROM python:3.11-slim
    
    # Set the working directory inside the container
    WORKDIR /app
    
    # Copy installed Python packages from the builder stage
    COPY --from=builder /root/.local /root/.local
    
    # Copy the rest of the application
    COPY app/ .
    
    # Make sure installed packages are found
    ENV PATH=/root/.local/bin:$PATH
    
    # Start the FastAPI application with Uvicorn
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    