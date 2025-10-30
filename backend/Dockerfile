FROM python:3.12-slim

# Create non-root app user
RUN addgroup --system --gid 10001 app \
 && adduser  --system --uid 10001 --ingroup app --home /app app

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app

# Install build deps for asyncpg + curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
      gcc curl \
  && rm -rf /var/lib/apt/lists/*

# Upgrade pip toolchain (optional but recommended)
RUN python -m pip install --upgrade pip setuptools wheel

# Copy requirement spec first for better layer caching
COPY --chown=app:app requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy app source
COPY --chown=app:app app /app/app

USER 10001:10001
EXPOSE 8000

# Gunicorn with Uvicorn workers (prod-ready)
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "2", "-b", "0.0.0.0:8000", "app.main:app"]
