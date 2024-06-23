# Use the official Python image as a base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev-compat \
    libmariadb-dev \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create and set the working directory
WORKDIR /src

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI application using Gunicorn with Uvicorn workers
CMD ["python", "app.py"]