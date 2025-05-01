# ======================
# Stage 1: Builder Stage
# ======================
FROM python:3.12.10-slim-bullseye as builder

# Set environment variables to customize Python and Debian behavior
ENV PATH=/root/.local/bin:$PATH \
    DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/install/lib/python3.12/site-packages:$PYTHONPATH

# Set the working directory
WORKDIR /fastapi-ml-stack

# Copy the healthcheck and requirements files
COPY healthcheck.py requirements.txt .

# Install dependencies without caching to reduce image size
RUN pip install --no-cache-dir \
    --prefix=/install -r requirements.txt

# Copy scripts to train model
COPY app app

# Train model
RUN python app/models/train_model.py

# ======================
# Stage 2: Runtime Stage
# ======================
FROM python:3.12.10-slim-bullseye

# Set the working directory
WORKDIR /fastapi-ml-stack

# Set environment variables for the runtime container
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app:$PYTHONPATH

# Copy the installed dependencies and files from the builder stage to the runtime environment
COPY --from=builder /install /usr/local
COPY --from=builder /fastapi-ml-stack/healthcheck.py .
COPY --from=builder /fastapi-ml-stack/requirements.txt .
COPY --from=builder /fastapi-ml-stack/app app

# Healthcheck
HEALTHCHECK CMD python healthcheck.py

# Application Execution
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
