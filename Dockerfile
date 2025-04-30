# ======================
# Stage 1: Builder Stage
# ======================
FROM python:3.12.10-slim-bullseye as builder

# Set environment variables to customize Python and Debian behavior
ENV PATH=/root/.local/bin:$PATH \
    DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements file into the container
COPY app/requirements.txt ./

# Install dependencies in the container without caching to reduce image size
RUN pip install --no-cache-dir \
    --prefix=/install -r requirements.txt

# ======================
# Stage 2: Runtime Stage
# ======================
FROM python:3.12.10-slim-bullseye

# Healthcheck
HEALTHCHECK CMD python /app/healthcheck.py

# Set environment variables for the runtime container
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the installed dependencies from the builder stage to the runtime environment
COPY --from=builder /install /usr/local

# Copy healthcheck script
COPY ./healthcheck.py /app/

# Copy the application code into the container
COPY ./app /app/app

# Application Execution
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]