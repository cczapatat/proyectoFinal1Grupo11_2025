# Base image
FROM --platform=linux/amd64 python:3.9.6

RUN mkdir .config_app
COPY credentials.json /.config_app/credentials.json
RUN export GOOGLE_APPLICATION_CREDENTIALS="/.config_app/credentials.json"
ENV GOOGLE_APPLICATION_CREDENTIALS="/.config_app/credentials.json"

# Metadata
LABEL maintainer="jc.torresm1@uniandes.edu.co"

# Create and use a non-root user
RUN groupadd -r appuser
RUN useradd -r -m -g appuser appuser

# Switch to the non-root user
USER appuser

# Set the working directory
WORKDIR /app

# Copy application files
COPY ./src /app/src
COPY ./requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Set environment variables
ENV FLASK_APP=./src/main.py
ENV PYTHONUNBUFFERED=1

# Expose the desired port
EXPOSE 3000

CMD ["python", "src/main.py"]
