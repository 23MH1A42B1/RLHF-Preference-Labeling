# RLHF Preference Labeling & Data Export Application Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including curl for health checks and postgres libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and seed assets
COPY data/ ./data/
COPY server/ ./server/
COPY downstream/ ./downstream/
COPY scripts/ ./scripts/

# Expose backend port
EXPOSE 8000

ENV PORT=8000
ENV HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1

# Run FastAPI backend via Uvicorn
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]

