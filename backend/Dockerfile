# TandemHire Backend Dockerfile

FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements file from backend/
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend code (including /app folder)
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV DATABASE_URL=sqlite:///./dev.db
ENV UPLOAD_DIR=/tmp/tandemhire_uploads

# Create upload directory
RUN mkdir -p /tmp/tandemhire_uploads

# Expose backend port
EXPOSE 8000

# Run FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

