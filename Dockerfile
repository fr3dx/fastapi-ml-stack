# ----------------------
# Stage 1: Builder
# ----------------------
    FROM python:3.11-slim as builder

    # Set the working directory
    WORKDIR /app
    
    # Copy only the requirements file to leverage Docker cache
    COPY requirements.txt .
    
    # Install system dependencies and Python packages
    RUN apt-get update && apt-get install -y build-essential && \
        pip install --upgrade pip && \
        pip install --user -r requirements.txt
    
    # ----------------------
    # Stage 2: Final image
    # ----------------------
    FROM python:3.11-slim
    
    # Set the working directory inside the container
    WORKDIR /app
    
    # Copy installed Python packages from the builder stage
    COPY --from=builder /root/.local /root/.local
    
    # Copy the rest of the application
    COPY . .
    
    # Make sure installed packages are found
    ENV PATH=/root/.local/bin:$PATH
    
    # Start the FastAPI application with Uvicorn
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    