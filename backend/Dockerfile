# Build argument for Python version
ARG PYTHON_VERSION=3.12

# --- Build stage ---
FROM python:${PYTHON_VERSION}-slim AS builder

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Install build dependencies for asyncpg
RUN apt-get update && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip toolchain
RUN python -m pip install --upgrade pip setuptools wheel

# Build Python wheels
COPY requirements.txt .
RUN pip install --user --no-warn-script-location -r requirements.txt

# --- Runtime stage ---
FROM python:${PYTHON_VERSION}-slim

# OCI labels
LABEL org.opencontainers.image.title="Farout Backend" \
      org.opencontainers.image.description="FastAPI backend for Star Citizen organization management" \
      org.opencontainers.image.vendor="Farout" \
      org.opencontainers.image.version="1.0.0"

# Create non-root app user
RUN addgroup --system --gid 10001 app \
 && adduser --system --uid 10001 --ingroup app --home /app app

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PATH=/app/.local/bin:$PATH

# Install only runtime dependencies (curl for healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=builder --chown=app:app /root/.local /app/.local

# Copy app source and migrations
COPY --chown=app:app app /app/app
COPY --chown=app:app migrations /app/migrations

USER 10001:10001
EXPOSE 8000

# Health check
HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -fsS --max-time 2 http://127.0.0.1:8000/health || exit 1

# Gunicorn with Uvicorn workers (configurable via GUNICORN_WORKERS env var)
CMD ["sh", "-c", "gunicorn -k uvicorn.workers.UvicornWorker -w ${GUNICORN_WORKERS:-2} -b 0.0.0.0:8000 app.main:app"]
