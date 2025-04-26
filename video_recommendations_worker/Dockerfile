FROM --platform=linux/amd64 python:3.10.16-slim

RUN mkdir .config_app
COPY credentials.json /.config_app/credentials.json
RUN export GOOGLE_APPLICATION_CREDENTIALS="/.config_app/credentials.json"
ENV GOOGLE_APPLICATION_CREDENTIALS="/.config_app/credentials.json"

WORKDIR /app

# Install system and Python dependencies
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip

# Copy application code and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Run the worker
CMD ["python", "main.py"]
