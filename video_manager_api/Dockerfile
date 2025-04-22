FROM --platform=linux/amd64 python:3.10.16-slim

# Set up working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up Google Cloud credentials
RUN mkdir /.config_app
COPY credentials.json /.config_app/credentials.json
ENV GOOGLE_APPLICATION_CREDENTIALS="/.config_app/credentials.json"

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose the port
EXPOSE 3021

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3021"]
