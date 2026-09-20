FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for SQLite
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/app ./app
COPY backend/migrations ./migrations
COPY backend/policy.yaml .
COPY backend/registry.yaml .
COPY backend/taxonomy_slice.yaml .
COPY configs ./configs
COPY backend/artifacts/seed ./artifacts/seed

# Create artifacts directory
RUN mkdir -p /app/artifacts

# Set environment
ENV PYTHONPATH=/app
ENV APP_ENV=production

# Run as non-root
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]