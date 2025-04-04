FROM --platform=linux/amd64 python:3.10.16-slim

RUN mkdir .config_app
COPY credentials.json /.config_app/credentials.json
RUN export GOOGLE_APPLICATION_CREDENTIALS="/.config_app/credentials.json"
ENV GOOGLE_APPLICATION_CREDENTIALS="/.config_app/credentials.json"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set Python path
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose port 8000
EXPOSE 3020

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3020"]
