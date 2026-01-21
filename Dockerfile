# Pull base image
FROM python:3.13-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

# Set work directory
WORKDIR /app

EXPOSE 8000

# Copy the requirements file and install dependencies
COPY .env requirements.txt ./

# Install updates and dependencies in single image layer
RUN apt update && apt -y upgrade && \
    # install mandatory packages
    python3 -m pip install --no-cache-dir -r /app/requirements.txt

# Copy application code into the container
COPY src/ ./src

# Copy static files into the container
COPY static/ ./static

# Command to run the application with Uvicorn
CMD ["uvicorn", "src.api.v1.main:app", "--host", "0.0.0.0", "--port", "8000"]