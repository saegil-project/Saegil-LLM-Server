# Base image
FROM python:3.13-alpine

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 8000

# Environment variables
# Note: ELEVENLABS_API_KEY should be provided at runtime
ENV PYTHONUNBUFFERED=1

# Run FastAPI application
CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8000"]
