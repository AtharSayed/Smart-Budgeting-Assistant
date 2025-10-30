# Dockerfile (root)
FROM python:3.12-slim

WORKDIR /code

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Expose ports (FastAPI:8000, Flask:5000)
EXPOSE 8000 5000

# Default command (overridden in compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]