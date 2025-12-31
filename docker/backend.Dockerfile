FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    lilypond \
    && rm -rf /var/lib/apt/lists/*

# Copy and install the core package first
COPY reharmonizer-core /app/reharmonizer-core
RUN pip install --no-cache-dir -e /app/reharmonizer-core

# Copy backend requirements (without core package since we already installed it)
COPY backend/requirements.txt .

# Install backend dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend .

# Expose port
EXPOSE 8000

# Default command (can be overridden in docker-compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
