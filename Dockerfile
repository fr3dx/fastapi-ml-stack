# ======================
# Stage 1: Builder Stage
# ======================
FROM python:3.11-slim as builder

# Environment Configuration
ENV PATH=/root/.local/bin:$PATH \
    DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

# Application Setup
WORKDIR /app

# Dependency Installation
COPY app/requirements.txt ./
RUN pip install \
    --default-timeout=100 \
    --no-cache-dir \
    --user \
    -r requirements.txt

# ======================
# Stage 2: Runtime Stage
# ======================
FROM python:3.11-slim

# Environment Configuration
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1

# Application Setup
WORKDIR /app

# Copy Dependencies from Builder
COPY --from=builder /root/.local /root/.local

# Copy Application Code
COPY app/ ./

# Health Check (Recommended Addition)
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Application Execution
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]